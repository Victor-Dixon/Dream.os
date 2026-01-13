"""
Tests for Message Bus Port Interface
====================================

Tests for src/domain/ports/message_bus.py following repository pattern.

V2 Compliance: < 300 lines, ≥85% coverage.
"""

import pytest
from typing import Any, Dict
from unittest.mock import Mock, MagicMock

from src.domain.ports.message_bus import MessageBus


class MockMessageBus(MessageBus):
    """Mock implementation of MessageBus interface for testing."""
    
    def __init__(self):
        self._subscribers: Dict[str, Dict[str, Any]] = {}
        self._event_count = 0
        self._available = True
    
    def publish(
        self,
        event_type: str,
        event_data: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Publish event."""
        if not event_type or not event_type.strip():
            raise ValueError("Event type cannot be empty")
        if not isinstance(event_data, dict):
            raise ValueError("Event data must be a dictionary")
        if not self._available:
            raise RuntimeError("Message bus not available")
        
        self._event_count += 1
        
        # Notify subscribers
        handlers = self._subscribers.get(event_type, {})
        wildcard_handlers = self._subscribers.get("*", {})
        
        for handler_id, handler_info in {**handlers, **wildcard_handlers}.items():
            handler = handler_info["handler"]
            try:
                handler(event_type, event_data)
            except Exception:
                pass  # Handler errors shouldn't break publish
        
        return True
    
    def subscribe(
        self,
        event_type: str,
        handler: Any,
        handler_id: str = None
    ) -> str:
        """Subscribe to events."""
        if not event_type or not event_type.strip():
            raise ValueError("Event type cannot be empty")
        if not callable(handler):
            raise ValueError("Handler must be callable")
        
        if handler_id is None:
            handler_id = f"handler_{len(self._subscribers.get(event_type, {}))}"
        
        if event_type not in self._subscribers:
            self._subscribers[event_type] = {}
        
        self._subscribers[event_type][handler_id] = {
            "handler": handler,
            "event_type": event_type
        }
        
        return handler_id
    
    def unsubscribe(self, handler_id: str) -> bool:
        """Unsubscribe handler."""
        if not handler_id or not handler_id.strip():
            raise ValueError("Handler ID cannot be empty")
        
        for event_type in self._subscribers:
            if handler_id in self._subscribers[event_type]:
                del self._subscribers[event_type][handler_id]
                return True
        
        return False
    
    def get_subscribers(self, event_type: str = None) -> Dict[str, list[str]]:
        """Get subscribers."""
        if event_type:
            handlers = self._subscribers.get(event_type, {})
            return {event_type: list(handlers.keys())}
        else:
            return {
                et: list(handlers.keys())
                for et, handlers in self._subscribers.items()
            }
    
    def is_available(self) -> bool:
        """Check if available."""
        return self._available
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        total_handlers = sum(
            len(handlers) for handlers in self._subscribers.values()
        )
        return {
            "total_events": self._event_count,
            "subscribers_count": total_handlers,
            "event_types": list(self._subscribers.keys()),
            "available": self._available
        }


class TestMessageBusPort:
    """Test suite for MessageBus port interface."""
    
    def test_publish_event_success(self):
        """Test publishing event successfully."""
        bus = MockMessageBus()
        result = bus.publish("test.event", {"data": "value"})
        assert result is True
        assert bus.get_stats()["total_events"] == 1
    
    def test_publish_event_empty_type_raises_error(self):
        """Test that empty event type raises ValueError."""
        bus = MockMessageBus()
        with pytest.raises(ValueError, match="Event type cannot be empty"):
            bus.publish("", {"data": "value"})
    
    def test_publish_event_invalid_data_raises_error(self):
        """Test that invalid event data raises ValueError."""
        bus = MockMessageBus()
        with pytest.raises(ValueError, match="Event data must be a dictionary"):
            bus.publish("test.event", "not-a-dict")
    
    def test_publish_event_with_metadata(self):
        """Test publishing event with metadata."""
        bus = MockMessageBus()
        result = bus.publish(
            "test.event",
            {"data": "value"},
            metadata={"source": "test"}
        )
        assert result is True
    
    def test_subscribe_success(self):
        """Test subscribing to events."""
        bus = MockMessageBus()
        handler = Mock()
        handler_id = bus.subscribe("test.event", handler)
        assert handler_id is not None
        assert handler_id in bus.get_subscribers("test.event")["test.event"]
    
    def test_subscribe_with_custom_id(self):
        """Test subscribing with custom handler ID."""
        bus = MockMessageBus()
        handler = Mock()
        handler_id = bus.subscribe("test.event", handler, handler_id="custom-id")
        assert handler_id == "custom-id"
        assert "custom-id" in bus.get_subscribers("test.event")["test.event"]
    
    def test_subscribe_empty_event_type_raises_error(self):
        """Test that empty event type raises ValueError."""
        bus = MockMessageBus()
        handler = Mock()
        with pytest.raises(ValueError, match="Event type cannot be empty"):
            bus.subscribe("", handler)
    
    def test_subscribe_non_callable_handler_raises_error(self):
        """Test that non-callable handler raises ValueError."""
        bus = MockMessageBus()
        with pytest.raises(ValueError, match="Handler must be callable"):
            bus.subscribe("test.event", "not-callable")
    
    def test_subscribe_wildcard_events(self):
        """Test subscribing to all events with wildcard."""
        bus = MockMessageBus()
        handler = Mock()
        handler_id = bus.subscribe("*", handler)
        assert handler_id is not None
        
        # Publish event - wildcard handler should receive it
        bus.publish("test.event", {"data": "value"})
        handler.assert_called_once()
    
    def test_unsubscribe_success(self):
        """Test unsubscribing handler."""
        bus = MockMessageBus()
        handler = Mock()
        handler_id = bus.subscribe("test.event", handler)
        result = bus.unsubscribe(handler_id)
        assert result is True
        assert handler_id not in bus.get_subscribers("test.event")["test.event"]
    
    def test_unsubscribe_not_found_returns_false(self):
        """Test unsubscribing non-existent handler returns False."""
        bus = MockMessageBus()
        result = bus.unsubscribe("non-existent")
        assert result is False
    
    def test_unsubscribe_empty_id_raises_error(self):
        """Test that empty handler ID raises ValueError."""
        bus = MockMessageBus()
        with pytest.raises(ValueError, match="Handler ID cannot be empty"):
            bus.unsubscribe("")
    
    def test_get_subscribers_specific_event(self):
        """Test getting subscribers for specific event type."""
        bus = MockMessageBus()
        handler1 = Mock()
        handler2 = Mock()
        bus.subscribe("test.event", handler1, "handler-1")
        bus.subscribe("test.event", handler2, "handler-2")
        bus.subscribe("other.event", Mock(), "handler-3")
        
        subscribers = bus.get_subscribers("test.event")
        assert "test.event" in subscribers
        assert len(subscribers["test.event"]) == 2
        assert "handler-1" in subscribers["test.event"]
        assert "handler-2" in subscribers["test.event"]
    
    def test_get_subscribers_all_events(self):
        """Test getting subscribers for all events."""
        bus = MockMessageBus()
        bus.subscribe("test.event", Mock(), "handler-1")
        bus.subscribe("other.event", Mock(), "handler-2")
        
        subscribers = bus.get_subscribers()
        assert "test.event" in subscribers
        assert "other.event" in subscribers
    
    def test_is_available_returns_true(self):
        """Test is_available returns True when available."""
        bus = MockMessageBus()
        assert bus.is_available() is True
    
    def test_is_available_returns_false(self):
        """Test is_available returns False when not available."""
        bus = MockMessageBus()
        bus._available = False
        assert bus.is_available() is False
    
    def test_publish_when_not_available_raises_error(self):
        """Test that publishing when not available raises RuntimeError."""
        bus = MockMessageBus()
        bus._available = False
        with pytest.raises(RuntimeError, match="Message bus not available"):
            bus.publish("test.event", {"data": "value"})
    
    def test_get_stats_returns_correct_data(self):
        """Test get_stats returns correct statistics."""
        bus = MockMessageBus()
        bus.subscribe("test.event", Mock(), "handler-1")
        bus.publish("test.event", {"data": "value"})
        
        stats = bus.get_stats()
        assert stats["total_events"] == 1
        assert stats["subscribers_count"] == 1
        assert "test.event" in stats["event_types"]
        assert stats["available"] is True
    
    def test_publish_notifies_subscribers(self):
        """Test that publishing notifies all subscribers."""
        bus = MockMessageBus()
        handler1 = Mock()
        handler2 = Mock()
        bus.subscribe("test.event", handler1, "handler-1")
        bus.subscribe("test.event", handler2, "handler-2")
        
        bus.publish("test.event", {"data": "value"})
        
        handler1.assert_called_once_with("test.event", {"data": "value"})
        handler2.assert_called_once_with("test.event", {"data": "value"})


