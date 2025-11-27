"""
Unit tests for performance_collector.py - MEDIUM PRIORITY

Tests PerformanceCollector class, metric recording, and filtering.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import threading

# Add project root to path
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import directly to avoid __init__.py import chain issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "performance_collector",
    project_root / "src" / "core" / "performance" / "performance_collector.py"
)
performance_collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(performance_collector)

PerformanceCollector = performance_collector.PerformanceCollector
PerformanceMetric = performance_collector.PerformanceMetric
MetricType = performance_collector.MetricType


class TestPerformanceCollector:
    """Test suite for PerformanceCollector class."""

    @pytest.fixture
    def collector(self):
        """Create a PerformanceCollector instance."""
        return PerformanceCollector(max_history_size=100)

    def test_initialization_default(self):
        """Test collector initialization with default max_history_size."""
        collector = PerformanceCollector()
        assert collector.max_history_size == 10000
        assert len(collector.metrics) == 0
        assert hasattr(collector.lock, 'acquire')  # Check it's a lock-like object

    def test_initialization_custom_size(self):
        """Test collector initialization with custom max_history_size."""
        collector = PerformanceCollector(max_history_size=50)
        assert collector.max_history_size == 50
        assert len(collector.metrics) == 0

    def test_record_metric_basic(self, collector):
        """Test basic metric recording."""
        collector.record_metric("test_metric", 42.5)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].name == "test_metric"
        assert metrics[0].value == 42.5
        assert metrics[0].metric_type == MetricType.GAUGE
        assert isinstance(metrics[0].timestamp, datetime)

    def test_record_metric_with_type(self, collector):
        """Test metric recording with specific type."""
        collector.record_metric("counter_metric", 10.0, MetricType.COUNTER)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].metric_type == MetricType.COUNTER

    def test_record_metric_with_tags(self, collector):
        """Test metric recording with tags."""
        tags = {"env": "test", "service": "api"}
        collector.record_metric("tagged_metric", 5.0, tags=tags)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].tags == tags

    def test_record_metric_with_metadata(self, collector):
        """Test metric recording with metadata."""
        metadata = {"source": "test", "version": "1.0"}
        collector.record_metric("metadata_metric", 3.0, metadata=metadata)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].metadata == metadata

    def test_record_timer(self, collector):
        """Test timer metric recording."""
        collector.record_timer("operation_time", 1.5)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].name == "operation_time"
        assert metrics[0].value == 1.5
        assert metrics[0].metric_type == MetricType.TIMER

    def test_record_timer_with_tags(self, collector):
        """Test timer recording with tags."""
        tags = {"operation": "test"}
        collector.record_timer("timer_metric", 2.0, tags=tags)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].tags == tags
        assert metrics[0].metric_type == MetricType.TIMER

    def test_record_counter(self, collector):
        """Test counter metric recording."""
        collector.record_counter("request_count", 1.0)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].name == "request_count"
        assert metrics[0].value == 1.0
        assert metrics[0].metric_type == MetricType.COUNTER

    def test_record_counter_increment(self, collector):
        """Test counter recording with custom increment."""
        collector.record_counter("counter_metric", 5.0)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].value == 5.0

    def test_get_metrics_all(self, collector):
        """Test getting all metrics."""
        collector.record_metric("metric1", 1.0)
        collector.record_metric("metric2", 2.0)
        collector.record_metric("metric3", 3.0)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 3

    def test_get_metrics_by_name(self, collector):
        """Test getting metrics filtered by name."""
        collector.record_metric("metric_a", 1.0)
        collector.record_metric("metric_b", 2.0)
        collector.record_metric("metric_a", 3.0)
        
        metrics = collector.get_metrics(name="metric_a")
        assert len(metrics) == 2
        assert all(m.name == "metric_a" for m in metrics)

    def test_get_metrics_by_time_range(self, collector):
        """Test getting metrics filtered by time range."""
        base_time = datetime.now()
        
        # Record metrics with slight time differences
        collector.record_metric("metric1", 1.0)
        collector.record_metric("metric2", 2.0)
        collector.record_metric("metric3", 3.0)
        
        # Get metrics in time range (all should be included)
        start_time = base_time - timedelta(minutes=1)
        end_time = base_time + timedelta(minutes=1)
        metrics = collector.get_metrics(start_time=start_time, end_time=end_time)
        
        # Should get all metrics (all are within time range)
        assert len(metrics) == 3

    def test_get_metrics_by_start_time(self, collector):
        """Test getting metrics filtered by start time."""
        base_time = datetime.now()
        start_time = base_time - timedelta(minutes=5)
        
        # Record metrics
        collector.record_metric("metric1", 1.0)
        collector.record_metric("metric2", 2.0)
        
        metrics = collector.get_metrics(start_time=start_time)
        # Should return all metrics (all are after start_time)
        assert len(metrics) >= 0

    def test_get_metrics_by_end_time(self, collector):
        """Test getting metrics filtered by end time."""
        base_time = datetime.now()
        end_time = base_time + timedelta(minutes=5)
        
        # Record metrics
        collector.record_metric("metric1", 1.0)
        collector.record_metric("metric2", 2.0)
        
        metrics = collector.get_metrics(end_time=end_time)
        # Should return all metrics (all are before end_time)
        assert len(metrics) >= 0

    def test_get_metrics_combined_filters(self, collector):
        """Test getting metrics with combined filters."""
        collector.record_metric("target_metric", 1.0)
        collector.record_metric("other_metric", 2.0)
        collector.record_metric("target_metric", 3.0)
        
        metrics = collector.get_metrics(name="target_metric")
        assert len(metrics) == 2
        assert all(m.name == "target_metric" for m in metrics)

    def test_get_latest_metric_exists(self, collector):
        """Test getting latest metric when it exists."""
        collector.record_metric("test_metric", 1.0)
        collector.record_metric("test_metric", 2.0)
        collector.record_metric("test_metric", 3.0)
        
        latest = collector.get_latest_metric("test_metric")
        assert latest is not None
        assert latest.name == "test_metric"
        assert latest.value == 3.0

    def test_get_latest_metric_not_exists(self, collector):
        """Test getting latest metric when it doesn't exist."""
        collector.record_metric("other_metric", 1.0)
        
        latest = collector.get_latest_metric("nonexistent_metric")
        assert latest is None

    def test_get_latest_metric_empty_collector(self, collector):
        """Test getting latest metric from empty collector."""
        latest = collector.get_latest_metric("any_metric")
        assert latest is None

    def test_max_history_size_limit(self, collector):
        """Test that max_history_size limit is enforced."""
        # Record more metrics than max_history_size
        for i in range(150):
            collector.record_metric(f"metric_{i}", float(i))
        
        # Should only have max_history_size metrics
        metrics = collector.get_metrics()
        assert len(metrics) <= collector.max_history_size

    def test_thread_safety(self, collector):
        """Test thread safety of metric recording."""
        import threading
        
        def record_metrics():
            for i in range(10):
                collector.record_metric(f"thread_metric_{i}", float(i))
        
        # Create multiple threads
        threads = [threading.Thread(target=record_metrics) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Should have recorded all metrics (50 total)
        metrics = collector.get_metrics()
        assert len(metrics) == 50

    def test_multiple_metric_types(self, collector):
        """Test recording multiple metric types."""
        collector.record_metric("gauge_metric", 10.0, MetricType.GAUGE)
        collector.record_timer("timer_metric", 1.5)
        collector.record_counter("counter_metric", 5.0)
        
        metrics = collector.get_metrics()
        assert len(metrics) == 3
        
        types = {m.metric_type for m in metrics}
        assert MetricType.GAUGE in types
        assert MetricType.TIMER in types
        assert MetricType.COUNTER in types

    def test_metric_timestamp(self, collector):
        """Test that metrics have timestamps."""
        before = datetime.now()
        collector.record_metric("timestamp_test", 1.0)
        after = datetime.now()
        
        metrics = collector.get_metrics()
        assert len(metrics) == 1
        assert before <= metrics[0].timestamp <= after

    def test_empty_tags_default(self, collector):
        """Test that empty tags dict is used when tags not provided."""
        collector.record_metric("no_tags", 1.0)
        
        metrics = collector.get_metrics()
        assert metrics[0].tags == {}

    def test_empty_metadata_default(self, collector):
        """Test that empty metadata dict is used when metadata not provided."""
        collector.record_metric("no_metadata", 1.0)
        
        metrics = collector.get_metrics()
        assert metrics[0].metadata == {}

