#!/usr/bin/env python3
"""Core vector database utilities.

This module provides a minimal SSOT interface for storing agent status
embeddings. It uses SQLite under the hood and exposes helper functions for
interacting with the ``agent_status_embeddings`` table.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Sequence
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field



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


# Backward compatibility shim - use SSOT from src.services.models.vector_models
import warnings
from src.services.models.vector_models import SearchResult as SSOTSearchResult

class SearchResult(SSOTSearchResult):
    """
    Backward compatibility shim for SearchResult - SSOT consolidated.
    
    DEPRECATED: Use src.services.models.vector_models.SearchResult instead.
    This class is maintained for backward compatibility only.
    
    Supports both legacy initialization patterns:
    1. document_id, content, similarity_score, metadata (original pattern)
    2. document (VectorDocument), score, metadata (VectorDocument variant)
    
    <!-- SSOT Domain: data -->
    """
    
    def __init__(self, document_id: str = None, content: str = None, 
                 similarity_score: float = None, metadata: Dict[str, Any] = None,
                 document: 'VectorDocument' = None, score: float = None):
        """Initialize with legacy parameters - supports both patterns."""
        # Handle VectorDocument variant
        if document is not None:
            warnings.warn(
                "SearchResult (VectorDocument variant) is deprecated. "
                "Use src.services.models.vector_models.SearchResult instead. "
                "Use create_search_result_from_document() to convert.",
                DeprecationWarning,
                stacklevel=2
            )
            document_id = document.id
            content = document.content
            similarity_score = score or 0.0
            metadata = metadata or {}
            # Store document reference for backward compatibility
            super().__init__(
                document_id=document_id,
                content=content,
                similarity_score=similarity_score,
                metadata=metadata,
                document=document,
                score=score
            )
        else:
            # Handle standard pattern
            if document_id is None or content is None or similarity_score is None:
                raise ValueError("Either (document_id, content, similarity_score, metadata) or (document, score, metadata) must be provided")
            super().__init__(
                document_id=document_id,
                content=content,
                similarity_score=similarity_score,
                metadata=metadata or {}
            )
    
    def to_ssot(self) -> 'SSOTSearchResult':
        """Convert to SSOT SearchResult (for VectorDocument variant compatibility)."""
        return self


class VectorDocument:
    """Vector document representation."""

    def __init__(self, id: str, content: str, embedding: list, metadata: Dict[str, Any]):
        self.id = id
        self.content = content
        self.embedding = embedding
        self.metadata = metadata


class EmbeddingModel(Enum):
    """Supported embedding models."""
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI_ADA = "openai-ada-002"
    OPENAI_3_SMALL = "openai-3-small"
    OPENAI_3_LARGE = "openai-3-large"


class VectorDatabaseStats:
    """Vector database statistics."""

    def __init__(self):
        self.total_documents = 0
        self.collections = {}

# ---------------------------------------------------------------------------
# Single source of truth constants
# ---------------------------------------------------------------------------
DB_PATH = Path("data/vector_database.db")
AGENT_STATUS_TABLE = "agent_status_embeddings"


@dataclass
class CollectionConfig:
    """Configuration for vector database collections."""

    name: str
    description: str
    embedding_dimension: int
    similarity_threshold: float = 0.7
    max_documents: int = 10000
    metadata: Optional[Dict[str, Any]] = None

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {AGENT_STATUS_TABLE} (
    agent_id TEXT PRIMARY KEY,
    raw_status TEXT NOT NULL,
    embedding TEXT NOT NULL,
    last_updated TEXT NOT NULL
)
"""


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection ensuring the status table exists."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    return conn


# ---------------------------------------------------------------------------
# Agent status embedding operations
# ---------------------------------------------------------------------------


