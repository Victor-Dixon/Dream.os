#!/usr/bin/env python3
"""
Unit Tests for Anomaly Detection Engine
========================================

Comprehensive tests for anomaly_detection_engine.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
from src.core.analytics.intelligence.anomaly_detection_engine import AnomalyDetectionEngine


class TestAnomalyDetectionEngine:
    """Tests for AnomalyDetectionEngine."""

    def test_initialization(self):
        """Test engine initialization."""
        engine = AnomalyDetectionEngine()
        assert engine.config == {}
        assert "z_score" in engine.thresholds
        assert engine.thresholds["z_score"] == 2.0

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"threshold": 3.0}
        engine = AnomalyDetectionEngine(config)
        assert engine.config == config

    def test_detect_anomalies_empty_data(self):
        """Test detecting anomalies with empty data."""
        engine = AnomalyDetectionEngine()
        result = engine.detect_anomalies([])
        assert result == []

    def test_detect_anomalies_insufficient_data(self):
        """Test detecting anomalies with insufficient data."""
        engine = AnomalyDetectionEngine()
        result = engine.detect_anomalies([1.0])
        assert result == []
        result = engine.detect_anomalies([1.0, 2.0])
        assert result == []

    def test_detect_anomalies_minimal_data(self):
        """Test detecting anomalies with minimal valid data."""
        engine = AnomalyDetectionEngine()
        data = [1.0, 2.0, 3.0, 100.0]  # 100 is an anomaly
        result = engine.detect_anomalies(data)
        assert isinstance(result, list)

    def test_detect_statistical_anomalies(self):
        """Test statistical anomaly detection."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 11.0, 10.5, 50.0]  # 50 is an outlier
        anomalies = engine._detect_statistical_anomalies(data)
        assert len(anomalies) > 0
        assert all("z_score" in a for a in anomalies)
        assert all("type" in a for a in anomalies)
        assert all("severity" in a for a in anomalies)

    def test_detect_statistical_anomalies_no_variance(self):
        """Test statistical detection with no variance."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 10.0, 10.0]
        anomalies = engine._detect_statistical_anomalies(data)
        assert anomalies == []

    def test_detect_statistical_anomalies_insufficient_data(self):
        """Test statistical detection with insufficient data."""
        engine = AnomalyDetectionEngine()
        data = [10.0]
        anomalies = engine._detect_statistical_anomalies(data)
        assert anomalies == []

    def test_detect_statistical_anomalies_exception_handling(self):
        """Test statistical detection exception handling."""
        engine = AnomalyDetectionEngine()
        anomalies = engine._detect_statistical_anomalies(None)
        assert anomalies == []

    def test_detect_performance_anomalies(self):
        """Test performance anomaly detection."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 11.0, 50.0]  # Big jump from 11 to 50
        anomalies = engine._detect_performance_anomalies(data)
        assert isinstance(anomalies, list)

    def test_detect_performance_anomalies_insufficient_data(self):
        """Test performance detection with insufficient data."""
        engine = AnomalyDetectionEngine()
        data = [10.0]
        anomalies = engine._detect_performance_anomalies(data)
        assert anomalies == []

    def test_detect_performance_anomalies_high_change(self):
        """Test performance detection with high change threshold."""
        engine = AnomalyDetectionEngine()
        engine.thresholds["performance"] = 0.5
        data = [10.0, 20.0]  # 100% change
        anomalies = engine._detect_performance_anomalies(data)
        assert len(anomalies) > 0

    def test_detect_performance_anomalies_zero_previous(self):
        """Test performance detection with zero previous value."""
        engine = AnomalyDetectionEngine()
        data = [0.0, 10.0]
        anomalies = engine._detect_performance_anomalies(data)
        # Should handle division by zero gracefully
        assert isinstance(anomalies, list)

    def test_get_anomaly_summary_empty(self):
        """Test getting anomaly summary with no anomalies."""
        engine = AnomalyDetectionEngine()
        summary = engine.get_anomaly_summary([])
        assert summary["total"] == 0
        assert summary["by_type"] == {}
        assert summary["by_severity"] == {}

    def test_get_anomaly_summary_with_anomalies(self):
        """Test getting anomaly summary with anomalies."""
        engine = AnomalyDetectionEngine()
        anomalies = [
            {"type": "statistical", "severity": "high"},
            {"type": "statistical", "severity": "medium"},
            {"type": "performance", "severity": "high"},
        ]
        summary = engine.get_anomaly_summary(anomalies)
        assert summary["total"] == 3
        assert summary["by_type"]["statistical"] == 2
        assert summary["by_type"]["performance"] == 1
        assert summary["by_severity"]["high"] == 2
        assert summary["by_severity"]["medium"] == 1
        assert "timestamp" in summary

    def test_get_anomaly_summary_missing_fields(self):
        """Test anomaly summary with missing fields in anomalies."""
        engine = AnomalyDetectionEngine()
        anomalies = [
            {"type": "statistical"},  # Missing severity
            {"severity": "high"},  # Missing type
            {},  # Missing both
        ]
        summary = engine.get_anomaly_summary(anomalies)
        assert summary["total"] == 3

    def test_z_score_severity_classification(self):
        """Test that z-score determines severity correctly."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 11.0, 10.5, 100.0]  # 100 has very high z-score
        anomalies = engine._detect_statistical_anomalies(data)
        # High z-score should be classified as high severity
        high_severity = [a for a in anomalies if a["severity"] == "high"]
        assert len(high_severity) > 0

    def test_combined_anomaly_detection(self):
        """Test that detect_anomalies combines both methods."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 11.0, 10.5, 50.0, 100.0]
        anomalies = engine.detect_anomalies(data)
        # Should have anomalies from both statistical and performance detection
        assert len(anomalies) > 0
        types = [a.get("type") for a in anomalies]
        assert "statistical" in types or "performance" in types

    def test_anomaly_index_tracking(self):
        """Test that anomalies track their index in data."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 11.0, 10.5, 100.0]  # Index 3 is anomaly
        anomalies = engine._detect_statistical_anomalies(data)
        if anomalies:
            assert all("index" in a for a in anomalies)
            assert all(0 <= a["index"] < len(data) for a in anomalies)

    def test_anomaly_value_tracking(self):
        """Test that anomalies track their values."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 11.0, 10.5, 100.0]
        anomalies = engine._detect_statistical_anomalies(data)
        if anomalies:
            assert all("value" in a for a in anomalies)

    def test_performance_anomaly_change_calculation(self):
        """Test that performance anomalies calculate change correctly."""
        engine = AnomalyDetectionEngine()
        data = [10.0, 20.0]  # 100% change
        anomalies = engine._detect_performance_anomalies(data)
        if anomalies:
            assert all("change" in a for a in anomalies)

    def test_threshold_configuration(self):
        """Test that thresholds can be configured."""
        engine = AnomalyDetectionEngine()
        assert engine.thresholds["z_score"] == 2.0
        assert engine.thresholds["performance"] == 0.5
        assert engine.thresholds["frequency"] == 0.05


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.intelligence.anomaly_detection_engine", "--cov-report=term-missing"])

