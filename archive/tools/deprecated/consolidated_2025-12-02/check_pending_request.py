#!/usr/bin/env python3
"""
Check Pending Multi-Agent Request - CLI Tool
============================================

Check if an agent has a pending multi-agent request and display the message.

Usage:
    python tools/check_pending_request.py --agent Agent-4
    python tools/check_pending_request.py --all

Author: Agent-4 (Captain)
Date: 2025-11-27
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.multi_agent_request_validator import get_multi_agent_validator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Check for pending multi-agent requests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check specific agent
  python tools/check_pending_request.py --agent Agent-4
  
  # Check all agents
  python tools/check_pending_request.py --all
        """
    )
    
    parser.add_argument(
        "--agent", "-a",
        help="Agent ID to check (e.g., Agent-4)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Check all agents (Agent-1 through Agent-8)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.agent and not args.all:
        parser.error("Must specify --agent or --all")
    
    # Get agent list
    if args.all:
        agents = [f"Agent-{i}" for i in range(1, 9)]
    else:
        agents = [args.agent]
    
    # Check each agent
    validator = get_multi_agent_validator()
    
    print(f"🔍 Checking pending requests for {len(agents)} agent(s)...\n")
    
    pending_count = 0
    for agent_id in agents:
        pending_message = validator.get_pending_request_message(agent_id)
        
        if pending_message:
            pending_count += 1
            print(f"🔴 {agent_id}: HAS PENDING REQUEST")
            print("=" * 60)
            print(pending_message)
            print("=" * 60)
            print()
        else:
            print(f"🟢 {agent_id}: No pending requests")
            print()
    
    print(f"\n📊 Summary: {pending_count}/{len(agents)} agent(s) have pending requests")
    
    if pending_count > 0:
        print("\n💡 Tip: Agents with pending requests cannot send messages until they respond")
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())

