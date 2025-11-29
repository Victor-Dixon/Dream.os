"""
Tests for cursor_db.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

from src.services.cursor_db import CursorTask, CursorTaskRepository, DEFAULT_DB_PATH
import pytest
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
import sys
import os
import time

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))


class TestCursorTask:
    """Test CursorTask dataclass."""

    def test_create_cursor_task(self):
        """Test creating CursorTask instance."""
        task = CursorTask(
            task_id="test-123",
            agent_id="Agent-1",
            status="pending"
        )

        assert task.task_id == "test-123"
        assert task.agent_id == "Agent-1"
        assert task.status == "pending"

    def test_cursor_task_all_fields(self):
        """Test CursorTask has all required fields."""
        task = CursorTask(
            task_id="task-1",
            agent_id="Agent-2",
            status="completed"
        )

        assert hasattr(task, 'task_id')
        assert hasattr(task, 'agent_id')
        assert hasattr(task, 'status')

    def test_cursor_task_different_statuses(self):
        """Test CursorTask with different status values."""
        statuses = ["pending", "in_progress", "completed", "failed"]

        for status in statuses:
            task = CursorTask(
                task_id=f"task-{status}",
                agent_id="Agent-3",
                status=status
            )
            assert task.status == status


class TestCursorTaskRepository:
    """Test CursorTaskRepository class."""

    def test_init_with_default_path(self):
        """Test repository initialization with default path."""
        repo = CursorTaskRepository()
        assert repo.db_path == DEFAULT_DB_PATH

    def test_init_with_custom_path(self):
        """Test repository initialization with custom path."""
        custom_path = Path("custom/path.db")
        repo = CursorTaskRepository(custom_path)
        assert repo.db_path == custom_path

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_get_task_existing(self, mock_connect):
        """Test getting an existing task."""
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test-1', 'Agent-1', 'pending')

        repo = CursorTaskRepository(Path("test.db"))
        task = repo.get_task('test-1')

        assert task is not None
        assert task.task_id == 'test-1'
        assert task.agent_id == 'Agent-1'
        assert task.status == 'pending'
        mock_conn.execute.assert_called_once()
        assert 'SELECT' in mock_conn.execute.call_args[0][0]

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_get_task_non_existing(self, mock_connect):
        """Test getting a non-existing task."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        repo = CursorTaskRepository(Path("test.db"))
        task = repo.get_task('non-existent')

        assert task is None

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_get_task_different_id(self, mock_connect):
        """Test getting task with different ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test-2', 'Agent-2', 'completed')

        repo = CursorTaskRepository(Path("test.db"))
        task = repo.get_task('test-2')

        assert task is not None
        assert task.task_id == 'test-2'
        assert task.agent_id == 'Agent-2'
        assert task.status == 'completed'

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_task_exists_true(self, mock_connect):
        """Test task_exists returns True for existing task."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test-1', 'Agent-1', 'pending')

        repo = CursorTaskRepository(Path("test.db"))
        assert repo.task_exists('test-1') is True

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_task_exists_false(self, mock_connect):
        """Test task_exists returns False for non-existing task."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        repo = CursorTaskRepository(Path("test.db"))
        assert repo.task_exists('non-existent') is False

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_get_task_returns_cursor_task(self, mock_connect):
        """Test get_task returns CursorTask instance."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test-1', 'Agent-1', 'pending')

        repo = CursorTaskRepository(Path("test.db"))
        task = repo.get_task('test-1')

        assert isinstance(task, CursorTask)
        assert hasattr(task, 'task_id')
        assert hasattr(task, 'agent_id')
        assert hasattr(task, 'status')

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_get_task_uses_parameterized_query(self, mock_connect):
        """Test that get_task uses parameterized query (SQL injection protection)."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        repo = CursorTaskRepository(Path("test.db"))
        malicious_id = "test-1' OR '1'='1"
        repo.get_task(malicious_id)

        # Verify parameterized query was used
        call_args = mock_conn.execute.call_args
        assert '?' in call_args[0][0]  # Query has placeholder
        # Parameter passed separately
        assert call_args[0][1] == (malicious_id,)

    @patch('src.services.cursor_db.sqlite3.connect')
    def test_task_exists_uses_parameterized_query(self, mock_connect):
        """Test that task_exists uses parameterized query (SQL injection protection)."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        repo = CursorTaskRepository(Path("test.db"))
        malicious_id = "test-1' OR '1'='1"
        repo.task_exists(malicious_id)

        # Verify parameterized query was used
        call_args = mock_conn.execute.call_args
        assert '?' in call_args[0][0]  # Query has placeholder
        # Parameter passed separately
        assert call_args[0][1] == (malicious_id,)
