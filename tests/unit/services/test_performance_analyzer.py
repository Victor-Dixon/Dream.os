#!/usr/bin/env python3
"""
Unit Tests for Performance Analyzer
====================================

Tests for performance analysis service.
"""

import pytest
from unittest.mock import Mock, patch

try:
    from src.services.performance_analyzer import PerformanceAnalyzer
    PERFORMANCE_ANALYZER_AVAILABLE = True
except ImportError:
    PERFORMANCE_ANALYZER_AVAILABLE = False


@pytest.mark.skipif(not PERFORMANCE_ANALYZER_AVAILABLE, reason="Performance analyzer not available")
class TestPerformanceAnalyzer:
    """Unit tests for Performance Analyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = PerformanceAnalyzer("Agent-1")
        
        assert analyzer is not None
        assert analyzer.agent_id == "Agent-1"

    def test_analyze_agent_performance(self):
        """Test agent performance analysis."""
        analyzer = PerformanceAnalyzer("Agent-1")
        
        # Test that analyzer can be initialized and used
        assert analyzer.agent_id == "Agent-1"
        assert analyzer.logger is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

