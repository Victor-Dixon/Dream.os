"""
Document Utils
==============

Document CRUD utility functions for vector database operations.

<!-- SSOT Domain: web -->

V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from datetime import datetime, timedelta
from typing import Any

from src.core.unified_logging_system import get_logger
from src.services.vector_database_service_unified import get_vector_database_service

from .models import Document, DocumentRequest, PaginationRequest


class DocumentUtils:
    """Utility functions for document operations."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.service = get_vector_database_service()

    def get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """Retrieve documents with pagination from the vector database."""
        try:
            return self.service.get_documents(request)
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("Failed to get documents: %s", exc)
            return {
                "documents": [],
                "pagination": {
                    "page": request.page,
                    "per_page": request.per_page,
                    "total": 0,
                    "total_pages": 0,
                    "has_prev": False,
                    "has_next": False,
                },
                "total": 0,
            }

    def simulate_get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """Alias maintained for compatibility with previous mock implementation."""
        return self.get_documents(request)

    def simulate_add_document(self, request: DocumentRequest) -> Document:
        """Simulate adding a document."""
        return Document(
            id=f"doc_{int(datetime.now().timestamp())}",
            title=request.title,
            content=request.content,
            collection=request.collection,
            tags=request.tags or [],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            size=f"{len(request.content) / 1000:.1f} KB",
        )

    def simulate_get_document(self, document_id: str) -> Document:
        """Simulate getting a specific document."""
        return Document(
            id=document_id,
            title="Sample Document",
            content="This is a sample document content.",
            collection="agent_system",
            tags=["sample", "test"],
            created_at="2025-01-27T10:00:00Z",
            updated_at="2025-01-27T10:00:00Z",
            size="1.2 KB",
        )

    def simulate_update_document(self, document_id: str, data: dict[str, Any]) -> Document:
        """Simulate updating a document."""
        return Document(
            id=document_id,
            title=data.get("title", "Updated Document"),
            content=data.get("content", "Updated content"),
            collection=data.get("collection", "agent_system"),
            tags=data.get("tags", []),
            created_at="2025-01-27T10:00:00Z",
            updated_at=datetime.now().isoformat(),
            size=f'{len(data.get("content", "")) / 1000:.1f} KB',
        )

    def simulate_delete_document(self, document_id: str) -> bool:
        """Simulate deleting a document."""
        return True
