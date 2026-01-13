"""
Vector Database Models
======================

Data models for vector database operations.
V2 Compliance: < 200 lines, single responsibility.

Author: Agent-7 - Repository Cloning & Consolidation Specialist
Created: 2025-10-11 (fixing missing import)


<!-- SSOT Domain: web -->
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalyticsData:
    """Analytics data model for vector database reporting."""

    total_documents: int
    search_queries: int
    average_response_time: float
    success_rate: float
    top_searches: list[dict[str, Any]] = field(default_factory=list)
    document_distribution: dict[str, int] = field(default_factory=dict)
    search_trends: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Collection:
    """Vector database collection model."""

    id: str
    name: str
    document_count: int
    description: str = ""
    last_updated: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExportData:
    """Export data model for vector database exports."""

    collection: str
    format: str
    data: Any
    filename: str
    size: str
    metadata: dict[str, Any] = field(default_factory=dict)
    generated_at: str = ""


@dataclass
class ExportRequest:
    """Export request model."""

    collection: str
    format: str = "json"
    include_metadata: bool = True
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchRequest:
    """Search request model."""

    query: str
    collection: str = "all"
    limit: int = 10
    filters: dict[str, Any] = field(default_factory=dict)


# Backward compatibility shim - use SSOT from src.services.models.vector_models
from src.services.models.vector_models import SearchResult as SSOTSearchResult

@dataclass
class SearchResult(SSOTSearchResult):
    """
    Backward compatibility shim for SearchResult.
    
    DEPRECATED: Use src.services.models.vector_models.SearchResult instead.
    This class is maintained for backward compatibility only.
    
    <!-- SSOT Domain: data -->
    """
    
    def __init__(self, id: str, title: str, content: str, collection: str, 
                 relevance: float, tags: list[str] = None, created_at: str = "",
                 updated_at: str = "", size: str = "", metadata: dict[str, Any] = None,
                 score: float | None = None):
        """Initialize with web model parameters."""
        super().__init__(
            document_id=id,
            content=content,
            similarity_score=relevance,
            metadata=metadata or {},
            id=id,
            title=title,
            collection=collection,
            relevance=relevance,
            tags=tags or [],
            created_at=created_at,
            updated_at=updated_at,
            size=size,
            score=score
        )


@dataclass
class Document:
    """Document model for vector database."""

    id: str
    title: str
    content: str
    collection: str
    tags: list[str] = field(default_factory=list)
    size: str = ""
    created_at: str = ""
    updated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)


@dataclass
class DocumentRequest:
    """Document request model."""

    collection: str
    document_id: str
    include_embedding: bool = False


@dataclass
class PaginationRequest:
    """Pagination request model."""

    page: int = 1
    per_page: int = 25
    collection: str = "all"
    sort_by: str = "created_at"
    sort_order: str = "desc"
    filters: dict[str, Any] = field(default_factory=dict)
