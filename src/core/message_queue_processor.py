#!/usr/bin/env python3
"""
Message Queue Processor — V3 Compliant
======================================

Hard-boundary message delivery engine with deterministic processing loop.
PyAutoGUI primary delivery with inbox fallback when primary fails.

V3 Constraints: <400 lines, single responsibility, pure processing engine
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

from __future__ import annotations

import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..utils.swarm_time import format_swarm_timestamp

from .keyboard_control_lock import keyboard_control
from .message_queue import MessageQueue, QueueConfig

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
        self.messaging_core = messaging_core  # Injected core (None = use default real core)
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
            max_messages: None = continuous runner, int = process N then stop
            batch_size: Number of items per dequeue
            interval: Sleep between cycles when continuous

        Returns:
            Number of messages processed
        """
        self.running = True
        processed = 0
        logger.info("🔄 Queue processor booted")

        try:
            while self.running:
                if max_messages and processed >= max_messages:
                    break

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
            True if delivery successful, False otherwise
        """
        try:
            msg = getattr(entry, "message", None)
            if not msg:
                logger.warning(f"Entry {entry.queue_id} missing message")
                self.queue.mark_failed(entry.queue_id, "no_message")
                return False

            # Extract message fields with fallbacks
            recipient = msg.get("recipient") or msg.get("to")
            content = msg.get("content") or msg.get("message", "")
            sender = msg.get("sender") or msg.get("from", "SYSTEM")
            metadata = msg.get("metadata", {})

            if not recipient:
                logger.warning(f"Entry {entry.queue_id} missing recipient")
                self.queue.mark_failed(entry.queue_id, "missing_recipient")
                return False

            if not content:
                logger.warning(f"Entry {entry.queue_id} missing content")
                self.queue.mark_failed(entry.queue_id, "missing_content")
                return False

            # VALIDATION: Check if recipient has pending multi-agent request
            # This validates at queue processor level (defense in depth)
            # Messages from other sources or queued before validation will be caught here
            try:
                from ..core.multi_agent_request_validator import get_multi_agent_validator

                validator = get_multi_agent_validator()
                can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                    agent_id=recipient,
                    target_recipient=sender,  # Allow if responding to request sender
                    message_content=content
                )

                if not can_send:
                    # Recipient has pending request - block delivery
                    logger.warning(
                        f"❌ Queue delivery blocked for {recipient} - pending multi-agent request"
                    )
                    self.queue.mark_failed(
                        entry.queue_id,
                        f"blocked_pending_request: {pending_info.get('collector_id', 'unknown') if pending_info else 'unknown'}"
                    )

                    # Store error message in entry metadata for visibility
                    if hasattr(entry, 'metadata'):
                        entry.metadata = entry.metadata or {}
                        entry.metadata["blocked_reason"] = "pending_multi_agent_request"
                        entry.metadata["blocked_error_message"] = error_message

                    return False

                # If responding to request sender, auto-route to collector
                if pending_info and sender == pending_info["sender"]:
                    try:
                        from ..core.multi_agent_responder import get_multi_agent_responder
                        responder = get_multi_agent_responder()

                        # Auto-submit response to collector
                        collector_id = pending_info["collector_id"]
                        responder.submit_response(
                            collector_id, recipient, content)

                        logger.info(
                            f"✅ Auto-routed response from {recipient} to collector {collector_id}"
                        )
                        # Continue with normal delivery (message still sent)
                    except Exception as e:
                        logger.debug(
                            f"Error auto-routing response in queue: {e}")
                        # Continue with normal delivery

            except ImportError:
                # Validator not available, proceed normally
                pass
            except Exception as e:
                logger.debug(f"Error validating recipient in queue: {e}")
                # Continue with normal flow (don't block on validation errors)

            # Route delivery: unified messaging core only
            ok = self._route_delivery(recipient, content, metadata)

            # Mark queue state
            if ok:
                self.queue.mark_delivered(entry.queue_id)
            else:
                self.queue.mark_failed(entry.queue_id, "delivery_failed")

            # Log to repository (non-blocking)
            self._log_delivery(entry, sender, recipient, content, ok)

            return ok

        except Exception as e:
            logger.error(
                f"Unhandled entry error ({entry.queue_id}): {e}", exc_info=True
            )
            try:
                self.queue.mark_failed(entry.queue_id, "processor_exception")
            except Exception:
                logger.error(
                    f"Failed to mark entry {entry.queue_id} as failed")
            return False

    def _route_delivery(self, recipient: str, content: str, metadata: dict = None) -> bool:
        """
        Route delivery: PyAutoGUI primary, inbox fallback.

        Deterministic pipeline:
        1. Check if agent's Cursor queue is full (skip PyAutoGUI if full)
        2. Try unified messaging core (PyAutoGUI delivery) - PRIMARY
        3. On failure, fallback to inbox file delivery - BACKUP
           (Used when Cursor queue is full or PyAutoGUI unavailable)

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful (either path), False otherwise
        """
        try:
            # Check if agent's Cursor queue is marked as full
            # IMPORTANT: PyAutoGUI doesn't fail when queue is full - it successfully queues
            # But if agent already has many messages queued, adding more makes them fall behind
            # So we skip PyAutoGUI and use inbox to prevent queue buildup
            try:
                from ..utils.agent_queue_status import AgentQueueStatus

                if AgentQueueStatus.is_full(recipient):
                    logger.info(
                        f"⏭️  Skipping PyAutoGUI for {recipient} (queue has many messages), using inbox to prevent further delay"
                    )
                    return self._deliver_fallback_inbox(recipient, content, metadata or {})
            except ImportError:
                # Queue status utility not available, proceed normally
                pass
            except Exception as e:
                logger.debug(f"Error checking queue status: {e}")
                # Continue with normal flow

            # PRIMARY: Try PyAutoGUI delivery first
            success = self._deliver_via_core(
                recipient, content, metadata or {})
            if success:
                return True

            # BACKUP: Fallback to inbox when PyAutoGUI fails
            # (e.g., when Cursor queue is full with pending prompts)
            logger.warning(
                f"PyAutoGUI delivery failed for {recipient}, using inbox fallback"
            )
            return self._deliver_fallback_inbox(recipient, content, metadata or {})
        except Exception as e:
            logger.error(f"Delivery routing error: {e}")
            # Last resort: try inbox fallback
            try:
                return self._deliver_fallback_inbox(recipient, content, metadata or {})
            except Exception as fallback_error:
                logger.error(f"Inbox fallback also failed: {fallback_error}")
                return False

    def _deliver_via_core(self, recipient: str, content: str, metadata: dict = None) -> bool:
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

            # Use injected messaging core if provided (for stress testing/mocking)
            if self.messaging_core is not None:
                # Injected core (mock or adapter) - no keyboard control needed
                ok = self.messaging_core.send_message(
                    content=content,
                    sender="SYSTEM",
                    recipient=recipient,
                    message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                    priority=UnifiedMessagePriority.REGULAR,
                    tags=[UnifiedMessageTag.SYSTEM],
                    metadata=metadata or {},
                )
            else:
                # Default: Real messaging core with keyboard control
                from .messaging_core import send_message

                # Wrap in keyboard control to prevent race conditions
                with keyboard_control(f"queue_delivery::{recipient}"):
                    ok = send_message(
                        content=content,
                        sender="SYSTEM",
                        recipient=recipient,
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                        priority=UnifiedMessagePriority.REGULAR,
                        tags=[UnifiedMessageTag.SYSTEM],
                        metadata=metadata or {},
                    )

            if ok:
                logger.info(f"📨 Core delivered → {recipient}")
            else:
                logger.warning(f"⚠️ Core delivery failed → {recipient}")

            return ok

        except ImportError as e:
            logger.warning(f"Messaging core unavailable: {e}")
            return False
        except Exception as e:
            logger.error(f"Core delivery error: {e}", exc_info=True)
            return False

    def _deliver_fallback_inbox(self, recipient: str, content: str, metadata: dict = None) -> bool:
        """
        Fallback path: Write to workspace inbox when PyAutoGUI fails.

        Used when:
        - PyAutoGUI delivery fails
        - Cursor queue is full (agent has pending prompts)
        - Keyboard lock timeout
        - Any PyAutoGUI error

        This ensures messages are never lost even when primary delivery fails.

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if file written successfully, False otherwise
        """
        try:
            from src.utils.inbox_utility import create_inbox_message

            # Extract sender from metadata if available
            sender = metadata.get("sender", "SYSTEM") if metadata else "SYSTEM"
            priority = metadata.get(
                "priority", "normal") if metadata else "normal"

            # Use inbox utility for file creation
            success = create_inbox_message(
                recipient=recipient,
                sender=sender,
                content=content,
                priority=priority,
                message_type="text",
                tags=["queue_fallback", "system"]
            )

            if success:
                logger.info(f"📥 Inbox fallback delivered → {recipient}")
            else:
                logger.error(f"❌ Inbox fallback failed → {recipient}")

            return success

        except Exception as e:
            logger.error(f"Inbox fallback failed: {e}", exc_info=True)
            return False

    def _log_delivery(
        self,
        entry: Any,
        sender: str,
        recipient: str,
        content: str,
        success: bool,
    ) -> None:
        """
        Log message delivery to repository (non-blocking).

        Enhanced logging with error isolation. Repository failures
        don't affect delivery status.

        Args:
            entry: Queue entry that was processed
            sender: Message sender
            recipient: Message recipient
            content: Message content
            success: Whether delivery was successful
        """
        if not self.message_repository:
            return

        try:
            self.message_repository.log_message(
                queue_id=entry.queue_id,
                from_agent=sender,
                to_agent=recipient,
                content=content[:200],  # Truncate for storage
                status="delivered" if success else "failed",
                timestamp=format_swarm_timestamp(),
            )
        except Exception as e:
            logger.warning(f"Repo log failure (non-blocking): {e}")

    @staticmethod
    def main() -> None:
        """CLI entry point for running processor as module."""
        max_messages: Optional[int] = None
        if len(sys.argv) > 1:
            try:
                max_messages = int(sys.argv[1])
            except ValueError:
                logger.warning(f"Invalid max_messages arg: {sys.argv[1]}")

        processor = MessageQueueProcessor()
        processor.process_queue(max_messages=max_messages, batch_size=1)


if __name__ == "__main__":
    MessageQueueProcessor.main()
