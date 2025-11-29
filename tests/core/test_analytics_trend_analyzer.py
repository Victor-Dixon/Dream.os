#!/usr/bin/env python3
"""
Unit Tests for Trend Analyzer
==============================

Comprehensive tests for trend_analyzer.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
import statistics
from src.core.analytics.intelligence.pattern_analysis.trend_analyzer import TrendAnalyzer


class TestTrendAnalyzer:
    """Tests for TrendAnalyzer."""

    def test_initialization(self):
        """Test trend analyzer initialization."""
        analyzer = TrendAnalyzer()
        assert analyzer is not None

    def test_analyze_trends_empty_data(self):
        """Test analyzing trends with empty data."""
        analyzer = TrendAnalyzer()
        result = analyzer.analyze_trends([])
        assert "error" in result
        assert result["error"] == "No data provided"

    def test_analyze_trends_single_item(self):
        """Test analyzing trends with single data item."""
        analyzer = TrendAnalyzer()
        data = [{"value": 10}]
        result = analyzer.analyze_trends(data)
        assert "message" in result
        assert "Insufficient data" in result["message"]

    def test_analyze_trends_insufficient_numeric(self):
        """Test analyzing trends with insufficient numeric values."""
        analyzer = TrendAnalyzer()
        data = [{"text": "value"}, {"text": "value2"}]
        result = analyzer.analyze_trends(data)
        assert "message" in result
        assert "Insufficient data" in result["message"]

    def test_analyze_trends_increasing(self):
        """Test analyzing increasing trend."""
        analyzer = TrendAnalyzer()
        data = [
            {"value": 10, "timestamp": "2025-01-01"},
            {"value": 20, "timestamp": "2025-01-02"},
            {"value": 30, "timestamp": "2025-01-03"},
            {"value": 40, "timestamp": "2025-01-04"},
        ]
        result = analyzer.analyze_trends(data)
        assert "direction" in result
        assert result["direction"] == "increasing"
        assert "strength" in result
        assert "slope" in result
        assert result["slope"] > 0

    def test_analyze_trends_decreasing(self):
        """Test analyzing decreasing trend."""
        analyzer = TrendAnalyzer()
        data = [
            {"value": 40},
            {"value": 30},
            {"value": 20},
            {"value": 10},
        ]
        result = analyzer.analyze_trends(data)
        assert result["direction"] == "decreasing"
        assert result["slope"] < 0

    def test_analyze_trends_stable(self):
        """Test analyzing stable trend."""
        analyzer = TrendAnalyzer()
        data = [
            {"value": 10},
            {"value": 10.1},
            {"value": 9.9},
            {"value": 10},
        ]
        result = analyzer.analyze_trends(data)
        assert result["direction"] == "stable"

    def test_analyze_trends_includes_metadata(self):
        """Test that trend analysis includes metadata."""
        analyzer = TrendAnalyzer()
        data = [{"value": 10}, {"value": 20}, {"value": 30}]
        result = analyzer.analyze_trends(data)
        assert "data_points" in result
        assert "mean" in result
        assert "median" in result
        assert result["data_points"] == 3

    def test_analyze_trends_exception_handling(self):
        """Test exception handling in analyze_trends."""
        analyzer = TrendAnalyzer()
        result = analyzer.analyze_trends(None)
        assert "error" in result

    def test_calculate_trend_direction_increasing(self):
        """Test calculating increasing trend direction."""
        analyzer = TrendAnalyzer()
        values = [10.0, 20.0, 30.0, 40.0]
        direction = analyzer._calculate_trend_direction(values)
        assert direction == "increasing"

    def test_calculate_trend_direction_decreasing(self):
        """Test calculating decreasing trend direction."""
        analyzer = TrendAnalyzer()
        values = [40.0, 30.0, 20.0, 10.0]
        direction = analyzer._calculate_trend_direction(values)
        assert direction == "decreasing"

    def test_calculate_trend_direction_stable(self):
        """Test calculating stable trend direction."""
        analyzer = TrendAnalyzer()
        values = [10.0, 10.0, 10.0, 10.0]
        direction = analyzer._calculate_trend_direction(values)
        assert direction == "stable"

    def test_calculate_trend_direction_insufficient_data(self):
        """Test trend direction with insufficient data."""
        analyzer = TrendAnalyzer()
        values = [10.0]
        direction = analyzer._calculate_trend_direction(values)
        assert direction == "stable"

    def test_calculate_trend_direction_exception_handling(self):
        """Test exception handling in trend direction calculation."""
        analyzer = TrendAnalyzer()
        direction = analyzer._calculate_trend_direction(None)
        assert direction == "unknown"

    def test_calculate_trend_strength(self):
        """Test calculating trend strength."""
        analyzer = TrendAnalyzer()
        values = [10.0, 20.0, 30.0, 40.0]
        strength = analyzer._calculate_trend_strength(values)
        assert 0.0 <= strength <= 1.0

    def test_calculate_trend_strength_insufficient_data(self):
        """Test trend strength with insufficient data."""
        analyzer = TrendAnalyzer()
        values = [10.0, 20.0]
        strength = analyzer._calculate_trend_strength(values)
        assert strength == 0.0

    def test_calculate_trend_strength_zero_mean(self):
        """Test trend strength with zero mean."""
        analyzer = TrendAnalyzer()
        values = [0.0, 0.0, 0.0]
        strength = analyzer._calculate_trend_strength(values)
        assert strength == 0.0

    def test_calculate_trend_strength_exception_handling(self):
        """Test exception handling in trend strength calculation."""
        analyzer = TrendAnalyzer()
        strength = analyzer._calculate_trend_strength(None)
        assert strength == 0.0

    def test_calculate_trend_slope(self):
        """Test calculating trend slope."""
        analyzer = TrendAnalyzer()
        values = [10.0, 20.0, 30.0, 40.0]
        slope = analyzer._calculate_trend_slope(values)
        assert slope > 0

    def test_calculate_trend_slope_negative(self):
        """Test calculating negative trend slope."""
        analyzer = TrendAnalyzer()
        values = [40.0, 30.0, 20.0, 10.0]
        slope = analyzer._calculate_trend_slope(values)
        assert slope < 0

    def test_calculate_trend_slope_zero(self):
        """Test calculating zero trend slope."""
        analyzer = TrendAnalyzer()
        values = [10.0, 10.0, 10.0]
        slope = analyzer._calculate_trend_slope(values)
        assert slope == 0.0

    def test_calculate_trend_slope_insufficient_data(self):
        """Test trend slope with insufficient data."""
        analyzer = TrendAnalyzer()
        values = [10.0]
        slope = analyzer._calculate_trend_slope(values)
        assert slope == 0.0

    def test_calculate_trend_slope_exception_handling(self):
        """Test exception handling in trend slope calculation."""
        analyzer = TrendAnalyzer()
        slope = analyzer._calculate_trend_slope(None)
        assert slope == 0.0

    def test_mixed_data_types(self):
        """Test analyzing trends with mixed data types."""
        analyzer = TrendAnalyzer()
        data = [
            {"value": 10, "text": "a"},
            {"value": 20, "text": "b"},
            {"value": 30, "text": "c"},
        ]
        result = analyzer.analyze_trends(data)
        assert "direction" in result
        assert result["direction"] == "increasing"

    def test_multiple_numeric_fields(self):
        """Test analyzing trends with multiple numeric fields."""
        analyzer = TrendAnalyzer()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 10},
            {"value": 30, "count": 15},
        ]
        result = analyzer.analyze_trends(data)
        assert "direction" in result
        # Should analyze all numeric values combined


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.intelligence.pattern_analysis.trend_analyzer", "--cov-report=term-missing"])

