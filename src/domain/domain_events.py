"""
<!-- SSOT Domain: core -->

Domain Events - Business Events
===============================

Domain events represent significant business events that occur within the domain.
They enable loose coupling and event-driven architecture.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from .value_objects.ids import AgentId, TaskId
from src.core.utils.serialization_utils import to_dict


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events.

    Domain events are immutable and contain all necessary information
    about what happened in the domain.
    """

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    event_version: int = 1

    @property
    def event_type(self) -> str:
        """Get the event type name."""
        return self.__class__.__name__

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary representation using SSOT utility."""
        return to_dict(self)


@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    """Event raised when a new task is created."""

    task_id: Optional[TaskId] = None
    title: Optional[str] = None
    priority: Optional[int] = None

    def __post_init__(self):
        """Validate required fields."""
        if self.task_id is None:
            raise ValueError("task_id is required")
        if self.title is None:
            raise ValueError("title is required")
        if self.priority is None:
            raise ValueError("priority is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Preserve custom fields
        if self.task_id:
            result["task_id"] = str(self.task_id)
        return result


@dataclass(frozen=True)
class TaskAssigned(DomainEvent):
    """Event raised when a task is assigned to an agent."""

    task_id: Optional[TaskId] = None
    agent_id: Optional[AgentId] = None
    assigned_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate required fields."""
        if self.task_id is None:
            raise ValueError("task_id is required")
        if self.agent_id is None:
            raise ValueError("agent_id is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Preserve custom fields
        if self.task_id:
            result["task_id"] = str(self.task_id)
        if self.agent_id:
            result["agent_id"] = str(self.agent_id)
        return result


@dataclass(frozen=True)
class TaskCompleted(DomainEvent):
    """Event raised when a task is completed."""

    task_id: Optional[TaskId] = None
    agent_id: Optional[AgentId] = None
    completed_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate required fields."""
        if self.task_id is None:
            raise ValueError("task_id is required")
        if self.agent_id is None:
            raise ValueError("agent_id is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Preserve custom fields
        if self.task_id:
            result["task_id"] = str(self.task_id)
        if self.agent_id:
            result["agent_id"] = str(self.agent_id)
        return result


@dataclass(frozen=True)
class AgentActivated(DomainEvent):
    """Event raised when an agent becomes active."""

    agent_id: Optional[AgentId] = None
    activated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate required fields."""
        if self.agent_id is None:
            raise ValueError("agent_id is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Preserve custom fields
        if self.agent_id:
            result["agent_id"] = str(self.agent_id)
        return result


@dataclass(frozen=True)
class AgentDeactivated(DomainEvent):
    """Event raised when an agent becomes inactive."""

    agent_id: Optional[AgentId] = None
    deactivated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate required fields."""
        if self.agent_id is None:
            raise ValueError("agent_id is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Preserve custom fields
        if self.agent_id:
            result["agent_id"] = str(self.agent_id)
        return result
