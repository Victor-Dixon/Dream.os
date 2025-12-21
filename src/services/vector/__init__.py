#!/usr/bin/env python3
"""
Vector Database Module - Public API Exports
===========================================

<!-- SSOT Domain: integration -->

Public API exports for vector database service.
Extracted from vector_database_service_unified.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

# Integration Layer
from .vector_database_integration import LocalVectorStore

# Service Core
from .vector_database_service import VectorDatabaseService

# Helpers
from .vector_database_helpers import (
    VectorOperationResult,
    DEFAULT_COLLECTION,
)
from .vector_database_chromadb_helpers import (
    metadata_matches,
    metadata_to_document,
    sort_documents,
    to_csv,
)

# Factory function
from .vector_database_service import get_vector_database_service

__all__ = [
    # Integration Layer
    "LocalVectorStore",
    # Service Core
    "VectorDatabaseService",
    # Helpers
    "VectorOperationResult",
    "DEFAULT_COLLECTION",
    # ChromaDB Helpers
    "metadata_matches",
    "metadata_to_document",
    "sort_documents",
    "to_csv",
    # Factory
    "get_vector_database_service",
]

