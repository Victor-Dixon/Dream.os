#!/usr/bin/env python3
"""
Unit Tests for Prediction Analyzer
==================================

Comprehensive tests for prediction_analyzer.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import pytest
from src.core.analytics.processors.prediction.prediction_analyzer import PredictionAnalyzer


class TestPredictionAnalyzer:
    """Tests for PredictionAnalyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = PredictionAnalyzer()
        assert analyzer.config == {}

    def test_initialization_with_config(self):
        """Test analyzer initialization with config."""
        config = {"threshold": 0.8}
        analyzer = PredictionAnalyzer(config)
        assert analyzer.config == config

    def test_analyze_prediction(self):
        """Test analyze_prediction method."""
        analyzer = PredictionAnalyzer()
        prediction = {
            "prediction_id": "pred_001",
            "confidence": 0.75,
            "value": 100
        }
        result = analyzer.analyze_prediction(prediction)
        assert "prediction_id" in result
        assert result["prediction_id"] == "pred_001"
        assert "analysis_timestamp" in result
        assert "confidence_level" in result
        assert "quality_score" in result
        assert "recommendations" in result

    def test_analyze_prediction_missing_id(self):
        """Test analyze_prediction with missing prediction_id."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.5}
        result = analyzer.analyze_prediction(prediction)
        assert result["prediction_id"] == "unknown"

    def test_analyze_prediction_high_confidence(self):
        """Test analyze_prediction with high confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {
            "prediction_id": "pred_high",
            "confidence": 0.9
        }
        result = analyzer.analyze_prediction(prediction)
        assert result["confidence_level"] in ["very_high", "high"]
        assert result["quality_score"] > 0

    def test_analyze_prediction_low_confidence(self):
        """Test analyze_prediction with low confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {
            "prediction_id": "pred_low",
            "confidence": 0.3
        }
        result = analyzer.analyze_prediction(prediction)
        assert result["confidence_level"] == "low"
        assert len(result["recommendations"]) > 0

    def test_analyze_prediction_medium_confidence(self):
        """Test analyze_prediction with medium confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {
            "prediction_id": "pred_medium",
            "confidence": 0.6
        }
        result = analyzer.analyze_prediction(prediction)
        assert result["confidence_level"] in ["medium", "high"]

    def test_calculate_quality_score(self):
        """Test _calculate_quality_score method."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.8}
        score = analyzer._calculate_quality_score(prediction)
        assert 0.0 <= score <= 1.0
        assert score > 0

    def test_calculate_quality_score_high_confidence(self):
        """Test quality score with high confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.95}
        score = analyzer._calculate_quality_score(prediction)
        assert score <= 1.0  # Should be capped at 1.0

    def test_calculate_quality_score_low_confidence(self):
        """Test quality score with low confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.2}
        score = analyzer._calculate_quality_score(prediction)
        assert score >= 0.0

    def test_calculate_quality_score_missing_confidence(self):
        """Test quality score with missing confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {}
        score = analyzer._calculate_quality_score(prediction)
        assert 0.0 <= score <= 1.0

    def test_generate_recommendations_low_confidence(self):
        """Test recommendations for low confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.3}
        recommendations = analyzer._generate_recommendations(prediction)
        assert len(recommendations) > 0
        assert any("more data" in rec.lower() or "review" in rec.lower() for rec in recommendations)

    def test_generate_recommendations_medium_confidence(self):
        """Test recommendations for medium confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.6}
        recommendations = analyzer._generate_recommendations(prediction)
        assert len(recommendations) > 0

    def test_generate_recommendations_high_confidence(self):
        """Test recommendations for high confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {"confidence": 0.8}
        recommendations = analyzer._generate_recommendations(prediction)
        assert len(recommendations) > 0
        assert any("good" in rec.lower() for rec in recommendations)

    def test_generate_recommendations_missing_confidence(self):
        """Test recommendations with missing confidence."""
        analyzer = PredictionAnalyzer()
        prediction = {}
        recommendations = analyzer._generate_recommendations(prediction)
        assert len(recommendations) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.processors.prediction.prediction_analyzer", "--cov-report=term-missing"])

