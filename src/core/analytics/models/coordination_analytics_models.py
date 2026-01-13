#!/usr/bin/env python3
"""
Coordination Analytics Models - V2 Compliance Module
===================================================

<!-- SSOT Domain: analytics -->

Data models for coordination analytics operations.
Extracted from coordination_analytics_orchestrator.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.utils.validation_utils import validate_positive, validate_range
from src.core.utils.serialization_utils import to_dict



class AnalyticsMetric(Enum):
    """Analytics metric types."""

    EFFICIENCY = "efficiency"
    THROUGHPUT = "throughput"
    SUCCESS_RATE = "success_rate"
    RESPONSE_TIME = "response_time"
    COORDINATION_QUALITY = "coordination_quality"
    SWARM_HEALTH = "swarm_health"


class OptimizationRecommendation(Enum):
    """Optimization recommendation types."""

    ROUTE_OPTIMIZATION = "route_optimization"
    BATCH_PROCESSING = "batch_processing"
    PRIORITY_QUEUING = "priority_queuing"
    LOAD_BALANCING = "load_balancing"
    CACHING = "caching"
    RETRY_STRATEGY = "retry_strategy"


@dataclass
class CoordinationAnalyticsData:
    """Coordination analytics data structure."""

    timestamp: datetime
    efficiency_score: float
    throughput: int
    success_rate: float
    average_response_time: float
    coordination_quality: float
    swarm_health: float
    active_agents: int
    total_tasks: int
    recommendations: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        from src.core.utils.serialization_utils import to_dict
        return to_dict(self)

    def get_summary(self) -> dict[str, Any]:
        """Get summary of key metrics."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "efficiency_score": self.efficiency_score,
            "success_rate": self.success_rate,
            "active_agents": self.active_agents,
            "total_tasks": self.total_tasks,
            "recommendations_count": len(self.recommendations),
        }


@dataclass
class AnalyticsReport:
    """Analytics report structure."""

    report_id: str
    generated_at: datetime
    data: CoordinationAnalyticsData
    trends: dict[str, Any]
    recommendations: list[str]
    summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        from src.core.utils.serialization_utils import to_dict
        result = to_dict(self)
        # Ensure nested data is serialized
        if "data" in result and hasattr(self.data, 'to_dict'):
            result["data"] = self.data.to_dict()
        return result


@dataclass
class AnalyticsConfig:
    """Analytics configuration."""

    enable_real_time_monitoring: bool = True
    analysis_interval_seconds: int = 60
    history_retention_hours: int = 24
    target_efficiency: float = 0.45
    enable_recommendations: bool = True
    cache_ttl_seconds: int = 300

    def validate(self) -> None:
        """Validate configuration using SSOT validation utilities."""
        validate_positive(
            self.analysis_interval_seconds,
            "Analysis interval",
            min_val=1,
        )
        validate_positive(
            self.history_retention_hours,
            "History retention",
            min_val=1,
        )
        validate_range(
            self.target_efficiency,
            min_val=0.0,
            max_val=1.0,
            field_name="Target efficiency",
        )
        validate_positive(
            self.cache_ttl_seconds,
            "Cache TTL",
            min_val=1,
        )
