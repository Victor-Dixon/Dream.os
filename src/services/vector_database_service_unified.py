#!/usr/bin/env python3
"""
UNIFIED VECTOR DATABASE SERVICE - Backward Compatibility Shim
=============================================================

<!-- SSOT Domain: integration -->

Backward compatibility shim for vector_database_service_unified.py.
All functionality has been extracted to src/services/vector/ modules.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

# Import all public APIs from vector module for backward compatibility
try:
    from .vector import (
        # Integration Layer
        LocalVectorStore,
        # Service Core
        VectorDatabaseService,
        # Helpers
        VectorOperationResult,
        DEFAULT_COLLECTION,
        # Factory
        get_vector_database_service,
    )
    VECTOR_DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Vector database not available: {e}")
    # Provide dummy implementations
    LocalVectorStore = None
    VectorDatabaseService = None
    VectorOperationResult = None
    DEFAULT_COLLECTION = "default"
    def get_vector_database_service():
        return None
    VECTOR_DATABASE_AVAILABLE = False

__all__ = [
    # Integration Layer
    "LocalVectorStore",
    # Service Core
    "VectorDatabaseService",
    # Helpers
    "VectorOperationResult",
    "DEFAULT_COLLECTION",
    # Factory
    "get_vector_database_service",
]
