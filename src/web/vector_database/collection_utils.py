"""
Collection Utils
================

Collection management utility functions for vector database operations.

<!-- SSOT Domain: web -->

V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from src.core.unified_logging_system import get_logger
from src.services.vector_database_service_unified import get_vector_database_service

from .models import Collection, ExportData, ExportRequest


class CollectionUtils:
    """Utility functions for collection operations."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.service = get_vector_database_service()

    def get_collections(self) -> list[Collection]:
        """Retrieve collections from the vector database."""
        try:
            return self.service.list_collections()
        except Exception as exc:  # pragma: no cover
            self.logger.error("Failed to load collections: %s", exc)
            return []

    def simulate_get_collections(self) -> list[Collection]:
        """Alias maintained for compatibility with previous mock implementation."""
        return self.get_collections()

    def export_data(self, request: ExportRequest) -> ExportData:
        """Export collection data using the vector database service."""
        try:
            return self.service.export_collection(request)
        except Exception as exc:  # pragma: no cover
            self.logger.error("Failed to export data: %s", exc)
            raise

    def simulate_export_data(self, request: ExportRequest) -> ExportData:
        """Alias maintained for compatibility with previous mock implementation."""
        return self.export_data(request)
