#!/usr/bin/env python3
"""
Core Delivery for Message Queue Processing
==========================================

Handles direct delivery via core messaging system.
"""

import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)


def deliver_via_core(recipient: str, content: str, metadata: dict, message_type_str: str, sender: str, priority_str: str, tags_list: list) -> bool:
    """
    Deliver message via core messaging system (direct PyAutoGUI delivery).

    Args:
        recipient: Target agent ID
        content: Message content
        metadata: Message metadata
        message_type_str: Message type string
        sender: Sender identifier
        priority_str: Priority string
        tags_list: Tags list

    Returns:
        True if delivery successful, False otherwise
    """
    try:
        # Direct PyAutoGUI delivery - no CLI, no fallback simulation
        from src.core.messaging_pyautogui import send_message_pyautogui

        # Check if PyAutoGUI delivery is requested
        use_pyautogui = True
        if isinstance(metadata, dict):
            use_pyautogui = metadata.get("use_pyautogui", True)

        if not use_pyautogui:
            # Fall back to inbox delivery
            from .delivery_inbox import deliver_fallback_inbox
            return deliver_fallback_inbox(recipient, content, metadata, message_type_str, sender, priority_str, tags_list)

        # Direct PyAutoGUI delivery
        success = send_message_pyautogui(recipient, content)

        if success:
            logger.info(f"✅ Message delivered via PyAutoGUI to {recipient}")
            return True
        else:
            logger.error(f"❌ PyAutoGUI delivery failed for {recipient}")
            return False

    except Exception as e:
        logger.error(f"❌ Core delivery error: {e}")
        return False