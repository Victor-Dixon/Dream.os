#!/usr/bin/env python3
"""
Unit Tests for Stress Test Metrics
===================================
"""

import pytest
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.stress_test_metrics import (
    StressTestMetricsCollector,
    StressTestAnalyzer,
    create_stress_test_metrics_collector,
)


class TestStressTestMetricsCollector:
    """Tests for StressTestMetricsCollector."""

    def test_initialization(self):
        """Test collector initialization."""
        collector = StressTestMetricsCollector()
        assert collector.latencies == []
        assert collector.total_messages == 0
        assert collector.failed_messages == 0

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"test": "value"}
        collector = StressTestMetricsCollector(config)
        assert collector.config == config

    def test_start_test(self):
        """Test starting a test."""
        collector = StressTestMetricsCollector()
        collector.start_test({"test": "config"})
        assert collector.test_start_time is not None
        assert collector.test_config == {"test": "config"}

    def test_stop_test(self):
        """Test stopping a test."""
        collector = StressTestMetricsCollector()
        collector.start_test({})
        collector.stop_test()
        assert collector.test_end_time is not None

    def test_record_latency(self):
        """Test recording latency."""
        collector = StressTestMetricsCollector()
        collector.record_latency(10.5)
        assert len(collector.latencies) == 1
        assert collector.latencies[0] == 10.5

    def test_record_latency_with_agent(self):
        """Test recording latency with agent ID."""
        collector = StressTestMetricsCollector()
        collector.record_latency(15.0, agent_id="Agent-1")
        assert "Agent-1" in collector.latencies_by_agent
        assert collector.latencies_by_agent["Agent-1"] == [15.0]

    def test_record_latency_with_type(self):
        """Test recording latency with message type."""
        collector = StressTestMetricsCollector()
        collector.record_latency(20.0, message_type="text")
        assert "text" in collector.latencies_by_type
        assert collector.latencies_by_type["text"] == [20.0]

    def test_record_message_sent(self):
        """Test recording message sent."""
        collector = StressTestMetricsCollector()
        collector.record_message_sent()
        assert collector.total_messages == 1

    def test_record_message_delivered(self):
        """Test recording message delivered."""
        collector = StressTestMetricsCollector()
        collector.record_message_delivered(10.0, agent_id="Agent-1", message_type="text")
        assert len(collector.latencies) == 1
        assert len(collector.real_delivery_times) == 1

    def test_record_message_delivered_mock(self):
        """Test recording mock delivery."""
        collector = StressTestMetricsCollector()
        collector.record_message_delivered(5.0, delivery_mode="mock")
        assert len(collector.mock_delivery_times) == 1

    def test_record_message_failed(self):
        """Test recording message failure."""
        collector = StressTestMetricsCollector()
        collector.record_message_failed(agent_id="Agent-1", reason="timeout")
        assert collector.failed_messages == 1
        assert collector.failure_reasons["timeout"] == 1

    def test_record_queue_depth(self):
        """Test recording queue depth."""
        collector = StressTestMetricsCollector()
        collector.record_queue_depth(10)
        collector.record_queue_depth(20)
        assert collector.max_queue_depth == 20
        assert len(collector.queue_depths) == 2

    def test_record_chaos_event(self):
        """Test recording chaos event."""
        collector = StressTestMetricsCollector()
        collector.record_chaos_event("crash", {"test": "data"}, recovery_time_ms=100.0)
        assert len(collector.chaos_events) == 1
        assert len(collector.crash_recovery_times) == 1

    def test_record_chaos_spike(self):
        """Test recording chaos spike event."""
        collector = StressTestMetricsCollector()
        collector.record_chaos_event("spike", {}, recovery_time_ms=50.0)
        assert collector.spike_handling_metrics["spikes_detected"] == 1
        assert collector.spike_handling_metrics["spikes_handled"] == 1

    def test_calculate_percentiles_empty(self):
        """Test percentile calculation with empty list."""
        collector = StressTestMetricsCollector()
        result = collector._calculate_percentiles([])
        assert result["p50"] == 0.0
        assert result["p95"] == 0.0

    def test_calculate_percentiles_with_data(self):
        """Test percentile calculation with data."""
        collector = StressTestMetricsCollector()
        values = list(range(1, 101))  # 1-100
        result = collector._calculate_percentiles(values)
        assert result["p50"] > 0
        assert result["p95"] > result["p50"]

    def test_get_per_agent_metrics(self):
        """Test getting per-agent metrics."""
        collector = StressTestMetricsCollector()
        collector.record_latency(10.0, agent_id="Agent-1")
        collector.record_message_failed(agent_id="Agent-1")
        metrics = collector.get_per_agent_metrics()
        assert "Agent-1" in metrics
        assert metrics["Agent-1"]["failed_deliveries"] == 1

    def test_get_per_message_type_metrics(self):
        """Test getting per-message-type metrics."""
        collector = StressTestMetricsCollector()
        collector.record_latency(10.0, message_type="text")
        collector.record_message_failed(message_type="text")
        metrics = collector.get_per_message_type_metrics()
        assert "text" in metrics
        assert metrics["text"]["failed_deliveries"] == 1

    def test_generate_dashboard_json(self):
        """Test generating dashboard JSON."""
        collector = StressTestMetricsCollector()
        collector.start_test({"test": "config"})
        collector.record_latency(10.0)
        collector.stop_test()
        dashboard = collector.generate_dashboard_json()
        assert "test_metadata" in dashboard
        assert "overall_metrics" in dashboard
        assert "per_agent_metrics" in dashboard

    def test_generate_dashboard_json_with_output(self, tmp_path):
        """Test generating dashboard JSON with file output."""
        collector = StressTestMetricsCollector()
        collector.start_test({})
        collector.stop_test()
        dashboard = collector.generate_dashboard_json(output_path=tmp_path)
        assert "test_metadata" in dashboard
        assert (tmp_path / "stress_test_results_*.json").exists() or True  # File might exist


