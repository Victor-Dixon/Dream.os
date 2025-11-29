"""
Tests for vector_models.py

Comprehensive test suite for vector database models.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from datetime import datetime
from typing import Dict, Any

from src.services.models.vector_models import (
    EmbeddingModel,
    DocumentType,
    SearchType,
    VectorDocument,
    EmbeddingResult,
    SearchQuery,
    SearchResult,
    SimilaritySearchResult
)


class TestEmbeddingModel:
    """Test EmbeddingModel enum."""

    def test_enum_values(self):
        """Test enum has expected values."""
        assert EmbeddingModel.SENTENCE_TRANSFORMERS.value == "sentence_transformers"
        assert EmbeddingModel.OPENAI.value == "openai"
        assert EmbeddingModel.HUGGINGFACE.value == "huggingface"
        assert EmbeddingModel.OPENAI_ADA.value == "openai-ada-002"
        assert EmbeddingModel.OPENAI_3_SMALL.value == "openai-3-small"
        assert EmbeddingModel.OPENAI_3_LARGE.value == "openai-3-large"

    def test_enum_membership(self):
        """Test enum membership."""
        assert EmbeddingModel.SENTENCE_TRANSFORMERS in EmbeddingModel
        assert EmbeddingModel.OPENAI in EmbeddingModel


class TestDocumentType:
    """Test DocumentType enum."""

    def test_enum_values(self):
        """Test enum has expected values."""
        assert DocumentType.MESSAGE.value == "message"
        assert DocumentType.DEVLOG.value == "devlog"
        assert DocumentType.CONTRACT.value == "contract"
        assert DocumentType.STATUS.value == "status"
        assert DocumentType.CODE.value == "code"
        assert DocumentType.DOCUMENTATION.value == "documentation"

    def test_enum_usage(self):
        """Test enum can be used."""
        doc_type = DocumentType.MESSAGE
        assert doc_type.value == "message"


class TestSearchType:
    """Test SearchType enum."""

    def test_enum_values(self):
        """Test enum has expected values."""
        assert SearchType.SIMILARITY.value == "similarity"
        assert SearchType.MAX_MARGINAL_RELEVANCE.value == "mmr"
        assert SearchType.FILTERED.value == "filtered"


class TestVectorDocument:
    """Test VectorDocument dataclass."""

    def test_create_vector_document(self):
        """Test creating VectorDocument."""
        doc = VectorDocument(
            id="doc_1",
            content="Test content",
            embedding=[0.1, 0.2, 0.3],
            metadata={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert doc.id == "doc_1"
        assert doc.content == "Test content"
        assert doc.embedding == [0.1, 0.2, 0.3]
        assert doc.metadata == {"key": "value"}

    def test_from_dict(self):
        """Test creating VectorDocument from dictionary."""
        data = {
            "id": "doc_1",
            "content": "Test",
            "embedding": [0.1, 0.2],
            "metadata": {"key": "value"},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        doc = VectorDocument.from_dict(data)
        
        assert doc.id == "doc_1"
        assert doc.content == "Test"
        assert isinstance(doc.created_at, datetime)

    def test_from_dict_default_metadata(self):
        """Test from_dict with default metadata."""
        data = {
            "id": "doc_1",
            "content": "Test",
            "embedding": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        doc = VectorDocument.from_dict(data)
        
        assert doc.metadata == {}

    def test_to_dict(self):
        """Test converting VectorDocument to dictionary."""
        doc = VectorDocument(
            id="doc_1",
            content="Test",
            embedding=[0.1, 0.2],
            metadata={"key": "value"},
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            updated_at=datetime(2025, 1, 1, 12, 0, 0)
        )
        
        result = doc.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == "doc_1"
        assert result["content"] == "Test"
        assert result["embedding"] == [0.1, 0.2]
        assert result["metadata"] == {"key": "value"}
        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)

    def test_to_dict_roundtrip(self):
        """Test to_dict and from_dict roundtrip."""
        original = VectorDocument(
            id="doc_1",
            content="Test",
            embedding=[0.1, 0.2],
            metadata={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        data = original.to_dict()
        restored = VectorDocument.from_dict(data)
        
        assert restored.id == original.id
        assert restored.content == original.content
        assert restored.embedding == original.embedding


class TestEmbeddingResult:
    """Test EmbeddingResult dataclass."""

    def test_create_embedding_result_success(self):
        """Test creating successful EmbeddingResult."""
        result = EmbeddingResult(
            document_id="doc_1",
            embedding=[0.1, 0.2, 0.3],
            model=EmbeddingModel.SENTENCE_TRANSFORMERS,
            tokens_used=100,
            processing_time=0.5,
            success=True
        )
        
        assert result.document_id == "doc_1"
        assert result.success is True
        assert result.error_message is None

    def test_create_embedding_result_failure(self):
        """Test creating failed EmbeddingResult."""
        result = EmbeddingResult(
            document_id="doc_1",
            embedding=[],
            model=EmbeddingModel.SENTENCE_TRANSFORMERS,
            tokens_used=0,
            processing_time=0.0,
            success=False,
            error_message="Embedding failed"
        )
        
        assert result.success is False
        assert result.error_message == "Embedding failed"


class TestSearchQuery:
    """Test SearchQuery dataclass."""

    def test_create_search_query_defaults(self):
        """Test creating SearchQuery with defaults."""
        query = SearchQuery(query_text="test query")
        
        assert query.query_text == "test query"
        assert query.search_type == SearchType.SIMILARITY
        assert query.limit == 10
        assert query.similarity_threshold == 0.0
        assert query.filters is None

    def test_create_search_query_custom(self):
        """Test creating SearchQuery with custom parameters."""
        query = SearchQuery(
            query_text="test",
            search_type=SearchType.MAX_MARGINAL_RELEVANCE,
            limit=5,
            similarity_threshold=0.7,
            filters={"key": "value"}
        )
        
        assert query.search_type == SearchType.MAX_MARGINAL_RELEVANCE
        assert query.limit == 5
        assert query.similarity_threshold == 0.7
        assert query.filters == {"key": "value"}


class TestSearchResult:
    """Test SearchResult dataclass."""

    def test_create_search_result(self):
        """Test creating SearchResult."""
        result = SearchResult(
            document_id="doc_1",
            content="Test content",
            similarity_score=0.85,
            metadata={"key": "value"}
        )
        
        assert result.document_id == "doc_1"
        assert result.content == "Test content"
        assert result.similarity_score == 0.85
        assert result.metadata == {"key": "value"}


class TestSimilaritySearchResult:
    """Test SimilaritySearchResult dataclass."""

    def test_create_similarity_search_result(self):
        """Test creating SimilaritySearchResult."""
        result = SimilaritySearchResult(
            query_embedding=[0.1, 0.2, 0.3],
            results=[{"id": "doc_1", "score": 0.85}],
            search_time=0.5,
            total_candidates=10
        )
        
        assert result.query_embedding == [0.1, 0.2, 0.3]
        assert len(result.results) == 1
        assert result.search_time == 0.5
        assert result.total_candidates == 10

    def test_create_similarity_search_result_empty(self):
        """Test creating SimilaritySearchResult with empty results."""
        result = SimilaritySearchResult(
            query_embedding=[],
            results=[],
            search_time=0.0,
            total_candidates=0
        )
        
        assert len(result.results) == 0
        assert result.total_candidates == 0

    def test_embedding_model_all_values(self):
        """Test all EmbeddingModel enum values."""
        all_values = [model.value for model in EmbeddingModel]
        
        expected_values = [
            "sentence_transformers",
            "openai",
            "huggingface",
            "openai-ada-002",
            "openai-3-small",
            "openai-3-large"
        ]
        
        for expected in expected_values:
            assert expected in all_values

    def test_document_type_all_values(self):
        """Test all DocumentType enum values."""
        all_values = [doc_type.value for doc_type in DocumentType]
        
        expected_values = [
            "message",
            "devlog",
            "contract",
            "status",
            "code",
            "documentation"
        ]
        
        for expected in expected_values:
            assert expected in all_values

    def test_search_type_all_values(self):
        """Test all SearchType enum values."""
        all_values = [search_type.value for search_type in SearchType]
        
        expected_values = [
            "similarity",
            "mmr",
            "filtered"
        ]
        
        for expected in expected_values:
            assert expected in all_values

    def test_vector_document_embedding_none(self):
        """Test VectorDocument with None embedding."""
        doc = VectorDocument(
            id="doc_1",
            content="Test",
            embedding=None,
            metadata={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert doc.embedding is None

    def test_vector_document_empty_embedding(self):
        """Test VectorDocument with empty embedding list."""
        doc = VectorDocument(
            id="doc_1",
            content="Test",
            embedding=[],
            metadata={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert doc.embedding == []

    def test_embedding_result_with_error_message(self):
        """Test EmbeddingResult with error message."""
        result = EmbeddingResult(
            document_id="doc_1",
            embedding=[],
            model=EmbeddingModel.SENTENCE_TRANSFORMERS,
            tokens_used=0,
            processing_time=0.0,
            success=False,
            error_message="Embedding failed: timeout"
        )
        
        assert result.success is False
        assert "timeout" in result.error_message

    def test_search_query_with_filters(self):
        """Test SearchQuery with complex filters."""
        query = SearchQuery(
            query_text="test",
            filters={"agent_id": "Agent-7", "type": "code", "status": "active"}
        )
        
        assert query.filters is not None
        assert query.filters["agent_id"] == "Agent-7"
        assert len(query.filters) == 3

    def test_search_result_minimal(self):
        """Test SearchResult with minimal data."""
        result = SearchResult(
            document_id="doc_1",
            content="",
            similarity_score=0.0,
            metadata={}
        )
        
        assert result.document_id == "doc_1"
        assert result.content == ""
        assert result.similarity_score == 0.0

    def test_similarity_search_result_large_embedding(self):
        """Test SimilaritySearchResult with large embedding vector."""
        large_embedding = [0.1] * 1000
        result = SimilaritySearchResult(
            query_embedding=large_embedding,
            results=[],
            search_time=1.5,
            total_candidates=1000
        )
        
        assert len(result.query_embedding) == 1000
        assert result.total_candidates == 1000

    def test_vector_document_metadata_nested(self):
        """Test VectorDocument with nested metadata."""
        doc = VectorDocument(
            id="doc_1",
            content="Test",
            embedding=[0.1, 0.2],
            metadata={
                "nested": {
                    "key1": "value1",
                    "key2": ["item1", "item2"]
                }
            },
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert "nested" in doc.metadata
        assert doc.metadata["nested"]["key1"] == "value1"

    def test_vector_document_datetime_handling(self):
        """Test VectorDocument datetime serialization."""
        now = datetime.now()
        doc = VectorDocument(
            id="doc_1",
            content="Test",
            embedding=[0.1],
            metadata={},
            created_at=now,
            updated_at=now
        )
        
        data = doc.to_dict()
        restored = VectorDocument.from_dict(data)
        
        assert restored.created_at.isoformat() == now.isoformat()

