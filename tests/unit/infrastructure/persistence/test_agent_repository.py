"""
Tests for Agent Repository - Infrastructure Domain

Tests for agent repository that handles agent persistence operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.persistence.agent_repository import AgentRepository
from src.infrastructure.persistence.database_connection import DatabaseConnection
from src.infrastructure.persistence.persistence_models import Agent


@pytest.fixture
def mock_db_connection():
    """Mock DatabaseConnection to avoid real SQLite operations."""
    mock_db = MagicMock(spec=DatabaseConnection)
    mock_db.db_path = ":memory:"
    mock_db.execute_query.return_value = []
    mock_db.execute_update.return_value = 1
    mock_db.create_tables.return_value = None
    return mock_db


class TestAgentRepository:
    """Tests for AgentRepository SSOT."""

    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_initialization(self, mock_schema, mock_db_connection):
        """Test AgentRepository initializes correctly."""
        repo = AgentRepository(mock_db_connection)
        assert repo.db == mock_db_connection
        mock_schema.assert_called_once()

    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_save_agent(self, mock_schema, mock_db_connection):
        """Test save agent operation."""
        repo = AgentRepository(mock_db_connection)
        agent = Agent(
            id="test-agent-1",
            name="Test Agent",
            role="test_role",
            capabilities=["test_capability"],
            max_concurrent_tasks=3,
            is_active=True,
        )
        repo.save(agent)
        assert mock_db_connection.execute_update.called

    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_get_agent(self, mock_schema, mock_db_connection):
        """Test get agent operation."""
        now = datetime.now().isoformat()
        mock_db_connection.execute_query.return_value = [
            ("test-agent-2", "Test Agent 2", "test_role", json.dumps(["cap"]), 3, 1, now, None)
        ]
        repo = AgentRepository(mock_db_connection)
        retrieved = repo.get("test-agent-2")
        assert retrieved is not None
        assert retrieved.id == "test-agent-2"

    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_get_nonexistent_agent(self, mock_schema, mock_db_connection):
        """Test get nonexistent agent returns None."""
        mock_db_connection.execute_query.return_value = []
        repo = AgentRepository(mock_db_connection)
        retrieved = repo.get("nonexistent-agent")
        assert retrieved is None

    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_delete_agent(self, mock_schema, mock_db_connection):
        """Test delete agent operation."""
        repo = AgentRepository(mock_db_connection)
        result = repo.delete("test-agent-3")
        assert result is True
        assert mock_db_connection.execute_update.called

    @patch.object(AgentRepository, "_row_to_agent")
    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_list_all_agents(self, mock_schema, mock_row_to_agent, mock_db_connection):
        """Test list_all returns all agents."""
        mock_row_to_agent.side_effect = [
            Agent(
                id=f"test-agent-{i}",
                name=f"Test Agent {i}",
                role="test_role",
                capabilities=["test_capability"],
                max_concurrent_tasks=3,
                is_active=True,
            )
            for i in range(3)
        ]
        now = datetime.now().isoformat()
        mock_db_connection.execute_query.return_value = [
            (f"test-agent-{i}", f"Test Agent {i}", "test_role", json.dumps(["test_capability"]), 3, 1, now, None)
            for i in range(3)
        ]
        repo = AgentRepository(mock_db_connection)
        agents = list(repo.list_all(limit=10))
        assert len(agents) == 3

    @patch.object(AgentRepository, "_row_to_agent")
    @patch.object(AgentRepository, "_ensure_schema")
    def test_agent_repository_get_active_agents(self, mock_schema, mock_row_to_agent, mock_db_connection):
        """Test get_active returns only active agents."""
        mock_row_to_agent.side_effect = [
            Agent(
                id="active-agent",
                name="Active Agent",
                role="test_role",
                capabilities=["test_capability"],
                max_concurrent_tasks=3,
                is_active=True,
            )
        ]
        now = datetime.now().isoformat()
        mock_db_connection.execute_query.return_value = [
            ("active-agent", "Active Agent", "test_role", json.dumps(["test_capability"]), 3, 1, now, now)
        ]
        repo = AgentRepository(mock_db_connection)
        active_agents = list(repo.get_active())
        assert len(active_agents) == 1
        assert all(agent.is_active for agent in active_agents)

