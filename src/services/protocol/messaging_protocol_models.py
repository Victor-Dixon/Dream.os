"""
<!-- SSOT Domain: integration -->

Messaging Protocol Models - V2 Compliance Module
================================================

Protocol models for message routing and optimization.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any


class MessageRoute(Enum):
    """Message routing options."""

    CACHED = "cached"
    DIRECT = "direct"
    OPTIMIZED = "optimized"
    BATCHED = "batched"
    LOAD_BALANCED = "load_balanced"
    QUEUED = "queued"


class ProtocolOptimizationStrategy(Enum):
    """Protocol optimization strategies."""

    ROUTE_OPTIMIZATION = "route_optimization"
    MESSAGE_BATCHING = "message_batching"
    LOAD_BALANCING = "load_balancing"
    CACHING = "caching"


@dataclass
class RouteOptimization:
    """Route optimization data."""

    success_rate: float = 1.0
    latency_ms: float = 50.0


@dataclass
class OptimizationConfig:
    """Optimization configuration."""

    enable_load_balancing: bool = True
    enable_caching: bool = True
    enable_batching: bool = True


def create_default_config() -> OptimizationConfig:
    """Create default optimization config."""
    return OptimizationConfig()


# Route priority order for selection
ROUTE_PRIORITY_ORDER = [
    MessageRoute.CACHED,
    MessageRoute.DIRECT,
    MessageRoute.OPTIMIZED,
    MessageRoute.BATCHED,
    MessageRoute.LOAD_BALANCED,
    MessageRoute.QUEUED,
]


__all__ = [
    "MessageRoute",
    "ProtocolOptimizationStrategy",
    "RouteOptimization",
    "OptimizationConfig",
    "create_default_config",
    "ROUTE_PRIORITY_ORDER",
]

