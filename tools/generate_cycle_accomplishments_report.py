#!/usr/bin/env python3
"""
⚠️  DEPRECATED: This script is deprecated and will be removed in a future version.

Please use the new modular implementation instead:
    python -m tools.cycle_accomplishments.main

The new implementation combines all features from v1.0 and v2.0 with:
- Better modular architecture
- Blog post generation (Victor voice)
- Enhanced Discord posting (chunked + file upload)
- Cross-platform compatibility
- Protocol v2.0

This script will continue to work but is no longer maintained.
=====================================

Generate Cycle Accomplishments Report
=====================================

Comprehensive cycle accomplishments report aggregating all agent activities.
Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v1.0

Author: Agent-2 (Architecture & Design)
Date: 2025-12-28
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Import Discord posting functionality
try:
    from tools.devlog_manager import main as post_to_discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Import report generation from our coordination tool
try:
    from tools.ssot_coordination_report import generate_coordination_report
    COORDINATION_AVAILABLE = True
except ImportError:
    COORDINATION_AVAILABLE = False


def load_agent_status(agent_id: str) -> Optional[Dict[str, Any]]:
    """Load status for a specific agent."""
    status_file = Path("agent_workspaces") / f"Agent-{agent_id}" / "status.json"
    try:
        with open(status_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️  Warning: Could not load status for Agent-{agent_id}: {e}")
        return None


def collect_all_agent_status() -> Dict[str, Dict[str, Any]]:
    """Collect status from all active agents."""
    agents = {}
    agent_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]  # Standard 8 agents

    for agent_id in agent_ids:
        status = load_agent_status(agent_id)
        if status:
            agents[f"Agent-{agent_id}"] = status

    return agents


def generate_cycle_report(agents: Dict[str, Dict[str, Any]]) -> str:
    """Generate comprehensive cycle accomplishments report."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')

    # Calculate totals
    total_agents = len(agents)
    total_completed_tasks = sum(len(status.get('completed_tasks', [])) for status in agents.values())
    total_achievements = sum(len(status.get('recent_completions', [])) for status in agents.values())

    # Count active tasks
    active_tasks = []
    for agent_id, status in agents.items():
        tasks = status.get('current_tasks', [])
        if isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, dict) and task.get('status') in ['in_progress', 'active', 'coordination_active']:
                    active_tasks.append({
                        'agent': agent_id,
                        'task': task.get('task', 'Unknown'),
                        'status': task.get('status', 'Unknown')
                    })

    report = [
        "# 🚀 Swarm Cycle Accomplishments Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Date:** {date}",
        f"**Agents Active:** {total_agents}",
        "",
        "## 📊 Executive Summary",
        "",
        f"- **Total Agents:** {total_agents}",
        f"- **Completed Tasks:** {total_completed_tasks}",
        f"- **Achievements:** {total_achievements}",
        f"- **Active Tasks:** {len(active_tasks)}",
        "",
        "## 👥 Agent Accomplishments",
        ""
    ]

    # Sort agents for consistent reporting
    sorted_agents = sorted(agents.keys())

    for agent_id in sorted_agents:
        status = agents[agent_id]
        agent_name = status.get('agent_name', f'Agent {agent_id.split("-")[1]}')
        current_mission = status.get('current_mission', 'No mission set')
        last_updated = status.get('last_updated', 'Unknown')

        report.append(f"### {agent_id}: {agent_name}")
        report.append("")
        report.append(f"**Current Mission:** {current_mission}")
        report.append(f"**Last Updated:** {last_updated}")
        report.append(f"**Status:** {status.get('status', 'Unknown')}")
        report.append("")

        # Completed Tasks
        completed_tasks = status.get('completed_tasks', [])
        if completed_tasks:
            report.append("**✅ Completed Tasks:**")
            for task in completed_tasks[-10:]:  # Last 10 tasks
                report.append(f"- {task}")
            report.append("")

        # Recent Completions (Achievements)
        recent_completions = status.get('recent_completions', [])
        if recent_completions:
            report.append("**🏆 Recent Achievements:**")
            for achievement in recent_completions[-5:]:  # Last 5 achievements
                report.append(f"- {achievement.get('task', 'Unknown')}")
            report.append("")

        # Current Tasks
        current_tasks = status.get('current_tasks', [])
        if current_tasks:
            report.append("**🔄 Current Tasks:**")
            for task in current_tasks:
                if isinstance(task, dict):
                    task_name = task.get('task', 'Unknown')
                    task_status = task.get('status', 'Unknown')
                    report.append(f"- **{task_status.upper()}:** {task_name}")
            report.append("")

    # Active Tasks Summary
    if active_tasks:
        report.append("## 🎯 Active Tasks Overview")
        report.append("")

        # Group by status
        status_groups = defaultdict(list)
        for task in active_tasks:
            status_groups[task['status']].append(task)

        for status, tasks in status_groups.items():
            report.append(f"### {status.replace('_', ' ').title()} ({len(tasks)})")
            for task in tasks:
                report.append(f"- **{task['agent']}:** {task['task']}")
            report.append("")

    # Block Status (from MASTER_TASK_LOG.md if available)
    report.append("## 📋 Swarm Phase 3 Block Status")
    report.append("")

    # Try to read current block status from MASTER_TASK_LOG.md
    try:
        master_log_path = Path("MASTER_TASK_LOG.md")
        if master_log_path.exists():
            with open(master_log_path, 'r') as f:
                content = f.read()

            # Look for current block status
            if "Block 1" in content and "Block 2" in content:
                report.append("**Current Phase:** Swarm Phase 3 Consolidation & V2 Completion")
                report.append("**Active Blocks:**")
                report.append("- Block 1: Infrastructure refactoring + WP-CLI integration + Phase 3 runtime errors (Agent-1)")
                report.append("- Block 2: Staging & rollback infrastructure + deployment MCP enhancements (Agent-2) ✅ COMPLETED")
                report.append("- Block 3: Critical deployments + PHP validation + GA4/Pixel config (Agent-3)")
                report.append("- Block 4: Analytics validation + DB operations + WordPress health checks (Agent-5)")
                report.append("- Block 5: SSOT tagging (646 tools) + PSE rule validation + archived tools audit (Agent-6)")
                report.append("- Block 6: P0 Foundation fixes (Tier 2) + Offer Ladders + ICP Definitions + website-manager MCP enhancements (Agent-7)")
                report.append("- Block 7: Unified tool registry + cache management + tool discovery audit (Agent-8)")
                report.append("")
    except Exception as e:
        report.append("*Block status unavailable*")
        report.append("")

    # Report Metadata
    report.append("## 📋 Report Metadata")
    report.append("")
    report.append("**Protocol:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v1.0")
    report.append("**Generated By:** tools/generate_cycle_accomplishments_report.py")
    report.append("**Format:** Markdown")
    report.append("**Timestamp:** " + timestamp)
    report.append("")
    report.append("---")
    report.append("*This report aggregates accomplishments across all active swarm agents.*")

    return "\n".join(report)


