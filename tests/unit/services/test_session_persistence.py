"""
Tests for session_persistence.py - SessionPersistence class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from src.services.chatgpt.session_persistence import SessionPersistence


class TestSessionPersistence:
    """Test SessionPersistence class."""

    @pytest.mark.asyncio
    async def test_load_session_data_success(self, tmp_path):
        """Test successful session data loading."""
        cookie_file = tmp_path / "cookies.json"
        cookie_data = {
            "cookies": {"cookie1": "value1"},
            "session_data": {"key": "value"},
        }
        cookie_file.write_text(json.dumps(cookie_data))

        cookie_cache = {}
        session_data = {}
        logger = Mock()

        await SessionPersistence.load_session_data(
            tmp_path, cookie_cache, session_data, logger
        )

        assert cookie_cache == {"cookie1": "value1"}
        assert session_data == {"key": "value"}

    @pytest.mark.asyncio
    async def test_load_session_data_not_found(self, tmp_path):
        """Test session data loading when file not found."""
        cookie_cache = {}
        session_data = {}
        logger = Mock()

        await SessionPersistence.load_session_data(
            tmp_path, cookie_cache, session_data, logger
        )

        assert cookie_cache == {}
        assert session_data == {}

    @pytest.mark.asyncio
    async def test_load_session_data_invalid_json(self, tmp_path):
        """Test session data loading with invalid JSON."""
        cookie_file = tmp_path / "cookies.json"
        cookie_file.write_text("invalid json")

        cookie_cache = {}
        session_data = {}
        logger = Mock()

        await SessionPersistence.load_session_data(
            tmp_path, cookie_cache, session_data, logger
        )

        assert cookie_cache == {}
        assert session_data == {}

    @pytest.mark.asyncio
    async def test_load_session_data_exception(self, tmp_path):
        """Test session data loading with exception."""
        cookie_cache = {}
        session_data = {}
        logger = Mock()

        with patch("builtins.open", side_effect=Exception("IO Error")):
            await SessionPersistence.load_session_data(
                tmp_path, cookie_cache, session_data, logger
            )

        assert cookie_cache == {}
        assert session_data == {}

    @pytest.mark.asyncio
    async def test_save_session_data_success(self, tmp_path):
        """Test successful session data saving."""
        cookie_cache = {"cookie1": "value1"}
        session_data = {"key": "value"}
        logger = Mock()

        await SessionPersistence.save_session_data(
            tmp_path, cookie_cache, session_data, logger
        )

        cookie_file = tmp_path / "cookies.json"
        assert cookie_file.exists()

        with open(cookie_file) as f:
            data = json.load(f)

        assert data["cookies"] == {"cookie1": "value1"}
        assert data["session_data"] == {"key": "value"}
        assert "timestamp" in data
        assert data["version"] == "2.0.0"

    @pytest.mark.asyncio
    async def test_save_session_data_exception(self, tmp_path):
        """Test session data saving with exception."""
        cookie_cache = {"cookie1": "value1"}
        session_data = {"key": "value"}
        logger = Mock()

        with patch("builtins.open", side_effect=Exception("IO Error")):
            await SessionPersistence.save_session_data(
                tmp_path, cookie_cache, session_data, logger
            )

        # Should not raise, just log error

    def test_clear_session_files_success(self, tmp_path):
        """Test successful session file clearing."""
        cookie_file = tmp_path / "cookies.json"
        cookie_file.write_text(json.dumps({"cookies": {}}))

        logger = Mock()

        result = SessionPersistence.clear_session_files(tmp_path, True, logger)

        assert result is True
        assert not cookie_file.exists()

    def test_clear_session_files_not_persistent(self, tmp_path):
        """Test session file clearing when not persistent."""
        cookie_file = tmp_path / "cookies.json"
        cookie_file.write_text(json.dumps({"cookies": {}}))

        logger = Mock()

        result = SessionPersistence.clear_session_files(tmp_path, False, logger)

        assert result is True
        assert cookie_file.exists()  # Should not delete

    def test_clear_session_files_not_exists(self, tmp_path):
        """Test session file clearing when directory doesn't exist."""
        logger = Mock()

        result = SessionPersistence.clear_session_files(
            Path("nonexistent"), True, logger
        )

        assert result is True

    def test_clear_session_files_exception(self, tmp_path):
        """Test session file clearing with exception."""
        logger = Mock()
        cookie_file = tmp_path / "cookies.json"
        cookie_file.write_text(json.dumps({"cookies": {}}))

        with patch("pathlib.Path.unlink", side_effect=Exception("Error")):
            result = SessionPersistence.clear_session_files(tmp_path, True, logger)

        assert result is False

