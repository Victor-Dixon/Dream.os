"""
Tests for message_batching_service.py

Comprehensive tests for message batching, consolidation, and queue management.
Target: 10+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
import json
import tempfile
import shutil

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
    """Tests for MessageBatch class."""

    def test_initialization(self):
        """Test batch initialization."""
        batch = MessageBatch("Agent-6", "Agent-1")
        assert batch.agent_id == "Agent-6"
        assert batch.recipient == "Agent-1"
        assert batch.messages == []
        assert batch.metadata == {}

    def test_add_message(self):
        """Test adding message to batch."""
        batch = MessageBatch("Agent-6", "Agent-1")
        batch.add_message("Test message 1")
        assert batch.size() == 1
        assert "Test message 1" in batch.messages

    def test_add_multiple_messages(self):
        """Test adding multiple messages."""
        batch = MessageBatch("Agent-6", "Agent-1")
        for i in range(5):
            batch.add_message(f"Message {i}")
        assert batch.size() == 5

    def test_add_message_max_size(self):
        """Test adding message when batch is at max size."""
        batch = MessageBatch("Agent-6", "Agent-1")
        # Add messages up to max size
        for i in range(MessageBatch.MAX_BATCH_SIZE):
            batch.add_message(f"Message {i}")
        assert batch.size() == MessageBatch.MAX_BATCH_SIZE
        
        # Adding one more should still work (warning logged)
        batch.add_message("Overflow message")
        assert batch.size() == MessageBatch.MAX_BATCH_SIZE + 1

    def test_get_consolidated_message_empty(self):
        """Test getting consolidated message from empty batch."""
        batch = MessageBatch("Agent-6", "Agent-1")
        result = batch.get_consolidated_message()
        assert result == ""

    def test_get_consolidated_message_single(self):
        """Test getting consolidated message with single message."""
        batch = MessageBatch("Agent-6", "Agent-1")
        batch.add_message("Test message")
        result = batch.get_consolidated_message()
        
        assert "[BATCHED UPDATES from Agent-6]" in result
        assert "UPDATE 1/1:" in result
        assert "Test message" in result
        assert "BATCH SUMMARY: 1 updates consolidated" in result

    def test_get_consolidated_message_multiple(self):
        """Test getting consolidated message with multiple messages."""
        batch = MessageBatch("Agent-6", "Agent-1")
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
        batch = MessageBatch("Agent-6", "Agent-1")
        batch.add_message("Test message")
        assert batch.size() == 1
        batch.clear()
        assert batch.size() == 0
        assert batch.messages == []

    def test_size(self):
        """Test getting batch size."""
        batch = MessageBatch("Agent-6", "Agent-1")
        assert batch.size() == 0
        batch.add_message("Message 1")
        assert batch.size() == 1
        batch.add_message("Message 2")
        assert batch.size() == 2


class TestMessageBatchingService:
    """Tests for MessageBatchingService class."""

    def test_initialization(self):
        """Test service initialization."""
        service = MessageBatchingService()
        assert service._batches == {}
        assert service._lock is not None

    def test_start_batch(self):
        """Test starting a new batch."""
        service = MessageBatchingService()
        result = service.start_batch("Agent-6", "Agent-1")
        
        assert result is True
        batch_key = service._get_batch_key("Agent-6", "Agent-1")
        assert batch_key in service._batches

    def test_start_batch_overwrites_existing(self):
        """Test starting batch when one already exists."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        service.add_to_batch("Agent-6", "Agent-1", "Message 1")
        
        # Start new batch should clear existing
        service.start_batch("Agent-6", "Agent-1")
        status = service.get_batch_status("Agent-6", "Agent-1")
        assert status["message_count"] == 0

    def test_add_to_batch_success(self):
        """Test adding message to existing batch."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        result = service.add_to_batch("Agent-6", "Agent-1", "Test message")
        
        assert result is True
        status = service.get_batch_status("Agent-6", "Agent-1")
        assert status["message_count"] == 1

    def test_add_to_batch_no_batch(self):
        """Test adding message when no batch exists."""
        service = MessageBatchingService()
        result = service.add_to_batch("Agent-6", "Agent-1", "Test message")
        
        assert result is False

    def test_send_batch_success(self):
        """Test sending batch successfully."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        service.add_to_batch("Agent-6", "Agent-1", "Message 1")
        service.add_to_batch("Agent-6", "Agent-1", "Message 2")
        
        success, consolidated = service.send_batch("Agent-6", "Agent-1")
        
        assert success is True
        assert "Message 1" in consolidated
        assert "Message 2" in consolidated
        # Batch should be removed after sending
        status = service.get_batch_status("Agent-6", "Agent-1")
        assert status["exists"] is False

    def test_send_batch_empty(self):
        """Test sending empty batch."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        
        success, consolidated = service.send_batch("Agent-6", "Agent-1")
        
        assert success is False
        assert consolidated == ""

    def test_send_batch_no_batch(self):
        """Test sending when no batch exists."""
        service = MessageBatchingService()
        success, consolidated = service.send_batch("Agent-6", "Agent-1")
        
        assert success is False
        assert consolidated == ""

    def test_get_batch_status_exists(self):
        """Test getting status when batch exists."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        service.add_to_batch("Agent-6", "Agent-1", "Message 1")
        
        status = service.get_batch_status("Agent-6", "Agent-1")
        
        assert status["exists"] is True
        assert status["agent_id"] == "Agent-6"
        assert status["recipient"] == "Agent-1"
        assert status["message_count"] == 1
        assert "created_at" in status

    def test_get_batch_status_not_exists(self):
        """Test getting status when batch doesn't exist."""
        service = MessageBatchingService()
        status = service.get_batch_status("Agent-6", "Agent-1")
        
        assert status["exists"] is False
        assert "message" in status

    def test_cancel_batch_success(self):
        """Test cancelling batch successfully."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        service.add_to_batch("Agent-6", "Agent-1", "Message 1")
        
        result = service.cancel_batch("Agent-6", "Agent-1")
        
        assert result is True
        status = service.get_batch_status("Agent-6", "Agent-1")
        assert status["exists"] is False

    def test_cancel_batch_not_exists(self):
        """Test cancelling batch that doesn't exist."""
        service = MessageBatchingService()
        result = service.cancel_batch("Agent-6", "Agent-1")
        
        assert result is False

    def test_save_batch_history(self):
        """Test saving batch history."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        service.add_to_batch("Agent-6", "Agent-1", "Message 1")
        
        batch = service._batches[service._get_batch_key("Agent-6", "Agent-1")]
        consolidated = batch.get_consolidated_message()
        
        with patch('builtins.open', mock_open()) as mock_file:
            service._save_batch_history(batch, consolidated)
            mock_file.assert_called_once()
            # Verify JSON was written
            call_args = mock_file.call_args
            assert 'batch_Agent-6_' in str(call_args[0][0])

    def test_save_batch_history_exception(self):
        """Test saving batch history when exception occurs."""
        service = MessageBatchingService()
        service.start_batch("Agent-6", "Agent-1")
        batch = service._batches[service._get_batch_key("Agent-6", "Agent-1")]
        
        with patch('builtins.open', side_effect=Exception("Test error")):
            # Should not raise exception
            service._save_batch_history(batch, "test message")

    def test_get_batch_key(self):
        """Test getting batch key."""
        service = MessageBatchingService()
        key = service._get_batch_key("Agent-6", "Agent-1")
        assert key == "Agent-6→Agent-1"


class TestBatchingServiceConvenienceFunctions:
    """Tests for convenience functions."""

    def test_get_batching_service_singleton(self):
        """Test that get_batching_service returns singleton."""
        service1 = get_batching_service()
        service2 = get_batching_service()
        assert service1 is service2

    def test_start_batch_function(self):
        """Test start_batch convenience function."""
        result = start_batch("Agent-6", "Agent-1")
        assert result is True
        status = get_batch_status("Agent-6", "Agent-1")
        assert status["exists"] is True

    def test_add_to_batch_function(self):
        """Test add_to_batch convenience function."""
        start_batch("Agent-6", "Agent-1")
        result = add_to_batch("Agent-6", "Agent-1", "Test message")
        assert result is True

    def test_send_batch_function(self):
        """Test send_batch convenience function."""
        start_batch("Agent-6", "Agent-1")
        add_to_batch("Agent-6", "Agent-1", "Message 1")
        success, consolidated = send_batch("Agent-6", "Agent-1")
        assert success is True
        assert "Message 1" in consolidated

    def test_get_batch_status_function(self):
        """Test get_batch_status convenience function."""
        start_batch("Agent-6", "Agent-1")
        status = get_batch_status("Agent-6", "Agent-1")
        assert status["exists"] is True

    def test_cancel_batch_function(self):
        """Test cancel_batch convenience function."""
        start_batch("Agent-6", "Agent-1")
        result = cancel_batch("Agent-6", "Agent-1")
        assert result is True
