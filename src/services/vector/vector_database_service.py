#!/usr/bin/env python3
"""
Vector Database Service Module
===============================

<!-- SSOT Domain: integration -->

Service core for vector database operations.
Handles ChromaDB integration and fallback to LocalVectorStore.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

try:
    import chromadb
    from chromadb.api.models.Collection import Collection as ChromaCollection
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
except ImportError:
    chromadb = None
    SentenceTransformerEmbeddingFunction = None
    ChromaCollection = None

from src.core.base.base_service import BaseService
from src.core.unified_logging_system import get_logger
from src.services.models.vector_models import VectorDocument
from src.services.vector.vector_database_helpers import (
    DEFAULT_COLLECTION,
    VectorOperationResult,
)
from src.services.vector.vector_database_integration import LocalVectorStore
from src.web.vector_database.models import (
    Collection as WebCollection,
    Document,
    ExportData,
    ExportRequest,
    PaginationRequest,
    SearchRequest,
    SearchResult,
)

LOGGER = get_logger(__name__)
_SERVICE_INSTANCE: "VectorDatabaseService | None" = None
_SERVICE_LOCK = Lock()


class VectorDatabaseService(BaseService):
    """Unified interface that prefers ChromaDB but gracefully degrades."""

    def __init__(
        self,
        persist_path: str = "data/vector_db",
        default_collection: str = DEFAULT_COLLECTION,
    ) -> None:
        super().__init__("VectorDatabaseService")
        self.persist_path = Path(persist_path)
        self.default_collection = default_collection
        self._client: chromadb.Client | None = None
        self._embedding_function: SentenceTransformerEmbeddingFunction | None = None
        self._collection_cache: dict[str, Any] = {}
        self._fallback_store: LocalVectorStore | None = None
        self._initialize_client()

    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Search documents."""
        if self._client:
            return self._search_chromadb(request)
        if self._fallback_store:
            return self._fallback_store.search(request)
        raise RuntimeError("Vector database is not available")

    def get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """Get paginated documents."""
        if self._client:
            documents = self._fetch_documents(request)
            return documents
        if self._fallback_store:
            return self._fallback_store.get_documents(request)
        raise RuntimeError("Vector database is not available")

    def list_collections(self) -> list[WebCollection]:
        """List all collections."""
        if self._client:
            return self._list_chroma_collections()
        if self._fallback_store:
            return self._fallback_store.list_collections()
        return []

    def export_collection(self, request: ExportRequest) -> ExportData:
        """Export collection data."""
        if self._client:
            documents = self._get_collection_documents(request.collection, request.filters or {})
            body = (
                self._to_csv(documents)
                if request.format.lower() == "csv"
                else json.dumps(documents, indent=2)
            )
            filename = (
                f"{request.collection}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}."
                f"{request.format}"
            )
            return ExportData(
                collection=request.collection,
                format=request.format,
                data=body,
                filename=filename,
                size=f"{len(body) / 1024:.1f} KB",
                generated_at=datetime.utcnow().isoformat(),
            )
        if self._fallback_store:
            return self._fallback_store.export_collection(request)
        raise RuntimeError("Vector database is not available")

    def add_document(
        self, document: VectorDocument, collection_name: str | None = None
    ) -> VectorOperationResult:
        """Add document to vector database."""
        collection = collection_name or self.default_collection
        if self._client:
            try:
                collection_ref = self._get_collection(collection)
                collection_ref.add(
                    ids=[document.id],
                    documents=[document.content],
                    metadatas=[document.metadata or {}],
                    embeddings=[document.embedding]
                    if document.embedding
                    else None,
                )
                return VectorOperationResult(success=True, message="Document indexed")
            except Exception as exc:
                self.logger.error("Failed to add document to ChromaDB: %s", exc)
                return VectorOperationResult(success=False, message=str(exc))

        if self._fallback_store:
            return self._fallback_store.add_document(document, collection)
        return VectorOperationResult(success=False, message="Vector database unavailable")

    def _initialize_client(self) -> None:
        """Initialize ChromaDB client or fallback store."""
        if chromadb is None:
            self.logger.info("chromadb not installed; using local fallback store")
            self._fallback_store = LocalVectorStore()
            return

        try:
            self._embedding_function = self._build_embedding_function()
            if self._embedding_function is None:
                raise RuntimeError("SentenceTransformer embeddings unavailable")

            self._client = chromadb.PersistentClient(path=str(self.persist_path))
            self.logger.info("Connected to ChromaDB at %s", self.persist_path)
        except Exception as exc:
            self.logger.warning("Falling back to local store: %s", exc)
            self._client = None
            self._fallback_store = LocalVectorStore()

    def _build_embedding_function(self) -> SentenceTransformerEmbeddingFunction | None:
        """Build embedding function."""
        if SentenceTransformerEmbeddingFunction is None:
            self.logger.warning("sentence-transformers not available")
            return None

        try:
            return SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        except Exception as exc:
            self.logger.warning("Failed to initialize embedding model: %s", exc)
            return None

    def _resolve_collection_name(self, name: str | None) -> str:
        """Resolve collection name."""
        if not name or name in ("all", "default"):
            return self.default_collection
        return name

    def _get_collection(self, name: str) -> ChromaCollection:
        """Get or create collection."""
        resolved = self._resolve_collection_name(name)
        if resolved not in self._collection_cache:
            self._collection_cache[resolved] = self._client.get_or_create_collection(  # type: ignore[arg-type]
                name=resolved,
                embedding_function=self._embedding_function,
            )
        return self._collection_cache[resolved]

    def _search_chromadb(self, request: SearchRequest) -> list[SearchResult]:
        """Search ChromaDB."""
        collection = self._get_collection(request.collection)
        where_filter = request.filters or None
        try:
            results = collection.query(
                query_texts=[request.query],
                n_results=request.limit,
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as exc:
            self.logger.error("ChromaDB query failed: %s", exc)
            return []

        mapped_results: list[SearchResult] = []
        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
            document = self._metadata_to_document(doc_id, content, metadata)
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

    def _fetch_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """Fetch paginated documents."""
        documents = self._get_collection_documents(request.collection, request.filters or {})
        documents = self._sort_documents(documents, request.sort_by, request.sort_order)

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

    def _get_collection_documents(
        self, collection_name: str, filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Get all documents in collection."""
        collection = self._get_collection(collection_name)
        records = collection.get(include=["documents", "metadatas"])
        ids = records.get("ids", [])
        documents = records.get("documents", [])
        metadatas = records.get("metadatas", [])

        mapped_docs: list[dict[str, Any]] = []
        for doc_id, content, metadata in zip(ids, documents, metadatas):
            metadata = metadata or {}
            if filters and not self._metadata_matches(metadata, filters):
                continue

            document = self._metadata_to_document(doc_id, content, metadata)
            mapped_docs.append(document.__dict__)

        return mapped_docs

    def _list_chroma_collections(self) -> list[WebCollection]:
        """List ChromaDB collections."""
        collections: list[WebCollection] = []
        for collection in self._client.list_collections():  # type: ignore[union-attr]
            try:
                count = self._client.get_collection(collection.name).count()  # type: ignore[union-attr]
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

    @staticmethod
    def _metadata_matches(metadata: dict[str, Any], filters: dict[str, Any]) -> bool:
        """Check if metadata matches filters."""
        for key, expected in filters.items():
            if metadata.get(key) != expected:
                return False
        return True

    @staticmethod
    def _metadata_to_document(
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

    @staticmethod
    def _sort_documents(
        documents: list[dict[str, Any]], sort_by: str, sort_order: str
    ) -> list[dict[str, Any]]:
        """Sort documents by field."""
        reverse = sort_order.lower() == "desc"
        try:
            return sorted(documents, key=lambda doc: doc.get(sort_by, ""), reverse=reverse)
        except Exception:
            return documents

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


def get_vector_database_service() -> VectorDatabaseService:
    """Return a shared instance of the vector database service."""
    global _SERVICE_INSTANCE
    if _SERVICE_INSTANCE is None:
        with _SERVICE_LOCK:
            if _SERVICE_INSTANCE is None:
                _SERVICE_INSTANCE = VectorDatabaseService()
    return _SERVICE_INSTANCE

