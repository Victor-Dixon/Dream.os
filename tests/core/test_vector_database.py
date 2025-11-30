#!/usr/bin/env python3
"""
Unit tests for vector_database.py - Infrastructure Test Coverage

Tests vector database utilities, connection helpers, and agent status operations.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sqlite3
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.vector_database import (
    get_connection,
    upsert_agent_status,
    fetch_agent_status,
    VectorDatabaseStats,
    CollectionConfig,
    AGENT_STATUS_TABLE,
    DB_PATH,
)
# Note: There are duplicate definitions in vector_database.py
# The exported ones are at the bottom of the file (dataclass versions)
from src.core.vector_database import (
    DocumentType,
    VectorDocument,
    EmbeddingModel,
    SearchQuery,
    SearchType,
    SearchResult,
)


class TestVectorDatabaseConnection:
    """Test suite for database connection helpers."""

    def test_get_connection_default_path(self, tmp_path):
        """Test getting connection with default path."""
        with patch('src.core.vector_database.DB_PATH', tmp_path / "vector_database.db"):
            conn = get_connection()
            assert conn is not None
            assert isinstance(conn, sqlite3.Connection)
            conn.close()

    def test_get_connection_custom_path(self, tmp_path):
        """Test getting connection with custom path."""
        custom_path = tmp_path / "custom.db"
        conn = get_connection(db_path=custom_path)
        assert conn is not None
        assert custom_path.exists()
        conn.close()

    def test_get_connection_creates_parent_dirs(self, tmp_path):
        """Test that connection creates parent directories."""
        nested_path = tmp_path / "nested" / "path" / "vector_database.db"
        conn = get_connection(db_path=nested_path)
        assert nested_path.parent.exists()
        assert nested_path.exists()
        conn.close()

    def test_get_connection_creates_table(self, tmp_path):
        """Test that connection creates agent status table."""
        with patch('src.core.vector_database.DB_PATH', tmp_path / "vector_database.db"):
            conn = get_connection()
            cursor = conn.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (AGENT_STATUS_TABLE,)
            )
            row = cursor.fetchone()
            assert row is not None
            assert row[0] == AGENT_STATUS_TABLE
            conn.close()


class TestAgentStatusOperations:
    """Test suite for agent status embedding operations."""

    @pytest.fixture
    def db_conn(self, tmp_path):
        """Create a temporary database connection."""
        db_path = tmp_path / "test_vector.db"
        conn = get_connection(db_path=db_path)
        yield conn
        conn.close()

    def test_upsert_agent_status_new(self, db_conn):
        """Test inserting new agent status."""
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        upsert_agent_status(
            db_conn,
            agent_id="Agent-1",
            raw_status='{"status": "active"}',
            embedding=embedding,
            last_updated="2025-01-01T12:00:00"
        )
        
        result = fetch_agent_status(db_conn, "Agent-1")
        assert result is not None
        agent_id, raw_status, fetched_embedding, last_updated = result
        assert agent_id == "Agent-1"
        assert raw_status == '{"status": "active"}'
        assert fetched_embedding == embedding
        assert last_updated == "2025-01-01T12:00:00"

    def test_upsert_agent_status_update(self, db_conn):
        """Test updating existing agent status."""
        embedding1 = [0.1, 0.2, 0.3]
        embedding2 = [0.4, 0.5, 0.6]
        
        upsert_agent_status(
            db_conn,
            agent_id="Agent-1",
            raw_status='{"status": "active"}',
            embedding=embedding1,
            last_updated="2025-01-01T12:00:00"
        )
        
        upsert_agent_status(
            db_conn,
            agent_id="Agent-1",
            raw_status='{"status": "inactive"}',
            embedding=embedding2,
            last_updated="2025-01-01T13:00:00"
        )
        
        result = fetch_agent_status(db_conn, "Agent-1")
        assert result is not None
        _, raw_status, fetched_embedding, last_updated = result
        assert raw_status == '{"status": "inactive"}'
        assert fetched_embedding == embedding2
        assert last_updated == "2025-01-01T13:00:00"

    def test_fetch_agent_status_existing(self, db_conn):
        """Test fetching existing agent status."""
        embedding = [0.1, 0.2, 0.3]
        upsert_agent_status(
            db_conn,
            agent_id="Agent-1",
            raw_status='{"status": "active"}',
            embedding=embedding,
            last_updated="2025-01-01T12:00:00"
        )
        
        result = fetch_agent_status(db_conn, "Agent-1")
        assert result is not None
        agent_id, raw_status, fetched_embedding, last_updated = result
        assert agent_id == "Agent-1"
        assert isinstance(fetched_embedding, list)
        assert len(fetched_embedding) == 3

    def test_fetch_agent_status_nonexistent(self, db_conn):
        """Test fetching non-existent agent status."""
        result = fetch_agent_status(db_conn, "Agent-999")
        assert result is None

    def test_upsert_multiple_agents(self, db_conn):
        """Test upserting multiple agents."""
        for i in range(1, 4):
            upsert_agent_status(
                db_conn,
                agent_id=f"Agent-{i}",
                raw_status=f'{{"status": "active{i}"}}',
                embedding=[float(i), float(i+1), float(i+2)],
                last_updated=f"2025-01-01T{12+i}:00:00"
            )
        
        for i in range(1, 4):
            result = fetch_agent_status(db_conn, f"Agent-{i}")
            assert result is not None
            assert result[0] == f"Agent-{i}"


class TestEnums:
    """Test suite for enum classes."""

    def test_document_type_enum(self):
        """Test DocumentType enum values (using exported version)."""
        assert DocumentType.AGENT_STATUS.value == "agent_status"
        assert DocumentType.MESSAGE.value == "message"
        assert DocumentType.LOG.value == "log"
        assert DocumentType.CONFIG.value == "config"

    def test_search_type_enum(self):
        """Test SearchType enum values (using exported version)."""
        assert SearchType.SEMANTIC.value == "semantic"
        assert SearchType.KEYWORD.value == "keyword"
        assert SearchType.HYBRID.value == "hybrid"

    def test_embedding_model_enum(self):
        """Test EmbeddingModel enum values (using exported version)."""
        assert EmbeddingModel.SENTENCE_TRANSFORMERS.value == "sentence_transformers"
        assert EmbeddingModel.OPENAI_ADA.value == "openai_ada"
        assert EmbeddingModel.OPENAI_3_SMALL.value == "openai_3_small"
        assert EmbeddingModel.OPENAI_3_LARGE.value == "openai_3_large"


class TestDataClasses:
    """Test suite for dataclass definitions."""

    def test_collection_config(self):
        """Test CollectionConfig dataclass."""
        config = CollectionConfig(
            name="test_collection",
            description="Test collection",
            embedding_dimension=128,
            similarity_threshold=0.7,
            max_documents=1000
        )
        assert config.name == "test_collection"
        assert config.description == "Test collection"
        assert config.embedding_dimension == 128
        assert config.similarity_threshold == 0.7
        assert config.max_documents == 1000
        assert config.metadata is None

    def test_collection_config_with_metadata(self):
        """Test CollectionConfig with metadata."""
        metadata = {"key": "value"}
        config = CollectionConfig(
            name="test",
            description="Test",
            embedding_dimension=128,
            metadata=metadata
        )
        assert config.metadata == metadata

    def test_vector_document(self):
        """Test VectorDocument dataclass."""
        doc = VectorDocument(
            content="Test content",
            metadata={"key": "value"}
        )
        assert doc.content == "Test content"
        assert doc.metadata == {"key": "value"}
        assert doc.document_id is None
        assert doc.document_type is None

    def test_vector_document_with_all_fields(self):
        """Test VectorDocument with all fields."""
        doc = VectorDocument(
            content="Test",
            metadata={},
            document_id="doc1",
            document_type=DocumentType.MESSAGE
        )
        assert doc.document_id == "doc1"
        assert doc.document_type == DocumentType.MESSAGE

    def test_search_query(self):
        """Test SearchQuery dataclass."""
        query = SearchQuery(
            query_text="test query",
            limit=20,
            threshold=0.5
        )
        assert query.query_text == "test query"
        assert query.limit == 20
        assert query.threshold == 0.5
        assert query.search_type is None
        assert query.metadata_filter is None

    def test_search_query_with_all_fields(self):
        """Test SearchQuery with all fields."""
        query = SearchQuery(
            query_text="test",
            limit=10,
            threshold=0.7,
            search_type=SearchType.SEMANTIC,
            metadata_filter={"agent": "Agent-1"}
        )
        assert query.search_type == SearchType.SEMANTIC
        assert query.metadata_filter == {"agent": "Agent-1"}

    def test_search_result(self):
        """Test SearchResult dataclass."""
        doc = VectorDocument(content="test", metadata={})
        result = SearchResult(
            document=doc,
            score=0.95,
            metadata={"key": "value"}
        )
        assert result.document == doc
        assert result.score == 0.95
        assert result.metadata == {"key": "value"}

    def test_vector_database_stats(self):
        """Test VectorDatabaseStats dataclass."""
        stats = VectorDatabaseStats(
            total_documents=100,
            total_collections=5
        )
        assert stats.total_documents == 100
        assert stats.total_collections == 5
        assert stats.last_updated is None
        assert stats.storage_size is None

    def test_vector_database_stats_with_all_fields(self):
        """Test VectorDatabaseStats with all fields."""
        stats = VectorDatabaseStats(
            total_documents=100,
            total_collections=5,
            last_updated="2025-01-01T12:00:00",
            storage_size=1024
        )
        assert stats.last_updated == "2025-01-01T12:00:00"
        assert stats.storage_size == 1024


class TestSearchResultDataclass:
    """Test suite for SearchResult dataclass."""

    def test_search_result_initialization(self):
        """Test SearchResult dataclass initialization."""
        doc = VectorDocument(content="Test content", metadata={})
        result = SearchResult(
            document=doc,
            score=0.95,
            metadata={"key": "value"}
        )
        assert result.document == doc
        assert result.score == 0.95
        assert result.metadata == {"key": "value"}


class TestConstants:
    """Test suite for module constants."""

    def test_agent_status_table_constant(self):
        """Test AGENT_STATUS_TABLE constant."""
        assert AGENT_STATUS_TABLE == "agent_status_embeddings"

    def test_db_path_constant(self):
        """Test DB_PATH constant."""
        assert DB_PATH == Path("data/vector_database.db")

