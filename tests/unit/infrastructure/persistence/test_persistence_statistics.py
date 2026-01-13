"""
Tests for Persistence Statistics - Infrastructure Domain

Tests for persistence layer statistics functionality.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-06
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.persistence.persistence_statistics import PersistenceStatistics
from src.infrastructure.persistence.database_connection import DatabaseConnection
from src.infrastructure.persistence.persistence_models import PersistenceConfig


class TestPersistenceStatistics:
    """Tests for PersistenceStatistics SSOT."""

    def test_persistence_statistics_initialization(self):
        """Test PersistenceStatistics initializes correctly."""
        config = PersistenceConfig(db_path=":memory:")
        db_conn = DatabaseConnection(config)
        stats = PersistenceStatistics(db_conn)
        assert stats.db == db_conn

    def test_persistence_statistics_get_database_stats(self):
        """Test get_database_stats returns comprehensive stats."""
        config = PersistenceConfig(db_path=":memory:")
        db_conn = DatabaseConnection(config)
        stats = PersistenceStatistics(db_conn)
        statistics = stats.get_database_stats()
        assert isinstance(statistics, dict)
        assert "total_agents" in statistics
        assert "active_agents" in statistics
        assert "total_tasks" in statistics
        assert "pending_tasks" in statistics
        assert "completed_tasks" in statistics
        assert "assigned_tasks" in statistics
        assert "database_size" in statistics
        assert "table_info" in statistics

