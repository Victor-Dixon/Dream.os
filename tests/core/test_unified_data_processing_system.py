"""
Tests for Unified Data Processing System
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from src.core.unified_data_processing_system import (
    read_json,
    write_json,
    ensure_directory,
    resolve_path,
    write_file
)


class TestReadJson:
    """Test suite for read_json function."""

    def test_read_json_success(self, tmp_path):
        """Test reading valid JSON file."""
        json_file = tmp_path / "test.json"
        data = {"key": "value", "number": 42}
        json_file.write_text(json.dumps(data))
        
        result = read_json(str(json_file))
        assert result == data

    def test_read_json_file_not_exists(self, tmp_path):
        """Test reading non-existent file returns empty dict."""
        json_file = tmp_path / "nonexistent.json"
        result = read_json(str(json_file))
        assert result == {}

    def test_read_json_invalid_json(self, tmp_path):
        """Test reading invalid JSON returns empty dict."""
        json_file = tmp_path / "invalid.json"
        json_file.write_text("not valid json {")
        
        result = read_json(str(json_file))
        assert result == {}

    def test_read_json_handles_exception(self, tmp_path):
        """Test read_json handles exceptions gracefully."""
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = read_json("test.json")
            assert result == {}


class TestWriteJson:
    """Test suite for write_json function."""

    def test_write_json_success(self, tmp_path):
        """Test writing JSON file successfully."""
        json_file = tmp_path / "output.json"
        data = {"key": "value", "number": 42}
        
        result = write_json(str(json_file), data)
        assert result is True
        assert json_file.exists()
        
        loaded = json.loads(json_file.read_text())
        assert loaded == data

    def test_write_json_creates_directory(self, tmp_path):
        """Test write_json creates parent directory."""
        json_file = tmp_path / "subdir" / "output.json"
        data = {"test": "data"}
        
        result = write_json(str(json_file), data)
        assert result is True
        assert json_file.exists()

    def test_write_json_handles_exception(self):
        """Test write_json handles exceptions gracefully."""
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Access denied")):
            result = write_json("test.json", {"key": "value"})
            assert result is False


class TestEnsureDirectory:
    """Test suite for ensure_directory function."""

    def test_ensure_directory_creates_new(self, tmp_path):
        """Test ensure_directory creates new directory."""
        new_dir = tmp_path / "new_directory"
        result = ensure_directory(str(new_dir))
        
        assert result is True
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_ensure_directory_exists(self, tmp_path):
        """Test ensure_directory handles existing directory."""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()
        
        result = ensure_directory(str(existing_dir))
        assert result is True

    def test_ensure_directory_creates_parents(self, tmp_path):
        """Test ensure_directory creates parent directories."""
        nested_dir = tmp_path / "level1" / "level2" / "level3"
        result = ensure_directory(str(nested_dir))
        
        assert result is True
        assert nested_dir.exists()

    def test_ensure_directory_handles_exception(self):
        """Test ensure_directory handles exceptions gracefully."""
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Access denied")):
            result = ensure_directory("test_dir")
            assert result is False


class TestResolvePath:
    """Test suite for resolve_path function."""

    def test_resolve_path_absolute(self, tmp_path):
        """Test resolve_path returns absolute path."""
        test_path = tmp_path / "test.txt"
        result = resolve_path(str(test_path))
        
        assert isinstance(result, Path)
        assert result.is_absolute()

    def test_resolve_path_relative(self, tmp_path):
        """Test resolve_path resolves relative path."""
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            result = resolve_path("relative.txt")
            assert isinstance(result, Path)
            assert result.is_absolute()


class TestWriteFile:
    """Test suite for write_file function."""

    def test_write_file_success(self, tmp_path):
        """Test writing file successfully."""
        test_file = tmp_path / "output.txt"
        content = "Test content\nLine 2"
        
        result = write_file(str(test_file), content)
        assert result is True
        assert test_file.exists()
        assert test_file.read_text() == content

    def test_write_file_creates_directory(self, tmp_path):
        """Test write_file creates parent directory."""
        test_file = tmp_path / "subdir" / "output.txt"
        content = "Test"
        
        result = write_file(str(test_file), content)
        assert result is True
        assert test_file.exists()

    def test_write_file_handles_exception(self):
        """Test write_file handles exceptions gracefully."""
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = write_file("test.txt", "content")
            assert result is False


