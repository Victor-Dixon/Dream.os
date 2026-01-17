#!/usr/bin/env python3
"""
Messaging Core Services - Service Layer Architecture
===================================================

<!-- SSOT Domain: integration -->

Core messaging services following service layer pattern.
Extracted from monolithic messaging_unified.py for better maintainability.

SERVICES INCLUDED:
- MessageQueueService: Queue management and persistence
- TemplateResolutionService: Dynamic message formatting
- DeliveryOrchestrationService: Coordinates delivery methods
- MessageValidationService: Content validation and sanitization
- MessagingCoreOrchestrator: Main orchestration layer

PHASE 2 INFRASTRUCTURE REFACTORING:
- Service layer pattern implementation
- Clear separation of concerns
- Dependency injection for testability
- Modular design for extensibility

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-16
"""

import json
import logging
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable
from uuid import uuid4

try:
    # Try absolute imports first
    from messaging_models import (
        UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
        UnifiedMessageTag, DeliveryMethod, MessageStatus
    )
    from messaging_template_texts import MESSAGE_TEMPLATES
except ImportError:
    # Fallback to relative imports if absolute imports fail
    from .messaging_models import (
        UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
        UnifiedMessageTag, DeliveryMethod, MessageStatus
    )
    from .messaging_template_texts import MESSAGE_TEMPLATES

logger = logging.getLogger(__name__)