def upsert_agent_status(
    conn: sqlite3.Connection,
    agent_id: str,
    raw_status: str,
    embedding: Sequence[float],
    last_updated: str,
) -> None:
    """Insert or update an agent status embedding."""
    payload = (
        agent_id,
        raw_status,
        json.dumps(list(embedding)),
        last_updated,
    )
    conn.execute(
        f"""
        INSERT INTO {AGENT_STATUS_TABLE}
            (agent_id, raw_status, embedding, last_updated)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET
            raw_status=excluded.raw_status,
            embedding=excluded.embedding,
            last_updated=excluded.last_updated
        """,
        payload,
    )
    conn.commit()


def fetch_agent_status(
    conn: sqlite3.Connection, agent_id: str
) -> tuple[str, str, Sequence[float], str] | None:
    """Fetch a stored agent status embedding."""
    cursor = conn.execute(
        (
            f"SELECT agent_id, raw_status, embedding, last_updated "
            f"FROM {AGENT_STATUS_TABLE} WHERE agent_id=?"
        ),
        (agent_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    stored_id, raw_status, embedding_json, last_updated = row
    return stored_id, raw_status, json.loads(embedding_json), last_updated


@dataclass
class VectorDocument:
    """Document for vector database operations."""

    content: str
    metadata: Dict[str, Any]
    document_id: Optional[str] = None
    document_type: Optional['DocumentType'] = None


class DocumentType(Enum):
    """Document types for vector database."""

    AGENT_STATUS = "agent_status"
    MESSAGE = "message"
    LOG = "log"
    CONFIG = "config"


class EmbeddingModel(Enum):
    """Embedding model types."""

    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI_ADA = "openai_ada"
    OPENAI_3_SMALL = "openai_3_small"
    OPENAI_3_LARGE = "openai_3_large"


# Backward compatibility shim - use SSOT from src.services.models.vector_models
import warnings
from src.services.models.vector_models import SearchQuery as SSOTSearchQuery

@dataclass
class SearchQuery(SSOTSearchQuery):
    """
    Backward compatibility shim for SearchQuery.
    
    DEPRECATED: Use src.services.models.vector_models.SearchQuery instead.
    This class is maintained for backward compatibility only.
    This class will be removed in a future version.
    
    <!-- SSOT Domain: data -->
    """
    
    def __init__(self, query_text: str, limit: int = 10, threshold: float = 0.0, 
                 search_type: Optional['SearchType'] = None, 
                 metadata_filter: Optional[Dict[str, Any]] = None):
        """Initialize with legacy parameters."""
        warnings.warn(
            "SearchQuery from src.core.vector_database is deprecated. "
            "Use src.services.models.vector_models.SearchQuery instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(
            query_text=query_text,
            limit=limit,
            threshold=threshold,  # Maps to similarity_threshold
            search_type=search_type,
            metadata_filter=metadata_filter  # Maps to filters
        )


class SearchType(Enum):
    """Search types for vector operations."""

    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"


# Backward compatibility: Create adapter function for VectorDocument variant
def create_search_result_from_document(document: VectorDocument, score: float, metadata: Dict[str, Any]) -> 'SSOTSearchResult':
    """
    Create SSOT SearchResult from VectorDocument variant.
    
    DEPRECATED: Use SearchResult(document=document, score=score, metadata=metadata) instead.
    This function is maintained for backward compatibility only.
    """
    warnings.warn(
        "create_search_result_from_document() is deprecated. "
        "Use SearchResult(document=document, score=score, metadata=metadata) instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return SearchResult(document=document, score=score, metadata=metadata)


@dataclass
class VectorDatabaseStats:
    """Statistics for vector database operations."""

    total_documents: int
    total_collections: int
    last_updated: Optional[str] = None
    storage_size: Optional[int] = None


__all__ = [
    "AGENT_STATUS_TABLE",
    "CollectionConfig",
    "DocumentType",
    "EmbeddingModel",
    "get_connection",
    "SearchQuery",
    "SearchResult",
    "SearchType",
    "upsert_agent_status",
    "VectorDatabaseStats",
    "VectorDocument",
    "fetch_agent_status",
]
