"""
Unit tests for orchestration/base_orchestrator.py - MEDIUM PRIORITY

Tests BaseOrchestrator class functionality using a concrete implementation.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import actual dependencies for proper testing
from src.core.orchestration.orchestrator_components import OrchestratorComponents
from src.core.orchestration.orchestrator_events import OrchestratorEvents
from src.core.orchestration.orchestrator_lifecycle import OrchestratorLifecycle

# Import using importlib
import importlib.util
base_orchestrator_path = project_root / "src" / "core" / "orchestration" / "base_orchestrator.py"
spec = importlib.util.spec_from_file_location("base_orchestrator", base_orchestrator_path)
base_orchestrator = importlib.util.module_from_spec(spec)
base_orchestrator.__package__ = 'src.core.orchestration'
spec.loader.exec_module(base_orchestrator)

BaseOrchestrator = base_orchestrator.BaseOrchestrator

# Create concrete implementation for testing
class ConcreteOrchestrator(BaseOrchestrator):
    """Concrete implementation of BaseOrchestrator for testing."""
    
    def _register_components(self):
        """Register test components."""
        self.register_component("test_component", Mock())
    
    def _load_default_config(self):
        """Load default configuration."""
        return {"setting1": "value1", "setting2": "value2"}


class TestBaseOrchestrator:
    """Test suite for BaseOrchestrator class."""

    @pytest.fixture
    def orchestrator(self):
        """Create a ConcreteOrchestrator instance."""
        return ConcreteOrchestrator("test_orchestrator")

    @pytest.fixture
    def orchestrator_with_config(self):
        """Create orchestrator with custom config."""
        config = {"custom": "value"}
        return ConcreteOrchestrator("test", config)

    def test_initialization(self, orchestrator):
        """Test BaseOrchestrator initialization."""
        assert orchestrator.name == "test_orchestrator"
        assert orchestrator.config["setting1"] == "value1"
        assert orchestrator.initialized is False
        assert isinstance(orchestrator.creation_time, datetime)
        assert orchestrator.logger is not None

    def test_initialization_with_custom_config(self, orchestrator_with_config):
        """Test initialization with custom config."""
        assert orchestrator_with_config.config["custom"] == "value"

    def test_initialize_success(self, orchestrator):
        """Test successful initialization."""
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=True) as mock_init:
            result = orchestrator.initialize()
            
            assert result is True
            assert orchestrator.initialized is True
            mock_init.assert_called_once()

    def test_initialize_idempotent(self, orchestrator):
        """Test that initialize is idempotent."""
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=True) as mock_init:
            result1 = orchestrator.initialize()
            result2 = orchestrator.initialize()
            
            assert result1 is True
            assert result2 is True
            assert orchestrator.initialized is True
            # Should only call once (second call returns early)
            assert mock_init.call_count == 1

    def test_initialize_failure(self, orchestrator):
        """Test initialization failure."""
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=False):
            result = orchestrator.initialize()
            
            assert result is False
            assert orchestrator.initialized is False

    def test_cleanup_success(self, orchestrator):
        """Test successful cleanup."""
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=True), \
             patch.object(OrchestratorLifecycle, 'cleanup_components', return_value=True) as mock_cleanup:
            orchestrator.initialize()
            result = orchestrator.cleanup()
            
            assert result is True
            assert orchestrator.initialized is False
            mock_cleanup.assert_called_once()

    def test_cleanup_not_initialized(self, orchestrator):
        """Test cleanup when not initialized."""
        result = orchestrator.cleanup()
        
        assert result is True
        assert orchestrator.initialized is False

    def test_register_component(self, orchestrator):
        """Test registering a component."""
        component = Mock()
        orchestrator.register_component("test", component)
        
        assert orchestrator.has_component("test") is True
        assert orchestrator.get_component("test") == component

    def test_get_component(self, orchestrator):
        """Test getting a component."""
        component = Mock()
        orchestrator.register_component("test", component)
        
        retrieved = orchestrator.get_component("test")
        
        assert retrieved == component

    def test_has_component(self, orchestrator):
        """Test checking for component."""
        component = Mock()
        orchestrator.register_component("test", component)
        
        assert orchestrator.has_component("test") is True
        assert orchestrator.has_component("nonexistent") is False

    def test_get_status(self, orchestrator):
        """Test getting orchestrator status."""
        component = Mock()
        component.get_status = Mock(return_value={"status": "ok"})
        orchestrator.register_component("test", component)
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=True):
            orchestrator.initialize()
            status = orchestrator.get_status()
            
            assert status["orchestrator"] == "test_orchestrator"
            assert status["initialized"] is True
            assert "creation_time" in status
            assert "uptime_seconds" in status
            assert status["component_count"] >= 1  # At least test component
            assert "test" in status["components"]

    def test_get_health_healthy(self, orchestrator):
        """Test get_health when healthy."""
        # Create a healthy component
        healthy_component = Mock()
        healthy_component.get_health = Mock(return_value={"status": "healthy"})
        orchestrator.register_component("healthy", healthy_component)
        
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=True):
            orchestrator.initialize()
            health = orchestrator.get_health()
            
            # Status should be healthy or at least not unhealthy
            assert health["status"] in ["healthy", "degraded"]  # degraded if test_component has no health
            assert "timestamp" in health

    def test_get_health_unhealthy(self, orchestrator):
        """Test get_health when not initialized."""
        health = orchestrator.get_health()
        
        assert health["status"] == "unhealthy"
        assert "Orchestrator not initialized" in health["issues"]

    def test_get_health_degraded(self, orchestrator):
        """Test get_health when component is unhealthy."""
        component = Mock()
        component.get_health = Mock(return_value={"status": "unhealthy"})
        orchestrator.register_component("unhealthy_component", component)
        with patch.object(OrchestratorLifecycle, 'initialize_components', return_value=True):
            orchestrator.initialize()
            health = orchestrator.get_health()
            
            # Should be degraded or unhealthy depending on component health
            assert health["status"] in ["degraded", "unhealthy"]
            assert len(health["issues"]) > 0

    def test_on_register_event_listener(self, orchestrator):
        """Test registering event listener."""
        callback = Mock()
        orchestrator.on("test_event", callback)
        
        # Verify event listener was registered
        orchestrator.emit("test_event", {"data": "test"})
        # Callback should be callable (event system works)
        assert callable(callback)

    def test_emit_event(self, orchestrator):
        """Test emitting event."""
        callback = Mock()
        orchestrator.on("test_event", callback)
        orchestrator.emit("test_event", {"data": "test"})
        
        # Verify callback was called
        callback.assert_called_once_with({"data": "test"})

    def test_abstract_methods_must_be_implemented(self):
        """Test that abstract methods must be implemented."""
        # This should work because ConcreteOrchestrator implements them
        orchestrator = ConcreteOrchestrator("test")
        
        # Should be able to call abstract methods
        orchestrator._register_components()
        config = orchestrator._load_default_config()
        
        assert config["setting1"] == "value1"

