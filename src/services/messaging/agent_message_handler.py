#!/usr/bin/env python3
"""
Agent Message Handler - Messaging Infrastructure
===============================================

<!-- SSOT Domain: integration -->

Handles single-agent message delivery via message queue.
Extracted from coordination_handlers.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)
from src.core.messaging_models_core import MessageCategory

from .agent_message_helpers import (
    build_queue_metadata,
    detect_and_determine_sender,
    format_message_for_queue,
    handle_blocked_message,
    send_message_with_fallback,
    send_validated_message,
    update_last_inbound_category,
    validate_and_prepare_message,
)
from .message_deduplication_service import check_message_duplicate
from .message_formatters import _map_category_from_type

logger = logging.getLogger(__name__)


def send_to_agent(
    agent: str,
    message,
    priority=UnifiedMessagePriority.REGULAR,
    use_pyautogui=False,
    stalled: bool = False,
    send_mode: Optional[str] = None,
    sender: str = None,
    message_category: Optional[MessageCategory] = None,
    message_metadata: Optional[Dict[str, Any]] = None,
    queue_repository=None,
    detect_sender_func=None,
    determine_message_type_func=None,
):
    """Send message to agent via message queue. Routes through queue for PyAutoGUI orchestration."""
    try:
        # Check for duplicate messages to prevent coordination loops
        message_id = message_metadata.get("message_id") if isinstance(message_metadata, dict) else None
        if message_id and check_message_duplicate(message_id):
            logger.warning(f"🚫 Blocking duplicate message delivery: {message_id} to {agent}")
            return {
                "success": False,
                "blocked": True,
                "reason": "duplicate_message",
                "error_message": f"Message {message_id} already processed - preventing coordination loop",
                "agent": agent,
            }
        message_type, sender_final = detect_and_determine_sender(
            sender, agent, detect_sender_func, determine_message_type_func
        )
        category = message_category or _map_category_from_type(message_type)

        # Hardened A2A detection: if the message text clearly indicates A2A intent
        # but category was not set to A2A, either auto-promote or hard error.
        if isinstance(message, str):
            text = message.strip()
            if text.lower().startswith("a2a:") and category != MessageCategory.A2A:
                if sender_final and sender_final.upper().startswith("AGENT-"):
                    logger.info(
                        "🔄 Promoting message to A2A based on 'A2A:' prefix and Agent sender "
                        "(sender=%s, recipient=%s)",
                        sender_final,
                        agent,
                    )
                    category = MessageCategory.A2A
                else:
                    error_msg = (
                        "Message starts with 'A2A:' but sender is not an Agent-*. "
                        "Set AGENT_CONTEXT=Agent-X or use --sender Agent-X / --category a2a "
                        "with the messaging CLI."
                    )
                    block_result = {
                        "success": False,
                        "blocked": True,
                        "reason": "invalid_a2a_sender",
                        "error_message": error_msg,
                        "agent": agent,
                    }
                    handle_blocked_message(block_result, agent)
                    return block_result

        block_result, _ = validate_and_prepare_message(
            sender_final, agent, message, category)
        if block_result:
            handle_blocked_message(block_result, agent)
            return block_result
        return send_validated_message(
            queue_repository,
            sender_final,
            agent,
            message,
            category,
            stalled,
            use_pyautogui,
            send_mode,
            priority,
            message_type,
        )
    except Exception as e:
        logger.error(f"Error sending message to {agent}: {e}")
        return False
