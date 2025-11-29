"""
Tests for protocol/route_manager.py

Comprehensive tests for route management, routing logic, and route operations.
Target: 12+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.services.protocol.route_manager import RouteManager
from src.services.protocol.messaging_protocol_models import (
    MessageRoute,
    RouteOptimization,
)


class TestRouteManager:
    """Tests for RouteManager class."""

    def test_initialization(self):
        """Test route manager initialization."""
        manager = RouteManager()
        assert manager.routes == {}
        assert manager.route_configs == {}

    def test_add_route_success(self):
        """Test adding route successfully."""
        manager = RouteManager()
        result = manager.add_route(
            "test_route",
            MessageRoute.DIRECT,
            RouteOptimization(),
            {"timeout": 30}
        )
        
        assert result is True
        assert "test_route" in manager.routes
        assert "test_route" in manager.route_configs
        assert manager.route_configs["test_route"]["type"] == MessageRoute.DIRECT
        assert manager.route_configs["test_route"]["config"]["timeout"] == 30

    def test_add_route_without_optimization(self):
        """Test adding route without optimization (creates default)."""
        manager = RouteManager()
        result = manager.add_route("test_route", MessageRoute.DIRECT)
        
        assert result is True
        assert "test_route" in manager.routes
        assert isinstance(manager.routes["test_route"], RouteOptimization)

    def test_add_route_without_config(self):
        """Test adding route without config."""
        manager = RouteManager()
        result = manager.add_route("test_route", MessageRoute.BATCH, RouteOptimization())
        
        assert result is True
        assert manager.route_configs["test_route"]["config"] == {}

    def test_add_route_exception_handling(self):
        """Test add_route handles exceptions gracefully."""
        manager = RouteManager()
        
        with patch.object(manager, 'routes', side_effect=Exception("Test error")):
            result = manager.add_route("test_route", MessageRoute.DIRECT)
            assert result is False

    def test_remove_route_success(self):
        """Test removing route successfully."""
        manager = RouteManager()
        manager.add_route("test_route", MessageRoute.DIRECT)
        
        result = manager.remove_route("test_route")
        
        assert result is True
        assert "test_route" not in manager.routes
        assert "test_route" not in manager.route_configs

    def test_remove_route_not_found(self):
        """Test removing route that doesn't exist."""
        manager = RouteManager()
        result = manager.remove_route("nonexistent")
        
        assert result is False

    def test_remove_route_removes_both_storage(self):
        """Test removing route removes from both routes and configs."""
        manager = RouteManager()
        manager.add_route("test_route", MessageRoute.DIRECT, None, {"key": "value"})
        
        assert "test_route" in manager.routes
        assert "test_route" in manager.route_configs
        
        manager.remove_route("test_route")
        
        assert "test_route" not in manager.routes
        assert "test_route" not in manager.route_configs

    def test_get_route_success(self):
        """Test getting route information successfully."""
        manager = RouteManager()
        optimization = RouteOptimization()
        manager.add_route("test_route", MessageRoute.DIRECT, optimization, {"timeout": 30})
        
        route_info = manager.get_route("test_route")
        
        assert route_info is not None
        assert route_info["name"] == "test_route"
        assert route_info["optimization"] == optimization
        assert route_info["config"]["timeout"] == 30

    def test_get_route_not_found(self):
        """Test getting route that doesn't exist."""
        manager = RouteManager()
        route_info = manager.get_route("nonexistent")
        
        assert route_info is None

    def test_get_route_without_config(self):
        """Test getting route that was added without config."""
        manager = RouteManager()
        manager.add_route("test_route", MessageRoute.DIRECT)
        
        route_info = manager.get_route("test_route")
        
        assert route_info is not None
        assert route_info["config"] == {}

    def test_list_routes_empty(self):
        """Test listing routes when empty."""
        manager = RouteManager()
        routes = manager.list_routes()
        
        assert routes == []

    def test_list_routes_multiple(self):
        """Test listing multiple routes."""
        manager = RouteManager()
        manager.add_route("route1", MessageRoute.DIRECT)
        manager.add_route("route2", MessageRoute.BATCH)
        manager.add_route("route3", MessageRoute.QUEUE)
        
        routes = manager.list_routes()
        
        assert len(routes) == 3
        assert "route1" in routes
        assert "route2" in routes
        assert "route3" in routes

    def test_get_route_stats_empty(self):
        """Test getting route stats when no routes."""
        manager = RouteManager()
        stats = manager.get_route_stats()
        
        assert stats == {}

    def test_get_route_stats_multiple_routes(self):
        """Test getting stats for multiple routes."""
        manager = RouteManager()
        opt1 = RouteOptimization()
        opt1.success_rate = 0.95
        opt1.latency_ms = 50.0
        opt2 = RouteOptimization()
        opt2.success_rate = 0.90
        opt2.latency_ms = 100.0
        
        manager.add_route("route1", MessageRoute.DIRECT, opt1)
        manager.add_route("route2", MessageRoute.BATCH, opt2)
        
        stats = manager.get_route_stats()
        
        assert len(stats) == 2
        assert stats["route1"]["success_rate"] == 0.95
        assert stats["route1"]["latency_ms"] == 50.0
        assert stats["route2"]["success_rate"] == 0.90
        assert stats["route2"]["latency_ms"] == 100.0

    def test_add_route_logs_info(self):
        """Test that add_route logs info."""
        manager = RouteManager()
        
        with patch('src.services.protocol.route_manager.logger') as mock_logger:
            manager.add_route("test_route", MessageRoute.DIRECT)
            assert mock_logger.info.called

    def test_remove_route_logs_info(self):
        """Test that remove_route logs info."""
        manager = RouteManager()
        manager.add_route("test_route", MessageRoute.DIRECT)
        
        with patch('src.services.protocol.route_manager.logger') as mock_logger:
            manager.remove_route("test_route")
            assert mock_logger.info.called

    def test_add_route_overwrites_existing(self):
        """Test that adding route with same name overwrites existing."""
        manager = RouteManager()
        opt1 = RouteOptimization()
        opt2 = RouteOptimization()
        
        manager.add_route("test_route", MessageRoute.DIRECT, opt1)
        manager.add_route("test_route", MessageRoute.BATCH, opt2)
        
        assert manager.routes["test_route"] == opt2
        assert manager.route_configs["test_route"]["type"] == MessageRoute.BATCH

