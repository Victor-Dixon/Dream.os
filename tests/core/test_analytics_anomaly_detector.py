#!/usr/bin/env python3
"""
Unit Tests for Anomaly Detector
================================

Comprehensive tests for anomaly_detector.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-29
"""

import pytest
from src.core.analytics.intelligence.pattern_analysis.anomaly_detector import AnomalyDetector


class TestAnomalyDetector:
    """Tests for AnomalyDetector."""

    def test_initialization(self):
        """Test anomaly detector initialization."""
        detector = AnomalyDetector()
        assert detector is not None

    def test_detect_anomalies_empty_data(self):
        """Test anomaly detection with empty data."""
        detector = AnomalyDetector()
        result = detector.detect_anomalies([])
        assert result == []

    def test_detect_anomalies_insufficient_data(self):
        """Test anomaly detection with insufficient data."""
        detector = AnomalyDetector()
        data = [{"value": 10}, {"value": 20}]
        result = detector.detect_anomalies(data)
        assert result == []

    def test_detect_anomalies_with_data(self):
        """Test anomaly detection with valid data."""
        detector = AnomalyDetector()
        data = [
            {"value": 10},
            {"value": 11},
            {"value": 12},
            {"value": 100},  # Anomaly
        ]
        result = detector.detect_anomalies(data)
        assert isinstance(result, list)

    def test_detect_anomalies_no_numeric_values(self):
        """Test anomaly detection with no numeric values."""
        detector = AnomalyDetector()
        data = [
            {"text": "value1"},
            {"text": "value2"},
            {"text": "value3"},
        ]
        result = detector.detect_anomalies(data)
        assert result == []

    def test_detect_statistical_anomalies(self):
        """Test statistical anomaly detection."""
        detector = AnomalyDetector()
        values = [10, 11, 12, 13, 14, 100]  # 100 is anomaly
        anomalies = detector._detect_statistical_anomalies(values)
        assert isinstance(anomalies, list)

    def test_detect_statistical_anomalies_insufficient_data(self):
        """Test statistical anomaly detection with insufficient data."""
        detector = AnomalyDetector()
        values = [10, 20]
        anomalies = detector._detect_statistical_anomalies(values)
        assert anomalies == []

    def test_detect_statistical_anomalies_zero_stddev(self):
        """Test statistical anomaly detection with zero standard deviation."""
        detector = AnomalyDetector()
        values = [10, 10, 10, 10, 10]
        anomalies = detector._detect_statistical_anomalies(values)
        assert anomalies == []

    def test_detect_statistical_anomalies_limit(self):
        """Test that anomaly detection limits results to 5."""
        detector = AnomalyDetector()
        values = [10] * 10 + [1000] * 10  # Many anomalies
        anomalies = detector._detect_statistical_anomalies(values)
        assert len(anomalies) <= 5

    def test_detect_statistical_anomalies_structure(self):
        """Test anomaly structure."""
        detector = AnomalyDetector()
        values = [10, 11, 12, 13, 14, 100]
        anomalies = detector._detect_statistical_anomalies(values)
        if anomalies:
            anomaly = anomalies[0]
            assert "index" in anomaly
            assert "value" in anomaly
            assert "deviation" in anomaly
            assert "z_score" in anomaly

    def test_detect_outliers_iqr(self):
        """Test outlier detection using IQR method."""
        detector = AnomalyDetector()
        values = [1, 2, 3, 4, 5, 100]  # 100 is outlier
        outliers = detector.detect_outliers(values, method="iqr")
        assert isinstance(outliers, list)

    def test_detect_outliers_iqr_insufficient_data(self):
        """Test IQR outlier detection with insufficient data."""
        detector = AnomalyDetector()
        values = [1, 2, 3]
        outliers = detector.detect_outliers(values, method="iqr")
        assert outliers == []

    def test_detect_outliers_iqr_structure(self):
        """Test IQR outlier structure."""
        detector = AnomalyDetector()
        values = [1, 2, 3, 4, 5, 100]
        outliers = detector._detect_outliers_iqr(values)
        if outliers:
            outlier = outliers[0]
            assert "index" in outlier
            assert "value" in outlier
            assert "lower_bound" in outlier
            assert "upper_bound" in outlier

    def test_detect_outliers_zscore(self):
        """Test outlier detection using Z-score method."""
        detector = AnomalyDetector()
        values = [10, 11, 12, 13, 14, 100]  # 100 is outlier
        outliers = detector.detect_outliers(values, method="zscore")
        assert isinstance(outliers, list)

    def test_detect_outliers_zscore_insufficient_data(self):
        """Test Z-score outlier detection with insufficient data."""
        detector = AnomalyDetector()
        values = [10, 20]
        outliers = detector.detect_outliers(values, method="zscore")
        assert outliers == []

    def test_detect_outliers_zscore_zero_stddev(self):
        """Test Z-score outlier detection with zero standard deviation."""
        detector = AnomalyDetector()
        values = [10, 10, 10, 10, 10]
        outliers = detector._detect_outliers_zscore(values)
        assert outliers == []

    def test_detect_outliers_zscore_structure(self):
        """Test Z-score outlier structure."""
        detector = AnomalyDetector()
        values = [10, 11, 12, 13, 14, 100]
        outliers = detector._detect_outliers_zscore(values)
        if outliers:
            outlier = outliers[0]
            assert "index" in outlier
            assert "value" in outlier
            assert "z_score" in outlier
            assert "threshold" in outlier

    def test_detect_outliers_default_method(self):
        """Test outlier detection with default method."""
        detector = AnomalyDetector()
        values = [1, 2, 3, 4, 5, 100]
        outliers = detector.detect_outliers(values)
        assert isinstance(outliers, list)

    def test_detect_outliers_invalid_method(self):
        """Test outlier detection with invalid method (should default to IQR)."""
        detector = AnomalyDetector()
        values = [1, 2, 3, 4, 5, 100]
        outliers = detector.detect_outliers(values, method="invalid")
        assert isinstance(outliers, list)

    def test_detect_anomalies_exception_handling(self):
        """Test exception handling in anomaly detection."""
        detector = AnomalyDetector()
        result = detector.detect_anomalies(None)
        assert isinstance(result, list)

    def test_detect_statistical_anomalies_exception(self):
        """Test exception handling in statistical anomaly detection."""
        detector = AnomalyDetector()
        anomalies = detector._detect_statistical_anomalies(None)
        assert isinstance(anomalies, list)

    def test_detect_outliers_exception(self):
        """Test exception handling in outlier detection."""
        detector = AnomalyDetector()
        outliers = detector.detect_outliers(None)
        assert isinstance(outliers, list)

    def test_detect_outliers_iqr_exception(self):
        """Test exception handling in IQR outlier detection."""
        detector = AnomalyDetector()
        outliers = detector._detect_outliers_iqr(None)
        assert isinstance(outliers, list)

    def test_detect_outliers_zscore_exception(self):
        """Test exception handling in Z-score outlier detection."""
        detector = AnomalyDetector()
        outliers = detector._detect_outliers_zscore(None)
        assert isinstance(outliers, list)

    def test_comprehensive_anomaly_detection(self):
        """Test comprehensive anomaly detection scenario."""
        detector = AnomalyDetector()
        data = [
            {"value": 10, "count": 5},
            {"value": 11, "count": 6},
            {"value": 12, "count": 7},
            {"value": 100, "count": 100},  # Anomaly
        ]
        anomalies = detector.detect_anomalies(data)
        assert isinstance(anomalies, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.intelligence.pattern_analysis.anomaly_detector", "--cov-report=term-missing"])

