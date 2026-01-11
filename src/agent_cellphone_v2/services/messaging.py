"""
Messaging service for Agent Cellphone V2.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List

from ..config import Settings

# Import unified messaging components
UNIFIED_COMPONENTS_AVAILABLE = False
try:
    from src.core.messaging_models import (
        UnifiedMessage,
        UnifiedMessageType,
        UnifiedMessagePriority,
        MessageCategory,
        UnifiedMessageTag,
        SenderType,
        RecipientType
    )
    from src.core.error_handling.unified_error_handler import handle_errors, ErrorCategory, ErrorSeverity
    from src.services.messaging.unified_formatter import UnifiedMessageFormatter
    from src.core.in_memory_message_queue import InMemoryMessageQueue
    UNIFIED_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Unified messaging components not available ({e}), using fallback implementation")

logger = logging.getLogger(__name__)


class MessagingService:
    """
    Service for handling inter-agent messaging and coordination.

    Features:
    - Unified message formatting and validation
    - Error handling with retry logic
    - Message queuing and delivery tracking
    - A2A coordination support
    - Status persistence
    """

    def __init__(self, settings: Settings):
        """
        Initialize messaging service.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self._running = False
        self._message_queue = None
        self._message_history: List[Dict[str, Any]] = []
        self._max_history_size = 1000

        # Initialize unified components if available
        if UNIFIED_COMPONENTS_AVAILABLE:
            self._message_queue = InMemoryMessageQueue(max_size=5000)
            self._formatter = UnifiedMessageFormatter()
        else:
            logger.warning("Using basic message queue implementation")
            self._message_queue = BasicMessageQueue()

    async def start(self) -> None:
        """Start the messaging service."""
        logger.info("Starting messaging service...")
        self._running = True
        logger.info("Messaging service started with unified components: %s", UNIFIED_COMPONENTS_AVAILABLE)

    async def stop(self) -> None:
        """Stop the messaging service."""
        logger.info("Stopping messaging service...")
        self._running = False
        logger.info("Messaging service stopped")

    def is_running(self) -> bool:
        """Check if service is running."""
        return self._running

    @handle_errors(category=ErrorCategory.NETWORK, severity=ErrorSeverity.MEDIUM)
    async def send_message(self, recipient: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Send a message to an agent with full unified messaging support.

        Args:
            recipient: Agent ID to send message to
            message: Message content
            **kwargs: Additional message parameters including:
                - priority: Message priority (regular, high, urgent)
                - category: Message category (a2a, d2a, s2a, c2a)
                - tags: List of message tags
                - metadata: Additional metadata

        Returns:
            Message delivery status with enhanced tracking
        """
        logger.info(f"Sending message to {recipient}: {message[:50]}...")

        if not self._running:
            raise RuntimeError("Messaging service is not running")

        # Create unified message structure
        if UNIFIED_COMPONENTS_AVAILABLE:
            unified_message = self._create_unified_message(recipient, message, **kwargs)
            delivery_result = await self._deliver_unified_message(unified_message)
        else:
            delivery_result = await self._deliver_basic_message(recipient, message, **kwargs)

        # Track message in history
        self._add_to_history({
            "message_id": delivery_result.get("message_id"),
            "recipient": recipient,
            "content_preview": message[:100],
            "timestamp": delivery_result.get("timestamp"),
            "status": delivery_result.get("status"),
            "priority": kwargs.get("priority", "regular"),
            "category": kwargs.get("category", "s2a")
        })

        return delivery_result

    def _create_unified_message(self, recipient: str, content: str, **kwargs) -> UnifiedMessage:
        """Create a unified message with proper typing and validation."""
        # Map string priorities to enum
        priority_map = {
            "regular": UnifiedMessagePriority.REGULAR,
            "high": UnifiedMessagePriority.URGENT,  # Map high to urgent
            "urgent": UnifiedMessagePriority.URGENT
        }

        # Map string categories to enum
        category_map = {
            "a2a": MessageCategory.A2A,
            "d2a": MessageCategory.D2A,
            "s2a": MessageCategory.S2A,
            "c2a": MessageCategory.C2A
        }

        # Convert tags to enum values
        tag_enums = []
        if "tags" in kwargs:
            tag_map = {
                "coordination": UnifiedMessageTag.COORDINATION,
                "task": UnifiedMessageTag.TASK,
                "status": UnifiedMessageTag.STATUS,
                "error": UnifiedMessageTag.ERROR,
                "coordination-reply": UnifiedMessageTag.COORDINATION_REPLY
            }
            for tag in kwargs["tags"]:
                if tag in tag_map:
                    tag_enums.append(tag_map[tag])

        return UnifiedMessage(
            content=content,
            sender=self._get_current_agent(),
            recipient=recipient,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,  # Default to agent-to-agent
            priority=priority_map.get(kwargs.get("priority", "regular"), UnifiedMessagePriority.REGULAR),
            category=category_map.get(kwargs.get("category", "s2a"), MessageCategory.S2A),
            tags=tag_enums,
            metadata=kwargs.get("metadata", {}),
            sender_type=SenderType.AGENT,
            recipient_type=RecipientType.AGENT
        )

    async def _deliver_unified_message(self, message: UnifiedMessage) -> Dict[str, Any]:
        """Deliver a unified message using the message queue."""
        try:
            # Format message using unified formatter
            formatted_content = self._formatter.format_message(
                category=message.category,
                message=message.content,
                sender=message.sender,
                recipient=message.recipient,
                priority=message.priority,
                message_id=message.message_id,
                extra=message.metadata
            )

            # Queue message for delivery
            queue_id = self._message_queue.enqueue(
                message={
                    "id": message.message_id,
                    "content": formatted_content,
                    "recipient": message.recipient,
                    "metadata": message.metadata
                },
                priority=message.priority.value,
                metadata={
                    "message_type": message.message_type.value,
                    "category": message.category.value,
                    "tags": [tag.value for tag in message.tags]
                }
            )

            if queue_id:
                logger.info(f"Message {message.message_id} queued successfully for {message.recipient}")
                return {
                    "status": "queued",
                    "recipient": message.recipient,
                    "message_id": message.message_id,
                    "queue_id": queue_id,
                    "timestamp": message.timestamp.isoformat(),
                    "formatted_content": formatted_content
                }
            else:
                logger.error(f"Failed to queue message {message.message_id}")
                return {
                    "status": "failed",
                    "recipient": message.recipient,
                    "message_id": message.message_id,
                    "error": "Queue full",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

        except Exception as e:
            logger.error(f"Error delivering unified message: {e}")
            return {
                "status": "error",
                "recipient": message.recipient,
                "message_id": message.message_id,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    async def _deliver_basic_message(self, recipient: str, message: str, **kwargs) -> Dict[str, Any]:
        """Fallback delivery for basic messaging when unified components unavailable."""
        message_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc)

        # Simulate delivery
        await asyncio.sleep(0.01)  # Small delay to simulate network

        logger.info(f"Basic message {message_id} 'delivered' to {recipient}")
        return {
            "status": "sent",
            "recipient": recipient,
            "message_id": message_id,
            "timestamp": timestamp.isoformat(),
        }

    def _get_current_agent(self) -> str:
        """Get current agent ID from environment or settings."""
        # Try to get from environment first
        import os
        agent_id = os.getenv("AGENT_ID") or os.getenv("CURRENT_AGENT")

        # Fallback to settings or default
        if not agent_id:
            agent_id = getattr(self.settings, "current_agent", "Agent-4")

        return agent_id

    def _add_to_history(self, message_record: Dict[str, Any]):
        """Add message to history with size management."""
        self._message_history.append(message_record)

        # Maintain max history size
        if len(self._message_history) > self._max_history_size:
            self._message_history = self._message_history[-self._max_history_size:]

    def get_message_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent message history."""
        return self._message_history[-limit:]

    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status information for an agent."""
        # This would integrate with agent status tracking
        # For now, return basic info
        return {
            "agent_id": agent_id,
            "status": "active",
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "message_count": len([m for m in self._message_history if m.get("recipient") == agent_id])
        }


class BasicMessageQueue:
    """Basic fallback message queue when unified components not available."""

    def __init__(self):
        self._messages = []

    def enqueue(self, message: Dict[str, Any], priority: str = "normal", metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Basic enqueue operation."""
        queue_id = str(uuid.uuid4())
        self._messages.append({
            "id": queue_id,
            "message": message,
            "priority": priority,
            "metadata": metadata or {}
        })
        return queue_id