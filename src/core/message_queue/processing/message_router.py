#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Message Router - Route Message Delivery
=======================================

Routes message delivery with fallback logic (PyAutoGUI primary, inbox backup).
"""

import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


def route_message_delivery(
    recipient: str,
    content: str,
    metadata: dict,
    message_type_str: Optional[str],
    sender: str,
    priority_str: str,
    tags_list: list,
    deliver_via_core: Callable[[str, str, dict, Optional[str], str, str, list], bool],
    deliver_fallback_inbox: Callable[[str, str, dict, Optional[str], str], bool],
) -> bool:
    """
    Route message delivery with fallback logic.

    Primary: PyAutoGUI delivery via messaging core
    Backup: Inbox fallback when PyAutoGUI fails

    Args:
        recipient: Agent ID to deliver to
        content: Message content
        metadata: Message metadata
        message_type_str: Message type string
        sender: Sender identifier
        priority_str: Priority string
        tags_list: Tags list
        deliver_via_core: Function to deliver via messaging core
        deliver_fallback_inbox: Function to deliver via inbox fallback

    Returns:
        True if delivery successful, False otherwise
    """
    try:
        metadata = metadata or {}

        # CRITICAL: Check use_pyautogui flag from metadata
        # If explicitly set to False, skip PyAutoGUI and use inbox only
        # Default to True for backward compatibility
        use_pyautogui = metadata.get("use_pyautogui", True)

        if not use_pyautogui:
            logger.info(
                f"use_pyautogui=False in metadata for {recipient}, using inbox delivery"
            )
            return deliver_fallback_inbox(recipient, content, metadata, sender, priority_str)

        # Check if queue is full (skip PyAutoGUI if so)
        try:
            from ....utils.agent_queue_status import AgentQueueStatus
            queue_status = AgentQueueStatus()
            if queue_status.is_queue_full(recipient):
                logger.warning(
                    f"Queue full for {recipient}, skipping PyAutoGUI, using inbox"
                )
                return deliver_fallback_inbox(recipient, content, metadata, sender, priority_str)
        except ImportError:
            # Queue status utility not available, proceed normally
            pass
        except Exception as e:
            logger.debug(f"Error checking queue status: {e}")
            # Continue with normal flow

        # PRIMARY: Try PyAutoGUI delivery first
        success = deliver_via_core(
            recipient, content, metadata, message_type_str, sender, priority_str, tags_list or []
        )
        if success:
            return True

        # BACKUP: Fallback to inbox when PyAutoGUI fails
        # (e.g., when Cursor queue is full with pending prompts)
        logger.warning(
            f"PyAutoGUI delivery failed for {recipient}, using inbox fallback"
        )
        return deliver_fallback_inbox(recipient, content, metadata, sender, priority_str)
    except Exception as e:
        logger.error(f"Delivery routing error: {e}")
        # Last resort: try inbox fallback
        try:
            return deliver_fallback_inbox(recipient, content, metadata or {}, sender, priority_str)
        except Exception as fallback_error:
            logger.error(f"Inbox fallback also failed: {fallback_error}")
            return False
