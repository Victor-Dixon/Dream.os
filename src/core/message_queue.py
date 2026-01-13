#!/usr/bin/env python3
"""
Message Queue System - Agent Cellphone V2
=========================================

<!-- SSOT Domain: integration -->

Persistent message queuing system following SOLID principles.

SOLID Principles:
- SRP: Each class has single responsibility
- OCP: Open for extension, closed for modification
- LSP: Proper inheritance hierarchies
- ISP: Small, specific interfaces
- DIP: Dependency injection for abstractions

Architecture:
- Repository Pattern: MessageQueue handles persistent storage
- Service Layer: QueueProcessor orchestrates delivery attempts
- Dependency Injection: Modular components injected via constructor

@maintainer Agent-1 (System Recovery Specialist)
@license MIT
"""

from typing import Any, Dict, List, Optional, Callable
import asyncio
import uuid
from datetime import datetime
from pathlib import Path

from .message_queue_interfaces import (
    IMessageQueue,
    IQueuePersistence,
    IQueueProcessor,
    IMessageQueueLogger,
    IQueueEntry
)
from .message_queue_persistence import FileQueuePersistence, QueueEntry
from .message_queue_statistics import QueueStatisticsCalculator, QueueHealthMonitor


class QueueConfig:
    """Configuration for message queue."""

    def __init__(
        self,
        queue_directory: str = "message_queue",
        max_queue_size: int = 1000,
        processing_batch_size: int = 10,
        max_age_days: int = 7,
        retry_base_delay: float = 1.0,
        retry_max_delay: float = 300.0,
        cleanup_interval: int = 3600
    ):
        """Initialize queue configuration."""
        self.queue_directory = queue_directory
        self.max_queue_size = max_queue_size
        self.processing_batch_size = processing_batch_size
        self.max_age_days = max_age_days
        self.retry_base_delay = retry_base_delay
        self.retry_max_delay = retry_max_delay
        self.cleanup_interval = cleanup_interval


