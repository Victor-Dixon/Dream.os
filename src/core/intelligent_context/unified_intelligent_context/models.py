"""
Intelligent Context Search Models
==================================

Data models for intelligent context search operations.
V2 Compliance: < 200 lines, single responsibility.

<!-- SSOT Domain: data -->

Author: Agent-2 - Architecture & Design Specialist
Mission: Placeholder Implementation - Intelligent Context Search
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
import warnings


class ContextType(Enum):
    """Context type enumeration."""

    MISSION = "mission"
    AGENT_CAPABILITY = "agent_capability"
    EMERGENCY = "emergency"
    TASK = "task"
    DOCUMENTATION = "documentation"


class Priority(Enum):
    """
    Priority enumeration.

    ⚠️ DEPRECATED

    This enum has been consolidated into `src/core/coordination/swarm/coordination_models.py` as SSOT.
    Please update imports to use the SSOT location instead.

    Migration:
      OLD: from swarm.coordination_models import Priority
      NEW: from core.coordination.swarm.coordination_models import Priority

    Note: SSOT has TaskPriority (LOW, MEDIUM, HIGH, CRITICAL) - use TaskPriority or alias.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

warnings.warn(
    "Priority is deprecated. Use src/core/coordination/swarm/coordination_models.py instead.",
    DeprecationWarning,
    stacklevel=2,
)


class Status(Enum):
    """Status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


# DEPRECATED: Use SSOT from src.services.models.vector_models instead
from src.services.models.vector_models import SearchResult as SSOTSearchResult

@dataclass
class SearchResult(SSOTSearchResult):
    """
    DEPRECATED: This class is maintained for backward compatibility only.
    
    Use src.services.models.vector_models.SearchResult instead.
    
    This class will be removed in a future version.
    """
    
    def __init__(self, result_id: str, title: str = "", description: str = "",
                 relevance_score: float = 0.0, context_type: ContextType | None = None,
                 metadata: dict[str, Any] = None, timestamp: datetime = None):
        """Initialize with legacy parameters."""
        warnings.warn(
            "SearchResult from src.core.intelligent_context.unified_intelligent_context.models is deprecated. "
            "Use src.services.models.vector_models.SearchResult instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(
            document_id=result_id,
            content=description or title or "",
            similarity_score=relevance_score,
            metadata=metadata or {},
            result_id=result_id,
            title=title,
            description=description,
            relevance_score=relevance_score,
            context_type=context_type,
            timestamp=timestamp or datetime.now()
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        from src.core.utils.serialization_utils import to_dict
        result = to_dict(self)
        # Preserve custom aliases
        if "result_id" not in result and hasattr(self, 'result_id_alias') and self.result_id_alias:
            result["result_id"] = self.result_id_alias
        if "relevance_score" not in result and hasattr(self, 'relevance_score_alias') and self.relevance_score_alias:
            result["relevance_score"] = self.relevance_score_alias
        return result


