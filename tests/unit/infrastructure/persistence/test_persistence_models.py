"""
Tests for Persistence Models - Infrastructure Domain

Tests for persistence layer data models.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from datetime import datetime

from src.infrastructure.persistence.persistence_models import (
    PersistenceConfig,
    Agent,
    TaskPersistenceModel,
)


class TestPersistenceConfig:
    """Tests for PersistenceConfig."""

    def test_persistence_config_defaults(self):
        """Test PersistenceConfig with default values."""
        config = PersistenceConfig()
        assert config.db_path == "data/unified.db"
        assert config.auto_migrate is True
        assert config.connection_timeout == 30.0

    def test_persistence_config_custom_values(self):
        """Test PersistenceConfig with custom values."""
        config = PersistenceConfig(
            db_path="custom.db",
            auto_migrate=False,
            connection_timeout=60.0,
        )
        assert config.db_path == "custom.db"
        assert config.auto_migrate is False
        assert config.connection_timeout == 60.0


class TestAgent:
    """Tests for Agent model."""

    def test_agent_initialization(self):
        """Test Agent initializes correctly."""
        agent = Agent(
            id="agent-1",
            name="Test Agent",
            role="test_role",
            capabilities=["cap1", "cap2"],
        )
        assert agent.id == "agent-1"
        assert agent.name == "Test Agent"
        assert agent.role == "test_role"
        assert agent.capabilities == ["cap1", "cap2"]
        assert agent.max_concurrent_tasks == 3
        assert agent.is_active is True
        assert agent.created_at is not None
        assert isinstance(agent.created_at, datetime)

    def test_agent_with_custom_values(self):
        """Test Agent with custom values."""
        created = datetime(2024, 1, 1)
        agent = Agent(
            id="agent-2",
            name="Custom Agent",
            role="custom_role",
            capabilities=[],
            max_concurrent_tasks=5,
            is_active=False,
            created_at=created,
        )
        assert agent.max_concurrent_tasks == 5
        assert agent.is_active is False
        assert agent.created_at == created


class TestTaskPersistenceModel:
    """Tests for TaskPersistenceModel."""

    def test_task_initialization(self):
        """Test TaskPersistenceModel initializes correctly."""
        task = TaskPersistenceModel(
            id="task-1",
            title="Test Task",
            description="Test description",
        )
        assert task.id == "task-1"
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.assigned_agent_id is None
        assert task.status == "pending"
        assert task.priority == 1
        assert task.created_at is not None
        assert isinstance(task.created_at, datetime)
        assert task.completed_at is None

    def test_task_with_custom_values(self):
        """Test TaskPersistenceModel with custom values."""
        created = datetime(2024, 1, 1)
        completed = datetime(2024, 1, 2)
        task = TaskPersistenceModel(
            id="task-2",
            title="Custom Task",
            description="Custom description",
            assigned_agent_id="agent-1",
            status="completed",
            priority=5,
            created_at=created,
            completed_at=completed,
        )
        assert task.assigned_agent_id == "agent-1"
        assert task.status == "completed"
        assert task.priority == 5
        assert task.created_at == created
        assert task.completed_at == completed

