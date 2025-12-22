#!/usr/bin/env python3
"""
Message Routing Service - Service Layer Pattern
===============================================

Encapsulates business logic for message routing decisions.
Handles sender detection, message type determination, and category mapping.

V2 Compliance | Author: Agent-1 | Date: 2025-12-22
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Optional, Tuple

from src.core.messaging_core import UnifiedMessageType
from src.core.messaging_models_core import MessageCategory

from ..agent_message_helpers import detect_and_determine_sender
from ..message_formatters import _map_category_from_type

logger = logging.getLogger(__name__)


class MessageRoutingService:
    """Service for determining message routing and categorization."""

    def determine_sender_and_type(
        self,
        sender: Optional[str],
        recipient: str,
        detect_sender_func: Optional[Callable[[], str]] = None,
        determine_message_type_func: Optional[
            Callable[[str, str], Tuple[UnifiedMessageType, str]]
        ] = None,
    ) -> Tuple[UnifiedMessageType, str]:
        """
        Determine sender and message type.

        Args:
            sender: Explicit sender (if provided)
            recipient: Message recipient
            detect_sender_func: Optional function to detect sender
            determine_message_type_func: Optional function to determine message type

        Returns:
            Tuple of (message_type, sender_final)
        """
        return detect_and_determine_sender(
            sender, recipient, detect_sender_func, determine_message_type_func
        )

    def determine_category(
        self,
        message_type: UnifiedMessageType,
        explicit_category: Optional[MessageCategory] = None,
    ) -> MessageCategory:
        """
        Determine message category from type or use explicit category.

        Args:
            message_type: Determined message type
            explicit_category: Explicitly provided category

        Returns:
            Message category
        """
        if explicit_category:
            return explicit_category
        return _map_category_from_type(message_type)

