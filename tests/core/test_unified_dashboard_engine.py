"""
Unit tests for unified_dashboard/engine.py - MEDIUM PRIORITY

Tests DashboardEngine class functionality.
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

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class PerformanceMetric:
    def __init__(self, metric_id, name, metric_type, value, **kwargs):
        self.metric_id = metric_id
        self.name = name
        self.metric_type = metric_type
        self.value = value
        for key, value in kwargs.items():
            setattr(self, key, value)

class DashboardConfig:
    def __init__(self, config_id, **kwargs):
        self.config_id = config_id
        for key, value in kwargs.items():
            setattr(self, key, value)

class DashboardWidget:
    def __init__(self, widget_id, **kwargs):
        self.widget_id = widget_id
        for key, value in kwargs.items():
            setattr(self, key, value)

class PerformanceAlert:
    def __init__(self, alert_id, level, message, **kwargs):
        self.alert_id = alert_id
        self.level = level
        self.message = message
        for key, value in kwargs.items():
            setattr(self, key, value)

class PerformanceReport:
    def __init__(self, report_id, report_type="standard", **kwargs):
        self.report_id = report_id
        self.report_type = report_type
        for key, value in kwargs.items():
            setattr(self, key, value)

# Mock the models module before importing
mock_models = MagicMock()
mock_models.MetricType = MetricType
mock_models.PerformanceMetric = PerformanceMetric
mock_models.DashboardConfig = DashboardConfig
mock_models.DashboardWidget = DashboardWidget
mock_models.AlertLevel = AlertLevel
mock_models.PerformanceAlert = PerformanceAlert
mock_models.PerformanceReport = PerformanceReport

# Patch sys.modules
sys.modules['src.core.performance.unified_dashboard.models'] = mock_models

# Mock MetricManager and WidgetManager
mock_metric_manager = MagicMock()
mock_widget_manager = MagicMock()

# Import using importlib to bypass __init__.py chain
import importlib.util
engine_path = project_root / "src" / "core" / "performance" / "unified_dashboard" / "engine.py"
spec = importlib.util.spec_from_file_location("engine", engine_path)
engine = importlib.util.module_from_spec(spec)
engine.__package__ = 'src.core.performance.unified_dashboard'

# Patch metric_manager and widget_manager imports
with patch.dict('sys.modules', {
    'src.core.performance.unified_dashboard.models': mock_models,
    'src.core.performance.unified_dashboard.metric_manager': mock_metric_manager,
    'src.core.performance.unified_dashboard.widget_manager': mock_widget_manager,
}):
    # Mock the classes
    mock_metric_manager.MetricManager = MagicMock
    mock_widget_manager.WidgetManager = MagicMock
    
    spec.loader.exec_module(engine)

DashboardEngine = engine.DashboardEngine


class TestDashboardEngine:
    """Test suite for DashboardEngine class."""

    @pytest.fixture
    def engine_instance(self):
        """Create a DashboardEngine instance."""
        # Create mock MetricManager and WidgetManager instances
        mock_metric_mgr = MagicMock()
        mock_metric_mgr.get_metrics_count = Mock(return_value=0)
        mock_metric_mgr.get_metrics_summary = Mock(return_value={"total_metrics": 0})
        mock_metric_mgr.add_metric = Mock(return_value=True)
        mock_metric_mgr.get_metric = Mock(return_value=None)
        mock_metric_mgr.get_metrics_by_type = Mock(return_value=[])
        mock_metric_mgr.get_all_metrics = Mock(return_value=[])
        mock_metric_mgr.clear_metrics = Mock()
        
        mock_widget_mgr = MagicMock()
        mock_widget_mgr.get_widgets_count = Mock(return_value=0)
        mock_widget_mgr.get_summary = Mock(return_value={"total_widgets": 0})
        mock_widget_mgr.add_widget = Mock(return_value=True)
        mock_widget_mgr.get_widget = Mock(return_value=None)
        mock_widget_mgr.get_all_widgets = Mock(return_value=[])
        mock_widget_mgr.add_config = Mock(return_value=True)
        mock_widget_mgr.get_config = Mock(return_value=None)
        mock_widget_mgr.get_all_configs = Mock(return_value=[])
        mock_widget_mgr.clear_all = Mock()
        
        # Patch the MetricManager and WidgetManager classes
        with patch.object(engine, 'MetricManager', return_value=mock_metric_mgr), \
             patch.object(engine, 'WidgetManager', return_value=mock_widget_mgr):
            instance = DashboardEngine()
            instance.metric_manager = mock_metric_mgr
            instance.widget_manager = mock_widget_mgr
            return instance

    @pytest.fixture
    def sample_metric(self):
        """Create a sample PerformanceMetric."""
        return PerformanceMetric(
            metric_id="test_metric_1",
            name="test_metric",
            metric_type=MetricType.GAUGE,
            value=42.5
        )

    @pytest.fixture
    def sample_widget(self):
        """Create a sample DashboardWidget."""
        return DashboardWidget(widget_id="test_widget_1")

    @pytest.fixture
    def sample_config(self):
        """Create a sample DashboardConfig."""
        return DashboardConfig(config_id="test_config_1")

    @pytest.fixture
    def sample_alert(self):
        """Create a sample PerformanceAlert."""
        return PerformanceAlert(
            alert_id="test_alert_1",
            level=AlertLevel.WARNING,
            message="Test alert"
        )

    @pytest.fixture
    def sample_report(self):
        """Create a sample PerformanceReport."""
        return PerformanceReport(report_id="test_report_1")

    def test_initialization(self, engine_instance):
        """Test DashboardEngine initialization."""
        assert engine_instance.alerts == {}
        assert engine_instance.reports == {}
        assert engine_instance.metric_manager is not None
        assert engine_instance.widget_manager is not None

    def test_add_metric(self, engine_instance, sample_metric):
        """Test adding a metric."""
        engine_instance.metric_manager.add_metric.return_value = True
        
        result = engine_instance.add_metric(sample_metric)
        
        assert result is True
        engine_instance.metric_manager.add_metric.assert_called_once_with(sample_metric)

    def test_get_metric(self, engine_instance, sample_metric):
        """Test getting a metric."""
        engine_instance.metric_manager.get_metric.return_value = sample_metric
        
        retrieved = engine_instance.get_metric("test_metric_1")
        
        assert retrieved == sample_metric
        engine_instance.metric_manager.get_metric.assert_called_once_with("test_metric_1")

    def test_get_metrics_by_type(self, engine_instance):
        """Test getting metrics by type."""
        mock_metrics = [PerformanceMetric("m1", "m1", MetricType.GAUGE, 1.0)]
        engine_instance.metric_manager.get_metrics_by_type.return_value = mock_metrics
        
        result = engine_instance.get_metrics_by_type(MetricType.GAUGE)
        
        assert result == mock_metrics
        engine_instance.metric_manager.get_metrics_by_type.assert_called_once_with(MetricType.GAUGE)

    def test_add_widget(self, engine_instance, sample_widget):
        """Test adding a widget."""
        engine_instance.widget_manager.add_widget.return_value = True
        
        result = engine_instance.add_widget(sample_widget)
        
        assert result is True
        engine_instance.widget_manager.add_widget.assert_called_once_with(sample_widget)

    def test_get_widget(self, engine_instance, sample_widget):
        """Test getting a widget."""
        engine_instance.widget_manager.get_widget.return_value = sample_widget
        
        retrieved = engine_instance.get_widget("test_widget_1")
        
        assert retrieved == sample_widget
        engine_instance.widget_manager.get_widget.assert_called_once_with("test_widget_1")

    def test_add_config(self, engine_instance, sample_config):
        """Test adding a config."""
        engine_instance.widget_manager.add_config.return_value = True
        
        result = engine_instance.add_config(sample_config)
        
        assert result is True
        engine_instance.widget_manager.add_config.assert_called_once_with(sample_config)

    def test_add_alert_success(self, engine_instance, sample_alert):
        """Test adding a valid alert."""
        result = engine_instance.add_alert(sample_alert)
        
        assert result is True
        assert "test_alert_1" in engine_instance.alerts
        assert engine_instance.alerts["test_alert_1"] == sample_alert

    def test_add_alert_invalid_none(self, engine_instance):
        """Test adding None alert."""
        result = engine_instance.add_alert(None)
        
        assert result is False

    def test_add_alert_invalid_no_id(self, engine_instance):
        """Test adding alert without alert_id."""
        alert = PerformanceAlert(alert_id=None, level=AlertLevel.INFO, message="test")
        result = engine_instance.add_alert(alert)
        
        assert result is False

    def test_get_alert(self, engine_instance, sample_alert):
        """Test getting an alert."""
        engine_instance.add_alert(sample_alert)
        
        retrieved = engine_instance.get_alert("test_alert_1")
        
        assert retrieved == sample_alert

    def test_get_alert_not_exists(self, engine_instance):
        """Test getting a non-existent alert."""
        retrieved = engine_instance.get_alert("nonexistent")
        
        assert retrieved is None

    def test_remove_alert_success(self, engine_instance, sample_alert):
        """Test removing an alert."""
        engine_instance.add_alert(sample_alert)
        
        result = engine_instance.remove_alert("test_alert_1")
        
        assert result is True
        assert "test_alert_1" not in engine_instance.alerts

    def test_remove_alert_not_exists(self, engine_instance):
        """Test removing a non-existent alert."""
        result = engine_instance.remove_alert("nonexistent")
        
        assert result is False

    def test_add_report_success(self, engine_instance, sample_report):
        """Test adding a valid report."""
        result = engine_instance.add_report(sample_report)
        
        assert result is True
        assert "test_report_1" in engine_instance.reports
        assert engine_instance.reports["test_report_1"] == sample_report

    def test_add_report_invalid_none(self, engine_instance):
        """Test adding None report."""
        result = engine_instance.add_report(None)
        
        assert result is False

    def test_get_report(self, engine_instance, sample_report):
        """Test getting a report."""
        engine_instance.add_report(sample_report)
        
        retrieved = engine_instance.get_report("test_report_1")
        
        assert retrieved == sample_report

    def test_get_report_not_exists(self, engine_instance):
        """Test getting a non-existent report."""
        retrieved = engine_instance.get_report("nonexistent")
        
        assert retrieved is None

    def test_remove_report_success(self, engine_instance, sample_report):
        """Test removing a report."""
        engine_instance.add_report(sample_report)
        
        result = engine_instance.remove_report("test_report_1")
        
        assert result is True
        assert "test_report_1" not in engine_instance.reports

    def test_get_status(self, engine_instance):
        """Test getting engine status."""
        engine_instance.metric_manager.get_metrics_count = Mock(return_value=5)
        engine_instance.widget_manager.get_widgets_count = Mock(return_value=3)
        
        status = engine_instance.get_status()
        
        assert "status" in status
        assert status["metrics_count"] == 5
        assert status["widgets_count"] == 3
        assert status["alerts_count"] == 0
        assert status["reports_count"] == 0

    def test_get_summary(self, engine_instance):
        """Test getting engine summary."""
        engine_instance.metric_manager.get_metrics_summary = Mock(return_value={"total_metrics": 2})
        engine_instance.widget_manager.get_summary = Mock(return_value={"total_widgets": 1})
        
        summary = engine_instance.get_summary()
        
        assert "metrics" in summary
        assert "widgets" in summary
        assert "alerts" in summary
        assert "reports" in summary

    def test_clear_resources(self, engine_instance, sample_metric, sample_widget, sample_alert, sample_report):
        """Test clearing all resources."""
        engine_instance.add_metric(sample_metric)
        engine_instance.add_widget(sample_widget)
        engine_instance.add_alert(sample_alert)
        engine_instance.add_report(sample_report)
        
        engine_instance.clear_resources()
        
        engine_instance.metric_manager.clear_metrics.assert_called_once()
        assert len(engine_instance.alerts) == 0
        assert len(engine_instance.reports) == 0
        engine_instance.widget_manager.clear_all.assert_called_once()

