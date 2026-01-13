"""
<!-- SSOT Domain: integration -->

Route Manager - V2 Compliant Module
===================================

Manages message routes (add, remove, get, list).
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging
from typing import Any

from ...core.base.base_service import BaseService
from .messaging_protocol_models import MessageRoute, RouteOptimization

logger = logging.getLogger(__name__)


class RouteManager(BaseService):
    """Manages message routes."""

    def __init__(self):
        """Initialize route manager."""
        super().__init__("RouteManager")
        self.routes: dict[str, RouteOptimization] = {}
        self.route_configs: dict[str, dict[str, Any]] = {}

    def add_route(
        self,
        route_name: str,
        route_type: MessageRoute,
        optimization: RouteOptimization | None = None,
        config: dict[str, Any] | None = None,
    ) -> bool:
        """
        Add a new route.

        Args:
            route_name: Name of the route
            route_type: Type of route
            optimization: Optional optimization data
            config: Optional route configuration

        Returns:
            True if route added successfully
        """
        try:
            if optimization is None:
                optimization = RouteOptimization()

            self.routes[route_name] = optimization
            self.route_configs[route_name] = {
                "type": route_type,
                "config": config or {},
            }
            self.logger.info(f"Added route: {route_name} ({route_type.value})")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add route {route_name}: {e}")
            return False

    def remove_route(self, route_name: str) -> bool:
        """
        Remove a route.

        Args:
            route_name: Name of the route to remove

        Returns:
            True if route removed successfully
        """
        if route_name not in self.routes:
            self.logger.warning(f"Route {route_name} not found")
            return False

        del self.routes[route_name]
        if route_name in self.route_configs:
            del self.route_configs[route_name]

        self.logger.info(f"Removed route: {route_name}")
        return True

    def get_route(self, route_name: str) -> dict[str, Any] | None:
        """
        Get route information.

        Args:
            route_name: Name of the route

        Returns:
            Route information dict or None if not found
        """
        if route_name not in self.routes:
            return None

        route_info = {
            "name": route_name,
            "optimization": self.routes[route_name],
            "config": self.route_configs.get(route_name, {}),
        }
        return route_info

    def list_routes(self) -> list[str]:
        """
        List all registered routes.

        Returns:
            List of route names
        """
        return list(self.routes.keys())

    def get_route_stats(self) -> dict[str, Any]:
        """Get statistics for all routes."""
        stats = {}
        for route_name, optimization in self.routes.items():
            stats[route_name] = {
                "success_rate": optimization.success_rate,
                "latency_ms": optimization.latency_ms,
            }
        return stats

