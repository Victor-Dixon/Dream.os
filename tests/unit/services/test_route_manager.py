"""
Unit tests for route_manager.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.protocol.route_manager import RouteManager
from src.services.protocol.messaging_protocol_models import MessageRoute, RouteOptimization


class TestRouteManager:
    """Test suite for RouteManager."""

    @pytest.fixture
    def manager(self):
        """Create RouteManager instance."""
        return RouteManager()

    def test_manager_initialization(self, manager):
        """Test manager initializes correctly."""
        assert manager is not None
        assert manager.routes == {}
        assert manager.route_configs == {}

    def test_add_route_success(self, manager):
        """Test adding route successfully."""
        route_name = "test_route"
        route_type = MessageRoute.PRIORITY
        
        result = manager.add_route(route_name, route_type)
        
        assert result is True
        assert route_name in manager.routes
        assert route_name in manager.route_configs

    def test_add_route_with_optimization(self, manager):
        """Test adding route with optimization."""
        route_name = "optimized_route"
        route_type = MessageRoute.PRIORITY
        optimization = RouteOptimization()
        
        result = manager.add_route(route_name, route_type, optimization)
        
        assert result is True
        assert manager.routes[route_name] == optimization

    def test_remove_route_exists(self, manager):
        """Test removing existing route."""
        route_name = "test_route"
        manager.add_route(route_name, MessageRoute.PRIORITY)
        
        result = manager.remove_route(route_name)
        
        assert result is True
        assert route_name not in manager.routes

    def test_remove_route_not_exists(self, manager):
        """Test removing non-existent route."""
        result = manager.remove_route("non_existent")
        
        assert result is False

    def test_get_route_exists(self, manager):
        """Test getting existing route."""
        route_name = "test_route"
        manager.add_route(route_name, MessageRoute.PRIORITY)
        
        route_info = manager.get_route(route_name)
        
        assert route_info is not None
        assert route_info["name"] == route_name

    def test_get_route_not_exists(self, manager):
        """Test getting non-existent route."""
        route_info = manager.get_route("non_existent")
        
        assert route_info is None

    def test_list_routes_empty(self, manager):
        """Test listing routes when empty."""
        routes = manager.list_routes()
        
        assert routes == []

    def test_list_routes_with_routes(self, manager):
        """Test listing routes when routes exist."""
        manager.add_route("route1", MessageRoute.PRIORITY)
        manager.add_route("route2", MessageRoute.STANDARD)
        
        routes = manager.list_routes()
        
        assert len(routes) == 2
        assert "route1" in routes
        assert "route2" in routes

