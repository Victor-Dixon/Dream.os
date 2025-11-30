#!/usr/bin/env python3
"""
Unit Tests for Coordination Analytics Models
============================================
"""

import pytest
from datetime import datetime
from src.core.analytics.models.coordination_analytics_models import (
    AnalyticsMetric,
    OptimizationRecommendation,
    CoordinationAnalyticsData,
    AnalyticsReport,
    AnalyticsConfig,
)


class TestAnalyticsMetric:
    """Tests for AnalyticsMetric enum."""

    def test_enum_values(self):
        """Test enum has correct values."""
        assert AnalyticsMetric.EFFICIENCY.value == "efficiency"
        assert AnalyticsMetric.THROUGHPUT.value == "throughput"
        assert AnalyticsMetric.SUCCESS_RATE.value == "success_rate"


class TestOptimizationRecommendation:
    """Tests for OptimizationRecommendation enum."""

    def test_enum_values(self):
        """Test enum has correct values."""
        assert OptimizationRecommendation.ROUTE_OPTIMIZATION.value == "route_optimization"
        assert OptimizationRecommendation.BATCH_PROCESSING.value == "batch_processing"


class TestCoordinationAnalyticsData:
    """Tests for CoordinationAnalyticsData dataclass."""

    def test_initialization(self):
        """Test data initialization."""
        data = CoordinationAnalyticsData(
            timestamp=datetime.now(),
            efficiency_score=0.85,
            throughput=100,
            success_rate=0.95,
            average_response_time=1.5,
            coordination_quality=0.9,
            swarm_health=0.88,
            active_agents=8,
            total_tasks=50,
            recommendations=["test"],
        )
        assert data.efficiency_score == 0.85
        assert data.active_agents == 8

    def test_to_dict(self):
        """Test converting to dictionary."""
        data = CoordinationAnalyticsData(
            timestamp=datetime.now(),
            efficiency_score=0.85,
            throughput=100,
            success_rate=0.95,
            average_response_time=1.5,
            coordination_quality=0.9,
            swarm_health=0.88,
            active_agents=8,
            total_tasks=50,
            recommendations=[],
        )
        result = data.to_dict()
        assert isinstance(result, dict)
        assert "efficiency_score" in result

    def test_get_summary(self):
        """Test getting summary."""
        data = CoordinationAnalyticsData(
            timestamp=datetime.now(),
            efficiency_score=0.85,
            throughput=100,
            success_rate=0.95,
            average_response_time=1.5,
            coordination_quality=0.9,
            swarm_health=0.88,
            active_agents=8,
            total_tasks=50,
            recommendations=["rec1", "rec2"],
        )
        summary = data.get_summary()
        assert "efficiency_score" in summary
        assert summary["recommendations_count"] == 2


class TestAnalyticsReport:
    """Tests for AnalyticsReport dataclass."""

    def test_initialization(self):
        """Test report initialization."""
        data = CoordinationAnalyticsData(
            timestamp=datetime.now(),
            efficiency_score=0.85,
            throughput=100,
            success_rate=0.95,
            average_response_time=1.5,
            coordination_quality=0.9,
            swarm_health=0.88,
            active_agents=8,
            total_tasks=50,
            recommendations=[],
        )
        report = AnalyticsReport(
            report_id="test-123",
            generated_at=datetime.now(),
            data=data,
            trends={"test": "trend"},
            recommendations=["rec1"],
            summary={"key": "value"},
        )
        assert report.report_id == "test-123"

    def test_to_dict(self):
        """Test converting to dictionary."""
        data = CoordinationAnalyticsData(
            timestamp=datetime.now(),
            efficiency_score=0.85,
            throughput=100,
            success_rate=0.95,
            average_response_time=1.5,
            coordination_quality=0.9,
            swarm_health=0.88,
            active_agents=8,
            total_tasks=50,
            recommendations=[],
        )
        report = AnalyticsReport(
            report_id="test-123",
            generated_at=datetime.now(),
            data=data,
            trends={},
            recommendations=[],
            summary={},
        )
        result = report.to_dict()
        assert "report_id" in result
        assert "data" in result


class TestAnalyticsConfig:
    """Tests for AnalyticsConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AnalyticsConfig()
        assert config.enable_real_time_monitoring is True
        assert config.analysis_interval_seconds == 60

    def test_custom_values(self):
        """Test custom configuration values."""
        config = AnalyticsConfig(
            enable_real_time_monitoring=False,
            analysis_interval_seconds=30,
        )
        assert config.enable_real_time_monitoring is False
        assert config.analysis_interval_seconds == 30

    def test_validate_success(self):
        """Test successful validation."""
        config = AnalyticsConfig()
        config.validate()

    def test_validate_invalid_interval(self):
        """Test validation with invalid interval."""
        config = AnalyticsConfig(analysis_interval_seconds=0)
        with pytest.raises(ValueError):
            config.validate()

    def test_validate_invalid_retention(self):
        """Test validation with invalid retention."""
        config = AnalyticsConfig(history_retention_hours=0)
        with pytest.raises(ValueError):
            config.validate()

    def test_validate_invalid_efficiency(self):
        """Test validation with invalid efficiency."""
        config = AnalyticsConfig(target_efficiency=1.5)
        with pytest.raises(ValueError):
            config.validate()

    def test_validate_invalid_cache_ttl(self):
        """Test validation with invalid cache TTL."""
        config = AnalyticsConfig(cache_ttl_seconds=0)
        with pytest.raises(ValueError):
            config.validate()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

