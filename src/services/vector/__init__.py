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

# Lazy imports for vector database functionality to prevent system initialization
import importlib

VECTOR_SERVICES_AVAILABLE = False
LocalVectorStore = None
VectorDatabaseService = None

def _lazy_import_vector_services():
    """Lazy import vector services."""
    global VECTOR_SERVICES_AVAILABLE, LocalVectorStore, VectorDatabaseService

    if VECTOR_SERVICES_AVAILABLE:
        return

    try:
        from .vector_database_integration import LocalVectorStore as _LocalVectorStore
        from .vector_database_service import VectorDatabaseService as _VectorDatabaseService

        LocalVectorStore = _LocalVectorStore
        VectorDatabaseService = _VectorDatabaseService
        VECTOR_SERVICES_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️  Vector services not available: {e}")
        VECTOR_SERVICES_AVAILABLE = False

def get_vector_database_service():
    """Get vector database service with lazy loading."""
    _lazy_import_vector_services()
    if VectorDatabaseService:
        return VectorDatabaseService()
    return None

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

