"""
Unit tests for task_handler.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.handlers.task_handler import TaskHandler


class TestTaskHandler:
    """Test suite for TaskHandler."""

    @pytest.fixture
    def handler(self):
        """Create TaskHandler instance."""
        return TaskHandler()

    def test_handler_initialization(self, handler):
        """Test handler initializes correctly."""
        assert handler is not None
        assert handler.exit_code == 0

    def test_can_handle_get_next_task(self, handler):
        """Test can_handle detects get_next_task."""
        args = Mock()
        args.get_next_task = True
        args.list_tasks = False
        args.task_status = False
        args.complete_task = False
        
        assert handler.can_handle(args) is True

    def test_can_handle_list_tasks(self, handler):
        """Test can_handle detects list_tasks."""
        args = Mock()
        args.get_next_task = False
        args.list_tasks = True
        args.task_status = False
        args.complete_task = False
        
        assert handler.can_handle(args) is True

    def test_can_handle_task_status(self, handler):
        """Test can_handle detects task_status."""
        args = Mock()
        args.get_next_task = False
        args.list_tasks = False
        args.task_status = True
        args.complete_task = False
        
        assert handler.can_handle(args) is True

    def test_can_handle_complete_task(self, handler):
        """Test can_handle detects complete_task."""
        args = Mock()
        args.get_next_task = False
        args.list_tasks = False
        args.task_status = False
        args.complete_task = True
        
        assert handler.can_handle(args) is True

    def test_can_handle_none(self, handler):
        """Test can_handle returns False for non-task commands."""
        args = Mock()
        args.get_next_task = False
        args.list_tasks = False
        args.task_status = False
        args.complete_task = False
        
        assert handler.can_handle(args) is False

    @patch('src.services.helpers.task_repo_loader.SimpleTaskRepository')
    def test_handle_get_next_task(self, mock_repo_class, handler):
        """Test handle routes to get_next_task handler."""
        args = Mock()
        args.get_next_task = True
        args.list_tasks = False
        args.task_status = False
        args.complete_task = False
        args.agent = "Agent-1"
        
        mock_repo = Mock()
        mock_repo.get_pending.return_value = []
        mock_repo_class.return_value = mock_repo
        
        result = handler.handle(args)
        
        assert result is True
        assert handler.exit_code == 0

    @patch('src.services.helpers.task_repo_loader.SimpleTaskRepository')
    def test_handle_import_error(self, mock_repo_class, handler):
        """Test handle handles import errors gracefully."""
        args = Mock()
        args.get_next_task = True
        args.list_tasks = False
        args.task_status = False
        args.complete_task = False
        mock_repo_class.side_effect = ImportError("Module not found")
        
        result = handler.handle(args)
        
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.helpers.task_repo_loader.SimpleTaskRepository')
    def test_handle_exception(self, mock_repo_class, handler):
        """Test handle handles exceptions gracefully."""
        args = Mock()
        args.get_next_task = True
        args.list_tasks = False
        args.task_status = False
        args.complete_task = False
        mock_repo_class.side_effect = Exception("Test error")
        
        result = handler.handle(args)
        
        assert result is True
        assert handler.exit_code == 1

