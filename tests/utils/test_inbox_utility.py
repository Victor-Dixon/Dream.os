"""
Unit tests for inbox_utility.py - HIGH PRIORITY

Tests inbox message creation functionality.
Target: ≥85% coverage, 5+ tests per file
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import tempfile
import shutil

# Import inbox utility
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.inbox_utility import create_inbox_message, _format_inbox_message


class TestCreateInboxMessage:
    """Test suite for create_inbox_message function."""

    @pytest.fixture
    def temp_inbox_dir(self, tmp_path):
        """Create temporary inbox directory."""
        inbox_dir = tmp_path / "agent_workspaces" / "Agent-1" / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        return inbox_dir

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_success(self, mock_path_class, mock_timestamp, mock_filename, temp_inbox_dir):
        """Test successful inbox message creation."""
        mock_filename.return_value = "20251128_120000"
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        # Create a real Path mock that works
        def path_side_effect(*args):
            if len(args) == 1 and isinstance(args[0], str):
                if "inbox" in args[0]:
                    mock_path = MagicMock()
                    mock_path.mkdir = Mock()
                    mock_path.write_text = Mock()
                    return mock_path
            return Path(*args)
        
        mock_path_class.side_effect = path_side_effect
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="urgent"
        )
        
        # Should return True on success
        assert result is True

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_with_tags(self, mock_path_class, mock_timestamp, mock_filename, temp_inbox_dir):
        """Test inbox message creation with tags."""
        mock_filename.return_value = "20251128_120000"
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        mock_path = MagicMock()
        mock_path.mkdir = Mock()
        mock_path.write_text = Mock()
        mock_path_class.return_value = mock_path
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            tags=["urgent", "coordination"]
        )
        
        assert result is True

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_custom_type(self, mock_path_class, mock_timestamp, mock_filename, temp_inbox_dir):
        """Test inbox message creation with custom message type."""
        mock_filename.return_value = "20251128_120000"
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        mock_path = MagicMock()
        mock_path.mkdir = Mock()
        mock_path.write_text = Mock()
        mock_path_class.return_value = mock_path
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="broadcast"
        )
        
        assert result is True

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_file_error(self, mock_path_class, mock_filename, temp_inbox_dir):
        """Test inbox message creation with file write error."""
        mock_filename.return_value = "20251128_120000"
        
        mock_path = MagicMock()
        mock_path.mkdir = Mock()
        mock_path.write_text = Mock(side_effect=IOError("Permission denied"))
        mock_path_class.return_value = mock_path
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message"
        )
        
        # Should return False on error
        assert result is False

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_directory_creation(self, mock_path_class, mock_filename, temp_inbox_dir):
        """Test that inbox directory is created if it doesn't exist."""
        mock_filename.return_value = "20251128_120000"
        
        mock_path = MagicMock()
        mock_mkdir = Mock()
        mock_path.mkdir = mock_mkdir
        mock_path.write_text = Mock()
        mock_path_class.return_value = mock_path
        
        create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message"
        )
        
        # Verify mkdir was called
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


class TestFormatInboxMessage:
    """Test suite for _format_inbox_message function."""

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_basic(self, mock_timestamp):
        """Test basic message formatting."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="urgent",
            message_type="text",
            tags=[]
        )
        
        assert "INBOX MESSAGE - TEXT" in result
        assert "From**: Agent-4" in result
        assert "To**: Agent-1" in result
        assert "Priority**: urgent" in result
        assert "Test message" in result
        assert "2025-11-28 12:00:00" in result

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_with_tags(self, mock_timestamp):
        """Test message formatting with tags."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="broadcast",
            tags=["urgent", "coordination"]
        )
        
        assert "INBOX MESSAGE - BROADCAST" in result
        assert "Tags**: urgent, coordination" in result

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_no_tags(self, mock_timestamp):
        """Test message formatting without tags."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="text",
            tags=[]
        )
        
        assert "Tags**: none" in result

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_swarm_tagline(self, mock_timestamp):
        """Test that message includes swarm tagline."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="text",
            tags=[]
        )
        
        assert "WE. ARE. SWARM" in result
        assert "⚡🔥" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



Tests inbox message creation functionality.
Target: ≥85% coverage, 5+ tests per file
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import tempfile
import shutil

# Import inbox utility
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.inbox_utility import create_inbox_message, _format_inbox_message


