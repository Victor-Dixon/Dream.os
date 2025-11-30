"""
Tests for Vector Integration Analytics
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.core.vector_integration_analytics import (
    VectorIntegrationAnalytics,
    create_vector_integration_analytics
)


class TestVectorIntegrationAnalytics:
    """Test suite for VectorIntegrationAnalytics class."""

    def test_init(self):
        """Test VectorIntegrationAnalytics initialization."""
        analytics = VectorIntegrationAnalytics()
        
        assert analytics.analytics_data["integrations_tracked"] == 0
        assert analytics.analytics_data["performance_metrics"] == {}
        assert analytics.analytics_data["error_rates"] == {}
        assert "last_updated" in analytics.analytics_data

    def test_track_integration(self):
        """Test track_integration records integration."""
        analytics = VectorIntegrationAnalytics()
        metrics = {"latency": 0.5, "throughput": 100}
        
        result = analytics.track_integration("integration_1", metrics)
        
        assert result is True
        assert analytics.analytics_data["integrations_tracked"] == 1
        assert analytics.analytics_data["performance_metrics"]["integration_1"] == metrics

    def test_track_integration_multiple(self):
        """Test track_integration tracks multiple integrations."""
        analytics = VectorIntegrationAnalytics()
        
        analytics.track_integration("integration_1", {"metric": 1})
        analytics.track_integration("integration_2", {"metric": 2})
        
        assert analytics.analytics_data["integrations_tracked"] == 2
        assert len(analytics.analytics_data["performance_metrics"]) == 2

    def test_get_integration_stats_specific(self):
        """Test get_integration_stats for specific integration."""
        analytics = VectorIntegrationAnalytics()
        metrics = {"latency": 0.5, "throughput": 100}
        analytics.track_integration("integration_1", metrics)
        
        result = analytics.get_integration_stats("integration_1")
        
        assert result == metrics

    def test_get_integration_stats_nonexistent(self):
        """Test get_integration_stats for non-existent integration."""
        analytics = VectorIntegrationAnalytics()
        
        result = analytics.get_integration_stats("nonexistent")
        
        assert result == {}

    def test_get_integration_stats_all(self):
        """Test get_integration_stats returns all stats when no ID provided."""
        analytics = VectorIntegrationAnalytics()
        analytics.track_integration("integration_1", {"metric": 1})
        analytics.track_integration("integration_2", {"metric": 2})
        
        result = analytics.get_integration_stats()
        
        assert result["total_integrations"] == 2
        assert "performance_metrics" in result
        assert "error_rates" in result
        assert "last_updated" in result

    def test_analyze_performance_trends(self):
        """Test analyze_performance_trends returns trends."""
        analytics = VectorIntegrationAnalytics()
        
        result = analytics.analyze_performance_trends()
        
        assert "average_performance" in result
        assert "trend_direction" in result
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)

    def test_generate_report(self):
        """Test generate_report generates report string."""
        analytics = VectorIntegrationAnalytics()
        analytics.track_integration("integration_1", {"metric": 1})
        
        report = analytics.generate_report()
        
        assert isinstance(report, str)
        assert "Vector Integration Analytics Report" in report
        assert "Total Integrations Tracked" in report
        assert "integration_1" in report or "1" in report

    def test_generate_report_includes_stats(self):
        """Test generate_report includes integration stats."""
        analytics = VectorIntegrationAnalytics()
        analytics.track_integration("test_integration", {"latency": 0.5})
        
        report = analytics.generate_report()
        
        assert "test_integration" in report or "1" in report


class TestFactoryFunction:
    """Test suite for create_vector_integration_analytics function."""

    def test_create_vector_integration_analytics(self):
        """Test factory function creates instance."""
        analytics = create_vector_integration_analytics()
        
        assert isinstance(analytics, VectorIntegrationAnalytics)
        assert analytics.analytics_data["integrations_tracked"] == 0

