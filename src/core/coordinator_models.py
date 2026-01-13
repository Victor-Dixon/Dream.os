#!/usr/bin/env python3
"""
Coordinator Models - V2 Compliant
================================

<!-- SSOT Domain: integration -->

Base models and data structures for the unified coordinator system.

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-01-27
Purpose: Modular coordinator system models
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.utils.serialization_utils import to_dict


class CoordinationStatus(Enum):
    """Coordination status enumeration."""

    INITIALIZING = "initializing"
    OPERATIONAL = "operational"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class TargetType(Enum):
    """Coordination target type enumeration."""

    TASK = "task"
    RESOURCE = "resource"
    SERVICE = "service"
    AGENT = "agent"
    SYSTEM = "system"


class Priority(Enum):
    """Priority level enumeration."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class CoordinationTarget:
    """Represents a coordination target with enhanced metadata."""

    target_id: str
    target_type: TargetType
    priority: Priority
    status: CoordinationStatus
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.target_id:
            raise ValueError("Target ID cannot be empty")

        if isinstance(self.target_type, str):
            self.target_type = TargetType(self.target_type)

        if isinstance(self.priority, int):
            self.priority = Priority(self.priority)

        if isinstance(self.status, str):
            self.status = CoordinationStatus(self.status)

    def update_metadata(self, updates: dict[str, Any]) -> None:
        """Update target metadata."""
        self.metadata.update(updates)
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        """Check if target is active."""
        return self.status == CoordinationStatus.OPERATIONAL

    def to_dict(self) -> dict[str, Any]:
        """Convert target to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class CoordinationResult:
    """Result of a coordination operation."""

    success: bool
    operation: str
    result: Any = None
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    coordinator: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class CoordinatorStatus:
    """Comprehensive coordinator status information."""

    name: str
    initialized: bool
    coordination_status: CoordinationStatus
    config: dict[str, Any]
    start_time: datetime
    uptime_seconds: float
    operations_count: int
    error_count: int
    success_rate: float
    targets_count: int
    targets_by_type: dict[str, int]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Convert status to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class CoordinatorConfig:
    """Coordinator configuration with validation."""

    name: str
    config: dict[str, Any] = field(default_factory=dict)
    max_targets: int = 1000
    operation_timeout: float = 30.0
    retry_attempts: int = 3
    enable_logging: bool = True
    enable_metrics: bool = True

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name:
            raise ValueError("Coordinator name cannot be empty")

        if self.max_targets <= 0:
            raise ValueError("Max targets must be positive")

        if self.operation_timeout <= 0:
            raise ValueError("Operation timeout must be positive")

        if self.retry_attempts < 0:
            raise ValueError("Retry attempts cannot be negative")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback."""
        return self.config.get(key, default)

    def update(self, updates: dict[str, Any]) -> None:
        """Update configuration."""
        self.config.update(updates)

    def validate(self) -> bool:
        """Validate configuration."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False
