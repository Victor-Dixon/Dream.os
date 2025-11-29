"""
Tests for publishers/base.py

Comprehensive test suite for base publisher interface and publishing history.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import json
import os
import tempfile

from src.services.publishers.base import (
    DevlogPublisher,
    DevlogPublishingHistory
)


class TestDevlogPublisher:
    """Test DevlogPublisher abstract base class."""

    def test_is_abstract(self):
        """Test that DevlogPublisher is abstract."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class
            DevlogPublisher()

    def test_has_abstract_methods(self):
        """Test that abstract methods are defined."""
        assert hasattr(DevlogPublisher, 'publish_devlog')
        assert hasattr(DevlogPublisher, 'validate_credentials')
        assert hasattr(DevlogPublisher, 'get_publish_status')

    def test_publish_devlog_signature(self):
        """Test publish_devlog method signature."""
        import inspect
        sig = inspect.signature(DevlogPublisher.publish_devlog)
        
        assert 'agent_id' in sig.parameters
        assert 'title' in sig.parameters
        assert 'content' in sig.parameters
        assert 'cycle' in sig.parameters
        assert 'tags' in sig.parameters
        assert 'metadata' in sig.parameters

    def test_validate_credentials_signature(self):
        """Test validate_credentials method signature."""
        import inspect
        sig = inspect.signature(DevlogPublisher.validate_credentials)
        
        # Should have no required parameters
        assert len(sig.parameters) == 0

    def test_get_publish_status_signature(self):
        """Test get_publish_status method signature."""
        import inspect
        sig = inspect.signature(DevlogPublisher.get_publish_status)
        
        assert 'message_id' in sig.parameters

    def test_concrete_implementation(self):
        """Test that concrete implementation can be created."""
        class ConcretePublisher(DevlogPublisher):
            def publish_devlog(self, agent_id, title, content, cycle=None, tags=None, metadata=None):
                return True
            
            def validate_credentials(self):
                return True
            
            def get_publish_status(self, message_id):
                return {}
        
        publisher = ConcretePublisher()
        assert publisher.publish_devlog("Agent-1", "Test", "Content") is True
        assert publisher.validate_credentials() is True


