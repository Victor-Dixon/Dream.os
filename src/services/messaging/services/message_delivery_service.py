#!/usr/bin/env python3
"""
Message Delivery Service - Service Layer Pattern
================================================

Encapsulates business logic for message delivery orchestration.
Handles queue operations, fallback logic, and delivery coordination.

V2 Compliance | Author: Agent-1 | Date: 2025-12-22
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority, UnifiedMessageType
from src.core.messaging_models_core import MessageCategory

from ..agent_message_helpers import (
    send_message_with_fallback,
    update_last_inbound_category,
)
from ..domain.interfaces.queue_repository import IQueueRepository
from .message_formatting_service import MessageFormattingService
from .message_routing_service import MessageRoutingService
from .message_validation_service import MessageValidationService

logger = logging.getLogger(__name__)


class MessageDeliveryService:
    """Service for orchestrating message delivery."""

    def __init__(
        self,
        queue_repository: Optional[IQueueRepository] = None,
        validation_service: Optional[MessageValidationService] = None,
        routing_service: Optional[MessageRoutingService] = None,
        formatting_service: Optional[MessageFormattingService] = None,
    ):
        """
        Initialize message delivery service.

        Args:
            queue_repository: Queue repository instance
            validation_service: Validation service instance
            routing_service: Routing service instance
            formatting_service: Formatting service instance
        """
        self.queue_repository = queue_repository
        self.validation_service = validation_service or MessageValidationService()
        self.routing_service = routing_service or MessageRoutingService()
        self.formatting_service = formatting_service or MessageFormattingService()

    def deliver_message(
        self,
        recipient: str,
        message: Any,
        sender: Optional[str] = None,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        category: Optional[MessageCategory] = None,
        stalled: bool = False,
        use_pyautogui: bool = False,
        send_mode: Optional[str] = None,
        detect_sender_func: Optional[Any] = None,
        determine_message_type_func: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Deliver message to recipient with full orchestration.

        Args:
            recipient: Message recipient
            message: Message content
            sender: Explicit sender
            priority: Message priority
            category: Message category
            stalled: Use stalled delivery mode
            use_pyautogui: Use PyAutoGUI for delivery
            send_mode: Send mode override
            detect_sender_func: Optional sender detection function
            determine_message_type_func: Optional message type determination function

        Returns:
            Delivery result dictionary
        """
        # Step 1: Determine sender and message type
        message_type, sender_final = self.routing_service.determine_sender_and_type(
            sender, recipient, detect_sender_func, determine_message_type_func
        )

        # Step 2: Determine category
        final_category = self.routing_service.determine_category(
            message_type, category
        )

        # Step 3: Validate A2A category consistency
        if isinstance(message, str):
            is_valid, block_result = self.validation_service.validate_a2a_category(
                message, final_category, sender_final, recipient
            )
            if not is_valid:
                return block_result or {"success": False, "blocked": True}

        # Step 4: Validate message
        block_result, _ = self.validation_service.validate_message(
            sender_final, recipient, message, final_category
        )
        if block_result:
            return block_result

        # Step 5: Format and template message
        templated_message = self.formatting_service.apply_template(
            message, final_category, sender_final, recipient, priority
        )
        formatted_message = self.formatting_service.format_for_queue(
            templated_message, final_category
        )

        # Step 6: Build metadata
        metadata = self.formatting_service.build_metadata(
            stalled, use_pyautogui, send_mode, final_category
        )

        # Step 7: Deliver via queue with fallback
        result = send_message_with_fallback(
            self.queue_repository,
            sender_final,
            recipient,
            formatted_message,
            priority,
            message_type,
            metadata,
        )

        # Step 8: Update last inbound category
        update_last_inbound_category(recipient, final_category)

        return result


