"""
Unit tests for src/services/swarm_intelligence_manager.py

Tests swarm intelligence functionality including:
- Swarm intelligence retrieval
- Coordination opportunities
- Swarm synchronization
- Knowledge sharing
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from src.services.swarm_intelligence_manager import SwarmIntelligenceManager


class TestSwarmIntelligenceManager:
    """Test swarm intelligence manager."""

    @pytest.fixture
    def manager_with_vector_db(self):
        """Create manager with vector DB available."""
        with patch('src.services.swarm_intelligence_manager.get_vector_database_service') as mock_get:
            mock_vector_db = MagicMock()
            mock_get.return_value = mock_vector_db
            
            manager = SwarmIntelligenceManager("Agent-5")
            return manager

    @pytest.fixture
    def manager_without_vector_db(self):
        """Create manager without vector DB."""
        with patch('src.services.swarm_intelligence_manager.get_vector_database_service') as mock_get:
            mock_get.side_effect = ImportError("Vector DB not available")
            
            manager = SwarmIntelligenceManager("Agent-5")
            return manager

    def test_init_with_vector_db(self, manager_with_vector_db):
        """Test initialization with vector database."""
        assert manager_with_vector_db.agent_id == "Agent-5"
        assert manager_with_vector_db.vector_integration["status"] == "connected"

    def test_init_without_vector_db(self, manager_without_vector_db):
        """Test initialization without vector database."""
        assert manager_without_vector_db.agent_id == "Agent-5"
        assert manager_without_vector_db.vector_integration["status"] == "disconnected"

    def test_load_config(self, manager_with_vector_db):
        """Test configuration loading."""
        config = manager_with_vector_db.config
        
        assert "swarm_agents" in config
        assert "coordination_threshold" in config
        assert "knowledge_sharing_enabled" in config
        assert len(config["swarm_agents"]) == 8

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_get_swarm_intelligence(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test getting swarm intelligence."""
        mock_search.return_value = [MagicMock()]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        result = manager_with_vector_db.get_swarm_intelligence("test query")
        
        assert "query" in result
        assert "insights" in result
        assert "coordination_opportunities" in result
        assert "swarm_patterns" in result
        assert "confidence" in result
        assert "source_agents" in result
        assert "timestamp" in result

    def test_get_swarm_intelligence_fallback(self, manager_without_vector_db):
        """Test getting swarm intelligence with fallback mode."""
        result = manager_without_vector_db.get_swarm_intelligence("test query")
        
        assert result["query"] == "test query"
        assert result["fallback_mode"] is True
        assert len(result["insights"]) > 0

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_sync_with_swarm(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test syncing with swarm."""
        mock_search.return_value = [MagicMock()]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        result = manager_with_vector_db.sync_with_swarm()
        
        assert isinstance(result, bool)

    def test_sync_with_swarm_no_vector_db(self, manager_without_vector_db):
        """Test syncing with swarm when vector DB unavailable."""
        result = manager_without_vector_db.sync_with_swarm()
        
        assert result is False

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_search_collective_knowledge(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test searching collective knowledge."""
        mock_result = MagicMock()
        mock_result.document.content = "Test content"
        mock_search.return_value = [mock_result]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        insights = manager_with_vector_db._search_collective_knowledge("test")
        
        assert isinstance(insights, list)

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_find_coordination_opportunities(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test finding coordination opportunities."""
        mock_search.return_value = [MagicMock()]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        opportunities = manager_with_vector_db._find_coordination_opportunities("test")
        
        assert isinstance(opportunities, list)

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_analyze_swarm_patterns(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test analyzing swarm patterns."""
        mock_result = MagicMock()
        mock_result.document.tags = ["coordination", "testing"]
        mock_search.return_value = [mock_result]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        patterns = manager_with_vector_db._analyze_swarm_patterns("test")
        
        assert isinstance(patterns, list)

    def test_calculate_confidence_no_insights(self, manager_with_vector_db):
        """Test confidence calculation with no insights."""
        confidence = manager_with_vector_db._calculate_confidence([])
        
        assert confidence == 0.3

    def test_calculate_confidence_with_insights(self, manager_with_vector_db):
        """Test confidence calculation with insights."""
        insights = ["insight1", "insight2", "insight3"]
        confidence = manager_with_vector_db._calculate_confidence(insights)
        
        assert 0.3 <= confidence <= 0.9

    def test_get_contributing_agents(self, manager_with_vector_db):
        """Test getting contributing agents."""
        insights = ["From Agent-1: content", "From Agent-2: content"]
        agents = manager_with_vector_db._get_contributing_agents(insights)
        
        assert isinstance(agents, list)
        assert "Agent-1" in agents
        assert "Agent-2" in agents

    def test_get_contributing_agents_no_insights(self, manager_with_vector_db):
        """Test getting contributing agents with no insights."""
        agents = manager_with_vector_db._get_contributing_agents([])
        
        assert isinstance(agents, list)

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_share_knowledge_with_swarm(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test sharing knowledge with swarm."""
        mock_result = MagicMock()
        mock_result.document.tags = []
        mock_search.return_value = [mock_result]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        count = manager_with_vector_db._share_knowledge_with_swarm()
        
        assert isinstance(count, int)
        assert count >= 0

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_update_from_swarm_knowledge(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test updating from swarm knowledge."""
        mock_result = MagicMock()
        mock_result.document.tags = ["swarm-shared", "coordination"]
        mock_search.return_value = [mock_result]
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        count = manager_with_vector_db._update_from_swarm_knowledge()
        
        assert isinstance(count, int)
        assert count >= 0

    def test_is_relevant_to_agent_relevant(self, manager_with_vector_db):
        """Test relevance check with relevant document."""
        mock_doc = MagicMock()
        mock_doc.tags = ["coordination", "testing"]
        
        is_relevant = manager_with_vector_db._is_relevant_to_agent(mock_doc)
        
        assert is_relevant is True

    def test_is_relevant_to_agent_not_relevant(self, manager_with_vector_db):
        """Test relevance check with non-relevant document."""
        mock_doc = MagicMock()
        mock_doc.tags = ["other", "tags"]
        
        is_relevant = manager_with_vector_db._is_relevant_to_agent(mock_doc)
        
        assert is_relevant is False

    def test_is_relevant_to_agent_no_tags(self, manager_with_vector_db):
        """Test relevance check with no tags."""
        mock_doc = MagicMock()
        mock_doc.tags = None
        
        is_relevant = manager_with_vector_db._is_relevant_to_agent(mock_doc)
        
        assert is_relevant is False

    def test_get_fallback_intelligence(self, manager_with_vector_db):
        """Test getting fallback intelligence."""
        result = manager_with_vector_db._get_fallback_intelligence("test query")
        
        assert result["query"] == "test query"
        assert result["fallback_mode"] is True
        assert len(result["insights"]) > 0
        assert "confidence" in result

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_get_swarm_intelligence_error_handling(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test error handling in get_swarm_intelligence."""
        mock_search.side_effect = Exception("Test error")
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        result = manager_with_vector_db.get_swarm_intelligence("test")
        
        assert "error" in result
        assert result["query"] == "test"

    @patch('src.services.swarm_intelligence_manager.search_vector_database')
    @patch('src.services.swarm_intelligence_manager.SearchQuery')
    def test_sync_with_swarm_error_handling(self, mock_search_query, mock_search, manager_with_vector_db):
        """Test error handling in sync_with_swarm."""
        mock_search.side_effect = Exception("Test error")
        mock_query_instance = MagicMock()
        mock_search_query.return_value = mock_query_instance
        
        result = manager_with_vector_db.sync_with_swarm()
        
        assert result is False

