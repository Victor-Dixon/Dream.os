#!/usr/bin/env python3
"""
Tests for Message Repository
=============================

Tests for message data access layer.

Author: Agent-7
Date: 2025-11-27
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

from src.repositories.message_repository import MessageRepository


class TestMessageRepository:
    """Test suite for MessageRepository."""

    @pytest.fixture
    def temp_file(self):
        """Create temporary messages file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = Path(f.name)
            yield temp_path
            if temp_path.exists():
                temp_path.unlink()

    @pytest.fixture
    def repository(self, temp_file):
        """Create MessageRepository instance."""
        return MessageRepository(str(temp_file))

    def test_initialization(self, repository, temp_file):
        """Test repository initialization."""
        assert repository.messages_file == temp_file
        assert repository.messages_file.exists()

    def test_save_message(self, repository):
        """Test saving a message."""
        message_data = {
            "message_id": "msg-1",
            "sender": "Agent-1",
            "recipient": "Agent-7",
            "content": "Test message"
        }
        
        result = repository.save_message(message_data)
        assert result is True

    def test_get_message(self, repository):
        """Test getting a message."""
        message_data = {
            "message_id": "msg-1",
            "sender": "Agent-1",
            "content": "Test message"
        }
        repository.save_message(message_data)
        
        message = repository.get_message("msg-1")
        assert message is not None
        assert message["message_id"] == "msg-1"

    def test_get_messages_by_recipient(self, repository):
        """Test getting messages by recipient."""
        messages = [
            {"message_id": "msg-1", "recipient": "Agent-7", "content": "Test 1"},
            {"message_id": "msg-2", "recipient": "Agent-7", "content": "Test 2"},
            {"message_id": "msg-3", "recipient": "Agent-8", "content": "Test 3"}
        ]
        
        for msg in messages:
            repository.save_message(msg)
        
        agent7_messages = repository.get_messages_by_recipient("Agent-7")
        assert len(agent7_messages) == 2

    def test_get_all_messages(self, repository):
        """Test getting all messages."""
        messages = [
            {"message_id": "msg-1", "content": "Test 1"},
            {"message_id": "msg-2", "content": "Test 2"}
        ]
        
        for msg in messages:
            repository.save_message(msg)
        
        all_messages = repository.get_all_messages()
        assert len(all_messages) >= 2

