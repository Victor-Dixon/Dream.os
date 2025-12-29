"""
<!-- SSOT Domain: core -->

Strategic Oversight Models - V2 Compliance
==========================================

Core data models for strategic oversight operations.
Consolidates models from various sources into single SSOT.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .enums import (
    AgentRole,
    ConfidenceLevel,
    ImpactLevel,
    InsightType,
    MissionStatus,
    PriorityLevel,
)


@dataclass
class SwarmCoordinationInsight:
    """Swarm coordination insight data model."""

    insight_id: str
    insight_type: InsightType
    title: str = ""
    description: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    confidence_level: ConfidenceLevel = None  # Alias for confidence
    impact: ImpactLevel = ImpactLevel.MEDIUM
    impact_level: ImpactLevel = None  # Alias for impact
    evidence: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Post-initialization processing."""
        if self.confidence_level is None:
            self.confidence_level = self.confidence
        if self.impact_level is None:
            self.impact_level = self.impact


@dataclass
class AgentPerformanceMetrics:
    """Agent performance metrics data model."""

    metrics_id: str = ""
    agent_id: str = ""
    agent_role: AgentRole = None
    performance_score: float = 0.0
    efficiency: float = 0.0
    coordination_score: float = 0.0
    task_completion_rate: float = 0.0
    response_time: float = 0.0
    total_tasks: int = 0
    completed_tasks: int = 0
    success_rate: float = 0.0
    average_completion_time: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SystemHealthMetrics:
    """System health metrics data model."""

    metrics_id: str = ""
    overall_health_score: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_latency: float = 0.0
    active_agents: int = 0
    system_status: str = "unknown"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StrategicRecommendation:
    """Strategic recommendation data model."""

    recommendation_id: str
    title: str = ""
    description: str = ""
    priority: PriorityLevel = PriorityLevel.MEDIUM
    priority_level: PriorityLevel = None  # Alias for priority
    impact: ImpactLevel = ImpactLevel.MEDIUM
    impact_level: ImpactLevel = None  # Alias for impact
    implementation_effort: str = "medium"
    expected_benefits: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Post-initialization processing."""
        if self.priority_level is None:
            self.priority_level = self.priority
        if self.impact_level is None:
            self.impact_level = self.impact


@dataclass
class SwarmCoordinationStatus:
    """Swarm coordination status data model."""

    status_id: str
    status_name: str = ""
    description: str = ""
    active_agents: list[str] = field(default_factory=list)
    coordination_level: str = "medium"
    efficiency_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StrategicMission:
    """Strategic mission data model."""

    mission_id: str
    mission_name: str = ""
    description: str = ""
    priority: PriorityLevel = PriorityLevel.MEDIUM
    status: MissionStatus = MissionStatus.PENDING
    assigned_agents: list[str] = field(default_factory=list)
    target_date: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StrategicOversightReport:
    """Strategic oversight report data model."""

    report_id: str
    report_type: str = ""
    title: str = ""
    description: str = ""
    insights: list[SwarmCoordinationInsight] = field(default_factory=list)
    recommendations: list[StrategicRecommendation] = field(default_factory=list)
    performance_metrics: list[AgentPerformanceMetrics] = field(default_factory=list)
    system_health: SystemHealthMetrics = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class VectorDatabaseMetrics:
    """Vector database metrics data model."""

    metrics_id: str = ""
    total_vectors: int = 0
    index_size: float = 0.0
    query_performance: float = 0.0
    index_health: str = "unknown"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StrategicOversightModels:
    """Container for all strategic oversight models."""

    insights: list[SwarmCoordinationInsight] = field(default_factory=list)
    recommendations: list[StrategicRecommendation] = field(default_factory=list)
    performance_metrics: list[AgentPerformanceMetrics] = field(default_factory=list)
    system_health: SystemHealthMetrics = None
    missions: list[StrategicMission] = field(default_factory=list)


__all__ = [
    "SwarmCoordinationInsight",
    "AgentPerformanceMetrics",
    "SystemHealthMetrics",
    "StrategicRecommendation",
    "SwarmCoordinationStatus",
    "StrategicMission",
    "StrategicOversightReport",
    "VectorDatabaseMetrics",
    "StrategicOversightModels",
]

