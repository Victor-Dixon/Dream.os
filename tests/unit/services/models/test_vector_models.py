"""
Tests for Vector Models - SSOT Verification

Tests for SearchResult and SearchQuery SSOT models.
Ensures backward compatibility and SSOT compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-05
"""

import pytest
from datetime import datetime
from typing import Dict, Any

from src.services.models.vector_models import (
    SearchResult,
    SearchQuery,
    SearchType,
    VectorDocument,
    EmbeddingModel,
)


class TestSearchQuery:
    """Tests for SearchQuery SSOT model."""

    def test_search_query_creation(self):
        """Test basic SearchQuery creation."""
        query = SearchQuery(
            query_text="test query",
            search_type=SearchType.SIMILARITY,
            limit=10,
            similarity_threshold=0.5
        )
        assert query.query_text == "test query"
        assert query.search_type == SearchType.SIMILARITY
        assert query.limit == 10
        assert query.similarity_threshold == 0.5

    def test_search_query_backward_compatibility_query(self):
        """Test backward compatibility with 'query' field."""
        query = SearchQuery(
            query="legacy query",
            limit=5
        )
        assert query.query_text == "legacy query"
        assert query.query_alias == "legacy query"

    def test_search_query_backward_compatibility_threshold(self):
        """Test backward compatibility with 'threshold' field."""
        query = SearchQuery(
            query_text="test",
            threshold=0.7
        )
        assert query.similarity_threshold == 0.7
        assert query.threshold_alias == 0.7

    def test_search_query_backward_compatibility_metadata_filter(self):
        """Test backward compatibility with 'metadata_filter' field."""
        filters = {"agent_id": "Agent-1"}
        query = SearchQuery(
            query_text="test",
            metadata_filter=filters
        )
        assert query.filters == filters
        assert query.metadata_filter_alias == filters

    def test_search_query_defaults(self):
        """Test SearchQuery default values."""
        query = SearchQuery(query_text="test")
        assert query.search_type == SearchType.SIMILARITY
        assert query.limit == 10
        assert query.similarity_threshold == 0.0
        assert query.filters is None

    def test_search_query_agent_id(self):
        """Test agent_id field for agent-specific queries."""
        query = SearchQuery(
            query_text="test",
            agent_id="Agent-8"
        )
        assert query.agent_id == "Agent-8"


class TestSearchResult:
    """Tests for SearchResult SSOT model."""

    def test_search_result_creation(self):
        """Test basic SearchResult creation."""
        result = SearchResult(
            document_id="doc1",
            content="test content",
            similarity_score=0.85,
            metadata={"key": "value"}
        )
        assert result.document_id == "doc1"
        assert result.content == "test content"
        assert result.similarity_score == 0.85
        assert result.metadata == {"key": "value"}

    def test_search_result_backward_compatibility_id(self):
        """Test backward compatibility with 'id' field."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.5,
            metadata={},
            id="doc1"  # id is optional, document_id is required
        )
        assert result.document_id == "doc1"
        assert result.id_alias == "doc1"

    def test_search_result_backward_compatibility_result_id(self):
        """Test backward compatibility with 'result_id' field."""
        result = SearchResult(
            document_id="result1",
            content="test",
            similarity_score=0.5,
            metadata={},
            result_id="result1"  # result_id is optional, document_id is required
        )
        assert result.document_id == "result1"
        assert result.result_id_alias == "result1"

    def test_search_result_backward_compatibility_score(self):
        """Test backward compatibility with 'score' field."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.9,  # Set directly, score is optional alias
            metadata={},
            score=0.9
        )
        assert result.similarity_score == 0.9
        assert result.score_alias == 0.9

    def test_search_result_backward_compatibility_relevance(self):
        """Test backward compatibility with 'relevance' field."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.8,  # Set directly, relevance is optional alias
            metadata={},
            relevance=0.8
        )
        assert result.similarity_score == 0.8
        assert result.relevance_alias == 0.8

    def test_search_result_backward_compatibility_relevance_score(self):
        """Test backward compatibility with 'relevance_score' field."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.75,  # Set directly, relevance_score is optional alias
            metadata={},
            relevance_score=0.75
        )
        assert result.similarity_score == 0.75
        assert result.relevance_score_alias == 0.75

    def test_search_result_web_fields(self):
        """Test web-specific fields (title, collection, tags)."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.5,
            metadata={},
            title="Test Title",
            collection="test_collection",
            tags=["tag1", "tag2"]
        )
        assert result.title == "Test Title"
        assert result.collection == "test_collection"
        assert result.tags == ["tag1", "tag2"]

    def test_search_result_context_fields(self):
        """Test intelligent context fields."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.5,
            metadata={},
            source_type="vector_db",
            source_id="source1",
            timestamp=datetime.now()
        )
        assert result.source_type == "vector_db"
        assert result.source_id == "source1"
        assert result.timestamp is not None

    def test_search_result_to_dict(self):
        """Test SearchResult to_dict conversion."""
        result = SearchResult(
            document_id="doc1",
            content="test content",
            similarity_score=0.85,
            metadata={"key": "value"},
            title="Test Title"
        )
        result_dict = result.to_dict()
        assert result_dict["document_id"] == "doc1"
        assert result_dict["content"] == "test content"
        assert result_dict["similarity_score"] == 0.85
        assert result_dict["metadata"] == {"key": "value"}
        assert result_dict["title"] == "Test Title"

    def test_search_result_default_metadata(self):
        """Test SearchResult handles None metadata."""
        result = SearchResult(
            document_id="doc1",
            content="test",
            similarity_score=0.5,
            metadata=None
        )
        assert result.metadata == {}


class TestSearchType:
    """Tests for SearchType enum."""

    def test_search_type_values(self):
        """Test SearchType enum values."""
        assert SearchType.SIMILARITY.value == "similarity"
        assert SearchType.MAX_MARGINAL_RELEVANCE.value == "mmr"
        assert SearchType.FILTERED.value == "filtered"


class TestVectorDocument:
    """Tests for VectorDocument model."""

    def test_vector_document_creation(self):
        """Test VectorDocument creation."""
        doc = VectorDocument(
            id="doc1",
            content="test content",
            embedding=[0.1, 0.2, 0.3],
            metadata={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert doc.id == "doc1"
        assert doc.content == "test content"
        assert len(doc.embedding) == 3

    def test_vector_document_from_dict(self):
        """Test VectorDocument from_dict."""
        data = {
            "id": "doc1",
            "content": "test",
            "embedding": [0.1, 0.2],
            "metadata": {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        doc = VectorDocument.from_dict(data)
        assert doc.id == "doc1"
        assert doc.content == "test"

    def test_vector_document_to_dict(self):
        """Test VectorDocument to_dict."""
        doc = VectorDocument(
            id="doc1",
            content="test",
            embedding=[0.1, 0.2],
            metadata={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        doc_dict = doc.to_dict()
        assert doc_dict["id"] == "doc1"
        assert doc_dict["content"] == "test"
        assert "embedding" in doc_dict


class TestEmbeddingModel:
    """Tests for EmbeddingModel enum."""

    def test_embedding_model_values(self):
        """Test EmbeddingModel enum values."""
        assert EmbeddingModel.SENTENCE_TRANSFORMERS.value == "sentence_transformers"
        assert EmbeddingModel.OPENAI.value == "openai"
        assert EmbeddingModel.HUGGINGFACE.value == "huggingface"

