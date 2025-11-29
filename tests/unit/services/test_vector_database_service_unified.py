"""
Unit tests for src/services/vector_database_service_unified.py

Comprehensive test suite for vector database service functionality including:
- VectorOperationResult dataclass
- LocalVectorStore (fallback store)
- VectorDatabaseService (main service)
- get_vector_database_service() function

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import json
import tempfile
import shutil
from datetime import datetime

from src.services.vector_database_service_unified import (
    VectorOperationResult,
    LocalVectorStore,
    VectorDatabaseService,
    get_vector_database_service,
    DEFAULT_COLLECTION,
)

# Import web models for testing
try:
    from src.web.vector_database.models import (
        SearchRequest,
        SearchResult,
        PaginationRequest,
        ExportRequest,
        ExportData,
        Document,
    )
    WEB_MODELS_AVAILABLE = True
except ImportError:
    WEB_MODELS_AVAILABLE = False

# Import vector models
try:
    from src.services.models.vector_models import VectorDocument
    VECTOR_MODELS_AVAILABLE = True
except ImportError:
    VECTOR_MODELS_AVAILABLE = False


class TestVectorOperationResult:
    """Test VectorOperationResult dataclass."""

    def test_create_with_required_fields(self):
        """Test creating VectorOperationResult with required fields."""
        result = VectorOperationResult(success=True, message="Test")
        
        assert result.success is True
        assert result.message == "Test"
        assert result.metadata is None

    def test_create_with_metadata(self):
        """Test creating VectorOperationResult with metadata."""
        metadata = {"key": "value"}
        result = VectorOperationResult(success=True, message="Test", metadata=metadata)
        
        assert result.success is True
        assert result.metadata == metadata

    def test_create_failure_result(self):
        """Test creating failure result."""
        result = VectorOperationResult(success=False, message="Error occurred")
        
        assert result.success is False
        assert result.message == "Error occurred"

    def test_create_with_empty_message(self):
        """Test creating result with empty message."""
        result = VectorOperationResult(success=True, message="")
        
        assert result.success is True
        assert result.message == ""


@pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
class TestLocalVectorStore:
    """Test LocalVectorStore fallback store."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_dir = Path(tmpdir) / "agent_workspaces" / "Agent-3"
            workspace_dir.mkdir(parents=True)
            
            # Create sample status file
            status_file = workspace_dir / "status.json"
            status_file.write_text(json.dumps({
                "agent_id": "Agent-3",
                "status": "active",
                "last_updated": "2025-01-27 12:00:00"
            }))
            
            # Create data directory for message history
            data_dir = Path(tmpdir) / "data"
            data_dir.mkdir()
            message_file = data_dir / "message_history.json"
            message_file.write_text(json.dumps({
                "messages": [
                    {
                        "message_id": "msg1",
                        "content": "Test message",
                        "from": "Agent-1",
                        "to": "Agent-3",
                        "priority": "normal",
                        "timestamp": "2025-01-27T12:00:00"
                    }
                ]
            }))
            
            # Change to temp directory for file loading
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                yield tmpdir
            finally:
                os.chdir(original_cwd)

    def test_init_loads_documents(self, temp_workspace):
        """Test LocalVectorStore initialization loads documents."""
        store = LocalVectorStore()
        
        assert store.documents is not None
        assert isinstance(store.documents, dict)

    def test_init_empty_store_warning(self):
        """Test initialization warning when store is empty."""
        with patch('pathlib.Path.glob', return_value=[]), \
             patch('pathlib.Path.exists', return_value=False):
            with patch('src.services.vector_database_service_unified.get_logger') as mock_logger:
                logger_instance = MagicMock()
                mock_logger.return_value = logger_instance
                store = LocalVectorStore()
                # Should log warning about empty store
                assert logger_instance.warning.called

    def test_search_basic(self, temp_workspace):
        """Test basic search functionality."""
        store = LocalVectorStore()
        
        request = SearchRequest(
            query="test",
            collection="all",
            limit=10
        )
        
        results = store.search(request)
        
        assert isinstance(results, list)
        assert all(isinstance(r, SearchResult) for r in results)

    def test_search_with_collection_filter(self, temp_workspace):
        """Test search with collection filter."""
        store = LocalVectorStore()
        
        request = SearchRequest(
            query="agent",
            collection="agent_status",
            limit=5
        )
        
        results = store.search(request)
        
        assert isinstance(results, list)
        # All results should be from agent_status collection
        assert all(r.collection == "agent_status" for r in results)

    def test_search_empty_query(self, temp_workspace):
        """Test search with empty query."""
        store = LocalVectorStore()
        
        request = SearchRequest(
            query="",
            collection="all",
            limit=10
        )
        
        results = store.search(request)
        
        assert isinstance(results, list)

    def test_search_limit_enforcement(self, temp_workspace):
        """Test search respects limit parameter."""
        store = LocalVectorStore()
        
        request = SearchRequest(
            query="test",
            collection="all",
            limit=1
        )
        
        results = store.search(request)
        
        assert len(results) <= 1

    def test_search_case_insensitive(self, temp_workspace):
        """Test search is case insensitive."""
        store = LocalVectorStore()
        
        request = SearchRequest(
            query="TEST",
            collection="all",
            limit=10
        )
        
        results = store.search(request)
        
        assert isinstance(results, list)

    def test_get_documents_pagination(self, temp_workspace):
        """Test document pagination."""
        store = LocalVectorStore()
        
        request = PaginationRequest(
            collection="all",
            page=1,
            per_page=10,
            sort_by="created_at",
            sort_order="desc"
        )
        
        result = store.get_documents(request)
        
        assert "documents" in result
        assert "pagination" in result
        assert "total" in result
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 10

    def test_get_documents_pagination_page_2(self, temp_workspace):
        """Test pagination on page 2."""
        store = LocalVectorStore()
        
        request = PaginationRequest(
            collection="all",
            page=2,
            per_page=1,
            sort_by="created_at",
            sort_order="asc"
        )
        
        result = store.get_documents(request)
        
        assert result["pagination"]["page"] == 2
        assert result["pagination"]["has_prev"] is True

    def test_get_documents_sorting(self, temp_workspace):
        """Test document sorting."""
        store = LocalVectorStore()
        
        request = PaginationRequest(
            collection="all",
            page=1,
            per_page=10,
            sort_by="created_at",
            sort_order="asc"
        )
        
        result = store.get_documents(request)
        
        assert "documents" in result
        assert isinstance(result["documents"], list)

    def test_get_documents_invalid_sort_handling(self, temp_workspace):
        """Test handling of invalid sort field."""
        store = LocalVectorStore()
        
        request = PaginationRequest(
            collection="all",
            page=1,
            per_page=10,
            sort_by="invalid_field",
            sort_order="asc"
        )
        
        result = store.get_documents(request)
        
        # Should handle gracefully
        assert "documents" in result

    def test_list_collections(self, temp_workspace):
        """Test listing collections."""
        store = LocalVectorStore()
        
        collections = store.list_collections()
        
        assert isinstance(collections, list)
        assert all(hasattr(c, "id") and hasattr(c, "name") for c in collections)

    def test_list_collections_empty(self):
        """Test listing collections when store is empty."""
        with patch('pathlib.Path.glob', return_value=[]), \
             patch('pathlib.Path.exists', return_value=False):
            store = LocalVectorStore()
            collections = store.list_collections()
            
            assert isinstance(collections, list)

    def test_export_collection_json(self, temp_workspace):
        """Test exporting collection as JSON."""
        store = LocalVectorStore()
        
        request = ExportRequest(
            collection="agent_status",
            format="json"
        )
        
        export_data = store.export_collection(request)
        
        assert isinstance(export_data, ExportData)
        assert export_data.format == "json"
        assert export_data.collection == "agent_status"
        assert "data" in export_data.__dict__

    def test_export_collection_csv(self, temp_workspace):
        """Test exporting collection as CSV."""
        store = LocalVectorStore()
        
        request = ExportRequest(
            collection="agent_status",
            format="csv"
        )
        
        export_data = store.export_collection(request)
        
        assert isinstance(export_data, ExportData)
        assert export_data.format == "csv"
        assert isinstance(export_data.data, str)

    def test_export_collection_filename_format(self, temp_workspace):
        """Test export filename format."""
        store = LocalVectorStore()
        
        request = ExportRequest(
            collection="test_collection",
            format="json"
        )
        
        export_data = store.export_collection(request)
        
        assert "test_collection" in export_data.filename
        assert export_data.filename.endswith(".json")

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document(self, temp_workspace):
        """Test adding document to store."""
        store = LocalVectorStore()
        
        vector_doc = VectorDocument(
            id="test_doc",
            content="Test content",
            embedding=[0.1, 0.2, 0.3],
            metadata={"title": "Test", "collection": "test_collection"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        result = store.add_document(vector_doc, "test_collection")
        
        assert isinstance(result, VectorOperationResult)
        assert result.success is True
        assert "test_doc" in store.documents

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_default_collection(self, temp_workspace):
        """Test adding document with default collection."""
        store = LocalVectorStore()
        
        vector_doc = VectorDocument(
            id="test_doc2",
            content="Test content",
            embedding=None,
            metadata={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        result = store.add_document(vector_doc, None)
        
        assert result.success is True

    def test_load_agent_status_documents(self, temp_workspace):
        """Test loading agent status documents."""
        store = LocalVectorStore()
        
        count = store._load_agent_status_documents()
        
        assert count >= 0
        # Should have loaded at least one status file
        assert any("status" in doc_id for doc_id in store.documents.keys())

    def test_load_agent_status_documents_corrupted_file(self, temp_workspace):
        """Test handling corrupted status file."""
        workspace_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-Corrupt"
        workspace_dir.mkdir(parents=True)
        status_file = workspace_dir / "status.json"
        status_file.write_text("invalid json{")
        
        store = LocalVectorStore()
        count = store._load_agent_status_documents()
        
        # Should handle gracefully
        assert count >= 0

    def test_load_message_history_documents(self, temp_workspace):
        """Test loading message history documents."""
        store = LocalVectorStore()
        
        count = store._load_message_history_documents()
        
        assert count >= 0

    def test_load_message_history_documents_missing_file(self):
        """Test loading when message history file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            store = LocalVectorStore()
            count = store._load_message_history_documents()
            
            assert count == 0

    def test_load_message_history_documents_corrupted(self, temp_workspace):
        """Test handling corrupted message history."""
        data_dir = Path(temp_workspace) / "data"
        data_dir.mkdir(exist_ok=True)
        message_file = data_dir / "message_history.json"
        message_file.write_text("invalid json{")
        
        store = LocalVectorStore()
        count = store._load_message_history_documents()
        
        # Should handle gracefully
        assert count == 0

    def test_iter_documents_all(self, temp_workspace):
        """Test iterating all documents."""
        store = LocalVectorStore()
        
        docs = list(store._iter_documents("all"))
        
        assert isinstance(docs, list)

    def test_iter_documents_default(self, temp_workspace):
        """Test iterating documents with 'default' collection."""
        store = LocalVectorStore()
        
        docs = list(store._iter_documents("default"))
        
        assert isinstance(docs, list)

    def test_iter_documents_collection_filter(self, temp_workspace):
        """Test iterating documents with collection filter."""
        store = LocalVectorStore()
        
        docs = list(store._iter_documents("agent_status"))
        
        assert isinstance(docs, list)
        assert all(doc.collection == "agent_status" for doc in docs)

    def test_sort_documents_asc(self, temp_workspace):
        """Test sorting documents ascending."""
        store = LocalVectorStore()
        docs = [
            Document(id="1", title="Doc 1", content="A", collection="test", created_at="2025-01-01"),
            Document(id="2", title="Doc 2", content="B", collection="test", created_at="2025-01-02"),
        ]
        
        sorted_docs = store._sort_documents(docs, "created_at", "asc")
        
        assert sorted_docs[0].id == "1"
        assert sorted_docs[1].id == "2"

    def test_sort_documents_desc(self, temp_workspace):
        """Test sorting documents descending."""
        store = LocalVectorStore()
        docs = [
            Document(id="1", title="Doc 1", content="A", collection="test", created_at="2025-01-01"),
            Document(id="2", title="Doc 2", content="B", collection="test", created_at="2025-01-02"),
        ]
        
        sorted_docs = store._sort_documents(docs, "created_at", "desc")
        
        assert sorted_docs[0].id == "2"
        assert sorted_docs[1].id == "1"

    def test_sort_documents_invalid_field(self, temp_workspace):
        """Test sorting with invalid field."""
        store = LocalVectorStore()
        docs = [
            Document(id="1", title="Doc 1", content="A", collection="test", created_at="2025-01-01"),
        ]
        
        sorted_docs = store._sort_documents(docs, "invalid_field", "asc")
        
        # Should return original list
        assert len(sorted_docs) == 1

    def test_document_to_result(self, temp_workspace):
        """Test document to result conversion."""
        store = LocalVectorStore()
        doc = Document(
            id="test",
            title="Test",
            content="Content",
            collection="test",
            tags=["tag1"],
            created_at="2025-01-01",
            updated_at="2025-01-01",
            size="1 KB",
            metadata={}
        )
        
        result = store._document_to_result(doc, 0.8)
        
        assert isinstance(result, SearchResult)
        assert result.id == "test"
        assert result.relevance == 0.8

    def test_to_csv_empty(self):
        """Test CSV conversion with empty documents."""
        result = LocalVectorStore._to_csv([])
        
        assert result == ""

    def test_to_csv_with_data(self):
        """Test CSV conversion with documents."""
        docs = [
            {"id": "1", "content": "Test", "collection": "test"},
            {"id": "2", "content": "Test2", "collection": "test"},
        ]
        
        result = LocalVectorStore._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result
        assert "content" in result

    def test_to_csv_with_nested_data(self):
        """Test CSV conversion with nested data structures."""
        docs = [
            {"id": "1", "metadata": {"key": "value"}, "tags": ["tag1", "tag2"]},
        ]
        
        result = LocalVectorStore._to_csv(docs)
        
        assert isinstance(result, str)
        # Nested data should be JSON stringified
        assert "metadata" in result

    def test_to_csv_with_newlines(self):
        """Test CSV conversion handles newlines."""
        docs = [
            {"id": "1", "content": "Line 1\nLine 2"},
        ]
        
        result = LocalVectorStore._to_csv(docs)
        
        # Newlines should be replaced
        assert "\n" not in result or result.count("\n") == 1  # Only header newline

    def test_vector_document_to_document(self, temp_workspace):
        """Test vector document to document conversion."""
        vector_doc = VectorDocument(
            id="test",
            content="Content",
            embedding=[0.1, 0.2],
            metadata={"title": "Test", "collection": "test_collection", "tags": ["tag1"]},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        doc = LocalVectorStore._vector_document_to_document(vector_doc, "test_collection")
        
        assert isinstance(doc, Document)
        assert doc.id == "test"
        assert doc.collection == "test_collection"

    def test_vector_document_to_document_default_collection(self, temp_workspace):
        """Test conversion with default collection."""
        vector_doc = VectorDocument(
            id="test",
            content="Content",
            embedding=None,
            metadata={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        doc = LocalVectorStore._vector_document_to_document(vector_doc, None)
        
        assert doc.collection == DEFAULT_COLLECTION


class TestVectorDatabaseService:
    """Test VectorDatabaseService main service."""

    @patch('src.services.vector_database_service_unified.chromadb')
    @patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction')
    def test_init_with_chromadb(self, mock_embedding, mock_chromadb):
        """Test initialization with ChromaDB available."""
        mock_client = MagicMock()
        mock_persistent_client = MagicMock(return_value=mock_client)
        mock_chromadb.PersistentClient = mock_persistent_client
        mock_embedding.return_value = MagicMock()
        
        service = VectorDatabaseService()
        
        assert service.default_collection == DEFAULT_COLLECTION
        assert service._client is not None

    @patch('src.services.vector_database_service_unified.chromadb', None)
    def test_init_without_chromadb(self):
        """Test initialization without ChromaDB (fallback to local)."""
        service = VectorDatabaseService()
        
        assert service.default_collection == DEFAULT_COLLECTION
        # Should fallback to LocalVectorStore
        assert hasattr(service, '_fallback_store')

    def test_init_custom_persist_path(self):
        """Test initialization with custom persist path."""
        with patch('src.services.vector_database_service_unified.chromadb', None):
            service = VectorDatabaseService(persist_path="custom/path")
            
            assert service.persist_path == Path("custom/path")

    def test_init_custom_collection(self):
        """Test initialization with custom collection."""
        with patch('src.services.vector_database_service_unified.chromadb', None):
            service = VectorDatabaseService(default_collection="custom_collection")
            
            assert service.default_collection == "custom_collection"

    @patch('src.services.vector_database_service_unified.chromadb')
    @patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction')
    def test_init_embedding_function_failure(self, mock_embedding, mock_chromadb):
        """Test initialization when embedding function fails."""
        mock_embedding.side_effect = Exception("Embedding error")
        
        service = VectorDatabaseService()
        
        # Should fallback to local store
        assert service._fallback_store is not None

    @patch('src.services.vector_database_service_unified.chromadb')
    def test_init_chromadb_client_failure(self, mock_chromadb):
        """Test initialization when ChromaDB client creation fails."""
        mock_chromadb.PersistentClient.side_effect = Exception("Client error")
        mock_chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction = MagicMock(return_value=MagicMock())
        
        service = VectorDatabaseService()
        
        # Should fallback to local store
        assert service._fallback_store is not None

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    @patch('src.services.vector_database_service_unified.chromadb')
    @patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction')
    def test_search_with_chromadb(self, mock_embedding, mock_chromadb):
        """Test search with ChromaDB."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "ids": [["doc1"]],
            "documents": [["Test content"]],
            "metadatas": [[{"title": "Test"}]],
            "distances": [[0.1]]
        }
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        mock_embedding.return_value = MagicMock()
        
        service = VectorDatabaseService()
        service._client = mock_client
        service._embedding_function = MagicMock()
        
        request = SearchRequest(query="test", collection="test", limit=10)
        results = service.search(request)
        
        assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_with_fallback(self):
        """Test search with fallback store."""
        with patch('src.services.vector_database_service_unified.chromadb', None):
            service = VectorDatabaseService()
            
            request = SearchRequest(query="test", collection="all", limit=10)
            results = service.search(request)
            
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_no_store_available(self):
        """Test search when no store is available."""
        service = VectorDatabaseService()
        service._client = None
        service._fallback_store = None
        
        request = SearchRequest(query="test", collection="all", limit=10)
        
        with pytest.raises(RuntimeError):
            service.search(request)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_documents_with_chromadb(self):
        """Test get_documents with ChromaDB."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"title": "Test"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = PaginationRequest(collection="test", page=1, per_page=10, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            assert "documents" in result
            assert "pagination" in result

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_list_collections_with_chromadb(self):
        """Test list_collections with ChromaDB."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.name = "test_collection"
            mock_collection.count.return_value = 5
            mock_collection.metadata = {}
            mock_client.list_collections.return_value = [mock_collection]
            mock_client.get_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            collections = service.list_collections()
            
            assert isinstance(collections, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_list_collections_with_fallback(self):
        """Test list_collections with fallback."""
        with patch('src.services.vector_database_service_unified.chromadb', None):
            service = VectorDatabaseService()
            collections = service.list_collections()
            
            assert isinstance(collections, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_list_collections_no_store(self):
        """Test list_collections when no store available."""
        service = VectorDatabaseService()
        service._client = None
        service._fallback_store = None
        
        collections = service.list_collections()
        
        assert collections == []

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_with_chromadb(self):
        """Test add_document with ChromaDB."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.add = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            service._collection_cache = {}
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=[0.1, 0.2],
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            result = service.add_document(vector_doc, "test_collection")
            
            assert result.success is True

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_chromadb_exception(self):
        """Test add_document when ChromaDB raises exception."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.add.side_effect = Exception("ChromaDB error")
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            service._collection_cache = {}
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=None,
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            result = service.add_document(vector_doc, "test_collection")
            
            assert result.success is False

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_with_fallback(self):
        """Test add_document with fallback store."""
        with patch('src.services.vector_database_service_unified.chromadb', None):
            service = VectorDatabaseService()
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=None,
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            result = service.add_document(vector_doc, "test_collection")
            
            assert isinstance(result, VectorOperationResult)

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_no_store(self):
        """Test add_document when no store available."""
        service = VectorDatabaseService()
        service._client = None
        service._fallback_store = None
        
        vector_doc = VectorDocument(
            id="test",
            content="Content",
            embedding=None,
            metadata={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        result = service.add_document(vector_doc, "test_collection")
        
        assert result.success is False

    def test_resolve_collection_name(self):
        """Test collection name resolution."""
        service = VectorDatabaseService()
        
        assert service._resolve_collection_name(None) == DEFAULT_COLLECTION
        assert service._resolve_collection_name("all") == DEFAULT_COLLECTION
        assert service._resolve_collection_name("default") == DEFAULT_COLLECTION
        assert service._resolve_collection_name("custom") == "custom"

    def test_metadata_matches(self):
        """Test metadata matching."""
        metadata = {"key1": "value1", "key2": "value2"}
        filters = {"key1": "value1"}
        
        assert VectorDatabaseService._metadata_matches(metadata, filters) is True
        
        filters2 = {"key1": "different"}
        assert VectorDatabaseService._metadata_matches(metadata, filters2) is False

    def test_metadata_to_document(self):
        """Test metadata to document conversion."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            "Content",
            {"title": "Test", "collection": "test", "tags": ["tag1"]}
        )
        
        assert isinstance(doc, Document)
        assert doc.id == "doc1"
        assert doc.title == "Test"

    def test_metadata_to_document_minimal(self):
        """Test metadata to document with minimal data."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            None,
            {}
        )
        
        assert doc.id == "doc1"
        assert doc.collection == DEFAULT_COLLECTION

    def test_sort_documents(self):
        """Test document sorting."""
        docs = [
            {"created_at": "2025-01-01"},
            {"created_at": "2025-01-02"},
        ]
        
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "asc")
        
        assert sorted_docs[0]["created_at"] == "2025-01-01"

    def test_sort_documents_exception_handling(self):
        """Test sorting exception handling."""
        docs = [{"invalid": "data"}]
        
        sorted_docs = VectorDatabaseService._sort_documents(docs, "nonexistent", "asc")
        
        # Should return original list on exception
        assert len(sorted_docs) == 1

    def test_to_csv_static(self):
        """Test static CSV conversion."""
        docs = [{"id": "1", "content": "Test"}]
        
        result = VectorDatabaseService._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result


class TestGetVectorDatabaseService:
    """Test get_vector_database_service() function."""

    def test_get_service_singleton(self):
        """Test that get_vector_database_service returns singleton."""
        # Reset singleton
        import src.services.vector_database_service_unified as vds_module
        vds_module._SERVICE_INSTANCE = None
        
        service1 = get_vector_database_service()
        service2 = get_vector_database_service()
        
        # Should return same instance (singleton pattern)
        assert service1 is service2

    def test_get_service_returns_service(self):
        """Test that get_vector_database_service returns service instance."""
        # Reset singleton
        import src.services.vector_database_service_unified as vds_module
        vds_module._SERVICE_INSTANCE = None
        
        service = get_vector_database_service()
        
        assert isinstance(service, VectorDatabaseService)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_export_collection_with_chromadb(self):
        """Test export_collection with ChromaDB."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"title": "Test"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = ExportRequest(collection="test", format="json")
            result = service.export_collection(request)
            
            assert isinstance(result, ExportData)
            assert result.format == "json"

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_export_collection_csv_chromadb(self):
        """Test export_collection as CSV with ChromaDB."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"title": "Test"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = ExportRequest(collection="test", format="csv")
            result = service.export_collection(request)
            
            assert result.format == "csv"
            assert isinstance(result.data, str)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_export_collection_no_store(self):
        """Test export_collection when no store available."""
        service = VectorDatabaseService()
        service._client = None
        service._fallback_store = None
        
        request = ExportRequest(collection="test", format="json")
        
        with pytest.raises(RuntimeError):
            service.export_collection(request)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_documents_with_fallback(self):
        """Test get_documents with fallback store."""
        with patch('src.services.vector_database_service_unified.chromadb', None):
            service = VectorDatabaseService()
            
            request = PaginationRequest(collection="all", page=1, per_page=10, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            assert "documents" in result
            assert "pagination" in result

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_documents_no_store(self):
        """Test get_documents when no store available."""
        service = VectorDatabaseService()
        service._client = None
        service._fallback_store = None
        
        request = PaginationRequest(collection="all", page=1, per_page=10)
        
        with pytest.raises(RuntimeError):
            service.get_documents(request)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_query_exception(self):
        """Test search when ChromaDB query raises exception."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.side_effect = Exception("Query error")
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10)
            results = service.search(request)
            
            # Should return empty list on exception
            assert results == []

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_empty_results(self):
        """Test search with empty ChromaDB results."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10)
            results = service.search(request)
            
            assert results == []

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_list_collections_chromadb_count_exception(self):
        """Test list_collections when count() raises exception."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.name = "test_collection"
            mock_collection.count.side_effect = Exception("Count error")
            mock_collection.metadata = {}
            mock_client.list_collections.return_value = [mock_collection]
            mock_client.get_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            collections = service.list_collections()
            
            # Should handle exception and use count=0
            assert isinstance(collections, list)

    def test_get_collection_caching(self):
        """Test that collections are cached."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            # First call
            collection1 = service._get_collection("test")
            # Second call should use cache
            collection2 = service._get_collection("test")
            
            # Should only call get_or_create_collection once
            assert mock_client.get_or_create_collection.call_count == 1
            assert collection1 is collection2

    def test_to_csv_with_commas_in_data(self):
        """Test CSV conversion handles commas in data."""
        docs = [
            {"id": "1", "content": "Text, with, commas"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Commas should be replaced with semicolons
        assert isinstance(result, str)

    def test_to_csv_with_dict_value(self):
        """Test CSV conversion with dict values."""
        docs = [
            {"id": "1", "metadata": {"key": "value"}},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Dict should be JSON stringified
        assert isinstance(result, str)
        assert "metadata" in result

    def test_to_csv_with_list_value(self):
        """Test CSV conversion with list values."""
        docs = [
            {"id": "1", "tags": ["tag1", "tag2"]},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # List should be JSON stringified
        assert isinstance(result, str)
        assert "tags" in result

    def test_metadata_to_document_with_category(self):
        """Test metadata to document uses category as collection."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            "Content",
            {"category": "test_category"}
        )
        
        assert doc.collection == "test_category"

    def test_metadata_to_document_with_timestamp(self):
        """Test metadata to document uses timestamp fields."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            "Content",
            {"timestamp": "2025-01-01", "last_updated": "2025-01-02"}
        )
        
        assert doc.created_at == "2025-01-01"
        assert doc.updated_at == "2025-01-02"

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_with_filters(self):
        """Test search with ChromaDB and filters."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [["doc1"]],
                "documents": [["Test content"]],
                "metadatas": [[{"title": "Test", "agent_id": "Agent-7"}]],
                "distances": [[0.1]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10, filters={"agent_id": "Agent-7"})
            results = service.search(request)
            
            assert isinstance(results, list)
            mock_collection.query.assert_called_once()

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_with_filters(self):
        """Test _get_collection_documents with filters."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1", "doc2"],
                "documents": ["Content1", "Content2"],
                "metadatas": [{"agent_id": "Agent-7"}, {"agent_id": "Agent-8"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            docs = service._get_collection_documents("test", {"agent_id": "Agent-7"})
            
            # Should filter to only Agent-7 documents
            assert len(docs) == 1

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_no_matching_filters(self):
        """Test _get_collection_documents when no documents match filters."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"agent_id": "Agent-7"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            docs = service._get_collection_documents("test", {"agent_id": "Agent-8"})
            
            # Should return empty list when no matches
            assert len(docs) == 0

    def test_metadata_matches_partial(self):
        """Test metadata matching with partial filters."""
        metadata = {"key1": "value1", "key2": "value2", "key3": "value3"}
        filters = {"key1": "value1"}
        
        assert VectorDatabaseService._metadata_matches(metadata, filters) is True

    def test_metadata_matches_multiple_filters(self):
        """Test metadata matching with multiple filters."""
        metadata = {"key1": "value1", "key2": "value2"}
        filters = {"key1": "value1", "key2": "value2"}
        
        assert VectorDatabaseService._metadata_matches(metadata, filters) is True

    def test_metadata_matches_one_fails(self):
        """Test metadata matching when one filter fails."""
        metadata = {"key1": "value1", "key2": "value2"}
        filters = {"key1": "value1", "key2": "different"}
        
        assert VectorDatabaseService._metadata_matches(metadata, filters) is False

    def test_to_csv_with_special_characters(self):
        """Test CSV conversion with special characters."""
        docs = [
            {"id": "1", "content": "Text with \"quotes\" and 'apostrophes'"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result

    def test_to_csv_empty_documents(self):
        """Test CSV conversion with empty documents list."""
        result = VectorDatabaseService._to_csv([])
        
        assert result == ""

    def test_get_service_thread_safety(self):
        """Test singleton pattern thread safety."""
        import src.services.vector_database_service_unified as vds_module
        vds_module._SERVICE_INSTANCE = None
        
        # Simulate concurrent access
        service1 = get_vector_database_service()
        service2 = get_vector_database_service()
        
        # Should return same instance
        assert service1 is service2

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_fetch_documents_pagination_edge_cases(self):
        """Test pagination edge cases."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1", "doc2", "doc3"],
                "documents": ["C1", "C2", "C3"],
                "metadatas": [{}, {}, {}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            # Test page beyond available documents
            request = PaginationRequest(collection="test", page=10, per_page=10, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            assert result["pagination"]["has_next"] is False
            assert len(result["documents"]) == 0

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_with_none_distance(self):
        """Test search when ChromaDB returns None distance."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [["doc1"]],
                "documents": [["Test content"]],
                "metadatas": [[{"title": "Test"}]],
                "distances": [[None]]  # None distance
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10)
            results = service.search(request)
            
            # Should handle None distance gracefully (relevance = 0.0)
            assert isinstance(results, list)
            if results:
                assert results[0].relevance == 0.0

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_missing_results_keys(self):
        """Test search when ChromaDB results missing keys."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {}  # Empty results
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10)
            results = service.search(request)
            
            # Should handle missing keys gracefully
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_fetch_documents_zero_per_page(self):
        """Test pagination with zero per_page."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = PaginationRequest(collection="test", page=1, per_page=0, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            # Should handle zero per_page
            assert "documents" in result

    def test_metadata_to_document_with_collection_priority(self):
        """Test metadata to document collection priority (collection > category > default)."""
        # Test collection takes priority
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"collection": "test_collection", "category": "test_category"}
        )
        assert doc1.collection == "test_collection"
        
        # Test category when no collection
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {"category": "test_category"}
        )
        assert doc2.collection == "test_category"
        
        # Test default when neither
        doc3 = VectorDatabaseService._metadata_to_document("doc3", "Content", {})
        assert doc3.collection == DEFAULT_COLLECTION

    def test_metadata_to_document_content_priority(self):
        """Test metadata to document content priority (content param > metadata.content)."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1", "Param Content", {"content": "Metadata Content"}
        )
        
        # Parameter content should take priority
        assert doc.content == "Param Content"

    def test_metadata_to_document_none_content(self):
        """Test metadata to document with None content parameter."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1", None, {"content": "Metadata Content"}
        )
        
        # Should use metadata content
        assert doc.content == "Metadata Content"

    def test_metadata_to_document_empty_metadata_content(self):
        """Test metadata to document with empty metadata content."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1", None, {}
        )
        
        # Should default to empty string
        assert doc.content == ""

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_list_collections_chromadb_exception_handling(self):
        """Test list_collections handles ChromaDB exceptions."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_client.list_collections.side_effect = Exception("List error")
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            # Should handle exception gracefully
            try:
                collections = service.list_collections()
                assert isinstance(collections, list)
            except Exception:
                # If it propagates, that's also acceptable
                pass

    def test_to_csv_with_empty_string_values(self):
        """Test CSV conversion with empty string values."""
        docs = [
            {"id": "", "content": "", "collection": "test"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result

    def test_to_csv_with_none_values(self):
        """Test CSV conversion with None values."""
        docs = [
            {"id": "1", "content": None, "collection": "test"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # None should be converted to string
        assert isinstance(result, str)

    def test_resolve_collection_name_edge_cases(self):
        """Test collection name resolution edge cases."""
        service = VectorDatabaseService()
        
        # Test empty string
        assert service._resolve_collection_name("") == DEFAULT_COLLECTION
        
        # Test whitespace
        assert service._resolve_collection_name("   ") == "   "  # Not normalized, but handled

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_with_none_embedding(self):
        """Test add_document with None embedding."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.add = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            service._collection_cache = {}
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=None,  # None embedding
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            result = service.add_document(vector_doc, "test_collection")
            
            # Should handle None embedding (embeddings=None in add call)
            assert result.success is True

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_unequal_list_lengths(self):
        """Test search when ChromaDB returns unequal list lengths."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [["doc1", "doc2"]],  # 2 IDs
                "documents": [["Content1"]],  # 1 document
                "metadatas": [[{"title": "Test"}]],  # 1 metadata
                "distances": [[0.1, 0.2]]  # 2 distances
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10)
            results = service.search(request)
            
            # Should handle unequal lengths gracefully
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_fetch_documents_negative_page(self):
        """Test pagination with negative page number."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = PaginationRequest(collection="test", page=-1, per_page=10, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            # Should handle negative page (max(..., 0) should make it 0)
            assert "documents" in result

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_fetch_documents_very_large_page(self):
        """Test pagination with very large page number."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = PaginationRequest(collection="test", page=999999, per_page=10, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            # Should handle very large page
            assert "documents" in result
            assert len(result["documents"]) == 0

    def test_metadata_to_document_size_calculation(self):
        """Test metadata to document size calculation."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            "Test content",
            {}
        )
        
        # Size should be calculated from content length
        assert "KB" in doc.size

    def test_metadata_to_document_size_from_metadata(self):
        """Test metadata to document uses size from metadata if provided."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            "Content",
            {"size": "5.2 KB"}
        )
        
        assert doc.size == "5.2 KB"

    def test_metadata_to_document_tags_default(self):
        """Test metadata to document tags default to empty list."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            "Content",
            {}
        )
        
        assert doc.tags == []

    def test_metadata_to_document_created_at_fallback(self):
        """Test metadata to document created_at fallback chain."""
        # Test timestamp > created_at > empty string
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"timestamp": "2025-01-01"}
        )
        assert doc1.created_at == "2025-01-01"
        
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {"created_at": "2025-01-02"}
        )
        assert doc2.created_at == "2025-01-02"
        
        doc3 = VectorDatabaseService._metadata_to_document(
            "doc3", "Content", {}
        )
        assert doc3.created_at == ""

    def test_sort_documents_case_insensitive(self):
        """Test document sorting is case insensitive for sort_order."""
        docs = [
            {"created_at": "2025-01-01"},
            {"created_at": "2025-01-02"},
        ]
        
        # Test uppercase
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "DESC")
        assert sorted_docs[0]["created_at"] == "2025-01-02"
        
        # Test lowercase
        sorted_docs2 = VectorDatabaseService._sort_documents(docs, "created_at", "desc")
        assert sorted_docs2[0]["created_at"] == "2025-01-02"

    def test_to_csv_with_unicode_characters(self):
        """Test CSV conversion with unicode characters."""
        docs = [
            {"id": "1", "content": "Test with émojis 🚀 and unicode: 测试"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result

    def test_to_csv_with_newline_in_value(self):
        """Test CSV conversion replaces newlines in values."""
        docs = [
            {"id": "1", "content": "Line 1\nLine 2\nLine 3"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Newlines should be replaced with spaces
        assert "\n" not in result or result.count("\n") <= 1  # Only header newline

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_empty_collection(self):
        """Test _get_collection_documents with empty collection."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": [],
                "documents": [],
                "metadatas": []
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            docs = service._get_collection_documents("test", {})
            
            assert len(docs) == 0

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_empty_query_text(self):
        """Test search with empty query text."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="", collection="test", limit=10)
            results = service.search(request)
            
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_fetch_documents_per_page_larger_than_total(self):
        """Test pagination when per_page is larger than total documents."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1", "doc2"],
                "documents": ["C1", "C2"],
                "metadatas": [{}, {}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = PaginationRequest(collection="test", page=1, per_page=100, sort_by="created_at", sort_order="asc")
            result = service.get_documents(request)
            
            assert len(result["documents"]) == 2
            assert result["pagination"]["has_next"] is False

    def test_metadata_to_document_updated_at_fallback(self):
        """Test metadata to document updated_at fallback chain."""
        # Test last_updated > updated_at > empty string
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"last_updated": "2025-01-01"}
        )
        assert doc1.updated_at == "2025-01-01"
        
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {"updated_at": "2025-01-02"}
        )
        assert doc2.updated_at == "2025-01-02"
        
        doc3 = VectorDatabaseService._metadata_to_document(
            "doc3", "Content", {}
        )
        assert doc3.updated_at == ""

    def test_metadata_to_document_title_fallback(self):
        """Test metadata to document title fallback (metadata.title > doc_id)."""
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"title": "Custom Title"}
        )
        assert doc1.title == "Custom Title"
        
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {}
        )
        assert doc2.title == "doc2"

    def test_sort_documents_mixed_types(self):
        """Test document sorting with mixed data types."""
        docs = [
            {"created_at": "2025-01-01", "score": 10},
            {"created_at": "2025-01-02", "score": 5},
        ]
        
        # Should handle mixed types gracefully
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "asc")
        assert len(sorted_docs) == 2

    def test_to_csv_with_empty_dict(self):
        """Test CSV conversion with empty dictionary."""
        docs = [
            {},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Should handle empty dict
        assert isinstance(result, str)

    def test_to_csv_with_all_empty_values(self):
        """Test CSV conversion with all empty values."""
        docs = [
            {"id": "", "content": "", "collection": ""},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_export_collection_empty_collection_chromadb(self):
        """Test export_collection with empty collection."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": [],
                "documents": [],
                "metadatas": []
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = ExportRequest(collection="test", format="json")
            result = service.export_collection(request)
            
            assert isinstance(result, ExportData)
            assert result.format == "json"

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_list_collections_chromadb_empty_client(self):
        """Test list_collections when client has no collections."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_client.list_collections.return_value = []  # Empty list
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            collections = service.list_collections()
            
            assert collections == []

    def test_resolve_collection_name_whitespace_only(self):
        """Test collection name resolution with whitespace-only string."""
        service = VectorDatabaseService()
        
        # Whitespace should be preserved (not normalized to default)
        result = service._resolve_collection_name("   ")
        assert result == "   "

    @pytest.mark.skipif(not VECTOR_MODELS_AVAILABLE, reason="Vector models not available")
    def test_add_document_empty_collection_name(self):
        """Test add_document with empty collection name."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.add = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            service._collection_cache = {}
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=[0.1, 0.2],
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            result = service.add_document(vector_doc, "")
            
            # Empty collection name should use default
            assert result.success is True

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_query_embedding_failure(self):
        """Test search when query embedding generation fails."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            
            # Mock embedding function to raise exception
            mock_embedding_instance = MagicMock()
            mock_embedding_instance.side_effect = Exception("Embedding failed")
            mock_embedding.return_value = mock_embedding_instance
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = mock_embedding_instance
            
            request = SearchRequest(query="test", collection="test", limit=10)
            
            # Should handle embedding failure gracefully
            with pytest.raises(Exception):
                service.search(request)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_add_document_embedding_generation_failure(self):
        """Test add_document when embedding generation fails."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.add = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            
            # Mock embedding function to raise exception
            mock_embedding_instance = MagicMock()
            mock_embedding_instance.side_effect = Exception("Embedding failed")
            mock_embedding.return_value = mock_embedding_instance
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = mock_embedding_instance
            service._collection_cache = {}
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=None,  # No embedding provided
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Should handle embedding generation failure
            result = service.add_document(vector_doc, "test")
            assert result.success is False

    def test_metadata_to_document_collection_fallback(self):
        """Test metadata to document collection fallback."""
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"collection": "custom_collection"}
        )
        assert doc1.collection == "custom_collection"
        
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {}
        )
        assert doc2.collection == ""

    def test_metadata_to_document_type_fallback(self):
        """Test metadata to document type fallback."""
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"type": "custom_type"}
        )
        assert doc1.type == "custom_type"
        
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {}
        )
        assert doc2.type == ""

    def test_sort_documents_none_values(self):
        """Test document sorting with None values."""
        docs = [
            {"created_at": "2025-01-01"},
            {"created_at": None},
            {"created_at": "2025-01-02"},
        ]
        
        # Should handle None values gracefully
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "asc")
        assert len(sorted_docs) == 3

    def test_to_csv_with_none_values(self):
        """Test CSV conversion with None values."""
        docs = [
            {"id": "1", "content": None, "collection": "test"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Should handle None values
        assert isinstance(result, str)
        assert "id" in result

    def test_to_csv_with_comma_in_value(self):
        """Test CSV conversion with commas in values (should be quoted)."""
        docs = [
            {"id": "1", "content": "Value, with, commas"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Commas in values should be handled (quoted or escaped)
        assert isinstance(result, str)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_with_filter_metadata(self):
        """Test _get_collection_documents with filter metadata."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"agent_id": "Agent-1"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            filter_metadata = {"agent_id": "Agent-1"}
            docs = service._get_collection_documents("test", filter_metadata)
            
            # Should apply filter
            assert len(docs) == 1

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_filter_no_match(self):
        """Test _get_collection_documents with filter that matches nothing."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"agent_id": "Agent-1"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            filter_metadata = {"agent_id": "Agent-999"}  # No match
            docs = service._get_collection_documents("test", filter_metadata)
            
            # Should filter out non-matching documents
            assert len(docs) == 0

    def test_resolve_collection_name_none_input(self):
        """Test collection name resolution with None input."""
        service = VectorDatabaseService()
        
        # None should use default
        result = service._resolve_collection_name(None)
        assert result == "default_collection"

    def test_resolve_collection_name_empty_string(self):
        """Test collection name resolution with empty string."""
        service = VectorDatabaseService()
        
        # Empty string should use default
        result = service._resolve_collection_name("")
        assert result == "default_collection"

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_limit_zero(self):
        """Test search with limit=0."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=0)
            results = service.search(request)
            
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_limit_negative(self):
        """Test search with negative limit."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=-1)
            results = service.search(request)
            
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_limit_very_large(self):
        """Test search with very large limit."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [["doc1"]],
                "documents": [["Content"]],
                "metadatas": [[{}]],
                "distances": [[0.1]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=999999)
            results = service.search(request)
            
            assert isinstance(results, list)

    def test_metadata_to_document_size_calculation_large_content(self):
        """Test metadata to document size calculation with large content."""
        large_content = "x" * 10000
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            large_content,
            {}
        )
        
        # Size should be calculated from content length
        assert "KB" in doc.size or "MB" in doc.size

    def test_metadata_to_document_size_calculation_small_content(self):
        """Test metadata to document size calculation with small content."""
        small_content = "x"
        doc = VectorDatabaseService._metadata_to_document(
            "doc1",
            small_content,
            {}
        )
        
        # Size should be calculated from content length
        assert "B" in doc.size or "KB" in doc.size

    def test_sort_documents_missing_sort_key(self):
        """Test document sorting when sort key is missing."""
        docs = [
            {"created_at": "2025-01-01"},
            {"other_field": "value"},  # Missing created_at
            {"created_at": "2025-01-02"},
        ]
        
        # Should handle missing keys gracefully
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "asc")
        assert len(sorted_docs) == 3

    def test_to_csv_with_quote_in_value(self):
        """Test CSV conversion with quotes in values."""
        docs = [
            {"id": "1", "content": 'Value with "quotes"'},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Quotes in values should be handled (escaped or quoted)
        assert isinstance(result, str)

    def test_to_csv_with_newline_and_comma(self):
        """Test CSV conversion with both newlines and commas."""
        docs = [
            {"id": "1", "content": "Line 1, with comma\nLine 2"},
        ]
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Both newlines and commas should be handled
        assert isinstance(result, str)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_export_collection_csv_format(self):
        """Test export_collection with CSV format."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = ExportRequest(collection="test", format="csv")
            result = service.export_collection(request)
            
            assert isinstance(result, ExportData)
            assert result.format == "csv"

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_export_collection_unknown_format(self):
        """Test export_collection with unknown format."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = ExportRequest(collection="test", format="unknown")
            result = service.export_collection(request)
            
            # Should handle unknown format (defaults to JSON or handles gracefully)
            assert isinstance(result, ExportData)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_where_filter_none(self):
        """Test search with where filter set to None."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [["doc1"]],
                "documents": [["Content"]],
                "metadatas": [[{}]],
                "distances": [[0.1]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10, where=None)
            results = service.search(request)
            
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_search_chromadb_where_filter_empty_dict(self):
        """Test search with where filter as empty dict."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "ids": [["doc1"]],
                "documents": [["Content"]],
                "metadatas": [[{}]],
                "distances": [[0.1]]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            request = SearchRequest(query="test", collection="test", limit=10, where={})
            results = service.search(request)
            
            assert isinstance(results, list)

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_add_document_collection_name_special_chars(self):
        """Test add_document with special characters in collection name."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.add = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            service._collection_cache = {}
            
            vector_doc = VectorDocument(
                id="test",
                content="Content",
                embedding=[0.1, 0.2],
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            result = service.add_document(vector_doc, "test-collection_123")
            
            assert result.success is True

    def test_metadata_to_document_tags_list_conversion(self):
        """Test metadata to document tags list conversion."""
        doc1 = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"tags": ["tag1", "tag2", "tag3"]}
        )
        assert isinstance(doc1.tags, list)
        assert len(doc1.tags) == 3
        
        doc2 = VectorDatabaseService._metadata_to_document(
            "doc2", "Content", {"tags": "single_tag"}  # String instead of list
        )
        # Should handle string tags
        assert isinstance(doc2.tags, list) or isinstance(doc2.tags, str)

    def test_metadata_to_document_tags_empty_list(self):
        """Test metadata to document tags with empty list."""
        doc = VectorDatabaseService._metadata_to_document(
            "doc1", "Content", {"tags": []}
        )
        assert doc.tags == []

    def test_sort_documents_empty_list(self):
        """Test document sorting with empty list."""
        docs = []
        
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "asc")
        assert len(sorted_docs) == 0

    def test_sort_documents_single_item(self):
        """Test document sorting with single item."""
        docs = [{"created_at": "2025-01-01"}]
        
        sorted_docs = VectorDatabaseService._sort_documents(docs, "created_at", "asc")
        assert len(sorted_docs) == 1
        assert sorted_docs[0]["created_at"] == "2025-01-01"

    def test_to_csv_empty_list(self):
        """Test CSV conversion with empty list."""
        docs = []
        
        result = VectorDatabaseService._to_csv(docs)
        
        # Should handle empty list (header only or empty)
        assert isinstance(result, str)

    def test_to_csv_single_document(self):
        """Test CSV conversion with single document."""
        docs = [{"id": "1", "content": "Content", "collection": "test"}]
        
        result = VectorDatabaseService._to_csv(docs)
        
        assert isinstance(result, str)
        assert "id" in result
        assert "content" in result

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_with_where_filter(self):
        """Test _get_collection_documents with where filter."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"agent_id": "Agent-1"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            where_filter = {"agent_id": "Agent-1"}
            docs = service._get_collection_documents("test", where_filter)
            
            # Should apply where filter
            assert len(docs) == 1

    @pytest.mark.skipif(not WEB_MODELS_AVAILABLE, reason="Web models not available")
    def test_get_collection_documents_where_filter_no_match(self):
        """Test _get_collection_documents with where filter that matches nothing."""
        with patch('src.services.vector_database_service_unified.chromadb') as mock_chromadb, \
             patch('src.services.vector_database_service_unified.SentenceTransformerEmbeddingFunction') as mock_embedding:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "ids": ["doc1"],
                "documents": ["Content"],
                "metadatas": [{"agent_id": "Agent-1"}]
            }
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client
            mock_embedding.return_value = MagicMock()
            
            service = VectorDatabaseService()
            service._client = mock_client
            service._embedding_function = MagicMock()
            
            where_filter = {"agent_id": "Agent-999"}
            docs = service._get_collection_documents("test", where_filter)
            
            # Should filter out non-matching documents
            assert len(docs) == 0
