#!/usr/bin/env python3
"""
Vector Database ChromaDB Operations Module
==========================================

<!-- SSOT Domain: integration -->

ChromaDB-specific operations for vector database service.
Extracted from vector_database_service.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

from typing import Any

from src.services.vector.vector_database_chromadb_helpers import (
    metadata_matches,
    metadata_to_document,
    sort_documents,
)
from src.web.vector_database.models import (
    Collection as WebCollection,
    PaginationRequest,
    SearchRequest,
    SearchResult,
)

try:
    from chromadb.api.models.Collection import Collection as ChromaCollection
except ImportError:
    ChromaCollection = None


def search_chromadb(
    collection: ChromaCollection,
    request: SearchRequest,
) -> list[SearchResult]:
    """Search ChromaDB collection."""
    where_filter = request.filters or None
    try:
        results = collection.query(
            query_texts=[request.query],
            n_results=request.limit,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )
    except Exception as exc:
        return []

    mapped_results: list[SearchResult] = []
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
        document = metadata_to_document(doc_id, content, metadata)
        relevance = 1.0 - distance if distance is not None else 0.0
        mapped_results.append(
            SearchResult(
                id=document.id,
                title=document.title,
                content=document.content,
                collection=document.collection,
                relevance=relevance,
                tags=document.tags,
                created_at=document.created_at,
                updated_at=document.updated_at,
                size=document.size,
                metadata=document.metadata,
                score=relevance,
            )
        )

    return mapped_results


def get_collection_documents(
    collection: ChromaCollection,
    filters: dict[str, Any],
) -> list[dict[str, Any]]:
    """Get all documents in collection."""
    records = collection.get(include=["documents", "metadatas"])
    ids = records.get("ids", [])
    documents = records.get("documents", [])
    metadatas = records.get("metadatas", [])

    mapped_docs: list[dict[str, Any]] = []
    for doc_id, content, metadata in zip(ids, documents, metadatas):
        metadata = metadata or {}
        if filters and not metadata_matches(metadata, filters):
            continue

        document = metadata_to_document(doc_id, content, metadata)
        mapped_docs.append(document.__dict__)

    return mapped_docs


def fetch_documents(
    collection: ChromaCollection,
    request: PaginationRequest,
    filters: dict[str, Any],
) -> dict[str, Any]:
    """Fetch paginated documents from ChromaDB."""
    documents = get_collection_documents(collection, filters)
    documents = sort_documents(documents, request.sort_by, request.sort_order)

    total = len(documents)
    start = max((request.page - 1) * request.per_page, 0)
    end = start + request.per_page
    page_docs = documents[start:end]

    return {
        "documents": page_docs,
        "pagination": {
            "page": request.page,
            "per_page": request.per_page,
            "total": total,
            "total_pages": (total + request.per_page - 1) // request.per_page,
            "has_prev": request.page > 1,
            "has_next": end < total,
        },
        "total": total,
    }


def list_chroma_collections(client: Any) -> list[WebCollection]:
    """List ChromaDB collections."""
    collections: list[WebCollection] = []
    for collection in client.list_collections():
        try:
            count = client.get_collection(collection.name).count()
        except Exception:
            count = 0

        metadata = getattr(collection, "metadata", {}) or {}
        collections.append(
            WebCollection(
                id=collection.name,
                name=collection.name,
                document_count=count,
                description=metadata.get("description", ""),
                last_updated=metadata.get("last_updated", ""),
                metadata=metadata,
            )
        )
    return collections

