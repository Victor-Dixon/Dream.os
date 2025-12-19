#!/usr/bin/env python3
"""
Message Queue Processor - Main Processor
========================================

Main processor orchestrator for message queue processing.
Uses extracted modules for parsing, validation, routing, error handling, and retries.

V2 Compliance: <200 lines (orchestrator only)
"""

import logging
import time
from typing import Any, Optional

from ....core.message_queue import MessageQueue, QueueConfig
from ....core.message_queue_persistence import QueueEntry
from ..processing.message_parser import parse_message_data
from ..processing.message_validator import validate_message_data
from ..processing.message_router import route_message_delivery
from ..handlers.error_handler import handle_delivery_error
from ..handlers.retry_handler import (
    should_retry_delivery,
    handle_retry_failure,
    handle_retry_scheduled,
)
from ..utils.queue_utilities import (
    safe_dequeue,
    get_activity_tracker,
    mark_agent_delivering,
    mark_agent_inactive,
)

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
    """

    def __init__(
        self,
        queue: Optional[MessageQueue] = None,
        message_repository: Optional[Any] = None,
        config: Optional[QueueConfig] = None,
        messaging_core: Optional[Any] = None,
    ) -> None:
        """Initialize message queue processor."""
        self.config = config or QueueConfig()
        self.queue = queue or MessageQueue(config=self.config)
        self.message_repository = message_repository
        self.messaging_core = messaging_core
        self.running = False

        # Initialize performance metrics collector
        try:
            from src.core.message_queue_performance_metrics import MessageQueuePerformanceMetrics
            self.performance_metrics = MessageQueuePerformanceMetrics()
            self.performance_metrics.start_session()
        except Exception as e:
            logger.warning(f"Performance metrics not available: {e}")
            self.performance_metrics = None

    def process_queue(
        self,
        max_messages: Optional[int] = None,
        batch_size: int = 1,
        interval: float = 5.0,
    ) -> int:
        """Process queued messages in controlled batches."""
        self.running = True
        processed = 0

        try:
            while self.running:
                entries = safe_dequeue(self.queue, batch_size)
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

                    if ok:
                        # Extended pause after successful delivery
                        time.sleep(3.0)
                        logger.debug(
                            f"✅ Delivery complete for {getattr(entry, 'recipient', 'unknown')}, waiting 3.0s before next agent")
                    else:
                        time.sleep(5.0)  # Extended pause after failed delivery
                        logger.debug(
                            f"⚠️ Delivery failed, waiting 5.0s for recovery before next agent")

                if max_messages and processed >= max_messages:
                    break

        except KeyboardInterrupt:
            logger.info("🛑 Stopped by operator")
        except Exception as e:
            logger.error(f"Fatal queue loop error: {e}", exc_info=True)
        finally:
            self.running = False

            if self.performance_metrics:
                session_summary = self.performance_metrics.end_session()
                logger.info(f"📊 Performance metrics: {session_summary}")

            logger.info(f"✅ Queue processor complete: {processed} delivered")

        return processed

    def _deliver_entry(self, entry: Any) -> bool:
        """Deliver queue entry using extracted modules."""
        tracker = get_activity_tracker()
        queue_id = getattr(entry, 'queue_id', 'unknown')
        message = getattr(entry, 'message', None)

        # Start performance tracking
        delivery_start_time = None
        if self.performance_metrics:
            delivery_start_time = self.performance_metrics.start_delivery_tracking(
                queue_id)

        try:
            # Check retry status
            entry_metadata = getattr(entry, 'metadata', {})
            delivery_attempts = entry_metadata.get('delivery_attempts', 0)
            max_retries = 3

            if delivery_attempts >= max_retries:
                logger.warning(
                    f"Entry {queue_id} exceeded max retries ({max_retries})")
                self.queue.mark_failed(
                    queue_id, f"max_retries_exceeded ({max_retries})")
                return False

            if not message:
                logger.warning(f"Entry {queue_id} missing message")
                self.queue.mark_failed(queue_id, "no_message")
                return False

            # Parse message data
            parsed = parse_message_data(message)
            recipient = parsed["recipient"]
            content = parsed["content"]
            message_type_str = parsed["message_type_str"]
            sender = parsed["sender"]
            priority_str = parsed["priority_str"]
            tags_list = parsed["tags_list"]
            metadata = parsed["metadata"]

            # Validate message data
            is_valid, error_msg = validate_message_data(
                queue_id, recipient, content, tracker)
            if not is_valid:
                self.queue.mark_failed(queue_id, error_msg)
                return False

            # Mark agent as delivering
            mark_agent_delivering(tracker, recipient, queue_id)

            # Route delivery
            success = route_message_delivery(
                recipient, content, metadata, message_type_str, sender, priority_str, tags_list,
                self._deliver_via_core,
                self._deliver_fallback_inbox,
            )

            # Get use_pyautogui flag
            use_pyautogui = True
            if isinstance(metadata, dict):
                use_pyautogui = metadata.get("use_pyautogui", True)
            elif hasattr(entry, 'metadata') and isinstance(entry.metadata, dict):
                use_pyautogui = entry.metadata.get("use_pyautogui", True)

            # Record performance metrics
            if self.performance_metrics and delivery_start_time:
                delivery_method = 'pyautogui' if use_pyautogui else 'inbox'
                content_len = len(content) if content else 0
                attempt_num = entry_metadata.get('delivery_attempts', 0) + 1
                retry_delay = entry_metadata.get('next_retry_delay')

                self.performance_metrics.end_delivery_tracking(
                    queue_id=queue_id,
                    recipient=recipient,
                    delivery_method=delivery_method,
                    success=success,
                    start_time=delivery_start_time,
                    attempt_number=attempt_num,
                    content_length=content_len,
                    retry_delay=retry_delay
                )

            if success:
                self.queue.mark_delivered(queue_id)
                if self.message_repository:
                    try:
                        self.message_repository.log_message(message)
                    except Exception:
                        pass
                mark_agent_inactive(tracker, recipient)
                return True
            else:
                # Handle retry logic
                should_retry, attempt_num, delay = should_retry_delivery(
                    queue_id, entry, self.queue)
                if should_retry:
                    handle_retry_scheduled(
                        queue_id, attempt_num, delay, self.queue)
                else:
                    handle_retry_failure(
                        queue_id, attempt_num, self.queue, tracker, recipient)
                mark_agent_inactive(tracker, recipient)
                return False

        except Exception as e:
            use_pyautogui = True
            content = None
            if 'parsed' in locals():
                content = parsed.get("content")
                metadata = parsed.get("metadata", {})
                if isinstance(metadata, dict):
                    use_pyautogui = metadata.get("use_pyautogui", True)

            handle_delivery_error(
                queue_id, e, self.queue, tracker, recipient,
                self.performance_metrics, delivery_start_time, use_pyautogui, content
            )
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
        """Primary path: Unified messaging core (PyAutoGUI delivery or injected mock)."""
        try:
            from src.core.messaging_models_core import (
                UnifiedMessageType,
                UnifiedMessagePriority,
                UnifiedMessageTag,
            )

            # Parse message_type
            if message_type_str:
                try:
                    message_type = UnifiedMessageType(message_type_str)
                except (ValueError, TypeError):
                    message_type_map = {
                        "captain_to_agent": UnifiedMessageType.CAPTAIN_TO_AGENT,
                        "agent_to_agent": UnifiedMessageType.AGENT_TO_AGENT,
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
            else:
                if sender and recipient:
                    if sender.startswith("Agent-") and recipient.startswith("Agent-"):
                        message_type = UnifiedMessageType.AGENT_TO_AGENT
                    elif sender.startswith("Agent-") and recipient.upper() in ["CAPTAIN", "AGENT-4"]:
                        message_type = UnifiedMessageType.AGENT_TO_AGENT
                    elif sender.upper() in ["CAPTAIN", "AGENT-4"]:
                        message_type = UnifiedMessageType.CAPTAIN_TO_AGENT
                    else:
                        message_type = UnifiedMessageType.SYSTEM_TO_AGENT
                else:
                    message_type = UnifiedMessageType.SYSTEM_TO_AGENT

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

            # Use injected messaging core if provided
            if self.messaging_core is not None:
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
                from ....core.messaging_core import send_message
                from ....core.keyboard_control_lock import keyboard_control

                # Preserve message category in metadata
                delivery_metadata = dict(metadata) if metadata else {}
                if isinstance(metadata, dict):
                    category_str = metadata.get('message_category')
                    if category_str:
                        try:
                            from src.core.messaging_models_core import MessageCategory
                            category_from_meta = MessageCategory(
                                category_str.lower())
                            delivery_metadata['message_category'] = category_from_meta.value
                        except (ValueError, AttributeError):
                            pass

                with keyboard_control(f"queue_delivery::{recipient}"):
                    ok = send_message(
                        content=content,
                        sender=sender,
                        recipient=recipient,
                        message_type=message_type,
                        priority=priority,
                        tags=tags,
                        metadata=delivery_metadata,
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
        """Backup path: Inbox file-based delivery."""
        try:
            from ....utils.inbox_utility import create_inbox_message

            actual_sender = sender or metadata.get("sender", "SYSTEM")
            actual_priority = priority_str or metadata.get(
                "priority", "normal")

            success = create_inbox_message(
                recipient=recipient,
                content=content,
                sender=actual_sender,
                priority=actual_priority,
            )

            if not success:
                logger.error(f"❌ Inbox delivery failed for {recipient}")
                return False

            logger.info(f"✅ Inbox delivery verified for {recipient}")
            return True
        except ImportError:
            logger.warning("Inbox utility not available")
            return False
        except Exception as e:
            logger.error(f"Inbox delivery error: {e}", exc_info=True)
            return False
