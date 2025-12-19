#!/usr/bin/env python3
"""
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
