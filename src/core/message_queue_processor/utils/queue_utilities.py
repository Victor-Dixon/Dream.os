#!/usr/bin/env python3
"""
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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


<<<<<<< HEAD
def mark_agent_delivering(tracker, agent_id: str, queue_id: str) -> None:
=======
def mark_agent_delivering(agent_id: str) -> None:
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    """
    Mark an agent as actively delivering messages.

    Args:
<<<<<<< HEAD
        tracker: Activity tracker instance
        agent_id: ID of the agent
        queue_id: Queue ID of the message being delivered
    """
    # Note: tracker parameter is for future use, currently using global tracker
    _activity_tracker.mark_active(agent_id)


def mark_agent_inactive(tracker, agent_id: str) -> None:
=======
        agent_id: ID of the agent
    """
    _activity_tracker.mark_active(agent_id)


def mark_agent_inactive(agent_id: str) -> None:
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    """
    Mark an agent as inactive (not delivering).

    Args:
<<<<<<< HEAD
        tracker: Activity tracker instance
        agent_id: ID of the agent
    """
    # Note: tracker parameter is for future use, currently using global tracker
    _activity_tracker.mark_inactive(agent_id)
=======
<!-- SSOT Domain: core -->

Queue Utilities - Helper Functions for Message Queue Processing
================================================================

Utility functions for message queue processing operations.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def safe_dequeue(queue: Any, batch_size: int) -> list[Any]:
    """
    Safely dequeue messages with error isolation.
    
    Args:
        queue: MessageQueue instance
        batch_size: Number of messages to dequeue
        
    Returns:
        List of queue entries (empty list on error)
    """
    try:
        return queue.dequeue(batch_size=batch_size)
    except Exception as e:
        logger.error(f"Dequeue error: {e}", exc_info=True)
        return []


def get_activity_tracker() -> Optional[Any]:
    """
    Get activity tracker instance.
    
    Returns:
        Activity tracker instance or None if unavailable
    """
    try:
        from ....core.agent_activity_tracker import get_activity_tracker
        return get_activity_tracker()
    except Exception:
        return None  # Non-critical if tracker unavailable


def mark_agent_delivering(
    tracker: Optional[Any],
    recipient: str,
    queue_id: str,
) -> None:
    """
    Mark agent as delivering message.
    
    Args:
        tracker: Activity tracker instance
        recipient: Recipient identifier
        queue_id: Queue entry ID
    """
    if tracker and recipient and recipient.startswith("Agent-"):
        try:
            tracker.mark_delivering(recipient, queue_id)
        except Exception:
            pass  # Non-critical tracking failure


def mark_agent_inactive(
    tracker: Optional[Any],
    recipient: str,
) -> None:
    """
    Mark agent as inactive.
    
    Args:
        tracker: Activity tracker instance
        recipient: Recipient identifier
    """
    if tracker and recipient and recipient.startswith("Agent-"):
        try:
            tracker.mark_inactive(recipient)
        except Exception:
            pass  # Non-critical tracking failure
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        agent_id: ID of the agent
    """
    _activity_tracker.mark_inactive(agent_id)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