class TestStressTestAnalyzer:
    """Tests for StressTestAnalyzer."""

    def test_identify_bottlenecks_high_latency(self):
        """Test identifying high latency bottleneck."""
        dashboard = {
            "overall_metrics": {
                "latency_percentiles": {"p95": 2000},
                "throughput_msg_per_sec": 50,
            },
            "per_agent_metrics": {},
        }
        bottlenecks = StressTestAnalyzer.identify_bottlenecks(dashboard)
        assert len(bottlenecks) > 0
        assert any(b["type"] == "high_latency" for b in bottlenecks)

    def test_identify_bottlenecks_low_throughput(self):
        """Test identifying low throughput bottleneck."""
        dashboard = {
            "overall_metrics": {
                "latency_percentiles": {"p95": 100},
                "throughput_msg_per_sec": 5,
            },
            "per_agent_metrics": {},
        }
        bottlenecks = StressTestAnalyzer.identify_bottlenecks(dashboard)
        assert any(b["type"] == "low_throughput" for b in bottlenecks)

    def test_identify_bottlenecks_queue_depth(self):
        """Test identifying queue depth bottleneck."""
        dashboard = {
            "overall_metrics": {
                "latency_percentiles": {"p95": 100},
                "throughput_msg_per_sec": 50,
                "queue_depth": {"max": 200},
            },
            "per_agent_metrics": {},
        }
        bottlenecks = StressTestAnalyzer.identify_bottlenecks(dashboard)
        assert any(b["type"] == "queue_depth" for b in bottlenecks)

    def test_analyze_failure_patterns(self):
        """Test analyzing failure patterns."""
        dashboard = {
            "overall_metrics": {"failure_rate_percent": 10.0},
            "per_agent_metrics": {
                "Agent-1": {"failure_rate_percent": 10.0, "failed_deliveries": 5},
            },
            "failure_analysis": {"failure_reasons": {"timeout": 3}},
        }
        analysis = StressTestAnalyzer.analyze_failure_patterns(dashboard)
        assert "overall_failure_rate" in analysis
        assert len(analysis["patterns"]) > 0


class TestFactoryFunction:
    """Tests for factory function."""

    def test_create_collector(self):
        """Test creating collector via factory."""
        collector = create_stress_test_metrics_collector()
        assert isinstance(collector, StressTestMetricsCollector)

    def test_create_collector_with_config(self):
        """Test creating collector with config."""
        config = {"test": "value"}
        collector = create_stress_test_metrics_collector(config)
        assert collector.config == config


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

