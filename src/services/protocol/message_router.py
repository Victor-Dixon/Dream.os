"""
<!-- SSOT Domain: integration -->

Message Router - V2 Compliant Module
=====================================

Routes messages based on priority, type, and routing strategies.
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging
from datetime import datetime
from typing import Any

from ...core.base.base_service import BaseService
from ...core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
)
from .messaging_protocol_models import (
    MessageRoute,
    OptimizationConfig,
    ProtocolOptimizationStrategy,
    RouteOptimization,
    create_default_config,
)
from .routers.route_analyzer import RouteAnalyzer

logger = logging.getLogger(__name__)


class MessageRouter(BaseService):
    """Routes messages based on priority, type, and strategies."""

    def __init__(self, config: OptimizationConfig | None = None):
        """Initialize message router."""
        super().__init__("MessageRouter")
        self.config = config or create_default_config()
        self.analyzer = RouteAnalyzer(self.config)
        self.route_cache: dict[str, RouteOptimization] = {}
        self.failed_routes: dict[str, datetime] = {}

    def route_message(
        self,
        message: UnifiedMessage,
        strategies: list[ProtocolOptimizationStrategy] | None = None,
    ) -> MessageRoute:
        """
        Route a message based on priority and strategies.

        Args:
            message: Message to route
            strategies: Optional list of optimization strategies

        Returns:
            Selected route for the message
        """
        if strategies is None:
            strategies = []

        # Determine strategies based on message properties
        if message.priority == UnifiedMessagePriority.URGENT:
            strategies.append(ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION)

        if message.message_type == UnifiedMessageType.BROADCAST:
            strategies.append(ProtocolOptimizationStrategy.MESSAGE_BATCHING)

        # Analyze and select route
        route = self.analyzer.analyze_route_options(
            message, strategies, self.route_cache, self.failed_routes
        )

        logger.info(f"Routed message {message.message_id} via {route.value}")
        return route

    def route_with_priority(
        self, message: UnifiedMessage, priority_override: UnifiedMessagePriority | None = None
    ) -> MessageRoute:
        """
        Route message with priority override.

        Args:
            message: Message to route
            priority_override: Optional priority override

        Returns:
            Selected route
        """
        if priority_override:
            message.priority = priority_override

        return self.route_message(message)

    def route_with_strategy(
        self,
        message: UnifiedMessage,
        strategy: ProtocolOptimizationStrategy,
    ) -> MessageRoute:
        """
        Route message with specific strategy.

        Args:
            message: Message to route
            strategy: Strategy to use

        Returns:
            Selected route
        """
        return self.route_message(message, strategies=[strategy])

    def update_route_performance(
        self, route_key: str, latency_ms: float, success: bool
    ) -> None:
        """Update route performance metrics."""
        self.analyzer.update_route_performance(route_key, latency_ms, success)

    def get_router_status(self) -> dict[str, Any]:
        """Get router status information."""
        return {
            "analyzer_status": self.analyzer.get_analyzer_status(),
            "cached_routes": len(self.route_cache),
            "failed_routes": len(self.failed_routes),
        }

