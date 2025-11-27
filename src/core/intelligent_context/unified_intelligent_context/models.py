"""
Intelligent Context Search Models
==================================

Data models for intelligent context search operations.
V2 Compliance: < 200 lines, single responsibility.

Author: Agent-2 - Architecture & Design Specialist
Mission: Placeholder Implementation - Intelligent Context Search
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ContextType(Enum):
    """Context type enumeration."""

    MISSION = "mission"
    AGENT_CAPABILITY = "agent_capability"
    EMERGENCY = "emergency"
    TASK = "task"
    DOCUMENTATION = "documentation"


class Priority(Enum):
    """Priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(Enum):
    """Status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass
class SearchResult:
    """Search result structure for intelligent context search."""

    result_id: str
    title: str = ""
    description: str = ""
    relevance_score: float = 0.0
    context_type: ContextType | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "result_id": self.result_id,
            "title": self.title,
            "description": self.description,
            "relevance_score": self.relevance_score,
            "context_type": self.context_type.value if self.context_type else None,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


