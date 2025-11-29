"""
Tests for message_batching_service.py

Comprehensive tests for message batching service.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from pathlib import Path
from src.services.message_batching_service import (
    MessageBatch,
    MessageBatchingService,
    get_batching_service,
    start_batch,
    add_to_batch,
    send_batch,
    get_batch_status,
    cancel_batch,
)


class TestMessageBatch:
    """Tests for MessageBatch."""

    def test_initialization(self):
        """Test batch initialization."""
        batch = MessageBatch("Agent-1", "Agent-2")
        assert batch.agent_id == "Agent-1"
        assert batch.recipient == "Agent-2"
        assert batch.messages == []
        assert isinstance(batch.created_at, datetime)
        assert batch.metadata == {}

    def test_add_message(self):
        """Test adding message to batch."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Test message 1")
        batch.add_message("Test message 2")
        
        assert len(batch.messages) == 2
        assert batch.messages[0] == "Test message 1"
        assert batch.messages[1] == "Test message 2"

    def test_add_message_size_limit(self):
        """Test batch size limit."""
        batch = MessageBatch("Agent-1", "Agent-2")
        # Add messages up to limit
        for i in range(MessageBatch.MAX_BATCH_SIZE):
            batch.add_message(f"Message {i}")
        
        # Adding one more should trigger warning but still add
        batch.add_message("Over limit")
        assert len(batch.messages) == MessageBatch.MAX_BATCH_SIZE + 1

    def test_get_consolidated_message_empty(self):
        """Test getting consolidated message from empty batch."""
        batch = MessageBatch("Agent-1", "Agent-2")
        result = batch.get_consolidated_message()
        assert result == ""

    def test_get_consolidated_message_single(self):
        """Test getting consolidated message with single message."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Test message")
        result = batch.get_consolidated_message()
        
        assert "[BATCHED UPDATES from Agent-1]" in result
        assert "UPDATE 1/1:" in result
        assert "Test message" in result
        assert "BATCH SUMMARY: 1 updates consolidated" in result

    def test_get_consolidated_message_multiple(self):
        """Test getting consolidated message with multiple messages."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Message 1")
        batch.add_message("Message 2")
        batch.add_message("Message 3")
        result = batch.get_consolidated_message()
        
        assert "UPDATE 1/3:" in result
        assert "UPDATE 2/3:" in result
        assert "UPDATE 3/3:" in result
        assert "Message 1" in result
        assert "Message 2" in result
        assert "Message 3" in result
        assert "BATCH SUMMARY: 3 updates consolidated" in result

    def test_clear(self):
        """Test clearing batch."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Test message")
        batch.clear()
        
        assert len(batch.messages) == 0

    def test_size(self):
        """Test getting batch size."""
        batch = MessageBatch("Agent-1", "Agent-2")
        assert batch.size() == 0
        
        batch.add_message("Message 1")
        assert batch.size() == 1
        
        batch.add_message("Message 2")
        assert batch.size() == 2


class TestMessageBatchingService:
    """Tests for MessageBatchingService."""

    def test_initialization(self):
        """Test service initialization."""
        service = MessageBatchingService()
        assert service._batches == {}
        assert service._lock is not None
        assert service._batch_dir.exists()

    def test_get_batch_key(self):
        """Test batch key generation."""
        service = MessageBatchingService()
        key = service._get_batch_key("Agent-1", "Agent-2")
        assert key == "Agent-1→Agent-2"

    def test_start_batch(self):
        """Test starting a new batch."""
        service = MessageBatchingService()
        result = service.start_batch("Agent-1", "Agent-2")
        
        assert result is True
        batch_key = service._get_batch_key("Agent-1", "Agent-2")
        assert batch_key in service._batches
        assert service._batches[batch_key].agent_id == "Agent-1"
        assert service._batches[batch_key].recipient == "Agent-2"

    def test_start_batch_existing(self):
        """Test starting batch when one already exists."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Message 1")
        
        # Start again should clear existing
        result = service.start_batch("Agent-1", "Agent-2")
        assert result is True
        batch_key = service._get_batch_key("Agent-1", "Agent-2")
        assert service._batches[batch_key].size() == 0

    def test_add_to_batch_success(self):
        """Test adding message to batch successfully."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        result = service.add_to_batch("Agent-1", "Agent-2", "Test message")
        
        assert result is True
        batch_key = service._get_batch_key("Agent-1", "Agent-2")
        assert service._batches[batch_key].size() == 1

    def test_add_to_batch_no_batch(self):
        """Test adding message when no batch exists."""
        service = MessageBatchingService()
        result = service.add_to_batch("Agent-1", "Agent-2", "Test message")
        
        assert result is False

    def test_send_batch_success(self):
        """Test sending batch successfully."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Message 1")
        service.add_to_batch("Agent-1", "Agent-2", "Message 2")
        
        with patch.object(service, '_save_batch_history'):
            success, message = service.send_batch("Agent-1", "Agent-2")
            
            assert success is True
            assert "Message 1" in message
            assert "Message 2" in message
            assert "BATCH SUMMARY: 2 updates consolidated" in message
            # Batch should be removed after sending
            batch_key = service._get_batch_key("Agent-1", "Agent-2")
            assert batch_key not in service._batches

    def test_send_batch_no_batch(self):
        """Test sending batch when no batch exists."""
        service = MessageBatchingService()
        success, message = service.send_batch("Agent-1", "Agent-2")
        
        assert success is False
        assert message == ""

    def test_send_batch_empty(self):
        """Test sending empty batch."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        success, message = service.send_batch("Agent-1", "Agent-2")
        
        assert success is False
        assert message == ""

    def test_get_batch_status_exists(self):
        """Test getting batch status when batch exists."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Message 1")
        
        status = service.get_batch_status("Agent-1", "Agent-2")
        
        assert status["exists"] is True
        assert status["agent_id"] == "Agent-1"
        assert status["recipient"] == "Agent-2"
        assert status["message_count"] == 1
        assert "created_at" in status

    def test_get_batch_status_not_exists(self):
        """Test getting batch status when batch doesn't exist."""
        service = MessageBatchingService()
        status = service.get_batch_status("Agent-1", "Agent-2")
        
        assert status["exists"] is False
        assert "message" in status

    def test_cancel_batch_success(self):
        """Test cancelling batch successfully."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Message 1")
        
        result = service.cancel_batch("Agent-1", "Agent-2")
        
        assert result is True
        batch_key = service._get_batch_key("Agent-1", "Agent-2")
        assert batch_key not in service._batches

    def test_cancel_batch_not_exists(self):
        """Test cancelling batch when it doesn't exist."""
        service = MessageBatchingService()
        result = service.cancel_batch("Agent-1", "Agent-2")
        
        assert result is False

    def test_save_batch_history(self):
        """Test saving batch history."""
        service = MessageBatchingService()
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Message 1")
        consolidated = batch.get_consolidated_message()
        
        with patch('builtins.open', mock_open()) as mock_file:
            service._save_batch_history(batch, consolidated)
            mock_file.assert_called_once()
            # Verify JSON was written
            assert mock_file().write.called

    def test_save_batch_history_exception(self):
        """Test exception handling in save_batch_history."""
        service = MessageBatchingService()
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Message 1")
        consolidated = batch.get_consolidated_message()
        
        with patch('builtins.open', side_effect=Exception("Test error")):
            # Should not raise, just log error
            service._save_batch_history(batch, consolidated)


