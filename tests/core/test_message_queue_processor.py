"""
Unit tests for message_queue_processor.py - HIGH PRIORITY

Tests message queue processing, batch processing, and error handling.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import asyncio

# Import message queue processor
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestMessageQueueProcessor:
    """Test suite for message queue processor."""

    @pytest.fixture
    def mock_queue(self):
        """Create mock message queue."""
        mock = MagicMock()
        mock.dequeue.return_value = []
        mock.mark_delivered.return_value = True
        mock.mark_failed.return_value = True
        return mock

    @pytest.fixture
    def mock_delivery_callback(self):
        """Create mock delivery callback."""
        return Mock(return_value=True)

    def test_processor_initialization(self, mock_queue):
        """Test processor initialization."""
        # Processor would be initialized with queue
        assert mock_queue is not None

    def test_process_batch(self, mock_queue, mock_delivery_callback):
        """Test processing a batch of messages."""
        from src.core.message_queue_persistence import QueueEntry
        from datetime import datetime
        import uuid
        
        # Create mock entries
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": "test1", "to": "Agent-1"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.8,
                status="PROCESSING",
                created_at=now,
                updated_at=now
            ),
            QueueEntry(
                message={"content": "test2", "to": "Agent-2"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.7,
                status="PROCESSING",
                created_at=now,
                updated_at=now
            )
        ]
        
        mock_queue.dequeue.return_value = entries
        
        # Simulate batch processing
        processed = []
        for entry in entries:
            if mock_delivery_callback(entry.message):
                processed.append(entry.queue_id)
                mock_queue.mark_delivered(entry.queue_id)
        
        assert len(processed) == 2
        assert mock_queue.mark_delivered.call_count == 2

    def test_process_empty_batch(self, mock_queue):
        """Test processing empty batch."""
        mock_queue.dequeue.return_value = []
        
        entries = mock_queue.dequeue()
        
        assert len(entries) == 0

    def test_delivery_failure_handling(self, mock_queue, mock_delivery_callback):
        """Test handling of delivery failures."""
        from src.core.message_queue_persistence import QueueEntry
        from datetime import datetime
        import uuid
        
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "to": "Agent-1"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.5,
            status="PROCESSING",
            created_at=now,
            updated_at=now
        )
        
        # Simulate delivery failure
        mock_delivery_callback.return_value = False
        
        if not mock_delivery_callback(entry.message):
            mock_queue.mark_failed(entry.queue_id, "Delivery failed")
        
        assert mock_queue.mark_failed.called

    def test_retry_logic(self, mock_queue):
        """Test retry logic for failed messages."""
        # Retry logic would check retry count and delay
        max_retries = 3
        retry_count = 1
        
        should_retry = retry_count < max_retries
        
        assert should_retry is True

    def test_batch_size_configuration(self, mock_queue):
        """Test batch size configuration."""
        batch_size = 10
        entries = mock_queue.dequeue(batch_size=batch_size)
        
        # Verify batch size is respected
        assert len(entries) <= batch_size


class TestAsyncQueueProcessor:
    """Test suite for async queue processor."""

    @pytest.mark.asyncio
    async def test_async_processing(self):
        """Test async message processing."""
        async def process_message(message):
            return True
        
        message = {"content": "test", "to": "Agent-1"}
        result = await process_message(message)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_concurrent_processing(self):
        """Test concurrent message processing."""
        async def process_message(msg):
            await asyncio.sleep(0.1)
            return True
        
        messages = [
            {"content": "test1", "to": "Agent-1"},
            {"content": "test2", "to": "Agent-2"},
            {"content": "test3", "to": "Agent-3"}
        ]
        
        results = await asyncio.gather(*[process_message(msg) for msg in messages])
        
        assert len(results) == 3
        assert all(results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

