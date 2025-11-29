#!/usr/bin/env python3
"""
Send Multi-Agent Request - CLI Tool
===================================

Send a message to multiple agents and collect their responses into one combined message.

This is JET FUEL for swarm coordination - powers autonomous multi-agent coordination!

Usage:
    python tools/send_multi_agent_request.py --agents Agent-1,Agent-2,Agent-3 --message "What's your status?"
    python tools/send_multi_agent_request.py --all --message "Team status update" --timeout 600

Author: Agent-4 (Captain) - Autonomous Implementation
Date: 2025-11-27
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import MessageCoordinator
from src.core.messaging_models_core import UnifiedMessagePriority


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Send multi-agent request (JET FUEL for swarm coordination)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Request from specific agents
  python tools/send_multi_agent_request.py --agents Agent-1,Agent-2,Agent-3 --message "Status?"
  
  # Request from all agents
  python tools/send_multi_agent_request.py --all --message "Team update"
  
  # With custom timeout
  python tools/send_multi_agent_request.py --all --message "Status?" --timeout 600
  
  # Wait for all responses
  python tools/send_multi_agent_request.py --all --message "Ready?" --wait-for-all
        """
    )
    
    parser.add_argument(
        "--agents", "-a",
        help="Comma-separated list of agent IDs (e.g., Agent-1,Agent-2,Agent-3)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Send to all agents (Agent-1 through Agent-8)"
    )
    
    parser.add_argument(
        "--message", "-m",
        required=True,
        help="Message content to send"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Timeout in seconds (default: 300 = 5 minutes)"
    )
    
    parser.add_argument(
        "--wait-for-all",
        action="store_true",
        help="Wait for all agents to respond (default: send on timeout)"
    )
    
    parser.add_argument(
        "--priority", "-p",
        choices=["regular", "urgent"],
        default="regular",
        help="Message priority (default: regular)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.agents and not args.all:
        parser.error("Must specify --agents or --all")
    
    # Get recipient list
    if args.all:
        recipients = [f"Agent-{i}" for i in range(1, 9)]
    else:
        recipients = [agent.strip() for agent in args.agents.split(",")]
    
    # Validate agent IDs
    valid_recipients = []
    for agent in recipients:
        if agent.startswith("Agent-") and len(agent) >= 7:
            valid_recipients.append(agent)
        else:
            print(f"⚠️  Invalid agent ID: {agent}")
    
    if not valid_recipients:
        print("❌ No valid agents specified")
        return 1
    
    # Get priority
    priority = UnifiedMessagePriority.URGENT if args.priority == "urgent" else UnifiedMessagePriority.REGULAR
    
    # Send multi-agent request
    print(f"🚀 Sending multi-agent request to {len(valid_recipients)} agent(s)...")
    print(f"📋 Message: {args.message[:100]}...")
    print(f"⏱️  Timeout: {args.timeout} seconds")
    print(f"⏳ Wait for all: {args.wait_for_all}")
    print()
    
    collector_id = MessageCoordinator.send_multi_agent_request(
        recipients=valid_recipients,
        message=args.message,
        sender="CAPTAIN",
        priority=priority,
        timeout_seconds=args.timeout,
        wait_for_all=args.wait_for_all
    )
    
    if collector_id:
        print(f"✅ Multi-agent request created!")
        print(f"📊 Collector ID: {collector_id}")
        print(f"👥 Recipients: {', '.join(valid_recipients)}")
        print()
        print("💡 Responses will be collected and combined into one message")
        print("💡 Combined message will be delivered when all agents respond (or timeout)")
        print()
        print("🐝 WE. ARE. SWARM. ⚡🔥")
        print("🚀 JET FUEL ACTIVATED - POWERING SWARM TOWARDS AGI!")
        return 0
    else:
        print("❌ Failed to create multi-agent request")
        return 1


if __name__ == "__main__":
    sys.exit(main())

