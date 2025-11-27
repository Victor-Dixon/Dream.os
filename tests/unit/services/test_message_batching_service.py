"""
Unit tests for message_batching_service.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path

from src.services.message_batching_service import (
    MessageBatch,
    MessageBatchingService,
)


class TestMessageBatch:
    """Tests for MessageBatch class."""

    def test_init(self):
        """Test MessageBatch initialization."""
        batch = MessageBatch("Agent-1", "Agent-2")
        assert batch.agent_id == "Agent-1"
        assert batch.recipient == "Agent-2"
        assert batch.messages == []
        assert isinstance(batch.created_at, datetime)
        assert batch.metadata == {}

    def test_add_message(self):
        """Test adding message to batch."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Test message")
        assert len(batch.messages) == 1
        assert batch.messages[0] == "Test message"

    def test_add_message_max_size(self):
        """Test batch size limit enforcement."""
        batch = MessageBatch("Agent-1", "Agent-2")
        # Add messages up to max size
        for i in range(MessageBatch.MAX_BATCH_SIZE):
            batch.add_message(f"Message {i}")
        assert batch.size() == MessageBatch.MAX_BATCH_SIZE
        # Adding one more should trigger warning but still add
        batch.add_message("Overflow message")
        assert batch.size() == MessageBatch.MAX_BATCH_SIZE + 1

    def test_get_consolidated_message_empty(self):
        """Test consolidated message for empty batch."""
        batch = MessageBatch("Agent-1", "Agent-2")
        result = batch.get_consolidated_message()
        assert result == ""

    def test_get_consolidated_message_single(self):
        """Test consolidated message for single message."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Test message")
        result = batch.get_consolidated_message()
        assert "BATCHED UPDATES from Agent-1" in result
        assert "UPDATE 1/1:" in result
        assert "Test message" in result
        assert "BATCH SUMMARY: 1 updates" in result

    def test_get_consolidated_message_multiple(self):
        """Test consolidated message for multiple messages."""
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
        assert "BATCH SUMMARY: 3 updates" in result

    def test_clear(self):
        """Test clearing batch."""
        batch = MessageBatch("Agent-1", "Agent-2")
        batch.add_message("Test message")
        assert batch.size() == 1
        batch.clear()
        assert batch.size() == 0
        assert batch.messages == []

    def test_size(self):
        """Test batch size method."""
        batch = MessageBatch("Agent-1", "Agent-2")
        assert batch.size() == 0
        batch.add_message("Message 1")
        assert batch.size() == 1
        batch.add_message("Message 2")
        assert batch.size() == 2


class TestMessageBatchingService:
    """Tests for MessageBatchingService class."""

    def test_init(self):
        """Test MessageBatchingService initialization."""
        service = MessageBatchingService()
        assert service._batches == {}
        assert service._batch_dir.exists()

    def test_get_batch_key(self):
        """Test batch key generation."""
        service = MessageBatchingService()
        key = service._get_batch_key("Agent-1", "Agent-2")
        assert key == "Agent-1→Agent-2"

    def test_add_to_batch_no_batch_started(self):
        """Test adding message to batch without starting batch."""
        service = MessageBatchingService()
        result = service.add_to_batch("Agent-1", "Agent-2", "Test message")
        assert result is False

    def test_add_to_batch_after_start(self):
        """Test adding message to batch after starting."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        result = service.add_to_batch("Agent-1", "Agent-2", "Test message")
        assert result is True
        key = "Agent-1→Agent-2"
        assert key in service._batches
        assert service._batches[key].size() == 1

    def test_send_batch(self):
        """Test sending batch."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Test message")
        success, message = service.send_batch("Agent-1", "Agent-2")
        assert success is True
        assert "Test message" in message
        # Batch should be deleted after sending
        key = "Agent-1→Agent-2"
        assert key not in service._batches

    def test_send_batch_empty(self):
        """Test sending empty batch."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        success, message = service.send_batch("Agent-1", "Agent-2")
        assert success is False
        assert message == ""

    def test_send_batch_no_batch(self):
        """Test sending batch that doesn't exist."""
        service = MessageBatchingService()
        success, message = service.send_batch("Agent-1", "Agent-2")
        assert success is False
        assert message == ""

    def test_get_batch_status_no_batch(self):
        """Test getting batch status when no batch exists."""
        service = MessageBatchingService()
        status = service.get_batch_status("Agent-1", "Agent-2")
        assert status["exists"] is False

    def test_get_batch_status_with_batch(self):
        """Test getting batch status when batch exists."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Test message")
        status = service.get_batch_status("Agent-1", "Agent-2")
        assert status["exists"] is True
        assert status["message_count"] == 1

    def test_cancel_batch(self):
        """Test cancelling batch."""
        service = MessageBatchingService()
        service.start_batch("Agent-1", "Agent-2")
        service.add_to_batch("Agent-1", "Agent-2", "Test message")
        assert service.get_batch_status("Agent-1", "Agent-2")["exists"] is True
        result = service.cancel_batch("Agent-1", "Agent-2")
        assert result is True
        assert service.get_batch_status("Agent-1", "Agent-2")["exists"] is False

    def test_cancel_batch_no_batch(self):
        """Test cancelling batch that doesn't exist."""
        service = MessageBatchingService()
        result = service.cancel_batch("Agent-1", "Agent-2")
        assert result is False

