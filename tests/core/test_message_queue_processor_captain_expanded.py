"""
Expanded test coverage for message_queue_processor.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 6
Expanding existing test file to 30+ tests for ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import sys
import tempfile
import json

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_processor import MessageQueueProcessor


class TestMessageQueueProcessorExpanded:
    """Expanded test suite for MessageQueueProcessor - 30+ tests for ≥85% coverage"""

    @pytest.fixture
    def mock_queue(self):
        """Create mock message queue"""
        queue = Mock()
        queue.enqueue.return_value = "test-queue-id"
        queue.dequeue.return_value = []
        queue.get_entry_status.return_value = "PENDING"
        queue.mark_delivered.return_value = True
        queue.mark_failed.return_value = True
        return queue

    @pytest.fixture
    def mock_repository(self):
        """Create mock message repository"""
        repo = Mock()
        repo.save_message.return_value = None
        return repo

    @pytest.fixture
    def processor(self, mock_queue, mock_repository):
        """Create MessageQueueProcessor instance"""
        return MessageQueueProcessor(
            queue=mock_queue,
            message_repository=mock_repository
        )

    # ========== Initialization Tests ==========

    def test_initialization_with_queue_and_repository(self, mock_queue, mock_repository):
        """Test initialization with queue and repository"""
        processor = MessageQueueProcessor(
            queue=mock_queue,
            message_repository=mock_repository
        )
        assert processor.queue == mock_queue
        assert processor.message_repository == mock_repository

    def test_initialization_without_repository(self, mock_queue):
        """Test initialization without repository"""
        processor = MessageQueueProcessor(queue=mock_queue)
        assert processor.queue == mock_queue
        assert processor.message_repository is None

    def test_initialization_with_config(self, mock_queue):
        """Test initialization with custom config"""
        config = Mock()
        config.max_batch_size = 10
        processor = MessageQueueProcessor(queue=mock_queue, config=config)
        assert processor.config == config

    # ========== Process Queue Tests ==========

    @patch('src.core.message_queue_processor.time.sleep')
    def test_process_queue_continuous_mode(self, mock_sleep, processor, mock_queue):
        """Test process_queue in continuous mode"""
        mock_queue.dequeue.side_effect = [[], [], KeyboardInterrupt()]
        
        with pytest.raises(KeyboardInterrupt):
            processor.process_queue(continuous=True, max_messages=None)
        
        assert mock_queue.dequeue.called

    @patch('src.core.message_queue_processor.time.sleep')
    def test_process_queue_max_messages(self, mock_sleep, processor, mock_queue):
        """Test process_queue with max_messages limit"""
        mock_queue.dequeue.return_value = []
        processor.process_queue(continuous=False, max_messages=5)
        assert mock_queue.dequeue.called

    def test_process_queue_exception_handling(self, processor, mock_queue):
        """Test process_queue handles exceptions gracefully"""
        mock_queue.dequeue.side_effect = Exception("Queue error")
        
        # Should not raise exception
        processor.process_queue(continuous=False, max_messages=1)

    # ========== Safe Dequeue Tests ==========

    def test_safe_dequeue_success(self, processor, mock_queue):
        """Test _safe_dequeue returns entries successfully"""
        mock_entries = [Mock(), Mock()]
        mock_queue.dequeue.return_value = mock_entries
        
        result = processor._safe_dequeue(batch_size=2)
        assert result == mock_entries

    def test_safe_dequeue_exception(self, processor, mock_queue):
        """Test _safe_dequeue handles exceptions"""
        mock_queue.dequeue.side_effect = Exception("Dequeue error")
        
        result = processor._safe_dequeue(batch_size=1)
        assert result == []

    # ========== Deliver Entry Tests ==========

    def test_deliver_entry_missing_message(self, processor):
        """Test _deliver_entry with missing message"""
        entry = Mock()
        entry.message = None
        
        result = processor._deliver_entry(entry)
        assert result is False

    def test_deliver_entry_missing_recipient(self, processor):
        """Test _deliver_entry with missing recipient"""
        entry = Mock()
        entry.message = {"content": "test"}
        
        result = processor._deliver_entry(entry)
        assert result is False

    def test_deliver_entry_missing_content(self, processor):
        """Test _deliver_entry with missing content"""
        entry = Mock()
        entry.message = {"recipient": "Agent-1"}
        
        result = processor._deliver_entry(entry)
        assert result is False

    @patch('src.core.message_queue_processor.validate_message')
    def test_deliver_entry_validation_failure(self, mock_validate, processor):
        """Test _deliver_entry when validation fails"""
        mock_validate.return_value = False
        entry = Mock()
        entry.message = {"content": "test", "recipient": "Agent-1"}
        
        result = processor._deliver_entry(entry)
        assert result is False

    @patch('src.core.message_queue_processor.validate_message')
    @patch.object(MessageQueueProcessor, '_route_delivery')
    def test_deliver_entry_success(self, mock_route, mock_validate, processor):
        """Test _deliver_entry successful delivery"""
        mock_validate.return_value = True
        mock_route.return_value = True
        entry = Mock()
        entry.message = {"content": "test", "recipient": "Agent-1"}
        entry.queue_id = "test-123"
        
        result = processor._deliver_entry(entry)
        assert result is True
        mock_route.assert_called_once()

    @patch('src.core.message_queue_processor.validate_message')
    @patch.object(MessageQueueProcessor, '_route_delivery')
    def test_deliver_entry_delivery_failure(self, mock_route, mock_validate, processor, mock_queue):
        """Test _deliver_entry when delivery fails"""
        mock_validate.return_value = True
        mock_route.return_value = False
        entry = Mock()
        entry.message = {"content": "test", "recipient": "Agent-1"}
        entry.queue_id = "test-123"
        
        result = processor._deliver_entry(entry)
        assert result is False
        mock_queue.mark_failed.assert_called()

    @patch('src.core.message_queue_processor.validate_message')
    @patch.object(MessageQueueProcessor, '_route_delivery')
    def test_deliver_entry_exception(self, mock_route, mock_validate, processor, mock_queue):
        """Test _deliver_entry handles exceptions"""
        mock_validate.return_value = True
        mock_route.side_effect = Exception("Delivery error")
        entry = Mock()
        entry.message = {"content": "test", "recipient": "Agent-1"}
        entry.queue_id = "test-123"
        
        result = processor._deliver_entry(entry)
        assert result is False
        mock_queue.mark_failed.assert_called()

    # ========== Route Delivery Tests ==========

    @patch.object(MessageQueueProcessor, '_deliver_via_core')
    def test_route_delivery_core_success(self, mock_deliver, processor):
        """Test _route_delivery via core messaging success"""
        mock_deliver.return_value = True
        
        message = {"content": "test", "recipient": "Agent-1"}
        result = processor._route_delivery(message)
        assert result is True
        mock_deliver.assert_called_once()

    @patch.object(MessageQueueProcessor, '_deliver_via_core')
    @patch.object(MessageQueueProcessor, '_deliver_fallback_inbox')
    def test_route_delivery_core_failure_fallback(self, mock_fallback, mock_deliver, processor):
        """Test _route_delivery falls back to inbox when core fails"""
        mock_deliver.return_value = False
        mock_fallback.return_value = True
        
        message = {"content": "test", "recipient": "Agent-1"}
        result = processor._route_delivery(message)
        assert result is True
        mock_fallback.assert_called_once()

    @patch.object(MessageQueueProcessor, '_deliver_via_core')
    def test_route_delivery_exception(self, mock_deliver, processor):
        """Test _route_delivery handles exceptions"""
        mock_deliver.side_effect = Exception("Routing error")
        
        message = {"content": "test", "recipient": "Agent-1"}
        result = processor._route_delivery(message)
        assert result is False

    # ========== Deliver Via Core Tests ==========

    @patch('src.core.message_queue_processor.send_message')
    def test_deliver_via_core_success(self, mock_send, processor):
        """Test _deliver_via_core successful delivery"""
        mock_send.return_value = True
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_via_core(message)
        assert result is True
        assert mock_send.called

    @patch('src.core.message_queue_processor.send_message')
    def test_deliver_via_core_failure(self, mock_send, processor):
        """Test _deliver_via_core delivery failure"""
        mock_send.return_value = False
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_via_core(message)
        assert result is False

    @patch('src.core.message_queue_processor.send_message')
    def test_deliver_via_core_import_error(self, mock_send, processor):
        """Test _deliver_via_core handles ImportError"""
        mock_send.side_effect = ImportError("Module not found")
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_via_core(message)
        assert result is False

    @patch('src.core.message_queue_processor.send_message')
    def test_deliver_via_core_exception(self, mock_send, processor):
        """Test _deliver_via_core handles general exceptions"""
        mock_send.side_effect = Exception("Delivery error")
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_via_core(message)
        assert result is False

    # ========== Deliver Fallback Inbox Tests ==========

    @patch('src.core.message_queue_processor.deliver_to_inbox')
    def test_deliver_fallback_inbox_success(self, mock_deliver, processor):
        """Test _deliver_fallback_inbox successful delivery"""
        mock_deliver.return_value = True
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_fallback_inbox(message)
        assert result is True
        assert mock_deliver.called

    @patch('src.core.message_queue_processor.deliver_to_inbox')
    def test_deliver_fallback_inbox_failure(self, mock_deliver, processor):
        """Test _deliver_fallback_inbox delivery failure"""
        mock_deliver.return_value = False
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_fallback_inbox(message)
        assert result is False

    @patch('src.core.message_queue_processor.deliver_to_inbox')
    def test_deliver_fallback_inbox_exception(self, mock_deliver, processor):
        """Test _deliver_fallback_inbox handles exceptions"""
        mock_deliver.side_effect = Exception("Inbox error")
        message = {"content": "test", "recipient": "Agent-1", "sender": "Agent-4"}
        
        result = processor._deliver_fallback_inbox(message)
        assert result is False

    # ========== Log Delivery Tests ==========

    def test_log_delivery_with_repository(self, processor, mock_repository):
        """Test _log_delivery with repository"""
        entry = Mock()
        entry.queue_id = "test-123"
        entry.message = {"content": "test", "recipient": "Agent-1"}
        
        processor._log_delivery(entry, success=True)
        assert mock_repository.save_message.called

    def test_log_delivery_without_repository(self, processor):
        """Test _log_delivery without repository"""
        processor.message_repository = None
        entry = Mock()
        entry.queue_id = "test-123"
        
        # Should not raise exception
        processor._log_delivery(entry, success=True)

    def test_log_delivery_failure(self, processor, mock_repository):
        """Test _log_delivery logs failure"""
        entry = Mock()
        entry.queue_id = "test-123"
        entry.message = {"content": "test"}
        
        processor._log_delivery(entry, success=False)
        assert mock_repository.save_message.called

    def test_log_delivery_exception(self, processor, mock_repository):
        """Test _log_delivery handles exceptions"""
        mock_repository.save_message.side_effect = Exception("Log error")
        entry = Mock()
        entry.queue_id = "test-123"
        
        # Should not raise exception
        processor._log_delivery(entry, success=True)

    # ========== Main Method Tests ==========

    @patch('src.core.message_queue_processor.MessageQueueProcessor')
    @patch('src.core.message_queue_processor.get_message_queue')
    def test_main_valid_args(self, mock_get_queue, mock_processor_class):
        """Test main() with valid arguments"""
        mock_queue = Mock()
        mock_get_queue.return_value = mock_queue
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor
        
        with patch('sys.argv', ['message_queue_processor.py', '--max-messages', '10']):
            from src.core.message_queue_processor import main
            main()
        
        assert mock_processor.process_queue.called

    @patch('src.core.message_queue_processor.MessageQueueProcessor')
    @patch('src.core.message_queue_processor.get_message_queue')
    def test_main_invalid_args(self, mock_get_queue, mock_processor_class):
        """Test main() with invalid arguments"""
        mock_queue = Mock()
        mock_get_queue.return_value = mock_queue
        
        with patch('sys.argv', ['message_queue_processor.py', '--invalid']):
            from src.core.message_queue_processor import main
            # Should handle gracefully
            try:
                main()
            except SystemExit:
                pass

