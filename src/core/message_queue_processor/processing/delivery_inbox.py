#!/usr/bin/env python3
"""
Delivery Inbox - Fallback Inbox Delivery
========================================

Backup path for inbox file-based delivery when PyAutoGUI fails.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def deliver_fallback_inbox(
    recipient: str,
    content: str,
    metadata: dict,
    sender: Optional[str] = None,
    priority_str: Optional[str] = None,
) -> bool:
    """
    Backup path: Inbox file-based delivery.

    Used when PyAutoGUI delivery fails (e.g., Cursor queue full).

    Args:
        recipient: Agent ID to deliver to
        content: Message content
        metadata: Message metadata
        sender: Sender identifier (preserved from message)
        priority_str: Priority string (preserved from message)

    Returns:
        True if inbox delivery successful, False otherwise
    """
    try:
        from ....utils.inbox_utility import create_inbox_message

        actual_sender = sender or metadata.get("sender", "SYSTEM")
        actual_priority = priority_str or metadata.get("priority", "normal")

        success = create_inbox_message(
            recipient=recipient,
            content=content,
            sender=actual_sender,
            priority=actual_priority,
        )

        if not success:
            logger.error(f"❌ Inbox delivery failed for {recipient}")
            return False

        logger.info(f"✅ Inbox delivery verified for {recipient}")
        return True
    except ImportError:
        logger.warning("Inbox utility not available")
        return False
    except Exception as e:
        logger.error(f"Inbox delivery error: {e}", exc_info=True)
        return False
