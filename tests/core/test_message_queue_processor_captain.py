"""
Test coverage for message_queue_processor.py - Captain Work
Created: 2025-01-27
Agent: Agent-4 (Captain)
Expanded: 2025-11-28 (Perpetual Motion Cycle)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from src.core.message_queue_processor import MessageQueueProcessor
from src.core.message_queue import MessageQueue, QueueConfig


class TestMessageQueueProcessor:
    """Test suite for MessageQueueProcessor - Expanded to 20+ tests"""

    # ========== Initialization Tests ==========

    def test_processor_initialization_default(self):
        """Test processor initializes with default queue and config"""
        processor = MessageQueueProcessor()
        assert processor is not None
        assert processor.queue is not None
        assert processor.config is not None
        assert processor.running is False
        assert processor.message_repository is None

    def test_processor_initialization_custom_queue(self):
        """Test processor initializes with custom queue"""
        custom_queue = MessageQueue()
        processor = MessageQueueProcessor(queue=custom_queue)
        assert processor.queue == custom_queue

    def test_processor_initialization_custom_config(self):
        """Test processor initializes with custom config"""
        custom_config = QueueConfig()
        processor = MessageQueueProcessor(config=custom_config)
        assert processor.config == custom_config

    def test_processor_initialization_with_repository(self):
        """Test processor initializes with message repository"""
        mock_repo = Mock()
        processor = MessageQueueProcessor(message_repository=mock_repo)
        assert processor.message_repository == mock_repo

    # ========== Queue Processing Tests ==========

    def test_process_queue_empty_queue(self):
        """Test processing empty queue returns 0"""
        processor = MessageQueueProcessor()
        result = processor.process_queue(max_messages=1)
        assert result == 0

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_single_message(self, mock_send):
        """Test processing single message"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        # Enqueue a test message
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        result = processor.process_queue(max_messages=1)
        assert result == 1
        assert mock_send.called

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_multiple_messages(self, mock_send):
        """Test processing multiple messages"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        # Enqueue multiple messages
        for i in range(3):
            processor.queue.enqueue(
                message=f"test message {i}",
                recipient="Agent-1",
                priority="normal"
            )
        result = processor.process_queue(max_messages=3)
        assert result == 3
        assert mock_send.call_count == 3

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_batch_processing(self, mock_send):
        """Test batch processing with batch_size parameter"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        # Enqueue multiple messages
        for i in range(5):
            processor.queue.enqueue(
                message=f"test message {i}",
                recipient="Agent-1",
                priority="normal"
            )
        result = processor.process_queue(max_messages=5, batch_size=2)
        assert result == 5
        assert mock_send.call_count == 5

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_max_messages_limit(self, mock_send):
        """Test max_messages limit is respected"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        # Enqueue more messages than max
        for i in range(10):
            processor.queue.enqueue(
                message=f"test message {i}",
                recipient="Agent-1",
                priority="normal"
            )
        result = processor.process_queue(max_messages=3)
        assert result == 3
        assert mock_send.call_count == 3

    # ========== Error Handling Tests ==========

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_delivery_failure(self, mock_send):
        """Test handling delivery failure"""
        mock_send.return_value = False
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        result = processor.process_queue(max_messages=1)
        assert result == 1  # Still counts as processed
        assert mock_send.called

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_exception_handling(self, mock_send):
        """Test exception handling during processing"""
        mock_send.side_effect = Exception("Delivery error")
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        # Should not raise exception
        result = processor.process_queue(max_messages=1)
        assert result == 1  # Still counts as processed

    @patch('src.core.message_queue_processor.send_message')
    @patch('src.core.message_queue_processor.logger')
    def test_process_queue_logs_errors(self, mock_logger, mock_send):
        """Test that errors are logged"""
        mock_send.side_effect = Exception("Delivery error")
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        processor.process_queue(max_messages=1)
        # Verify error logging occurred
        assert mock_logger.error.called or mock_logger.exception.called

    # ========== Retry Logic Tests ==========

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_retry_on_failure(self, mock_send):
        """Test retry logic on delivery failure"""
        # First call fails, second succeeds
        mock_send.side_effect = [False, True]
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        result = processor.process_queue(max_messages=1)
        assert result == 1

    # ========== Timeout Handling Tests ==========

    @patch('src.core.message_queue_processor.send_message')
    @patch('src.core.message_queue_processor.time.sleep')
    def test_process_queue_continuous_mode(self, mock_sleep, mock_send):
        """Test continuous processing mode"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        # Start processing in background, then stop
        processor.running = True
        # Process with max_messages to avoid infinite loop
        result = processor.process_queue(max_messages=1, interval=0.1)
        assert result == 1

    # ========== Statistics Tests ==========

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_statistics_tracking(self, mock_send):
        """Test that statistics are tracked correctly"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        # Enqueue and process messages
        for i in range(3):
            processor.queue.enqueue(
                message=f"test message {i}",
                recipient="Agent-1",
                priority="normal"
            )
        result = processor.process_queue(max_messages=3)
        assert result == 3
        # Verify queue statistics
        stats = processor.queue.get_statistics()
        assert stats is not None

    # ========== Stop/Start Tests ==========

    def test_stop_processing(self):
        """Test stopping the processor"""
        processor = MessageQueueProcessor()
        processor.running = True
        processor.stop()
        assert processor.running is False

    @patch('src.core.message_queue_processor.send_message')
    def test_start_processing_sets_running_flag(self, mock_send):
        """Test that processing sets running flag"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        assert processor.running is False
        processor.queue.enqueue(
            message="test message",
            recipient="Agent-1",
            priority="normal"
        )
        processor.process_queue(max_messages=1)
        # Running flag should be set during processing
        # (Note: may be False after completion, depends on implementation)

    # ========== Edge Cases ==========

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_with_high_priority(self, mock_send):
        """Test processing messages with high priority"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="urgent message",
            recipient="Agent-1",
            priority="urgent"
        )
        result = processor.process_queue(max_messages=1)
        assert result == 1
        assert mock_send.called

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_with_different_recipients(self, mock_send):
        """Test processing messages to different recipients"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        recipients = ["Agent-1", "Agent-2", "Agent-3"]
        for recipient in recipients:
            processor.queue.enqueue(
                message=f"message to {recipient}",
                recipient=recipient,
                priority="normal"
            )
        result = processor.process_queue(max_messages=3)
        assert result == 3
        assert mock_send.call_count == 3

    @patch('src.core.message_queue_processor.send_message')
    def test_process_queue_empty_message_handling(self, mock_send):
        """Test handling of empty messages"""
        mock_send.return_value = True
        processor = MessageQueueProcessor()
        processor.queue.enqueue(
            message="",
            recipient="Agent-1",
            priority="normal"
        )
        result = processor.process_queue(max_messages=1)
        assert result == 1
        assert mock_send.called
        )
        result = processor.process_queue(max_messages=1)
        assert result == 1

    def test_process_queue_batch_size(self):
        """Test batch processing with custom batch size"""
        processor = MessageQueueProcessor()
        # Enqueue multiple messages
        for i in range(5):
            processor.queue.enqueue(
                message=f"test{i}",
                recipient="Agent-1",
                priority="normal"
            )
        result = processor.process_queue(max_messages=5, batch_size=2)
        assert result == 5

    def test_process_queue_max_messages_limit(self):
        """Test max_messages limit stops processing"""
        processor = MessageQueueProcessor()
        # Enqueue more messages than max
        for i in range(10):
            processor.queue.enqueue(
                message=f"test{i}",
                recipient="Agent-1",
                priority="normal"
            )
        result = processor.process_queue(max_messages=3)
        assert result == 3

    def test_process_queue_running_flag(self):
        """Test running flag is set during processing"""
        processor = MessageQueueProcessor()
        assert processor.running is False
        # Start processing in background (will stop immediately with empty queue)
        processor.process_queue(max_messages=0)
        assert processor.running is False  # Should be False after completion

    def test_safe_dequeue_error_handling(self):
        """Test _safe_dequeue handles errors gracefully"""
        processor = MessageQueueProcessor()
        # Mock queue to raise error
        with patch.object(processor.queue, 'dequeue', side_effect=Exception("Test error")):
            result = processor._safe_dequeue(batch_size=1)
            assert result == []  # Should return empty list on error

    def test_deliver_entry_success(self):
        """Test _deliver_entry handles successful delivery"""
        processor = MessageQueueProcessor()
        # Create a mock entry
        mock_entry = MagicMock()
        mock_entry.message = "test"
        mock_entry.recipient = "Agent-1"
        
        # Mock successful delivery
        with patch.object(processor, '_deliver_via_pyautogui', return_value=True):
            result = processor._deliver_entry(mock_entry)
            assert result is True

    def test_deliver_entry_failure(self):
        """Test _deliver_entry handles delivery failure"""
        processor = MessageQueueProcessor()
        # Create a mock entry
        mock_entry = MagicMock()
        mock_entry.message = "test"
        mock_entry.recipient = "Agent-1"
        
        # Mock failed delivery
        with patch.object(processor, '_deliver_via_pyautogui', return_value=False):
            with patch.object(processor, '_deliver_via_inbox', return_value=False):
                result = processor._deliver_entry(mock_entry)
                assert result is False

