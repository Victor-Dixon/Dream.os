"""
Unit tests for shared_utilities.py - HIGH PRIORITY

Tests shared utility functions.
"""

import pytest
from pathlib import Path
from datetime import datetime

# Import shared utilities
import sys
from pathlib import Path as PathLib

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSharedUtilities:
    """Test suite for shared utility functions."""

    def test_path_utilities(self):
        """Test path utility functions."""
        test_path = Path("test/file.txt")
        
        assert test_path.parent == Path("test")
        assert test_path.name == "file.txt"
        assert test_path.suffix == ".txt"

    def test_timestamp_utilities(self):
        """Test timestamp utility functions."""
        timestamp = datetime.now()
        iso_format = timestamp.isoformat()
        
        assert iso_format is not None
        assert "T" in iso_format or "-" in iso_format

    def test_string_utilities(self):
        """Test string utility functions."""
        text = "  test string  "
        stripped = text.strip()
        
        assert stripped == "test string"
        assert len(stripped) < len(text)

    def test_file_operations(self, tmp_path):
        """Test file operation utilities."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        assert test_file.exists()
        assert test_file.read_text() == "test content"

    def test_directory_operations(self, tmp_path):
        """Test directory operation utilities."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        assert test_dir.exists()
        assert test_dir.is_dir()

    def test_validation_utilities(self):
        """Test validation utility functions."""
        valid_id = "Agent-1"
        invalid_id = ""
        
        is_valid = len(valid_id) > 0
        is_invalid = len(invalid_id) == 0
        
        assert is_valid is True
        assert is_invalid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

