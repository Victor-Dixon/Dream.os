#!/usr/bin/env python3
"""
Error Handler - Handle Message Delivery Errors
==============================================

Handles errors during message delivery processing.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def handle_delivery_error(
    queue_id: str,
    error: Exception,
    queue: Any,
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
