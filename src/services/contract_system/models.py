#!/usr/bin/env python3
"""
Contract Models - Agent Cellphone V2
===================================

Data models for the contract system.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from datetime import datetime
from enum import Enum
from typing import Any

from src.core.utils.serialization_utils import to_dict


class ContractStatus(Enum):
    """Contract status enumeration."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ContractPriority(Enum):
    """Contract priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# NOTE: TaskStatus enum below is deprecated - use coordination_models.py instead


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ContractTask:
    """Contract task data model (contract system domain-specific, not to be confused with domain entity Task)."""

    def __init__(self, **kwargs):
        """Initialize task with provided data."""
        self.task_id = kwargs.get("task_id", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.status = kwargs.get("status", TaskStatus.PENDING.value)
        self.priority = kwargs.get("priority", ContractPriority.MEDIUM.value)
        self.assigned_to = kwargs.get("assigned_to", "")
        self.created_at = kwargs.get("created_at", datetime.now().isoformat())
        self.due_date = kwargs.get("due_date", "")
        self.completed_at = kwargs.get("completed_at", "")
        self.last_updated = kwargs.get("last_updated", datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContractTask":
        """Create task from dictionary."""
        return cls(**data)

    def update_status(self, status: str) -> None:
        """Update task status."""
        self.status = status
        self.last_updated = datetime.now().isoformat()

        if status == TaskStatus.COMPLETED.value:
            self.completed_at = datetime.now().isoformat()

    def assign_to(self, agent_id: str) -> None:
        """Assign task to agent."""
        self.assigned_to = agent_id
        self.status = TaskStatus.IN_PROGRESS.value
        self.last_updated = datetime.now().isoformat()


class Contract:
    """Contract data model."""

    def __init__(self, **kwargs):
        """Initialize contract with provided data."""
        self.contract_id = kwargs.get("contract_id", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.status = kwargs.get("status", ContractStatus.PENDING.value)
        self.priority = kwargs.get("priority", ContractPriority.MEDIUM.value)
        self.assigned_to = kwargs.get("assigned_to", "")
        self.created_at = kwargs.get("created_at", datetime.now().isoformat())
        self.assigned_at = kwargs.get("assigned_at", "")
        self.completed_at = kwargs.get("completed_at", "")
        self.tasks = kwargs.get("tasks", [])
        self.last_updated = kwargs.get("last_updated", datetime.now().isoformat())
        
        # ROI Scoring Fields
        self.user_value = kwargs.get("user_value", 0.0)
        self.risk = kwargs.get("risk", 1.0)
        self.effort = kwargs.get("effort", 1.0)
        self.dependency_count = kwargs.get("dependency_count", 0)
        self.roi_score = kwargs.get("roi_score", 0.0)

    def to_dict(self) -> dict[str, Any]:
        """Convert contract to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contract":
        """Create contract from dictionary."""
        return cls(**data)

    def update_status(self, status: str) -> None:
        """Update contract status."""
        self.status = status
        self.last_updated = datetime.now().isoformat()

        if status == ContractStatus.COMPLETED.value:
            self.completed_at = datetime.now().isoformat()

    def assign_to(self, agent_id: str) -> None:
        """Assign contract to agent."""
        self.assigned_to = agent_id
        self.status = ContractStatus.ACTIVE.value
        self.assigned_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()

    def add_task(self, task: dict[str, Any]) -> None:
        """Add task to contract."""
        if not self.tasks:
            self.tasks = []
        self.tasks.append(task)
        self.last_updated = datetime.now().isoformat()

    def calculate_roi(self) -> float:
        """
        Calculate ROI score based on user value, risk, effort, and dependencies.
        
        Formula: User Value / (Effort + Dependency Count) / Risk
        Risk is 1-10 (1=low, 10=high).
        Effort is arbitrary units (e.g. hours or points).
        User Value is arbitrary units (e.g. 1-100).
        """
        effort_factor = max(0.1, float(self.effort) + float(self.dependency_count))
        risk_penalty = max(1.0, float(self.risk))
        
        self.roi_score = float(self.user_value) / effort_factor / risk_penalty
        return self.roi_score
