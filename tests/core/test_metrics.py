#!/usr/bin/env python3
"""
Unit Tests for Core Metrics Module
===================================
"""

import pytest
from datetime import datetime
from src.core.metrics import (
    Metric,
    MetricsCollector,
    CounterMetrics,
    OptimizationRunMetrics,
    gather_run_metrics,
)


class TestMetric:
    """Tests for Metric dataclass."""

    def test_metric_creation(self):
        """Test creating a metric."""
        metric = Metric(name="test_metric", value=42.5)
        assert metric.name == "test_metric"
        assert metric.value == 42.5


class TestMetricsCollector:
    """Tests for MetricsCollector."""

    def test_initialization(self):
        """Test collector initialization."""
        collector = MetricsCollector()
        assert collector._metrics == {}
        assert collector.total_operations == 0

    def test_record_metric(self):
        """Test recording a metric."""
        collector = MetricsCollector()
        collector.record("test_metric", 10.5)
        assert collector.get("test_metric") == 10.5

    def test_get_nonexistent_metric(self):
        """Test getting nonexistent metric."""
        collector = MetricsCollector()
        assert collector.get("nonexistent") is None

    def test_get_all_metrics(self):
        """Test getting all metrics."""
        collector = MetricsCollector()
        collector.record("metric1", 10.0)
        collector.record("metric2", 20.0)
        all_metrics = collector.all()
        assert len(all_metrics) == 2
        assert all_metrics["metric1"] == 10.0
        assert all_metrics["metric2"] == 20.0

    def test_record_success(self):
        """Test recording a successful operation."""
        collector = MetricsCollector()
        collector.record_success()
        assert collector.total_operations == 1
        assert collector.successful_operations == 1
        assert collector.failed_operations == 0

    def test_record_failure(self):
        """Test recording a failed operation."""
        collector = MetricsCollector()
        collector.record_failure()
        assert collector.total_operations == 1
        assert collector.successful_operations == 0
        assert collector.failed_operations == 1

    def test_mixed_success_failure(self):
        """Test recording mixed success and failure."""
        collector = MetricsCollector()
        collector.record_success()
        collector.record_success()
        collector.record_failure()
        assert collector.total_operations == 3
        assert collector.successful_operations == 2
        assert collector.failed_operations == 1

    def test_record_overwrites_existing(self):
        """Test that recording overwrites existing metric."""
        collector = MetricsCollector()
        collector.record("test", 10.0)
        collector.record("test", 20.0)
        assert collector.get("test") == 20.0


class TestCounterMetrics:
    """Tests for CounterMetrics."""

    def test_initialization(self):
        """Test counter initialization."""
        counter = CounterMetrics()
        assert counter.counters == {}

    def test_increment_counter(self):
        """Test incrementing a counter."""
        counter = CounterMetrics()
        counter.increment("test_counter")
        assert counter.get("test_counter") == 1

    def test_increment_by_amount(self):
        """Test incrementing by specific amount."""
        counter = CounterMetrics()
        counter.increment("test_counter", 5)
        assert counter.get("test_counter") == 5

    def test_get_nonexistent_counter(self):
        """Test getting nonexistent counter returns 0."""
        counter = CounterMetrics()
        assert counter.get("nonexistent") == 0

    def test_multiple_increments(self):
        """Test multiple increments accumulate."""
        counter = CounterMetrics()
        counter.increment("test", 3)
        counter.increment("test", 2)
        assert counter.get("test") == 5

    def test_multiple_counters(self):
        """Test multiple independent counters."""
        counter = CounterMetrics()
        counter.increment("counter1")
        counter.increment("counter2", 2)
        assert counter.get("counter1") == 1
        assert counter.get("counter2") == 2


class TestOptimizationRunMetrics:
    """Tests for OptimizationRunMetrics dataclass."""

    def test_metric_creation(self):
        """Test creating optimization run metrics."""
        metrics = OptimizationRunMetrics(
            timestamp="2025-01-01T00:00:00",
            tasks_processed=100,
            errors=5,
            duration=10.5,
        )
        assert metrics.tasks_processed == 100
        assert metrics.errors == 5
        assert metrics.duration == 10.5

    def test_gather_run_metrics(self):
        """Test gather_run_metrics function."""
        metrics = gather_run_metrics(
            tasks_processed=50,
            errors=2,
            duration=5.0,
        )
        assert metrics.tasks_processed == 50
        assert metrics.errors == 2
        assert metrics.duration == 5.0
        assert isinstance(metrics.timestamp, str)

    def test_gather_run_metrics_with_datetime(self):
        """Test gather_run_metrics with custom datetime."""
        custom_time = datetime(2025, 1, 1, 12, 0, 0)
        metrics = gather_run_metrics(
            tasks_processed=10,
            errors=0,
            duration=2.0,
            _now=custom_time,
        )
        assert "2025-01-01" in metrics.timestamp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

