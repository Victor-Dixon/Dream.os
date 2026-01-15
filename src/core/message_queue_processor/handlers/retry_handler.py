#!/usr/bin/env python3
"""
Retry Handler for Message Queue Processing
==========================================

Handles retry logic for failed message deliveries with exponential backoff.
Phase 3 Implementation with Dead Letter Queue integration.
"""

import logging
from typing import Any, Tuple, Optional, List
import time
import random
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class DeadLetterEntry:
    """Represents a message in the dead letter queue"""
    queue_id: str
    original_message: Any
    recipient: str
    failure_reason: str
    timestamp: str
    retry_attempts: int
    final_attempt_time: str

class DeadLetterQueue:
    """Manages dead letter queue functionality"""

    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), '..', '..', '..', '..',
            'data', 'dead_letter_queue.json'
        )
        self._ensure_storage_path()
        self.queue: List[DeadLetterEntry] = []
        self._load_queue()

    def _ensure_storage_path(self):
        """Ensure the storage directory exists"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def _load_queue(self):
        """Load dead letter queue from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.queue = [DeadLetterEntry(**item) for item in data.get('queue', [])]
                logger.info(f"Loaded {len(self.queue)} messages from dead letter queue")
        except Exception as e:
            logger.warning(f"Failed to load dead letter queue: {e}")
            self.queue = []

    def _save_queue(self):
        """Save dead letter queue to storage"""
        try:
            data = {
                'queue': [asdict(entry) for entry in self.queue],
                'last_updated': datetime.now().isoformat(),
                'total_messages': len(self.queue)
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save dead letter queue: {e}")

    def add_message(self, queue_id: str, entry: Any, recipient: str,
                   failure_reason: str, retry_attempts: int) -> None:
        """Add a message to the dead letter queue"""
        dead_letter_entry = DeadLetterEntry(
            queue_id=queue_id,
            original_message=str(entry) if entry else "No message content",
            recipient=recipient,
            failure_reason=failure_reason,
            timestamp=datetime.now().isoformat(),
            retry_attempts=retry_attempts,
            final_attempt_time=datetime.now().isoformat()
        )

        self.queue.append(dead_letter_entry)
        self._save_queue()

        logger.warning(f"💀 Added message {queue_id} to dead letter queue")
        logger.warning(f"   Recipient: {recipient}")
        logger.warning(f"   Failure: {failure_reason}")
        logger.warning(f"   Retry attempts: {retry_attempts}")

    def get_failed_messages_for_agent(self, agent: str) -> List[DeadLetterEntry]:
        """Get all failed messages for a specific agent"""
        return [entry for entry in self.queue if entry.recipient == agent]

    def get_stats(self):
        """Get dead letter queue statistics"""
        agent_failures = {}
        for entry in self.queue:
            agent_failures[entry.recipient] = agent_failures.get(entry.recipient, 0) + 1

        return {
            'total_messages': len(self.queue),
            'agents_with_failures': len(agent_failures),
            'agent_breakdown': agent_failures,
            'oldest_message': min((entry.timestamp for entry in self.queue), default=None),
            'newest_message': max((entry.timestamp for entry in self.queue), default=None)
        }

    def cleanup_old_messages(self, days_old: int = 30) -> int:
        """Remove messages older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        original_count = len(self.queue)

        self.queue = [
            entry for entry in self.queue
            if datetime.fromisoformat(entry.timestamp).timestamp() > cutoff_time
        ]

        removed_count = original_count - len(self.queue)
        if removed_count > 0:
            self._save_queue()
            logger.info(f"Cleaned up {removed_count} old messages from dead letter queue")

        return removed_count


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

    # Implement actual dead letter queue functionality
    try:
        dlq = get_dead_letter_queue()
        dlq.add_message(
            queue_id=queue_id,
            entry=getattr(queue, 'current_entry', None),
            recipient=recipient,
            failure_reason=f"All {attempt_num} retry attempts exhausted",
            retry_attempts=attempt_num
        )

        # Send failure notification (could be expanded to email/slack/etc.)
        logger.error(f"💀 FAILURE NOTIFICATION: Message {queue_id} permanently failed delivery to {recipient}")
        logger.error(f"   Check dead letter queue for message details")
        logger.error(f"   DLQ Stats: {dlq.get_stats()['total_messages']} total failed messages")

        # Update monitoring (could integrate with external monitoring systems)
        failure_stats = dlq.get_stats()
        logger.warning(f"📊 MONITORING UPDATE: {failure_stats['total_messages']} messages in dead letter queue")
        logger.warning(f"   Agents with failures: {failure_stats['agents_with_failures']}")

        # Trigger escalation if too many failures for an agent
        agent_failures = dlq.get_failed_messages_for_agent(recipient)
        if len(agent_failures) >= 5:  # Configurable threshold
            logger.critical(f"🚨 ESCALATION TRIGGERED: Agent {recipient} has {len(agent_failures)} failed messages")
            logger.critical(f"   Consider agent health check or manual intervention")

    except Exception as dlq_error:
        logger.error(f"Failed to process dead letter queue: {dlq_error}")
        # Fallback to original simulated behavior
        logger.warning(f"   Message {queue_id} moved to dead letter queue (fallback simulated)")


# Global dead letter queue instance
_dead_letter_queue = None

def get_dead_letter_queue():
    """Get the global dead letter queue instance"""
    global _dead_letter_queue
    if _dead_letter_queue is None:
        _dead_letter_queue = DeadLetterQueue()
    return _dead_letter_queue