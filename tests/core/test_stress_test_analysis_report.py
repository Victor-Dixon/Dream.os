#!/usr/bin/env python3
"""
Unit Tests for Stress Test Analysis Report
==========================================
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from src.core.stress_test_analysis_report import StressTestAnalysisReport


class TestStressTestAnalysisReport:
    """Tests for StressTestAnalysisReport."""

    def test_initialization(self):
        """Test report generator initialization."""
        report = StressTestAnalysisReport()
        assert report.analyzer is not None
        assert report.logger is not None

    def test_initialization_with_dashboard_data(self):
        """Test initialization with dashboard data."""
        dashboard_data = {"test": "data"}
        report = StressTestAnalysisReport(dashboard_data)
        assert report.analyzer is not None

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_full_report(self, mock_analyzer_class):
        """Test generating full report."""
        # Mock analyzer methods
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.analyze_latency_patterns.return_value = {}
        mock_analyzer.generate_optimization_opportunities.return_value = []
        mock_analyzer.generate_performance_recommendations.return_value = []
        mock_analyzer.generate_dashboard_visualization_data.return_value = {}
        mock_analyzer.dashboard_data = {"overall_metrics": {}}
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        result = report.generate_full_report()
        assert "report_metadata" in result
        assert "executive_summary" in result

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_full_report_with_output_dir(self, mock_analyzer_class, tmp_path):
        """Test generating report with output directory."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.analyze_latency_patterns.return_value = {}
        mock_analyzer.generate_optimization_opportunities.return_value = []
        mock_analyzer.generate_performance_recommendations.return_value = []
        mock_analyzer.generate_dashboard_visualization_data.return_value = {}
        mock_analyzer.dashboard_data = {"overall_metrics": {}}
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        result = report.generate_full_report(output_dir=tmp_path)
        assert "report_metadata" in result

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_executive_summary(self, mock_analyzer_class):
        """Test generating executive summary."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.generate_optimization_opportunities.return_value = []
        mock_analyzer.dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100},
                "throughput_msg_per_sec": 50,
                "failure_rate_percent": 1.0,
            }
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        summary = report._generate_executive_summary()
        assert "test_performance" in summary
        assert "critical_issues" in summary

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_calculate_severity_breakdown(self, mock_analyzer_class):
        """Test calculating severity breakdown."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = [
            {"severity": "high", "type": "test1"},
            {"severity": "medium", "type": "test2"},
        ]
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        breakdown = report._calculate_severity_breakdown()
        assert breakdown["high"]["count"] == 1
        assert breakdown["medium"]["count"] == 1

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_key_findings_high_latency(self, mock_analyzer_class):
        """Test generating key findings for high latency."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 600},
                "throughput_msg_per_sec": 50,
                "failure_rate_percent": 0.5,
            }
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        findings = report._generate_key_findings()
        assert len(findings) > 0
        assert any(f["category"] == "latency" for f in findings)

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_key_findings_low_throughput(self, mock_analyzer_class):
        """Test generating key findings for low throughput."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100},
                "throughput_msg_per_sec": 30,
                "failure_rate_percent": 0.5,
            }
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        findings = report._generate_key_findings()
        assert any(f["category"] == "throughput" for f in findings)

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_key_findings_high_failure_rate(self, mock_analyzer_class):
        """Test generating key findings for high failure rate."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.dashboard_data = {
            "overall_metrics": {
                "latency_percentiles": {"p99": 100},
                "throughput_msg_per_sec": 50,
                "failure_rate_percent": 3.0,
            }
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        findings = report._generate_key_findings()
        assert any(f["category"] == "reliability" for f in findings)

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_action_items(self, mock_analyzer_class):
        """Test generating action items."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = [
            {"severity": "high", "type": "test", "description": "Test bottleneck"},
        ]
        mock_analyzer.generate_optimization_opportunities.return_value = []
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        actions = report._generate_action_items()
        assert len(actions) > 0

    @patch('src.core.stress_test_analysis_report.StressTestMetricsAnalyzer')
    def test_generate_markdown_summary(self, mock_analyzer_class, tmp_path):
        """Test generating markdown summary."""
        mock_analyzer = MagicMock()
        mock_analyzer.identify_bottlenecks.return_value = []
        mock_analyzer.dashboard_data = {"overall_metrics": {}}
        mock_analyzer_class.return_value = mock_analyzer
        
        report = StressTestAnalysisReport()
        report_data = {
            "report_metadata": {"generated_at": "2025-01-01T00:00:00"},
            "executive_summary": {
                "test_performance": {"overall_status": "good"},
            },
            "bottleneck_analysis": {"bottlenecks": []},
            "key_findings": [],
            "action_items": [],
        }
        output_file = tmp_path / "test_summary.md"
        report._generate_markdown_summary(report_data, output_file)
        assert output_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

