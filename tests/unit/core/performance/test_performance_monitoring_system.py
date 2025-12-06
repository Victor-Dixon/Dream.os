"""
Tests for performance_monitoring_system.py - PerformanceMonitoringSystem class.

Target: ≥85% coverage, comprehensive test suite.
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-05
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.core.performance.performance_monitoring_system import (
    PerformanceMonitoringSystem,
    PerformanceMetric,
    PerformanceReport,
    create_performance_monitoring_system,
    get_performance_monitor,
)


class TestPerformanceMetric:
    """Test PerformanceMetric dataclass."""

    def test_init(self):
        """Test PerformanceMetric initialization."""
        timestamp = datetime.now()
        metric = PerformanceMetric(
            name="test_metric",
            value=42.5,
            timestamp=timestamp,
            category="test",
            unit="ms",
        )
        assert metric.name == "test_metric"
        assert metric.value == 42.5
        assert metric.timestamp == timestamp
        assert metric.category == "test"
        assert metric.unit == "ms"

    def test_init_defaults(self):
        """Test PerformanceMetric with default values."""
        timestamp = datetime.now()
        metric = PerformanceMetric(
            name="test_metric",
            value=42.5,
            timestamp=timestamp,
        )
        assert metric.category == "general"
        assert metric.unit == "ms"

    def test_to_dict(self):
        """Test PerformanceMetric to_dict conversion."""
        timestamp = datetime.now()
        metric = PerformanceMetric(
            name="test_metric",
            value=42.5,
            timestamp=timestamp,
            category="test",
            unit="ms",
        )
        result = metric.to_dict()
        assert result["name"] == "test_metric"
        assert result["value"] == 42.5
        assert result["category"] == "test"
        assert result["unit"] == "ms"
        assert isinstance(result["timestamp"], str)


class TestPerformanceReport:
    """Test PerformanceReport dataclass."""

    def test_init(self):
        """Test PerformanceReport initialization."""
        timestamp = datetime.now()
        metrics = [
            PerformanceMetric(
                name="test_metric",
                value=42.5,
                timestamp=timestamp,
            )
        ]
        report = PerformanceReport(
            report_id="test_report_001",
            timestamp=timestamp,
            metrics=metrics,
            summary="Test summary",
        )
        assert report.report_id == "test_report_001"
        assert report.timestamp == timestamp
        assert len(report.metrics) == 1
        assert report.summary == "Test summary"

    def test_init_default_summary(self):
        """Test PerformanceReport with default summary."""
        timestamp = datetime.now()
        report = PerformanceReport(
            report_id="test_report_002",
            timestamp=timestamp,
            metrics=[],
        )
        assert report.summary == ""

    def test_to_dict(self):
        """Test PerformanceReport to_dict conversion."""
        timestamp = datetime.now()
        metrics = [
            PerformanceMetric(
                name="test_metric",
                value=42.5,
                timestamp=timestamp,
            )
        ]
        report = PerformanceReport(
            report_id="test_report_003",
            timestamp=timestamp,
            metrics=metrics,
            summary="Test summary",
        )
        result = report.to_dict()
        assert result["report_id"] == "test_report_003"
        assert result["summary"] == "Test summary"
        assert len(result["metrics"]) == 1
        assert isinstance(result["timestamp"], str)


class TestPerformanceMonitoringSystem:
    """Test PerformanceMonitoringSystem class."""

    def test_init(self):
        """Test PerformanceMonitoringSystem initialization."""
        monitor = PerformanceMonitoringSystem()
        assert monitor is not None
        assert monitor.is_monitoring is False
        assert monitor.monitoring_interval == 5.0
        assert len(monitor.metrics_history) == 0

    def test_init_with_logger(self):
        """Test PerformanceMonitoringSystem initialization with logger."""
        logger = Mock()
        monitor = PerformanceMonitoringSystem(logger=logger)
        assert monitor.logger == logger

    def test_start_monitoring(self):
        """Test start_monitoring method."""
        monitor = PerformanceMonitoringSystem()
        result = monitor.start_monitoring()
        assert result is True
        assert monitor.is_monitoring is True

    def test_start_monitoring_already_started(self):
        """Test start_monitoring when already monitoring."""
        monitor = PerformanceMonitoringSystem()
        monitor.start_monitoring()
        result = monitor.start_monitoring()
        assert result is True
        assert monitor.is_monitoring is True

    def test_stop_monitoring(self):
        """Test stop_monitoring method."""
        monitor = PerformanceMonitoringSystem()
        monitor.start_monitoring()
        result = monitor.stop_monitoring()
        assert result is True
        assert monitor.is_monitoring is False

    @patch("src.core.performance.performance_monitoring_system.psutil")
    def test_collect_metrics(self, mock_psutil):
        """Test collect_metrics method."""
        # Mock psutil responses
        mock_psutil.cpu_percent.return_value = 50.0
        mock_memory = Mock()
        mock_memory.percent = 60.0
        mock_psutil.virtual_memory.return_value = mock_memory
        mock_disk = Mock()
        mock_disk.used = 50000000000
        mock_disk.total = 100000000000
        mock_psutil.disk_usage.return_value = mock_disk

        monitor = PerformanceMonitoringSystem()
        metrics = monitor.collect_metrics()

        assert len(metrics) == 3
        assert any(m.name == "cpu_usage" for m in metrics)
        assert any(m.name == "memory_usage" for m in metrics)
        assert any(m.name == "disk_usage" for m in metrics)
        assert len(monitor.metrics_history) == 3

    @patch("src.core.performance.performance_monitoring_system.psutil")
    def test_collect_metrics_error_handling(self, mock_psutil):
        """Test collect_metrics error handling."""
        mock_psutil.cpu_percent.side_effect = Exception("Test error")
        monitor = PerformanceMonitoringSystem()
        metrics = monitor.collect_metrics()
        assert metrics == []

    @patch("src.core.performance.performance_monitoring_system.psutil")
    def test_generate_report(self, mock_psutil):
        """Test generate_report method."""
        # Mock psutil responses
        mock_psutil.cpu_percent.return_value = 50.0
        mock_memory = Mock()
        mock_memory.percent = 60.0
        mock_psutil.virtual_memory.return_value = mock_memory
        mock_disk = Mock()
        mock_disk.used = 50000000000
        mock_disk.total = 100000000000
        mock_psutil.disk_usage.return_value = mock_disk

        monitor = PerformanceMonitoringSystem()
        report = monitor.generate_report()

        assert isinstance(report, PerformanceReport)
        assert report.report_id.startswith("perf_report_")
        assert len(report.metrics) == 3
        assert "Performance report" in report.summary

    def test_generate_report_error_handling(self):
        """Test generate_report error handling."""
        monitor = PerformanceMonitoringSystem()
        with patch.object(
            monitor, "collect_metrics", side_effect=Exception("Test error")
        ):
            report = monitor.generate_report()
            assert isinstance(report, PerformanceReport)
            assert report.report_id.startswith("error_report_")
            assert "Error generating report" in report.summary

    def test_get_system_status(self):
        """Test get_system_status method."""
        monitor = PerformanceMonitoringSystem()
        status = monitor.get_system_status()

        assert isinstance(status, dict)
        assert status["is_monitoring"] is False
        assert status["metrics_count"] == 0
        assert status["monitoring_interval"] == 5.0
        assert status["status"] == "stopped"

    def test_get_system_status_monitoring(self):
        """Test get_system_status when monitoring."""
        monitor = PerformanceMonitoringSystem()
        monitor.start_monitoring()
        status = monitor.get_system_status()

        assert status["is_monitoring"] is True
        assert status["status"] == "active"

    def test_get_metrics_summary_empty(self):
        """Test get_metrics_summary when no metrics."""
        monitor = PerformanceMonitoringSystem()
        summary = monitor.get_metrics_summary()

        assert isinstance(summary, dict)
        assert "No metrics collected" in summary["message"]

    @patch("src.core.performance.performance_monitoring_system.psutil")
    def test_get_metrics_summary_with_metrics(self, mock_psutil):
        """Test get_metrics_summary with metrics."""
        # Mock psutil responses
        mock_psutil.cpu_percent.return_value = 50.0
        mock_memory = Mock()
        mock_memory.percent = 60.0
        mock_psutil.virtual_memory.return_value = mock_memory
        mock_disk = Mock()
        mock_disk.used = 50000000000
        mock_disk.total = 100000000000
        mock_psutil.disk_usage.return_value = mock_disk

        monitor = PerformanceMonitoringSystem()
        monitor.collect_metrics()
        summary = monitor.get_metrics_summary()

        assert isinstance(summary, dict)
        assert summary["total_metrics"] == 3
        assert summary["latest_metrics"] == 3
        assert "latest_cpu" in summary
        assert "latest_memory" in summary

    def test_cleanup(self):
        """Test cleanup method."""
        monitor = PerformanceMonitoringSystem()
        monitor.start_monitoring()
        monitor.cleanup()

        assert monitor.is_monitoring is False
        assert len(monitor.metrics_history) == 0


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_performance_monitoring_system(self):
        """Test create_performance_monitoring_system factory."""
        monitor = create_performance_monitoring_system()
        assert isinstance(monitor, PerformanceMonitoringSystem)

    def test_create_performance_monitoring_system_with_logger(self):
        """Test create_performance_monitoring_system with logger."""
        logger = Mock()
        monitor = create_performance_monitoring_system(logger=logger)
        assert monitor.logger == logger

    def test_get_performance_monitor(self):
        """Test get_performance_monitor factory."""
        monitor = get_performance_monitor()
        assert isinstance(monitor, PerformanceMonitoringSystem)

