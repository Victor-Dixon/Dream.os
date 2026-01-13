#!/usr/bin/env python3
"""
<<<<<<< HEAD
Error Handler for Message Queue Processing
==========================================

Handles delivery errors and logging.
=======
<!-- SSOT Domain: core -->

Error Handler - Handle Message Delivery Errors
==============================================

Handles errors during message delivery processing.
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
"""

import logging
from typing import Any, Optional
<<<<<<< HEAD
import time
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

logger = logging.getLogger(__name__)


def handle_delivery_error(
    queue_id: str,
    error: Exception,
    queue: Any,
<<<<<<< HEAD
    tracker: Any,
    recipient: str,
    performance_metrics: Any,
    delivery_start_time: float,
    use_pyautogui: bool,
    content: Any
) -> None:
    """
    Handle delivery error with comprehensive logging and metrics.

    Args:
        queue_id: Unique identifier for the queue entry
        error: The exception that occurred
        queue: Queue object for potential requeue operations
        tracker: Agent activity tracker
        recipient: Agent that was supposed to receive the message
        performance_metrics: Performance metrics collector
        delivery_start_time: Timestamp when delivery started
        use_pyautogui: Whether PyAutoGUI was used in delivery attempt
        content: The message content that failed to deliver
    """
    delivery_duration = time.time() - delivery_start_time

    # Log comprehensive error information
    logger.error(f"🚨 Message delivery failed for queue_id: {queue_id}")
    logger.error(f"   Recipient: {recipient}")
    logger.error(f"   Error: {type(error).__name__}: {str(error)}")
    logger.error(f"   Delivery time: {delivery_duration:.2f}s")
    logger.error(f"   Used PyAutoGUI: {use_pyautogui}")

    # Record error in performance metrics if available
    if performance_metrics and hasattr(performance_metrics, 'record_delivery_error'):
        try:
            performance_metrics.record_delivery_error(
                queue_id=queue_id,
                recipient=recipient,
                error_type=type(error).__name__,
                error_message=str(error),
                delivery_duration=delivery_duration,
                used_pyautogui=use_pyautogui
            )
        except Exception as metrics_error:
            logger.warning(f"Failed to record delivery error metrics: {metrics_error}")

    # Log content summary (truncated for security)
    content_summary = str(content)[:200] + "..." if len(str(content)) > 200 else str(content)
    logger.error(f"   Content summary: {content_summary}")

    # Mark agent as inactive due to delivery failure
    if tracker and hasattr(tracker, 'mark_inactive'):
        try:
            tracker.mark_inactive(recipient)
            logger.info(f"   Marked agent {recipient} as inactive due to delivery failure")
        except Exception as tracker_error:
            logger.warning(f"Failed to mark agent inactive: {tracker_error}")
=======
    tracker: Optional[Any] = None,
    recipient: Optional[str] = None,
    performance_metrics: Optional[Any] = None,
    delivery_start_time: Optional[float] = None,
    use_pyautogui: bool = True,
    content: Optional[str] = None,
) -> None:
    """
    Handle delivery error and update queue state.
    
    Args:
        queue_id: Queue entry ID
        error: Exception that occurred
        queue: MessageQueue instance
        tracker: Optional activity tracker
        recipient: Recipient identifier
        performance_metrics: Optional performance metrics collector
        delivery_start_time: Optional delivery start time
        use_pyautogui: Whether PyAutoGUI was used
        content: Message content
    """
    logger.error(f"Delivery error for {queue_id}: {error}", exc_info=True)
    
    # Record performance metrics for error case
    if performance_metrics and delivery_start_time:
        try:
            delivery_method = 'pyautogui' if use_pyautogui else 'inbox'
            content_len = len(content) if content else 0
            entry_metadata = getattr(error, 'metadata', {}) if hasattr(error, 'metadata') else {}
            attempt_num = entry_metadata.get('delivery_attempts', 0) + 1
            
            performance_metrics.end_delivery_tracking(
                queue_id=queue_id,
                recipient=recipient or 'unknown',
                delivery_method=delivery_method,
                success=False,
                start_time=delivery_start_time,
                attempt_number=attempt_num,
                content_length=content_len
            )
        except Exception:
            pass  # Non-critical metrics failure
    
    queue.mark_failed(queue_id, str(error))
    
    # Mark agent as inactive on error
    if tracker and recipient and recipient.startswith("Agent-"):
        try:
            tracker.mark_inactive(recipient)
        except Exception:
            pass  # Non-critical tracking failure
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
