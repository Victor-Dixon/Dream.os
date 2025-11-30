#!/usr/bin/env python3
"""
Message Queue Processor - Deterministic Queue Processing
=======================================================

Processes queued messages with dependency injection for messaging core.
Supports both real and mock messaging cores for testing.

V2 Compliance: <400 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import logging
import time
from typing import Any, Optional

from .message_queue import MessageQueue, QueueConfig
from .message_queue_persistence import QueueEntry

logger = logging.getLogger(__name__)


class MessageQueueProcessor:
    """
    Deterministic processor for queued messages.

    Responsibilities:
    • Read from queue
    • Deliver message via unified messaging core
    • Mark delivered/failed
    • Log to repository (optional)
    • PyAutoGUI delivery (primary)
    • Inbox fallback on delivery failure (backup)
    • Error handling and logging

    V3 Compliance:
    • Single responsibility: Queue processing only
    • Hard boundaries: Clear error isolation
    • Deterministic: Predictable delivery pipeline
    • Type-safe: Stricter type usage
    """

    def __init__(
        self,
        queue: Optional[MessageQueue] = None,
        message_repository: Optional[Any] = None,
        config: Optional[QueueConfig] = None,
        messaging_core: Optional[Any] = None,
    ) -> None:
        """Initialize message queue processor.

        Args:
            queue: MessageQueue instance (creates default if None)
            message_repository: MessageRepository for logging (optional)
            config: QueueConfig instance (creates default if None)
            messaging_core: Optional messaging core for dependency injection (for testing)
        """
        self.config = config or QueueConfig()
        self.queue = queue or MessageQueue(config=self.config)
        self.message_repository = message_repository
        # Injected core (None = use default real core)
        self.messaging_core = messaging_core
        self.running = False

    def process_queue(
        self,
        max_messages: Optional[int] = None,
        batch_size: int = 1,
        interval: float = 5.0,
    ) -> int:
        """
        Process queued messages in controlled batches.

        Args:
            max_messages: Maximum messages to process (None = unlimited)
            batch_size: Number of messages to process per batch
            interval: Sleep interval between batches (seconds)

        Returns:
            Number of messages processed
        """
        self.running = True
        processed = 0

        try:
            while self.running:
                entries = self._safe_dequeue(batch_size)
                if not entries:
                    if max_messages is None:
                        time.sleep(interval)
                        continue
                    break

                for entry in entries:
                    if max_messages and processed >= max_messages:
                        break

                    ok = self._deliver_entry(entry)
                    processed += 1

                if max_messages and processed >= max_messages:
                    break

        except KeyboardInterrupt:
            logger.info("🛑 Stopped by operator")
        except Exception as e:
            logger.error(f"Fatal queue loop error: {e}", exc_info=True)
        finally:
            self.running = False
            logger.info(f"✅ Queue processor complete: {processed} delivered")

        return processed

    def _safe_dequeue(self, batch_size: int) -> list[Any]:
        """Safely dequeue messages with error isolation.

        Args:
            batch_size: Number of messages to dequeue

        Returns:
            List of queue entries (empty list on error)
        """
        try:
            return self.queue.dequeue(batch_size=batch_size)
        except Exception as e:
            logger.error(f"Dequeue error: {e}", exc_info=True)
            return []

    def _deliver_entry(self, entry: Any) -> bool:
        """
        Deliver queue entry → log → mark state.

        Error isolation: Each step wrapped in try/except to prevent
        cascade failures. One entry failure doesn't stop processing.

        Args:
            entry: Queue entry with message data

        Returns:
            True if delivered, False otherwise
        """
        try:
            # Extract message data
            message = getattr(entry, 'message', None)
            queue_id = getattr(entry, 'queue_id', 'unknown')

            if not message:
                logger.warning(f"Entry {queue_id} missing message")
                self.queue.mark_failed(queue_id, "no_message")
                return False

            # FIXED: Extract recipient/content handling both dict and UnifiedMessage object
            # Supports concurrent calls from different sources (Discord, CLI, queue, etc.)
            if isinstance(message, dict):
                # Message is a dict (serialized format)
                recipient = message.get("recipient") or message.get("to")
                content = message.get("content")
                message_type_str = message.get(
                    "message_type") or message.get("type")
                sender = message.get("sender") or message.get("from", "SYSTEM")
                priority_str = message.get("priority", "regular")
                tags_list = message.get("tags", [])
                metadata = message.get("metadata", {})
            else:
                # Message is UnifiedMessage object (object format)
                recipient = getattr(message, "recipient", None)
                content = getattr(message, "content", None)
                message_type_attr = getattr(message, "message_type", None)
                if message_type_attr:
                    message_type_str = getattr(
                        message_type_attr, "value", None) or str(message_type_attr)
                else:
                    message_type_str = None
                sender = getattr(message, "sender", "SYSTEM")
                priority_attr = getattr(message, "priority", None)
                if priority_attr:
                    priority_str = getattr(
                        priority_attr, "value", None) or str(priority_attr)
                else:
                    priority_str = "regular"
                tags_attr = getattr(message, "tags", [])
                tags_list = [getattr(t, "value", None) or str(t)
                             for t in tags_attr] if tags_attr else []
                metadata = getattr(message, "metadata", {})

            if not recipient:
                logger.warning(f"Entry {queue_id} missing recipient")
                self.queue.mark_failed(queue_id, "missing_recipient")
                return False

            if not content:
                logger.warning(f"Entry {queue_id} missing content")
                self.queue.mark_failed(queue_id, "missing_content")
                return False

            # Route delivery with preserved message_type
            success = self._route_delivery(
                recipient, content, metadata, message_type_str, sender, priority_str, tags_list
            )

            if success:
                self.queue.mark_delivered(queue_id)
                if self.message_repository:
                    try:
                        self.message_repository.log_message(message)
                    except Exception:
                        pass  # Non-critical logging failure
                return True
            else:
                self.queue.mark_failed(queue_id, "delivery_failed")
                return False

        except Exception as e:
            queue_id = getattr(entry, 'queue_id', 'unknown')
            logger.error(f"Delivery error for {queue_id}: {e}", exc_info=True)
            self.queue.mark_failed(queue_id, str(e))
            return False

    def _route_delivery(
        self,
        recipient: str,
        content: str,
        metadata: dict = None,
        message_type_str: str = None,
        sender: str = "SYSTEM",
        priority_str: str = "regular",
        tags_list: list = None,
    ) -> bool:
        """
        Route message delivery with fallback logic.

        Primary: PyAutoGUI delivery via messaging core
        Backup: Inbox fallback when PyAutoGUI fails

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful, False otherwise
        """
        try:
            # Check if queue is full (skip PyAutoGUI if so)
            try:
                from ..utils.agent_queue_status import AgentQueueStatus
                queue_status = AgentQueueStatus()
                if queue_status.is_queue_full(recipient):
                    logger.warning(
                        f"Queue full for {recipient}, skipping PyAutoGUI, using inbox"
                    )
                    return self._deliver_fallback_inbox(recipient, content, metadata or {}, sender, priority_str)
            except ImportError:
                # Queue status utility not available, proceed normally
                pass
            except Exception as e:
                logger.debug(f"Error checking queue status: {e}")
                # Continue with normal flow

            # PRIMARY: Try PyAutoGUI delivery first
            success = self._deliver_via_core(
                recipient, content, metadata or {}, message_type_str, sender, priority_str, tags_list or []
            )
            if success:
                return True

            # BACKUP: Fallback to inbox when PyAutoGUI fails
            # (e.g., when Cursor queue is full with pending prompts)
            logger.warning(
                f"PyAutoGUI delivery failed for {recipient}, using inbox fallback"
            )
            return self._deliver_fallback_inbox(recipient, content, metadata or {}, sender, priority_str)
        except Exception as e:
            logger.error(f"Delivery routing error: {e}")
            # Last resort: try inbox fallback
            try:
                return self._deliver_fallback_inbox(recipient, content, metadata or {}, sender, priority_str)
            except Exception as fallback_error:
                logger.error(f"Inbox fallback also failed: {fallback_error}")
                return False

    def _deliver_via_core(
        self,
        recipient: str,
        content: str,
        metadata: dict = None,
        message_type_str: str = None,
        sender: str = "SYSTEM",
        priority_str: str = "regular",
        tags_list: list = None,
    ) -> bool:
        """
        Primary path: Unified messaging core (PyAutoGUI delivery or injected mock).

        Uses injected messaging_core if provided (for testing), otherwise uses real core.
        V3 Unified Imports: Uses src.core.messaging_core.send_message
        Keyboard control: Wraps delivery in keyboard_control context (only for real core)

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful, False otherwise
        """
        try:
            from .messaging_models_core import (
                UnifiedMessageType,
                UnifiedMessagePriority,
                UnifiedMessageTag,
            )

            # Parse message_type from string (preserve from queue entry)
            if message_type_str:
                try:
                    # Try to match enum value directly
                    message_type = UnifiedMessageType(message_type_str)
                except (ValueError, TypeError):
                    # Fallback: map string to enum
                    message_type_map = {
                        "captain_to_agent": UnifiedMessageType.CAPTAIN_TO_AGENT,
                        "agent_to_agent": UnifiedMessageType.AGENT_TO_AGENT,
                        # Fixed: Map to AGENT_TO_AGENT
                        "agent_to_captain": UnifiedMessageType.AGENT_TO_AGENT,
                        "system_to_agent": UnifiedMessageType.SYSTEM_TO_AGENT,
                        "human_to_agent": UnifiedMessageType.HUMAN_TO_AGENT,
                        "onboarding": UnifiedMessageType.ONBOARDING,
                        "text": UnifiedMessageType.TEXT,
                        "broadcast": UnifiedMessageType.BROADCAST,
                    }
                    message_type = message_type_map.get(
                        message_type_str.lower(), UnifiedMessageType.SYSTEM_TO_AGENT
                    )
                    logger.debug(
                        f"📍 Mapped message_type_str '{message_type_str}' to {message_type}")
            else:
                # Default based on sender/recipient if message_type not specified
                # Try to infer from sender/recipient
                if sender and recipient:
                    sender_upper = sender.upper()
                    recipient_upper = recipient.upper()

                    # Agent-to-Agent (including Agent-to-Captain - use AGENT_TO_AGENT)
                    if sender.startswith("Agent-") and recipient.startswith("Agent-"):
                        message_type = UnifiedMessageType.AGENT_TO_AGENT
                    # Agent-to-Captain (Agent-4) - use AGENT_TO_AGENT (not a separate type)
                    elif sender.startswith("Agent-") and recipient_upper in ["CAPTAIN", "AGENT-4"]:
                        # Fixed: Use AGENT_TO_AGENT, not non-existent AGENT_TO_CAPTAIN
                        message_type = UnifiedMessageType.AGENT_TO_AGENT
                    # Captain-to-Agent
                    elif sender_upper in ["CAPTAIN", "AGENT-4"]:
                        message_type = UnifiedMessageType.CAPTAIN_TO_AGENT
                    # System-to-Agent
                    else:
                        message_type = UnifiedMessageType.SYSTEM_TO_AGENT
                else:
                    # Default to SYSTEM_TO_AGENT if not specified
                    message_type = UnifiedMessageType.SYSTEM_TO_AGENT

                logger.debug(
                    f"📍 Inferred message_type={message_type} from sender={sender}, recipient={recipient}")

            # Parse priority
            try:
                priority = UnifiedMessagePriority(priority_str.lower())
            except (ValueError, TypeError):
                priority = UnifiedMessagePriority.REGULAR

            # Parse tags
            tags = []
            if tags_list:
                for tag_str in tags_list:
                    try:
                        if isinstance(tag_str, str):
                            tags.append(UnifiedMessageTag(tag_str.lower()))
                        else:
                            tags.append(tag_str)
                    except (ValueError, TypeError):
                        pass
            if not tags:
                tags = [UnifiedMessageTag.SYSTEM]

            # Use injected messaging core if provided (for stress testing/mocking)
            if self.messaging_core is not None:
                # Injected core (mock or adapter) - no keyboard control needed
                ok = self.messaging_core.send_message(
                    content=content,
                    sender=sender,
                    recipient=recipient,
                    message_type=message_type,
                    priority=priority,
                    tags=tags,
                    metadata=metadata or {},
                )
            else:
                # Default: Real messaging core with keyboard control
                from .messaging_core import send_message
                from .keyboard_control_lock import keyboard_control

                # Wrap in keyboard control to prevent race conditions
                with keyboard_control(f"queue_delivery::{recipient}"):
                    ok = send_message(
                        content=content,
                        sender=sender,
                        recipient=recipient,
                        message_type=message_type,
                        priority=priority,
                        tags=tags,
                        metadata=metadata or {},
                    )

            return ok

        except ImportError as e:
            logger.error(f"Import error in _deliver_via_core: {e}")
            return False
        except Exception as e:
            logger.error(f"Error in _deliver_via_core: {e}", exc_info=True)
            return False

    def _deliver_fallback_inbox(
        self, recipient: str, content: str, metadata: dict,
        sender: str = None, priority_str: str = None
    ) -> bool:
        """
        Backup path: Inbox file-based delivery.

        Used when PyAutoGUI delivery fails (e.g., Cursor queue full).

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata
            sender: Sender identifier (preserved from message)
            priority_str: Priority string (preserved from message)

        Returns:
            True if inbox delivery successful, False otherwise
        """
        try:
            from ..utils.inbox_utility import create_inbox_message

            # FIXED: Preserve actual sender and priority from message, not metadata
            actual_sender = sender or metadata.get("sender", "SYSTEM")
            actual_priority = priority_str or metadata.get(
                "priority", "normal")

            return create_inbox_message(
                recipient=recipient,
                content=content,
                sender=actual_sender,
                priority=actual_priority,
            )
        except ImportError:
            logger.warning("Inbox utility not available")
            return False
        except Exception as e:
            logger.error(f"Inbox delivery error: {e}", exc_info=True)
            return False
