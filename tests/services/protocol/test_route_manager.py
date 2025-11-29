"""
Tests for route_manager.py

Comprehensive tests for route management.
Target: ≥85% coverage
"""

import pytest
from src.services.protocol.route_manager import RouteManager
from src.services.protocol.messaging_protocol_models import (
    MessageRoute,
    RouteOptimization,
)


class TestRouteManager:
    """Tests for RouteManager."""

    def test_route_manager_initialization(self):
        """Test RouteManager initialization."""
        manager = RouteManager()
        assert manager.routes == {}
        assert manager.route_configs == {}

    def test_add_route_success(self):
        """Test adding a route successfully."""
        manager = RouteManager()
        result = manager.add_route(
            "test_route",
            MessageRoute.DIRECT,
            RouteOptimization(success_rate=0.95, latency_ms=30.0),
        )
        
        assert result is True
        assert "test_route" in manager.routes
        assert "test_route" in manager.route_configs

    def test_add_route_with_config(self):
        """Test adding a route with configuration."""
        manager = RouteManager()
        config = {"timeout": 60, "retries": 3}
        result = manager.add_route(
            "test_route",
            MessageRoute.DIRECT,
            config=config,
        )
        
        assert result is True
        assert manager.route_configs["test_route"]["config"] == config

    def test_add_route_default_optimization(self):
        """Test adding a route with default optimization."""
        manager = RouteManager()
        result = manager.add_route("test_route", MessageRoute.DIRECT)
        
        assert result is True
        assert "test_route" in manager.routes
        assert isinstance(manager.routes["test_route"], RouteOptimization)

    def test_add_route_multiple(self):
        """Test adding multiple routes."""
        manager = RouteManager()
        manager.add_route("route1", MessageRoute.DIRECT)
        manager.add_route("route2", MessageRoute.CACHED)
        manager.add_route("route3", MessageRoute.BATCHED)
        
        assert len(manager.routes) == 3
        assert len(manager.route_configs) == 3

    def test_remove_route_success(self):
        """Test removing a route successfully."""
        manager = RouteManager()
        manager.add_route("test_route", MessageRoute.DIRECT)
        
        result = manager.remove_route("test_route")
        
        assert result is True
        assert "test_route" not in manager.routes
        assert "test_route" not in manager.route_configs

    def test_remove_route_not_found(self):
        """Test removing a non-existent route."""
        manager = RouteManager()
        
        result = manager.remove_route("nonexistent")
        
        assert result is False

    def test_get_route_success(self):
        """Test getting a route successfully."""
        manager = RouteManager()
        manager.add_route("test_route", MessageRoute.DIRECT)
        
        route_info = manager.get_route("test_route")
        
        assert route_info is not None
        assert route_info["name"] == "test_route"
        assert "optimization" in route_info
        assert "config" in route_info

    def test_get_route_not_found(self):
        """Test getting a non-existent route."""
        manager = RouteManager()
        
        route_info = manager.get_route("nonexistent")
        
        assert route_info is None

    def test_list_routes_empty(self):
        """Test listing routes when empty."""
        manager = RouteManager()
        
        routes = manager.list_routes()
        
        assert routes == []

    def test_list_routes_multiple(self):
        """Test listing multiple routes."""
        manager = RouteManager()
        manager.add_route("route1", MessageRoute.DIRECT)
        manager.add_route("route2", MessageRoute.CACHED)
        manager.add_route("route3", MessageRoute.BATCHED)
        
        routes = manager.list_routes()
        
        assert len(routes) == 3
        assert "route1" in routes
        assert "route2" in routes
        assert "route3" in routes

    def test_get_route_stats(self):
        """Test getting route statistics."""
        manager = RouteManager()
        manager.add_route(
            "route1",
            MessageRoute.DIRECT,
            RouteOptimization(success_rate=0.95, latency_ms=30.0),
        )
        manager.add_route(
            "route2",
            MessageRoute.CACHED,
            RouteOptimization(success_rate=0.98, latency_ms=20.0),
        )
        
        stats = manager.get_route_stats()
        
        assert "route1" in stats
        assert "route2" in stats
        assert stats["route1"]["success_rate"] == 0.95
        assert stats["route1"]["latency_ms"] == 30.0
        assert stats["route2"]["success_rate"] == 0.98
        assert stats["route2"]["latency_ms"] == 20.0

    def test_get_route_stats_empty(self):
        """Test getting route statistics when empty."""
        manager = RouteManager()
        
        stats = manager.get_route_stats()
        
        assert stats == {}
