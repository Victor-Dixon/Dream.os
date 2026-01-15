#!/usr/bin/env python3
"""
Vector Database Integration Module
===================================

<!-- SSOT Domain: integration -->

Integration layer for vector database operations.
Handles LocalVectorStore fallback implementation.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable



from src.services.models.vector_models import VectorDocument
from src.services.vector.vector_database_helpers import (
    DEFAULT_COLLECTION,
    VectorOperationResult,
)
from src.web.vector_database.models import (
    Collection as WebCollection,
    Document,
    ExportData,
    ExportRequest,
    PaginationRequest,
    SearchRequest,
    SearchResult,
)


class LocalVectorStore:
    """Lightweight fallback store backed by project artifacts."""

    def __init__(self) -> None:
        self.logger = get_logger(f"{__name__}.LocalVectorStore")
        self.documents: dict[str, Document] = {}
        self._load_documents()

    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Return fuzzy matches when the real vector db is unavailable."""
        scored_results: list[tuple[float, SearchResult]] = []
        for document in self._iter_documents(request.collection):
            score = SequenceMatcher(
                None, request.query.lower(), document.content.lower()
            ).ratio()
            scored_results.append((score, self._document_to_result(document, score)))

        scored_results.sort(key=lambda item: item[0], reverse=True)
        return [result for _, result in scored_results[: request.limit]]

    def get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """Get paginated documents."""
        docs = list(self._iter_documents(request.collection))
        docs = self._sort_documents(docs, request.sort_by, request.sort_order)

        total = len(docs)
        start = max((request.page - 1) * request.per_page, 0)
        end = start + request.per_page
        page_docs = docs[start:end]

        return {
            "documents": [doc.__dict__ for doc in page_docs],
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

    def list_collections(self) -> list[WebCollection]:
        """List all collections."""
        counts: dict[str, list[Document]] = defaultdict(list)
        for doc in self.documents.values():
            counts[doc.collection].append(doc)

        collections: list[WebCollection] = []
        for name, docs in counts.items():
            last_updated = max((doc.updated_at for doc in docs), default="")
            collections.append(
                WebCollection(
                    id=name,
                    name=name.replace("_", " ").title(),
                    document_count=len(docs),
                    description=f"Local fallback collection: {name}",
                    last_updated=last_updated,
                    metadata={"source": "local_fallback"},
                )
            )
        return collections

    def export_collection(self, request: ExportRequest) -> ExportData:
        """Export collection data."""
        docs = [doc.__dict__ for doc in self._iter_documents(request.collection)]
        payload = (
            self._to_csv(docs) if request.format.lower() == "csv" else json.dumps(docs, indent=2)
        )
        filename = (
            f"{request.collection}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            f".{request.format}"
        )
        return ExportData(
            collection=request.collection,
            format=request.format,
            data=payload,
            filename=filename,
            size=f"{len(payload) / 1024:.1f} KB",
            generated_at=datetime.utcnow().isoformat(),
        )

    def add_document(
        self, document: VectorDocument, collection_name: str | None = None
    ) -> VectorOperationResult:
        """Add document to local store."""
        doc = self._vector_document_to_document(document, collection_name)
        self.documents[doc.id] = doc
        return VectorOperationResult(success=True, message="Indexed in local store")

    def _load_documents(self) -> None:
        """Load documents from project artifacts."""
        loaded = self._load_agent_status_documents()
        loaded += self._load_message_history_documents()
        if loaded == 0:
            self.logger.warning("Local vector store is empty; results may be limited")

    def _load_agent_status_documents(self) -> int:
        """Load agent status documents."""
        count = 0
        for status_file in Path("agent_workspaces").glob("Agent-*/status.json"):
            try:
                data = json.loads(status_file.read_text(encoding="utf-8"))
            except Exception as exc:
                self.logger.warning("Failed to read %s: %s", status_file, exc)
                continue

            agent_id = status_file.parent.name
            document = Document(
                id=f"{agent_id}_status",
                title=f"{agent_id} Status",
                content=json.dumps(data, indent=2),
                collection="agent_status",
                tags=[agent_id, "status"],
                size=f"{status_file.stat().st_size / 1024:.1f} KB",
                created_at=data.get("last_updated", ""),
                updated_at=data.get("last_updated", ""),
                metadata=data,
            )
            self.documents[document.id] = document
            count += 1
        return count

    def _load_message_history_documents(self) -> int:
        """Load message history documents."""
        count = 0
        message_file = Path("data/message_history.json")
        if not message_file.exists():
            return count

        try:
            data = json.loads(message_file.read_text(encoding="utf-8"))
        except Exception as exc:
            self.logger.warning("Failed to read message history: %s", exc)
            return count

        for entry in data.get("messages", []):
            content = entry.get("content", "")
            doc_id = entry.get("message_id") or f"message_{count}"
            document = Document(
                id=doc_id,
                title=f"Message {doc_id}",
                content=content,
                collection="messages",
                tags=[
                    entry.get("from", "unknown"),
                    entry.get("to", "unknown"),
                    entry.get("priority", "regular"),
                ],
                size=f"{len(content) / 1024:.1f} KB",
                created_at=entry.get("timestamp", ""),
                updated_at=entry.get("timestamp", ""),
                metadata=entry,
            )
            self.documents[document.id] = document
            count += 1

        return count

    def _iter_documents(self, collection: str) -> Iterable[Document]:
        """Iterate over documents in collection."""
        for document in self.documents.values():
            if collection not in ("all", "default") and document.collection != collection:
                continue
            yield document

    def _sort_documents(
        self, documents: list[Document], sort_by: str, sort_order: str
    ) -> list[Document]:
        """Sort documents by field."""
        reverse = sort_order.lower() == "desc"
        try:
            return sorted(documents, key=lambda doc: getattr(doc, sort_by, ""), reverse=reverse)
        except Exception:
            return documents

    def _document_to_result(self, document: Document, score: float) -> SearchResult:
        """Convert document to search result."""
        return SearchResult(
            id=document.id,
            title=document.title,
            content=document.content,
            collection=document.collection,
            relevance=score,
            tags=document.tags,
            created_at=document.created_at,
            updated_at=document.updated_at,
            size=document.size,
            metadata=document.metadata,
            score=score,
        )

    @staticmethod
    def _to_csv(documents: list[dict[str, Any]]) -> str:
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

    @staticmethod
    def _vector_document_to_document(
        document: VectorDocument, collection_name: str | None
    ) -> Document:
        """Convert VectorDocument to Document."""
        metadata = document.metadata or {}
        collection = metadata.get("collection") or collection_name or DEFAULT_COLLECTION
        timestamp = datetime.utcnow().isoformat()
        return Document(
            id=document.id,
            title=metadata.get("title", document.id),
            content=document.content,
            collection=collection,
            tags=metadata.get("tags", []),
            size=metadata.get("size", f"{len(document.content) / 1024:.1f} KB"),
            created_at=metadata.get("created_at", timestamp),
            updated_at=metadata.get("updated_at", timestamp),
            metadata=metadata,
            embedding=document.embedding,
        )

