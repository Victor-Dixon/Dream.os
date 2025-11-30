#!/usr/bin/env python3
"""
Unit Tests for Prediction Validator
====================================
"""

import pytest
from src.core.analytics.processors.prediction.prediction_validator import PredictionValidator


class TestPredictionValidator:
    """Tests for PredictionValidator."""

    def test_initialization(self):
        """Test validator initialization."""
        validator = PredictionValidator()
        assert validator.config == {}
        assert validator.logger is not None

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"test": "value"}
        validator = PredictionValidator(config)
        assert validator.config == config

    def test_validate_input_data_valid(self):
        """Test validating valid input data."""
        validator = PredictionValidator()
        data = {"test": "value", "key": 123}
        result = validator.validate_input_data(data)
        assert result is True

    def test_validate_input_data_not_dict(self):
        """Test validating non-dictionary input."""
        validator = PredictionValidator()
        result = validator.validate_input_data("not a dict")
        assert result is False

    def test_validate_input_data_empty_dict(self):
        """Test validating empty dictionary."""
        validator = PredictionValidator()
        result = validator.validate_input_data({})
        assert result is False

    def test_validate_input_data_list(self):
        """Test validating list input."""
        validator = PredictionValidator()
        result = validator.validate_input_data([])
        assert result is False

    def test_validate_prediction_result_valid(self):
        """Test validating valid prediction result."""
        validator = PredictionValidator()
        result = {
            "prediction_id": "test-123",
            "predicted_value": 42.5,
            "confidence": 0.9,
        }
        assert validator.validate_prediction_result(result) is True

    def test_validate_prediction_result_not_dict(self):
        """Test validating non-dictionary result."""
        validator = PredictionValidator()
        result = validator.validate_prediction_result("not a dict")
        assert result is False

    def test_validate_prediction_result_missing_prediction_id(self):
        """Test validating result missing prediction_id."""
        validator = PredictionValidator()
        result = {
            "predicted_value": 42.5,
            "confidence": 0.9,
        }
        assert validator.validate_prediction_result(result) is False

    def test_validate_prediction_result_missing_predicted_value(self):
        """Test validating result missing predicted_value."""
        validator = PredictionValidator()
        result = {
            "prediction_id": "test-123",
            "confidence": 0.9,
        }
        assert validator.validate_prediction_result(result) is False

    def test_validate_prediction_result_missing_confidence(self):
        """Test validating result missing confidence."""
        validator = PredictionValidator()
        result = {
            "prediction_id": "test-123",
            "predicted_value": 42.5,
        }
        assert validator.validate_prediction_result(result) is False

    def test_validate_prediction_result_with_extra_fields(self):
        """Test validating result with additional fields."""
        validator = PredictionValidator()
        result = {
            "prediction_id": "test-123",
            "predicted_value": 42.5,
            "confidence": 0.9,
            "extra_field": "value",
        }
        assert validator.validate_prediction_result(result) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

