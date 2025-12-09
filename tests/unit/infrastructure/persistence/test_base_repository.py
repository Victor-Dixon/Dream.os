"""
Tests for Base Repository - Infrastructure Domain

Tests for base repository pattern implementation.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.persistence.base_repository import BaseRepository
from src.infrastructure.persistence.database_connection import DatabaseConnection
from src.infrastructure.persistence.persistence_models import PersistenceConfig


class TestBaseRepository:
    """Tests for BaseRepository SSOT."""

    def test_base_repository_initialization(self):
        """Test BaseRepository initializes correctly."""
        config = PersistenceConfig(db_path=":memory:")
        db_conn = DatabaseConnection(config)
        
        # BaseRepository is abstract, so we'll test via a concrete implementation
        # Import AgentRepository which extends BaseRepository
        from src.infrastructure.persistence.agent_repository import AgentRepository
        repo = AgentRepository(db_conn)
        assert repo.db == db_conn

    def test_base_repository_database_connection(self):
        """Test BaseRepository has database connection."""
        config = PersistenceConfig(db_path=":memory:")
        db_conn = DatabaseConnection(config)
        
        from src.infrastructure.persistence.agent_repository import AgentRepository
        repo = AgentRepository(db_conn)
        assert hasattr(repo, 'db')
        assert repo.db is not None

