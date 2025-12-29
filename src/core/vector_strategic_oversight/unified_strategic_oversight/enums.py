"""
<!-- SSOT Domain: core -->

Strategic Oversight Enums - V2 Compliance
==========================================

Enumeration types for strategic oversight operations.
Single source of truth for all enum values.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence level enumeration."""

    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ImpactLevel(Enum):
    """Impact level enumeration."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class InsightType(Enum):
    """Insight type enumeration."""

    COORDINATION_ANALYSIS = "coordination_analysis"
    COLLABORATION = "collaboration"
    MISSION_COORDINATION = "mission_coordination"
    PERFORMANCE = "performance"
    SYSTEM_HEALTH = "system_health"
    STRATEGIC_PLANNING = "strategic_planning"


class PriorityLevel(Enum):
    """Priority level enumeration."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AgentRole(Enum):
    """Agent role enumeration."""

    CAPTAIN = "captain"
    COORDINATOR = "coordinator"
    SPECIALIST = "specialist"
    ANALYST = "analyst"
    EXECUTOR = "executor"


class MissionStatus(Enum):
    """Mission status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class EmergencyStatus(Enum):
    """Emergency status enumeration."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReportType(Enum):
    """Report type enumeration."""

    SUMMARY = "summary"
    DETAILED = "detailed"
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    STATUS = "status"


__all__ = [
    "ConfidenceLevel",
    "ImpactLevel",
    "InsightType",
    "PriorityLevel",
    "AgentRole",
    "MissionStatus",
    "EmergencyStatus",
    "ReportType",
]

