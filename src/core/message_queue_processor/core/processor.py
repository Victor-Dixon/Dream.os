#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Message Queue Processor - Main Processor
========================================

Main processor orchestrator for message queue processing.
Uses extracted modules for parsing, validation, routing, error handling, and retries.

V2 Compliance: <200 lines (orchestrator only)
"""

import logging
import os
import time
from typing import Any, Optional

from ....core.message_queue import MessageQueue, QueueConfig
from ....core.message_queue_persistence import QueueEntry
from systems.output_flywheel.integration.status_json_integration import (
    StatusJsonIntegration,
)
from ..processing.message_parser import parse_message_data
from ..processing.message_validator import validate_message_data
from ...message_queue.processing.message_router import route_message_delivery
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
# Broadcast messages use longer delay to prevent routing race conditions
INTER_AGENT_DELAY_BROADCAST = 5.0  # Delay for broadcast messages (matches broadcast_helpers.py)


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
        self.output_flywheel_integration = self._init_output_flywheel_integration()
        self.output_flywheel_check_interval = float(
            os.getenv("OUTPUT_FLYWHEEL_STATUS_INTERVAL", "60")
        )
        self.next_output_flywheel_check = (
            time.time() + self.output_flywheel_check_interval
            if self.output_flywheel_integration
            else None
        )

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
                self._maybe_trigger_output_flywheel()
                # Dequeue batch of entries using MessageQueue interface
                try:
                    entries = self.queue.dequeue(batch_size)
                    if not entries:
                        # Fallback: try to load directly from persistence if queue interface fails
                        try:
                            all_entries = self.queue.persistence.load_entries()
                            pending_entries = [e for e in all_entries if getattr(e, 'status', '') == 'PENDING']
                            if pending_entries:
                                # Sort by priority (highest first) and take batch
                                pending_entries.sort(key=lambda x: getattr(x, 'priority_score', 0.5), reverse=True)
                                entries = pending_entries[:batch_size]
                                logger.info(f"Fallback dequeue: found {len(entries)} pending entries")
                        except Exception as fallback_e:
                            logger.warning(f"Fallback dequeue also failed: {fallback_e}")

                        if not entries:
                            if max_messages is None:
                                time.sleep(interval)
                                continue
                            break
                except Exception as e:
                    logger.error(f"Failed to dequeue messages: {e}")
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
                    
                    # Check if this is a broadcast message to use broadcast delay
                    message = getattr(entry, 'message', {})
                    message_type = message.get('message_type', '') if isinstance(message, dict) else ''
                    is_broadcast = message_type == 'broadcast'
                    delay_seconds = INTER_AGENT_DELAY_BROADCAST if is_broadcast else (INTER_AGENT_DELAY_SUCCESS if ok else INTER_AGENT_DELAY_FAILURE)

                    if ok:
                        # Extended pause after successful delivery to prevent routing race conditions
                        # Use broadcast delay for broadcast messages, otherwise use standard delay
                        time.sleep(delay_seconds)
                        # Production: Debug logging removed for performance
                        logger.debug(
                            f"✅ Delivery complete for {recipient}, waiting {delay_seconds}s before next agent{' (BROADCAST)' if is_broadcast else ''}")
                    else:
                        time.sleep(delay_seconds)  # Extended pause after failed delivery
                        # Production: Debug logging removed for performance
                        logger.debug(
                            f"⚠️ Delivery failed, waiting {delay_seconds}s for recovery before next agent{' (BROADCAST)' if is_broadcast else ''}")

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

    def _init_output_flywheel_integration(self) -> Optional[StatusJsonIntegration]:
        agent_id = os.getenv("OUTPUT_FLYWHEEL_AGENT_ID")
        if not agent_id:
            return None
        logger.info(
            "🔄 Output Flywheel integration enabled for %s",
            agent_id,
        )
        return StatusJsonIntegration(agent_id)

    def _maybe_trigger_output_flywheel(self) -> None:
        if not self.output_flywheel_integration:
            return

        now = time.time()
        if self.next_output_flywheel_check is None or now < self.next_output_flywheel_check:
            return

        try:
            session = self.output_flywheel_integration.check_and_trigger()
            if session and isinstance(session, dict):
                artifacts = session.get("artifacts", {})
                session_id = session.get("session_id")
                if artifacts:
                    self.output_flywheel_integration.update_status_with_artifacts(
                        artifacts,
                        session_id,
                    )
        except Exception as exc:
            logger.warning(
                "Output Flywheel integration check failed: %s",
                exc,
            )
        finally:
            self.next_output_flywheel_check = now + self.output_flywheel_check_interval

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
            is_valid, error_msg = validate_message_data(parsed)
            if not is_valid:
                self.queue.mark_failed(queue_id, error_msg)
                return False

            # Mark agent as delivering
            mark_agent_delivering(tracker, recipient, queue_id)

            # Route delivery
            success = route_message_delivery(
                recipient, content, metadata, message_type_str, sender, priority_str, tags_list,
                lambda r, c, m, mt, s, p, t: deliver_via_core(
                    r, c, m, mt, s, p, t),
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

            # Enhanced error handling with specific error messages
            error_details = {
                'KeyError': 'Missing required message field (likely message_type_str)',
                'AttributeError': 'Agent coordinate or window issue',
                'TimeoutError': 'PyAutoGUI operation timed out',
                'Exception': f'General delivery error: {str(e)}'
            }.get(type(e).__name__, f'Unexpected error: {str(e)}')

            # Update metadata with error details
            entry_metadata = getattr(entry, 'metadata', {})
            entry_metadata.update({
                'error_message': error_details,
                'error_type': type(e).__name__,
                'delivery_attempt': entry_metadata.get('delivery_attempts', 0) + 1,
                'last_error_time': time.time()
            })

            handle_delivery_error(
                queue_id, e, self.queue, tracker, recipient,
                self.performance_metrics, delivery_start_time, use_pyautogui, content
            )
            return False

    def process_message(self, message: Any) -> bool:
        """
        Process a single message (smoke test compatibility method).

        This method provides compatibility with smoke tests that expect
        individual message processing capability.
        """
        try:
            # Create a queue entry from the message
            entry = QueueEntry(
                queue_id="smoke_test",
                message={"content": message, "type": "smoke_test"},
                priority="normal",
                status="pending"
            )

            # Use the existing delivery logic
            return self._deliver_entry(entry)
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return False

    def enqueue_message(self, message: Any, priority: str = "normal") -> bool:
        """
        Enqueue a single message (smoke test compatibility method).

        This method provides compatibility with smoke tests that expect
        individual message enqueueing capability.
        """
        try:
            # Create a queue entry
            entry = QueueEntry(
                queue_id="smoke_test",
                message={"content": message, "type": "smoke_test"},
                priority=priority,
                status="pending"
            )

            # Add to queue
            self.queue.enqueue(entry)
            logger.info(f"Enqueued message with priority {priority}")
            return True
        except Exception as e:
            logger.error(f"Failed to enqueue message: {e}")
            return False


def main():
    """Main entry point for the message queue processor service."""
    import signal
    import sys

    # Create processor instance
    processor = MessageQueueProcessor()

    def signal_handler(signum, frame):
        """Handle shutdown signals."""
        logger.info("Received shutdown signal, stopping processor...")
        processor.running = False  # Set running to False to stop the loop
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        logger.info("Starting Message Queue Processor service...")
        # Run the processor (this will block until stopped)
        processor.process_queue()  # This runs the processing loop
    except Exception as e:
        logger.error(f"Message Queue Processor failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()