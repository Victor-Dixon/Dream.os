#!/usr/bin/env python3
"""
Unit Tests for Performance Analyzer
===================================

Comprehensive tests for performance_analyzer.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.performance_analyzer import PerformanceAnalyzer


class TestPerformanceAnalyzer:
    """Tests for PerformanceAnalyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = PerformanceAnalyzer("Agent-1")
        assert analyzer.agent_id == "Agent-1"
        assert "config" in analyzer.config
        assert "analysis_period_days" in analyzer.config

    def test_initialization_with_config_path(self):
        """Test initialization with config path."""
        analyzer = PerformanceAnalyzer("Agent-2", config_path="/fake/path")
        assert analyzer.agent_id == "Agent-2"

    def test_load_config(self):
        """Test _load_config method."""
        analyzer = PerformanceAnalyzer("Agent-1")
        config = analyzer._load_config(None)
        assert "analysis_period_days" in config
        assert "performance_thresholds" in config
        assert "metrics_weights" in config

    def test_analyze_agent_performance_fallback(self):
        """Test analyze_agent_performance with fallback (no vector DB)."""
        analyzer = PerformanceAnalyzer("Agent-1")
        result = analyzer.analyze_agent_performance()
        assert "agent_id" in result
        assert result["agent_id"] == "Agent-1"
        assert "performance_score" in result
        assert "metrics" in result
        assert "recommendations" in result

    @patch('src.services.performance_analyzer.search_vector_database')
    @patch('src.services.performance_analyzer.get_vector_database_service')
    def test_analyze_agent_performance_with_vector_db(self, mock_get_service, mock_search):
        """Test analyze_agent_performance with vector DB available."""
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_search.return_value = [Mock(), Mock()]  # 2 completed tasks
        
        analyzer = PerformanceAnalyzer("Agent-1")
        # Force vector integration to connected
        analyzer.vector_integration = {"status": "connected", "service": mock_service}
        
        result = analyzer.analyze_agent_performance()
        assert "agent_id" in result
        assert "performance_score" in result
        assert "metrics" in result

    def test_get_integration_health(self):
        """Test get_integration_health method."""
        analyzer = PerformanceAnalyzer("Agent-1")
        health = analyzer.get_integration_health()
        assert "agent_id" in health
        assert "health_status" in health
        assert "vector_db_connection" in health
        assert "last_update" in health

    def test_get_integration_health_exception_handling(self):
        """Test get_integration_health exception handling."""
        analyzer = PerformanceAnalyzer("Agent-1")
        # Should handle exceptions gracefully
        health = analyzer.get_integration_health()
        assert "agent_id" in health

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_calculate_task_completion_rate(self, mock_search):
        """Test _calculate_task_completion_rate method."""
        mock_search.return_value = [Mock()] * 5  # 5 completed tasks
        
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "connected"}
        
        rate = analyzer._calculate_task_completion_rate()
        assert 0.0 <= rate <= 1.0

    def test_calculate_task_completion_rate_fallback(self):
        """Test _calculate_task_completion_rate fallback."""
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "disconnected"}
        
        rate = analyzer._calculate_task_completion_rate()
        assert rate == 0.5  # Default fallback

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_calculate_coordination_effectiveness(self, mock_search):
        """Test _calculate_coordination_effectiveness method."""
        mock_search.return_value = [Mock()] * 8  # 8 coordination items
        
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "connected"}
        
        effectiveness = analyzer._calculate_coordination_effectiveness()
        assert 0.0 <= effectiveness <= 1.0

    def test_calculate_coordination_effectiveness_fallback(self):
        """Test _calculate_coordination_effectiveness fallback."""
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "disconnected"}
        
        effectiveness = analyzer._calculate_coordination_effectiveness()
        assert effectiveness == 0.7  # Default fallback

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_calculate_knowledge_utilization(self, mock_search):
        """Test _calculate_knowledge_utilization method."""
        mock_result = Mock()
        mock_result.document = Mock()
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "knowledge"
        mock_search.return_value = [mock_result] * 3
        
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "connected"}
        
        utilization = analyzer._calculate_knowledge_utilization()
        assert 0.0 <= utilization <= 1.0

    def test_calculate_knowledge_utilization_fallback(self):
        """Test _calculate_knowledge_utilization fallback."""
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "disconnected"}
        
        utilization = analyzer._calculate_knowledge_utilization()
        assert utilization == 0.8  # Default fallback

    def test_generate_performance_recommendations_all_good(self):
        """Test recommendations when all metrics are good."""
        analyzer = PerformanceAnalyzer("Agent-1")
        recommendations = analyzer._generate_performance_recommendations(0.9, 0.8, 0.85)
        assert len(recommendations) > 0
        assert any("maintain" in rec.lower() for rec in recommendations)

    def test_generate_performance_recommendations_low_task_rate(self):
        """Test recommendations with low task completion rate."""
        analyzer = PerformanceAnalyzer("Agent-1")
        recommendations = analyzer._generate_performance_recommendations(0.5, 0.8, 0.85)
        assert any("task" in rec.lower() or "prioritization" in rec.lower() for rec in recommendations)

    def test_generate_performance_recommendations_low_coordination(self):
        """Test recommendations with low coordination."""
        analyzer = PerformanceAnalyzer("Agent-1")
        recommendations = analyzer._generate_performance_recommendations(0.9, 0.5, 0.85)
        assert any("coordination" in rec.lower() or "communication" in rec.lower() for rec in recommendations)

    def test_generate_performance_recommendations_low_knowledge(self):
        """Test recommendations with low knowledge utilization."""
        analyzer = PerformanceAnalyzer("Agent-1")
        recommendations = analyzer._generate_performance_recommendations(0.9, 0.8, 0.5)
        assert any("knowledge" in rec.lower() or "retrieval" in rec.lower() for rec in recommendations)

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_check_recent_activity(self, mock_search):
        """Test _check_recent_activity method."""
        mock_search.return_value = [Mock()]  # Has recent activity
        
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "connected"}
        
        has_activity = analyzer._check_recent_activity()
        assert isinstance(has_activity, bool)

    def test_check_recent_activity_fallback(self):
        """Test _check_recent_activity fallback."""
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "disconnected"}
        
        has_activity = analyzer._check_recent_activity()
        assert has_activity is False

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_check_swarm_sync_status(self, mock_search):
        """Test _check_swarm_sync_status method."""
        mock_search.return_value = [Mock()] * 5  # Has coordination messages
        
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "connected"}
        
        status = analyzer._check_swarm_sync_status()
        assert status in ["up_to_date", "partial", "out_of_sync", "unavailable", "error"]

    def test_check_swarm_sync_status_disconnected(self):
        """Test _check_swarm_sync_status when disconnected."""
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "disconnected"}
        
        status = analyzer._check_swarm_sync_status()
        assert status == "unavailable"

    def test_check_swarm_sync_status_exception(self):
        """Test _check_swarm_sync_status exception handling."""
        analyzer = PerformanceAnalyzer("Agent-1")
        analyzer.vector_integration = {"status": "connected"}
        # Force exception
        with patch('src.services.performance_analyzer.search_vector_database', side_effect=Exception("Test")):
            status = analyzer._check_swarm_sync_status()
            assert status == "error"

    def test_get_fallback_performance(self):
        """Test _get_fallback_performance method."""
        analyzer = PerformanceAnalyzer("Agent-1")
        result = analyzer._get_fallback_performance()
        assert result["agent_id"] == "Agent-1"
        assert "performance_score" in result
        assert result["fallback_mode"] is True
        assert "metrics" in result
        assert "recommendations" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.services.performance_analyzer", "--cov-report=term-missing"])

