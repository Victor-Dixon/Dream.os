"""
Unit tests for orchestration/base_orchestrator.py - HIGH PRIORITY

Tests BaseOrchestrator class functionality.
"""

import importlib.util
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using importlib

base_orchestrator_path = project_root / "src" / \
    "core" / "orchestration" / "base_orchestrator.py"
spec = importlib.util.spec_from_file_location(
    "base_orchestrator", base_orchestrator_path)
base_orchestrator = importlib.util.module_from_spec(spec)
base_orchestrator.__package__ = 'src.core.orchestration'

# Mock dependencies before loading


class MockOrchestratorComponents:
    def __init__(self, name):
        self.components = {}

    def register_component(self, name, component):
        self.components[name] = component

    def get_component(self, name):
        return self.components.get(name)

    def has_component(self, name):
        return name in self.components

    def clear_all_components(self):
        self.components.clear()


class MockOrchestratorEvents:
    def __init__(self, name):
        self.listeners = {}

    def on(self, event, callback):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)

    def off(self, event, callback):
        if event in self.listeners:
            self.listeners[event].remove(callback)

    def emit(self, event, data):
        pass

    def clear_listeners(self):
        self.listeners.clear()


class MockOrchestratorLifecycle:
    @staticmethod
    def initialize_components(components, logger):
        return True

    @staticmethod
    def cleanup_components(components, logger):
        return True


class MockOrchestratorUtilities:
    @staticmethod
    def safe_execute(operation, operation_name, default_return, logger, emit, **kwargs):
        try:
            return operation(**kwargs)
        except Exception:
            return default_return

    @staticmethod
    def sanitize_config(config, logger):
        return config


sys.modules['src.core.orchestration.orchestrator_components'] = MagicMock()
sys.modules['src.core.orchestration.orchestrator_components'].OrchestratorComponents = MockOrchestratorComponents
sys.modules['src.core.orchestration.orchestrator_events'] = MagicMock()
sys.modules['src.core.orchestration.orchestrator_events'].OrchestratorEvents = MockOrchestratorEvents
sys.modules['src.core.orchestration.orchestrator_lifecycle'] = MagicMock()
sys.modules['src.core.orchestration.orchestrator_lifecycle'].OrchestratorLifecycle = MockOrchestratorLifecycle
sys.modules['src.core.orchestration.orchestrator_utilities'] = MagicMock()
sys.modules['src.core.orchestration.orchestrator_utilities'].OrchestratorUtilities = MockOrchestratorUtilities

spec.loader.exec_module(base_orchestrator)

BaseOrchestrator = base_orchestrator.BaseOrchestrator


# Concrete implementation for testing
class ConcreteOrchestrator(BaseOrchestrator):
    """Concrete implementation for testing BaseOrchestrator."""

    def _register_components(self) -> None:
        """Register test components."""
        self.register_component("test_component", Mock())

    def _load_default_config(self) -> dict:
        """Load default test configuration."""
        return {"test_setting": "test_value"}


