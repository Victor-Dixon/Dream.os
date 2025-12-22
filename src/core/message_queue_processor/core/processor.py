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
from ..processing.delivery_inbox import deliver_fallback_inbox
from ..processing.delivery_core import deliver_via_core
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

# Inter-agent delay constants to prevent race conditions in routing
# Increased delays to ensure PyAutoGUI routing stabilizes between agents
INTER_AGENT_DELAY_SUCCESS = 4.5  # Delay after successful delivery (increased from 3.0s)
INTER_AGENT_DELAY_FAILURE = 6.5  # Delay after failed delivery (increased from 5.0s)


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
            from ...message_queue_performance_metrics import MessageQueuePerformanceMetrics
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
                    recipient = getattr(entry, 'recipient', 'unknown')

                    # #region agent log
                    import json
                    from pathlib import Path
                    log_path = Path("d:\\Agent_Cellphone_V2_Repository\\.cursor\\debug.log")
                    delay_start = time.time()
                    try:
                        with open(log_path, 'a', encoding='utf-8') as f:
                            f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "processor.py:107", "message": "Before inter-agent delay", "data": {"recipient": recipient, "success": ok, "delay_seconds": INTER_AGENT_DELAY_SUCCESS if ok else INTER_AGENT_DELAY_FAILURE}, "timestamp": int(time.time() * 1000)}) + "\n")
                    except: pass
                    # #endregion

                    if ok:
                        # Extended pause after successful delivery to prevent routing race conditions
                        time.sleep(INTER_AGENT_DELAY_SUCCESS)
                        # #region agent log
                        delay_end = time.time()
                        actual_delay = delay_end - delay_start
                        try:
                            with open(log_path, 'a', encoding='utf-8') as f:
                                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "processor.py:121", "message": "After inter-agent delay (success)", "data": {"recipient": recipient, "expected_delay": INTER_AGENT_DELAY_SUCCESS, "actual_delay": round(actual_delay, 2)}, "timestamp": int(time.time() * 1000)}) + "\n")
                        except: pass
                        # #endregion
                        logger.debug(
                            f"✅ Delivery complete for {recipient}, waiting {INTER_AGENT_DELAY_SUCCESS}s before next agent")
                    else:
                        time.sleep(INTER_AGENT_DELAY_FAILURE)  # Extended pause after failed delivery
                        # #region agent log
                        delay_end = time.time()
                        actual_delay = delay_end - delay_start
                        try:
                            with open(log_path, 'a', encoding='utf-8') as f:
                                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "processor.py:133", "message": "After inter-agent delay (failure)", "data": {"recipient": recipient, "expected_delay": INTER_AGENT_DELAY_FAILURE, "actual_delay": round(actual_delay, 2)}, "timestamp": int(time.time() * 1000)}) + "\n")
                        except: pass
                        # #endregion
                        logger.debug(
                            f"⚠️ Delivery failed, waiting {INTER_AGENT_DELAY_FAILURE}s for recovery before next agent")

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
                lambda r, c, m, mt, s, p, t: deliver_via_core(
                    r, c, m, mt, s, p, t, self.messaging_core),
                deliver_fallback_inbox,
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