class TestBatchingServiceConvenienceFunctions:
    """Tests for convenience functions."""

    def test_get_batching_service_singleton(self):
        """Test that get_batching_service returns singleton."""
        # Reset global instance
        import src.services.message_batching_service as module
        module._batching_service = None
        
        service1 = get_batching_service()
        service2 = get_batching_service()
        
        assert service1 is service2
        assert isinstance(service1, MessageBatchingService)

    def test_start_batch_function(self):
        """Test start_batch convenience function."""
        import src.services.message_batching_service as module
        module._batching_service = None
        
        result = start_batch("Agent-1", "Agent-2")
        assert result is True

    def test_add_to_batch_function(self):
        """Test add_to_batch convenience function."""
        import src.services.message_batching_service as module
        module._batching_service = None
        
        start_batch("Agent-1", "Agent-2")
        result = add_to_batch("Agent-1", "Agent-2", "Test message")
        assert result is True

    def test_send_batch_function(self):
        """Test send_batch convenience function."""
        import src.services.message_batching_service as module
        module._batching_service = None
        
        start_batch("Agent-1", "Agent-2")
        add_to_batch("Agent-1", "Agent-2", "Message 1")
        
        with patch.object(get_batching_service(), '_save_batch_history'):
            success, message = send_batch("Agent-1", "Agent-2")
            assert success is True
            assert "Message 1" in message

    def test_get_batch_status_function(self):
        """Test get_batch_status convenience function."""
        import src.services.message_batching_service as module
        module._batching_service = None
        
        start_batch("Agent-1", "Agent-2")
        status = get_batch_status("Agent-1", "Agent-2")
        assert status["exists"] is True

    def test_cancel_batch_function(self):
        """Test cancel_batch convenience function."""
        import src.services.message_batching_service as module
        module._batching_service = None
        
        start_batch("Agent-1", "Agent-2")
        result = cancel_batch("Agent-1", "Agent-2")
        assert result is True

