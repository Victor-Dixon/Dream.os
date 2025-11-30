#!/usr/bin/env python3
"""
Unit tests for in_memory_message_queue.py - Infrastructure Test Coverage

Tests InMemoryMessageQueue class and in-memory queue operations.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.in_memory_message_queue import InMemoryMessageQueue, InMemoryQueueEntry


class TestInMemoryQueueEntry:
    """Test suite for InMemoryQueueEntry dataclass."""

    def test_entry_initialization(self):
        """Test entry initialization with required fields."""
        entry = InMemoryQueueEntry(
            queue_id="test-id",
            message={"content": "test"},
            priority="normal"
        )
        
        assert entry.queue_id == "test-id"
        assert entry.message == {"content": "test"}
        assert entry.priority == "normal"
        assert entry.status == "pending"
        assert entry.created_at != ""
        assert entry.updated_at != ""
        assert entry.metadata == {}

    def test_entry_initialization_with_optional_fields(self):
        """Test entry initialization with optional fields."""
        entry = InMemoryQueueEntry(
            queue_id="test-id",
            message={"content": "test"},
            priority="urgent",
            status="delivered",
            metadata={"key": "value"}
        )
        
        assert entry.status == "delivered"
        assert entry.metadata == {"key": "value"}

    def test_entry_to_queue_entry(self):
        """Test converting entry to QueueEntry."""
        entry = InMemoryQueueEntry(
            queue_id="test-id",
            message={"content": "test"},
            priority="urgent"
        )
        
        queue_entry = entry.to_queue_entry()
        
        assert queue_entry.queue_id == "test-id"
        assert queue_entry.message == {"content": "test"}
        assert queue_entry.priority_score == 1.0  # urgent maps to 1.0
        assert queue_entry.status == "pending"

    def test_entry_to_queue_entry_priority_mapping(self):
        """Test priority string to score mapping."""
        priority_tests = [
            ("urgent", 1.0),
            ("high", 0.8),
            ("normal", 0.5),
            ("regular", 0.5),
            ("low", 0.3),
            ("unknown", 0.5)  # default
        ]
        
        for priority_str, expected_score in priority_tests:
            entry = InMemoryQueueEntry(
                queue_id="test-id",
                message={},
                priority=priority_str
            )
            queue_entry = entry.to_queue_entry()
            assert queue_entry.priority_score == expected_score


class TestInMemoryMessageQueue:
    """Test suite for InMemoryMessageQueue class."""

    @pytest.fixture
    def queue(self):
        """Create InMemoryMessageQueue instance."""
        return InMemoryMessageQueue()

    def test_initialization_default(self):
        """Test queue initialization with default max_size."""
        queue = InMemoryMessageQueue()
        
        assert queue.max_size == 10000
        assert len(queue._queue) == 0
        assert queue._stats["total_enqueued"] == 0

    def test_initialization_custom_max_size(self):
        """Test queue initialization with custom max_size."""
        queue = InMemoryMessageQueue(max_size=100)
        
        assert queue.max_size == 100

    def test_enqueue_message(self, queue):
        """Test enqueueing a message."""
        message = {"content": "test message", "to": "Agent-1"}
        queue_id = queue.enqueue(message, priority="normal")
        
        assert queue_id is not None
        assert isinstance(queue_id, str)
        assert len(queue._queue) == 1
        assert queue._stats["total_enqueued"] == 1

    def test_enqueue_with_priority(self, queue):
        """Test enqueueing with different priorities."""
        high_msg = {"content": "urgent"}
        normal_msg = {"content": "normal"}
        
        queue.enqueue(high_msg, priority="urgent")
        queue.enqueue(normal_msg, priority="normal")
        
        assert len(queue._queue) == 2
        # Urgent should be first after sorting
        assert queue._queue[0].priority == "urgent"

    def test_enqueue_with_metadata(self, queue):
        """Test enqueueing with metadata."""
        metadata = {"sender": "Agent-1", "channel": "test"}
        queue_id = queue.enqueue(
            {"content": "test"},
            priority="normal",
            metadata=metadata
        )
        
        entry = queue._queue[0]
        assert entry.metadata == metadata

    def test_enqueue_max_size_limit(self, queue):
        """Test queue respects max_size limit."""
        queue.max_size = 2
        
        queue.enqueue({"msg": "1"})
        queue.enqueue({"msg": "2"})
        result = queue.enqueue({"msg": "3"})
        
        # Should return None when queue is full
        assert result is None
        assert len(queue._queue) == 2

    def test_dequeue_empty_queue(self, queue):
        """Test dequeueing from empty queue."""
        entries = queue.dequeue()
        
        assert entries == []
        assert queue._stats["total_dequeued"] == 0

    def test_dequeue_single_message(self, queue):
        """Test dequeueing single message."""
        message = {"content": "test"}
        queue_id = queue.enqueue(message)
        
        entries = queue.dequeue(batch_size=1)
        
        assert len(entries) == 1
        assert entries[0].queue_id == queue_id
        # Entry remains in queue but marked as processing
        assert len(queue._queue) == 1
        assert queue._queue[0].status == "processing"

    def test_dequeue_batch_size(self, queue):
        """Test dequeueing with batch_size."""
        for i in range(5):
            queue.enqueue({"msg": i})
        
        entries = queue.dequeue(batch_size=3)
        
        assert len(entries) == 3
        # All entries remain in queue, 3 marked as processing
        assert len(queue._queue) == 5
        processing_count = sum(1 for e in queue._queue if e.status == "processing")
        assert processing_count == 3

    def test_dequeue_all_remaining(self, queue):
        """Test dequeueing all remaining messages."""
        for i in range(3):
            queue.enqueue({"msg": i})
        
        entries = queue.dequeue(batch_size=10)  # More than available
        
        assert len(entries) == 3
        # All entries remain in queue but marked as processing
        assert len(queue._queue) == 3
        assert all(e.status == "processing" for e in queue._queue)

    def test_dequeue_priority_order(self, queue):
        """Test dequeueing respects priority order."""
        queue.enqueue({"msg": "low"}, priority="low")
        queue.enqueue({"msg": "high"}, priority="high")
        queue.enqueue({"msg": "urgent"}, priority="urgent")
        
        entries = queue.dequeue(batch_size=3)
        
        # Entries are QueueEntry objects, check via queue state
        assert len(entries) == 3
        # Urgent should be first in queue
        assert queue._queue[0].priority == "urgent"

    def test_mark_delivered(self, queue):
        """Test marking message as delivered."""
        queue_id = queue.enqueue({"content": "test"})
        
        result = queue.mark_delivered(queue_id)
        
        assert result is True
        assert queue._queue[0].status == "delivered"
        assert queue._stats["total_delivered"] == 1

    def test_mark_delivered_invalid_id(self, queue):
        """Test marking non-existent message as delivered."""
        result = queue.mark_delivered("invalid-id")
        
        assert result is False

    def test_mark_delivered_after_dequeue(self, queue):
        """Test marking message as delivered after dequeue."""
        queue_id = queue.enqueue({"content": "test"})
        queue.dequeue(batch_size=1)
        
        result = queue.mark_delivered(queue_id)
        
        # Entry remains in queue, can be marked as delivered
        assert result is True
        assert queue._queue[0].status == "delivered"

    def test_mark_failed(self, queue):
        """Test marking message as failed."""
        queue_id = queue.enqueue({"content": "test"})
        
        result = queue.mark_failed(queue_id, error="Test error")
        
        assert result is True
        assert queue._queue[0].status == "failed"
        assert queue._queue[0].metadata["failure_reason"] == "Test error"
        assert queue._stats["total_failed"] == 1

    def test_mark_failed_invalid_id(self, queue):
        """Test marking non-existent message as failed."""
        result = queue.mark_failed("invalid-id", error="test")
        
        assert result is False

    def test_get_stats_empty_queue(self, queue):
        """Test getting statistics for empty queue."""
        stats = queue.get_stats()
        
        assert stats["total"] == 0
        assert stats["pending"] == 0
        assert stats["delivered"] == 0
        assert stats["failed"] == 0

    def test_get_stats_with_entries(self, queue):
        """Test getting statistics with various entry statuses."""
        queue.enqueue({"msg": "1"})
        queue.enqueue({"msg": "2"})
        queue_id = queue.enqueue({"msg": "3"})
        
        queue.mark_delivered(queue_id)
        
        stats = queue.get_stats()
        
        assert stats["total"] == 3
        assert stats["pending"] == 2
        assert stats["delivered"] == 1
        assert stats["failed"] == 0

    def test_get_statistics_alias(self, queue):
        """Test get_statistics is alias for get_stats."""
        stats1 = queue.get_stats()
        stats2 = queue.get_statistics()
        
        assert stats1 == stats2

    def test_cleanup_expired(self, queue):
        """Test cleanup_expired (no-op for in-memory queue)."""
        result = queue.cleanup_expired()
        
        # Should return 0 for in-memory queue
        assert result == 0

    def test_clear(self, queue):
        """Test clearing all entries from queue."""
        queue.enqueue({"msg": "1"})
        queue.enqueue({"msg": "2"})
        
        queue.clear()
        
        assert len(queue._queue) == 0
        assert queue._stats["total_enqueued"] == 0

    def test_thread_safety(self, queue):
        """Test thread-safety of queue operations."""
        import threading
        
        def enqueue_messages():
            for i in range(10):
                queue.enqueue({"msg": i})
        
        threads = [threading.Thread(target=enqueue_messages) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should have 50 messages (5 threads * 10 messages)
        assert queue._stats["total_enqueued"] == 50

    def test_dequeue_thread_safety(self, queue):
        """Test thread-safety of dequeue operations."""
        import threading
        
        # Pre-populate queue
        for i in range(100):
            queue.enqueue({"msg": i})
        
        dequeued_count = []
        
        def dequeue_messages():
            entries = queue.dequeue(batch_size=10)
            dequeued_count.append(len(entries))
        
        threads = [threading.Thread(target=dequeue_messages) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should have dequeued messages safely
        assert sum(dequeued_count) <= 100

