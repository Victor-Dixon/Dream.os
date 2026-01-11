#!/usr/bin/env python3
"""
Messaging V3 API - Seamless Agent Integration
==============================================

Simple API for agents to send messages without CLI complexity.
"""

import logging
from typing import Optional, Dict, Any

from .delivery import send_message as _send_message
from .queue import MessageQueue
from .features import MessagingFeatures

logger = logging.getLogger(__name__)

# Global instances for convenience
_queue = MessageQueue()
_features = MessagingFeatures()


# ============================================================================
# SIMPLE AGENT API
# ============================================================================

def send_message(recipient: str, content: str, sender: str = "system") -> bool:
    """
    Send a message to another agent.

    Args:
        recipient: Agent ID (e.g., "Agent-1", "Agent-7")
        content: Message content
        sender: Your agent ID (e.g., "Agent-2")

    Returns:
        bool: True if delivered successfully

    Example:
        >>> from messaging_v3.api import send_message
        >>> send_message("Agent-1", "Hello from Agent-2!", sender="Agent-2")
    """
    return _send_message(recipient, content, sender)


def queue_message(recipient: str, content: str, sender: str = "system",
                 priority: str = "normal", category: str = "direct") -> str:
    """
    Queue a message for later delivery.

    Args:
        recipient: Agent ID
        content: Message content
        sender: Your agent ID
        priority: Message priority ("low", "normal", "high", "urgent")
        category: Message category

    Returns:
        str: Message ID

    Example:
        >>> from messaging_v3.api import queue_message
        >>> msg_id = queue_message("Agent-1", "Urgent task!", sender="Agent-2", priority="urgent")
    """
    from .message import Message
    message = Message(
        id=None,
        sender=sender,
        recipient=recipient,
        content=content,
        priority=priority,
        category=category
    )
    return _queue.enqueue(message)


# ============================================================================
# ADVANCED AGENT API
# ============================================================================

def send_a2a_coordination(from_agent: str, to_agent: str, content: str) -> bool:
    """
    Send A2A (Agent-to-Agent) coordination message.

    Args:
        from_agent: Your agent ID
        to_agent: Target agent ID
        content: Coordination content

    Returns:
        bool: Success status
    """
    return _features.send_a2a_coordination(from_agent, to_agent, content)


def broadcast_message(sender: str, content: str, priority: str = "normal") -> int:
    """
    Broadcast message to all agents.

    Args:
        sender: Your agent ID
        content: Broadcast content
        priority: Message priority

    Returns:
        int: Number of agents message was sent to
    """
    return _features.broadcast_message(sender, content, priority)


def get_agent_status(agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Get status of another agent.

    Args:
        agent_id: Agent to check

    Returns:
        dict: Agent status or None if not found
    """
    return _features.get_agent_status(agent_id)


def update_my_status(agent_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update your own status.

    Args:
        agent_id: Your agent ID
        updates: Status updates dict

    Returns:
        bool: Success status
    """
    return _features.update_agent_status(agent_id, updates)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_queue_status() -> Dict[str, Any]:
    """Get current message queue status."""
    return _features.get_queue_status()


def check_health() -> Dict[str, Any]:
    """Perform infrastructure health check."""
    return _features.perform_infrastructure_health_check()


def get_leaderboard() -> Dict[str, Any]:
    """Get agent performance leaderboard."""
    return _features.get_leaderboard()


# ============================================================================
# CONVENIENCE IMPORTS FOR AGENTS
# ============================================================================

__all__ = [
    # Basic messaging
    'send_message',
    'queue_message',

    # Advanced coordination
    'send_a2a_coordination',
    'broadcast_message',

    # Status management
    'get_agent_status',
    'update_my_status',

    # System utilities
    'get_queue_status',
    'check_health',
    'get_leaderboard',
]