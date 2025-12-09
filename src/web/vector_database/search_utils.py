"""
Search Utils
============

Search-related utility functions for vector database operations.

<!-- SSOT Domain: web -->

V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from src.core.unified_logging_system import get_logger
from src.services.vector_database_service_unified import get_vector_database_service

from .models import SearchRequest
# Use SSOT SearchResult - supports all web model fields (id, title, collection, tags, etc.)
from src.services.models.vector_models import SearchResult


class SearchUtils:
    """Utility functions for search operations."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.service = get_vector_database_service()

    def search_vector_database(self, request: SearchRequest) -> list[SearchResult]:
        """Perform a real vector database search."""
        try:
            return self.service.search(request)
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("Vector search failed: %s", exc)
            return []

    # Backwards compatibility for older callers referencing the mock function name.
    def simulate_vector_search(self, request: SearchRequest) -> list[SearchResult]:
        """Alias maintained for compatibility with older handlers."""
        return self.search_vector_database(request)