class MessageQueueService:
    """Service for managing message queues with persistence and routing."""

    def __init__(self, queue_dir: str = "message_queues"):
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(exist_ok=True)
        self._lock = threading.Lock()

    def enqueue_message(self, message: UnifiedMessage) -> bool:
        """Add message to appropriate queue with persistence."""
        try:
            with self._lock:
                queue_file = self._get_queue_file(message.recipient)
                queue_data = self._load_queue(queue_file)

                message_data = {
                    'id': str(message.id),
                    'content': message.content,
                    'sender': message.sender,
                    'recipient': message.recipient,
                    'message_type': message.message_type.value,
                    'priority': message.priority.value,
                    'tags': [tag.value for tag in message.tags],
                    'metadata': message.metadata,
                    'timestamp': message.timestamp.isoformat(),
                    'status': MessageStatus.QUEUED.value
                }

                queue_data['messages'].append(message_data)
                self._save_queue(queue_file, queue_data)

            logger.info(f"✅ Message {message.id} queued for {message.recipient}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to enqueue message: {e}")
            return False

    def dequeue_message(self, recipient: str) -> Optional[UnifiedMessage]:
        """Retrieve next message from queue."""
        try:
            with self._lock:
                queue_file = self._get_queue_file(recipient)
                queue_data = self._load_queue(queue_file)

                if not queue_data['messages']:
                    return None

                # Get highest priority message first
                messages = queue_data['messages']
                messages.sort(key=lambda m: self._get_priority_weight(m['priority']), reverse=True)

                message_data = messages.pop(0)
                self._save_queue(queue_file, queue_data)

                return self._deserialize_message(message_data)

        except Exception as e:
            logger.error(f"❌ Failed to dequeue message: {e}")
            return None

    def _get_queue_file(self, recipient: str) -> Path:
        """Get queue file path for recipient."""
        return self.queue_dir / f"{recipient}_queue.json"

    def _load_queue(self, queue_file: Path) -> Dict[str, Any]:
        """Load queue data from file."""
        if not queue_file.exists():
            return {'messages': []}

        try:
            with open(queue_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {'messages': []}

    def _save_queue(self, queue_file: Path, queue_data: Dict[str, Any]) -> None:
        """Save queue data to file."""
        with open(queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)

    def _get_priority_weight(self, priority: str) -> int:
        """Get priority weight for sorting."""
        weights = {
            UnifiedMessagePriority.URGENT.value: 3,
            UnifiedMessagePriority.REGULAR.value: 2,
            'normal': 1,
            'low': 0
        }
        return weights.get(priority, 1)

    def _deserialize_message(self, message_data: Dict[str, Any]) -> UnifiedMessage:
        """Convert queue data back to UnifiedMessage."""
        return UnifiedMessage(
            id=message_data['id'],
            content=message_data['content'],
            sender=message_data['sender'],
            recipient=message_data['recipient'],
            message_type=UnifiedMessageType(message_data['message_type']),
            priority=UnifiedMessagePriority(message_data['priority']),
            tags=[UnifiedMessageTag(tag) for tag in message_data.get('tags', [])],
            metadata=message_data.get('metadata', {}),
            timestamp=datetime.fromisoformat(message_data['timestamp'])
        )


class TemplateResolutionService:
    """Service for resolving and formatting message templates."""

    def __init__(self):
        self.templates = MESSAGE_TEMPLATES

    def resolve_template(self, template_key: str, **kwargs) -> str:
        """Resolve template with provided variables."""
        if template_key not in self.templates:
            logger.warning(f"Template {template_key} not found")
            return kwargs.get('content', '')

        template = self.templates[template_key]

        try:
            # Handle different template formats
            if isinstance(template, str):
                return template.format(**kwargs)
            elif isinstance(template, dict):
                # Handle structured templates
                base_template = template.get('template', '')
                return base_template.format(**kwargs)
            else:
                return str(template)

        except KeyError as e:
            logger.error(f"Missing template variable: {e}")
            return f"Template error: missing {e}"

    def format_message_content(self, message: UnifiedMessage, **context) -> str:
        """Format message content with template resolution."""
        if not message.content:
            return ""

        # Check if content is a template key
        if message.content in self.templates:
            template_vars = {
                'sender': message.sender,
                'recipient': message.recipient,
                'timestamp': message.timestamp.isoformat(),
                **context
            }
            return self.resolve_template(message.content, **template_vars)

        # Return content as-is if not a template
        return message.content

    def get_available_templates(self) -> List[str]:
        """Get list of available template keys."""
        return list(self.templates.keys())


class MessageValidationService:
    """Service for validating message content and structure."""

    def __init__(self):
        self.max_content_length = 10000
        self.max_metadata_size = 5000

    def validate_message(self, message: UnifiedMessage) -> Tuple[bool, List[str]]:
        """Validate message structure and content."""
        errors = []

        # Basic structure validation
        if not message.content:
            errors.append("Message content cannot be empty")

        if not message.sender:
            errors.append("Message sender cannot be empty")

        if not message.recipient:
            errors.append("Message recipient cannot be empty")

        # Content validation
        if len(message.content) > self.max_content_length:
            errors.append(f"Message content too long ({len(message.content)} > {self.max_content_length})")

        # Metadata validation
        if message.metadata:
            metadata_size = len(json.dumps(message.metadata))
            if metadata_size > self.max_metadata_size:
                errors.append(f"Message metadata too large ({metadata_size} > {self.max_metadata_size})")

        # Type validation
        if not isinstance(message.message_type, UnifiedMessageType):
            errors.append("Invalid message type")

        if not isinstance(message.priority, UnifiedMessagePriority):
            errors.append("Invalid message priority")

        # Tag validation
        for tag in message.tags:
            if not isinstance(tag, UnifiedMessageTag):
                errors.append(f"Invalid message tag: {tag}")

        return len(errors) == 0, errors

    def sanitize_content(self, content: str) -> str:
        """Sanitize message content for security."""
        if not content:
            return ""

        # Basic sanitization - remove potentially harmful content
        # This is a simplified version; production would need more robust sanitization
        sanitized = content.replace('\x00', '')  # Remove null bytes

        return sanitized[:self.max_content_length]  # Truncate if too long


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
        return {
            'queue_service': {
                'available': True,
                'queue_count': len(list(self.queue_service.queue_dir.glob("*_queue.json")))
            },
            'template_service': {
                'available': True,
                'template_count': len(self.template_service.get_available_templates())
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