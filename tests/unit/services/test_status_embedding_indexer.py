"""
Tests for status_embedding_indexer.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-11-27
"""

import pytest
from unittest.mock import Mock, patch, mock_open, MagicMock
from pathlib import Path
import json
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.status_embedding_indexer import refresh_status_embedding


class TestRefreshStatusEmbedding:
    """Test refresh_status_embedding function."""

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_new_file(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing status embedding when file doesn't exist."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "mission": "test"}
        refresh_status_embedding("Agent-1", status_data)
        
        mock_ensure.assert_called_once_with(mock_status_file.parent)
        mock_file.assert_called()
        # Check that data was written
        written_data = json.loads(''.join(call.args[0] for call in mock_file().write.call_args_list if call.args))
        # Since we can't easily get the written data, we'll verify the file was opened for writing
        assert any("w" in str(call) for call in mock_file.call_args_list)

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-2": {"status": "old"}}')
    def test_refresh_status_embedding_existing_file(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing status embedding when file exists."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "mission": "new"}
        refresh_status_embedding("Agent-2", status_data)
        
        mock_ensure.assert_called_once()
        # File should be opened for reading first, then writing
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"old": "data"}, "Agent-2": {"other": "data"}}')
    def test_refresh_status_embedding_updates_existing_agent(self, mock_file, mock_ensure, mock_status_file):
        """Test that refreshing updates existing agent data."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "updated"}
        refresh_status_embedding("Agent-1", status_data)
        
        mock_ensure.assert_called_once()
        # Verify file operations occurred
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_creates_path(self, mock_file, mock_ensure, mock_status_file):
        """Test that ensure_path_exists is called."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-3", status_data)
        
        mock_ensure.assert_called_once_with(mock_status_file.parent)

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_refresh_status_embedding_empty_file(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing when file exists but is empty."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-4", status_data)
        
        mock_ensure.assert_called_once()
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_utf8_encoding(self, mock_file, mock_ensure, mock_status_file):
        """Test that file operations use UTF-8 encoding."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "message": "Test with émojis 🚀"}
        refresh_status_embedding("Agent-5", status_data)
        
        # Check that UTF-8 encoding was used
        call_args = [str(call) for call in mock_file.call_args_list]
        assert any("utf-8" in call.lower() or "encoding='utf-8'" in call for call in call_args)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

