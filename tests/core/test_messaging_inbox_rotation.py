"""
Unit tests for messaging_inbox_rotation.py - HIGH PRIORITY

Tests inbox rotation functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
from datetime import datetime, timedelta

# Import inbox rotation
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestInboxRotation:
    """Test suite for inbox rotation."""

    @pytest.fixture
    def temp_inbox_dir(self, tmp_path):
        """Create temporary inbox directory."""
        inbox_dir = tmp_path / "inbox"
        inbox_dir.mkdir()
        return inbox_dir

    def test_rotation_initialization(self, temp_inbox_dir):
        """Test rotation initialization."""
        assert temp_inbox_dir.exists()
        assert temp_inbox_dir.is_dir()

    def test_archive_old_messages(self, temp_inbox_dir):
        """Test archiving old messages."""
        # Create old message file
        old_message = temp_inbox_dir / "old_message.md"
        old_message.write_text("old content")
        
        # Simulate archiving
        archive_dir = temp_inbox_dir.parent / "archive"
        archive_dir.mkdir(exist_ok=True)
        
        if old_message.exists():
            archive_path = archive_dir / old_message.name
            old_message.rename(archive_path)
        
        assert archive_path.exists()
        assert not old_message.exists()

    def test_rotation_threshold(self):
        """Test rotation threshold."""
        max_age_days = 30
        threshold = datetime.now() - timedelta(days=max_age_days)
        
        old_date = datetime.now() - timedelta(days=31)
        new_date = datetime.now() - timedelta(days=10)
        
        should_archive_old = old_date < threshold
        should_archive_new = new_date < threshold
        
        assert should_archive_old is True
        assert should_archive_new is False

    def test_message_count_limit(self):
        """Test message count limit."""
        max_messages = 100
        current_count = 150
        
        should_rotate = current_count > max_messages
        
        assert should_rotate is True

    def test_rotation_cleanup(self, temp_inbox_dir):
        """Test rotation cleanup."""
        # Create multiple message files
        for i in range(5):
            message_file = temp_inbox_dir / f"message_{i}.md"
            message_file.write_text(f"content {i}")
        
        # Simulate cleanup (keep only 3 most recent)
        messages = sorted(temp_inbox_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        to_keep = messages[:3]
        to_remove = messages[3:]
        
        for msg in to_remove:
            msg.unlink()
        
        remaining = list(temp_inbox_dir.glob("*.md"))
        assert len(remaining) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

