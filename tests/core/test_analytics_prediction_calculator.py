#!/usr/bin/env python3
"""
Unit Tests for Prediction Calculator
=====================================
"""

import pytest
from datetime import datetime
from src.core.analytics.processors.prediction.prediction_calculator import PredictionCalculator


class TestPredictionCalculator:
    """Tests for PredictionCalculator."""

    def test_initialization(self):
        """Test calculator initialization."""
        calculator = PredictionCalculator()
        assert calculator.config == {}
        assert calculator.logger is not None

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"test": "value"}
        calculator = PredictionCalculator(config)
        assert calculator.config == config

    def test_calculate_predicted_value_from_value(self):
        """Test calculating predicted value from 'value' field."""
        calculator = PredictionCalculator()
        data = {"value": 42.5}
        result = calculator.calculate_predicted_value(data)
        assert result == 42.5

    def test_calculate_predicted_value_from_predicted_value(self):
        """Test calculating from 'predicted_value' field."""
        calculator = PredictionCalculator()
        data = {"predicted_value": 100.0}
        result = calculator.calculate_predicted_value(data)
        assert result == 100.0

    def test_calculate_predicted_value_default(self):
        """Test default calculation when no value fields."""
        calculator = PredictionCalculator()
        data = {}
        result = calculator.calculate_predicted_value(data)
        assert result == 0.0

    def test_calculate_confidence_from_data(self):
        """Test calculating confidence from data."""
        calculator = PredictionCalculator()
        data = {"confidence": 0.95}
        result = calculator.calculate_confidence(data)
        assert result == 0.95

    def test_calculate_confidence_default(self):
        """Test default confidence calculation."""
        calculator = PredictionCalculator()
        data = {}
        result = calculator.calculate_confidence(data)
        assert result == 0.8

    def test_create_prediction_result(self):
        """Test creating prediction result."""
        calculator = PredictionCalculator()
        data = {
            "value": 50.0,
            "confidence": 0.9,
            "metadata": {"test": "data"},
        }
        result = calculator.create_prediction_result(data)
        assert "prediction_id" in result
        assert result["predicted_value"] == 50.0
        assert result["confidence"] == 0.9
        assert result["metadata"] == {"test": "data"}
        assert "timestamp" in result

    def test_create_prediction_result_with_prediction_id(self):
        """Test creating result with existing prediction_id."""
        calculator = PredictionCalculator()
        data = {
            "prediction_id": "test-id-123",
            "predicted_value": 75.0,
        }
        result = calculator.create_prediction_result(data)
        assert result["prediction_id"] == "test-id-123"

    def test_create_prediction_result_generates_id(self):
        """Test that prediction_id is generated if not provided."""
        calculator = PredictionCalculator()
        data = {"value": 10.0}
        result = calculator.create_prediction_result(data)
        assert "prediction_id" in result
        assert result["prediction_id"].startswith("pred_")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

