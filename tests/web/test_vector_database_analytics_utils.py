#!/usr/bin/env python3
"""
Tests for Vector Database Analytics Utils
=========================================

Comprehensive test suite for analytics utility functions.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import MagicMock, patch

from src.web.vector_database.analytics_utils import AnalyticsUtils
from src.web.vector_database.models import AnalyticsData


class TestAnalyticsUtils:
    """Test suite for AnalyticsUtils."""

    @pytest.fixture
    def analytics(self):
        """Create analytics utils instance."""
        return AnalyticsUtils()

    def test_analytics_initialization(self, analytics):
        """Test analytics utils initialization."""
        assert analytics is not None

    def test_simulate_get_analytics_returns_analytics_data(self, analytics):
        """Test simulate_get_analytics returns AnalyticsData."""
        result = analytics.simulate_get_analytics("7d")
        
        assert isinstance(result, AnalyticsData)
        assert result.total_documents == 2431
        assert result.search_queries == 1247
        assert result.average_response_time == 245.0
        assert result.success_rate == 98.5

    def test_simulate_get_analytics_top_searches(self, analytics):
        """Test analytics includes top searches."""
        result = analytics.simulate_get_analytics("7d")
        
        assert len(result.top_searches) == 5
        assert result.top_searches[0]["query"] == "web development"
        assert result.top_searches[0]["count"] == 45

    def test_simulate_get_analytics_document_distribution(self, analytics):
        """Test analytics includes document distribution."""
        result = analytics.simulate_get_analytics("7d")
        
        assert "agent_system" in result.document_distribution
        assert "project_docs" in result.document_distribution
        assert "development" in result.document_distribution
        assert "strategic_oversight" in result.document_distribution
        assert result.document_distribution["development"] == 1493

    def test_simulate_get_analytics_search_trends(self, analytics):
        """Test analytics includes search trends."""
        result = analytics.simulate_get_analytics("7d")
        
        assert len(result.search_trends) == 5
        assert "date" in result.search_trends[0]
        assert "queries" in result.search_trends[0]
        assert result.search_trends[0]["date"] == "2025-01-27"

    def test_simulate_get_analytics_different_time_ranges(self, analytics):
        """Test analytics works with different time ranges."""
        for time_range in ["1d", "7d", "30d", "all"]:
            result = analytics.simulate_get_analytics(time_range)
            
            assert isinstance(result, AnalyticsData)
            assert result.total_documents > 0

    def test_simulate_get_analytics_data_structure(self, analytics):
        """Test analytics data structure is complete."""
        result = analytics.simulate_get_analytics("7d")
        
        # Verify all required fields
        assert hasattr(result, 'total_documents')
        assert hasattr(result, 'search_queries')
        assert hasattr(result, 'average_response_time')
        assert hasattr(result, 'success_rate')
        assert hasattr(result, 'top_searches')
        assert hasattr(result, 'document_distribution')
        assert hasattr(result, 'search_trends')

    def test_simulate_get_analytics_consistency(self, analytics):
        """Test analytics returns consistent data."""
        result1 = analytics.simulate_get_analytics("7d")
        result2 = analytics.simulate_get_analytics("7d")
        
        # Should return same data (simulated)
        assert result1.total_documents == result2.total_documents
        assert result1.search_queries == result2.search_queries

    def test_simulate_get_analytics_types(self, analytics):
        """Test analytics data types are correct."""
        result = analytics.simulate_get_analytics("7d")
        
        assert isinstance(result.total_documents, int)
        assert isinstance(result.search_queries, int)
        assert isinstance(result.average_response_time, float)
        assert isinstance(result.success_rate, float)
        assert isinstance(result.top_searches, list)
        assert isinstance(result.document_distribution, dict)
        assert isinstance(result.search_trends, list)

