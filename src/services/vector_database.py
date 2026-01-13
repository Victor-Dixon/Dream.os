"""
Vector Database Service - Redirect Shim
======================================

Redirects imports from `src.services.vector_database` to the unified service.
This maintains backward compatibility for code expecting the old import path.

<!-- SSOT Domain: integration -->

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

# Redirect all imports to the unified service
from .vector_database_service_unified import (
    VectorDatabaseService,
    get_vector_database_service,
    VectorOperationResult,
)

# Re-export for backward compatibility
__all__ = [
    "VectorDatabaseService",
    "get_vector_database_service",
    "VectorOperationResult",
]

