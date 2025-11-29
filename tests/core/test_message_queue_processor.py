"""
Unit tests for message_queue_processor.py - HIGH PRIORITY

Comprehensive tests for message queue processing, batch operations, error handling.
Target: ≥85% coverage, 15+ test methods.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import sys
import uuid
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_processor import MessageQueueProcessor
from src.core.message_queue import MessageQueue, QueueConfig
from src.core.message_queue_persistence import QueueEntry


class TestMessageQueueProcessor:
    """Test suite for message queue processor."""

    @pytest.fixture
    def mock_queue(self):
        """Create mock message queue."""
        mock = MagicMock(spec=MessageQueue)
        mock.dequeue.return_value = []
        mock.mark_delivered.return_value = True
        mock.mark_failed.return_value = True
        return mock

    @pytest.fixture
    def mock_config(self):
        """Create mock queue config."""
        return QueueConfig()

    @pytest.fixture
    def mock_repository(self):
        """Create mock message repository."""
        mock = MagicMock()
        mock.log_message.return_value = None
        return mock

    @pytest.fixture
    def processor(self, mock_queue, mock_config, mock_repository):
        """Create processor with mocked dependencies."""
        return MessageQueueProcessor(
            queue=mock_queue,
            config=mock_config,
            message_repository=mock_repository
        )

    def test_processor_initialization_with_all_params(self, mock_queue, mock_config, mock_repository):
        """Test processor initialization with all parameters."""
        processor = MessageQueueProcessor(
            queue=mock_queue,
            config=mock_config,
            message_repository=mock_repository
        )
        
        assert processor.queue == mock_queue
        assert processor.config == mock_config
        assert processor.message_repository == mock_repository
        assert processor.running is False

    def test_processor_initialization_defaults(self):
        """Test processor initialization with defaults."""
        with patch('src.core.message_queue_processor.MessageQueue') as mock_queue_class:
            mock_queue = MagicMock()
            mock_queue_class.return_value = mock_queue
            
            processor = MessageQueueProcessor()
            
            assert processor.queue is not None
            assert processor.config is not None
            assert processor.message_repository is None
            assert processor.running is False

    def test_process_queue_with_max_messages(self, processor, mock_queue):
        """Test processing queue with max_messages limit."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": "test1", "recipient": "Agent-1", "sender": "SYSTEM"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now
            ),
            QueueEntry(
                message={"content": "test2", "recipient": "Agent-2", "sender": "SYSTEM"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.7,
                status="PENDING",
                created_at=now,
                updated_at=now
            )
        ]
        
        mock_queue.dequeue.return_value = entries
        with patch.object(processor, '_deliver_entry', return_value=True):
            result = processor.process_queue(max_messages=2, batch_size=1)
            
            assert result == 2
            assert processor.running is False

    def test_process_queue_continuous_mode(self, processor, mock_queue):
        """Test processing queue in continuous mode."""
        processor.running = True
        
        # First call returns entries, second returns empty (stops loop)
        entries = [
            QueueEntry(
                message={"content": "test", "recipient": "Agent-1", "sender": "SYSTEM"},
                queue_id=str(uuid.uuid4()),
                priority_score=0.8,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        mock_queue.dequeue.side_effect = [entries, []]
        with patch.object(processor, '_deliver_entry', return_value=True), \
             patch('time.sleep') as mock_sleep:
            processor.running = True
            # Simulate stopping after first batch
            def stop_after_first():
                processor.running = False
            mock_sleep.side_effect = stop_after_first
            
            result = processor.process_queue(max_messages=None, batch_size=1, interval=0.1)
            
            assert result >= 1

    def test_process_queue_keyboard_interrupt(self, processor, mock_queue):
        """Test handling KeyboardInterrupt during processing."""
        mock_queue.dequeue.side_effect = KeyboardInterrupt()
        
        result = processor.process_queue(max_messages=10)
        
        assert result == 0
        assert processor.running is False

    def test_process_queue_exception_handling(self, processor, mock_queue):
        """Test handling exceptions during processing."""
        mock_queue.dequeue.side_effect = Exception("Test error")
        
        result = processor.process_queue(max_messages=10)
        
        assert result == 0
        assert processor.running is False

    def test_safe_dequeue_success(self, processor, mock_queue):
        """Test successful dequeue operation."""
        entries = [MagicMock()]
        mock_queue.dequeue.return_value = entries
        
        result = processor._safe_dequeue(1)
        
        assert result == entries
        mock_queue.dequeue.assert_called_once_with(batch_size=1)

    def test_safe_dequeue_exception(self, processor, mock_queue):
        """Test dequeue with exception handling."""
        mock_queue.dequeue.side_effect = Exception("Dequeue error")
        
        result = processor._safe_dequeue(1)
        
        assert result == []

    def test_deliver_entry_success(self, processor, mock_queue):
        """Test successful entry delivery."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "recipient": "Agent-1", "sender": "SYSTEM"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        with patch.object(processor, '_route_delivery', return_value=True):
            result = processor._deliver_entry(entry)
            
            assert result is True
            mock_queue.mark_delivered.assert_called_once_with("test-id")

    def test_deliver_entry_missing_message(self, processor, mock_queue):
        """Test entry delivery with missing message."""
        entry = MagicMock()
        entry.message = None
        entry.queue_id = "test-id"
        
        result = processor._deliver_entry(entry)
        
        assert result is False
        mock_queue.mark_failed.assert_called_once_with("test-id", "no_message")

    def test_deliver_entry_missing_recipient(self, processor, mock_queue):
        """Test entry delivery with missing recipient."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "sender": "SYSTEM"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        result = processor._deliver_entry(entry)
        
        assert result is False
        mock_queue.mark_failed.assert_called_once_with("test-id", "missing_recipient")

    def test_deliver_entry_missing_content(self, processor, mock_queue):
        """Test entry delivery with missing content."""
        now = datetime.now()
        entry = QueueEntry(
            message={"recipient": "Agent-1", "sender": "SYSTEM"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        result = processor._deliver_entry(entry)
        
        assert result is False
        mock_queue.mark_failed.assert_called_once_with("test-id", "missing_content")

    def test_deliver_entry_delivery_failure(self, processor, mock_queue):
        """Test entry delivery when delivery fails."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "recipient": "Agent-1", "sender": "SYSTEM"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        with patch.object(processor, '_route_delivery', return_value=False):
            result = processor._deliver_entry(entry)
            
            assert result is False
            mock_queue.mark_failed.assert_called_once_with("test-id", "delivery_failed")

    def test_deliver_entry_exception_handling(self, processor, mock_queue):
        """Test exception handling in deliver_entry."""
        entry = MagicMock()
        entry.queue_id = "test-id"
        entry.message = {"content": "test", "recipient": "Agent-1"}
        getattr(entry, "message", None)  # Trigger attribute access
        
        with patch.object(processor, '_route_delivery', side_effect=Exception("Test error")):
            result = processor._deliver_entry(entry)
            
            assert result is False
            mock_queue.mark_failed.assert_called()

    def test_route_delivery_core_success(self, processor):
        """Test routing delivery via core (success)."""
        with patch.object(processor, '_deliver_via_core', return_value=True):
            result = processor._route_delivery("Agent-1", "test content", {})
            
            assert result is True

    def test_route_delivery_core_failure_fallback(self, processor):
        """Test routing delivery with core failure and inbox fallback."""
        with patch.object(processor, '_deliver_via_core', return_value=False), \
             patch.object(processor, '_deliver_fallback_inbox', return_value=True):
            result = processor._route_delivery("Agent-1", "test content", {})
            
            assert result is True

    def test_route_delivery_queue_full_skip_pygui(self, processor):
        """Test routing delivery when queue is full (skip PyAutoGUI)."""
        # Patch where it's imported inside the method (relative import ..utils)
        with patch('src.utils.agent_queue_status.AgentQueueStatus') as mock_status_class:
            mock_status_class.is_full.return_value = True
            
            with patch.object(processor, '_deliver_fallback_inbox', return_value=True):
                result = processor._route_delivery("Agent-1", "test content", {})
                
                assert result is True
                processor._deliver_fallback_inbox.assert_called_once()

    def test_deliver_via_core_success(self, processor):
        """Test delivery via core (success)."""
        with patch('src.core.messaging_core.send_message', return_value=True), \
             patch('src.core.keyboard_control_lock.keyboard_control') as mock_kb:
            mock_kb.return_value.__enter__ = MagicMock()
            mock_kb.return_value.__exit__ = MagicMock(return_value=None)
            
            result = processor._deliver_via_core("Agent-1", "test content", {})
            
            assert result is True

    def test_deliver_via_core_failure(self, processor):
        """Test delivery via core (failure)."""
        with patch('src.core.messaging_core.send_message', return_value=False), \
             patch('src.core.keyboard_control_lock.keyboard_control') as mock_kb:
            mock_kb.return_value.__enter__ = MagicMock()
            mock_kb.return_value.__exit__ = MagicMock(return_value=None)
            
            result = processor._deliver_via_core("Agent-1", "test content", {})
            
            assert result is False

    def test_deliver_via_core_import_error(self, processor):
        """Test delivery via core with ImportError."""
        with patch('builtins.__import__', side_effect=ImportError("Module not found")):
            result = processor._deliver_via_core("Agent-1", "test content", {})
            
            assert result is False

    def test_deliver_fallback_inbox_success(self, processor):
        """Test fallback inbox delivery (success)."""
        # Patch where it's imported inside the method (absolute import src.utils)
        with patch('src.utils.inbox_utility.create_inbox_message', return_value=True):
            result = processor._deliver_fallback_inbox("Agent-1", "test content", {"sender": "SYSTEM"})
            
            assert result is True

    def test_deliver_fallback_inbox_failure(self, processor):
        """Test fallback inbox delivery (failure)."""
        # Patch where it's imported inside the method (absolute import src.utils)
        with patch('src.utils.inbox_utility.create_inbox_message', return_value=False):
            result = processor._deliver_fallback_inbox("Agent-1", "test content", {})
            
            assert result is False

    def test_deliver_fallback_inbox_exception(self, processor):
        """Test fallback inbox delivery with exception."""
        # Patch where it's imported inside the method (absolute import src.utils)
        with patch('src.utils.inbox_utility.create_inbox_message', side_effect=Exception("Test error")):
            result = processor._deliver_fallback_inbox("Agent-1", "test content", {})
            
            assert result is False

    def test_log_delivery_with_repository(self, processor, mock_repository):
        """Test logging delivery with repository."""
        entry = MagicMock()
        entry.queue_id = "test-id"
        
        processor._log_delivery(entry, "SYSTEM", "Agent-1", "test content", True)
        
        mock_repository.log_message.assert_called_once()

    def test_log_delivery_without_repository(self, processor):
        """Test logging delivery without repository."""
        processor.message_repository = None
        entry = MagicMock()
        
        # Should not raise exception
        processor._log_delivery(entry, "SYSTEM", "Agent-1", "test content", True)

    def test_log_delivery_repository_exception(self, processor, mock_repository):
        """Test logging delivery when repository raises exception."""
        entry = MagicMock()
        entry.queue_id = "test-id"
        mock_repository.log_message.side_effect = Exception("Repo error")
        
        # Should not raise exception (non-blocking)
        processor._log_delivery(entry, "SYSTEM", "Agent-1", "test content", True)

    def test_main_function_valid_arg(self):
        """Test main() function with valid argument."""
        with patch('sys.argv', ['test_message_queue_processor.py', '5']), \
             patch('src.core.message_queue_processor.MessageQueueProcessor') as mock_processor_class:
            mock_processor = MagicMock()
            mock_processor.process_queue.return_value = 5
            mock_processor_class.return_value = mock_processor
            
            MessageQueueProcessor.main()
            
            mock_processor.process_queue.assert_called_once_with(max_messages=5, batch_size=1)

    def test_main_function_invalid_arg(self):
        """Test main() function with invalid argument."""
        with patch('sys.argv', ['test_message_queue_processor.py', 'invalid']), \
             patch('src.core.message_queue_processor.MessageQueueProcessor') as mock_processor_class:
            mock_processor = MagicMock()
            mock_processor.process_queue.return_value = 0
            mock_processor_class.return_value = mock_processor
            
            MessageQueueProcessor.main()
            
            mock_processor.process_queue.assert_called_once_with(max_messages=None, batch_size=1)

    def test_deliver_entry_with_validation_blocking(self, processor, mock_queue):
        """Test entry delivery blocked by multi-agent validator."""
        now = datetime.now()
        entry = QueueEntry(
            message={"content": "test", "recipient": "Agent-1", "sender": "SYSTEM"},
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        entry.metadata = {}
        
        # Patch where it's imported inside the method (relative import ..core)
        with patch('src.core.multi_agent_request_validator.get_multi_agent_validator') as mock_get_validator:
            mock_validator = MagicMock()
            mock_validator.validate_agent_can_send_message.return_value = (
                False, "Blocked", {"collector_id": "collector-1"}
            )
            mock_get_validator.return_value = mock_validator
            
            result = processor._deliver_entry(entry)
            
            assert result is False
            mock_queue.mark_failed.assert_called()
            assert entry.metadata.get("blocked_reason") == "pending_multi_agent_request"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
