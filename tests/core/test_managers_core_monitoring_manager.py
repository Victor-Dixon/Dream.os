"""
Unit tests for core_monitoring_manager.py - MEDIUM PRIORITY

Tests CoreMonitoringManager class and monitoring operations.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_monitoring_manager import CoreMonitoringManager


class TestCoreMonitoringManager:
    """Test suite for CoreMonitoringManager class."""

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    @pytest.fixture
    def manager(self):
        """Create CoreMonitoringManager instance with mocked managers."""
        with patch('src.core.managers.core_monitoring_manager.AlertManager') as mock_alert_class, \
             patch('src.core.managers.core_monitoring_manager.MetricManager') as mock_metric_class, \
             patch('src.core.managers.core_monitoring_manager.WidgetManager') as mock_widget_class:
            
            mock_alert = MagicMock()
            mock_alert.alerts = {}
            mock_alert.setup_default_alert_rules = MagicMock()
            mock_alert.create_alert = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_alert.acknowledge_alert = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_alert.resolve_alert = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_alert.get_alerts = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_alert_class.return_value = mock_alert
            
            mock_metric = MagicMock()
            mock_metric.metrics = {}
            mock_metric.metric_history = {}
            mock_metric.record_metric = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_metric.get_metrics = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_metric_class.return_value = mock_metric
            
            mock_widget = MagicMock()
            mock_widget.widgets = {}
            mock_widget.create_widget = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_widget.get_widgets = MagicMock(return_value=ManagerResult(success=True, data={}, metrics={}))
            mock_widget_class.return_value = mock_widget
            
            manager = CoreMonitoringManager()
            manager.alert_manager = mock_alert
            manager.metric_manager = mock_metric
            manager.widget_manager = mock_widget
            return manager

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert hasattr(manager, 'alert_manager')
        assert hasattr(manager, 'metric_manager')
        assert hasattr(manager, 'widget_manager')

    def test_initialize(self, manager, mock_context):
        """Test manager initialization with context."""
        result = manager.initialize(mock_context)
        assert result is True
        manager.alert_manager.setup_default_alert_rules.assert_called_once()

    def test_initialize_failure(self, manager, mock_context):
        """Test manager initialization failure."""
        manager.alert_manager.setup_default_alert_rules.side_effect = Exception("Setup failed")
        result = manager.initialize(mock_context)
        assert result is False

    def test_execute_create_alert(self, manager, mock_context):
        """Test execute create_alert operation."""
        expected_result = ManagerResult(
            success=True,
            data={"alert_id": "alert-123"},
            metrics={}
        )
        manager.alert_manager.create_alert.return_value = expected_result
        
        result = manager.execute(mock_context, "create_alert", {"alert_data": {"message": "Test alert"}})
        assert result.success is True
        assert result.data == {"alert_id": "alert-123"}
        manager.alert_manager.create_alert.assert_called_once_with(mock_context, {"message": "Test alert"})

    def test_execute_acknowledge_alert(self, manager, mock_context):
        """Test execute acknowledge_alert operation."""
        expected_result = ManagerResult(
            success=True,
            data={"alert_id": "alert-123", "acknowledged": True},
            metrics={}
        )
        manager.alert_manager.acknowledge_alert.return_value = expected_result
        
        result = manager.execute(mock_context, "acknowledge_alert", {"alert_id": "alert-123"})
        assert result.success is True
        manager.alert_manager.acknowledge_alert.assert_called_once_with(mock_context, {"alert_id": "alert-123"})

    def test_execute_resolve_alert(self, manager, mock_context):
        """Test execute resolve_alert operation."""
        expected_result = ManagerResult(
            success=True,
            data={"alert_id": "alert-123", "resolved": True},
            metrics={}
        )
        manager.alert_manager.resolve_alert.return_value = expected_result
        
        result = manager.execute(mock_context, "resolve_alert", {"alert_id": "alert-123"})
        assert result.success is True
        manager.alert_manager.resolve_alert.assert_called_once_with(mock_context, {"alert_id": "alert-123"})

    def test_execute_get_alerts(self, manager, mock_context):
        """Test execute get_alerts operation."""
        expected_result = ManagerResult(
            success=True,
            data={"alerts": [{"id": "alert-1"}, {"id": "alert-2"}]},
            metrics={}
        )
        manager.alert_manager.get_alerts.return_value = expected_result
        
        result = manager.execute(mock_context, "get_alerts", {})
        assert result.success is True
        assert len(result.data["alerts"]) == 2
        manager.alert_manager.get_alerts.assert_called_once_with(mock_context, {})

    def test_execute_record_metric(self, manager, mock_context):
        """Test execute record_metric operation."""
        expected_result = ManagerResult(
            success=True,
            data={"metric_name": "cpu_usage", "value": 75.5},
            metrics={}
        )
        manager.metric_manager.record_metric.return_value = expected_result
        
        result = manager.execute(mock_context, "record_metric", {"metric_name": "cpu_usage", "metric_value": 75.5})
        assert result.success is True
        manager.metric_manager.record_metric.assert_called_once_with(mock_context, "cpu_usage", 75.5)

    def test_execute_get_metrics(self, manager, mock_context):
        """Test execute get_metrics operation."""
        expected_result = ManagerResult(
            success=True,
            data={"metrics": {"cpu_usage": 75.5, "memory_usage": 60.0}},
            metrics={}
        )
        manager.metric_manager.get_metrics.return_value = expected_result
        
        result = manager.execute(mock_context, "get_metrics", {})
        assert result.success is True
        assert "cpu_usage" in result.data["metrics"]
        manager.metric_manager.get_metrics.assert_called_once_with(mock_context, {})

    def test_execute_create_widget(self, manager, mock_context):
        """Test execute create_widget operation."""
        expected_result = ManagerResult(
            success=True,
            data={"widget_id": "widget-123"},
            metrics={}
        )
        manager.widget_manager.create_widget.return_value = expected_result
        
        result = manager.execute(mock_context, "create_widget", {"widget_data": {"type": "chart"}})
        assert result.success is True
        assert result.data == {"widget_id": "widget-123"}
        manager.widget_manager.create_widget.assert_called_once_with(mock_context, {"type": "chart"})

    def test_execute_get_widgets(self, manager, mock_context):
        """Test execute get_widgets operation."""
        expected_result = ManagerResult(
            success=True,
            data={"widgets": [{"id": "widget-1"}, {"id": "widget-2"}]},
            metrics={}
        )
        manager.widget_manager.get_widgets.return_value = expected_result
        
        result = manager.execute(mock_context, "get_widgets", {})
        assert result.success is True
        assert len(result.data["widgets"]) == 2
        manager.widget_manager.get_widgets.assert_called_once_with(mock_context, {})

    def test_execute_unknown_operation(self, manager, mock_context):
        """Test execute with unknown operation."""
        result = manager.execute(mock_context, "unknown_operation", {})
        assert result.success is False
        assert result.error is not None
        assert "Unknown operation" in result.error

    def test_execute_error_handling(self, manager, mock_context):
        """Test execute error handling."""
        manager.alert_manager.create_alert.side_effect = Exception("Test error")
        result = manager.execute(mock_context, "create_alert", {"alert_data": {}})
        assert result.success is False
        assert result.error is not None
        assert "error" in result.error.lower()

    def test_create_alert(self, manager, mock_context):
        """Test create_alert public method."""
        expected_result = ManagerResult(
            success=True,
            data={"alert_id": "alert-456"},
            metrics={}
        )
        manager.alert_manager.create_alert.return_value = expected_result
        
        result = manager.create_alert(mock_context, {"message": "Test"})
        assert result.success is True
        assert result.data == {"alert_id": "alert-456"}
        manager.alert_manager.create_alert.assert_called_once_with(mock_context, {"message": "Test"})

    def test_record_metric(self, manager, mock_context):
        """Test record_metric public method."""
        expected_result = ManagerResult(
            success=True,
            data={"metric_name": "test_metric", "value": 42},
            metrics={}
        )
        manager.metric_manager.record_metric.return_value = expected_result
        
        result = manager.record_metric(mock_context, "test_metric", 42)
        assert result.success is True
        manager.metric_manager.record_metric.assert_called_once_with(mock_context, "test_metric", 42)

    def test_create_widget(self, manager, mock_context):
        """Test create_widget public method."""
        expected_result = ManagerResult(
            success=True,
            data={"widget_id": "widget-789"},
            metrics={}
        )
        manager.widget_manager.create_widget.return_value = expected_result
        
        result = manager.create_widget(mock_context, {"type": "gauge"})
        assert result.success is True
        assert result.data == {"widget_id": "widget-789"}
        manager.widget_manager.create_widget.assert_called_once_with(mock_context, {"type": "gauge"})

    def test_cleanup(self, manager, mock_context):
        """Test cleanup operation."""
        manager.alert_manager.alerts = {"alert-1": {"id": "alert-1"}}
        manager.metric_manager.metrics = {"metric-1": 100}
        manager.metric_manager.metric_history = {"metric-1": [100]}
        manager.widget_manager.widgets = {"widget-1": {"id": "widget-1"}}
        
        result = manager.cleanup(mock_context)
        assert result is True
        assert len(manager.alert_manager.alerts) == 0
        assert len(manager.metric_manager.metrics) == 0
        assert len(manager.metric_manager.metric_history) == 0
        assert len(manager.widget_manager.widgets) == 0

    def test_cleanup_error_handling(self, manager, mock_context):
        """Test cleanup error handling."""
        manager.alert_manager.alerts = None  # Cause error
        result = manager.cleanup(mock_context)
        assert result is False

    def test_get_status(self, manager):
        """Test get_status operation."""
        manager.alert_manager.alerts = {
            "alert-1": {"id": "alert-1", "resolved": False},
            "alert-2": {"id": "alert-2", "resolved": True}
        }
        manager.metric_manager.metrics = {"metric-1": 100, "metric-2": 200}
        manager.widget_manager.widgets = {"widget-1": {"id": "widget-1"}}
        
        status = manager.get_status()
        assert status["total_alerts"] == 2
        assert status["unresolved_alerts"] == 1
        assert status["total_metrics"] == 2
        assert status["total_widgets"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

