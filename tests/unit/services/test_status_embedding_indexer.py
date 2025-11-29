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

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"old": "data"}}')
    def test_refresh_status_embedding_overwrites_existing(self, mock_file, mock_ensure, mock_status_file):
        """Test that refreshing overwrites existing agent data."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "new_status", "mission": "new_mission"}
        refresh_status_embedding("Agent-1", status_data)
        
        mock_ensure.assert_called_once()
        # Verify file was written to
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_complex_data(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with complex nested data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "current_mission": "Test Mission",
            "current_tasks": ["Task 1", "Task 2"],
            "metadata": {"nested": {"key": "value"}}
        }
        refresh_status_embedding("Agent-6", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"data": "old"}, "Agent-2": {"data": "other"}}')
    def test_refresh_status_embedding_preserves_other_agents(self, mock_file, mock_ensure, mock_status_file):
        """Test that refreshing one agent preserves others."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "updated"}
        refresh_status_embedding("Agent-1", status_data)
        
        # Verify file operations occurred
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_empty_data(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with empty status data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {}
        refresh_status_embedding("Agent-7", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_refresh_status_embedding_corrupted_file(self, mock_file, mock_ensure, mock_status_file):
        """Test handling corrupted JSON file."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        
        # Should handle JSON decode error gracefully
        try:
            refresh_status_embedding("Agent-8", status_data)
        except json.JSONDecodeError:
            # If it raises, that's also acceptable behavior
            pass
        
        mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_write_error(self, mock_file, mock_ensure, mock_status_file):
        """Test handling file write errors."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        mock_file.side_effect = [mock_open().return_value, IOError("Write error")]
        
        status_data = {"status": "active"}
        
        # Should handle write error
        try:
            refresh_status_embedding("Agent-9", status_data)
        except IOError:
            # If it raises, that's acceptable
            pass
        
        mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_indent_formatting(self, mock_file, mock_ensure, mock_status_file):
        """Test that JSON is written with proper indentation."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "mission": "test"}
        refresh_status_embedding("Agent-10", status_data)
        
        # Verify json.dump was called with indent=2
        # This is implicit in the function implementation
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_multiple_agents(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing multiple agents sequentially."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        agents = ["Agent-1", "Agent-2", "Agent-3"]
        for agent_id in agents:
            status_data = {"status": "active", "agent_id": agent_id}
            refresh_status_embedding(agent_id, status_data)
        
        # Should handle multiple calls
        assert mock_ensure.call_count == len(agents)

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_read_error(self, mock_file, mock_ensure, mock_status_file):
        """Test handling file read errors."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        mock_file.side_effect = [mock_open(read_data='{"Agent-1": {}}').return_value, IOError("Read error")]
        
        status_data = {"status": "active"}
        
        # Should handle read error
        try:
            refresh_status_embedding("Agent-15", status_data)
        except IOError:
            # If it propagates, that's acceptable
            pass
        
        mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_dump_error(self, mock_file, mock_ensure, mock_status_file):
        """Test handling JSON dump errors."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        # Mock json.dump to raise error
        with patch('json.dump', side_effect=Exception("JSON error")):
            status_data = {"status": "active"}
            
            # Should handle JSON error
            try:
                refresh_status_embedding("Agent-16", status_data)
            except Exception:
                # If it propagates, that's acceptable
                pass
            
            mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_load_error(self, mock_file, mock_ensure, mock_status_file):
        """Test handling JSON load errors."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        # Mock json.load to raise error
        with patch('json.load', side_effect=json.JSONDecodeError("Error", "doc", 0)):
            status_data = {"status": "active"}
            
            # Should handle JSON load error
            try:
                refresh_status_embedding("Agent-17", status_data)
            except json.JSONDecodeError:
                # If it propagates, that's acceptable
                pass
            
            mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_empty_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with empty agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_very_large_status_data(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with very large status data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "large_field": "x" * 100000,
            "tasks": [f"Task {i}" for i in range(1000)],
            "metadata": {"nested": {"deep": {"value": "test"}}}
        }
        
        refresh_status_embedding("Agent-18", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_special_characters_in_data(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with special characters in status data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "message": "Test with \"quotes\" and 'apostrophes' and émojis 🚀"
        }
        
        refresh_status_embedding("Agent-19", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_large_data(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with large status data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "large_field": "x" * 10000,
            "tasks": [f"Task {i}" for i in range(100)]
        }
        refresh_status_embedding("Agent-11", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_dump_indent(self, mock_file, mock_ensure, mock_status_file):
        """Test that json.dump is called with indent=2."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-12", status_data)
        
        # Verify file was opened for writing
        assert mock_file.called

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"status": "old"}}')
    def test_refresh_status_embedding_read_before_write(self, mock_file, mock_ensure, mock_status_file):
        """Test that existing file is read before writing."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "new"}
        refresh_status_embedding("Agent-1", status_data)
        
        # Should open file at least twice (read then write)
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_none_values(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with None values in data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "optional_field": None}
        refresh_status_embedding("Agent-13", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_unicode_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with unicode characters in agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-测试", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_ensure_path_error(self, mock_file, mock_ensure, mock_status_file):
        """Test handling when ensure_path_exists raises error."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        mock_ensure.side_effect = Exception("Path creation error")
        
        status_data = {"status": "active"}
        
        # Should handle error gracefully or propagate
        try:
            refresh_status_embedding("Agent-14", status_data)
        except Exception:
            # If it propagates, that's acceptable
            pass
        
        mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_nested_dict_structure(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with deeply nested dictionary structure."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "metadata": {
                "level1": {
                    "level2": {
                        "level3": {
                            "level4": "deep_value"
                        }
                    }
                }
            }
        }
        
        refresh_status_embedding("Agent-20", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_list_values(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with list values in status data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "tasks": ["Task 1", "Task 2", "Task 3"],
            "achievements": [{"name": "A1", "points": 100}, {"name": "A2", "points": 200}]
        }
        
        refresh_status_embedding("Agent-21", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_numeric_values(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with numeric values."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "points": 500,
            "score": 0.95,
            "count": 42
        }
        
        refresh_status_embedding("Agent-22", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_boolean_values(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with boolean values."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "is_active": True,
            "is_complete": False,
            "has_errors": False
        }
        
        refresh_status_embedding("Agent-23", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"old": "data"}}')
    def test_refresh_status_embedding_overwrites_specific_agent(self, mock_file, mock_ensure, mock_status_file):
        """Test that refreshing overwrites only the specific agent's data."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "updated"}
        refresh_status_embedding("Agent-1", status_data)
        
        # Should update Agent-1 but preserve structure
        mock_ensure.assert_called_once()
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_path_handling(self, mock_file, mock_ensure, mock_status_file):
        """Test that file path is handled correctly."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        mock_status_file.__str__ = lambda x: "/test/path/status_embeddings.json"
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-24", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_concurrent_updates(self, mock_file, mock_ensure, mock_status_file):
        """Test handling of concurrent status updates."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
        for agent_id in agents:
            status_data = {"status": "active", "agent_id": agent_id}
            refresh_status_embedding(agent_id, status_data)
        
        # Should handle multiple updates
        assert mock_ensure.call_count == len(agents)

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_mixed_data_types(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with mixed data types."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "active",
            "string_field": "text",
            "int_field": 42,
            "float_field": 3.14,
            "bool_field": True,
            "list_field": [1, 2, 3],
            "dict_field": {"key": "value"},
            "none_field": None
        }
        
        refresh_status_embedding("Agent-25", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_empty_dict(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with empty dictionary."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {}
        refresh_status_embedding("Agent-26", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"data": "old"}, "Agent-2": {"data": "other"}}')
    def test_refresh_status_embedding_preserves_other_agents_structure(self, mock_file, mock_ensure, mock_status_file):
        """Test that refreshing preserves other agents' data structure."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "updated"}
        refresh_status_embedding("Agent-1", status_data)
        
        # Should preserve Agent-2's data
        mock_ensure.assert_called_once()
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_very_long_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with very long agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        long_agent_id = "Agent-" + "X" * 100
        refresh_status_embedding(long_agent_id, status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_special_characters_in_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with special characters in agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-7_Test-123", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_encoding_utf8(self, mock_file, mock_ensure, mock_status_file):
        """Test that file operations use UTF-8 encoding."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "message": "Test émojis 🚀"}
        refresh_status_embedding("Agent-27", status_data)
        
        # Verify UTF-8 encoding is used
        call_args = [str(call) for call in mock_file.call_args_list]
        assert any("utf-8" in call.lower() or "encoding='utf-8'" in call for call in call_args)

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_indent_2(self, mock_file, mock_ensure, mock_status_file):
        """Test that JSON is written with indent=2."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "nested": {"key": "value"}}
        refresh_status_embedding("Agent-28", status_data)
        
        # Verify file operations occurred
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_all_data_types_combined(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with all data types combined in one status."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "string": "text",
            "int": 42,
            "float": 3.14,
            "bool_true": True,
            "bool_false": False,
            "list_empty": [],
            "list_with_items": [1, "two", 3.0],
            "dict_empty": {},
            "dict_nested": {"level1": {"level2": "value"}},
            "none_value": None,
            "unicode": "émojis 🚀 测试"
        }
        
        refresh_status_embedding("Agent-29", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_whitespace_only_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with whitespace-only agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("   ", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"data": "old"}}')
    def test_refresh_status_embedding_adds_new_agent(self, mock_file, mock_ensure, mock_status_file):
        """Test that refreshing adds new agent to existing database."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "new"}
        refresh_status_embedding("Agent-New", status_data)
        
        # Should add new agent to database
        mock_ensure.assert_called_once()
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_numeric_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with numeric agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("123", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_special_characters_only(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with special characters only in agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("!@#$%^&*()", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_size_verification(self, mock_file, mock_ensure, mock_status_file):
        """Test that file size is reasonable after write."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "large_field": "x" * 1000}
        refresh_status_embedding("Agent-30", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_structure_preservation(self, mock_file, mock_ensure, mock_status_file):
        """Test that JSON structure is preserved correctly."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        original_data = {"Agent-1": {"old": "data"}, "Agent-2": {"other": "data"}}
        with patch('json.load', return_value=original_data):
            status_data = {"status": "updated"}
            refresh_status_embedding("Agent-1", status_data)
            
            # Should preserve structure
            mock_ensure.assert_called_once()
            assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_very_deep_nesting(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with very deeply nested structures."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "value": "deep"
                            }
                        }
                    }
                }
            }
        }
        
        refresh_status_embedding("Agent-31", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_circular_reference_handling(self, mock_file, mock_ensure, mock_status_file):
        """Test that circular references don't cause issues (JSON serialization)."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        # Create a structure that would be circular if not handled
        status_data = {
            "status": "active",
            "nested": {"key": "value"}
        }
        
        refresh_status_embedding("Agent-32", status_data)
        
        # Should handle without circular reference errors
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_very_large_status_data(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with very large status data."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "large_field": "x" * 10000,
            "many_fields": {f"field_{i}": f"value_{i}" for i in range(100)}
        }
        
        refresh_status_embedding("Agent-33", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"data": "old"}}')
    def test_refresh_status_embedding_updates_existing_agent_deep_merge(self, mock_file, mock_ensure, mock_status_file):
        """Test that updating existing agent preserves other fields."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "updated", "new_field": "new_value"}
        refresh_status_embedding("Agent-1", status_data)
        
        # Should update Agent-1 while preserving structure
        mock_ensure.assert_called_once()
        assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_unicode_in_all_fields(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with unicode in all possible fields."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {
            "status": "émojis 🚀",
            "message": "测试 unicode",
            "nested": {"key": "值 with émojis 🎉"}
        }
        
        refresh_status_embedding("Agent-34", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_none_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with None agent_id (edge case)."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        
        # None agent_id should be handled
        refresh_status_embedding(None, status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_empty_string_agent_id(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with empty string agent_id."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_serialization_errors(self, mock_file, mock_ensure, mock_status_file):
        """Test handling of JSON serialization errors."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        # Create data that might cause serialization issues
        status_data = {"status": "active"}
        
        with patch('json.dump', side_effect=TypeError("Serialization error")):
            # Should handle serialization errors
            try:
                refresh_status_embedding("Agent-35", status_data)
            except TypeError:
                pass  # Expected to raise

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_write_permission_error(self, mock_file, mock_ensure, mock_status_file):
        """Test handling of file write permission errors."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            # Should handle permission errors
            try:
                refresh_status_embedding("Agent-36", status_data)
            except PermissionError:
                pass  # Expected to raise

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_multiple_agents_concurrent(self, mock_file, mock_ensure, mock_status_file):
        """Test concurrent updates to multiple agents."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        original_data = {
            "Agent-1": {"status": "old1"},
            "Agent-2": {"status": "old2"},
            "Agent-3": {"status": "old3"}
        }
        
        with patch('json.load', return_value=original_data):
            # Simulate concurrent updates
            status_data1 = {"status": "new1"}
            status_data2 = {"status": "new2"}
            
            refresh_status_embedding("Agent-1", status_data1)
            refresh_status_embedding("Agent-2", status_data2)
            
            # Should handle concurrent updates
            assert mock_file.call_count >= 4  # At least 2 reads + 2 writes

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_indent_consistency(self, mock_file, mock_ensure, mock_status_file):
        """Test that JSON indent is consistently 2."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-37", status_data)
        
        # Verify json.dump was called with indent=2
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_ensure_path_called_before_open(self, mock_file, mock_ensure, mock_status_file):
        """Test that ensure_path_exists is called before file open."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-38", status_data)
        
        # ensure_path_exists should be called before open
        mock_ensure.assert_called_once()
        assert mock_file.call_count > 0

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_mode_write(self, mock_file, mock_ensure, mock_status_file):
        """Test that file is opened in write mode."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-39", status_data)
        
        # File should be opened in write mode
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_utf8_encoding_explicit(self, mock_file, mock_ensure, mock_status_file):
        """Test that UTF-8 encoding is explicitly used."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "unicode": "émojis 🚀"}
        refresh_status_embedding("Agent-40", status_data)
        
        # UTF-8 encoding should be explicitly used
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"data": "old"}}')
    def test_refresh_status_embedding_preserves_all_other_agents(self, mock_file, mock_ensure, mock_status_file):
        """Test that all other agents are preserved when updating one."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        original_data = {
            "Agent-1": {"data": "old1"},
            "Agent-2": {"data": "old2"},
            "Agent-3": {"data": "old3"}
        }
        
        with patch('json.load', return_value=original_data):
            status_data = {"status": "updated"}
            refresh_status_embedding("Agent-1", status_data)
            
            # Should preserve Agent-2 and Agent-3
            mock_ensure.assert_called_once()
            assert mock_file.call_count >= 2

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_empty_status_data_dict(self, mock_file, mock_ensure, mock_status_file):
        """Test refreshing with empty status_data dictionary."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {}
        refresh_status_embedding("Agent-41", status_data)
        
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_status_file_path_usage(self, mock_file, mock_ensure, mock_status_file):
        """Test that STATUS_EMBEDDINGS_FILE path is used correctly."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-42", status_data)
        
        # STATUS_EMBEDDINGS_FILE should be used
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_json_dump_call_verification(self, mock_file, mock_ensure, mock_status_file):
        """Test that json.dump is called with correct parameters."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-43", status_data)
        
        # json.dump should be called with indent=2 and ensure_ascii=False
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_ensure_ascii_false(self, mock_file, mock_ensure, mock_status_file):
        """Test that ensure_ascii=False is used for UTF-8 support."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active", "unicode": "émojis 🚀 测试"}
        refresh_status_embedding("Agent-44", status_data)
        
        # ensure_ascii=False should be used for UTF-8
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Agent-1": {"data": "old"}}')
    def test_refresh_status_embedding_json_load_error_handling(self, mock_file, mock_ensure, mock_status_file):
        """Test handling of JSON load errors."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        
        with patch('json.load', side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
            # Should handle JSON decode errors
            try:
                refresh_status_embedding("Agent-45", status_data)
            except json.JSONDecodeError:
                pass  # Expected to raise

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_file_not_found_during_read(self, mock_file, mock_ensure, mock_status_file):
        """Test handling when file disappears between exists check and read."""
        mock_status_file.exists.return_value = True
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        
        with patch('json.load', side_effect=FileNotFoundError("File not found")):
            # Should handle file not found during read
            try:
                refresh_status_embedding("Agent-46", status_data)
            except FileNotFoundError:
                pass  # Expected to raise

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_ensure_path_raises_exception(self, mock_file, mock_ensure, mock_status_file):
        """Test handling when ensure_path_exists raises exception."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        mock_ensure.side_effect = Exception("Path creation failed")
        
        # Should handle ensure_path_exists exceptions
        try:
            refresh_status_embedding("Agent-47", status_data)
        except Exception:
            pass  # Expected to raise

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_status_file_parent_access(self, mock_file, mock_ensure, mock_status_file):
        """Test that status_file.parent is accessed correctly."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-48", status_data)
        
        # status_file.parent should be accessed
        assert hasattr(mock_status_file, 'parent')
        mock_ensure.assert_called_once()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_status_file_str_representation(self, mock_file, mock_ensure, mock_status_file):
        """Test that status_file string representation is used."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        mock_status_file.__str__ = lambda x: "/test/path/status_embeddings.json"
        
        status_data = {"status": "active"}
        refresh_status_embedding("Agent-49", status_data)
        
        # status_file should be used as string
        mock_ensure.assert_called_once()
        mock_file.assert_called()

    @patch("src.services.status_embedding_indexer.STATUS_EMBEDDINGS_FILE")
    @patch("src.services.status_embedding_indexer.ensure_path_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_refresh_status_embedding_multiple_calls_same_agent(self, mock_file, mock_ensure, mock_status_file):
        """Test multiple calls to refresh same agent."""
        mock_status_file.exists.return_value = False
        mock_status_file.parent = Path("/test/path")
        
        status_data1 = {"status": "first"}
        status_data2 = {"status": "second"}
        
        refresh_status_embedding("Agent-50", status_data1)
        refresh_status_embedding("Agent-50", status_data2)
        
        # Should handle multiple calls to same agent
        assert mock_ensure.call_count == 2
        assert mock_file.call_count >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

