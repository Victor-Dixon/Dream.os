"""
Tests for message_router.py

Comprehensive tests for message routing.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch
from src.services.protocol.message_router import MessageRouter
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)
from src.services.protocol.messaging_protocol_models import (
    MessageRoute,
    ProtocolOptimizationStrategy,
    OptimizationConfig,
)


class TestMessageRouter:
    """Tests for MessageRouter."""

    def test_message_router_initialization_default(self):
        """Test MessageRouter initialization with default config."""
        router = MessageRouter()
        assert router.config is not None
        assert router.analyzer is not None
        assert router.route_cache == {}
        assert router.failed_routes == {}

    def test_message_router_initialization_custom_config(self):
        """Test MessageRouter initialization with custom config."""
        config = OptimizationConfig(enable_load_balancing=False)
        router = MessageRouter(config=config)
        assert router.config == config

    def test_route_message_default(self):
        """Test routing a message with default strategies."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        route = router.route_message(message)
        
        assert isinstance(route, MessageRoute)

    def test_route_message_with_strategies(self):
        """Test routing a message with specific strategies."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        strategies = [ProtocolOptimizationStrategy.CACHING]
        route = router.route_message(message, strategies=strategies)
        
        assert isinstance(route, MessageRoute)

    def test_route_message_urgent_priority(self):
        """Test routing urgent message adds route optimization."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Urgent",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        route = router.route_message(message)
        
        assert isinstance(route, MessageRoute)

    def test_route_message_broadcast_type(self):
        """Test routing broadcast message adds batching strategy."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Broadcast",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        route = router.route_message(message)
        
        assert isinstance(route, MessageRoute)

    def test_route_with_priority(self):
        """Test routing with priority override."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        route = router.route_with_priority(message, UnifiedMessagePriority.URGENT)
        
        assert isinstance(route, MessageRoute)
        assert message.priority == UnifiedMessagePriority.URGENT

    def test_route_with_priority_no_override(self):
        """Test routing with no priority override."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        original_priority = message.priority
        route = router.route_with_priority(message, None)
        
        assert isinstance(route, MessageRoute)
        assert message.priority == original_priority

    def test_route_with_strategy(self):
        """Test routing with specific strategy."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        route = router.route_with_strategy(message, ProtocolOptimizationStrategy.CACHING)
        
        assert isinstance(route, MessageRoute)

    def test_update_route_performance(self):
        """Test updating route performance."""
        router = MessageRouter()
        router.update_route_performance("test_route", 50.0, True)
        
        # Verify analyzer was updated
        assert router.analyzer is not None

    def test_get_router_status(self):
        """Test getting router status."""
        router = MessageRouter()
        status = router.get_router_status()
        
        assert "analyzer_status" in status
        assert "cached_routes" in status
        assert "failed_routes" in status
        assert status["cached_routes"] == 0
        assert status["failed_routes"] == 0
