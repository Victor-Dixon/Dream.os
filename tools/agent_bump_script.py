#!/usr/bin/env python3
"""
Agent Bump Script
=================

Bumps agents to wake them up or unstall them.
Used by the Discord BumpAgentView.

Author: Agent-6 (Coordination & Communication Specialist)
"""

from typing import List, Dict
import logging
from src.services.messaging.discord_message_helpers import queue_message_for_agent_by_number

logger = logging.getLogger(__name__)

def bump_agents_by_number(agent_numbers: List[int]) -> Dict[str, bool]:
    """
    Bump specified agents by number.
    
    Args:
        agent_numbers: List of agent numbers to bump
        
    Returns:
        Dictionary mapping agent_id to success boolean
    """
    results = {}
    
    for agent_num in agent_numbers:
        agent_id = f"Agent-{agent_num}"
        try:
            logger.info(f"Bumping {agent_id}...")
            
            result = queue_message_for_agent_by_number(
                agent_number=agent_num,
                message="BUMP - Status Check",
                priority="urgent",
                sender="Captain Agent-4",
                wait_for_delivery=False
            )
            
            success = result.get("success", False)
            results[agent_id] = success
            
            if success:
                logger.info(f"✅ Successfully bumped {agent_id}")
            else:
                logger.warning(f"❌ Failed to bump {agent_id}: {result.get('message')}")
                
        except Exception as e:
            logger.error(f"Error bumping {agent_id}: {e}")
            results[agent_id] = False
            
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bump agents")
    parser.add_argument("agents", metavar="N", type=int, nargs="+", help="Agent numbers to bump")
    args = parser.parse_args()
    
    results = bump_agents_by_number(args.agents)
    print(results)
