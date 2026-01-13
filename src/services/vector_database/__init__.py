#!/usr/bin/env python3
"""
Vector Database Service - SSOT for Vector DB Imports
====================================================

Provides single source of truth for vector database imports.
Consolidates duplicate import patterns across services.

<!-- SSOT Domain: services -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

from typing import Optional, List, Any

# Try to import vector database service and SSOT SearchQuery
try:
    from ..vector_database_service_unified import (
        get_vector_database_service,
        search_vector_database,
    )
    from ..models.vector_models import SearchQuery
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    
    # Fallback implementations
    def get_vector_database_service() -> None:
        """Fallback when vector DB unavailable."""
        return None
    
    def search_vector_database(query: Any) -> List[Any]:
        """Fallback when vector DB unavailable."""
        return []
    
    # Try to import SSOT SearchQuery even if vector DB service unavailable
    try:
        from ..models.vector_models import SearchQuery
    except ImportError:
        # Create minimal SearchQuery for type hints (last resort fallback)
        from dataclasses import dataclass
        
        @dataclass
        class SearchQuery:
            """
            Minimal SearchQuery for fallback - use SSOT when available.
            
            DEPRECATED: This is a last-resort fallback. Use src.services.models.vector_models.SearchQuery instead.
            """
            query: str = ""
            limit: int = 10


__all__ = [
    "get_vector_database_service",
    "search_vector_database",
    "SearchQuery",
    "VECTOR_DB_AVAILABLE",
]


