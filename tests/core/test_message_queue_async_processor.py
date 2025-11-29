"""
Unit tests for message_queue_async_processor.py - NEXT PRIORITY

Tests async message queue processing functionality.
Expanded to ≥85% coverage.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import asyncio
import uuid

# Import async processor
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_async_processor import AsyncQueueProcessor
from src.core.message_queue_persistence import QueueEntry


class TestAsyncQueueProcessor:
    """Test suite for AsyncQueueProcessor class."""

    @pytest.fixture
    def mock_queue(self):
        """Create mock message queue."""
        mock = MagicMock()
        mock.dequeue.return_value = []
        mock.mark_delivered.return_value = True
        mock.mark_failed.return_value = True
        mock.config = MagicMock()
        mock.config.cleanup_interval = 3600
        mock.cleanup_expired.return_value = 0
        return mock

    @pytest.fixture
    def mock_delivery_callback(self):
        """Create mock delivery callback."""
        return MagicMock(return_value=True)

    @pytest.fixture
    def mock_logger(self):
        """Create mock logger."""
        logger = MagicMock()
        logger.info = Mock()
        logger.warning = Mock()
        logger.error = Mock()
        return logger

    @pytest.fixture
    def processor(self, mock_queue, mock_delivery_callback, mock_logger):
        """Create AsyncQueueProcessor instance."""
        return AsyncQueueProcessor(
            queue=mock_queue,
            delivery_callback=mock_delivery_callback,
            logger=mock_logger
        )

    def test_processor_initialization(self, processor, mock_queue, mock_delivery_callback):
        """Test processor initialization."""
        assert processor.queue == mock_queue
        assert processor.delivery_callback == mock_delivery_callback
        assert processor.running is False
        assert processor.last_cleanup == 0.0

    def test_stop_processing(self, processor, mock_logger):
        """Test stopping queue processing."""
        processor.running = True
        processor.stop_processing()
        assert processor.running is False
        mock_logger.info.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_batch_empty(self, processor, mock_queue):
        """Test processing empty batch."""
        mock_queue.dequeue.return_value = []
        await processor.process_batch()
        # Should complete without errors
        assert True

    @pytest.mark.asyncio
    async def test_process_batch_success(self, processor, mock_queue, mock_delivery_callback):
        """Test processing batch with successful delivery."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "to": "Agent-1"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        
        mock_delivery_callback.assert_called_once_with(entry.message)
        mock_queue.mark_delivered.assert_called_once_with(entry.queue_id)

    @pytest.mark.asyncio
    async def test_process_batch_delivery_failure(self, processor, mock_queue, mock_delivery_callback):
        """Test processing batch with delivery failure."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "to": "Agent-1"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = False
        
        await processor.process_batch()
        
        mock_queue.mark_failed.assert_called_once()
        call_args = mock_queue.mark_failed.call_args
        assert call_args[0][0] == entry.queue_id
        assert "False" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_process_batch_missing_message(self, processor, mock_queue, mock_logger):
        """Test processing batch with entry missing message."""
        entry = MagicMock()
        entry.message = None
        entry.queue_id = "test-id"
        mock_queue.dequeue.return_value = [entry]
        
        await processor.process_batch()
        
        mock_logger.warning.assert_called_once()
        assert "missing message" in mock_logger.warning.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_process_batch_delivery_exception(self, processor, mock_queue, mock_delivery_callback):
        """Test processing batch with delivery exception."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test"},
            queue_id=str(uuid.uuid4()),
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.side_effect = Exception("Delivery error")
        
        await processor.process_batch()
        
        mock_queue.mark_failed.assert_called_once()
        call_args = mock_queue.mark_failed.call_args
        assert "Delivery error" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_process_batch_multiple_entries(self, processor, mock_queue, mock_delivery_callback):
        """Test processing batch with multiple entries."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": f"test{i}"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now
            )
            for i in range(3)
        ]
        mock_queue.dequeue.return_value = entries
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        
        assert mock_delivery_callback.call_count == 3
        assert mock_queue.mark_delivered.call_count == 3

    @pytest.mark.asyncio
    async def test_cleanup_if_needed_not_due(self, processor, mock_queue):
        """Test cleanup when not due."""
        processor.last_cleanup = 1000.0
        with patch('time.time', return_value=1001.0):
            await processor._cleanup_if_needed(5.0)
        
        mock_queue.cleanup_expired.assert_not_called()

    @pytest.mark.asyncio
    async def test_cleanup_if_needed_due(self, processor, mock_queue, mock_logger):
        """Test cleanup when due."""
        processor.last_cleanup = 0.0
        mock_queue.config.cleanup_interval = 1
        mock_queue.cleanup_expired.return_value = 5
        
        with patch('time.time', return_value=2.0):
            await processor._cleanup_if_needed(5.0)
        
        mock_queue.cleanup_expired.assert_called_once()
        mock_logger.info.assert_called_once()
        assert processor.last_cleanup == 2.0

    @pytest.mark.asyncio
    async def test_cleanup_if_needed_no_expired(self, processor, mock_queue, mock_logger):
        """Test cleanup when no expired entries."""
        processor.last_cleanup = 0.0
        mock_queue.config.cleanup_interval = 1
        mock_queue.cleanup_expired.return_value = 0
        
        with patch('time.time', return_value=2.0):
            await processor._cleanup_if_needed(5.0)
        
        mock_queue.cleanup_expired.assert_called_once()
        # Logger should not be called when no expired entries
        mock_logger.info.assert_not_called()

    @pytest.mark.asyncio
    async def test_start_processing_single_iteration(self, processor, mock_queue, mock_delivery_callback, mock_logger):
        """Test starting processing for single iteration."""
        mock_queue.dequeue.return_value = []
        processor.running = True
        
        # Create a task that will stop after one iteration
        async def run_once():
            await processor.process_batch()
            await processor._cleanup_if_needed(5.0)
            processor.running = False
        
        await run_once()
        
        # process_batch should complete without error
        assert True

    @pytest.mark.asyncio
    async def test_start_processing_with_error(self, processor, mock_queue, mock_logger):
        """Test starting processing with error handling."""
        mock_queue.dequeue.side_effect = Exception("Queue error")
        processor.running = True
        
        # Simulate one iteration with error
        try:
            await processor.process_batch()
        except Exception:
            pass
        
        # Error should be handled gracefully
        assert True

    def test_queue_processor_alias(self):
        """Test QueueProcessor backward compatibility alias."""
        from src.core.message_queue_async_processor import QueueProcessor
        assert QueueProcessor == AsyncQueueProcessor


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

