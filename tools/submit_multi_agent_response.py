#!/usr/bin/env python3
"""
Submit Multi-Agent Response - CLI Tool
======================================

Submit response to a pending multi-agent request.

Usage:
    python tools/submit_multi_agent_response.py --agent Agent-4 --collector collector_123 --response "My response here"
    python tools/submit_multi_agent_response.py --agent Agent-4 --response "My response"  # Auto-detect collector

Author: Agent-4 (Captain)
Date: 2025-11-27
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.multi_agent_responder import get_multi_agent_responder
from src.core.multi_agent_request_validator import get_multi_agent_validator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Submit response to multi-agent request",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Submit response with collector ID
  python tools/submit_multi_agent_response.py --agent Agent-4 --collector collector_123 --response "Working on it"
  
  # Auto-detect collector from pending request
  python tools/submit_multi_agent_response.py --agent Agent-4 --response "Status: 50% complete"
        """
    )
    
    parser.add_argument(
        "--agent", "-a",
        required=True,
        help="Agent ID responding (e.g., Agent-4)"
    )
    
    parser.add_argument(
        "--collector", "-c",
        help="Collector ID (optional - will auto-detect if not provided)"
    )
    
    parser.add_argument(
        "--response", "-r",
        required=True,
        help="Response content"
    )
    
    args = parser.parse_args()
    
    responder = get_multi_agent_responder()
    validator = get_multi_agent_validator()
    
    # Get collector ID
    collector_id = args.collector
    
    if not collector_id:
        # Auto-detect from pending request
        pending = validator.check_pending_request(args.agent)
        if not pending:
            print(f"❌ No pending request found for {args.agent}")
            print("💡 Use --collector to specify collector ID manually")
            return 1
        
        collector_id = pending["collector_id"]
        print(f"✅ Auto-detected collector: {collector_id}")
    
    # Submit response
    print(f"📤 Submitting response from {args.agent}...")
    print(f"📋 Collector ID: {collector_id}")
    print(f"💬 Response: {args.response[:100]}...")
    print()
    
    success = responder.submit_response(
        collector_id=collector_id,
        agent_id=args.agent,
        response=args.response
    )
    
    if success:
        print("✅ Response submitted successfully!")
        print("💡 Your response will be combined with other agents' responses")
        print("💡 Combined message will be sent to the request sender")
        print()
        print("🐝 WE. ARE. SWARM. ⚡🔥")
        return 0
    else:
        print("❌ Failed to submit response")
        print("💡 Check collector ID and ensure request is still pending")
        return 1


if __name__ == "__main__":
    sys.exit(main())

