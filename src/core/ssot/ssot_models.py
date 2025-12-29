#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

SSOT Models - V2 Compliant
=========================

Data models and enums for SSOT (Single Source of Truth) operations.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant SSOT data models
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.utils.serialization_utils import to_dict


class SSOTComponentType(Enum):
    """SSOT component types - consolidated from multiple files."""

    LOGGING = "logging"
    CONFIGURATION = "configuration"
    INTERFACE = "interface"
    MESSAGING = "messaging"
    FILE_LOCKING = "file_locking"
    VALIDATION = "validation"
    EXECUTION = "execution"


class SSOTExecutionPhase(Enum):
    """SSOT execution phases - consolidated from multiple files."""

    INITIALIZATION = "initialization"
    VALIDATION = "validation"
    EXECUTION = "execution"
    COORDINATION = "coordination"
    COMPLETION = "completion"


class SSOTValidationLevel(Enum):
    """SSOT validation levels - consolidated from multiple files."""

    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    STRESS = "stress"
    INTEGRATION = "integration"


@dataclass
class SSOTComponent:
    """SSOT component representation.

    DRY COMPLIANCE: Single component model for all SSOT operations.
    """

    component_id: str
    component_type: SSOTComponentType
    name: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class SSOTIntegrationResult:
    """Result of SSOT integration operation.

    DRY COMPLIANCE: Single result model for all SSOT operations.
    """

    component_id: str
    success: bool
    execution_time: float = 0.0
    error_message: str | None = None
    validation_results: dict[str, Any] = field(default_factory=dict)
    performance_metrics: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class SSOTExecutionTask:
    """SSOT execution task.

    DRY COMPLIANCE: Single task model for all SSOT execution operations.
    """

    task_id: str
    component_id: str
    phase: SSOTExecutionPhase
    dependencies: list[str] = field(default_factory=list)
    priority: int = 1
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class SSOTValidationReport:
    """SSOT validation report.

    DRY COMPLIANCE: Single validation report for all SSOT validation operations.
    """

    report_id: str
    component_id: str
    validation_level: SSOTValidationLevel
    results: list[SSOTIntegrationResult] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Ensure results are serialized
        if "results" in result:
            result["results"] = [result.to_dict() if hasattr(result, 'to_dict') else to_dict(result) for result in self.results]
        return result


class SSOTMetrics:
    """Metrics tracking for SSOT operations."""

    def __init__(self):
        """Initialize metrics."""
        self.total_components = 0
        self.total_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.average_execution_time = 0.0
        self.validation_reports_generated = 0

    def record_component_registration(self):
        """Record component registration."""
        self.total_components += 1

    def record_task_creation(self):
        """Record task creation."""
        self.total_tasks += 1

    def record_task_completion(self, success: bool, execution_time: float):
        """Record task completion."""
        if success:
            self.completed_tasks += 1
        else:
            self.failed_tasks += 1

        # Update average execution time
        total_completed = self.completed_tasks + self.failed_tasks
        if total_completed > 0:
            self.average_execution_time = (
                self.average_execution_time * (total_completed - 1) + execution_time
            ) / total_completed

    def record_report_generation(self):
        """Record validation report generation."""
        self.validation_reports_generated += 1

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Preserve computed success_rate
        if "success_rate" not in result:
            result["success_rate"] = (self.completed_tasks / max(1, self.total_tasks)) * 100
        return result
