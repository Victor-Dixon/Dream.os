#!/usr/bin/env python3
"""
Message Validation Service - Service Layer Pattern
==================================================

Encapsulates business logic for message validation.
Handles ack blocking, recipient validation, and message preparation.

V2 Compliance | Author: Agent-1 | Date: 2025-12-22
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

from src.core.messaging_models_core import MessageCategory

from ..agent_message_helpers import (
    check_ack_blocked,
    validate_recipient_can_receive,
)

logger = logging.getLogger(__name__)


class MessageValidationService:
    """Service for validating messages before delivery."""

    def validate_message(
        self,
        sender: str,
        recipient: str,
        message: Any,
        category: Optional[MessageCategory],
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Validate message and return blocking result if needed.

        Args:
            sender: Message sender
            recipient: Message recipient
            message: Message content
            category: Message category

        Returns:
            Tuple of (block_result, metadata) - both None if valid
        """
        # Check for ack blocking
        ack_block = check_ack_blocked(sender, message)
        if ack_block:
            ack_block["agent"] = recipient
            return ack_block, None

        # Check if recipient can receive messages
        can_send, error_message, pending_info = validate_recipient_can_receive(
            recipient, message
        )
        if not can_send:
            return {
                "success": False,
                "blocked": True,
                "reason": "pending_multi_agent_request",
                "error_message": error_message,
                "agent": recipient,
                "pending_info": pending_info,
            }, None

        return None, None

    def validate_a2a_category(
        self,
        message: str,
        category: MessageCategory,
        sender: str,
        recipient: str,
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate A2A message category consistency.

        Args:
            message: Message content
            category: Current message category
            sender: Message sender
            recipient: Message recipient

        Returns:
            Tuple of (is_valid, block_result) - block_result is None if valid
        """
        if not isinstance(message, str):
            return True, None

        text = message.strip().lower()
        if text.startswith("a2a:") and category != MessageCategory.A2A:
            if sender and sender.upper().startswith("AGENT-"):
                logger.info(
                    "🔄 Promoting message to A2A based on 'A2A:' prefix and Agent sender "
                    "(sender=%s, recipient=%s)",
                    sender,
                    recipient,
                )
                return True, None  # Valid, will be promoted
            else:
                error_msg = (
                    "Message starts with 'A2A:' but sender is not an Agent-*. "
                    "Set AGENT_CONTEXT=Agent-X or use --sender Agent-X / --category a2a "
                    "with the messaging CLI."
                )
                return False, {
                    "success": False,
                    "blocked": True,
                    "reason": "invalid_a2a_sender",
                    "error_message": error_msg,
                    "agent": recipient,
                }

        return True, None