class TestCreateInboxMessage:
    """Test suite for create_inbox_message function."""

    @pytest.fixture
    def temp_inbox_dir(self, tmp_path):
        """Create temporary inbox directory."""
        inbox_dir = tmp_path / "agent_workspaces" / "Agent-1" / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        return inbox_dir

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_success(self, mock_path_class, mock_timestamp, mock_filename, temp_inbox_dir):
        """Test successful inbox message creation."""
        mock_filename.return_value = "20251128_120000"
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        # Create a real Path mock that works
        def path_side_effect(*args):
            if len(args) == 1 and isinstance(args[0], str):
                if "inbox" in args[0]:
                    mock_path = MagicMock()
                    mock_path.mkdir = Mock()
                    mock_path.write_text = Mock()
                    return mock_path
            return Path(*args)
        
        mock_path_class.side_effect = path_side_effect
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="urgent"
        )
        
        # Should return True on success
        assert result is True

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_with_tags(self, mock_path_class, mock_timestamp, mock_filename, temp_inbox_dir):
        """Test inbox message creation with tags."""
        mock_filename.return_value = "20251128_120000"
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        mock_path = MagicMock()
        mock_path.mkdir = Mock()
        mock_path.write_text = Mock()
        mock_path_class.return_value = mock_path
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            tags=["urgent", "coordination"]
        )
        
        assert result is True

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_custom_type(self, mock_path_class, mock_timestamp, mock_filename, temp_inbox_dir):
        """Test inbox message creation with custom message type."""
        mock_filename.return_value = "20251128_120000"
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        mock_path = MagicMock()
        mock_path.mkdir = Mock()
        mock_path.write_text = Mock()
        mock_path_class.return_value = mock_path
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="broadcast"
        )
        
        assert result is True

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_file_error(self, mock_path_class, mock_filename, temp_inbox_dir):
        """Test inbox message creation with file write error."""
        mock_filename.return_value = "20251128_120000"
        
        mock_path = MagicMock()
        mock_path.mkdir = Mock()
        mock_path.write_text = Mock(side_effect=IOError("Permission denied"))
        mock_path_class.return_value = mock_path
        
        result = create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message"
        )
        
        # Should return False on error
        assert result is False

    @patch('src.utils.inbox_utility.format_swarm_timestamp_filename')
    @patch('src.utils.inbox_utility.Path')
    def test_create_inbox_message_directory_creation(self, mock_path_class, mock_filename, temp_inbox_dir):
        """Test that inbox directory is created if it doesn't exist."""
        mock_filename.return_value = "20251128_120000"
        
        mock_path = MagicMock()
        mock_mkdir = Mock()
        mock_path.mkdir = mock_mkdir
        mock_path.write_text = Mock()
        mock_path_class.return_value = mock_path
        
        create_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message"
        )
        
        # Verify mkdir was called
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


class TestFormatInboxMessage:
    """Test suite for _format_inbox_message function."""

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_basic(self, mock_timestamp):
        """Test basic message formatting."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="urgent",
            message_type="text",
            tags=[]
        )
        
        assert "INBOX MESSAGE - TEXT" in result
        assert "From**: Agent-4" in result
        assert "To**: Agent-1" in result
        assert "Priority**: urgent" in result
        assert "Test message" in result
        assert "2025-11-28 12:00:00" in result

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_with_tags(self, mock_timestamp):
        """Test message formatting with tags."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="broadcast",
            tags=["urgent", "coordination"]
        )
        
        assert "INBOX MESSAGE - BROADCAST" in result
        assert "Tags**: urgent, coordination" in result

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_no_tags(self, mock_timestamp):
        """Test message formatting without tags."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="text",
            tags=[]
        )
        
        assert "Tags**: none" in result

    @patch('src.utils.inbox_utility.format_swarm_timestamp')
    def test_format_inbox_message_swarm_tagline(self, mock_timestamp):
        """Test that message includes swarm tagline."""
        mock_timestamp.return_value = "2025-11-28 12:00:00"
        
        result = _format_inbox_message(
            recipient="Agent-1",
            sender="Agent-4",
            content="Test message",
            priority="normal",
            message_type="text",
            tags=[]
        )
        
        assert "WE. ARE. SWARM" in result
        assert "⚡🔥" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

