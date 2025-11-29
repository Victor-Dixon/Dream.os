"""
Tests for protocol/message_router.py

Comprehensive tests for message routing, protocol handling, and route optimization.
Target: 12+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from src.services.protocol.message_router import MessageRouter
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)
from src.services.protocol.messaging_protocol_models import (
    OptimizationConfig,
    ProtocolOptimizationStrategy,
    MessageRoute,
    RouteOptimization,
    create_default_config,
)


class TestMessageRouter:
    """Tests for MessageRouter class."""

    def test_initialization_default_config(self):
        """Test router initialization with default config."""
        router = MessageRouter()
        assert router.config is not None
        assert router.analyzer is not None
        assert router.route_cache == {}
        assert router.failed_routes == {}

    def test_initialization_custom_config(self):
        """Test router initialization with custom config."""
        config = create_default_config()
        router = MessageRouter(config)
        assert router.config == config

    def test_route_message_urgent_priority(self):
        """Test routing message with urgent priority."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="urgent test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router.analyzer, 'analyze_route_options') as mock_analyze:
            mock_analyze.return_value = MessageRoute.DIRECT
            route = router.route_message(message)
            
            assert route == MessageRoute.DIRECT
            # Should add ROUTE_OPTIMIZATION strategy for urgent
            call_args = mock_analyze.call_args
            strategies = call_args[0][1]
            assert ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION in strategies

    def test_route_message_broadcast_type(self):
        """Test routing broadcast message."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="broadcast test",
            sender="Agent-1",
            recipient="all",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router.analyzer, 'analyze_route_options') as mock_analyze:
            mock_analyze.return_value = MessageRoute.BATCH
            route = router.route_message(message)
            
            assert route == MessageRoute.BATCH
            # Should add MESSAGE_BATCHING strategy for broadcast
            call_args = mock_analyze.call_args
            strategies = call_args[0][1]
            assert ProtocolOptimizationStrategy.MESSAGE_BATCHING in strategies

    def test_route_message_with_custom_strategies(self):
        """Test routing message with custom strategies."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        custom_strategies = [ProtocolOptimizationStrategy.CACHE_OPTIMIZATION]
        
        with patch.object(router.analyzer, 'analyze_route_options') as mock_analyze:
            mock_analyze.return_value = MessageRoute.DIRECT
            route = router.route_message(message, strategies=custom_strategies)
            
            assert route == MessageRoute.DIRECT
            # Should include custom strategies
            call_args = mock_analyze.call_args
            strategies = call_args[0][1]
            assert ProtocolOptimizationStrategy.CACHE_OPTIMIZATION in strategies

    def test_route_message_regular_priority(self):
        """Test routing message with regular priority."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="regular test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router.analyzer, 'analyze_route_options') as mock_analyze:
            mock_analyze.return_value = MessageRoute.DIRECT
            route = router.route_message(message)
            
            assert route == MessageRoute.DIRECT
            # Regular priority should not add urgent strategies
            call_args = mock_analyze.call_args
            strategies = call_args[0][1]
            assert ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION not in strategies

    def test_route_with_priority_override(self):
        """Test routing with priority override."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router, 'route_message') as mock_route:
            mock_route.return_value = MessageRoute.DIRECT
            route = router.route_with_priority(message, UnifiedMessagePriority.URGENT)
            
            assert route == MessageRoute.DIRECT
            # Message priority should be overridden
            assert message.priority == UnifiedMessagePriority.URGENT

    def test_route_with_priority_override_none(self):
        """Test routing with no priority override."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        original_priority = message.priority
        
        with patch.object(router, 'route_message') as mock_route:
            mock_route.return_value = MessageRoute.DIRECT
            route = router.route_with_priority(message, None)
            
            assert route == MessageRoute.DIRECT
            # Priority should remain unchanged
            assert message.priority == original_priority

    def test_route_with_strategy(self):
        """Test routing with specific strategy."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router, 'route_message') as mock_route:
            mock_route.return_value = MessageRoute.DIRECT
            route = router.route_with_strategy(message, ProtocolOptimizationStrategy.CACHE_OPTIMIZATION)
            
            assert route == MessageRoute.DIRECT
            # Should call route_message with specific strategy
            mock_route.assert_called_once_with(message, strategies=[ProtocolOptimizationStrategy.CACHE_OPTIMIZATION])

    def test_update_route_performance(self):
        """Test updating route performance metrics."""
        router = MessageRouter()
        
        with patch.object(router.analyzer, 'update_route_performance') as mock_update:
            router.update_route_performance("route_key", 100.5, True)
            
            mock_update.assert_called_once_with("route_key", 100.5, True)

    def test_get_router_status(self):
        """Test getting router status."""
        router = MessageRouter()
        router.route_cache["route1"] = RouteOptimization()
        router.failed_routes["route2"] = None
        
        with patch.object(router.analyzer, 'get_analyzer_status') as mock_status:
            mock_status.return_value = {"status": "active"}
            status = router.get_router_status()
            
            assert "analyzer_status" in status
            assert status["cached_routes"] == 1
            assert status["failed_routes"] == 1

    def test_route_message_logs_info(self):
        """Test that route_message logs info."""
        router = MessageRouter()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router.analyzer, 'analyze_route_options') as mock_analyze, \
             patch('src.services.protocol.message_router.logger') as mock_logger:
            mock_analyze.return_value = MessageRoute.DIRECT
            router.route_message(message)
            
            # Should log routing info
            assert mock_logger.info.called

    def test_route_message_uses_cache_and_failed_routes(self):
        """Test that route_message passes cache and failed_routes to analyzer."""
        router = MessageRouter()
        router.route_cache["cached"] = RouteOptimization()
        router.failed_routes["failed"] = None
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(router.analyzer, 'analyze_route_options') as mock_analyze:
            mock_analyze.return_value = MessageRoute.DIRECT
            router.route_message(message)
            
            # Should pass cache and failed_routes
            call_args = mock_analyze.call_args
            assert call_args[0][2] == router.route_cache
            assert call_args[0][3] == router.failed_routes

