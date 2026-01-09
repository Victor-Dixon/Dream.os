#!/usr/bin/env python3
"""
Retry Handler for Message Queue Processing
=========================================

Handles message retry logic and scheduling with proper failure handling.
"""

import time
import random
import logging
import json
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Dict, List, Callable
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class FailedMessage:
    """Represents a failed message for dead letter queue"""
    message_id: str
    message_content: Any
    failure_reason: str
    total_attempts: int
    first_failure_time: datetime
    final_failure_time: datetime
    error_traceback: str
    metadata: Dict[str, Any]


class DeadLetterQueue:
    """Dead letter queue for permanently failed messages"""

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("data/dead_letter_queue")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._alert_handlers: List[Callable] = []

    def add_failed_message(self, failed_message: FailedMessage) -> None:
        """Add a failed message to the dead letter queue"""
        try:
            # Create filename with timestamp and message ID
            timestamp = failed_message.final_failure_time.strftime("%Y%m%d_%H%M%S")
            filename = f"failed_message_{failed_message.message_id}_{timestamp}.json"
            filepath = self.storage_path / filename

            # Save message to file
            with open(filepath, 'w', encoding='utf-8') as f:
                # Convert datetime objects to ISO format for JSON serialization
                message_dict = asdict(failed_message)
                message_dict['first_failure_time'] = failed_message.first_failure_time.isoformat()
                message_dict['final_failure_time'] = failed_message.final_failure_time.isoformat()
                json.dump(message_dict, f, indent=2, ensure_ascii=False)

            logger.warning(f"Message {failed_message.message_id} added to dead letter queue: {filepath}")

            # Trigger alerts
            self._trigger_alerts(failed_message)

        except Exception as e:
            logger.error(f"Failed to add message to dead letter queue: {e}")

    def add_alert_handler(self, handler: Callable) -> None:
        """Add an alert handler for failed messages"""
        self._alert_handlers.append(handler)

    def _trigger_alerts(self, failed_message: FailedMessage) -> None:
        """Trigger all alert handlers for a failed message"""
        for handler in self._alert_handlers:
            try:
                handler(failed_message)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")

    def get_failed_messages(self, limit: int = 100) -> List[FailedMessage]:
        """Get recent failed messages"""
        failed_messages = []

        try:
            # Get all failed message files, sorted by modification time (newest first)
            failed_files = sorted(
                self.storage_path.glob("failed_message_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )

            for filepath in failed_files[:limit]:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        message_dict = json.load(f)

                    # Convert ISO timestamps back to datetime
                    message_dict['first_failure_time'] = datetime.fromisoformat(message_dict['first_failure_time'])
                    message_dict['final_failure_time'] = datetime.fromisoformat(message_dict['final_failure_time'])

                    failed_message = FailedMessage(**message_dict)
                    failed_messages.append(failed_message)

                except Exception as e:
                    logger.error(f"Failed to load failed message from {filepath}: {e}")

        except Exception as e:
            logger.error(f"Failed to retrieve failed messages: {e}")

        return failed_messages


# Global dead letter queue instance
_dead_letter_queue = DeadLetterQueue()


def should_retry_delivery(error: Exception, attempt: int, max_attempts: int = 3) -> bool:
    """
    Determine if delivery should be retried.

    Args:
        error: The exception that occurred
        attempt: Current attempt number
        max_attempts: Maximum number of retry attempts

    Returns:
        True if should retry, False otherwise
    """
    if attempt >= max_attempts:
        return False

    # Don't retry certain types of errors
    error_str = str(error).lower()
    if "auth" in error_str or "permission" in error_str:
        return False

    return True


def handle_retry_failure(message: Any, final_error: Exception, total_attempts: int) -> None:
    """
    Handle final retry failure - message cannot be delivered.

    Args:
        message: The message that failed
        final_error: The final exception
        total_attempts: Total number of attempts made
    """
    # Generate message ID if not present
    message_id = getattr(message, 'id', getattr(message, 'message_id', f"msg_{int(time.time() * 1000)}"))

    # Create failed message record
    failed_message = FailedMessage(
        message_id=message_id,
        message_content=str(message),
        failure_reason=str(final_error),
        total_attempts=total_attempts,
        first_failure_time=datetime.now() - timedelta(minutes=total_attempts),  # Estimate
        final_failure_time=datetime.now(),
        error_traceback=traceback.format_exc(),
        metadata={
            'message_type': type(message).__name__,
            'error_type': type(final_error).__name__,
            'timestamp': datetime.now().isoformat()
        }
    )

    # Log the failure
    logger.error(f"Message delivery failed after {total_attempts} attempts: {final_error}")
    logger.error(f"Message ID: {message_id}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # Add to dead letter queue
    _dead_letter_queue.add_failed_message(failed_message)

    # Print summary for immediate visibility
    print(f"❌ CRITICAL: Message {message_id} failed permanently after {total_attempts} attempts")
    print(f"   Error: {final_error}")
    print(f"   Message added to dead letter queue for analysis")


def handle_retry_scheduled(message: Any, next_attempt: int, delay_seconds: int) -> None:
    """
    Handle retry scheduling with exponential backoff.

    Args:
        message: The message being retried
        next_attempt: The next attempt number
        delay_seconds: Delay before next attempt (will be overridden with exponential backoff)
    """
    # Implement exponential backoff with jitter
    base_delay = 5  # Base delay in seconds
    max_delay = 300  # Maximum delay (5 minutes)

    # Exponential backoff: base_delay * (2 ^ (attempt - 1))
    exponential_delay = min(base_delay * (2 ** (next_attempt - 1)), max_delay)

    # Add jitter (±25%) to prevent thundering herd
    import random
    jitter_range = exponential_delay * 0.25
    jitter = random.uniform(-jitter_range, jitter_range)
    actual_delay = exponential_delay + jitter

    # Ensure minimum delay
    actual_delay = max(actual_delay, 1)

    # Generate message ID if not present
    message_id = getattr(message, 'id', getattr(message, 'message_id', f"msg_{int(time.time() * 1000)}"))

    # Log the scheduling
    logger.info(f"Message {message_id} scheduled for retry {next_attempt} in {actual_delay:.1f} seconds")
    logger.info(f"Exponential backoff: base={base_delay}s, attempt={next_attempt}, exponential={exponential_delay:.1f}s, jitter={jitter:.1f}s")

    # Print summary for immediate visibility
    print(f"⏳ Message {message_id} scheduled for retry {next_attempt}")
    print(f"   Delay: {actual_delay:.1f} seconds (exponential backoff with jitter)")

    # In a real implementation, this would schedule the actual retry
    # For now, we just log and return the calculated delay
    return actual_delay


def get_failed_messages(limit: int = 100) -> List[FailedMessage]:
    """
    Get recent failed messages from dead letter queue.

    Args:
        limit: Maximum number of messages to return

    Returns:
        List of recent failed messages
    """
    return _dead_letter_queue.get_failed_messages(limit)


def add_failure_alert_handler(handler: Callable) -> None:
    """
    Add an alert handler for failed messages.

    Args:
        handler: Function to call when messages fail permanently
    """
    _dead_letter_queue.add_alert_handler(handler)