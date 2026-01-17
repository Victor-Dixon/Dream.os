#!/usr/bin/env python3
"""
Delivery Orchestration Service - Service Layer Architecture
========================================================

<!-- SSOT Domain: integration -->

Service for orchestrating message delivery across multiple methods.

Author: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-16
Refactored from messaging_core.py for V2 compliance (file size limits)
"""

import logging
from typing import List

# Use relative imports for V2 compliance
from ..messaging_models import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, DeliveryMethod

logger = logging.getLogger(__name__)


class DeliveryOrchestrationService:
    """Service for orchestrating message delivery across multiple methods."""

    def __init__(self):
        self.delivery_methods = {}
        self._register_delivery_methods()

    def _register_delivery_methods(self):
        """Register available delivery methods."""
        # Import delivery classes dynamically to avoid circular imports
        try:
            from messaging_pyautogui import PyAutoGUIMessagingDelivery
            self.delivery_methods[DeliveryMethod.PYAUTOGUI] = PyAutoGUIMessagingDelivery()
        except ImportError:
            logger.warning("PyAutoGUI delivery not available")

        try:
            from messaging_delivery_discord import DiscordDelivery
            self.delivery_methods[DeliveryMethod.DISCORD] = DiscordDelivery()
        except ImportError:
            logger.warning("Discord delivery not available")

    def deliver_message(self, message: UnifiedMessage,
                       preferred_method: DeliveryMethod = None) -> bool:
        """Deliver message using appropriate method."""
        method = preferred_method or self._determine_delivery_method(message)

        if method not in self.delivery_methods:
            logger.error(f"Delivery method {method} not available")
            return False

        delivery_service = self.delivery_methods[method]

        try:
            if hasattr(delivery_service, 'send_message'):
                return delivery_service.send_message(message)
            elif hasattr(delivery_service, 'deliver'):
                return delivery_service.deliver(message)
            else:
                logger.error(f"Delivery service {method} has no send method")
                return False

        except Exception as e:
            logger.error(f"Delivery failed via {method}: {e}")
            return False

    def _determine_delivery_method(self, message: UnifiedMessage) -> DeliveryMethod:
        """Determine best delivery method for message."""
        # Priority-based method selection
        if message.priority == UnifiedMessagePriority.URGENT:
            return DeliveryMethod.PYAUTOGUI  # Direct delivery for urgent messages

        # Type-based selection
        if message.message_type in [UnifiedMessageType.ONBOARDING, UnifiedMessageType.CAPTAIN_TO_AGENT]:
            return DeliveryMethod.PYAUTOGUI  # Direct for control messages

        # Default to PyAutoGUI for agent communication
        return DeliveryMethod.PYAUTOGUI

    def get_available_methods(self) -> List[DeliveryMethod]:
        """Get list of available delivery methods."""
        return list(self.delivery_methods.keys())