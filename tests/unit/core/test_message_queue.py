"""
Unit tests for src/core/message_queue.py

Tests message queue functionality including:
- Queue configuration
- Message enqueue/dequeue operations
- Status management (delivered/failed)
- Statistics and health monitoring
- Queue processor operations
"""

import pytest
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch

from src.core.message_queue import (
    QueueConfig,
    MessageQueue,
    AsyncQueueProcessor
)
from src.core.message_queue_persistence import QueueEntry


class TestQueueConfig:
    """Test queue configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = QueueConfig()
        assert config.queue_directory == "message_queue"
        assert config.max_queue_size == 1000
        assert config.processing_batch_size == 10
        assert config.max_age_days == 7
        assert config.retry_base_delay == 1.0
        assert config.retry_max_delay == 300.0
        assert config.cleanup_interval == 3600

    def test_custom_config(self):
        """Test custom configuration values."""
        config = QueueConfig(
            queue_directory="custom_queue",
            max_queue_size=500,
            processing_batch_size=5,
            max_age_days=3
        )
        assert config.queue_directory == "custom_queue"
        assert config.max_queue_size == 500
        assert config.processing_batch_size == 5
        assert config.max_age_days == 3


class TestMessageQueue:
    """Test MessageQueue operations."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary queue directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir) / "queue.json"

    @pytest.fixture
    def queue(self, temp_queue_dir):
        """Create MessageQueue instance."""
        config = QueueConfig(queue_directory=str(temp_queue_dir.parent))
        return MessageQueue(config=config)

    def test_enqueue_message(self, queue):
        """Test enqueueing a message."""
        message = {"type": "test", "content": "hello"}
        queue_id = queue.enqueue(message)
        
        assert queue_id is not None
        assert isinstance(queue_id, str)
        assert len(queue_id) > 0

    def test_enqueue_with_priority(self, queue):
        """Test enqueueing with priority."""
        class PriorityMessage:
            def __init__(self, priority):
                self.priority = priority
        
        high_priority = PriorityMessage(priority=1.0)
        low_priority = PriorityMessage(priority=0.1)
        
        high_id = queue.enqueue(high_priority)
        low_id = queue.enqueue(low_priority)
        
        # Dequeue should return high priority first
        entries = queue.dequeue(batch_size=2)
        assert len(entries) == 2
        assert entries[0].priority_score >= entries[1].priority_score

    def test_enqueue_max_size_limit(self, queue):
        """Test queue size limit enforcement."""
        config = QueueConfig(max_queue_size=2)
        limited_queue = MessageQueue(
            config=config,
            persistence=queue.persistence
        )
        
        queue.enqueue("message1")
        queue.enqueue("message2")
        
        # Third message should raise error
        with pytest.raises(RuntimeError, match="Queue size limit exceeded"):
            limited_queue.enqueue("message3")

    def test_dequeue_empty_queue(self, queue):
        """Test dequeueing from empty queue."""
        entries = queue.dequeue()
        assert entries == []

    def test_dequeue_messages(self, queue):
        """Test dequeueing messages."""
        msg1 = {"id": 1}
        msg2 = {"id": 2}
        
        id1 = queue.enqueue(msg1)
        id2 = queue.enqueue(msg2)
        
        entries = queue.dequeue(batch_size=2)
        assert len(entries) == 2
        assert entries[0].queue_id in [id1, id2]
        assert entries[1].queue_id in [id1, id2]

    def test_dequeue_batch_size(self, queue):
        """Test dequeueing with specific batch size."""
        for i in range(5):
            queue.enqueue(f"message{i}")
        
        entries = queue.dequeue(batch_size=3)
        assert len(entries) == 3

    def test_mark_delivered(self, queue):
        """Test marking message as delivered."""
        queue_id = queue.enqueue("test message")
        
        result = queue.mark_delivered(queue_id)
        assert result is True
        
        # Verify status in queue
        entries = queue.persistence.load_entries()
        delivered_entry = next(e for e in entries if e.queue_id == queue_id)
        assert delivered_entry.status == "DELIVERED"

    def test_mark_delivered_invalid_id(self, queue):
        """Test marking non-existent message as delivered."""
        result = queue.mark_delivered("invalid_id")
        assert result is False

    def test_mark_failed(self, queue):
        """Test marking message as failed."""
        queue_id = queue.enqueue("test message")
        error_msg = "Connection timeout"
        
        result = queue.mark_failed(queue_id, error_msg)
        assert result is True
        
        # Verify status and error
        entries = queue.persistence.load_entries()
        failed_entry = next(e for e in entries if e.queue_id == queue_id)
        assert failed_entry.status == "FAILED"
        assert failed_entry.metadata['last_error'] == error_msg
        assert failed_entry.delivery_attempts == 1

    def test_mark_failed_multiple_attempts(self, queue):
        """Test multiple failure attempts."""
        queue_id = queue.enqueue("test message")
        
        queue.mark_failed(queue_id, "Error 1")
        queue.mark_failed(queue_id, "Error 2")
        
        entries = queue.persistence.load_entries()
        failed_entry = next(e for e in entries if e.queue_id == queue_id)
        assert failed_entry.delivery_attempts == 2

    def test_get_statistics(self, queue):
        """Test getting queue statistics."""
        queue.enqueue("msg1")
        queue.enqueue("msg2")
        queue.enqueue("msg3")
        
        stats = queue.get_statistics()
        assert stats is not None
        assert isinstance(stats, dict)

    def test_cleanup_expired(self, queue):
        """Test cleaning up expired entries."""
        # Create old entry
        old_entry = QueueEntry(
            message="old message",
            queue_id="old_id",
            priority_score=0.5,
            status="PENDING",
            created_at=datetime.now() - timedelta(days=10),
            updated_at=datetime.now() - timedelta(days=10)
        )
        queue.persistence.save_entries([old_entry])
        
        # Create new entry
        queue.enqueue("new message")
        
        # Cleanup with short max_age
        config = QueueConfig(max_age_days=1)
        queue.config = config
        
        expired_count = queue.cleanup_expired()
        assert expired_count == 1
        
        # Verify old entry removed
        entries = queue.persistence.load_entries()
        assert len(entries) == 1
        assert entries[0].queue_id != "old_id"

    def test_get_health_status(self, queue):
        """Test getting queue health status."""
        queue.enqueue("test message")
        
        health = queue.get_health_status()
        assert health is not None
        assert isinstance(health, dict)

    def test_priority_calculation_with_enum(self, queue):
        """Test priority calculation with enum."""
        from enum import Enum
        
        class Priority(Enum):
            HIGH = 1.0
            LOW = 0.1
        
        class Message:
            def __init__(self):
                self.priority = Priority.HIGH
        
        message = Message()
        queue_id = queue.enqueue(message)
        
        entries = queue.dequeue()
        assert entries[0].priority_score == 1.0

    def test_priority_calculation_with_numeric(self, queue):
        """Test priority calculation with numeric value."""
        class Message:
            def __init__(self):
                self.priority = 0.8
        
        message = Message()
        queue_id = queue.enqueue(message)
        
        entries = queue.dequeue()
        assert entries[0].priority_score == 0.8

    def test_priority_calculation_default(self, queue):
        """Test default priority calculation."""
        message = {"no_priority": True}
        queue_id = queue.enqueue(message)
        
        entries = queue.dequeue()
        assert entries[0].priority_score == 0.5


