"""
Vector Models - V2 Compliance Module
===================================

Data models for vector database operations.

<!-- SSOT Domain: data -->

SSOT for SearchResult, SearchQuery, DocumentType, EmbeddingModel, and SearchType - All vector/search operations should use these models.

Author: Agent-1 (System Recovery Specialist)
Enhanced by: Agent-8 (Testing & Quality Assurance Specialist) - SSOT Consolidation
License: MIT
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.core.utils.serialization_utils import to_dict


class EmbeddingModel(Enum):
    """Supported embedding models."""
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    OPENAI_ADA = "openai-ada-002"
    OPENAI_3_SMALL = "openai-3-small"
    OPENAI_3_LARGE = "openai-3-large"


class DocumentType(Enum):
    """Document types for vector database."""
    MESSAGE = "message"
    DEVLOG = "devlog"
    CONTRACT = "contract"
    STATUS = "status"
    CODE = "code"
    DOCUMENTATION = "documentation"


class SearchType(Enum):
    """Search types for vector database."""
    SIMILARITY = "similarity"
    MAX_MARGINAL_RELEVANCE = "mmr"
    FILTERED = "filtered"


@dataclass
class VectorDocument:
    """Vector document representation."""

    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorDocument':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            content=data['content'],
            embedding=data['embedding'],
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class EmbeddingResult:
    """Result of embedding operation."""

    document_id: str
    embedding: List[float]
    model: EmbeddingModel
    tokens_used: int
    processing_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class SearchQuery:
    """
    Unified search query model - SSOT for all vector/search operations.
    
    This is the single source of truth for search queries across the codebase.
    Supports all query variants with backward compatibility.
    
    <!-- SSOT Domain: data -->
    """

    query_text: str = ""  # Default to empty string for backward compatibility
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    similarity_threshold: float = 0.0
    filters: Optional[Dict[str, Any]] = None
    
    # Backward compatibility aliases
    query: Optional[str] = None  # Alias for query_text (fallback stubs)
    threshold: Optional[float] = None  # Alias for similarity_threshold
    metadata_filter: Optional[Dict[str, Any]] = None  # Alias for filters
    agent_id: Optional[str] = None  # For agent-specific queries
    
    def __post_init__(self):
        """Initialize backward compatibility fields."""
        # Map query to query_text if provided and query_text is empty
        if self.query is not None and (not self.query_text or self.query_text == ""):
            self.query_text = self.query
        
        # Map threshold to similarity_threshold if provided
        if self.threshold is not None and self.similarity_threshold == 0.0:
            self.similarity_threshold = self.threshold
        
        # Map metadata_filter to filters if provided
        if self.metadata_filter is not None and self.filters is None:
            self.filters = self.metadata_filter
    
    @property
    def query_alias(self) -> str:
        """Backward compatibility: return query_text as 'query'."""
        return self.query_text
    
    @property
    def threshold_alias(self) -> float:
        """Backward compatibility: return similarity_threshold as 'threshold'."""
        return self.similarity_threshold
    
    @property
    def metadata_filter_alias(self) -> Optional[Dict[str, Any]]:
        """Backward compatibility: return filters as 'metadata_filter'."""
        return self.filters


@dataclass
class SearchResult:
    """
    Unified search result model - SSOT for all vector/search operations.
    
    This is the single source of truth for search results across the codebase.
    Supports all result variants with backward compatibility.
    
    <!-- SSOT Domain: data -->
    """

    # Core required fields (from most common variants)
    document_id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Optional fields for different use cases
    # Web/UI fields
    id: Optional[str] = None  # Alias for document_id (web models)
    title: Optional[str] = None  # Web models
    collection: Optional[str] = None  # Web models
    tags: List[str] = field(default_factory=list)  # Web models
    size: Optional[str] = None  # Web models
    created_at: Optional[str] = None  # Web models (string format)
    updated_at: Optional[str] = None  # Web models (string format)
    
    # Intelligent context fields
    result_id: Optional[str] = None  # Alias for document_id (context models)
    source_type: Optional[str] = None  # Context models
    source_id: Optional[str] = None  # Context models
    relevance_score: Optional[float] = None  # Alias for similarity_score
    description: Optional[str] = None  # Unified context
    context_type: Optional[Any] = None  # Unified context
    timestamp: Optional[datetime] = None  # Context models
    
    # Vector document reference (for core vector_database variant)
    document: Optional['VectorDocument'] = None  # Core variant uses document object
    
    # Score aliases
    score: Optional[float] = None  # Alias for similarity_score
    relevance: Optional[float] = None  # Alias for similarity_score
    
    def __post_init__(self):
        """Initialize backward compatibility fields."""
        # Map id to document_id if provided
        if self.id is not None and self.document_id == "":
            self.document_id = self.id
        
        # Map result_id to document_id if provided
        if self.result_id is not None and self.document_id == "":
            self.document_id = self.result_id
        
        # Map score to similarity_score if provided
        if self.score is not None and self.similarity_score == 0.0:
            self.similarity_score = self.score
        
        # Map relevance/relevance_score to similarity_score if provided
        if self.relevance is not None and self.similarity_score == 0.0:
            self.similarity_score = self.relevance
        if self.relevance_score is not None and self.similarity_score == 0.0:
            self.similarity_score = self.relevance_score
        
        # Ensure metadata is a dict
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def id_alias(self) -> str:
        """Backward compatibility: return document_id as 'id'."""
        return self.document_id
    
    @property
    def result_id_alias(self) -> str:
        """Backward compatibility: return document_id as 'result_id'."""
        return self.document_id
    
    @property
    def score_alias(self) -> float:
        """Backward compatibility: return similarity_score as 'score'."""
        return self.similarity_score
    
    @property
    def relevance_alias(self) -> float:
        """Backward compatibility: return similarity_score as 'relevance'."""
        return self.similarity_score
    
    @property
    def relevance_score_alias(self) -> float:
        """Backward compatibility: return similarity_score as 'relevance_score'."""
        return self.similarity_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with all fields using SSOT utility."""
        result = to_dict(self)
        
        # Add optional fields if present (custom logic preserved)
        if self.id:
            result["id"] = self.id
        if self.title:
            result["title"] = self.title
        if self.collection:
            result["collection"] = self.collection
        if self.tags:
            result["tags"] = self.tags
        if self.size:
            result["size"] = self.size
        if self.created_at:
            result["created_at"] = self.created_at
        if self.updated_at:
            result["updated_at"] = self.updated_at
        if self.result_id:
            result["result_id"] = self.result_id
        if self.source_type:
            result["source_type"] = self.source_type
        if self.source_id:
            result["source_id"] = self.source_id
        if self.relevance_score is not None:
            result["relevance_score"] = self.relevance_score
        if self.description:
            result["description"] = self.description
        if self.context_type:
            result["context_type"] = self.context_type
        if self.timestamp:
            result["timestamp"] = self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp
        if self.document:
            result["document"] = self.document.to_dict() if hasattr(self.document, 'to_dict') else str(self.document)
        if self.score is not None:
            result["score"] = self.score
        if self.relevance is not None:
            result["relevance"] = self.relevance
        
        return result


@dataclass
class SimilaritySearchResult:
    """Result of similarity search."""

    query_embedding: List[float]
    results: List[Dict[str, Any]]
    search_time: float
    total_candidates: int
