"""Unified Vector Database Service.

Bridges the ChromaDB-powered persistent store (when available) with a
local fallback store so higher-level utilities always interact with a
consistent interface. Provides concrete implementations for search,
document pagination, collection listing, export, and document indexing.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from threading import Lock
from typing import Any, Iterable

try:  # Optional dependency
    import chromadb
    from chromadb.api.models.Collection import Collection as ChromaCollection
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
except ImportError:  # pragma: no cover - optional dependency
    chromadb = None
    SentenceTransformerEmbeddingFunction = None
    ChromaCollection = None

from src.core.unified_logging_system import get_logger
from src.services.models.vector_models import VectorDocument
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
DEFAULT_COLLECTION = "agent_cellphone_v2"
_SERVICE_INSTANCE: "VectorDatabaseService | None" = None
_SERVICE_LOCK = Lock()


@dataclass(slots=True)
class VectorOperationResult:
    """Represents the outcome of a vector database write operation."""

    success: bool
    message: str = ""
    metadata: dict[str, Any] | None = None


class LocalVectorStore:
    """Lightweight fallback store backed by project artifacts."""

    def __init__(self) -> None:
        self.logger = get_logger(f"{__name__}.LocalVectorStore")
        self.documents: dict[str, Document] = {}
        self._load_documents()

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
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
        doc = self._vector_document_to_document(document, collection_name)
        self.documents[doc.id] = doc
        return VectorOperationResult(success=True, message="Indexed in local store")

    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _load_documents(self) -> None:
        loaded = self._load_agent_status_documents()
        loaded += self._load_message_history_documents()
        if loaded == 0:
            self.logger.warning("Local vector store is empty; results may be limited")

    def _load_agent_status_documents(self) -> int:
        count = 0
        for status_file in Path("agent_workspaces").glob("Agent-*/status.json"):
            try:
                data = json.loads(status_file.read_text(encoding="utf-8"))
            except Exception as exc:  # pragma: no cover - corrupted file
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
        count = 0
        message_file = Path("data/message_history.json")
        if not message_file.exists():
            return count

        try:
            data = json.loads(message_file.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover
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
        for document in self.documents.values():
            if collection not in ("all", "default") and document.collection != collection:
                continue
            yield document

    def _sort_documents(
        self, documents: list[Document], sort_by: str, sort_order: str
    ) -> list[Document]:
        reverse = sort_order.lower() == "desc"
        try:
            return sorted(documents, key=lambda doc: getattr(doc, sort_by, ""), reverse=reverse)
        except Exception:  # pragma: no cover - defensive
            return documents

    def _document_to_result(self, document: Document, score: float) -> SearchResult:
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
        if not documents:
            return ""

        # Flatten metadata keys for csv export.
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


class VectorDatabaseService:
    """Unified interface that prefers ChromaDB but gracefully degrades."""

    def __init__(
        self,
        persist_path: str = "data/vector_db",
        default_collection: str = DEFAULT_COLLECTION,
    ) -> None:
        self.logger = LOGGER
        self.persist_path = Path(persist_path)
        self.default_collection = default_collection
        self._client: chromadb.Client | None = None
        self._embedding_function: SentenceTransformerEmbeddingFunction | None = None
        self._collection_cache: dict[str, Any] = {}
        self._fallback_store: LocalVectorStore | None = None
        self._initialize_client()

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    def search(self, request: SearchRequest) -> list[SearchResult]:
        if self._client:
            return self._search_chromadb(request)
        if self._fallback_store:
            return self._fallback_store.search(request)
        raise RuntimeError("Vector database is not available")  # pragma: no cover

    def get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        if self._client:
            documents = self._fetch_documents(request)
            return documents
        if self._fallback_store:
            return self._fallback_store.get_documents(request)
        raise RuntimeError("Vector database is not available")  # pragma: no cover

    def list_collections(self) -> list[WebCollection]:
        if self._client:
            return self._list_chroma_collections()
        if self._fallback_store:
            return self._fallback_store.list_collections()
        return []

    def export_collection(self, request: ExportRequest) -> ExportData:
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
        raise RuntimeError("Vector database is not available")  # pragma: no cover

    def add_document(
        self, document: VectorDocument, collection_name: str | None = None
    ) -> VectorOperationResult:
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
            except Exception as exc:  # pragma: no cover - external dependency
                self.logger.error("Failed to add document to ChromaDB: %s", exc)
                return VectorOperationResult(success=False, message=str(exc))

        if self._fallback_store:
            return self._fallback_store.add_document(document, collection)
        return VectorOperationResult(success=False, message="Vector database unavailable")

    # ------------------------------------------------------------------ #
    # Initialization helpers                                             #
    # ------------------------------------------------------------------ #
    def _initialize_client(self) -> None:
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
        except Exception as exc:  # pragma: no cover - depends on host tooling
            self.logger.warning("Falling back to local store: %s", exc)
            self._client = None
            self._fallback_store = LocalVectorStore()

    def _build_embedding_function(self) -> SentenceTransformerEmbeddingFunction | None:
        if SentenceTransformerEmbeddingFunction is None:  # pragma: no cover
            self.logger.warning("sentence-transformers not available")
            return None

        try:
            return SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        except Exception as exc:  # pragma: no cover
            self.logger.warning("Failed to initialize embedding model: %s", exc)
            return None

    # ------------------------------------------------------------------ #
    # ChromaDB helpers                                                   #
    # ------------------------------------------------------------------ #
    def _resolve_collection_name(self, name: str | None) -> str:
        if not name or name in ("all", "default"):
            return self.default_collection
        return name

    def _get_collection(self, name: str) -> ChromaCollection:
        resolved = self._resolve_collection_name(name)
        if resolved not in self._collection_cache:
            self._collection_cache[resolved] = self._client.get_or_create_collection(  # type: ignore[arg-type]
                name=resolved,
                embedding_function=self._embedding_function,
            )
        return self._collection_cache[resolved]

    def _search_chromadb(self, request: SearchRequest) -> list[SearchResult]:
        collection = self._get_collection(request.collection)
        where_filter = request.filters or None
        try:
            results = collection.query(
                query_texts=[request.query],
                n_results=request.limit,
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as exc:  # pragma: no cover
            self.logger.error("ChromaDB query failed: %s", exc)
            return []

        # Chroma returns lists nested by query.
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
        collections: list[WebCollection] = []
        for collection in self._client.list_collections():  # type: ignore[union-attr]
            try:
                count = self._client.get_collection(collection.name).count()  # type: ignore[union-attr]
            except Exception:  # pragma: no cover
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
        for key, expected in filters.items():
            if metadata.get(key) != expected:
                return False
        return True

    @staticmethod
    def _metadata_to_document(
        doc_id: str, content: str | None, metadata: dict[str, Any]
    ) -> Document:
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
        reverse = sort_order.lower() == "desc"
        try:
            return sorted(documents, key=lambda doc: doc.get(sort_by, ""), reverse=reverse)
        except Exception:  # pragma: no cover
            return documents

    @staticmethod
    def _to_csv(documents: list[dict[str, Any]]) -> str:
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

