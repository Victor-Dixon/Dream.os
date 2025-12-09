#!/usr/bin/env python3
"""
Context Results Models - V2 Compliance
=======================================

Search and retrieval result structures.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .mission_models import MissionContext
from src.core.utils.serialization_utils import to_dict


# DEPRECATED: Use SSOT from src.services.models.vector_models instead
import warnings
from src.services.models.vector_models import SearchResult as SSOTSearchResult

@dataclass
class SearchResult(SSOTSearchResult):
    """
    DEPRECATED: This class is maintained for backward compatibility only.
    
    Use src.services.models.vector_models.SearchResult instead.
    
    This class will be removed in a future version.
    
    <!-- SSOT Domain: data -->
    """
    
    def __init__(self, result_id: str, content: str, relevance_score: float,
                 source_type: str, source_id: str, metadata: dict[str, Any] = None,
                 timestamp: datetime = None):
        """Initialize with legacy parameters."""
        warnings.warn(
            "SearchResult from src.core.intelligent_context.context_results is deprecated. "
            "Use src.services.models.vector_models.SearchResult instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(
            document_id=result_id,
            content=content,
            similarity_score=relevance_score,
            metadata=metadata or {},
            result_id=result_id,
            source_type=source_type,
            source_id=source_id,
            relevance_score=relevance_score,
            timestamp=timestamp or datetime.now()
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        # Use SSOT utility for base conversion, then add aliases
        result = to_dict(self)
        # Map aliases for backward compatibility
        if "result_id_alias" in result:
            result["result_id"] = result.pop("result_id_alias")
        if "relevance_score_alias" in result:
            result["relevance_score"] = result.pop("relevance_score_alias")
        return result


@dataclass
class ContextRetrievalResult:
    """Result of context retrieval operation."""

    success: bool
    mission_context: MissionContext | None = None
    search_results: list[SearchResult] = field(default_factory=list)
    agent_recommendations: list[dict[str, Any]] = field(default_factory=list)
    risk_assessment: dict[str, Any] | None = None
    success_prediction: dict[str, Any] | None = None
    execution_time_ms: float = 0.0
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Ensure nested search_results are serialized
        if "search_results" in result:
            result["search_results"] = [sr.to_dict() if hasattr(sr, 'to_dict') else sr for sr in self.search_results]
        return result


__all__ = ["SearchResult", "ContextRetrievalResult"]
