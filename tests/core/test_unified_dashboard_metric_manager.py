"""
Unit tests for unified_dashboard/metric_manager.py - MEDIUM PRIORITY

Tests MetricManager class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from enum import Enum
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Create mock models first
class MetricType(Enum):
    GAUGE = "gauge"
    COUNTER = "counter"
    TIMER = "timer"
    HISTOGRAM = "histogram"

class PerformanceMetric:
    def __init__(self, metric_id, name, metric_type, value, timestamp=None, updated_at=None):
        self.metric_id = metric_id
        self.name = name
        self.metric_type = metric_type
        self.value = value
        self.timestamp = timestamp or datetime.now()
        self.updated_at = updated_at or datetime.now()

# Mock the models module before importing
mock_models = MagicMock()
mock_models.MetricType = MetricType
mock_models.PerformanceMetric = PerformanceMetric

# Patch sys.modules to include our mock models
import sys
sys.modules['src.core.performance.unified_dashboard.models'] = mock_models

# Import using importlib to bypass __init__.py chain
import importlib.util
metric_manager_path = project_root / "src" / "core" / "performance" / "unified_dashboard" / "metric_manager.py"
spec = importlib.util.spec_from_file_location("metric_manager", metric_manager_path)
metric_manager = importlib.util.module_from_spec(spec)
metric_manager.__package__ = 'src.core.performance.unified_dashboard'
spec.loader.exec_module(metric_manager)

MetricManager = metric_manager.MetricManager


class TestMetricManager:
    """Test suite for MetricManager class."""

    @pytest.fixture
    def manager(self):
        """Create a MetricManager instance."""
        return MetricManager()

    @pytest.fixture
    def sample_metric(self):
        """Create a sample PerformanceMetric."""
        return PerformanceMetric(
            metric_id="test_metric_1",
            name="test_metric",
            metric_type=MetricType.GAUGE,
            value=42.5
        )

    def test_initialization(self, manager):
        """Test MetricManager initialization."""
        assert manager.metrics == {}
        assert manager.logger is not None

    def test_add_metric_success(self, manager, sample_metric):
        """Test adding a valid metric."""
        result = manager.add_metric(sample_metric)
        
        assert result is True
        assert "test_metric_1" in manager.metrics
        assert manager.metrics["test_metric_1"] == sample_metric

    def test_add_metric_invalid_none(self, manager):
        """Test adding None metric."""
        result = manager.add_metric(None)
        
        assert result is False
        assert len(manager.metrics) == 0

    def test_add_metric_invalid_no_id(self, manager):
        """Test adding metric without metric_id."""
        metric = PerformanceMetric(
            metric_id=None,
            name="test",
            metric_type=MetricType.GAUGE,
            value=1.0
        )
        result = manager.add_metric(metric)
        
        assert result is False

    def test_get_metric_exists(self, manager, sample_metric):
        """Test getting an existing metric."""
        manager.add_metric(sample_metric)
        
        retrieved = manager.get_metric("test_metric_1")
        
        assert retrieved == sample_metric
        assert retrieved.metric_id == "test_metric_1"

    def test_get_metric_not_exists(self, manager):
        """Test getting a non-existent metric."""
        retrieved = manager.get_metric("nonexistent")
        
        assert retrieved is None

    def test_get_metrics_by_type(self, manager):
        """Test getting metrics filtered by type."""
        metric1 = PerformanceMetric("m1", "gauge_metric", MetricType.GAUGE, 10.0)
        metric2 = PerformanceMetric("m2", "counter_metric", MetricType.COUNTER, 5.0)
        metric3 = PerformanceMetric("m3", "gauge_metric2", MetricType.GAUGE, 20.0)
        
        manager.add_metric(metric1)
        manager.add_metric(metric2)
        manager.add_metric(metric3)
        
        gauge_metrics = manager.get_metrics_by_type(MetricType.GAUGE)
        
        assert len(gauge_metrics) == 2
        assert all(m.metric_type == MetricType.GAUGE for m in gauge_metrics)

    def test_update_metric_success(self, manager, sample_metric):
        """Test updating an existing metric."""
        manager.add_metric(sample_metric)
        
        updates = {"value": 100.0, "name": "updated_name"}
        result = manager.update_metric("test_metric_1", updates)
        
        assert result is True
        assert manager.metrics["test_metric_1"].value == 100.0
        assert manager.metrics["test_metric_1"].name == "updated_name"
        assert manager.metrics["test_metric_1"].updated_at is not None

    def test_update_metric_not_exists(self, manager):
        """Test updating a non-existent metric."""
        result = manager.update_metric("nonexistent", {"value": 10.0})
        
        assert result is False

    def test_remove_metric_success(self, manager, sample_metric):
        """Test removing an existing metric."""
        manager.add_metric(sample_metric)
        
        result = manager.remove_metric("test_metric_1")
        
        assert result is True
        assert "test_metric_1" not in manager.metrics

    def test_remove_metric_not_exists(self, manager):
        """Test removing a non-existent metric."""
        result = manager.remove_metric("nonexistent")
        
        assert result is False

    def test_get_all_metrics(self, manager):
        """Test getting all metrics."""
        metric1 = PerformanceMetric("m1", "metric1", MetricType.GAUGE, 1.0)
        metric2 = PerformanceMetric("m2", "metric2", MetricType.COUNTER, 2.0)
        
        manager.add_metric(metric1)
        manager.add_metric(metric2)
        
        all_metrics = manager.get_all_metrics()
        
        assert len(all_metrics) == 2
        assert metric1 in all_metrics
        assert metric2 in all_metrics

    def test_get_metrics_count(self, manager):
        """Test getting metrics count."""
        assert manager.get_metrics_count() == 0
        
        manager.add_metric(PerformanceMetric("m1", "m1", MetricType.GAUGE, 1.0))
        assert manager.get_metrics_count() == 1
        
        manager.add_metric(PerformanceMetric("m2", "m2", MetricType.COUNTER, 2.0))
        assert manager.get_metrics_count() == 2

    def test_clear_metrics(self, manager):
        """Test clearing all metrics."""
        manager.add_metric(PerformanceMetric("m1", "m1", MetricType.GAUGE, 1.0))
        manager.add_metric(PerformanceMetric("m2", "m2", MetricType.COUNTER, 2.0))
        
        manager.clear_metrics()
        
        assert manager.get_metrics_count() == 0
        assert manager.metrics == {}

    def test_get_metrics_summary(self, manager):
        """Test getting metrics summary."""
        metric1 = PerformanceMetric("m1", "gauge_metric", MetricType.GAUGE, 10.0)
        metric2 = PerformanceMetric("m2", "counter_metric", MetricType.COUNTER, 5.0)
        
        manager.add_metric(metric1)
        manager.add_metric(metric2)
        
        summary = manager.get_metrics_summary()
        
        assert summary["total_metrics"] == 2
        assert "gauge" in summary["metric_types"]
        assert "counter" in summary["metric_types"]
        assert summary["last_updated"] is not None

    def test_get_metrics_summary_empty(self, manager):
        """Test getting metrics summary when no metrics exist."""
        summary = manager.get_metrics_summary()
        
        assert summary["total_metrics"] == 0
        assert summary["metric_types"] == []
        assert summary["last_updated"] is None

    def test_multiple_operations(self, manager):
        """Test multiple operations in sequence."""
        metric = PerformanceMetric("m1", "test", MetricType.GAUGE, 10.0)
        
        # Add
        assert manager.add_metric(metric) is True
        assert manager.get_metrics_count() == 1
        
        # Update
        assert manager.update_metric("m1", {"value": 20.0}) is True
        assert manager.get_metric("m1").value == 20.0
        
        # Remove
        assert manager.remove_metric("m1") is True
        assert manager.get_metrics_count() == 0
