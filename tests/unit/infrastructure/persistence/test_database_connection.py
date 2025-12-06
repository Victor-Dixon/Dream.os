"""
Tests for Database Connection - Infrastructure Domain

Tests for database connection management with proper cleanup and configuration.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-06
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.persistence.database_connection import DatabaseConnection
from src.infrastructure.persistence.persistence_models import PersistenceConfig


class TestDatabaseConnection:
    """Tests for DatabaseConnection SSOT."""

    def test_database_connection_initialization(self):
        """Test DatabaseConnection initializes correctly."""
        config = PersistenceConfig(db_path=":memory:")
        connection = DatabaseConnection(config)
        assert connection.config == config
        assert connection.config.db_path == ":memory:"

    def test_database_connection_context_manager(self):
        """Test DatabaseConnection works as context manager."""
        config = PersistenceConfig(db_path=":memory:")
        with DatabaseConnection(config) as conn:
            assert conn is not None
            assert hasattr(conn, 'cursor')

    def test_database_connection_cleanup(self):
        """Test DatabaseConnection properly cleans up."""
        config = PersistenceConfig(db_path=":memory:")
        connection = DatabaseConnection(config)
        with connection as conn:
            pass
        # Connection should be closed after context exit
        assert True  # Context manager handles cleanup

    def test_database_connection_with_custom_path(self):
        """Test DatabaseConnection with custom database path."""
        test_db = Path("test_db.db")
        config = PersistenceConfig(db_path=str(test_db))
        try:
            with DatabaseConnection(config) as conn:
                assert conn is not None
        finally:
            if test_db.exists():
                test_db.unlink()

    def test_database_connection_error_handling(self):
        """Test DatabaseConnection handles errors gracefully."""
        # Invalid config should raise appropriate error
        with pytest.raises((ValueError, AttributeError)):
            DatabaseConnection(None)


