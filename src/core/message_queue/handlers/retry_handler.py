#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Retry Handler - Handle Message Delivery Retries
===============================================

Handles retry logic for failed message deliveries with exponential backoff.
"""

import logging
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Exponential backoff delays: 5s, 15s, 45s
BACKOFF_DELAYS = [5.0, 15.0, 45.0]
MAX_RETRIES = 3


def should_retry_delivery(
    queue_id: str,
    entry: Any,
    queue: Any,
) -> tuple[bool, int, float]:
    """
    Check if delivery should be retried and calculate backoff delay.

    Args:
        queue_id: Queue entry ID
        entry: Queue entry
        queue: MessageQueue instance

    Returns:
        Tuple of (should_retry, attempt_number, delay_seconds)
    """
    entry_metadata = getattr(entry, 'metadata', {})
    current_attempts = entry_metadata.get('delivery_attempts', 0)
    new_attempts = current_attempts + 1

    # If already exceeded max retries, don't retry
    if new_attempts >= MAX_RETRIES:
        logger.warning(
            f"Entry {queue_id} exceeded max retries ({MAX_RETRIES}), "
            f"marking as permanently failed"
        )
        queue.mark_failed(queue_id, f"max_retries_exceeded ({MAX_RETRIES})")
        return False, new_attempts, 0.0

    # Calculate exponential backoff delay
    delay = BACKOFF_DELAYS[min(new_attempts - 1, len(BACKOFF_DELAYS) - 1)]

    # Update entry metadata with retry info
    if not hasattr(entry, 'metadata'):
        entry.metadata = {}
    entry.metadata['delivery_attempts'] = new_attempts
    entry.metadata['last_retry_time'] = datetime.now().isoformat()
    entry.metadata['next_retry_delay'] = delay

    return True, new_attempts, delay


def handle_retry_failure(
    queue_id: str,
    attempt_number: int,
    queue: Any,
    tracker: Optional[Any] = None,
    recipient: Optional[str] = None,
) -> None:
    """
    Handle permanent retry failure after max attempts.

    Args:
        queue_id: Queue entry ID
        attempt_number: Number of attempts made
        queue: MessageQueue instance
        tracker: Optional activity tracker
        recipient: Recipient identifier
    """
    logger.error(
        f"Delivery failed for {queue_id} after {attempt_number} attempts, "
        f"marking as permanently failed"
    )
    queue.mark_failed(
        queue_id, f"delivery_failed_after_{attempt_number}_attempts")

    # Mark agent as inactive after failed delivery
    if tracker and recipient and recipient.startswith("Agent-"):
        try:
            tracker.mark_inactive(recipient)
        except Exception:
            pass  # Non-critical tracking failure


def handle_retry_scheduled(
    queue_id: str,
    attempt_number: int,
    delay: float,
    queue: Any,
) -> None:
    """
    Schedule retry for failed delivery.

    Args:
        queue_id: Queue entry ID
        attempt_number: Attempt number
        delay: Retry delay in seconds
        queue: MessageQueue instance
    """
    logger.info(
        f"Delivery failed for {queue_id} (attempt {attempt_number}/{MAX_RETRIES}), "
        f"will retry in {delay}s"
    )
    # Reset to PENDING so it can be retried
    queue._reset_entry_for_retry(queue_id, attempt_number, delay)