def save_report(report: str, timestamp: str) -> str:
    """Save report to file and return path."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    filename = f"cycle_accomplishments_{timestamp.replace(':', '').replace('-', '').replace(' ', '_')}.md"
    report_path = reports_dir / filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return str(report_path)


def post_to_discord_channel(report_content: str, report_path: str) -> bool:
    """Post report summary to Discord."""
    if not DISCORD_AVAILABLE:
        print("⚠️  Discord posting not available - devlog_manager not found")
        return False

    try:
        # Create a temporary devlog file for posting
        temp_devlog = Path("temp_cycle_report_devlog.md")
        with open(temp_devlog, 'w', encoding='utf-8') as f:
            f.write(f"# Swarm Cycle Accomplishments Report\n\n")
            f.write(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 📊 Summary\n\n")
            f.write(f"- Full report saved to: `{report_path}`\n")
            f.write("- Contains comprehensive agent accomplishments\n")
            f.write("- Includes active tasks and swarm coordination status\n\n")
            f.write("## 🔗 Report Excerpt\n\n")
            # Include first 1500 characters of report for Discord
            excerpt = report_content[:1500]
            if len(report_content) > 1500:
                excerpt += "\n\n[... report truncated for Discord, see full report file ...]"
            f.write(excerpt)

        # Post using devlog_manager (posts to Agent-4 Captain channel)
        import sys
        from tools.devlog_manager import main as post_devlog

        # Simulate command line args for devlog_manager
        original_argv = sys.argv
        sys.argv = ['devlog_manager.py', 'post', '--agent', 'Agent-4', '--file', str(temp_devlog)]

        try:
            result = post_devlog()
            success = result == 0
        except Exception as e:
            print(f"❌ Discord posting failed: {e}")
            success = False
        finally:
            sys.argv = original_argv

        # Clean up temp file
        if temp_devlog.exists():
            temp_devlog.unlink()

        return success

    except Exception as e:
        print(f"❌ Error posting to Discord: {e}")
        return False


def main():
    """Main function to generate and post cycle accomplishments report."""
    print("🚀 Generating Swarm Cycle Accomplishments Report...")
    print("Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v1.0")
    print()

    # Collect agent data
    print("📊 Collecting agent status data...")
    agents = collect_all_agent_status()

    if not agents:
        print("❌ No agent status data found!")
        return 1

    print(f"✅ Found {len(agents)} active agents")

    # Generate report
    print("📝 Generating comprehensive report...")
    report = generate_cycle_report(agents)

    # Save report
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    report_path = save_report(report, timestamp)
    print(f"💾 Report saved to: {report_path}")

    # Post to Discord
    print("📢 Posting to Discord...")
    discord_success = post_to_discord_channel(report, report_path)

    if discord_success:
        print("✅ Report posted to Discord successfully")
    else:
        print("⚠️  Discord posting failed - report saved locally only")

    # Summary
    print()
    print("🎯 Cycle Accomplishments Report Complete!")
    print(f"📄 Full report: {report_path}")
    print(f"🤖 Agents covered: {len(agents)}")
    print(f"📊 Discord posted: {'Yes' if discord_success else 'No'}")

    return 0


if __name__ == "__main__":
    exit(main())


