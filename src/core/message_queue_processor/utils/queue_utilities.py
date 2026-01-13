#!/usr/bin/env python3
"""
Queue Utilities for Message Queue Processing
============================================

Utility functions for queue operations and agent tracking.
"""

from typing import Any, Optional


class ActivityTracker:
    """Tracks agent activity for message delivery."""

    def __init__(self):
        self.active_agents = set()

    def mark_active(self, agent_id: str) -> None:
        """Mark an agent as active."""
        self.active_agents.add(agent_id)

    def mark_inactive(self, agent_id: str) -> None:
        """Mark an agent as inactive."""
        self.active_agents.discard(agent_id)

    def is_active(self, agent_id: str) -> bool:
        """Check if an agent is active."""
        return agent_id in self.active_agents


# Global activity tracker instance
_activity_tracker = ActivityTracker()


def safe_dequeue(queue: Any) -> Optional[Any]:
    """
    Safely dequeue an item from a queue.

    Args:
        queue: Queue object to dequeue from

    Returns:
        Dequeued item or None if queue is empty
    """
    try:
        return queue.get_nowait()
    except Exception:
        return None


def get_activity_tracker() -> ActivityTracker:
    """
    Get the global activity tracker instance.

    Returns:
        ActivityTracker instance
    """
    return _activity_tracker


def mark_agent_delivering(tracker, agent_id: str, queue_id: str) -> None:
    """
    Mark an agent as actively delivering messages.

    Args:
        tracker: Activity tracker instance
        agent_id: ID of the agent
        queue_id: Queue ID of the message being delivered
    """
    # Note: tracker parameter is for future use, currently using global tracker
    _activity_tracker.mark_active(agent_id)


def mark_agent_inactive(tracker, agent_id: str) -> None:
    """
    Mark an agent as inactive (not delivering).

    Args:
        tracker: Activity tracker instance
        agent_id: ID of the agent
    """
    # Note: tracker parameter is for future use, currently using global tracker
    _activity_tracker.mark_inactive(agent_id)