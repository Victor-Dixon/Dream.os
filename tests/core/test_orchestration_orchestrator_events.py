"""
Unit tests for orchestration/orchestrator_events.py - MEDIUM PRIORITY

Tests OrchestratorEvents class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using importlib to bypass __init__.py chain
import importlib.util
events_path = project_root / "src" / "core" / "orchestration" / "orchestrator_events.py"
spec = importlib.util.spec_from_file_location("orchestrator_events", events_path)
orchestrator_events = importlib.util.module_from_spec(spec)
orchestrator_events.__package__ = 'src.core.orchestration'
spec.loader.exec_module(orchestrator_events)

OrchestratorEvents = orchestrator_events.OrchestratorEvents


class TestOrchestratorEvents:
    """Test suite for OrchestratorEvents class."""

    @pytest.fixture
    def events(self):
        """Create an OrchestratorEvents instance."""
        return OrchestratorEvents("test_orchestrator")

    @pytest.fixture
    def callback1(self):
        """Create a sample callback."""
        return Mock()

    @pytest.fixture
    def callback2(self):
        """Create another sample callback."""
        return Mock()

    def test_initialization(self, events):
        """Test OrchestratorEvents initialization."""
        assert events.orchestrator_name == "test_orchestrator"
        assert events._event_listeners == {}
        assert events.logger is not None

    def test_on_register_listener(self, events, callback1):
        """Test registering an event listener."""
        events.on("test_event", callback1)
        
        assert "test_event" in events._event_listeners
        assert callback1 in events._event_listeners["test_event"]

    def test_on_register_multiple_listeners(self, events, callback1, callback2):
        """Test registering multiple listeners for same event."""
        events.on("test_event", callback1)
        events.on("test_event", callback2)
        
        assert len(events._event_listeners["test_event"]) == 2
        assert callback1 in events._event_listeners["test_event"]
        assert callback2 in events._event_listeners["test_event"]

    def test_on_duplicate_listener(self, events, callback1):
        """Test registering same listener twice doesn't duplicate."""
        events.on("test_event", callback1)
        events.on("test_event", callback1)
        
        assert len(events._event_listeners["test_event"]) == 1
        assert callback1 in events._event_listeners["test_event"]

    def test_off_unregister_listener(self, events, callback1):
        """Test unregistering an event listener."""
        events.on("test_event", callback1)
        events.off("test_event", callback1)
        
        assert "test_event" not in events._event_listeners

    def test_off_removes_empty_event(self, events, callback1):
        """Test that off removes event when no listeners remain."""
        events.on("test_event", callback1)
        events.off("test_event", callback1)
        
        assert "test_event" not in events._event_listeners

    def test_off_keeps_other_listeners(self, events, callback1, callback2):
        """Test that off only removes specified listener."""
        events.on("test_event", callback1)
        events.on("test_event", callback2)
        events.off("test_event", callback1)
        
        assert callback2 in events._event_listeners["test_event"]
        assert callback1 not in events._event_listeners["test_event"]

    def test_emit_no_listeners(self, events):
        """Test emitting event with no listeners."""
        # Should not raise error
        events.emit("nonexistent_event", {"data": "test"})

    def test_emit_calls_listeners(self, events, callback1, callback2):
        """Test emitting event calls all listeners."""
        events.on("test_event", callback1)
        events.on("test_event", callback2)
        
        data = {"key": "value"}
        events.emit("test_event", data)
        
        callback1.assert_called_once_with(data)
        callback2.assert_called_once_with(data)

    def test_emit_with_none_data(self, events, callback1):
        """Test emitting event with None data."""
        events.on("test_event", callback1)
        
        events.emit("test_event", None)
        
        callback1.assert_called_once_with(None)

    def test_emit_handles_callback_error(self, events):
        """Test emit handles callback errors gracefully."""
        def failing_callback(data):
            raise Exception("Callback error")
        
        callback2 = Mock()
        
        events.on("test_event", failing_callback)
        events.on("test_event", callback2)
        
        # Should not raise, should call second callback
        events.emit("test_event", {"data": "test"})
        
        callback2.assert_called_once()

    def test_multiple_events(self, events, callback1, callback2):
        """Test managing multiple different events."""
        events.on("event1", callback1)
        events.on("event2", callback2)
        
        events.emit("event1", {"data": 1})
        events.emit("event2", {"data": 2})
        
        callback1.assert_called_once_with({"data": 1})
        callback2.assert_called_once_with({"data": 2})

    def test_off_nonexistent_event(self, events, callback1):
        """Test off with nonexistent event."""
        # Should not raise error
        events.off("nonexistent", callback1)

    def test_off_nonexistent_listener(self, events, callback1, callback2):
        """Test off with nonexistent listener."""
        events.on("test_event", callback1)
        events.off("test_event", callback2)  # callback2 not registered
        
        assert callback1 in events._event_listeners["test_event"]