class TestAsyncQueueProcessor:
    """Test AsyncQueueProcessor operations."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary queue directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir) / "queue.json"

    @pytest.fixture
    def queue(self, temp_queue_dir):
        """Create MessageQueue instance."""
        config = QueueConfig(queue_directory=str(temp_queue_dir.parent))
        return MessageQueue(config=config)

    @pytest.fixture
    def processor(self, queue):
        """Create AsyncQueueProcessor instance."""
        def delivery_callback(message):
            return True  # Always succeed
        
        return AsyncQueueProcessor(
            queue=queue,
            delivery_callback=delivery_callback
        )

    @pytest.mark.asyncio
    async def test_process_batch_success(self, processor, queue):
        """Test processing batch with successful delivery."""
        queue.enqueue("message1")
        queue.enqueue("message2")
        
        await processor.process_batch()
        
        # Verify messages marked as delivered
        entries = queue.persistence.load_entries()
        delivered = [e for e in entries if e.status == "DELIVERED"]
        assert len(delivered) == 2

    @pytest.mark.asyncio
    async def test_process_batch_failure(self, processor, queue):
        """Test processing batch with failed delivery."""
        def failing_callback(message):
            return False
        
        processor.delivery_callback = failing_callback
        
        queue_id = queue.enqueue("failing message")
        
        await processor.process_batch()
        
        # Verify message marked as failed
        entries = queue.persistence.load_entries()
        failed = [e for e in entries if e.status == "FAILED"]
        assert len(failed) == 1

    @pytest.mark.asyncio
    async def test_process_batch_exception(self, processor, queue):
        """Test processing batch with exception."""
        def exception_callback(message):
            raise ValueError("Test error")
        
        processor.delivery_callback = exception_callback
        
        queue_id = queue.enqueue("error message")
        
        await processor.process_batch()
        
        # Verify message marked as failed with error
        entries = queue.persistence.load_entries()
        failed = [e for e in entries if e.status == "FAILED"]
        assert len(failed) == 1
        assert "Test error" in failed[0].metadata.get('last_error', '')

    @pytest.mark.asyncio
    async def test_process_batch_empty_queue(self, processor):
        """Test processing empty queue."""
        await processor.process_batch()
        # Should not raise exception

    @pytest.mark.asyncio
    async def test_start_stop_processing(self, processor):
        """Test starting and stopping processor."""
        processor.start_processing()
        assert processor.running is True
        
        processor.stop_processing()
        assert processor.running is False

    @pytest.mark.asyncio
    async def test_cleanup_if_needed(self, processor, queue):
        """Test automatic cleanup during processing."""
        # Create old entry
        old_entry = QueueEntry(
            message="old",
            queue_id="old_id",
            priority_score=0.5,
            status="PENDING",
            created_at=datetime.now() - timedelta(days=10),
            updated_at=datetime.now() - timedelta(days=10)
        )
        queue.persistence.save_entries([old_entry])
        
        # Set short cleanup interval
        queue.config.cleanup_interval = 1
        processor.last_cleanup = 0
        
        await processor._cleanup_if_needed(interval=0.1)
        
        # Verify cleanup occurred
        entries = queue.persistence.load_entries()
        assert len(entries) == 0

    def test_message_missing_in_entry(self, processor, queue):
        """Test handling entry with missing message."""
        # Create entry without message attribute
        entry = QueueEntry(
            message=None,
            queue_id="no_msg_id",
            priority_score=0.5,
            status="PROCESSING",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        queue.persistence.save_entries([entry])
        
        # Should not raise exception
        asyncio.run(processor.process_batch())

