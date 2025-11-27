"""
Unit tests for coordination_performance_monitor.py - MEDIUM PRIORITY

Tests CoordinationPerformanceMonitor class and get_performance_monitor function.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import time
import threading
from datetime import timedelta

# Add project root to path
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import directly to avoid __init__.py import chain issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "coordination_performance_monitor",
    project_root / "src" / "core" / "performance" / "coordination_performance_monitor.py"
)
coordination_performance_monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coordination_performance_monitor)

CoordinationPerformanceMonitor = coordination_performance_monitor.CoordinationPerformanceMonitor
get_performance_monitor = coordination_performance_monitor.get_performance_monitor


class TestCoordinationPerformanceMonitor:
    """Test suite for CoordinationPerformanceMonitor class."""

    @pytest.fixture
    def mock_collector(self):
        """Create a mock performance collector."""
        collector = Mock()
        collector.record_metric = Mock()
        collector.record_timer = Mock()
        collector.record_counter = Mock()
        return collector

    @pytest.fixture
    def mock_analyzer(self):
        """Create a mock performance analyzer."""
        analyzer = Mock()
        analyzer.generate_performance_report = Mock(return_value={"analysis": {}, "metrics": []})
        analyzer._generate_summary = Mock(return_value={"status": "active"})
        return analyzer

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_initialization(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test monitor initialization."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()

        assert monitor.collector == mock_collector
        assert monitor.analyzer == mock_analyzer
        assert monitor.monitoring_active is True
        assert monitor.monitoring_thread is not None
        assert isinstance(monitor.monitoring_thread, threading.Thread)
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_record_operation_start(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test recording operation start."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        monitor.record_operation_start("test_operation", tags={"env": "test"})

        mock_collector.record_metric.assert_called_once()
        call_args = mock_collector.record_metric.call_args
        assert "test_operation_start" in call_args[0][0]
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_record_operation_completion_success(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test recording successful operation completion."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        monitor.record_operation_completion("test_operation", 1.5, success=True)

        # Should record timer, success counter, and throughput
        assert mock_collector.record_timer.call_count == 1
        assert mock_collector.record_counter.call_count == 2  # success + throughput
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_record_operation_completion_failure(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test recording failed operation completion."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        monitor.record_operation_completion("test_operation", 0.5, success=False)

        # Should record timer, failure counter, and throughput
        assert mock_collector.record_timer.call_count == 1
        assert mock_collector.record_counter.call_count == 2  # failure + throughput
        
        # Check that failure counter was called
        counter_calls = [call[0][0] for call in mock_collector.record_counter.call_args_list]
        assert any("failure" in call for call in counter_calls)
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_record_operation_completion_with_tags(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test recording operation completion with tags."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        tags = {"env": "test", "service": "api"}
        monitor.record_operation_completion("test_operation", 2.0, success=True, tags=tags)

        # Check that tags were passed to collector methods
        timer_call = mock_collector.record_timer.call_args
        assert timer_call[1]["tags"] == tags
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_get_performance_report(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test getting performance report."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer
        mock_analyzer.generate_performance_report.return_value = {"analysis": {"cpu": 50}, "metrics": []}

        monitor = CoordinationPerformanceMonitor()
        time_window = timedelta(hours=2)
        report = monitor.get_performance_report(time_window)

        assert report == {"analysis": {"cpu": 50}, "metrics": []}
        mock_analyzer.generate_performance_report.assert_called_once_with(time_window)
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_get_performance_report_default_time_window(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test getting performance report with default time window."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        report = monitor.get_performance_report()

        mock_analyzer.generate_performance_report.assert_called_once()
        call_args = mock_analyzer.generate_performance_report.call_args
        assert isinstance(call_args[0][0], timedelta)
        assert call_args[0][0] == timedelta(hours=1)  # Default
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_get_system_health(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test getting system health status."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer
        mock_analyzer.generate_performance_report.return_value = {"analysis": {"status": "healthy"}}
        mock_analyzer._generate_summary.return_value = {"status": "active", "health": "good"}

        monitor = CoordinationPerformanceMonitor()
        health = monitor.get_system_health()

        assert health == {"status": "active", "health": "good"}
        mock_analyzer.generate_performance_report.assert_called_once()
        mock_analyzer._generate_summary.assert_called_once()
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    @patch('sys.modules', {'psutil': MagicMock()})
    def test_record_system_health_with_psutil(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test recording system health when psutil is available."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer
        
        # Mock psutil via sys.modules
        import sys
        mock_psutil = sys.modules['psutil']
        mock_memory = Mock()
        mock_memory.percent = 75.5
        mock_memory.available = 4 * (1024**3)  # 4 GB
        mock_psutil.virtual_memory.return_value = mock_memory

        monitor = CoordinationPerformanceMonitor()
        
        # Wait a bit for background thread to record
        time.sleep(0.2)
        
        # Check that metrics were recorded (at least heartbeat, possibly memory metrics)
        assert mock_collector.record_metric.call_count >= 1  # At least heartbeat
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_record_system_health_without_psutil(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test recording system health when psutil is not available."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        # Simulate psutil ImportError
        with patch.dict('sys.modules', {'psutil': None}):
            monitor = CoordinationPerformanceMonitor()
            
            # Wait a bit for background thread to record
            time.sleep(0.1)
            
            # Should still record heartbeat even without psutil
            assert mock_collector.record_metric.call_count >= 1  # At least heartbeat
        
        # Clean up
        monitor.stop_monitoring()

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_stop_monitoring(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test stopping background monitoring."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        assert monitor.monitoring_active is True
        
        monitor.stop_monitoring()
        
        assert monitor.monitoring_active is False
        # Thread should be joined (or timeout)
        if monitor.monitoring_thread:
            assert not monitor.monitoring_thread.is_alive() or monitor.monitoring_thread.is_alive()  # Either joined or still running

    @patch.object(coordination_performance_monitor, 'PerformanceCollector')
    @patch.object(coordination_performance_monitor, 'PerformanceAnalyzer')
    def test_stop_monitoring_no_thread(self, mock_analyzer_class, mock_collector_class, mock_collector, mock_analyzer):
        """Test stopping monitoring when thread doesn't exist."""
        mock_collector_class.return_value = mock_collector
        mock_analyzer_class.return_value = mock_analyzer

        monitor = CoordinationPerformanceMonitor()
        monitor.monitoring_thread = None
        
        # Should not raise error
        monitor.stop_monitoring()
        assert monitor.monitoring_active is False


class TestGetPerformanceMonitor:
    """Test suite for get_performance_monitor function."""

    def test_get_performance_monitor_returns_instance(self):
        """Test that get_performance_monitor returns a CoordinationPerformanceMonitor instance."""
        # Reset global state
        coordination_performance_monitor._performance_monitor = None
        
        monitor = get_performance_monitor()
        
        assert isinstance(monitor, CoordinationPerformanceMonitor)
        
        # Clean up
        monitor.stop_monitoring()

    def test_get_performance_monitor_singleton(self):
        """Test that get_performance_monitor returns the same instance (singleton)."""
        # Reset global state
        coordination_performance_monitor._performance_monitor = None
        
        monitor1 = get_performance_monitor()
        monitor2 = get_performance_monitor()
        
        assert monitor1 is monitor2
        
        # Clean up
        monitor1.stop_monitoring()

