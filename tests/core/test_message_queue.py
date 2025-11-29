"""
Unit tests for message_queue.py - HIGH PRIORITY

Tests MessageQueue class, QueueConfig, enqueue, dequeue, and priority handling.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import uuid

# Import message queue components
import sys
from pathlib import Path as PathLib

# Add src to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue import MessageQueue, QueueConfig


class TestQueueConfig:
    """Test suite for QueueConfig class."""

    def test_default_configuration(self):
        """Test default configuration values."""
        config = QueueConfig()
        
        assert config.queue_directory == "message_queue"
        assert config.max_queue_size == 1000
        assert config.processing_batch_size == 10
        assert config.max_age_days == 7
        assert config.retry_base_delay == 1.0
        assert config.retry_max_delay == 300.0
        assert config.cleanup_interval == 3600

    def test_custom_configuration(self):
        """Test custom configuration values."""
        config = QueueConfig(
            queue_directory="custom_queue",
            max_queue_size=500,
            processing_batch_size=5,
            max_age_days=14
        )
        
        assert config.queue_directory == "custom_queue"
        assert config.max_queue_size == 500
        assert config.processing_batch_size == 5
        assert config.max_age_days == 14


class TestMessageQueue:
    """Test suite for MessageQueue class."""

    @pytest.fixture
    def mock_persistence(self):
        """Create mock persistence layer."""
        mock = MagicMock()
        mock.load_entries.return_value = []
        mock.save_entries.return_value = None
        mock.atomic_operation = lambda func: func()
        return mock

    @pytest.fixture
    def queue(self, mock_persistence):
        """Create MessageQueue instance with mocked dependencies."""
        config = QueueConfig(queue_directory=str(Path(tempfile.gettempdir()) / "test_queue"))
        return MessageQueue(
            config=config,
            persistence=mock_persistence,
            logger=None
        )

    def test_queue_initialization(self, mock_persistence):
        """Test queue initialization."""
        config = QueueConfig()
        queue = MessageQueue(
            config=config,
            persistence=mock_persistence,
            logger=None
        )
        
        assert queue.config == config
        assert queue.persistence == mock_persistence
        assert queue.statistics_calculator is not None
        assert queue.health_monitor is not None

    def test_enqueue_message(self, queue, mock_persistence):
        """Test enqueueing a message."""
        message = {"content": "test message", "to": "Agent-1"}
        
        queue_id = queue.enqueue(message)
        
        assert queue_id is not None
        assert isinstance(queue_id, str)
        assert len(queue_id) > 0
        # Verify persistence was called
        assert mock_persistence.save_entries.called

    def test_enqueue_with_priority(self, queue):
        """Test enqueueing message with priority."""
        high_priority_message = {
            "content": "urgent message",
            "priority": "urgent",
            "to": "Agent-1"
        }
        
        queue_id = queue.enqueue(high_priority_message)
        
        assert queue_id is not None
        # Priority should be calculated and stored

    def test_dequeue_messages(self, queue, mock_persistence):
        """Test dequeuing messages."""
        # Mock entries
        from src.core.message_queue_persistence import QueueEntry
        from datetime import datetime
        
        now = datetime.now()
        mock_entry = QueueEntry(
            message={"content": "test"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        mock_persistence.load_entries.return_value = [mock_entry]
        
        entries = queue.dequeue(batch_size=1)
        
        assert len(entries) == 1
        assert entries[0].status == "PROCESSING"

    def test_dequeue_empty_queue(self, queue, mock_persistence):
        """Test dequeuing from empty queue."""
        mock_persistence.load_entries.return_value = []
        
        entries = queue.dequeue()
        
        assert len(entries) == 0

    def test_mark_delivered(self, queue, mock_persistence):
        """Test marking message as delivered."""
        from src.core.message_queue_persistence import QueueEntry
        from datetime import datetime
        
        queue_id = str(uuid.uuid4())
        now = datetime.now()
        mock_entry = QueueEntry(
            message={"content": "test"},
            queue_id=queue_id,
            priority_score=0.5,
            status="PROCESSING",
            created_at=now,
            updated_at=now
        )
        mock_persistence.load_entries.return_value = [mock_entry]
        
        result = queue.mark_delivered(queue_id)
        
        assert result is True
        assert mock_entry.status == "DELIVERED"

    def test_mark_failed(self, queue, mock_persistence):
        """Test marking message as failed."""
        from src.core.message_queue_persistence import QueueEntry
        from datetime import datetime
        
        queue_id = str(uuid.uuid4())
        now = datetime.now()
        mock_entry = QueueEntry(
            message={"content": "test"},
            queue_id=queue_id,
            priority_score=0.5,
            status="PROCESSING",
            created_at=now,
            updated_at=now
        )
        mock_persistence.load_entries.return_value = [mock_entry]
        
        result = queue.mark_failed(queue_id, "Test error")
        
        assert result is True
        assert mock_entry.status == "FAILED"

    def test_get_statistics(self, queue):
        """Test getting queue statistics."""
        stats = queue.get_statistics()
        
        assert stats is not None
        assert isinstance(stats, dict)

    def test_get_health_status(self, queue):
        """Test getting queue health status."""
        health = queue.get_health_status()
        
        assert health is not None
        assert isinstance(health, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

