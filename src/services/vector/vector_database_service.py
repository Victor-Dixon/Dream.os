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
from src.services.vector.vector_database_chromadb_helpers import to_csv
from src.services.vector.vector_database_chromadb_operations import (
    fetch_documents as _fetch_documents_chromadb,
    get_collection_documents as _get_collection_documents_chromadb,
    list_chroma_collections as _list_chroma_collections,
    search_chromadb as _search_chromadb,
)
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
            collection = self._get_collection(request.collection)
            return _search_chromadb(collection, request)
        if self._fallback_store:
            return self._fallback_store.search(request)
        raise RuntimeError("Vector database is not available")

    def get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """Get paginated documents."""
        if self._client:
            collection = self._get_collection(request.collection)
            return _fetch_documents_chromadb(collection, request, request.filters or {})
        if self._fallback_store:
            return self._fallback_store.get_documents(request)
        raise RuntimeError("Vector database is not available")

    def list_collections(self) -> list[WebCollection]:
        """List all collections."""
        if self._client:
            return _list_chroma_collections(self._client)
        if self._fallback_store:
            return self._fallback_store.list_collections()
        return []

    def export_collection(self, request: ExportRequest) -> ExportData:
        """Export collection data."""
        if self._client:
            collection = self._get_collection(request.collection)
            documents = _get_collection_documents_chromadb(collection, request.filters or {})
            body = (
                to_csv(documents)
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




def get_vector_database_service() -> VectorDatabaseService:
    """Return a shared instance of the vector database service."""
    global _SERVICE_INSTANCE
    if _SERVICE_INSTANCE is None:
        with _SERVICE_LOCK:
            if _SERVICE_INSTANCE is None:
                _SERVICE_INSTANCE = VectorDatabaseService()
    return _SERVICE_INSTANCE

