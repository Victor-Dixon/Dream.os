"""
Unit Tests for Stress Test Metrics Analyzer
===========================================
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
from src.core.stress_test_metrics_analyzer import StressTestMetricsAnalyzer


class TestStressTestMetricsAnalyzer:
    """Tests for StressTestMetricsAnalyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = StressTestMetricsAnalyzer()
        assert analyzer.dashboard_data == {}
        assert analyzer.logger is not None

    def test_initialization_with_dashboard_data(self):
        """Test initialization with dashboard data."""
        dashboard_data = {"test": "data"}
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        assert analyzer.dashboard_data == dashboard_data

    def test_load_dashboard_from_file(self, tmp_path):
        """Test loading dashboard from file."""
        dashboard_file = tmp_path / "dashboard.json"
        dashboard_data = {"test": "data"}
        import json
        dashboard_file.write_text(json.dumps(dashboard_data))
        
        analyzer = StressTestMetricsAnalyzer()
        result = analyzer.load_dashboard_from_file(dashboard_file)
        assert result == dashboard_data
        assert analyzer.dashboard_data == dashboard_data

    def test_load_dashboard_from_file_not_found(self):
        """Test loading dashboard from non-existent file."""
        analyzer = StressTestMetricsAnalyzer()
        result = analyzer.load_dashboard_from_file(Path("nonexistent.json"))
        assert result == {}

    def test_analyze_latency_patterns(self):
        """Test analyzing latency patterns."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {
                    "p50": 50.0,
                    "p95": 100.0,
                    "p99": 200.0,
                }
            }
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        patterns = analyzer.analyze_latency_patterns()
        assert "p50" in patterns
        assert "p95" in patterns
        assert "p99" in patterns

    def test_identify_bottlenecks_high_latency(self):
        """Test identifying high latency bottleneck."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 600.0},
                "throughput_msg_per_sec": 50.0,
                "failure_rate_percent": 0.5,
                "queue_depth": {"max": 50},
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        bottlenecks = analyzer.identify_bottlenecks()
        assert len(bottlenecks) > 0
        assert any(b["type"] == "high_latency" for b in bottlenecks)

    def test_identify_bottlenecks_low_throughput(self):
        """Test identifying low throughput bottleneck."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100.0},
                "throughput_msg_per_sec": 30.0,
                "failure_rate_percent": 0.5,
                "queue_depth": {"max": 50},
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        bottlenecks = analyzer.identify_bottlenecks()
        assert any(b["type"] == "low_throughput" for b in bottlenecks)

    def test_identify_bottlenecks_high_failure_rate(self):
        """Test identifying high failure rate bottleneck."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100.0},
                "throughput_msg_per_sec": 50.0,
                "failure_rate_percent": 2.0,
                "queue_depth": {"max": 50},
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        bottlenecks = analyzer.identify_bottlenecks()
        assert any(b["type"] == "high_failure_rate" for b in bottlenecks)

    def test_identify_bottlenecks_queue_depth(self):
        """Test identifying queue depth bottleneck."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100.0},
                "throughput_msg_per_sec": 50.0,
                "failure_rate_percent": 0.5,
                "queue_depth": {"max": 150},
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        bottlenecks = analyzer.identify_bottlenecks()
        assert any(b["type"] == "queue_depth" for b in bottlenecks)

    def test_generate_optimization_opportunities(self):
        """Test generating optimization opportunities."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 600.0},
                "throughput_msg_per_sec": 30.0,
                "failure_rate_percent": 2.0,
                "queue_depth": {"max": 150},
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        opportunities = analyzer.generate_optimization_opportunities()
        assert len(opportunities) > 0
        assert all("category" in opp for opp in opportunities)

    def test_generate_performance_recommendations(self):
        """Test generating performance recommendations."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100.0},
                "throughput_msg_per_sec": 50.0,
                "failure_rate_percent": 0.5,
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        recommendations = analyzer.generate_performance_recommendations()
        assert "summary" in recommendations
        assert "bottlenecks" in recommendations

    def test_generate_dashboard_visualization_data(self):
        """Test generating dashboard visualization data."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p50": 50.0, "p95": 100.0, "p99": 200.0},
                "throughput_msg_per_sec": 50.0,
                "failure_rate_percent": 0.5,
                "queue_depth": {"max": 50, "avg": 25, "current": 10},
            },
            "per_agent_metrics": {
                "Agent-1": {"latency_percentiles": {"p99": 150.0}, "failure_rate_percent": 0.0},
            },
            "per_message_type_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        viz_data = analyzer.generate_dashboard_visualization_data()
        assert "charts" in viz_data
        assert "summary_metrics" in viz_data

    def test_assess_tail_latency(self):
        """Test assessing tail latency severity."""
        analyzer = StressTestMetricsAnalyzer()
        latency = {"p50": 50.0, "p99": 500.0}
        severity = analyzer._assess_tail_latency(latency)
        assert severity in ["none", "low", "medium", "high", "severe"]

    def test_analyze_latency_distribution(self):
        """Test analyzing latency distribution."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p50": 50.0, "p95": 100.0, "p99": 200.0},
            }
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        distribution = analyzer._analyze_latency_distribution()
        assert "spread" in distribution
        assert "consistency" in distribution

    def test_detect_latency_anomalies(self):
        """Test detecting latency anomalies."""
        analyzer = StressTestMetricsAnalyzer()
        latency = {"p99": 1200.0, "p95": 600.0}
        anomalies = analyzer._detect_latency_anomalies(latency)
        assert len(anomalies) > 0

    def test_generate_key_insights(self):
        """Test generating key insights."""
        dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 600.0},
                "failure_rate_percent": 2.0,
            },
            "per_agent_metrics": {},
        }
        analyzer = StressTestMetricsAnalyzer(dashboard_data)
        insights = analyzer._generate_key_insights()
        assert isinstance(insights, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


