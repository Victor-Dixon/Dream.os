#!/usr/bin/env python3
"""
Unit Tests for Pattern Extractor
=================================

Comprehensive tests for pattern_extractor.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-29
"""

import pytest
from src.core.analytics.intelligence.pattern_analysis.pattern_extractor import PatternExtractor


class TestPatternExtractor:
    """Tests for PatternExtractor."""

    def test_initialization(self):
        """Test pattern extractor initialization."""
        extractor = PatternExtractor()
        assert extractor is not None

    def test_extract_patterns_empty_data(self):
        """Test pattern extraction with empty data."""
        extractor = PatternExtractor()
        result = extractor.extract_patterns([])
        assert "error" in result
        assert result["error"] == "No data provided"

    def test_extract_patterns_with_data(self):
        """Test pattern extraction with valid data."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 8},
            {"value": 30, "count": 12},
        ]
        result = extractor.extract_patterns(data)
        assert "frequency_patterns" in result
        assert "value_patterns" in result
        assert "temporal_patterns" in result

    def test_extract_frequency_patterns(self):
        """Test frequency pattern extraction."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 8},
            {"value": 30, "count": 12},
        ]
        patterns = extractor._extract_frequency_patterns(data)
        assert "most_common_keys" in patterns
        assert "total_keys" in patterns
        assert "unique_keys" in patterns

    def test_extract_frequency_patterns_most_common(self):
        """Test most common keys extraction."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 8},
            {"value": 30, "count": 12},
        ]
        patterns = extractor._extract_frequency_patterns(data)
        assert len(patterns["most_common_keys"]) <= 5

    def test_extract_value_patterns(self):
        """Test value pattern extraction."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 8},
            {"value": 30, "count": 12},
        ]
        patterns = extractor._extract_value_patterns(data)
        assert "mean" in patterns
        assert "median" in patterns
        assert "min" in patterns
        assert "max" in patterns

    def test_extract_value_patterns_no_numeric(self):
        """Test value pattern extraction with no numeric values."""
        extractor = PatternExtractor()
        data = [
            {"text": "value1", "description": "desc1"},
            {"text": "value2", "description": "desc2"},
        ]
        patterns = extractor._extract_value_patterns(data)
        assert "message" in patterns
        assert "No numeric values found" in patterns["message"]

    def test_extract_value_patterns_statistics(self):
        """Test value pattern statistics calculation."""
        extractor = PatternExtractor()
        data = [{"value": i} for i in range(10, 20)]
        patterns = extractor._extract_value_patterns(data)
        assert patterns["mean"] > 0
        assert patterns["min"] == 10
        assert patterns["max"] == 19

    def test_extract_temporal_patterns(self):
        """Test temporal pattern extraction."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "timestamp": "2025-01-01"},
            {"value": 20, "date": "2025-01-02"},
        ]
        patterns = extractor._extract_temporal_patterns(data)
        assert "timestamp_fields" in patterns
        assert "has_temporal_data" in patterns

    def test_extract_temporal_patterns_with_timestamps(self):
        """Test temporal pattern extraction with timestamp fields."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "timestamp": "2025-01-01"},
            {"value": 20, "timestamp": "2025-01-02"},
        ]
        patterns = extractor._extract_temporal_patterns(data)
        assert patterns["has_temporal_data"] is True

    def test_extract_temporal_patterns_no_timestamps(self):
        """Test temporal pattern extraction without timestamp fields."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 8},
        ]
        patterns = extractor._extract_temporal_patterns(data)
        assert patterns["has_temporal_data"] is False

    def test_extract_patterns_exception_handling(self):
        """Test exception handling in pattern extraction."""
        extractor = PatternExtractor()
        result = extractor.extract_patterns(None)
        assert "error" in result

    def test_extract_frequency_patterns_exception(self):
        """Test exception handling in frequency pattern extraction."""
        extractor = PatternExtractor()
        patterns = extractor._extract_frequency_patterns(None)
        assert isinstance(patterns, dict)

    def test_extract_value_patterns_exception(self):
        """Test exception handling in value pattern extraction."""
        extractor = PatternExtractor()
        patterns = extractor._extract_value_patterns(None)
        assert isinstance(patterns, dict)

    def test_extract_temporal_patterns_exception(self):
        """Test exception handling in temporal pattern extraction."""
        extractor = PatternExtractor()
        patterns = extractor._extract_temporal_patterns(None)
        assert isinstance(patterns, dict)

    def test_extract_patterns_comprehensive(self):
        """Test comprehensive pattern extraction."""
        extractor = PatternExtractor()
        data = [
            {"value": 10, "count": 5, "timestamp": "2025-01-01"},
            {"value": 20, "count": 8, "timestamp": "2025-01-02"},
            {"value": 30, "count": 12, "timestamp": "2025-01-03"},
        ]
        result = extractor.extract_patterns(data)
        assert "frequency_patterns" in result
        assert "value_patterns" in result
        assert "temporal_patterns" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.intelligence.pattern_analysis.pattern_extractor", "--cov-report=term-missing"])