class MessageQueue(IMessageQueue):
    """SOLID-compliant message queue with dependency injection.

    Provides reliable message queuing with automatic retry and cleanup.
    Follows Single Responsibility Principle with separate persistence layer.
    """

    def __init__(
        self,
        config: Optional[QueueConfig] = None,
        persistence: Optional[IQueuePersistence] = None,
        statistics_calculator: Optional[QueueStatisticsCalculator] = None,
        health_monitor: Optional[QueueHealthMonitor] = None,
        logger: Optional[IMessageQueueLogger] = None
    ):
        """Initialize message queue with dependency injection."""
        self.config = config or QueueConfig()
        self.persistence = persistence or FileQueuePersistence(
            Path(self.config.queue_directory) / "queue.json"
        )
        self.statistics_calculator = statistics_calculator or QueueStatisticsCalculator()
        self.health_monitor = health_monitor or QueueHealthMonitor(
            self.statistics_calculator)
        self.logger = logger

        # Initialize queue file
        queue_file = Path(self.config.queue_directory) / "queue.json"
        queue_file.parent.mkdir(parents=True, exist_ok=True)

    def _log_info(self, message: str) -> None:
        """Log info message if logger available."""
        if self.logger:
            self.logger.info(message)

    def _log_warning(self, message: str) -> None:
        """Log warning message if logger available."""
        if self.logger:
            self.logger.warning(message)

    def _find_entry_by_id(self, entries: List[IQueueEntry], queue_id: str) -> Optional[IQueueEntry]:
        """Find queue entry by ID."""
        for entry in entries:
            if getattr(entry, 'queue_id', '') == queue_id:
                return entry
        return None

    def _update_entry_status(
        self, entry: IQueueEntry, status: str, error: Optional[str] = None
    ) -> None:
        """Update entry status and metadata."""
        entry.status = status
        entry.updated_at = datetime.now()

        if error:
            if not hasattr(entry, 'metadata'):
                entry.metadata = {}
            entry.metadata['last_error'] = error

        if status == "FAILED":
            if not hasattr(entry, 'delivery_attempts'):
                entry.delivery_attempts = 0
            entry.delivery_attempts += 1

    def enqueue(
        self,
        message: Any,
        delivery_callback: Optional[Callable[[Any], bool]] = None,
    ) -> str:
        """Add message to queue with priority-based ordering.

        Args:
            message: Message to queue
            delivery_callback: Optional callback for delivery attempts

        Returns:
            Queue ID for tracking
        """
        queue_id = str(uuid.uuid4())
        priority_score = self._calculate_priority_score(
            message, datetime.now())
        entry = self._create_queue_entry(
            queue_id, message, priority_score, delivery_callback)

        def _enqueue_operation():
            entries = self.persistence.load_entries()
            self._validate_queue_size(entries)
            entries.append(entry)
            self.persistence.save_entries(entries)
            self._log_info(
                f"Message queued: {queue_id} (priority: {priority_score})")
            return queue_id

        return self.persistence.atomic_operation(_enqueue_operation)

    def batch_enqueue(
        self,
        messages: List[Any],
        delivery_callback: Optional[Callable[[Any], bool]] = None,
    ) -> List[str]:
        """Enqueue multiple messages in a single atomic operation to prevent race conditions.
        
        Args:
            messages: List of messages to queue
            delivery_callback: Optional callback for delivery attempts
            
        Returns:
            List of queue IDs for tracking
        """
        queue_ids = []
        entries = []
        
        for message in messages:
            queue_id = str(uuid.uuid4())
            priority_score = self._calculate_priority_score(message, datetime.now())
            entry = self._create_queue_entry(queue_id, message, priority_score, delivery_callback)
            queue_ids.append(queue_id)
            entries.append(entry)
        
        def _batch_enqueue_operation():
            existing_entries = self.persistence.load_entries()
            self._validate_queue_size(existing_entries)
            existing_entries.extend(entries)
            self.persistence.save_entries(existing_entries)
            self._log_info(f"Batch enqueued {len(entries)} messages")
            return queue_ids
        
        return self.persistence.atomic_operation(_batch_enqueue_operation)

    def _create_queue_entry(
        self, queue_id: str, message: Any, priority_score: float,
        delivery_callback: Optional[Callable[[Any], bool]]
    ) -> QueueEntry:
        """Create new queue entry.
        
        FIXED: Normalize message format to dict to ensure consistent routing.
        Handles both UnifiedMessage objects and dict messages.
        """
        now = datetime.now()
        
        # FIXED: Normalize message to dict format for consistent routing
        # Prevents routing issues when messages come from different sources
        normalized_message = self._normalize_message(message)
        
        return QueueEntry(
            message=normalized_message,
            queue_id=queue_id,
            priority_score=priority_score,
            status="PENDING",
            created_at=now,
            updated_at=now,
            metadata={"delivery_callback": delivery_callback is not None},
        )
    
    def _normalize_message(self, message: Any) -> dict:
        """Normalize message to dict format for consistent routing.
        
        Handles both UnifiedMessage objects and dict messages.
        Ensures recipient is always extractable regardless of source.
        """
        if isinstance(message, dict):
            # Already a dict - ensure required fields exist
            return message
        
        # UnifiedMessage object - convert to dict
        from .messaging_models_core import UnifiedMessage
        if isinstance(message, UnifiedMessage):
            message_dict = {
                "recipient": message.recipient,
                "content": message.content,
                "sender": message.sender,
                "message_type": getattr(message.message_type, "value", None) or str(message.message_type),
                "priority": getattr(message.priority, "value", None) or str(message.priority),
                "tags": [getattr(tag, "value", None) or str(tag) for tag in message.tags],
                "metadata": message.metadata or {},
            }
            return message_dict
        
        # Fallback: try to extract as object attributes
        return {
            "recipient": getattr(message, "recipient", None) or getattr(message, "to", None),
            "content": getattr(message, "content", None) or getattr(message, "message", None),
            "sender": getattr(message, "sender", None) or getattr(message, "from", "SYSTEM"),
            "message_type": getattr(message, "message_type", "text"),
            "priority": getattr(message, "priority", "normal"),
            "tags": getattr(message, "tags", []),
            "metadata": getattr(message, "metadata", {}),
        }

    def _validate_queue_size(self, entries: List[IQueueEntry]) -> None:
        """Validate queue size limit."""
        if len(entries) >= self.config.max_queue_size:
            raise RuntimeError(
                f"Queue size limit exceeded: {self.config.max_queue_size}")

    def _calculate_priority_score(self, message: Any, now: datetime) -> float:
        """Calculate priority score for message.
        
        FIXED: Handles both UnifiedMessage objects and normalized dict messages.
        """
        # Check if message is dict (normalized format)
        if isinstance(message, dict):
            priority = message.get("priority", "regular")
            if isinstance(priority, str):
                # Map priority strings to scores
                priority_map = {"urgent": 1.0, "high": 0.8, "normal": 0.5, "regular": 0.5, "low": 0.3}
                return priority_map.get(priority.lower(), 0.5)
            elif isinstance(priority, (int, float)):
                return float(priority)
        
        # UnifiedMessage object format
        if hasattr(message, 'priority'):
            if hasattr(message.priority, 'value'):
                priority_value = message.priority.value
                if isinstance(priority_value, str):
                    priority_map = {"urgent": 1.0, "high": 0.8, "normal": 0.5, "regular": 0.5, "low": 0.3}
                    return priority_map.get(priority_value.lower(), 0.5)
                return float(priority_value)
            elif isinstance(message.priority, (int, float)):
                return float(message.priority)

        # Default priority
        return 0.5

    def dequeue(self, batch_size: Optional[int] = None) -> List[IQueueEntry]:
        """Get next messages for processing based on priority.

        Args:
            batch_size: Number of messages to retrieve (defaults to config)

        Returns:
            List of queue entries ready for processing
        """
        batch_size = batch_size or self.config.processing_batch_size

        def _dequeue_operation():
            entries = self.persistence.load_entries()
            pending_entries = self._get_pending_entries(entries)

            if not pending_entries:
                return []

            entries_to_process = self._select_top_priority_entries(
                pending_entries, batch_size)
            self._mark_entries_processing(entries_to_process)
            self.persistence.save_entries(entries)
            self._log_info(
                f"Dequeued {len(entries_to_process)} messages for processing")
            return entries_to_process

        return self.persistence.atomic_operation(_dequeue_operation)

    def _get_pending_entries(self, entries: List[IQueueEntry]) -> List[tuple]:
        """Get pending entries with priority scores for heap.
        
        Respects retry delays - entries with next_retry_delay won't be
        processed until delay has passed.
        """
        import heapq
        now = datetime.now()
        
        pending = []
        
        for i, e in enumerate(entries):
            if getattr(e, 'status', '') != 'PENDING':
                continue
            
            # Check if retry delay has passed
            metadata = getattr(e, 'metadata', {})
            next_retry_delay = metadata.get('next_retry_delay')
            last_retry_time = metadata.get('last_retry_time')
            
            if next_retry_delay and last_retry_time:
                try:
                    # Parse last_retry_time (handle both ISO format and datetime)
                    if isinstance(last_retry_time, str):
                        last_retry = datetime.fromisoformat(last_retry_time.replace('Z', '+00:00'))
                    else:
                        last_retry = last_retry_time
                    
                    # Handle timezone-aware vs naive
                    if hasattr(last_retry, 'tzinfo') and last_retry.tzinfo is not None:
                        # Timezone-aware - convert to naive for comparison
                        last_retry = last_retry.replace(tzinfo=None)
                    
                    elapsed = (now - last_retry).total_seconds()
                    if elapsed < next_retry_delay:
                        # Delay hasn't passed yet, skip this entry
                        continue
                except Exception:
                    # If parsing fails, allow entry (don't block on retry logic errors)
                    pass
            
            pending.append((-getattr(e, 'priority_score', 0), i, e))
        
        return pending

    def _select_top_priority_entries(
        self, pending_entries: List[tuple], batch_size: int
    ) -> List[IQueueEntry]:
        """Select top priority entries using heap."""
        import heapq
        heapq.heapify(pending_entries)
        entries_to_process = []

        for _ in range(min(batch_size, len(pending_entries))):
            _, _, entry = heapq.heappop(pending_entries)
            entries_to_process.append(entry)

        return entries_to_process

    def _mark_entries_processing(self, entries: List[IQueueEntry]) -> None:
        """Mark entries as processing."""
        for entry in entries:
            entry.status = "PROCESSING"
            entry.updated_at = datetime.now()

    def mark_delivered(self, queue_id: str) -> bool:
        """Mark message as successfully delivered."""

        def _mark_delivered_operation():
            entries = self.persistence.load_entries()
            entry = self._find_entry_by_id(entries, queue_id)

            if entry:
                self._update_entry_status(entry, "DELIVERED")
                self.persistence.save_entries(entries)
                self._log_info(f"Message marked as delivered: {queue_id}")
                return True

            self._log_warning(f"Queue entry not found: {queue_id}")
            return False

        return self.persistence.atomic_operation(_mark_delivered_operation)

    def mark_failed(self, queue_id: str, error: str) -> bool:
        """Mark message as failed and schedule retry."""

        def _mark_failed_operation():
            entries = self.persistence.load_entries()
            entry = self._find_entry_by_id(entries, queue_id)

            if entry:
                self._update_entry_status(entry, "FAILED", error)
                self.persistence.save_entries(entries)
                self._log_warning(
                    f"Message marked as failed: {queue_id} - {error}")
                return True

            self._log_warning(f"Queue entry not found: {queue_id}")
            return False

        return self.persistence.atomic_operation(_mark_failed_operation)
    
    def _reset_entry_for_retry(self, queue_id: str, attempts: int, delay: float) -> bool:
        """Reset entry to PENDING status for retry with backoff delay.
        
        Args:
            queue_id: Queue entry ID
            attempts: Current attempt count
            delay: Delay in seconds before next retry
            
        Returns:
            True if reset successful, False otherwise
        """
        from datetime import datetime, timedelta
        
        def _reset_operation():
            entries = self.persistence.load_entries()
            entry = self._find_entry_by_id(entries, queue_id)
            
            if entry:
                entry.status = "PENDING"
                entry.updated_at = datetime.now()
                
                # Store retry metadata
                if not hasattr(entry, 'metadata'):
                    entry.metadata = {}
                entry.metadata['delivery_attempts'] = attempts
                entry.metadata['last_retry_time'] = datetime.now().isoformat()
                entry.metadata['next_retry_delay'] = delay
                
                # Update priority score to schedule retry after delay
                # Higher priority for urgent retries, but still respect delay
                entry.priority_score = getattr(entry, 'priority_score', 0.5)
                
                self.persistence.save_entries(entries)
                self._log_info(
                    f"Entry {queue_id} reset to PENDING for retry "
                    f"(attempt {attempts}, delay {delay}s)")
                return True
            
            self._log_warning(f"Queue entry not found for retry: {queue_id}")
            return False
        
        return self.persistence.atomic_operation(_reset_operation)
    
    def resend_failed_messages(self, max_messages: Optional[int] = None) -> int:
        """Resend failed messages that haven't exceeded max retries.
        
        Args:
            max_messages: Maximum number of messages to resend (None = all)
            
        Returns:
            Number of messages reset for retry
        """
        from datetime import datetime, timedelta
        
        def _resend_operation():
            entries = self.persistence.load_entries()
            failed_entries = [
                e for e in entries 
                if getattr(e, 'status', '') == 'FAILED'
            ]
            
            if not failed_entries:
                return 0
            
            # Filter entries that can be retried (haven't exceeded max retries)
            max_retries = 3
            resettable = []
            
            for entry in failed_entries:
                attempts = getattr(entry, 'delivery_attempts', 0)
                if attempts < max_retries:
                    resettable.append(entry)
            
            if max_messages:
                resettable = resettable[:max_messages]
            
            # Reset entries to PENDING
            for entry in resettable:
                entry.status = "PENDING"
                entry.updated_at = datetime.now()
                attempts = getattr(entry, 'delivery_attempts', 0)
                
                if not hasattr(entry, 'metadata'):
                    entry.metadata = {}
                entry.metadata['delivery_attempts'] = attempts
                entry.metadata['resend_time'] = datetime.now().isoformat()
            
            if resettable:
                self.persistence.save_entries(entries)
                self._log_info(f"Reset {len(resettable)} failed messages for retry")
            
            return len(resettable)
        
        return self.persistence.atomic_operation(_resend_operation)

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive queue statistics."""

        def _get_statistics_operation():
            entries = self.persistence.load_entries()
            return self.statistics_calculator.calculate_statistics(entries)

        return self.persistence.atomic_operation(_get_statistics_operation)

    def cleanup_expired(self) -> int:
        """Remove expired entries from queue."""

        def _cleanup_operation():
            entries = self.persistence.load_entries()
            original_count = len(entries)
            active_entries = self._filter_expired_entries(entries)
            expired_count = original_count - len(active_entries)

            self.persistence.save_entries(active_entries)
            if expired_count > 0:
                self._log_info(f"Cleaned up {expired_count} expired entries")

            return expired_count

        return self.persistence.atomic_operation(_cleanup_operation)

    def _filter_expired_entries(self, entries: List[IQueueEntry]) -> List[IQueueEntry]:
        """Filter out expired entries."""
        max_age_seconds = self.config.max_age_days * 24 * 60 * 60
        now = datetime.now()
        active_entries = []

        for entry in entries:
            if not hasattr(entry, 'created_at'):
                active_entries.append(entry)
                continue

            age = (now - entry.created_at).total_seconds()
            if age <= max_age_seconds:
                active_entries.append(entry)

        return active_entries

    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive queue health status."""

        def _get_health_operation():
            entries = self.persistence.load_entries()
            return self.health_monitor.assess_health(entries)

        return self.persistence.atomic_operation(_get_health_operation)