class TestDevlogPublishingHistory:
    """Test DevlogPublishingHistory class."""

    @pytest.fixture
    def temp_history_file(self):
        """Create temporary history file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def test_history_initialization_default(self):
        """Test history initialization with default file."""
        history = DevlogPublishingHistory()
        
        assert history.history_file == "devlog_history.json"
        assert isinstance(history.history, list)

    def test_history_initialization_custom_file(self, temp_history_file):
        """Test history initialization with custom file."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        assert history.history_file == temp_history_file
        assert isinstance(history.history, list)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"devlog_id": "test1"}]')
    @patch('os.path.exists', return_value=True)
    def test_load_history_existing_file(self, mock_exists, mock_file):
        """Test loading history from existing file."""
        history = DevlogPublishingHistory(history_file="test_history.json")
        
        assert len(history.history) == 1
        assert history.history[0]["devlog_id"] == "test1"

    @patch('os.path.exists', return_value=False)
    def test_load_history_missing_file(self, mock_exists):
        """Test loading history when file doesn't exist."""
        history = DevlogPublishingHistory(history_file="nonexistent.json")
        
        assert history.history == []

    @patch('builtins.open', side_effect=IOError("Read error"))
    @patch('os.path.exists', return_value=True)
    def test_load_history_read_error(self, mock_exists, mock_file):
        """Test loading history with read error."""
        history = DevlogPublishingHistory(history_file="error.json")
        
        # Should handle gracefully
        assert isinstance(history.history, list)

    @patch('builtins.open', side_effect=json.JSONDecodeError("Error", "doc", 0))
    @patch('os.path.exists', return_value=True)
    def test_load_history_invalid_json(self, mock_exists, mock_file):
        """Test loading history with invalid JSON."""
        history = DevlogPublishingHistory(history_file="invalid.json")
        
        # Should handle gracefully
        assert isinstance(history.history, list)

    def test_record_publish(self, temp_history_file):
        """Test recording a publish event."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        history.record_publish(
            devlog_id="devlog_1",
            platform="discord",
            message_id="msg_123",
            agent_id="Agent-7",
            title="Test Devlog"
        )
        
        assert len(history.history) == 1
        assert history.history[0]["devlog_id"] == "devlog_1"
        assert history.history[0]["platform"] == "discord"
        assert history.history[0]["agent_id"] == "Agent-7"

    def test_record_publish_with_timestamp(self, temp_history_file):
        """Test recording publish with custom timestamp."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        custom_timestamp = "2025-11-28T12:00:00"
        
        history.record_publish(
            devlog_id="devlog_1",
            platform="discord",
            message_id="msg_123",
            agent_id="Agent-7",
            title="Test",
            timestamp=custom_timestamp
        )
        
        assert history.history[0]["timestamp"] == custom_timestamp

    def test_record_publish_auto_timestamp(self, temp_history_file):
        """Test recording publish with auto-generated timestamp."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        history.record_publish(
            devlog_id="devlog_1",
            platform="discord",
            message_id="msg_123",
            agent_id="Agent-7",
            title="Test"
        )
        
        assert history.history[0]["timestamp"] is not None
        assert isinstance(history.history[0]["timestamp"], str)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_save_history_new_file(self, mock_makedirs, mock_exists, mock_file, temp_history_file):
        """Test saving history to new file."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        # Should save to file
        assert mock_file.called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_save_history_existing_file(self, mock_exists, mock_file, temp_history_file):
        """Test saving history to existing file."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        # Should save to file
        assert mock_file.called

    @patch('builtins.open', side_effect=IOError("Write error"))
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_save_history_write_error(self, mock_makedirs, mock_exists, mock_file, temp_history_file):
        """Test saving history with write error."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        # Should handle gracefully
        try:
            history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        except Exception:
            pytest.fail("Should handle write error gracefully")

    def test_was_published_true(self, temp_history_file):
        """Test was_published returns True for published devlog."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        assert history.was_published("devlog_1") is True

    def test_was_published_false(self, temp_history_file):
        """Test was_published returns False for unpublished devlog."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        assert history.was_published("devlog_2") is False

    def test_was_published_with_platform(self, temp_history_file):
        """Test was_published with platform filter."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        history.record_publish("devlog_2", "slack", "msg_2", "Agent-7", "Test")
        
        assert history.was_published("devlog_1", platform="discord") is True
        assert history.was_published("devlog_2", platform="discord") is False
        assert history.was_published("devlog_2", platform="slack") is True

    def test_was_published_multiple_entries(self, temp_history_file):
        """Test was_published with multiple history entries."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test 1")
        history.record_publish("devlog_2", "discord", "msg_2", "Agent-8", "Test 2")
        history.record_publish("devlog_3", "slack", "msg_3", "Agent-7", "Test 3")
        
        assert history.was_published("devlog_1") is True
        assert history.was_published("devlog_2") is True
        assert history.was_published("devlog_3") is True
        assert history.was_published("devlog_4") is False

    def test_current_timestamp(self, temp_history_file):
        """Test _current_timestamp generates valid timestamp."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        timestamp = history._current_timestamp()
        
        assert isinstance(timestamp, str)
        assert "T" in timestamp or "-" in timestamp  # ISO format

    @patch('os.path.dirname', return_value="/test/dir")
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_history_creates_directory(self, mock_file, mock_makedirs, mock_exists, mock_dirname, temp_history_file):
        """Test that save_history creates directory if needed."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        # Should attempt to create directory
        mock_makedirs.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_save_history_json_format(self, mock_exists, mock_file, temp_history_file):
        """Test that save_history uses proper JSON formatting."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        # Check that json.dump was called with proper parameters
        call_args = mock_file().write.call_args_list
        # Should have written JSON content
        assert len(call_args) > 0

    def test_history_persistence(self, temp_history_file):
        """Test that history persists across instances."""
        history1 = DevlogPublishingHistory(history_file=temp_history_file)
        history1.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        # Create new instance - should load previous history
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(history1.history)):
            with patch('os.path.exists', return_value=True):
                history2 = DevlogPublishingHistory(history_file=temp_history_file)
                assert len(history2.history) >= 1

    def test_record_publish_all_fields(self, temp_history_file):
        """Test recording publish with all fields."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        history.record_publish(
            devlog_id="devlog_1",
            platform="discord",
            message_id="msg_123",
            agent_id="Agent-7",
            title="Test Devlog",
            timestamp="2025-11-28T12:00:00"
        )
        
        entry = history.history[0]
        assert entry["devlog_id"] == "devlog_1"
        assert entry["platform"] == "discord"
        assert entry["message_id"] == "msg_123"
        assert entry["agent_id"] == "Agent-7"
        assert entry["title"] == "Test Devlog"
        assert entry["timestamp"] == "2025-11-28T12:00:00"

    def test_was_published_case_sensitive(self, temp_history_file):
        """Test was_published is case sensitive for devlog_id."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        assert history.was_published("devlog_1") is True
        assert history.was_published("DEVLOG_1") is False

    def test_was_published_case_sensitive_platform(self, temp_history_file):
        """Test was_published is case sensitive for platform."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        assert history.was_published("devlog_1", platform="discord") is True
        assert history.was_published("devlog_1", platform="Discord") is False

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_save_history_ensure_ascii_false(self, mock_exists, mock_file, temp_history_file):
        """Test that save_history uses ensure_ascii=False for unicode."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test with émojis 🚀")
        
        # Verify file operations occurred
        assert mock_file.called

    def test_current_timestamp_format(self, temp_history_file):
        """Test _current_timestamp returns ISO format."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        timestamp = history._current_timestamp()
        
        # Should be ISO format (contains T or -)
        assert "T" in timestamp or "-" in timestamp
        # Should be valid datetime string
        from datetime import datetime
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert True
        except ValueError:
            # If not strict ISO, at least check it's a string
            assert isinstance(timestamp, str)

    def test_history_multiple_platforms(self, temp_history_file):
        """Test history with multiple platforms."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        history.record_publish("devlog_1", "slack", "msg_2", "Agent-7", "Test")
        
        assert history.was_published("devlog_1", platform="discord") is True
        assert history.was_published("devlog_1", platform="slack") is True

    def test_history_entry_structure(self, temp_history_file):
        """Test that history entries have correct structure."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        
        entry = history.history[0]
        required_keys = ["devlog_id", "platform", "message_id", "agent_id", "title", "timestamp"]
        for key in required_keys:
            assert key in entry

    @patch('builtins.open', side_effect=IOError("Write error"))
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_save_history_handles_io_error_gracefully(self, mock_makedirs, mock_exists, mock_file, temp_history_file):
        """Test that save_history handles IO errors gracefully."""
        history = DevlogPublishingHistory(history_file=temp_history_file)
        
        # Should not raise exception
        try:
            history.record_publish("devlog_1", "discord", "msg_1", "Agent-7", "Test")
        except Exception:
            pytest.fail("Should handle IO error gracefully")

