"""
Unit tests for src/services/agent_management.py

Tests agent management functionality including:
- Agent assignment management
- Agent status tracking
- Task context management
- Vector database integration
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime

from src.services.agent_management import (
    AgentAssignmentManager,
    AgentStatusManager,
    TaskContextManager,
)
from src.services.architectural_models import ArchitecturalPrinciple


class TestAgentAssignmentManager:
    """Test agent assignment manager."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "architectural_assignments.json"
            yield str(config_path)

    def test_init_loads_default_assignments(self, temp_config_dir):
        """Test initialization loads default assignments."""
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        
        assert len(manager.assignments) == 8
        assert manager.get_agent_principle("Agent-1") == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert manager.get_agent_principle("Agent-5") == ArchitecturalPrinciple.DEPENDENCY_INVERSION

    def test_init_loads_from_file(self, temp_config_dir):
        """Test initialization loads from existing config file."""
        config_data = {
            "Agent-1": "single_responsibility",
            "Agent-2": "open_closed",
        }
        
        Path(temp_config_dir).parent.mkdir(parents=True, exist_ok=True)
        with open(temp_config_dir, 'w') as f:
            json.dump(config_data, f)
        
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        
        assert manager.get_agent_principle("Agent-1") == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        assert manager.get_agent_principle("Agent-2") == ArchitecturalPrinciple.OPEN_CLOSED

    def test_get_agent_principle(self, temp_config_dir):
        """Test getting agent principle."""
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        
        principle = manager.get_agent_principle("Agent-1")
        assert principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY
        
        principle = manager.get_agent_principle("NonExistent")
        assert principle is None

    def test_assign_principle(self, temp_config_dir):
        """Test assigning principle to agent."""
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        
        manager.assign_principle("Agent-9", ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
        
        assert manager.get_agent_principle("Agent-9") == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY

    def test_get_all_assignments(self, temp_config_dir):
        """Test getting all assignments."""
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        
        assignments = manager.get_all_assignments()
        
        assert isinstance(assignments, dict)
        assert len(assignments) == 8
        assert "Agent-1" in assignments

    def test_get_agents_by_principle(self, temp_config_dir):
        """Test getting agents by principle."""
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        
        agents = manager.get_agents_by_principle(ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
        
        assert isinstance(agents, list)
        assert "Agent-1" in agents

    def test_save_assignments(self, temp_config_dir):
        """Test saving assignments to file."""
        manager = AgentAssignmentManager(config_path=temp_config_dir)
        manager.assign_principle("Agent-9", ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
        
        assert Path(temp_config_dir).exists()
        
        with open(temp_config_dir, 'r') as f:
            saved_data = json.load(f)
        
        assert "Agent-9" in saved_data
        assert saved_data["Agent-9"] == "SRP"


class TestAgentStatusManager:
    """Test agent status manager."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_dir = Path(tmpdir) / "agent_workspaces" / "Agent-5"
            workspace_dir.mkdir(parents=True)
            inbox_dir = workspace_dir / "inbox"
            inbox_dir.mkdir()
            
            # Create sample files
            (workspace_dir / "status.json").write_text('{"status": "active"}')
            (inbox_dir / "message1.md").write_text("# Test message")
            
            yield tmpdir

    @patch('src.services.agent_management.get_vector_database_service')
    def test_init_with_vector_db(self, mock_get_vector_db, temp_workspace):
        """Test initialization with vector database available."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        
        manager = AgentStatusManager("Agent-5")
        
        assert manager.agent_id == "Agent-5"
        assert manager.vector_integration["status"] == "connected"

    @patch('src.services.agent_management.get_vector_database_service')
    def test_init_without_vector_db(self, mock_get_vector_db, temp_workspace):
        """Test initialization without vector database."""
        mock_get_vector_db.side_effect = ImportError("Vector DB not available")
        
        manager = AgentStatusManager("Agent-5")
        
        assert manager.agent_id == "Agent-5"
        assert manager.vector_integration["status"] == "disconnected"

    @patch('src.services.agent_management.get_vector_database_service')
    @patch('src.services.agent_management.search_vector_database')
    def test_get_agent_status(self, mock_search, mock_get_vector_db, temp_workspace):
        """Test getting agent status."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        mock_search.return_value = [{"id": "1"}, {"id": "2"}]
        
        with patch('src.services.agent_management.Path') as mock_path:
            mock_path.return_value = Path(temp_workspace) / "agent_workspaces" / "Agent-5"
            
            manager = AgentStatusManager("Agent-5")
            status = manager.get_agent_status()
            
            assert status["agent_id"] == "Agent-5"
            assert status["status"] == "active"
            assert "recent_work_count" in status
            assert "pending_tasks_count" in status
            assert "last_activity" in status

    @patch('src.services.agent_management.get_vector_database_service')
    def test_get_integration_stats(self, mock_get_vector_db, temp_workspace):
        """Test getting integration statistics."""
        mock_vector_db = MagicMock()
        mock_vector_db.get_stats.return_value = MagicMock(total_documents=100)
        mock_get_vector_db.return_value = mock_vector_db
        
        with patch('src.services.agent_management.search_vector_database') as mock_search:
            mock_search.return_value = [{"id": "1"}]
            
            manager = AgentStatusManager("Agent-5")
            stats = manager.get_integration_stats()
            
            assert "total_documents" in stats
            assert "agent_documents" in stats
            assert stats["integration_status"] == "healthy"

    @patch('src.services.agent_management.get_vector_database_service')
    @patch('src.services.agent_management.search_vector_database')
    @patch('src.services.agent_management.SearchQuery')
    def test_get_recent_work_count(self, mock_search_query, mock_search, mock_get_vector_db, temp_workspace):
        """Test getting recent work count."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        mock_search.return_value = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        # Mock SearchQuery to accept any kwargs
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        manager = AgentStatusManager("Agent-5")
        count = manager._get_recent_work_count()
        
        assert count == 3

    @patch('src.services.agent_management.get_vector_database_service')
    def test_get_pending_tasks_count(self, mock_get_vector_db, temp_workspace):
        """Test getting pending tasks count."""
        mock_get_vector_db.side_effect = ImportError("Vector DB not available")
        
        with patch('src.services.agent_management.Path') as mock_path:
            workspace_path = Path(temp_workspace) / "agent_workspaces" / "Agent-5"
            mock_path.return_value = workspace_path
            
            manager = AgentStatusManager("Agent-5")
            count = manager._get_pending_tasks_count()
            
            assert count >= 0

    @patch('src.services.agent_management.get_vector_database_service')
    def test_get_last_activity(self, mock_get_vector_db, temp_workspace):
        """Test getting last activity timestamp."""
        mock_get_vector_db.side_effect = ImportError("Vector DB not available")
        
        with patch('src.services.agent_management.Path') as mock_path:
            workspace_path = Path(temp_workspace) / "agent_workspaces" / "Agent-5"
            mock_path.return_value = workspace_path
            
            manager = AgentStatusManager("Agent-5")
            activity = manager._get_last_activity()
            
            assert isinstance(activity, str)
            assert len(activity) > 0


class TestTaskContextManager:
    """Test task context manager."""

    @patch('src.services.agent_management.get_vector_database_service')
    def test_init_with_vector_db(self, mock_get_vector_db):
        """Test initialization with vector database."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        
        manager = TaskContextManager("Agent-5")
        
        assert manager.agent_id == "Agent-5"
        assert manager.vector_integration["status"] == "connected"

    @patch('src.services.agent_management.get_vector_database_service')
    def test_init_without_vector_db(self, mock_get_vector_db):
        """Test initialization without vector database."""
        mock_get_vector_db.side_effect = ImportError("Vector DB not available")
        
        manager = TaskContextManager("Agent-5")
        
        assert manager.agent_id == "Agent-5"
        assert manager.vector_integration["status"] == "disconnected"

    @patch('src.services.agent_management.get_vector_database_service')
    @patch('src.services.agent_management.search_vector_database')
    @patch('src.services.agent_management.format_search_result')
    @patch('src.services.agent_management.generate_recommendations')
    def test_get_task_context(self, mock_recommendations, mock_format, mock_search, mock_get_vector_db):
        """Test getting task context."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        mock_search.return_value = [{"id": "1"}]
        mock_format.return_value = {"formatted": "result"}
        mock_recommendations.return_value = ["Recommendation 1"]
        
        manager = TaskContextManager("Agent-5")
        context = manager.get_task_context("Test task")
        
        assert context["task_description"] == "Test task"
        assert "similar_tasks" in context
        assert "related_messages" in context
        assert "devlog_insights" in context
        assert "recommendations" in context
        assert context["context_loaded"] is True

    @patch('src.services.agent_management.get_vector_database_service')
    def test_get_task_context_fallback(self, mock_get_vector_db):
        """Test getting task context with fallback mode."""
        mock_get_vector_db.side_effect = ImportError("Vector DB not available")
        
        manager = TaskContextManager("Agent-5")
        context = manager.get_task_context("Test task")
        
        assert context["task_description"] == "Test task"
        assert context["fallback_mode"] is True
        assert context["context_loaded"] is False

    @patch('src.services.agent_management.get_vector_database_service')
    @patch('src.services.agent_management.search_vector_database')
    @patch('src.services.agent_management.SearchQuery')
    def test_search_similar_tasks(self, mock_search_query, mock_search, mock_get_vector_db):
        """Test searching for similar tasks."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        mock_search.return_value = [{"id": "1"}]
        # Mock SearchQuery to accept any kwargs
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        manager = TaskContextManager("Agent-5")
        results = manager._search_similar_tasks("Test task")
        
        assert isinstance(results, list)
        assert len(results) == 1

    @patch('src.services.agent_management.get_vector_database_service')
    @patch('src.services.agent_management.search_vector_database')
    def test_search_related_messages(self, mock_search, mock_get_vector_db):
        """Test searching for related messages."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        mock_search.return_value = [{"id": "1"}]
        
        manager = TaskContextManager("Agent-5")
        results = manager._search_related_messages("Test task")
        
        assert isinstance(results, list)

    @patch('src.services.agent_management.get_vector_database_service')
    @patch('src.services.agent_management.search_vector_database')
    def test_search_devlog_insights(self, mock_search, mock_get_vector_db):
        """Test searching for devlog insights."""
        mock_vector_db = MagicMock()
        mock_get_vector_db.return_value = mock_vector_db
        mock_search.return_value = [{"id": "1"}]
        
        manager = TaskContextManager("Agent-5")
        results = manager._search_devlog_insights("Test task")
        
        assert isinstance(results, list)

    @patch('src.services.agent_management.get_vector_database_service')
    def test_get_fallback_context(self, mock_get_vector_db):
        """Test getting fallback context."""
        mock_get_vector_db.side_effect = ImportError("Vector DB not available")
        
        manager = TaskContextManager("Agent-5")
        context = manager._get_fallback_context("Test task")
        
        assert context["task_description"] == "Test task"
        assert context["fallback_mode"] is True
        assert isinstance(context["recommendations"], list)

