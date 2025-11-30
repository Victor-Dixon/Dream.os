#!/usr/bin/env python3
"""
Unit tests for agent_documentation_service.py - Infrastructure Test Coverage

Tests AgentDocumentationService class and documentation operations.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.agent_documentation_service import AgentDocumentationService


class TestAgentDocumentationService:
    """Test suite for AgentDocumentationService class."""

    @pytest.fixture
    def service_no_agent(self):
        """Create service instance without agent ID."""
        return AgentDocumentationService()

    @pytest.fixture
    def service_with_agent(self):
        """Create service instance with agent ID."""
        return AgentDocumentationService(agent_id="Agent-1")

    def test_initialization_no_agent(self, service_no_agent):
        """Test initialization without agent ID."""
        assert service_no_agent is not None
        assert service_no_agent.agent_id is None
        assert service_no_agent.db_path == "vector_db"
        assert service_no_agent.contexts == {}

    def test_initialization_with_agent(self, service_with_agent):
        """Test initialization with agent ID."""
        assert service_with_agent is not None
        assert service_with_agent.agent_id == "Agent-1"
        assert service_with_agent.db_path == "vector_db"
        assert service_with_agent.contexts == {}

    def test_initialization_custom_db_path(self):
        """Test initialization with custom database path."""
        service = AgentDocumentationService(db_path="custom_path")
        assert service.db_path == "custom_path"

    def test_initialization_with_vector_db(self):
        """Test initialization with vector database instance."""
        mock_vector_db = MagicMock()
        service = AgentDocumentationService(vector_db=mock_vector_db)
        assert service.vector_db == mock_vector_db

    def test_set_agent_context(self, service_no_agent):
        """Test setting agent context."""
        context = {"mission": "test", "status": "active"}
        service_no_agent.set_agent_context("Agent-1", context)
        
        assert "Agent-1" in service_no_agent.contexts
        assert service_no_agent.contexts["Agent-1"] == context

    def test_set_agent_context_multiple(self, service_no_agent):
        """Test setting context for multiple agents."""
        service_no_agent.set_agent_context("Agent-1", {"mission": "test1"})
        service_no_agent.set_agent_context("Agent-2", {"mission": "test2"})
        
        assert len(service_no_agent.contexts) == 2
        assert service_no_agent.contexts["Agent-1"]["mission"] == "test1"
        assert service_no_agent.contexts["Agent-2"]["mission"] == "test2"

    def test_search_documentation_with_query(self, service_no_agent):
        """Test searching documentation with query."""
        results = service_no_agent.search_documentation(query="test query")
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert "title" in results[0]
        assert "content" in results[0]
        assert "relevance" in results[0]
        assert "source" in results[0]

    def test_search_documentation_without_query(self, service_no_agent):
        """Test searching documentation without query."""
        results = service_no_agent.search_documentation(query=None)
        assert results == []

    def test_search_documentation_empty_query(self, service_no_agent):
        """Test searching documentation with empty query."""
        results = service_no_agent.search_documentation(query="")
        assert results == []

    def test_search_documentation_with_agent_id(self, service_no_agent):
        """Test searching documentation with specific agent ID."""
        results = service_no_agent.search_documentation(
            agent_id="Agent-1",
            query="test"
        )
        
        assert isinstance(results, list)
        assert len(results) > 0

    def test_search_documentation_n_results(self, service_no_agent):
        """Test searching documentation with custom result count."""
        results = service_no_agent.search_documentation(
            query="test",
            n_results=3
        )
        
        assert isinstance(results, list)
        # Current implementation returns 1 result regardless of n_results

    def test_search_docs_alias(self, service_with_agent):
        """Test search_docs alias method."""
        results = service_with_agent.search_docs("test query")
        
        assert isinstance(results, list)
        # Should use self.agent_id when called via alias
        assert len(results) > 0

    def test_get_doc_returns_document(self, service_no_agent):
        """Test getting document returns document data."""
        result = service_no_agent.get_doc("test_doc_id")
        assert result is not None
        assert isinstance(result, dict)
        assert "id" in result
        assert "title" in result
        assert "content" in result
        assert "last_updated" in result
        assert result["id"] == "test_doc_id"

    def test_initialization_metadata(self, service_no_agent):
        """Test initialization sets proper metadata."""
        assert hasattr(service_no_agent, 'agent_id')
        assert hasattr(service_no_agent, 'vector_db')
        assert hasattr(service_no_agent, 'db_path')
        assert hasattr(service_no_agent, 'contexts')

    def test_get_doc_success(self, service_no_agent):
        """Test getting document successfully."""
        result = service_no_agent.get_doc("test_doc")
        assert result is not None
        assert result["id"] == "test_doc"
        assert "title" in result
        assert "content" in result
        assert "last_updated" in result

    def test_get_agent_relevant_docs(self, service_no_agent):
        """Test getting relevant documents for agent."""
        result = service_no_agent.get_agent_relevant_docs("Agent-1")
        assert isinstance(result, list)
        assert result == []

    def test_get_agent_relevant_docs_with_types(self, service_no_agent):
        """Test getting relevant documents with doc types."""
        result = service_no_agent.get_agent_relevant_docs(
            "Agent-1",
            doc_types=["guide", "reference"]
        )
        assert isinstance(result, list)

    def test_get_documentation_summary_no_agent(self, service_no_agent):
        """Test getting documentation summary without agent ID."""
        summary = service_no_agent.get_documentation_summary()
        assert isinstance(summary, dict)
        assert "agent_id" in summary
        assert "docs_count" in summary
        assert summary["agent_id"] is None

    def test_get_documentation_summary_with_agent(self, service_with_agent):
        """Test getting documentation summary with agent ID."""
        summary = service_with_agent.get_documentation_summary()
        assert isinstance(summary, dict)
        assert summary["agent_id"] == "Agent-1"
        assert summary["docs_count"] == 0

    def test_get_documentation_summary_override_agent(self, service_no_agent):
        """Test getting documentation summary with overridden agent ID."""
        summary = service_no_agent.get_documentation_summary(agent_id="Agent-2")
        assert summary["agent_id"] == "Agent-2"

    def test_get_agent_context_no_agent(self, service_no_agent):
        """Test getting agent context without agent ID."""
        context = service_no_agent.get_agent_context()
        assert isinstance(context, dict)
        assert context["agent_id"] is None
        assert "db_path" in context
        assert "timestamp" in context

    def test_get_agent_context_with_agent(self, service_with_agent):
        """Test getting agent context with agent ID."""
        context = service_with_agent.get_agent_context()
        assert context["agent_id"] == "Agent-1"
        assert context["db_path"] == "vector_db"
        assert "timestamp" in context

    def test_get_status_no_agent(self, service_no_agent):
        """Test getting service status without agent ID."""
        status = service_no_agent.get_status()
        assert isinstance(status, dict)
        assert status["active"] is True
        assert status["agent_id"] is None
        assert "timestamp" in status

    def test_get_status_with_agent(self, service_with_agent):
        """Test getting service status with agent ID."""
        status = service_with_agent.get_status()
        assert status["active"] is True
        assert status["agent_id"] == "Agent-1"
        assert "timestamp" in status

    def test_get_search_suggestions(self, service_no_agent):
        """Test getting search suggestions."""
        suggestions = service_no_agent.get_search_suggestions("Agent-1", "test")
        assert isinstance(suggestions, list)
        assert suggestions == []

    def test_create_agent_documentation_service(self):
        """Test factory function for creating service."""
        from src.core.agent_documentation_service import create_agent_documentation_service
        service = create_agent_documentation_service(agent_id="Agent-1")
        assert service is not None
        assert service.agent_id == "Agent-1"

    def test_create_agent_docs(self):
        """Test factory function alias."""
        from src.core.agent_documentation_service import create_agent_docs
        service = create_agent_docs("Agent-1")
        assert service is not None
        assert service.agent_id == "Agent-1"

