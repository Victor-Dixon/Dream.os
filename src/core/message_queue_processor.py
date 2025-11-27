#!/usr/bin/env python3
"""
Message Queue Processor — V3 Compliant
======================================

Hard-boundary message delivery engine with deterministic processing loop.
Unified messaging core integration with inbox fallback path.

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

from ..utils.swarm_time import format_swarm_timestamp, format_swarm_timestamp_filename, get_swarm_time_display

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
    • Inbox fallback on delivery failure

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
    ) -> None:
        """Initialize message queue processor.

        Args:
            queue: MessageQueue instance (creates default if None)
            message_repository: MessageRepository for logging (optional)
            config: QueueConfig instance (creates default if None)
        """
        self.config = config or QueueConfig()
        self.queue = queue or MessageQueue(config=self.config)
        self.message_repository = message_repository
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

            # Route delivery: unified core → inbox fallback
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
                logger.error(f"Failed to mark entry {entry.queue_id} as failed")
            return False

    def _route_delivery(self, recipient: str, content: str, metadata: dict = None) -> bool:
        """
        Route delivery: Attempt unified messaging → fallback inbox.

        Deterministic pipeline:
        1. Try unified messaging core (PyAutoGUI delivery)
        2. On failure, fallback to inbox file delivery

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful (either path), False otherwise
        """
        try:
            return self._deliver_via_core(recipient, content, metadata or {})
        except Exception as e:
            logger.warning(
                f"Core delivery failed, attempting inbox fallback: {e}"
            )
            return self._deliver_fallback_inbox(recipient, content)

    def _deliver_via_core(self, recipient: str, content: str, metadata: dict = None) -> bool:
        """
        Primary path: Unified messaging core (PyAutoGUI delivery).

        V3 Unified Imports: Uses src.core.messaging_core.send_message
        Keyboard control: Wraps delivery in keyboard_control context

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful, False otherwise
        """
        try:
            from .messaging_core import send_message
            from .messaging_models_core import (
                UnifiedMessageType,
                UnifiedMessagePriority,
                UnifiedMessageTag,
            )

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

    def _deliver_fallback_inbox(self, recipient: str, content: str) -> bool:
        """
        Fallback path: Write to workspace inbox.

        Used when unified messaging core is unavailable or fails.
        Creates markdown file in agent's inbox directory.

        Args:
            recipient: Agent ID to deliver to
            content: Message content

        Returns:
            True if file written successfully, False otherwise
        """
        try:
            inbox = Path(f"agent_workspaces/{recipient}/inbox")
            inbox.mkdir(parents=True, exist_ok=True)

            ts = format_swarm_timestamp_filename()
            file = inbox / f"QUEUE_MESSAGE_{ts}.md"

            file.write_text(
                self._format_inbox_message(recipient, content),
                encoding="utf-8",
            )

            logger.info(f"📥 Inbox delivered → {recipient}")
            return True

        except Exception as e:
            logger.error(f"Inbox fallback failed: {e}", exc_info=True)
            return False

    @staticmethod
    def _format_inbox_message(recipient: str, content: str) -> str:
        """Format message for inbox file delivery.

        Args:
            recipient: Agent ID
            content: Message content

        Returns:
            Formatted markdown string
        """
        return f"""# Queue Message

**From**: SYSTEM  
**To**: {recipient}  
**Timestamp**: {get_swarm_time_display()}

---

{content}

---

*Delivered via queue processor (fallback path)*  
"""

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
