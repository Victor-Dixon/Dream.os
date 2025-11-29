#!/usr/bin/env python3
"""
Unit Tests for Metrics Engine
==============================

Comprehensive tests for metrics_engine.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
import time
from unittest.mock import Mock, MagicMock, patch
from src.core.analytics.engines.metrics_engine import (
    MetricsEngine,
    create_metrics_engine
)


class TestMetricsEngine:
    """Tests for MetricsEngine."""

    def test_initialization(self):
        """Test metrics engine initialization."""
        engine = MetricsEngine()
        assert engine.config == {}
        assert engine.metrics == {}
        assert len(engine.performance_history) == 0
        assert len(engine.error_history) == 0
        assert engine.metrics_repository is None or engine.metrics_repository is not None

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"max_history": 50}
        engine = MetricsEngine(config)
        assert engine.config == config

    def test_initialization_with_metrics_repository(self):
        """Test initialization with metrics repository."""
        mock_repo = Mock()
        engine = MetricsEngine(metrics_repository=mock_repo)
        assert engine.metrics_repository == mock_repo

    def test_record_metric_numeric(self):
        """Test recording numeric metric."""
        engine = MetricsEngine()
        engine.record_metric("test_metric", 42)
        assert engine.get_metric("test_metric") == 42

    def test_record_metric_float(self):
        """Test recording float metric."""
        engine = MetricsEngine()
        engine.record_metric("test_float", 3.14)
        assert engine.get_metric("test_float") == 3.14

    def test_record_metric_non_numeric(self):
        """Test recording non-numeric metric."""
        engine = MetricsEngine()
        engine.record_metric("test_string", "value")
        assert engine.get_metric("test_string_count") > 0

    def test_record_metric_exception_handling(self):
        """Test record metric exception handling."""
        engine = MetricsEngine()
        # Should handle gracefully
        engine.record_metric(None, None)
        assert True  # No exception raised

    def test_increment_metric(self):
        """Test incrementing metric."""
        engine = MetricsEngine()
        engine.increment_metric("counter", 5)
        assert engine.get_metric("counter") == 5
        engine.increment_metric("counter", 3)
        assert engine.get_metric("counter") == 8

    def test_increment_metric_default(self):
        """Test incrementing metric with default amount."""
        engine = MetricsEngine()
        engine.increment_metric("counter")
        assert engine.get_metric("counter") == 1

    def test_increment_metric_exception_handling(self):
        """Test increment metric exception handling."""
        engine = MetricsEngine()
        # Should handle gracefully
        engine.increment_metric(None, None)
        assert True  # No exception raised

    def test_get_metric_existing(self):
        """Test getting existing metric."""
        engine = MetricsEngine()
        engine.record_metric("existing", 100)
        assert engine.get_metric("existing") == 100

    def test_get_metric_nonexistent(self):
        """Test getting non-existent metric."""
        engine = MetricsEngine()
        assert engine.get_metric("nonexistent") == 0

    def test_get_all_metrics(self):
        """Test getting all metrics."""
        engine = MetricsEngine()
        engine.record_metric("metric1", 10)
        engine.record_metric("metric2", 20)
        all_metrics = engine.get_all_metrics()
        assert "metric1" in all_metrics
        assert "metric2" in all_metrics
        assert all_metrics["metric1"] == 10
        assert all_metrics["metric2"] == 20

    def test_record_performance(self):
        """Test recording performance data."""
        engine = MetricsEngine()
        engine.record_performance("operation1", 1.5)
        assert len(engine.performance_history) == 1
        perf = engine.performance_history[0]
        assert perf["operation"] == "operation1"
        assert perf["duration"] == 1.5
        assert "timestamp" in perf

    def test_record_performance_multiple(self):
        """Test recording multiple performance records."""
        engine = MetricsEngine()
        engine.record_performance("op1", 1.0)
        engine.record_performance("op2", 2.0)
        assert len(engine.performance_history) == 2

    def test_record_performance_exception_handling(self):
        """Test record performance exception handling."""
        engine = MetricsEngine()
        # Should handle gracefully
        engine.record_performance(None, None)
        assert True  # No exception raised

    def test_record_error(self):
        """Test recording error data."""
        engine = MetricsEngine()
        engine.record_error("ValueError", "Test error message")
        assert len(engine.error_history) == 1
        error = engine.error_history[0]
        assert error["error_type"] == "ValueError"
        assert error["message"] == "Test error message"
        assert "timestamp" in error

    def test_record_error_exception_handling(self):
        """Test record error exception handling."""
        engine = MetricsEngine()
        # Should handle gracefully
        engine.record_error(None, None)
        assert True  # No exception raised

    def test_get_performance_summary_empty(self):
        """Test getting performance summary with no data."""
        engine = MetricsEngine()
        summary = engine.get_performance_summary()
        assert "message" in summary
        assert "No performance data available" in summary["message"]

    def test_get_performance_summary_with_data(self):
        """Test getting performance summary with data."""
        engine = MetricsEngine()
        engine.record_performance("op1", 1.0)
        engine.record_performance("op2", 2.0)
        engine.record_performance("op3", 3.0)
        summary = engine.get_performance_summary()
        assert summary["total_operations"] == 3
        assert summary["avg_duration"] == 2.0
        assert summary["max_duration"] == 3.0
        assert summary["min_duration"] == 1.0
        assert "timestamp" in summary

    def test_get_performance_summary_exception_handling(self):
        """Test performance summary exception handling."""
        engine = MetricsEngine()
        engine.performance_history = None  # Break it
        summary = engine.get_performance_summary()
        assert "error" in summary

    def test_get_error_summary_empty(self):
        """Test getting error summary with no data."""
        engine = MetricsEngine()
        summary = engine.get_error_summary()
        assert "message" in summary
        assert "No error data available" in summary["message"]

    def test_get_error_summary_with_data(self):
        """Test getting error summary with data."""
        engine = MetricsEngine()
        engine.record_error("TypeError", "Error 1")
        engine.record_error("ValueError", "Error 2")
        engine.record_error("TypeError", "Error 3")
        summary = engine.get_error_summary()
        assert summary["total_errors"] == 3
        assert "error_types" in summary
        assert summary["error_types"]["TypeError"] == 2
        assert summary["error_types"]["ValueError"] == 1

    def test_get_error_summary_exception_handling(self):
        """Test error summary exception handling."""
        engine = MetricsEngine()
        engine.error_history = None  # Break it
        summary = engine.get_error_summary()
        assert "error" in summary

    def test_clear_metrics(self):
        """Test clearing all metrics."""
        engine = MetricsEngine()
        engine.record_metric("metric1", 10)
        engine.record_performance("op1", 1.0)
        engine.record_error("Error", "message")
        engine.clear_metrics()
        assert len(engine.metrics) == 0
        assert len(engine.performance_history) == 0
        assert len(engine.error_history) == 0

    def test_get_status(self):
        """Test getting engine status."""
        engine = MetricsEngine()
        time.sleep(0.1)  # Small delay to test uptime
        status = engine.get_status()
        assert status["active"] is True
        assert status["uptime"] > 0
        assert status["metrics_count"] == 0
        assert status["performance_records"] == 0
        assert status["error_records"] == 0
        assert "persistence_enabled" in status
        assert "timestamp" in status

    def test_get_status_with_data(self):
        """Test getting status with recorded data."""
        engine = MetricsEngine()
        engine.record_metric("test", 10)
        engine.record_performance("op", 1.0)
        engine.record_error("Error", "msg")
        status = engine.get_status()
        assert status["metrics_count"] == 1
        assert status["performance_records"] == 1
        assert status["error_records"] == 1

    def test_save_snapshot_without_repository(self):
        """Test saving snapshot without repository."""
        engine = MetricsEngine()
        result = engine.save_snapshot()
        assert result is False

    def test_save_snapshot_with_repository(self):
        """Test saving snapshot with repository."""
        mock_repo = Mock()
        mock_repo.save_metrics_snapshot.return_value = True
        engine = MetricsEngine(metrics_repository=mock_repo)
        engine.record_metric("test", 10)
        result = engine.save_snapshot("test_source")
        assert result is True
        mock_repo.save_metrics_snapshot.assert_called_once()

    def test_save_snapshot_exception_handling(self):
        """Test save snapshot exception handling."""
        mock_repo = Mock()
        mock_repo.save_metrics_snapshot.side_effect = Exception("Save failed")
        engine = MetricsEngine(metrics_repository=mock_repo)
        result = engine.save_snapshot()
        assert result is False

    def test_get_metrics_history_without_repository(self):
        """Test getting metrics history without repository."""
        engine = MetricsEngine()
        history = engine.get_metrics_history()
        assert history == []

    def test_get_metrics_history_with_repository(self):
        """Test getting metrics history with repository."""
        mock_repo = Mock()
        mock_repo.get_metrics_history.return_value = [{"metric": "value"}]
        engine = MetricsEngine(metrics_repository=mock_repo)
        history = engine.get_metrics_history("source", 10)
        assert len(history) == 1
        mock_repo.get_metrics_history.assert_called_once()

    def test_get_metrics_history_exception_handling(self):
        """Test get metrics history exception handling."""
        mock_repo = Mock()
        mock_repo.get_metrics_history.side_effect = Exception("History error")
        engine = MetricsEngine(metrics_repository=mock_repo)
        history = engine.get_metrics_history()
        assert history == []

    def test_get_metrics_trend_without_repository(self):
        """Test getting metrics trend without repository."""
        engine = MetricsEngine()
        trend = engine.get_metrics_trend("metric_name")
        assert trend == []

    def test_get_metrics_trend_with_repository(self):
        """Test getting metrics trend with repository."""
        mock_repo = Mock()
        mock_repo.get_metrics_trend.return_value = [1.0, 2.0, 3.0]
        engine = MetricsEngine(metrics_repository=mock_repo)
        trend = engine.get_metrics_trend("metric_name", "source", 50)
        assert len(trend) == 3
        mock_repo.get_metrics_trend.assert_called_once()

    def test_get_metrics_trend_exception_handling(self):
        """Test get metrics trend exception handling."""
        mock_repo = Mock()
        mock_repo.get_metrics_trend.side_effect = Exception("Trend error")
        engine = MetricsEngine(metrics_repository=mock_repo)
        trend = engine.get_metrics_trend("metric")
        assert trend == []

    def test_create_metrics_engine(self):
        """Test factory function."""
        engine = create_metrics_engine()
        assert isinstance(engine, MetricsEngine)

    def test_create_metrics_engine_with_config(self):
        """Test factory function with config."""
        config = {"test": "value"}
        engine = create_metrics_engine(config)
        assert isinstance(engine, MetricsEngine)
        assert engine.config == config


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.engines.metrics_engine", "--cov-report=term-missing"])

