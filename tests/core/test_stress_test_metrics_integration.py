"""
Unit Tests for Stress Test Metrics Integration
==============================================
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from src.core.stress_test_metrics_integration import (
    StressTestMetricsIntegration,
    create_stress_test_integration,
)
from src.core.stress_test_metrics import StressTestMetricsCollector


class TestStressTestMetricsIntegration:
    """Tests for StressTestMetricsIntegration."""

    def test_initialization(self):
        """Test integration initialization."""
        integration = StressTestMetricsIntegration()
        assert integration.collector is not None
        assert isinstance(integration.collector, StressTestMetricsCollector)

    def test_initialization_with_collector(self):
        """Test initialization with custom collector."""
        collector = StressTestMetricsCollector()
        integration = StressTestMetricsIntegration(collector)
        assert integration.collector == collector

    def test_integrate_with_message_queue(self):
        """Test integrating with message queue."""
        integration = StressTestMetricsIntegration()
        mock_queue = MagicMock()
        integration.integrate_with_message_queue(mock_queue)
        # Should not raise exception

    def test_record_queue_event_message_queued(self):
        """Test recording message queued event."""
        integration = StressTestMetricsIntegration()
        integration.record_queue_event(
            "message_queued",
            queue_id="test_queue",
            agent_id="Agent-1",
            message_type="text",
            queue_depth=5,
        )
        assert integration.collector.total_messages == 1

    def test_record_queue_event_message_delivered(self):
        """Test recording message delivered event."""
        integration = StressTestMetricsIntegration()
        integration.record_queue_event(
            "message_delivered",
            queue_id="test_queue",
            agent_id="Agent-1",
            message_type="text",
            latency_ms=10.0,
            delivery_mode="real",
        )
        assert len(integration.collector.real_delivery_times) == 1

    def test_record_queue_event_message_failed(self):
        """Test recording message failed event."""
        integration = StressTestMetricsIntegration()
        integration.record_queue_event(
            "message_failed",
            queue_id="test_queue",
            agent_id="Agent-1",
            message_type="text",
            reason="timeout",
        )
        assert integration.collector.failed_messages == 1

    def test_integrate_with_stress_test_runner(self):
        """Test integrating with stress test runner."""
        integration = StressTestMetricsIntegration()
        test_config = {"duration": 60, "messages_per_second": 10.0}
        collector = integration.integrate_with_stress_test_runner(test_config)
        assert collector.test_start_time is not None
        assert collector.test_config == test_config

    @patch('src.core.stress_test_metrics_integration.StressTestAnalyzer')
    def test_finalize_stress_test(self, mock_analyzer_class, tmp_path):
        """Test finalizing stress test."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.analyze_failure_patterns.return_value = {}
        mock_analyzer_class.return_value = mock_analyzer
        
        integration = StressTestMetricsIntegration()
        integration.collector.start_test({"test": "config"})
        integration.collector.record_latency(10.0)
        
        dashboard = integration.finalize_stress_test(str(tmp_path))
        assert "test_metadata" in dashboard
        assert "analysis" in dashboard
        assert integration.collector.test_end_time is not None

    def test_finalize_stress_test_without_output_dir(self):
        """Test finalizing stress test without output directory."""
        integration = StressTestMetricsIntegration()
        integration.collector.start_test({})
        dashboard = integration.finalize_stress_test()
        assert "test_metadata" in dashboard


class TestFactoryFunction:
    """Tests for factory function."""

    def test_create_integration(self):
        """Test creating integration via factory."""
        integration = create_stress_test_integration()
        assert isinstance(integration, StressTestMetricsIntegration)

    def test_create_integration_with_collector(self):
        """Test creating integration with collector."""
        collector = StressTestMetricsCollector()
        integration = create_stress_test_integration(collector)
        assert integration.collector == collector


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


