"""
Tests for SQLite Agent Repository - Infrastructure Domain

Tests for SQLite-based agent repository (legacy compatibility).

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.persistence.sqlite_agent_repo import SqliteAgentRepository


class TestSqliteAgentRepository:
    """Tests for SqliteAgentRepository (legacy compatibility)."""

    def test_sqlite_agent_repository_initialization(self):
        """Test SqliteAgentRepository initializes correctly."""
        repo = SqliteAgentRepository(db_path=":memory:")
        assert repo.db_path == ":memory:"

