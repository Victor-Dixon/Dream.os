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

# Lazy imports for vector database to prevent system initialization
import importlib

VECTOR_DATABASE_AVAILABLE = False
LocalVectorStore = None
VectorDatabaseService = None
VectorOperationResult = None
DEFAULT_COLLECTION = "default"

# Global function that will be overridden
get_vector_database_service = lambda: None

def _lazy_import_vector_database():
    """Lazy import vector database functionality."""
    global VECTOR_DATABASE_AVAILABLE, LocalVectorStore, VectorDatabaseService, VectorOperationResult

    if VECTOR_DATABASE_AVAILABLE:
        return

    try:
        from .vector import (
            LocalVectorStore as _LocalVectorStore,
            VectorDatabaseService as _VectorDatabaseService,
            get_vector_database_service as _get_vector_database_service,
        )
        from .vector.vector_database_helpers import VectorOperationResult as _VectorOperationResult, DEFAULT_COLLECTION as _DEFAULT_COLLECTION

        LocalVectorStore = _LocalVectorStore
        VectorDatabaseService = _VectorDatabaseService
        VectorOperationResult = _VectorOperationResult
        DEFAULT_COLLECTION = _DEFAULT_COLLECTION
        VECTOR_DATABASE_AVAILABLE = True
    except ImportError as e:
        # Handle ONNX Runtime and other import issues
        if "onnxruntime" in str(e).lower() or "chromadb" in str(e).lower():
            # Vector services unavailable due to dependencies
            LocalVectorStore = None
            VectorDatabaseService = None
            VectorOperationResult = None
            VECTOR_DATABASE_AVAILABLE = False
        else:
            # Re-raise other import errors
            raise

        # Override the global function
        global get_vector_database_service
        get_vector_database_service = _get_vector_database_service

    except ImportError as e:
        print(f"⚠️  Vector database not available: {e}")
        VECTOR_DATABASE_AVAILABLE = False

# Initialize lazy loading
_lazy_import_vector_database()

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
