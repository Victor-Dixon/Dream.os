#!/usr/bin/env python3
"""
Unit Tests for Pattern Analysis Engine
=======================================

Comprehensive tests for pattern_analysis_engine.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.analytics.intelligence.pattern_analysis_engine import (
    PatternAnalysisEngine,
    create_pattern_analysis_engine
)


class TestPatternAnalysisEngine:
    """Tests for PatternAnalysisEngine."""

    def test_initialization(self):
        """Test engine initialization."""
        engine = PatternAnalysisEngine()
        assert engine.config == {}
        assert engine.analysis_history == []
        assert engine.pattern_extractor is not None
        assert engine.trend_analyzer is not None
        assert engine.anomaly_detector is not None

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"max_history": 50}
        engine = PatternAnalysisEngine(config)
        assert engine.config == config

    def test_analyze_patterns_with_data(self):
        """Test analyzing patterns with valid data."""
        engine = PatternAnalysisEngine()
        data = [
            {"value": 10, "timestamp": "2025-01-01"},
            {"value": 20, "timestamp": "2025-01-02"},
            {"value": 30, "timestamp": "2025-01-03"},
        ]
        result = engine.analyze_patterns(data)
        assert "patterns" in result
        assert "trends" in result
        assert "anomalies" in result
        assert result["data_points"] == 3
        assert "timestamp" in result

    def test_analyze_patterns_empty_data(self):
        """Test analyzing patterns with empty data."""
        engine = PatternAnalysisEngine()
        result = engine.analyze_patterns([])
        assert "error" in result

    def test_analyze_patterns_stores_in_history(self):
        """Test that analysis results are stored in history."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}, {"value": 2}]
        engine.analyze_patterns(data)
        assert len(engine.analysis_history) == 1

    def test_analyze_patterns_exception_handling(self):
        """Test analyze patterns exception handling."""
        engine = PatternAnalysisEngine()
        result = engine.analyze_patterns(None)
        assert "error" in result

    def test_get_analysis_summary_empty(self):
        """Test getting analysis summary with no data."""
        engine = PatternAnalysisEngine()
        summary = engine.get_analysis_summary()
        assert "message" in summary

    def test_get_analysis_summary_with_data(self):
        """Test getting analysis summary with data."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}, {"value": 2}]
        engine.analyze_patterns(data)
        summary = engine.get_analysis_summary()
        assert summary["total_analyses"] == 1
        assert "recent_analysis" in summary

    def test_get_analysis_summary_exception_handling(self):
        """Test analysis summary exception handling."""
        engine = PatternAnalysisEngine()
        engine.analysis_history = None  # Break it
        summary = engine.get_analysis_summary()
        assert "error" in summary

    def test_clear_analysis_history(self):
        """Test clearing analysis history."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}]
        engine.analyze_patterns(data)
        assert len(engine.analysis_history) == 1
        engine.clear_analysis_history()
        assert len(engine.analysis_history) == 0

    def test_get_status(self):
        """Test getting engine status."""
        engine = PatternAnalysisEngine()
        status = engine.get_status()
        assert status["active"] is True
        assert status["analyses_count"] == 0
        assert "timestamp" in status

    def test_get_status_with_analyses(self):
        """Test getting status with analyses."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}]
        engine.analyze_patterns(data)
        status = engine.get_status()
        assert status["analyses_count"] == 1

    def test_extract_patterns_delegation(self):
        """Test that extract_patterns delegates to pattern_extractor."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}]
        with patch.object(engine.pattern_extractor, 'extract_patterns') as mock_extract:
            mock_extract.return_value = {"pattern": "test"}
            result = engine.extract_patterns(data)
            mock_extract.assert_called_once_with(data)
            assert result == {"pattern": "test"}

    def test_analyze_trends_delegation(self):
        """Test that analyze_trends delegates to trend_analyzer."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}]
        with patch.object(engine.trend_analyzer, 'analyze_trends') as mock_analyze:
            mock_analyze.return_value = {"trend": "up"}
            result = engine.analyze_trends(data)
            mock_analyze.assert_called_once_with(data)
            assert result == {"trend": "up"}

    def test_detect_anomalies_delegation(self):
        """Test that detect_anomalies delegates to anomaly_detector."""
        engine = PatternAnalysisEngine()
        data = [{"value": 1}]
        with patch.object(engine.anomaly_detector, 'detect_anomalies') as mock_detect:
            mock_detect.return_value = []
            result = engine.detect_anomalies(data)
            mock_detect.assert_called_once_with(data)
            assert result == []

    def test_detect_outliers_delegation(self):
        """Test that detect_outliers delegates to anomaly_detector."""
        engine = PatternAnalysisEngine()
        values = [1.0, 2.0, 3.0]
        with patch.object(engine.anomaly_detector, 'detect_outliers') as mock_detect:
            mock_detect.return_value = []
            result = engine.detect_outliers(values, "iqr")
            mock_detect.assert_called_once_with(values, "iqr")
            assert result == []

    def test_detect_outliers_default_method(self):
        """Test detect_outliers with default method."""
        engine = PatternAnalysisEngine()
        values = [1.0, 2.0, 3.0]
        with patch.object(engine.anomaly_detector, 'detect_outliers') as mock_detect:
            mock_detect.return_value = []
            result = engine.detect_outliers(values)
            mock_detect.assert_called_once_with(values, "iqr")
            assert result == []

    def test_create_pattern_analysis_engine(self):
        """Test factory function."""
        engine = create_pattern_analysis_engine()
        assert isinstance(engine, PatternAnalysisEngine)

    def test_create_pattern_analysis_engine_with_config(self):
        """Test factory function with config."""
        config = {"test": "value"}
        engine = create_pattern_analysis_engine(config)
        assert isinstance(engine, PatternAnalysisEngine)
        assert engine.config == config

    def test_multiple_analyses_accumulate(self):
        """Test that multiple analyses accumulate in history."""
        engine = PatternAnalysisEngine()
        data1 = [{"value": 1}]
        data2 = [{"value": 2}]
        engine.analyze_patterns(data1)
        engine.analyze_patterns(data2)
        assert len(engine.analysis_history) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.intelligence.pattern_analysis_engine", "--cov-report=term-missing"])

