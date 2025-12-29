#!/usr/bin/env python3
"""
Message Formatting Service - Service Layer Pattern
==================================================

Encapsulates business logic for message formatting and templating.
Handles template application, message formatting, and metadata building.

<!-- SSOT Domain: integration -->

V2 Compliance | Author: Agent-1 | Date: 2025-12-22
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional

from src.core.messaging_models_core import MessageCategory

from ..agent_message_helpers import build_queue_metadata, format_message_for_queue
from ..message_formatters import _apply_template

logger = logging.getLogger(__name__)


class MessageFormattingService:
    """Service for formatting and templating messages."""

    def apply_template(
        self,
        message: Any,
        category: MessageCategory,
        sender: str,
        recipient: str,
        priority: Any,
    ) -> str:
        """
        Apply message template if needed.

        Args:
            message: Raw message content
            category: Message category
            sender: Message sender
            recipient: Message recipient
            priority: Message priority

        Returns:
            Templated message content
        """
        # Apply A2A coordination template for Agent-to-Agent messages
        if category == MessageCategory.A2A and isinstance(message, str):
            try:
                # Populate extra metadata with message content for template
                extra_meta = {
                    "ask": message,  # Map message content to 'ask' field in A2A template
                    "context": "",  # Empty context by default, can be extended later
                }
                return _apply_template(
                    category=MessageCategory.A2A,
                    message=message,
                    sender=sender,
                    recipient=recipient,
                    priority=priority,
                    message_id=str(uuid.uuid4()),
                    extra=extra_meta,
                )
            except Exception as e:
                logger.warning(
                    f"Template application failed, using raw message: {e}"
                )
                return message

        return message

    def format_for_queue(
        self,
        message: str,
        category: MessageCategory,
    ) -> str:
        """
        Format message for queue delivery.

        Args:
            message: Message content
            category: Message category

        Returns:
            Formatted message
        """
        return format_message_for_queue(message, category)

    def build_metadata(
        self,
        stalled: bool,
        use_pyautogui: bool,
        send_mode: Optional[str],
        category: Optional[MessageCategory],
    ) -> Dict[str, Any]:
        """
        Build queue metadata for message.

        Args:
            stalled: Use stalled delivery mode
            use_pyautogui: Use PyAutoGUI for delivery
            send_mode: Send mode override
            category: Message category

        Returns:
            Metadata dictionary
        """
        return build_queue_metadata(stalled, use_pyautogui, send_mode, category)






