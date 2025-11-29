"""
Tests for route_analyzer.py

Comprehensive tests for route analysis and scoring.
Target: ≥85% coverage

Note: route_analyzer has import dependencies that prevent direct testing.
Tests use mocking to work around missing protocol models.
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime
import sys
from pathlib import Path

# Import directly from file to avoid __init__.py issues
route_analyzer_path = Path(__file__).parent.parent.parent.parent / "src" / "services" / "protocol" / "routers" / "route_analyzer.py"
spec = __import__('importlib.util', fromlist=['spec_from_file_location']).spec_from_file_location(
    "route_analyzer", route_analyzer_path
)
route_analyzer = __import__('importlib.util', fromlist=['module_from_spec']).module_from_spec(spec)

# Mock the missing imports before loading
with patch.dict('sys.modules', {
    'src.services.messaging_protocol_models': MagicMock(),
    'src.services.protocol.messaging_protocol_models': MagicMock(),
}):
    spec.loader.exec_module(route_analyzer)

RouteAnalyzer = route_analyzer.RouteAnalyzer

from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)


# Mock the missing protocol models
class MockMessageRoute:
    """Mock MessageRoute enum."""
    CACHED = "cached"
    DIRECT = "direct"
    OPTIMIZED = "optimized"
    BATCHED = "batched"
    LOAD_BALANCED = "load_balanced"
    QUEUED = "queued"


class MockProtocolOptimizationStrategy:
    """Mock ProtocolOptimizationStrategy enum."""
    ROUTE_OPTIMIZATION = "route_optimization"
    MESSAGE_BATCHING = "message_batching"
    LOAD_BALANCING = "load_balancing"
    CACHING = "caching"


class MockRouteOptimization:
    """Mock RouteOptimization dataclass."""
    def __init__(self, success_rate=1.0, latency_ms=50.0):
        self.success_rate = success_rate
        self.latency_ms = latency_ms


class MockOptimizationConfig:
    """Mock OptimizationConfig."""
    def __init__(self, enable_load_balancing=True):
        self.enable_load_balancing = enable_load_balancing


def mock_create_default_config():
    """Mock create_default_config function."""
    return MockOptimizationConfig()


ROUTE_PRIORITY_ORDER = [
    MockMessageRoute.CACHED,
    MockMessageRoute.DIRECT,
    MockMessageRoute.OPTIMIZED,
    MockMessageRoute.BATCHED,
    MockMessageRoute.LOAD_BALANCED,
    MockMessageRoute.QUEUED,
]


@patch('src.services.protocol.routers.route_analyzer.MessageRoute', MockMessageRoute)
@patch('src.services.protocol.routers.route_analyzer.ProtocolOptimizationStrategy', MockProtocolOptimizationStrategy)
@patch('src.services.protocol.routers.route_analyzer.RouteOptimization', MockRouteOptimization)
@patch('src.services.protocol.routers.route_analyzer.OptimizationConfig', MockOptimizationConfig)
@patch('src.services.protocol.routers.route_analyzer.create_default_config', mock_create_default_config)
@patch('src.services.protocol.routers.route_analyzer.ROUTE_PRIORITY_ORDER', ROUTE_PRIORITY_ORDER)
class TestRouteAnalyzer:
    """Tests for RouteAnalyzer."""

    def test_initialization_default_config(self):
        """Test analyzer initialization with default config."""
        analyzer = RouteAnalyzer()
        assert analyzer.config is not None
        assert analyzer.route_performance == {}
        assert analyzer.route_usage_counts == {}

    def test_initialization_custom_config(self):
        """Test analyzer initialization with custom config."""
        config = MockOptimizationConfig(enable_load_balancing=False)
        analyzer = RouteAnalyzer(config=config)
        assert analyzer.config == config

    def test_analyze_route_options_urgent_direct(self):
        """Test route analysis for urgent message without optimization."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Urgent",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        result = analyzer.analyze_route_options(
            message,
            strategies=[],
            route_cache={},
            failed_routes={},
        )
        
        assert result == MockMessageRoute.DIRECT

    def test_analyze_route_options_urgent_with_optimization(self):
        """Test route analysis for urgent message with route optimization."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Urgent",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        # Mock performance data for fast route
        route_key = analyzer._generate_route_key(message)
        analyzer.route_performance[route_key] = [50.0, 60.0, 55.0]  # < 100ms average
        
        result = analyzer.analyze_route_options(
            message,
            strategies=[MockProtocolOptimizationStrategy.ROUTE_OPTIMIZATION],
            route_cache={},
            failed_routes={},
        )
        
        assert result == MockMessageRoute.DIRECT

    def test_analyze_route_options_urgent_with_cache(self):
        """Test route analysis for urgent message with cached route."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Urgent",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        route_key = analyzer._generate_route_key(message)
        analyzer.route_performance[route_key] = [50.0]
        route_cache = {route_key: MockRouteOptimization()}
        
        result = analyzer.analyze_route_options(
            message,
            strategies=[MockProtocolOptimizationStrategy.ROUTE_OPTIMIZATION],
            route_cache=route_cache,
            failed_routes={},
        )
        
        assert result == MockMessageRoute.CACHED

    def test_analyze_route_options_regular_priority(self):
        """Test route analysis for regular priority message."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Regular",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = analyzer.analyze_route_options(
            message,
            strategies=[],
            route_cache={},
            failed_routes={},
        )
        
        # Should select highest scoring route (CACHED with base score 10.0)
        assert result in [MockMessageRoute.CACHED, MockMessageRoute.DIRECT]

    def test_calculate_route_score_base_scores(self):
        """Test route score calculation with base scores."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        score = analyzer._calculate_route_score(
            message,
            MockMessageRoute.CACHED,
            strategies=[],
            route_cache={},
            failed_routes={},
        )
        
        assert score >= 10.0  # Base score for CACHED

    def test_calculate_route_score_batching_bonus(self):
        """Test route score with message batching bonus."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        score = analyzer._calculate_route_score(
            message,
            MockMessageRoute.BATCHED,
            strategies=[MockProtocolOptimizationStrategy.MESSAGE_BATCHING],
            route_cache={},
            failed_routes={},
        )
        
        assert score >= 9.0  # Base 6.0 + bonus 3.0

    def test_calculate_route_score_load_balancing_bonus(self):
        """Test route score with load balancing bonus."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        score = analyzer._calculate_route_score(
            message,
            MockMessageRoute.LOAD_BALANCED,
            strategies=[MockProtocolOptimizationStrategy.LOAD_BALANCING],
            route_cache={},
            failed_routes={},
        )
        
        assert score >= 7.0  # Base 5.0 + bonus 2.0

    def test_calculate_route_score_caching_bonus(self):
        """Test route score with caching bonus."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        score = analyzer._calculate_route_score(
            message,
            MockMessageRoute.CACHED,
            strategies=[MockProtocolOptimizationStrategy.CACHING],
            route_cache={},
            failed_routes={},
        )
        
        assert score >= 14.0  # Base 10.0 + bonus 4.0

    def test_calculate_route_score_with_cache_performance(self):
        """Test route score with route cache performance data."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        route_key = analyzer._generate_route_key(message)
        route_cache = {
            route_key: MockRouteOptimization(success_rate=0.95, latency_ms=30.0)
        }
        
        score = analyzer._calculate_route_score(
            message,
            MockMessageRoute.CACHED,
            strategies=[],
            route_cache=route_cache,
            failed_routes={},
        )
        
        # Should have performance adjustments
        assert score > 10.0

    def test_calculate_route_score_load_balancing_adjustment(self):
        """Test route score with load balancing adjustment."""
        analyzer = RouteAnalyzer()
        analyzer.config.enable_load_balancing = True
        analyzer.route_usage_counts[MockMessageRoute.DIRECT] = 50
        
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        score = analyzer._calculate_route_score(
            message,
            MockMessageRoute.DIRECT,
            strategies=[],
            route_cache={},
            failed_routes={},
        )
        
        # Should have load balancing adjustment
        assert score >= 8.0

    def test_generate_route_key(self):
        """Test route key generation."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        key = analyzer._generate_route_key(message)
        
        assert "Agent-1" in key
        assert "Agent-2" in key
        assert "regular" in key
        # Note: message.type.value - checking format (sender:recipient:priority:type)
        assert key.count(":") == 3

    def test_update_route_performance(self):
        """Test updating route performance."""
        analyzer = RouteAnalyzer()
        analyzer.update_route_performance("test_route", 50.0, True)
        
        assert "test_route" in analyzer.route_performance
        assert 50.0 in analyzer.route_performance["test_route"]

    def test_update_route_performance_limit(self):
        """Test route performance data limit."""
        analyzer = RouteAnalyzer()
        # Add more than 1000 entries
        for i in range(1001):
            analyzer.update_route_performance("test_route", float(i), True)
        
        # Should be limited to 500
        assert len(analyzer.route_performance["test_route"]) <= 500

    def test_update_route_performance_usage_count(self):
        """Test route usage count update."""
        analyzer = RouteAnalyzer()
        analyzer.update_route_performance("Agent-1:Agent-2:regular:text", 50.0, True)
        
        # Usage count should be updated
        assert len(analyzer.route_usage_counts) > 0

    def test_get_route_performance_summary(self):
        """Test getting route performance summary."""
        analyzer = RouteAnalyzer()
        analyzer.update_route_performance("route1", 50.0, True)
        analyzer.update_route_performance("route1", 60.0, True)
        analyzer.update_route_performance("route1", 55.0, True)
        
        summary = analyzer.get_route_performance_summary()
        
        assert "route1" in summary
        assert summary["route1"]["average_latency_ms"] == pytest.approx(55.0)
        assert summary["route1"]["min_latency_ms"] == 50.0
        assert summary["route1"]["max_latency_ms"] == 60.0
        assert summary["route1"]["sample_count"] == 3

    def test_get_route_performance_summary_empty(self):
        """Test getting performance summary with no data."""
        analyzer = RouteAnalyzer()
        summary = analyzer.get_route_performance_summary()
        
        assert summary == {}

    def test_get_route_usage_stats(self):
        """Test getting route usage statistics."""
        analyzer = RouteAnalyzer()
        analyzer.update_route_performance("route1", 50.0, True)
        analyzer.update_route_performance("route2", 60.0, True)
        
        stats = analyzer.get_route_usage_stats()
        
        assert isinstance(stats, dict)
        # Should be a copy, not the same object
        assert stats is not analyzer.route_usage_counts

    def test_clear_performance_data(self):
        """Test clearing performance data."""
        analyzer = RouteAnalyzer()
        analyzer.update_route_performance("route1", 50.0, True)
        analyzer.update_route_performance("route2", 60.0, True)
        
        analyzer.clear_performance_data()
        
        assert len(analyzer.route_performance) == 0
        assert len(analyzer.route_usage_counts) == 0

    def test_get_analyzer_status(self):
        """Test getting analyzer status."""
        analyzer = RouteAnalyzer()
        analyzer.update_route_performance("route1", 50.0, True)
        
        status = analyzer.get_analyzer_status()
        
        assert "tracked_routes" in status
        assert "usage_counts" in status
        assert "performance_summary" in status
        assert status["tracked_routes"] == 1

    def test_select_fastest_route_with_performance(self):
        """Test selecting fastest route with performance data."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        route_key = analyzer._generate_route_key(message)
        analyzer.route_performance[route_key] = [50.0, 60.0]  # < 100ms average
        
        result = analyzer._select_fastest_route(message, {})
        
        assert result == MockMessageRoute.DIRECT

    def test_select_fastest_route_with_cache(self):
        """Test selecting fastest route with cache."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        route_key = analyzer._generate_route_key(message)
        analyzer.route_performance[route_key] = [50.0]
        route_cache = {route_key: MockRouteOptimization()}
        
        result = analyzer._select_fastest_route(message, route_cache)
        
        assert result == MockMessageRoute.CACHED

    def test_select_fastest_route_no_performance(self):
        """Test selecting fastest route without performance data."""
        analyzer = RouteAnalyzer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        result = analyzer._select_fastest_route(message, {})
        
        assert result == MockMessageRoute.DIRECT

