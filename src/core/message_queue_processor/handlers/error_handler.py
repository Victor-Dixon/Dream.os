#!/usr/bin/env python3
"""
Error Handler for Message Queue Processing
==========================================

Handles delivery errors and logging.
"""

import logging
from typing import Any, Optional
import time

logger = logging.getLogger(__name__)


def handle_delivery_error(
    queue_id: str,
    error: Exception,
    queue: Any,
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