#!/usr/bin/env python3
"""
Message Formatting Service - Core Layer
======================================

Simplified message formatting service for PyAutoGUI messaging operations.
Provides message normalization and content formatting.

<!-- SSOT Domain: communication -->

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Union

from messaging_models import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, MessageCategory, UnifiedMessageTag, SenderType, RecipientType

logger = logging.getLogger(__name__)


class MessageFormattingService:
    """Service for formatting and normalizing messages for PyAutoGUI delivery."""

    def normalize_message(self, message: Any) -> Optional[UnifiedMessage]:
        """
        Normalize various message formats to UnifiedMessage object.

        Args:
            message: Message in various formats (dict, UnifiedMessage, str)

        Returns:
            UnifiedMessage object or None if normalization fails
        """
        try:
            if isinstance(message, UnifiedMessage):
                return message
            elif isinstance(message, dict):
                return self._normalize_dict_message(message)
            elif isinstance(message, str):
                return self._normalize_string_message(message)
            else:
                logger.error(f"Unsupported message type: {type(message)}")
                return None
        except Exception as e:
            logger.error(f"Message normalization failed: {e}")
            return None

    def _normalize_dict_message(self, message_dict: Dict[str, Any]) -> UnifiedMessage:
        """Normalize dictionary message to UnifiedMessage."""
        # Extract basic fields
        content = message_dict.get('content', message_dict.get('message', ''))
        sender = message_dict.get('sender', message_dict.get('from', 'UNKNOWN'))
        recipient = message_dict.get('recipient', message_dict.get('to', 'UNKNOWN'))

        # Extract message type
        message_type_str = message_dict.get('message_type', message_dict.get('type', 'text'))
        try:
            message_type = UnifiedMessageType(message_type_str)
        except ValueError:
            message_type = UnifiedMessageType.TEXT

        # Extract priority
        priority_str = message_dict.get('priority', 'regular')
        try:
            priority = UnifiedMessagePriority(priority_str)
        except ValueError:
            priority = UnifiedMessagePriority.REGULAR

        # Extract tags
        tags = []
        if 'tags' in message_dict:
            for tag in message_dict['tags']:
                try:
                    tags.append(UnifiedMessageTag(tag))
                except ValueError:
                    pass

        # Extract metadata
        metadata = message_dict.get('metadata', {})

        # Extract category
        category_str = message_dict.get('category', 's2a')
        try:
            category = MessageCategory(category_str)
        except ValueError:
            category = MessageCategory.S2A

        return UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags,
            metadata=metadata,
            category=category,
            message_id=message_dict.get('message_id', None),
            sender_type=SenderType.SYSTEM,
            recipient_type=RecipientType.AGENT
        )

    def _normalize_string_message(self, message_str: str) -> UnifiedMessage:
        """Normalize string message to UnifiedMessage."""
        return UnifiedMessage(
            content=message_str,
            sender="SYSTEM",
            recipient="UNKNOWN",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[],
            metadata={},
            category=MessageCategory.S2A,
            sender_type=SenderType.SYSTEM,
            recipient_type=RecipientType.AGENT
        )

    def format_message_content(self, message: UnifiedMessage, sender: str) -> str:
        """
        Format message content for delivery.

        Args:
            message: UnifiedMessage object
            sender: Sender identifier

        Returns:
            Formatted message content string
        """
        try:
            # Basic formatting - just return content for now
            # Could be extended to add prefixes, timestamps, etc.
            content = message.content

            # Add sender prefix if needed
            if sender and sender != "SYSTEM":
                content = f"[{sender}] {content}"

            return content
        except Exception as e:
            logger.error(f"Message content formatting failed: {e}")
            return message.content if hasattr(message, 'content') else str(message)