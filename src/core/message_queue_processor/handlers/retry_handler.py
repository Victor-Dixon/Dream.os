#!/usr/bin/env python3
"""
Retry Handler for Message Queue Processing
==========================================

Handles retry logic for failed message deliveries.
"""

import logging
from typing import Any, Tuple, Optional
import time
import random

logger = logging.getLogger(__name__)


def should_retry_delivery(queue_id: str, entry: Any, queue: Any) -> Tuple[bool, int, float]:
    """
    Determine if a failed delivery should be retried and calculate retry parameters.

    Args:
        queue_id: Unique identifier for the queue entry
        entry: Queue entry that failed to deliver
        queue: Queue object for checking retry metadata

    Returns:
        Tuple of (should_retry: bool, attempt_num: int, delay_seconds: float)
    """
    # Extract retry metadata from entry
    metadata = getattr(entry, 'metadata', {}) if hasattr(entry, 'metadata') else {}
    retry_count = metadata.get('retry_count', 0)
    max_retries = metadata.get('max_retries', 3)

    # Check if we've exceeded max retries
    if retry_count >= max_retries:
        logger.warning(f"🚫 Max retries ({max_retries}) exceeded for queue_id: {queue_id}")
        return False, retry_count, 0.0

    # Calculate exponential backoff with jitter
    attempt_num = retry_count + 1
    base_delay = min(30 * (2 ** retry_count), 300)  # Max 5 minutes
    jitter = random.uniform(0.5, 1.5)  # Add randomness to prevent thundering herd
    delay = base_delay * jitter

    logger.info(f"🔄 Scheduling retry {attempt_num}/{max_retries} for queue_id: {queue_id} in {delay:.1f}s")

    return True, attempt_num, delay


def handle_retry_scheduled(queue_id: str, attempt_num: int, delay: float, queue: Any) -> None:
    """
    Handle scheduling of a retry attempt.

    Args:
        queue_id: Unique identifier for the queue entry
        attempt_num: The retry attempt number
        delay: Delay in seconds before retry
        queue: Queue object for requeue operations
    """
    logger.info(f"📅 Retry {attempt_num} scheduled for queue_id: {queue_id} in {delay:.1f} seconds")

    # Update retry metadata and requeue with delay
    try:
        # This would typically involve updating the queue entry metadata
        # and potentially using a delay queue or scheduled retry mechanism
        # For now, we'll log the scheduling
        retry_time = time.time() + delay
        logger.info(f"   Retry scheduled for: {time.strftime('%H:%M:%S', time.localtime(retry_time))}")

        # In a full implementation, this would:
        # 1. Update the entry's retry_count in metadata
        # 2. Requeue the entry with a delay or timestamp
        # 3. Possibly use a separate retry queue

    except Exception as e:
        logger.error(f"Failed to schedule retry for queue_id {queue_id}: {e}")


def handle_retry_failure(queue_id: str, attempt_num: int, queue: Any, tracker: Any, recipient: str) -> None:
    """
    Handle final retry failure - no more retries will be attempted.

    Args:
        queue_id: Unique identifier for the queue entry
        attempt_num: The final retry attempt number
        queue: Queue object for potential dead letter queue operations
        tracker: Agent activity tracker
        recipient: Agent that failed to receive the message
    """
    logger.error(f"💀 All retries exhausted for queue_id: {queue_id} (attempt {attempt_num})")
    logger.error(f"   Final recipient: {recipient}")

    # Mark agent as permanently inactive for this message
    if tracker and hasattr(tracker, 'mark_inactive'):
        try:
            tracker.mark_inactive(recipient)
            logger.info(f"   Marked agent {recipient} as permanently inactive")
        except Exception as tracker_error:
            logger.warning(f"Failed to mark agent permanently inactive: {tracker_error}")

    # In a full implementation, this would:
    # 1. Move the message to a dead letter queue
    # 2. Send failure notifications
    # 3. Update monitoring dashboards
    # 4. Possibly trigger escalation procedures

    logger.warning(f"   Message {queue_id} moved to dead letter queue (simulated)")
    # TODO: Implement actual dead letter queue functionality