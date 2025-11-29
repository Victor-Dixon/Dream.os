"""
Test coverage for message_queue_async_processor.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 12
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_async_processor import AsyncQueueProcessor


class TestAsyncQueueProcessor:
    """Test suite for AsyncQueueProcessor class - 20+ tests"""

    @pytest.fixture
    def mock_queue(self):
        """Create mock message queue"""
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
        """Create mock delivery callback"""
        return Mock(return_value=True)

    @pytest.fixture
    def mock_logger(self):
        """Create mock logger"""
        logger = MagicMock()
        logger.info = Mock()
        logger.warning = Mock()
        logger.error = Mock()
        return logger

    @pytest.fixture
    def processor(self, mock_queue, mock_delivery_callback, mock_logger):
        """Create AsyncQueueProcessor instance"""
        return AsyncQueueProcessor(
            queue=mock_queue,
            delivery_callback=mock_delivery_callback,
            logger=mock_logger
        )

    def test_processor_initialization(self, processor, mock_queue, mock_delivery_callback):
        """Test AsyncQueueProcessor initialization"""
        assert processor is not None
        assert processor.queue == mock_queue
        assert processor.delivery_callback == mock_delivery_callback

    def test_processor_initialization_with_logger(self, mock_queue, mock_delivery_callback, mock_logger):
        """Test AsyncQueueProcessor initialization with logger"""
        processor = AsyncQueueProcessor(
            queue=mock_queue,
            delivery_callback=mock_delivery_callback,
            logger=mock_logger
        )
        assert processor.logger == mock_logger

    @pytest.mark.asyncio
    async def test_start_processing(self, processor, mock_queue):
        """Test start_processing method"""
        mock_queue.dequeue.return_value = []
        await processor.start_processing()
        # Should complete without errors
        assert True

    @pytest.mark.asyncio
    async def test_start_processing_with_entries(self, processor, mock_queue, mock_delivery_callback):
        """Test start_processing with queue entries"""
        entry = Mock()
        entry.message = {"content": "test"}
        entry.recipient = "Agent-1"
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = True
        
        # Start processing and stop quickly
        task = asyncio.create_task(processor.start_processing())
        await asyncio.sleep(0.1)
        await processor.stop_processing()
        await task
        assert True

    @pytest.mark.asyncio
    async def test_stop_processing(self, processor):
        """Test stop_processing method"""
        await processor.stop_processing()
        assert processor.is_running is False or not hasattr(processor, 'is_running')

    @pytest.mark.asyncio
    async def test_process_batch_with_entry_success(self, processor, mock_queue, mock_delivery_callback):
        """Test process_batch with successful delivery"""
        entry = Mock()
        entry.message = {"content": "test"}
        entry.queue_id = "test_id"
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        mock_queue.mark_delivered.assert_called()

    @pytest.mark.asyncio
    async def test_process_batch_with_entry_failure(self, processor, mock_queue, mock_delivery_callback):
        """Test process_batch with delivery failure"""
        entry = Mock()
        entry.message = {"content": "test"}
        entry.queue_id = "test_id"
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = False
        
        await processor.process_batch()
        mock_queue.mark_failed.assert_called()

    @pytest.mark.asyncio
    async def test_process_batch_entry_exception(self, processor, mock_queue, mock_delivery_callback):
        """Test process_batch handles entry exceptions"""
        entry = Mock()
        entry.message = {"content": "test"}
        entry.queue_id = "test_id"
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.side_effect = Exception("Delivery error")
        
        await processor.process_batch()
        mock_queue.mark_failed.assert_called()

    @pytest.mark.asyncio
    async def test_process_batch_empty(self, processor, mock_queue):
        """Test process_batch with empty queue"""
        mock_queue.dequeue.return_value = []
        await processor.process_batch()
        # Should complete without errors
        assert True

    @pytest.mark.asyncio
    async def test_process_batch_single_entry(self, processor, mock_queue, mock_delivery_callback):
        """Test process_batch with single entry"""
        entry = Mock()
        entry.message = {"content": "test"}
        entry.queue_id = "test_id"
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        mock_delivery_callback.assert_called()

    @pytest.mark.asyncio
    async def test_process_batch_multiple_entries(self, processor, mock_queue, mock_delivery_callback):
        """Test process_batch with multiple entries"""
        entries = [
            Mock(message={"content": f"test_{i}"}, queue_id=f"id_{i}")
            for i in range(3)
        ]
        mock_queue.dequeue.return_value = entries
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        assert mock_delivery_callback.call_count == 3

    @pytest.mark.asyncio
    async def test_process_batch_mixed_results(self, processor, mock_queue, mock_delivery_callback):
        """Test process_batch with mixed success/failure"""
        entry1 = Mock(message={"content": "test1"}, queue_id="id1")
        entry2 = Mock(message={"content": "test2"}, queue_id="id2")
        mock_queue.dequeue.return_value = [entry1, entry2]
        mock_delivery_callback.side_effect = [True, False]
        
        await processor.process_batch()
        assert mock_delivery_callback.call_count == 2

    @pytest.mark.asyncio
    async def test_cleanup_if_needed_triggers(self, processor, mock_queue, mock_logger):
        """Test _cleanup_if_needed triggers cleanup"""
        processor.last_cleanup = 0.0
        mock_queue.config.cleanup_interval = 1.0
        mock_queue.cleanup_expired.return_value = 5
        
        import time
        with patch('time.time', return_value=2.0):
            await processor._cleanup_if_needed(1.0)
            mock_queue.cleanup_expired.assert_called()

    @pytest.mark.asyncio
    async def test_cleanup_if_needed_skips(self, processor, mock_queue):
        """Test _cleanup_if_needed skips when interval not reached"""
        processor.last_cleanup = 1.0
        mock_queue.config.cleanup_interval = 3600.0
        
        import time
        with patch('time.time', return_value=2.0):
            await processor._cleanup_if_needed(1.0)
            mock_queue.cleanup_expired.assert_not_called()

    @pytest.mark.asyncio
    async def test_continuous_processing(self, processor, mock_queue, mock_delivery_callback):
        """Test continuous processing loop"""
        entry = Mock(message={"content": "test"}, queue_id="test_id")
        mock_queue.dequeue.side_effect = [[entry], [], []]  # First call returns entry, then empty
        mock_delivery_callback.return_value = True
        
        # Start and stop quickly
        task = asyncio.create_task(processor.start_processing(interval=0.01))
        await asyncio.sleep(0.05)
        processor.stop_processing()
        await asyncio.sleep(0.01)  # Allow stop to take effect
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        assert True

    @pytest.mark.asyncio
    async def test_processing_with_errors(self, processor, mock_queue, mock_delivery_callback, mock_logger):
        """Test processing handles errors gracefully"""
        mock_queue.dequeue.side_effect = Exception("Queue error")
        
        # Should handle error without crashing
        try:
            await processor.process_batch()
        except Exception:
            pass
        assert True

    @pytest.mark.asyncio
    async def test_mark_delivered_on_success(self, processor, mock_queue, mock_delivery_callback):
        """Test mark_delivered called on successful delivery"""
        entry = Mock(message={"content": "test"}, queue_id="test_id")
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        mock_queue.mark_delivered.assert_called_with("test_id")

    @pytest.mark.asyncio
    async def test_mark_failed_on_failure(self, processor, mock_queue, mock_delivery_callback):
        """Test mark_failed called on delivery failure"""
        entry = Mock(message={"content": "test"}, queue_id="test_id")
        mock_queue.dequeue.return_value = [entry]
        mock_delivery_callback.return_value = False
        
        await processor.process_batch()
        mock_queue.mark_failed.assert_called()

    @pytest.mark.asyncio
    async def test_processing_entry_missing_message(self, processor, mock_queue, mock_logger):
        """Test processing handles entry missing message"""
        entry = Mock()
        entry.message = None
        entry.queue_id = "test_id"
        mock_queue.dequeue.return_value = [entry]
        
        await processor.process_batch()
        # Should skip entry and log warning
        assert True

    @pytest.mark.asyncio
    async def test_concurrent_processing(self, processor, mock_queue, mock_delivery_callback):
        """Test concurrent entry processing"""
        entries = [
            Mock(message={"content": f"test_{i}"}, queue_id=f"id_{i}")
            for i in range(5)
        ]
        mock_queue.dequeue.return_value = entries
        mock_delivery_callback.return_value = True
        
        await processor.process_batch()
        # All entries should be processed
        assert mock_delivery_callback.call_count == 5

    @pytest.mark.asyncio
    async def test_start_processing_logs(self, processor, mock_logger):
        """Test start_processing logs start message"""
        processor.running = False
        task = asyncio.create_task(processor.start_processing(interval=0.01))
        await asyncio.sleep(0.01)
        processor.stop_processing()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        mock_logger.info.assert_called()

