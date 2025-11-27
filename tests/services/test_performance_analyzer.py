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

