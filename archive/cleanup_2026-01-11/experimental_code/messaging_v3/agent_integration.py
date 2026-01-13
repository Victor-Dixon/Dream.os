#!/usr/bin/env python3
"""
Agent Integration Helper - Make Messaging V3 Seamless
======================================================

Drop-in replacement for agent messaging. Just import and use!
"""

import os
import sys
from pathlib import Path

# Auto-setup imports for agents
_current_dir = Path(__file__).parent
_parent_dir = _current_dir.parent
sys.path.insert(0, str(_current_dir))
sys.path.insert(0, str(_parent_dir))

# Import everything agents need
from messaging_v3.api import (
    send_message,
    queue_message,
    send_a2a_coordination,
    broadcast_message,
    get_agent_status,
    update_my_status,
    get_queue_status,
    check_health,
    get_leaderboard,
)

# ============================================================================
# AGENT CONVENIENCE FUNCTIONS
# ============================================================================

def send_to_agent(recipient: str, message: str, agent_id: str = None) -> bool:
    """
    Send message to another agent (auto-detects sender).

    Args:
        recipient: Target agent (e.g., "Agent-1")
        message: Message content
        agent_id: Your agent ID (auto-detected if None)

    Returns:
        bool: Success status
    """
    if agent_id is None:
        agent_id = _detect_current_agent()
    return send_message(recipient, message, agent_id)


def coordinate_with_agent(recipient: str, task_description: str, agent_id: str = None) -> bool:
    """
    Send A2A coordination request to another agent.

    Args:
        recipient: Agent to coordinate with
        task_description: What you want to coordinate
        agent_id: Your agent ID (auto-detected if None)

    Returns:
        bool: Success status
    """
    if agent_id is None:
        agent_id = _detect_current_agent()
    return send_a2a_coordination(agent_id, recipient, task_description)


def update_status(updates: dict, agent_id: str = None) -> bool:
    """
    Update your agent status.

    Args:
        updates: Status updates dict
        agent_id: Your agent ID (auto-detected if None)

    Returns:
        bool: Success status
    """
    if agent_id is None:
        agent_id = _detect_current_agent()
    return update_my_status(agent_id, updates)


def broadcast_to_swarm(message: str, priority: str = "normal", agent_id: str = None) -> int:
    """
    Broadcast message to entire swarm.

    Args:
        message: Broadcast content
        priority: Message priority
        agent_id: Your agent ID (auto-detected if None)

    Returns:
        int: Number of agents reached
    """
    if agent_id is None:
        agent_id = _detect_current_agent()
    return broadcast_message(agent_id, message, priority)


# ============================================================================
# AUTO-DETECTION HELPERS
# ============================================================================

def _detect_current_agent() -> str:
    """
    Auto-detect which agent is running this code.

    Returns:
        str: Agent ID (e.g., "Agent-7")
    """
    # Try environment variable first
    agent_id = os.getenv('AGENT_ID')
    if agent_id:
        return agent_id

    # Try to detect from current working directory
    cwd = Path.cwd()
    for part in cwd.parts:
        if part.startswith('Agent-'):
            return part

    # Try to detect from process name or parent directory
    try:
        current_file = Path(__file__)
        for parent in current_file.parents:
            if parent.name.startswith('Agent-'):
                return parent.name
    except:
        pass

    # Default fallback
    return "Unknown-Agent"


# ============================================================================
# QUICK STATUS CHECKS
# ============================================================================

def am_i_active(agent_id: str = None) -> bool:
    """Check if your agent is marked as active."""
    if agent_id is None:
        agent_id = _detect_current_agent()
    status = get_agent_status(agent_id)
    return status and status.get('status') == 'ACTIVE_AGENT_MODE'


def get_my_status(agent_id: str = None) -> dict:
    """Get your current agent status."""
    if agent_id is None:
        agent_id = _detect_current_agent()
    return get_agent_status(agent_id) or {}


# ============================================================================
# EXAMPLES FOR AGENTS
# ============================================================================

AGENT_USAGE_EXAMPLES = """
# Agent Integration Examples
# ==========================

# Basic messaging
from messaging_v3.agent_integration import send_to_agent, coordinate_with_agent

# Send a simple message
send_to_agent("Agent-1", "Task completed successfully!")

# Coordinate with another agent
coordinate_with_agent("Agent-2", "Let's work on the database optimization together")

# Update your status
from messaging_v3.agent_integration import update_status
update_status({"current_task": "database_optimization", "progress": "75%"})

# Broadcast to entire swarm
from messaging_v3.agent_integration import broadcast_to_swarm
broadcast_to_swarm("System update completed - all agents please verify", priority="high")

# Check system health
from messaging_v3.agent_integration import check_health
health = check_health()
if health.get('overall_status') != 'healthy':
    print("System health issues detected!")

# Get swarm leaderboard
from messaging_v3.agent_integration import get_leaderboard
leaderboard = get_leaderboard()
print(f"Active agents: {leaderboard.get('active_agents', 0)}/8")
"""


if __name__ == "__main__":
    # Show usage examples when run directly
    print("🐝 Messaging V3 - Agent Integration")
    print("=" * 40)
    print()
    print("Current Agent:", _detect_current_agent())
    print("Agent Active:", am_i_active())
    print()
    print("Usage Examples:")
    print(AGENT_USAGE_EXAMPLES)