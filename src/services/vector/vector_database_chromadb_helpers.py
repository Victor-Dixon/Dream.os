#!/usr/bin/env python3
"""
Vector Database ChromaDB Helpers Module
========================================

<!-- SSOT Domain: integration -->

Helper functions for ChromaDB operations.
Extracted from vector_database_service.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import json
from typing import Any

from src.services.vector.vector_database_helpers import DEFAULT_COLLECTION
from src.web.vector_database.models import Document


def metadata_matches(metadata: dict[str, Any], filters: dict[str, Any]) -> bool:
    """Check if metadata matches filters."""
    for key, expected in filters.items():
        if metadata.get(key) != expected:
            return False
    return True


def metadata_to_document(
    doc_id: str, content: str | None, metadata: dict[str, Any]
) -> Document:
    """Convert metadata to Document."""
    content_value = content or metadata.get("content", "")
    title = metadata.get("title", doc_id)
    collection_name = metadata.get("collection", metadata.get("category", DEFAULT_COLLECTION))
    return Document(
        id=doc_id,
        title=title,
        content=content_value,
        collection=collection_name,
        tags=metadata.get("tags", []),
        size=metadata.get("size", f"{len(content_value) / 1024:.1f} KB"),
        created_at=metadata.get("created_at", metadata.get("timestamp", "")),
        updated_at=metadata.get("updated_at", metadata.get("last_updated", "")),
        metadata=metadata,
    )


def sort_documents(
    documents: list[dict[str, Any]], sort_by: str, sort_order: str
) -> list[dict[str, Any]]:
    """Sort documents by field."""
    reverse = sort_order.lower() == "desc"
    try:
        return sorted(documents, key=lambda doc: doc.get(sort_by, ""), reverse=reverse)
    except Exception:
        return documents


def to_csv(documents: list[dict[str, Any]]) -> str:
    """Convert documents to CSV format."""
    if not documents:
        return ""
    headers = set()
    for doc in documents:
        headers.update(doc.keys())
    ordered_headers = sorted(headers)
    lines = [",".join(ordered_headers)]
    for doc in documents:
        row = []
        for header in ordered_headers:
            value = doc.get(header, "")
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            row.append(str(value).replace("\n", " ").replace(",", ";"))
        lines.append(",".join(row))
    return "\n".join(lines)