class AsyncQueueProcessor(IQueueProcessor):
    """SOLID-compliant asynchronous queue processor.

    Processes queued messages with retry logic and error handling.
    Follows Single Responsibility Principle with focused processing logic.
    """

    def __init__(
        self,
        queue: IMessageQueue,
        delivery_callback: Callable[[Any], bool],
        logger: Optional[IMessageQueueLogger] = None
    ):
        """Initialize queue processor with dependency injection."""
        self.queue = queue
        self.delivery_callback = delivery_callback
        self.logger = logger
        self.running = False
        self.last_cleanup = 0.0

    async def start_processing(self, interval: float = 5.0) -> None:
        """Start continuous queue processing."""
        self.running = True
        if self.logger:
            self.logger.info("Queue processor started")

        while self.running:
            try:
                await self.process_batch()
                await self._cleanup_if_needed(interval)
                await asyncio.sleep(interval)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Queue processing error: {e}")
                await asyncio.sleep(interval)

    def stop_processing(self) -> None:
        """Stop queue processing."""
        self.running = False
        if self.logger:
            self.logger.info("Queue processor stopped")

    async def process_batch(self) -> None:
        """Process a batch of queued messages."""
        entries = self.queue.dequeue()

        for entry in entries:
            self._process_entry(entry)

    def _process_entry(self, entry: IQueueEntry) -> None:
        """Process single queue entry."""
        message = getattr(entry, 'message', None)
        queue_id = getattr(entry, 'queue_id', '')

        if message is None:
            if self.logger:
                self.logger.warning(f"Entry missing message: {queue_id}")
            return

        try:
            success = self.delivery_callback(message)
            if success:
                self.queue.mark_delivered(queue_id)
            else:
                self.queue.mark_failed(
                    queue_id, "Delivery callback returned False")
        except Exception as e:
            self.queue.mark_failed(queue_id, str(e))

    async def _cleanup_if_needed(self, interval: float) -> None:
        """Perform cleanup if interval has passed."""
        import time
        now = time.time()
        cleanup_interval = getattr(self.queue.config, 'cleanup_interval', 3600)

        if now - self.last_cleanup >= cleanup_interval:
            expired_count = self.queue.cleanup_expired()
            if expired_count > 0 and self.logger:
                self.logger.info(
                    f"Cleanup completed: {expired_count} expired entries removed")
            self.last_cleanup = now


# Backward compatibility alias
QueueProcessor = AsyncQueueProcessor
