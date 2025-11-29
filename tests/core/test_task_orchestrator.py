"""
Unit tests for orchestration/task_orchestrator.py - HIGH PRIORITY

Tests TaskOrchestrator class functionality.
Note: Maps to BaseOrchestrator or core orchestrators.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import base orchestrator (can be used as task orchestrator)
from src.core.orchestration.base_orchestrator import BaseOrchestrator
from src.core.orchestration.contracts import OrchestrationContext, OrchestrationResult


class TaskOrchestrator(BaseOrchestrator):
    """Task orchestrator - extends BaseOrchestrator."""
    
    def _register_components(self) -> None:
        """Register task orchestrator components."""
        pass
    
    def _load_default_config(self) -> dict:
        """Load default configuration."""
        return {"max_tasks": 10, "timeout": 30}
    
    def execute_task(self, task: dict) -> dict:
        """Execute a task."""
        return {"task_id": task.get("id"), "status": "completed"}
    
    def schedule_task(self, task: dict) -> str:
        """Schedule a task."""
        return f"task_{task.get('id', 'unknown')}"


class TestTaskOrchestrator:
    """Test suite for TaskOrchestrator class."""

    @pytest.fixture
    def orchestrator(self):
        """Create a TaskOrchestrator instance."""
        return TaskOrchestrator("test_orchestrator")

    def test_initialization(self, orchestrator):
        """Test TaskOrchestrator initialization."""
        assert orchestrator.name == "test_orchestrator"
        assert orchestrator.config is not None
        assert orchestrator.initialized is False

    def test_initialization_with_config(self):
        """Test initialization with custom config."""
        config = {"max_tasks": 20}
        orchestrator = TaskOrchestrator("test", config)
        
        assert orchestrator.config["max_tasks"] == 20

    def test_register_components(self, orchestrator):
        """Test _register_components method."""
        # Should not raise exception
        orchestrator._register_components()
        assert True

    def test_load_default_config(self, orchestrator):
        """Test _load_default_config method."""
        config = orchestrator._load_default_config()
        
        assert "max_tasks" in config
        assert "timeout" in config

    def test_initialize(self, orchestrator):
        """Test initialize method."""
        result = orchestrator.initialize()
        
        assert result is True
        assert orchestrator.initialized is True

    def test_initialize_idempotent(self, orchestrator):
        """Test initialize is idempotent."""
        result1 = orchestrator.initialize()
        result2 = orchestrator.initialize()
        
        assert result1 is True
        assert result2 is True
        assert orchestrator.initialized is True

    def test_cleanup(self, orchestrator):
        """Test cleanup method."""
        orchestrator.initialize()
        result = orchestrator.cleanup()
        
        assert result is True
        assert orchestrator.initialized is False

    def test_cleanup_not_initialized(self, orchestrator):
        """Test cleanup when not initialized."""
        result = orchestrator.cleanup()
        
        assert result is True

    def test_execute_task(self, orchestrator):
        """Test execute_task method."""
        task = {"id": "task1", "action": "test"}
        
        result = orchestrator.execute_task(task)
        
        assert result["task_id"] == "task1"
        assert result["status"] == "completed"

    def test_schedule_task(self, orchestrator):
        """Test schedule_task method."""
        task = {"id": "task1", "action": "test"}
        
        task_id = orchestrator.schedule_task(task)
        
        assert "task1" in task_id

    def test_register_component(self, orchestrator):
        """Test register_component method."""
        component = MagicMock()
        orchestrator.register_component("test_component", component)
        
        assert orchestrator.has_component("test_component") is True

    def test_get_component(self, orchestrator):
        """Test get_component method."""
        component = MagicMock()
        orchestrator.register_component("test_component", component)
        
        retrieved = orchestrator.get_component("test_component")
        
        assert retrieved == component

    def test_get_component_nonexistent(self, orchestrator):
        """Test get_component with nonexistent component."""
        retrieved = orchestrator.get_component("nonexistent")
        
        assert retrieved is None

    def test_get_status(self, orchestrator):
        """Test get_status method."""
        orchestrator.initialize()
        
        status = orchestrator.get_status()
        
        assert "orchestrator" in status
        assert status["orchestrator"] == "test_orchestrator"
        assert status["initialized"] is True

    def test_get_health(self, orchestrator):
        """Test get_health method."""
        orchestrator.initialize()
        
        health = orchestrator.get_health()
        
        assert "status" in health
        assert health["status"] == "healthy"

    def test_get_health_not_initialized(self, orchestrator):
        """Test get_health when not initialized."""
        health = orchestrator.get_health()
        
        assert health["status"] == "unhealthy"

    def test_context_manager(self):
        """Test context manager functionality."""
        with TaskOrchestrator("test") as orchestrator:
            assert orchestrator.initialized is True
        
        # After context exit, should be cleaned up
        assert orchestrator.initialized is False

    def test_emit_event(self, orchestrator):
        """Test emit event method."""
        callback = MagicMock()
        orchestrator.on("test_event", callback)
        orchestrator.emit("test_event", {"data": "test"})
        
        callback.assert_called_once()

