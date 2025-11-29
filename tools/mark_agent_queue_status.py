#!/usr/bin/env python3
"""
Mark Agent Queue Status - CLI Tool
===================================

CLI tool to mark agents as having full or available Cursor queues.

Usage:
    python tools/mark_agent_queue_status.py --agent Agent-4 --status full
    python tools/mark_agent_queue_status.py --agent Agent-4 --status available
    python tools/mark_agent_queue_status.py --agent Agent-4 --check

Author: Agent-4 (Captain)
Date: 2025-11-27
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.agent_queue_status import AgentQueueStatus


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Mark agent Cursor queue as full or available",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mark Agent-4 as full
  python tools/mark_agent_queue_status.py --agent Agent-4 --status full
  
  # Mark Agent-4 as available
  python tools/mark_agent_queue_status.py --agent Agent-4 --status available
  
  # Check Agent-4 status
  python tools/mark_agent_queue_status.py --agent Agent-4 --check
  
  # Mark all agents as available
  python tools/mark_agent_queue_status.py --all --status available
        """
    )
    
    parser.add_argument(
        "--agent", "-a",
        help="Agent ID (e.g., Agent-4)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Apply to all agents (Agent-1 through Agent-8)"
    )
    
    parser.add_argument(
        "--status", "-s",
        choices=["full", "available"],
        help="Queue status: 'full' or 'available'"
    )
    
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Check current queue status (don't modify)"
    )
    
    parser.add_argument(
        "--reason", "-r",
        default="Manual marking",
        help="Reason for marking (default: 'Manual marking')"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.agent and not args.all:
        parser.error("Must specify --agent or --all")
    
    if args.check and args.status:
        parser.error("Cannot use --check with --status")
    
    if not args.check and not args.status:
        parser.error("Must specify --status or --check")
    
    # Get agent list
    if args.all:
        agents = [f"Agent-{i}" for i in range(1, 9)]
    else:
        agents = [args.agent]
    
    # Execute command
    if args.check:
        # Check status
        print(f"📊 Checking queue status for {len(agents)} agent(s)...\n")
        for agent_id in agents:
            is_full = AgentQueueStatus.is_full(agent_id)
            status_info = AgentQueueStatus.get_status(agent_id)
            
            if status_info:
                status_emoji = "🔴" if is_full else "🟢"
                print(f"{status_emoji} {agent_id}: {'FULL' if is_full else 'AVAILABLE'}")
                print(f"   Reason: {status_info.get('reason', 'N/A')}")
                print(f"   Marked at: {status_info.get('marked_at', 'N/A')}")
            else:
                print(f"⚪ {agent_id}: Status not set (defaults to available)")
            print()
    else:
        # Mark status
        action = "marking as FULL" if args.status == "full" else "marking as AVAILABLE"
        print(f"🔄 {action} for {len(agents)} agent(s)...\n")
        
        success_count = 0
        for agent_id in agents:
            if args.status == "full":
                success = AgentQueueStatus.mark_full(agent_id, args.reason)
            else:
                success = AgentQueueStatus.mark_available(agent_id)
            
            if success:
                success_count += 1
                emoji = "🔴" if args.status == "full" else "🟢"
                print(f"{emoji} {agent_id}: {args.status.upper()}")
            else:
                print(f"❌ {agent_id}: Failed to update")
        
        print(f"\n✅ Successfully updated {success_count}/{len(agents)} agent(s)")
        
        if args.status == "full":
            print("\n💡 Tip: Messages to these agents will skip PyAutoGUI and go directly to inbox")
        else:
            print("\n💡 Tip: Messages to these agents will try PyAutoGUI delivery first")


if __name__ == "__main__":
    main()

