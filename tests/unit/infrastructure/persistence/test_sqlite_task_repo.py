"""
Tests for SQLite Task Repository - Infrastructure Domain

Tests for SQLite-based task repository (legacy compatibility).

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.persistence.sqlite_task_repo import SqliteTaskRepository


class TestSqliteTaskRepository:
    """Tests for SqliteTaskRepository (legacy compatibility)."""

    def test_sqlite_task_repository_initialization(self):
        """Test SqliteTaskRepository initializes correctly."""
        repo = SqliteTaskRepository(db_path=":memory:")
        assert repo.db_path == ":memory:"

