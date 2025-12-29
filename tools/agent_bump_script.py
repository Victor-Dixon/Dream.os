"""
Tool to bump agents (send a 'bump' message) to wake them up or check status.
This is a utility script used by the Discord bot.
"""

import sys
import os
import argparse
from typing import List, Optional

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.messaging.discord_message_helpers import queue_message_for_agent_by_number

def bump_agent_by_number(agent_number: int, message: str = "BUMP - Check In") -> bool:
    """Bump a single agent by number."""
    try:
        queue_message_for_agent_by_number(agent_number, message)
        print(f"✅ Bumped Agent-{agent_number}")
        return True
    except Exception as e:
        print(f"❌ Failed to bump Agent-{agent_number}: {e}")
        return False

def bump_agents_by_number(agent_numbers: List[int], message: str = "BUMP - Check In") -> None:
    """Bump multiple agents by number."""
    print(f"🚀 Bumping {len(agent_numbers)} agents...")
    for agent_num in agent_numbers:
        bump_agent_by_number(agent_num, message)
    print("✨ Bump sequence complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bump agents to wake them up")
    parser.add_argument('agents', metavar='N', type=int, nargs='+', help='Agent numbers to bump (e.g., 1 2 5)')
    parser.add_argument('--message', '-m', type=str, default="BUMP - Check In", help='Message content')
    
    args = parser.parse_args()
    
    bump_agents_by_number(args.agents, args.message)
