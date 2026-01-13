"""
Tests for extractor_storage.py - ConversationStorage class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from src.services.chatgpt.extractor_storage import ConversationStorage


class TestConversationStorage:
    """Test ConversationStorage class."""

    def test_init_defaults(self):
        """Test ConversationStorage initialization with defaults."""
        storage = ConversationStorage()
        assert storage.conversations_dir.name == "conversations"
        assert storage.save_format == "json"
        assert storage.logger is not None

    def test_init_custom(self):
        """Test ConversationStorage initialization with custom values."""
        custom_dir = Path("custom/storage")
        custom_logger = Mock()
        storage = ConversationStorage(
            storage_dir=custom_dir,
            save_format="json",
            logger=custom_logger,
        )
        assert storage.conversations_dir == custom_dir
        assert storage.save_format == "json"
        assert storage.logger == custom_logger

    def test_save_conversation_success(self, tmp_path):
        """Test successful conversation save."""
        storage = ConversationStorage(storage_dir=tmp_path)
        conversation = {
            "conversation_id": "test_conv",
            "messages": [{"role": "user", "text": "Hello"}],
            "extraction_time": time.time(),
        }

        result = storage.save_conversation(conversation)

        assert result is not None
        assert Path(result).exists()
        assert Path(result).name.startswith("test_conv_")

    def test_save_conversation_with_filename(self, tmp_path):
        """Test conversation save with custom filename."""
        storage = ConversationStorage(storage_dir=tmp_path)
        conversation = {"conversation_id": "test_conv", "messages": []}

        result = storage.save_conversation(conversation, "custom_file.json")

        assert result is not None
        assert Path(result).name == "custom_file.json"

    def test_save_conversation_generate_filename(self, tmp_path):
        """Test conversation save with generated filename."""
        storage = ConversationStorage(storage_dir=tmp_path)
        conversation = {
            "conversation_id": "test_conv",
            "extraction_time": 1234567890,
        }

        result = storage.save_conversation(conversation)

        assert result is not None
        assert "test_conv_1234567890.json" in Path(result).name

    def test_save_conversation_exception(self, tmp_path):
        """Test conversation save with exception."""
        storage = ConversationStorage(storage_dir=tmp_path)
        with patch("builtins.open", side_effect=Exception("IO Error")):
            result = storage.save_conversation({"conversation_id": "test"})
            assert result is None

    def test_load_conversation_success(self, tmp_path):
        """Test successful conversation load."""
        storage = ConversationStorage(storage_dir=tmp_path)
        conversation = {
            "conversation_id": "test_conv",
            "messages": [{"role": "user", "text": "Hello"}],
        }

        # Save first
        filename = storage.save_conversation(conversation, "test.json")

        # Load
        loaded = storage.load_conversation("test.json")

        assert loaded is not None
        assert loaded["conversation_id"] == "test_conv"
        assert len(loaded["messages"]) == 1

    def test_load_conversation_not_found(self, tmp_path):
        """Test conversation load when file not found."""
        storage = ConversationStorage(storage_dir=tmp_path)
        result = storage.load_conversation("nonexistent.json")
        assert result is None

    def test_load_conversation_invalid_json(self, tmp_path):
        """Test conversation load with invalid JSON."""
        storage = ConversationStorage(storage_dir=tmp_path)
        filepath = tmp_path / "invalid.json"
        filepath.write_text("invalid json content")

        result = storage.load_conversation("invalid.json")
        assert result is None

    def test_list_conversations_success(self, tmp_path):
        """Test successful conversation listing."""
        storage = ConversationStorage(storage_dir=tmp_path)

        # Save multiple conversations
        for i in range(3):
            conv = {
                "conversation_id": f"conv_{i}",
                "extraction_time": time.time() + i,
                "message_count": i,
            }
            storage.save_conversation(conv, f"conv_{i}.json")

        conversations = storage.list_conversations()

        assert len(conversations) == 3
        assert all("conversation_id" in c for c in conversations)
        assert all("message_count" in c for c in conversations)

    def test_list_conversations_empty(self, tmp_path):
        """Test conversation listing with no files."""
        storage = ConversationStorage(storage_dir=tmp_path)
        conversations = storage.list_conversations()
        assert conversations == []

    def test_list_conversations_sorted(self, tmp_path):
        """Test conversations are sorted by extraction time."""
        storage = ConversationStorage(storage_dir=tmp_path)

        # Save with different extraction times
        for i in range(3):
            conv = {
                "conversation_id": f"conv_{i}",
                "extraction_time": 1000 - i,  # Reverse order
            }
            storage.save_conversation(conv, f"conv_{i}.json")

        conversations = storage.list_conversations()

        # Should be sorted newest first (reverse=True)
        assert conversations[0]["extraction_time"] == 1000
        assert conversations[-1]["extraction_time"] == 998

    def test_cleanup_old_conversations(self, tmp_path, monkeypatch):
        """Test cleanup of old conversation files."""
        storage = ConversationStorage(storage_dir=tmp_path)

        # Create old file
        old_file = tmp_path / "old_conv.json"
        old_file.write_text(json.dumps({"conversation_id": "old"}))

        # Mock time.time() to return current time
        current_time = time.time()
        old_time = current_time - (31 * 24 * 60 * 60)  # 31 days ago

        # Patch the file's mtime directly
        import os
        os.utime(old_file, (old_time, old_time))

        count = storage.cleanup_old_conversations(max_age_days=30)

        assert count == 1
        assert not old_file.exists()

    def test_cleanup_old_conversations_none(self, tmp_path):
        """Test cleanup when no old files exist."""
        storage = ConversationStorage(storage_dir=tmp_path)

        # Create recent file
        recent_file = tmp_path / "recent_conv.json"
        recent_file.write_text(json.dumps({"conversation_id": "recent"}))

        count = storage.cleanup_old_conversations(max_age_days=30)
        assert count == 0

    def test_get_storage_info(self, tmp_path):
        """Test storage info retrieval."""
        storage = ConversationStorage(storage_dir=tmp_path)

        # Save a conversation
        storage.save_conversation({"conversation_id": "test"}, "test.json")

        info = storage.get_storage_info()

        assert info["storage_dir"] == str(tmp_path)
        assert info["save_format"] == "json"
        assert info["conversations_count"] == 1
        assert info["storage_exists"] is True

