#!/usr/bin/env python3
"""
Message Queue Processor Integration Test Suite
==============================================

Comprehensive integration tests for V3 Message Queue Processor
validating unified messaging core integration.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Test imports
from src.core.message_queue import MessageQueue, QueueConfig
from src.core.message_queue_processor import MessageQueueProcessor


class TestMessageQueueProcessorIntegration:
    """Integration tests for Message Queue Processor with unified messaging core."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary directory for queue storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def queue_config(self, temp_queue_dir):
        """Create queue configuration for testing."""
        return QueueConfig(queue_dir=str(temp_queue_dir))

    @pytest.fixture
    def message_queue(self, queue_config):
        """Create message queue instance."""
        return MessageQueue(config=queue_config)

    @pytest.fixture
    def processor(self, message_queue):
        """Create message queue processor instance."""
        return MessageQueueProcessor(queue=message_queue)

    def test_imports_available(self):
        """Test that all required imports are available."""
        # Test messaging_core import
        try:
            from src.core.messaging_core import send_message
            assert callable(send_message), "send_message should be callable"
        except ImportError as e:
            pytest.fail(f"Failed to import send_message: {e}")

        # Test messaging_models_core imports
        try:
            from src.core.messaging_models_core import (
                UnifiedMessageType,
                UnifiedMessagePriority,
                UnifiedMessageTag,
            )
            assert UnifiedMessageType.SYSTEM_TO_AGENT is not None
            assert UnifiedMessagePriority.REGULAR is not None
            assert UnifiedMessageTag.SYSTEM is not None
        except ImportError as e:
            pytest.fail(f"Failed to import messaging models: {e}")

    def test_processor_initialization(self, processor):
        """Test processor initializes correctly."""
        assert processor is not None
        assert processor.queue is not None
        assert processor.running is False

    def test_deliver_via_core_imports(self, processor):
        """Test that _deliver_via_core can import required modules."""
        # This tests the import path used in _deliver_via_core
        try:
            from src.core.messaging_core import send_message
            from src.core.messaging_models_core import (
                UnifiedMessageType,
                UnifiedMessagePriority,
                UnifiedMessageTag,
            )

            # Verify enums have expected values
            assert UnifiedMessageType.SYSTEM_TO_AGENT.value == "system_to_agent"
            assert UnifiedMessagePriority.REGULAR.value == "regular"
            assert UnifiedMessageTag.SYSTEM.value == "system"
        except ImportError as e:
            pytest.fail(f"Import test failed: {e}")

    @patch("src.core.message_queue_processor.send_message")
    def test_deliver_via_core_success(self, mock_send_message, processor):
        """Test successful delivery via unified messaging core."""
        mock_send_message.return_value = True

        result = processor._deliver_via_core("Agent-1", "Test message")

        assert result is True
        mock_send_message.assert_called_once()
        call_args = mock_send_message.call_args

        # Verify call arguments
        assert call_args.kwargs["content"] == "Test message"
        assert call_args.kwargs["sender"] == "SYSTEM"
        assert call_args.kwargs["recipient"] == "Agent-1"
        assert call_args.kwargs["message_type"].value == "system_to_agent"
        assert call_args.kwargs["priority"].value == "regular"
        assert len(call_args.kwargs["tags"]) == 1
        assert call_args.kwargs["tags"][0].value == "system"

    @patch("src.core.message_queue_processor.send_message")
    def test_deliver_via_core_failure(self, mock_send_message, processor):
        """Test failed delivery via unified messaging core."""
        mock_send_message.return_value = False

        result = processor._deliver_via_core("Agent-1", "Test message")

        assert result is False
        mock_send_message.assert_called_once()

    @patch("src.core.message_queue_processor.send_message")
    def test_deliver_via_core_exception(self, mock_send_message, processor):
        """Test exception handling in _deliver_via_core."""
        mock_send_message.side_effect = Exception("Delivery error")

        result = processor._deliver_via_core("Agent-1", "Test message")

        assert result is False

    def test_deliver_fallback_inbox(self, processor, temp_queue_dir):
        """Test inbox fallback delivery path."""
        # Mock agent workspace path
        with patch("src.core.message_queue_processor.Path") as mock_path:
            mock_inbox = MagicMock()
            mock_inbox.mkdir.return_value = None
            mock_file = MagicMock()
            mock_inbox.__truediv__.return_value = mock_file
            mock_path.return_value = mock_inbox

            result = processor._deliver_fallback_inbox("Agent-1", "Test message")

            assert result is True
            mock_inbox.mkdir.assert_called_once_with(parents=True, exist_ok=True)
            mock_file.write_text.assert_called_once()

    def test_route_delivery_primary_path(self, processor):
        """Test routing uses primary path (unified core) first."""
        with patch.object(
            processor, "_deliver_via_core", return_value=True
        ) as mock_core:
            with patch.object(
                processor, "_deliver_fallback_inbox"
            ) as mock_fallback:
                result = processor._route_delivery("Agent-1", "Test message")

                assert result is True
                mock_core.assert_called_once_with("Agent-1", "Test message")
                mock_fallback.assert_not_called()

    def test_route_delivery_fallback_path(self, processor):
        """Test routing falls back to inbox on core failure."""
        with patch.object(
            processor, "_deliver_via_core", side_effect=Exception("Core failed")
        ) as mock_core:
            with patch.object(
                processor, "_deliver_fallback_inbox", return_value=True
            ) as mock_fallback:
                result = processor._route_delivery("Agent-1", "Test message")

                assert result is True
                mock_core.assert_called_once()
                mock_fallback.assert_called_once_with("Agent-1", "Test message")

    def test_deliver_entry_complete_flow(self, processor):
        """Test complete entry delivery flow."""
        # Create mock entry
        mock_entry = MagicMock()
        mock_entry.queue_id = "test_queue_123"
        mock_entry.message = {
            "recipient": "Agent-1",
            "content": "Test message",
            "sender": "SYSTEM",
        }

        with patch.object(processor, "_route_delivery", return_value=True):
            with patch.object(processor.queue, "mark_delivered") as mock_mark:
                with patch.object(processor, "_log_delivery") as mock_log:
                    result = processor._deliver_entry(mock_entry)

                    assert result is True
                    mock_mark.assert_called_once_with("test_queue_123")
                    mock_log.assert_called_once()

    def test_deliver_entry_missing_recipient(self, processor):
        """Test entry delivery with missing recipient."""
        mock_entry = MagicMock()
        mock_entry.queue_id = "test_queue_123"
        mock_entry.message = {"content": "Test message"}

        with patch.object(processor.queue, "mark_failed") as mock_failed:
            result = processor._deliver_entry(mock_entry)

            assert result is False
            mock_failed.assert_called_once()
            assert "missing_recipient" in str(mock_failed.call_args)

    def test_deliver_entry_missing_content(self, processor):
        """Test entry delivery with missing content."""
        mock_entry = MagicMock()
        mock_entry.queue_id = "test_queue_123"
        mock_entry.message = {"recipient": "Agent-1"}

        with patch.object(processor.queue, "mark_failed") as mock_failed:
            result = processor._deliver_entry(mock_entry)

            assert result is False
            mock_failed.assert_called_once()
            assert "missing_content" in str(mock_failed.call_args)

    def test_format_inbox_message(self, processor):
        """Test inbox message formatting."""
        formatted = processor._format_inbox_message("Agent-1", "Test content")

        assert "Agent-1" in formatted
        assert "Test content" in formatted
        assert "SYSTEM" in formatted
        assert "Queue Message" in formatted

    @patch("src.core.message_queue_processor.send_message")
    def test_end_to_end_queue_processing(self, mock_send_message, processor):
        """Test end-to-end queue processing flow."""
        mock_send_message.return_value = True

        # Enqueue test message
        queue_id = processor.queue.enqueue(
            {
                "recipient": "Agent-1",
                "content": "Integration test message",
                "sender": "TEST_SYSTEM",
            }
        )

        assert queue_id is not None

        # Process single message
        processed = processor.process_queue(max_messages=1, batch_size=1)

        assert processed == 1
        mock_send_message.assert_called_once()

        # Verify message marked as delivered
        entry = processor.queue.get_entry(queue_id)
        assert entry is not None
        assert entry.status == "DELIVERED"

    def test_keyboard_control_integration(self, processor):
        """Test keyboard control context manager integration."""
        from src.core.keyboard_control_lock import keyboard_control

        # Verify keyboard_control is available
        assert callable(keyboard_control)

        # Test that it can be used as context manager
        with keyboard_control("test_lock"):
            pass  # Should not raise

    def test_message_type_enum_values(self):
        """Test that message type enum has expected values."""
        from src.core.messaging_models_core import UnifiedMessageType

        assert UnifiedMessageType.SYSTEM_TO_AGENT.value == "system_to_agent"
        assert UnifiedMessageType.TEXT.value == "text"
        assert UnifiedMessageType.BROADCAST.value == "broadcast"

    def test_priority_enum_values(self):
        """Test that priority enum has expected values."""
        from src.core.messaging_models_core import UnifiedMessagePriority

        assert UnifiedMessagePriority.REGULAR.value == "regular"
        assert UnifiedMessagePriority.URGENT.value == "urgent"

    def test_tag_enum_values(self):
        """Test that tag enum has expected values."""
        from src.core.messaging_models_core import UnifiedMessageTag

        assert UnifiedMessageTag.SYSTEM.value == "system"
        assert UnifiedMessageTag.CAPTAIN.value == "captain"

    @patch("src.core.message_queue_processor.send_message")
    def test_processor_with_repository(self, mock_send_message, processor):
        """Test processor integration with message repository."""
        mock_send_message.return_value = True

        # Create mock repository
        mock_repo = MagicMock()
        processor.message_repository = mock_repo

        # Enqueue and process
        queue_id = processor.queue.enqueue(
            {
                "recipient": "Agent-1",
                "content": "Test with repo",
                "sender": "TEST",
            }
        )

        processor.process_queue(max_messages=1, batch_size=1)

        # Verify repository was called
        assert mock_repo.log_message.called

    def test_error_isolation(self, processor):
        """Test that errors in one entry don't stop processing."""
        # Create two entries - one will fail, one will succeed
        queue_id_1 = processor.queue.enqueue(
            {"recipient": None, "content": "Will fail"}  # Missing recipient
        )

        queue_id_2 = processor.queue.enqueue(
            {"recipient": "Agent-1", "content": "Will succeed", "sender": "TEST"}
        )

        with patch.object(processor, "_route_delivery", return_value=True):
            processed = processor.process_queue(max_messages=2, batch_size=2)

            # Should process both, even though one fails
            assert processed == 2

            # First should be failed
            entry_1 = processor.queue.get_entry(queue_id_1)
            assert entry_1.status == "FAILED"

            # Second should be delivered
            entry_2 = processor.queue.get_entry(queue_id_2)
            assert entry_2.status == "DELIVERED"


    @patch("src.core.message_queue_processor.send_message")
    def test_batch_processing_multiple_messages(self, mock_send_message, processor):
        """Test batch processing with multiple messages."""
        mock_send_message.return_value = True
        
        # Enqueue multiple messages
        queue_ids = []
        for i in range(5):
            queue_id = processor.queue.enqueue({
                "recipient": f"Agent-{i+1}",
                "content": f"Batch message {i+1}",
                "sender": "TEST"
            })
            queue_ids.append(queue_id)
        
        # Process in batches
        processed = processor.process_queue(max_messages=5, batch_size=2)
        
        assert processed == 5
        assert mock_send_message.call_count == 5
        
        # Verify all marked as delivered
        for queue_id in queue_ids:
            entry = processor.queue.get_entry(queue_id)
            assert entry.status == "DELIVERED"

    @patch("src.core.message_queue_processor.send_message")
    def test_batch_processing_partial_batch(self, mock_send_message, processor):
        """Test processing partial batch when fewer messages than batch_size."""
        mock_send_message.return_value = True
        
        # Enqueue 3 messages
        queue_ids = []
        for i in range(3):
            queue_id = processor.queue.enqueue({
                "recipient": "Agent-1",
                "content": f"Message {i+1}",
                "sender": "TEST"
            })
            queue_ids.append(queue_id)
        
        # Process with batch_size=5 (larger than available)
        processed = processor.process_queue(max_messages=3, batch_size=5)
        
        assert processed == 3
        assert mock_send_message.call_count == 3

    def test_batch_processing_with_persistence_roundtrip(self, processor):
        """Test batch processing persists status correctly."""
        # Enqueue multiple messages
        queue_ids = []
        for i in range(3):
            queue_id = processor.queue.enqueue({
                "recipient": "Agent-1",
                "content": f"Persistence test {i+1}",
                "sender": "TEST"
            })
            queue_ids.append(queue_id)
        
        # Process with mock delivery
        with patch.object(processor, "_route_delivery", return_value=True):
            processed = processor.process_queue(max_messages=3, batch_size=1)
        
        assert processed == 3
        
        # Verify persistence - reload from file
        entries = processor.queue.persistence.load_entries()
        assert len(entries) == 3
        assert all(e.status == "DELIVERED" for e in entries)

    @patch("src.core.message_queue_processor.send_message")
    def test_batch_processing_mixed_success_failure(self, mock_send_message, processor):
        """Test batch processing with mixed success and failure."""
        mock_send_message.side_effect = [True, False, True]
        
        # Enqueue 3 messages
        queue_ids = []
        for i in range(3):
            queue_id = processor.queue.enqueue({
                "recipient": "Agent-1",
                "content": f"Mixed test {i+1}",
                "sender": "TEST"
            })
            queue_ids.append(queue_id)
        
        # Process all
        processed = processor.process_queue(max_messages=3, batch_size=3)
        
        assert processed == 3
        
        # Verify statuses
        entry1 = processor.queue.get_entry(queue_ids[0])
        entry2 = processor.queue.get_entry(queue_ids[1])
        entry3 = processor.queue.get_entry(queue_ids[2])
        
        assert entry1.status == "DELIVERED"
        assert entry2.status == "FAILED"
        assert entry3.status == "DELIVERED"

    def test_batch_processing_empty_queue(self, processor):
        """Test batch processing with empty queue."""
        processed = processor.process_queue(max_messages=5, batch_size=2)
        
        assert processed == 0

    @patch("src.core.message_queue_processor.send_message")
    def test_batch_processing_max_messages_limit(self, mock_send_message, processor):
        """Test batch processing respects max_messages limit."""
        mock_send_message.return_value = True
        
        # Enqueue 10 messages
        for i in range(10):
            processor.queue.enqueue({
                "recipient": "Agent-1",
                "content": f"Message {i+1}",
                "sender": "TEST"
            })
        
        # Process only 5
        processed = processor.process_queue(max_messages=5, batch_size=2)
        
        assert processed == 5
        assert mock_send_message.call_count == 5

    def test_processor_dependency_injection(self, message_queue):
        """Test processor accepts injected messaging core."""
        mock_core = MagicMock()
        mock_core.send_message.return_value = True
        
        processor = MessageQueueProcessor(
            queue=message_queue,
            messaging_core=mock_core
        )
        
        # Enqueue message
        queue_id = message_queue.enqueue({
            "recipient": "Agent-1",
            "content": "Injection test",
            "sender": "TEST"
        })
        
        # Process
        processed = processor.process_queue(max_messages=1)
        
        assert processed == 1
        assert mock_core.send_message.called
        assert processor.messaging_core == mock_core


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