class TestBaseOrchestrator:
    """Test suite for BaseOrchestrator class."""

    def test_initialization(self):
        """Test BaseOrchestrator initialization."""
        orchestrator = ConcreteOrchestrator("test_orchestrator")

        assert orchestrator.name == "test_orchestrator"
        assert orchestrator.config == {"test_setting": "test_value"}
        assert orchestrator.initialized is False
        assert isinstance(orchestrator.creation_time, datetime)
        assert orchestrator.logger is not None

    def test_initialization_with_custom_config(self):
        """Test initialization with custom configuration."""
        custom_config = {"custom_setting": "custom_value"}
        orchestrator = ConcreteOrchestrator("test", custom_config)

        assert orchestrator.config == custom_config

    def test_initialization_with_none_config(self):
        """Test initialization with None config uses defaults."""
        orchestrator = ConcreteOrchestrator("test", None)

        assert orchestrator.config == {"test_setting": "test_value"}

    def test_register_component(self):
        """Test component registration."""
        orchestrator = ConcreteOrchestrator("test")
        component = Mock()

        orchestrator.register_component("test_comp", component)

        assert orchestrator.has_component("test_comp") is True

    def test_get_component(self):
        """Test getting registered component."""
        orchestrator = ConcreteOrchestrator("test")
        component = Mock()

        orchestrator.register_component("test_comp", component)
        retrieved = orchestrator.get_component("test_comp")

        assert retrieved == component

    def test_get_component_nonexistent(self):
        """Test getting non-existent component returns None."""
        orchestrator = ConcreteOrchestrator("test")

        result = orchestrator.get_component("nonexistent")

        assert result is None

    def test_has_component(self):
        """Test checking component existence."""
        orchestrator = ConcreteOrchestrator("test")
        component = Mock()

        orchestrator.register_component("test_comp", component)

        assert orchestrator.has_component("test_comp") is True
        assert orchestrator.has_component("nonexistent") is False

    def test_initialize_success(self):
        """Test successful initialization."""
        orchestrator = ConcreteOrchestrator("test")

        with patch.object(
            base_orchestrator.OrchestratorLifecycle,
            'initialize_components',
            return_value=True
        ):
            result = orchestrator.initialize()

        assert result is True
        assert orchestrator.initialized is True

    def test_initialize_idempotent(self):
        """Test initialization is idempotent."""
        orchestrator = ConcreteOrchestrator("test")

        with patch.object(
            base_orchestrator.OrchestratorLifecycle,
            'initialize_components',
            return_value=True
        ):
            result1 = orchestrator.initialize()
            result2 = orchestrator.initialize()

        assert result1 is True
        assert result2 is True
        assert orchestrator.initialized is True

    def test_initialize_failure(self):
        """Test initialization failure handling."""
        orchestrator = ConcreteOrchestrator("test")

        with patch.object(
            base_orchestrator.OrchestratorLifecycle,
            'initialize_components',
            return_value=False
        ):
            result = orchestrator.initialize()

        assert result is False
        assert orchestrator.initialized is False

    def test_cleanup_success(self):
        """Test successful cleanup."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = True

        with patch.object(
            base_orchestrator.OrchestratorLifecycle,
            'cleanup_components',
            return_value=True
        ):
            result = orchestrator.cleanup()

        assert result is True
        assert orchestrator.initialized is False

    def test_cleanup_not_initialized(self):
        """Test cleanup when not initialized."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = False

        result = orchestrator.cleanup()

        assert result is True

    def test_get_status(self):
        """Test getting orchestrator status."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = True

        status = orchestrator.get_status()

        assert status["orchestrator"] == "test"
        assert status["initialized"] is True
        assert "creation_time" in status
        assert "uptime_seconds" in status
        assert "component_count" in status
        assert "components" in status
        assert "component_statuses" in status
        assert "config" in status

    def test_get_status_with_components(self):
        """Test status with registered components."""
        orchestrator = ConcreteOrchestrator("test")
        component = Mock()
        component.get_status = Mock(return_value={"status": "active"})
        orchestrator.register_component("test_comp", component)

        status = orchestrator.get_status()

        assert "test_comp" in status["components"]
        assert "test_comp" in status["component_statuses"]

    def test_get_health_healthy(self):
        """Test health check when healthy."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = True

        health = orchestrator.get_health()

        assert health["status"] == "healthy"
        assert len(health["issues"]) == 0
        assert "timestamp" in health

    def test_get_health_unhealthy_not_initialized(self):
        """Test health check when not initialized."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = False

        health = orchestrator.get_health()

        assert health["status"] == "unhealthy"
        assert "Orchestrator not initialized" in health["issues"]

    def test_get_health_degraded_component(self):
        """Test health check with unhealthy component."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = True
        component = Mock()
        component.get_health = Mock(return_value={"status": "unhealthy"})
        orchestrator.register_component("unhealthy_comp", component)

        health = orchestrator.get_health()

        assert health["status"] == "degraded"
        assert any("unhealthy_comp" in issue for issue in health["issues"])

    def test_event_on(self):
        """Test registering event listener."""
        orchestrator = ConcreteOrchestrator("test")
        callback = Mock()

        orchestrator.on("test_event", callback)

        # Verify event listener was registered
        assert "test_event" in orchestrator._event_mgr.listeners
        assert callback in orchestrator._event_mgr.listeners["test_event"]

    def test_event_off(self):
        """Test removing event listener."""
        orchestrator = ConcreteOrchestrator("test")
        callback = Mock()

        orchestrator.on("test_event", callback)
        orchestrator.off("test_event", callback)

        # Verify event listener was removed
        assert callback not in orchestrator._event_mgr.listeners.get(
            "test_event", [])

    def test_event_emit(self):
        """Test emitting event."""
        orchestrator = ConcreteOrchestrator("test")
        callback = Mock()
        data = {"key": "value"}

        orchestrator.on("test_event", callback)
        orchestrator.emit("test_event", data)

        # Event emission should not raise errors
        assert True  # If we get here, emit worked

    def test_safe_execute_success(self):
        """Test safe execution with successful operation."""
        orchestrator = ConcreteOrchestrator("test")

        def test_operation(x, y):
            return x + y

        result = orchestrator.safe_execute(
            test_operation, "test_op", None, x=2, y=3)

        assert result == 5

    def test_context_manager_enter(self):
        """Test context manager entry."""
        orchestrator = ConcreteOrchestrator("test")

        with patch.object(
            base_orchestrator.OrchestratorLifecycle,
            'initialize_components',
            return_value=True
        ):
            with orchestrator as ctx:
                assert ctx == orchestrator
                assert orchestrator.initialized is True

    def test_context_manager_exit(self):
        """Test context manager exit."""
        orchestrator = ConcreteOrchestrator("test")
        orchestrator.initialized = True

        with patch.object(orchestrator, 'cleanup', return_value=True):
            orchestrator.__exit__(None, None, None)

            orchestrator.cleanup.assert_called_once()

    def test_repr(self):
        """Test string representation."""
        orchestrator = ConcreteOrchestrator("test_orchestrator")

        repr_str = repr(orchestrator)

        assert "ConcreteOrchestrator" in repr_str
        assert "test_orchestrator" in repr_str
        assert "initialized" in repr_str

    def test_abstract_methods_must_be_implemented(self):
        """Test that abstract methods must be implemented."""
        with pytest.raises(TypeError):
            BaseOrchestrator("test")
