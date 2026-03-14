#!/usr/bin/env python3
"""
Messaging Core Orchestrator - Service Layer Architecture
======================================================

<!-- SSOT Domain: integration -->

Main orchestration service for core messaging operations.

Author: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-16
Refactored from messaging_core.py for V2 compliance (file size limits)
"""

import logging
from typing import Dict, Any

# Use relative imports for V2 compliance
from ..messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
)

# Import service modules
from .message_queue_service import MessageQueueService
from .template_resolution_service import TemplateResolutionService
from .message_validation_service import MessageValidationService
from .delivery_orchestration_service import DeliveryOrchestrationService

logger = logging.getLogger(__name__)


class MessagingCoreOrchestrator:
    """Main orchestration service for core messaging operations."""

    def __init__(self):
        self.queue_service = MessageQueueService()
        self.template_service = TemplateResolutionService()
        self.validation_service = MessageValidationService()
        self.delivery_service = DeliveryOrchestrationService()

    def send_message(self, message: UnifiedMessage,
                    validate: bool = True,
                    resolve_templates: bool = True) -> bool:
        """Send message through complete messaging pipeline."""
        try:
            # Validation phase
            if validate:
                is_valid, errors = self.validation_service.validate_message(message)
                if not is_valid:
                    logger.error(f"Message validation failed: {errors}")
                    return False

            # Template resolution phase
            if resolve_templates:
                message.content = self.template_service.format_message_content(message)

            # Sanitization phase
            message.content = self.validation_service.sanitize_content(message.content)

            # Delivery phase
            success = self.delivery_service.deliver_message(message)

            if success:
                logger.info(f"✅ Message sent successfully to {message.recipient}")
            else:
                logger.warning(f"⚠️ Message delivery failed to {message.recipient}")

            return success

        except Exception as e:
            logger.error(f"❌ Message orchestration failed: {e}")
            return False

    def queue_message(self, message: UnifiedMessage) -> bool:
        """Queue message for later processing."""
        return self.queue_service.enqueue_message(message)

    def process_queue(self, recipient: str) -> int:
        """Process queued messages for recipient."""
        processed = 0

        while True:
            message = self.queue_service.dequeue_message(recipient)
            if not message:
                break

            if self.send_message(message):
                processed += 1
            else:
                # Re-queue failed messages
                self.queue_message(message)
                break

        return processed

    def get_messaging_stats(self) -> Dict[str, Any]:
        """Get comprehensive messaging statistics."""
        available_templates = self.template_service.get_available_templates()
        file_templates = [t for t in available_templates if isinstance(t, str) and t.startswith('file:')]

        return {
            'queue_service': {
                'available': True,
                'queue_count': len(list(self.queue_service.queue_dir.glob("*_queue.json")))
            },
            'template_service': {
                'available': True,
                'template_count': len(available_templates),
                'file_templates': file_templates,
                'builtin_templates': len([t for t in available_templates if not (isinstance(t, str) and t.startswith('file:'))])
            },
            'validation_service': {
                'available': True,
                'max_content_length': self.validation_service.max_content_length
            },
            'delivery_service': {
                'available': True,
                'methods': [method.value for method in self.delivery_service.get_available_methods()]
            }
        }


# Legacy compatibility functions
def send_agent_message(sender: str, recipient: str, content: str,
                      message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                      priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                      **kwargs) -> bool:
    """Legacy function for sending agent-to-agent messages."""
    orchestrator = MessagingCoreOrchestrator()

    message = UnifiedMessage(
        content=content,
        sender=sender,
        recipient=recipient,
        message_type=message_type,
        priority=priority,
        tags=[],
        metadata=kwargs
    )

    return orchestrator.send_message(message)


def broadcast_message(content: str, priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                     **kwargs) -> bool:
    """Legacy function for broadcasting messages to all agents."""
    # This would need agent registry integration
    logger.warning("Broadcast functionality requires agent registry integration")
    return False


def get_messaging_stats() -> Dict[str, Any]:
    """Get messaging system statistics."""
    orchestrator = MessagingCoreOrchestrator()
    return orchestrator.get_messaging_stats()