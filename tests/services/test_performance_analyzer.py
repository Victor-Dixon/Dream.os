#!/usr/bin/env python3
"""
Tests for Performance Analyzer
================================

Tests for performance analysis operations.

Author: Agent-7
Date: 2025-11-27
"""

import pytest
from unittest.mock import MagicMock, patch

from src.services.performance_analyzer import PerformanceAnalyzer


class TestPerformanceAnalyzer:
    """Test suite for PerformanceAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create PerformanceAnalyzer instance."""
        with patch('src.services.performance_analyzer.get_vector_database_service'):
            return PerformanceAnalyzer('Agent-7')

    def test_initialization(self, analyzer):
        """Test PerformanceAnalyzer initialization."""
        assert analyzer.agent_id == "Agent-7"
        assert analyzer.logger is not None
        assert analyzer.config is not None

    def test_load_config(self, analyzer):
        """Test configuration loading."""
        config = analyzer._load_config(None)
        assert "analysis_period_days" in config
        assert "performance_thresholds" in config
        assert "metrics_weights" in config

    def test_analyze_agent_performance_connected(self, analyzer):
        """Test performance analysis with connected vector DB."""
        analyzer.vector_integration = {"status": "connected", "service": MagicMock()}
        
        result = analyzer.analyze_agent_performance()
        assert result is not None
        assert isinstance(result, dict)

    def test_analyze_agent_performance_disconnected(self, analyzer):
        """Test performance analysis with disconnected vector DB."""
        analyzer.vector_integration = {"status": "disconnected", "error": "Test error"}
        
        result = analyzer.analyze_agent_performance()
        assert result is not None
        assert isinstance(result, dict)

    def test_get_fallback_performance(self, analyzer):
        """Test fallback performance data."""
        result = analyzer._get_fallback_performance()
        assert result is not None
        assert isinstance(result, dict)
        assert result["agent_id"] == "Agent-7"
        assert "performance_score" in result

    def test_get_integration_health_connected(self, analyzer):
        """Test integration health check with connected vector DB."""
        analyzer.vector_integration = {"status": "connected", "service": MagicMock()}
        health = analyzer.get_integration_health()
        assert health["health_status"] in ["healthy", "warning", "degraded"]
        assert "agent_id" in health

    def test_get_integration_health_disconnected(self, analyzer):
        """Test integration health check with disconnected vector DB."""
        analyzer.vector_integration = {"status": "disconnected", "error": "Test"}
        health = analyzer.get_integration_health()
        assert health["health_status"] in ["degraded", "warning", "error"]

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_calculate_task_completion_rate(self, mock_search, analyzer):
        """Test task completion rate calculation."""
        mock_search.return_value = [MagicMock(), MagicMock()]  # 2 completed, 4 total
        rate = analyzer._calculate_task_completion_rate()
        assert 0.0 <= rate <= 1.0

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_calculate_coordination_effectiveness(self, mock_search, analyzer):
        """Test coordination effectiveness calculation."""
        mock_search.return_value = [MagicMock()] * 5
        effectiveness = analyzer._calculate_coordination_effectiveness()
        assert 0.0 <= effectiveness <= 1.0

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_calculate_knowledge_utilization(self, mock_search, analyzer):
        """Test knowledge utilization calculation."""
        mock_result = MagicMock()
        mock_result.document.document_type.value = "test"
        mock_search.return_value = [mock_result] * 3
        utilization = analyzer._calculate_knowledge_utilization()
        assert 0.0 <= utilization <= 1.0

    def test_generate_performance_recommendations_low_task_rate(self, analyzer):
        """Test recommendations for low task completion rate."""
        recommendations = analyzer._generate_performance_recommendations(0.5, 0.8, 0.8)
        assert any("task" in r.lower() for r in recommendations)

    def test_generate_performance_recommendations_low_coordination(self, analyzer):
        """Test recommendations for low coordination."""
        recommendations = analyzer._generate_performance_recommendations(0.8, 0.5, 0.8)
        assert any("coordination" in r.lower() for r in recommendations)

    def test_generate_performance_recommendations_all_good(self, analyzer):
        """Test recommendations when all metrics are good."""
        recommendations = analyzer._generate_performance_recommendations(0.9, 0.9, 0.9)
        assert any("maintain" in r.lower() for r in recommendations)

    @patch('src.services.performance_analyzer.search_vector_database')
    def test_check_recent_activity(self, mock_search, analyzer):
        """Test recent activity check."""
        mock_search.return_value = [MagicMock()]
        assert analyzer._check_recent_activity() is True
        mock_search.return_value = []
        assert analyzer._check_recent_activity() is False

    def test_check_swarm_sync_status_connected(self, analyzer):
        """Test swarm sync status check with connected DB."""
        analyzer.vector_integration = {"status": "connected"}
        with patch('src.services.performance_analyzer.search_vector_database') as mock_search:
            mock_search.return_value = [MagicMock()] * 10
            status = analyzer._check_swarm_sync_status()
            assert status in ["up_to_date", "partial", "out_of_sync", "error"]

