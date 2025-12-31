#!/usr/bin/env python3
"""
Cycle Accomplishments Report Generator - Main Entrypoint
=========================================================

Modular implementation combining best features from v1.0 and v2.0.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
Protocol Status: ACTIVE
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-30
V2 Compliant: Yes

Purpose:
- Collects agent status from all agent workspaces (Agent-1 through Agent-8)
- Generates comprehensive markdown reports with accomplishments, tasks, and achievements
- Generates Victor-voiced blog posts for autoblogger integration
- Posts to Discord with chunked messages and file uploads (Agent-4 channel)

Usage:
    python -m tools.cycle_accomplishments.main [--no-blog] [--no-discord] [--no-details] [--no-file]

Protocol Documentation:
    docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md

<!-- SSOT Domain: tools -->
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Import our modules
from tools.cycle_accomplishments.data_collector import (
    collect_all_agent_status,
    calculate_totals
)
from tools.cycle_accomplishments.report_generator import (
    generate_cycle_report,
    save_report
)
from tools.cycle_accomplishments.blog_generator import (
    generate_narrative_blog_content,
    save_blog_post
)
from tools.cycle_accomplishments.discord_poster import (
    post_to_discord,
    DISCORD_AVAILABLE
)


def main(args: Optional[argparse.Namespace] = None) -> int:
    """
    Main function to generate and post cycle accomplishments report.
    
    Args:
        args: Command line arguments (if None, parses from sys.argv)
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Parse arguments
    if args is None:
        parser = argparse.ArgumentParser(
            description="Generate comprehensive cycle accomplishments report",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Generate report, blog post, and post to Discord (default)
  python -m tools.cycle_accomplishments.main
  
  # Generate report only (no blog, no Discord)
  python -m tools.cycle_accomplishments.main --no-blog --no-discord
  
  # Generate report and blog, but skip Discord
  python -m tools.cycle_accomplishments.main --no-discord
  
  # Post to Discord but skip per-agent details
  python -m tools.cycle_accomplishments.main --no-details
            """
        )
        parser.add_argument(
            '--no-blog',
            action='store_true',
            help='Skip blog post generation'
        )
        parser.add_argument(
            '--no-discord',
            action='store_true',
            help='Skip Discord posting'
        )
        parser.add_argument(
            '--no-details',
            action='store_true',
            help='Skip per-agent details in Discord (summary and file only)'
        )
        parser.add_argument(
            '--no-file',
            action='store_true',
            help='Skip file upload to Discord (summary and details only)'
        )
        parser.add_argument(
            '--workspace-root',
            type=str,
            help='Root workspace path (defaults to current directory)'
        )
        parser.add_argument(
            '--agent-id',
            type=str,
            default='Agent-4',
            help='Target Discord agent channel (default: Agent-4)'
        )
        args = parser.parse_args()
    
    # Determine workspace root
    if args.workspace_root:
        workspace_root = Path(args.workspace_root).resolve()
    else:
        workspace_root = Path.cwd()
    
    print("🚀 Generating Swarm Cycle Accomplishments Report...")
    print("Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0")
    print(f"Workspace: {workspace_root}")
    print()
    
    # Collect agent data
    print("📊 Collecting agent status data...")
    agents = collect_all_agent_status(workspace_root=workspace_root)
    
    if not agents:
        print("❌ No agent status data found!")
        return 1
    
    print(f"✅ Found {len(agents)} active agents")
    
    # Calculate totals
    totals = calculate_totals(agents)
    print(f"📈 Totals: {totals['total_completed_tasks']} tasks, {totals['total_achievements']} achievements")
    
    # Generate report
    print("📝 Generating comprehensive report...")
    report_content = generate_cycle_report(agents, totals, workspace_root=workspace_root)
    
    # Save report
    report_path = save_report(report_content, workspace_root=workspace_root)
    print(f"💾 Report saved to: {report_path}")
    
    # Generate blog post (if requested)
    blog_path = None
    if not args.no_blog:
        print("✍️  Generating blog post (Victor voice)...")
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Convert agents dict to list for blog generator
        agents_data = list(agents.values())
        
        blog_content = generate_narrative_blog_content(
            agents_data,
            totals['total_completed_tasks'],
            totals['total_achievements'],
            totals['total_agents'],
            date_str,
            workspace_root=workspace_root
        )
        
        blog_path = save_blog_post(
            blog_content,
            date_str,
            totals['total_agents'],
            totals['total_completed_tasks'],
            workspace_root=workspace_root
        )
        print(f"📝 Blog post saved to: {blog_path}")
    
    # Post to Discord (if requested)
    discord_success = False
    if not args.no_discord:
        if not DISCORD_AVAILABLE:
            print("⚠️  Discord posting not available - DiscordRouterPoster not found")
        else:
            print("📢 Posting to Discord...")
            date_str = datetime.now().strftime('%Y-%m-%d')
            agents_data = list(agents.values())
            
            discord_success = post_to_discord(
                agents_data,
                date_str,
                totals['total_agents'],
                totals['total_completed_tasks'],
                totals['total_achievements'],
                report_path,
                agent_id=args.agent_id,
                include_details=not args.no_details,
                include_file=not args.no_file
            )
            
            if discord_success:
                print("✅ Report posted to Discord successfully")
            else:
                print("⚠️  Discord posting failed - report saved locally only")
    
    # Summary
    print()
    print("🎯 Cycle Accomplishments Report Complete!")
    print(f"📄 Full report: {report_path}")
    if blog_path:
        print(f"📝 Blog post: {blog_path}")
    print(f"🤖 Agents covered: {totals['total_agents']}")
    print(f"📊 Discord posted: {'Yes' if discord_success else 'No' if not args.no_discord else 'Skipped'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

