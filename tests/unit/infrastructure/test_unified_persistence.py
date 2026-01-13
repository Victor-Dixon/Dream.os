"""
Tests for Unified Persistence Service - Infrastructure Domain

Tests for unified persistence service that combines agent and task repositories.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.unified_persistence import UnifiedPersistenceService
from src.infrastructure.persistence.persistence_models import PersistenceConfig


class TestUnifiedPersistenceService:
    """Tests for UnifiedPersistenceService SSOT."""

    def test_unified_persistence_service_initialization(self):
        """Test UnifiedPersistenceService initializes correctly."""
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        assert service.config == config
        assert service.agent_repo is not None
        assert service.task_repo is not None
        assert service.stats is not None

    def test_unified_persistence_service_agent_repository_access(self):
        """Test agent_repository is accessible."""
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        assert service.agent_repo is not None

    def test_unified_persistence_service_task_repository_access(self):
        """Test task_repository is accessible."""
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        assert service.task_repo is not None

    def test_unified_persistence_service_statistics_access(self):
        """Test statistics is accessible."""
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        assert service.stats is not None

    def test_unified_persistence_service_with_custom_path(self):
        """Test UnifiedPersistenceService with custom database path."""
        test_db = Path("test_unified_persistence.db")
        config = PersistenceConfig(db_path=str(test_db))
        try:
            service = UnifiedPersistenceService(config)
            assert service.config.db_path == str(test_db)
            assert service.agent_repo is not None
            assert service.task_repo is not None
        finally:
            if test_db.exists():
                test_db.unlink()

    @patch('src.infrastructure.persistence.agent_repository.AgentRepository.list_all')
    def test_unified_persistence_service_list_agents(self, mock_list_all):
        """Test list_agents returns list of agents."""
        mock_list_all.return_value = []
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        agents = service.list_agents(limit=10)
        assert isinstance(agents, list)

    @patch('src.infrastructure.persistence.task_repository.TaskRepository.list_all')
    def test_unified_persistence_service_list_tasks(self, mock_list_all):
        """Test list_tasks returns list of tasks."""
        mock_list_all.return_value = []
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        tasks = service.list_tasks(limit=10)
        assert isinstance(tasks, list)

    def test_unified_persistence_service_get_database_stats(self):
        """Test get_database_stats returns statistics."""
        config = PersistenceConfig(db_path=":memory:")
        service = UnifiedPersistenceService(config)
        stats = service.get_database_stats()
        assert isinstance(stats, dict)

