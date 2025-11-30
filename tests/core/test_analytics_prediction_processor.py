#!/usr/bin/env python3
"""
Unit Tests for Prediction Processor
====================================

Comprehensive tests for prediction_processor.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
from src.core.analytics.processors.prediction_processor import (
    PredictionProcessor,
    create_prediction_processor
)


class TestPredictionProcessor:
    """Tests for PredictionProcessor."""

    def test_initialization(self):
        """Test prediction processor initialization."""
        processor = PredictionProcessor()
        assert processor.config == {}
        assert processor.stats["predictions_generated"] == 0

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"max_predictions": 100}
        processor = PredictionProcessor(config)
        assert processor.config == config

    def test_process_prediction(self):
        """Test processing a prediction."""
        processor = PredictionProcessor()
        data = {"value": 42.5, "confidence": 0.9}
        result = processor.process_prediction(data)
        assert "prediction_id" in result
        assert result["predicted_value"] == 42.5
        assert result["confidence"] == 0.9
        assert processor.stats["predictions_generated"] == 1

    def test_process_prediction_default_values(self):
        """Test processing prediction with default values."""
        processor = PredictionProcessor()
        data = {}
        result = processor.process_prediction(data)
        assert result["predicted_value"] == 0
        assert result["confidence"] == 0.8

    def test_process_prediction_includes_metadata(self):
        """Test that prediction includes metadata."""
        processor = PredictionProcessor()
        data = {"value": 10, "metadata": {"source": "test"}}
        result = processor.process_prediction(data)
        assert "metadata" in result
        assert result["metadata"]["source"] == "test"

    def test_process_prediction_validation_error(self):
        """Test processing prediction with validation error."""
        processor = PredictionProcessor()
        # This will fail validation (invalid confidence > 1)
        data = {"value": 10, "confidence": 1.5}
        result = processor.process_prediction(data)
        assert "error" in result
        assert processor.stats["validation_errors"] == 1

    def test_process_prediction_exception_handling(self):
        """Test exception handling in process_prediction."""
        processor = PredictionProcessor()
        result = processor.process_prediction(None)
        assert "error" in result
        assert processor.stats["processing_errors"] > 0

    def test_validate_prediction_success(self):
        """Test successful prediction validation."""
        processor = PredictionProcessor()
        prediction = {
            "prediction_id": "test",
            "predicted_value": 10,
            "confidence": 0.8
        }
        result = processor._validate_prediction(prediction)
        assert result is True

    def test_validate_prediction_missing_fields(self):
        """Test validation with missing fields."""
        processor = PredictionProcessor()
        prediction = {"prediction_id": "test"}  # Missing required fields
        result = processor._validate_prediction(prediction)
        assert result is False

    def test_validate_prediction_invalid_confidence(self):
        """Test validation with invalid confidence."""
        processor = PredictionProcessor()
        prediction = {
            "prediction_id": "test",
            "predicted_value": 10,
            "confidence": 1.5  # Invalid > 1
        }
        result = processor._validate_prediction(prediction)
        assert result is False

    def test_validate_prediction_negative_confidence(self):
        """Test validation with negative confidence."""
        processor = PredictionProcessor()
        prediction = {
            "prediction_id": "test",
            "predicted_value": 10,
            "confidence": -0.1  # Invalid < 0
        }
        result = processor._validate_prediction(prediction)
        assert result is False

    def test_validate_prediction_exception_handling(self):
        """Test exception handling in validation."""
        processor = PredictionProcessor()
        result = processor._validate_prediction(None)
        assert result is False

    def test_batch_process_predictions(self):
        """Test batch processing predictions."""
        processor = PredictionProcessor()
        predictions = [
            {"value": 10, "confidence": 0.8},
            {"value": 20, "confidence": 0.9},
            {"value": 30, "confidence": 0.7},
        ]
        results = processor.batch_process_predictions(predictions)
        assert len(results) == 3
        assert processor.stats["predictions_generated"] == 3

    def test_batch_process_predictions_empty(self):
        """Test batch processing with empty list."""
        processor = PredictionProcessor()
        results = processor.batch_process_predictions([])
        assert results == []

    def test_batch_process_predictions_exception_handling(self):
        """Test exception handling in batch processing."""
        processor = PredictionProcessor()
        results = processor.batch_process_predictions(None)
        assert isinstance(results, list)

    def test_get_processing_stats(self):
        """Test getting processing statistics."""
        processor = PredictionProcessor()
        processor.process_prediction({"value": 10, "confidence": 0.8})
        stats = processor.get_processing_stats()
        assert stats["predictions_generated"] == 1
        assert "success_rate" in stats

    def test_get_processing_stats_with_errors(self):
        """Test getting stats with errors."""
        processor = PredictionProcessor()
        processor.process_prediction({"value": 10, "confidence": 1.5})  # Invalid
        stats = processor.get_processing_stats()
        assert stats["validation_errors"] > 0

    def test_reset_stats(self):
        """Test resetting statistics."""
        processor = PredictionProcessor()
        processor.process_prediction({"value": 10, "confidence": 0.8})
        assert processor.stats["predictions_generated"] == 1
        processor.reset_stats()
        assert processor.stats["predictions_generated"] == 0

    def test_get_status(self):
        """Test getting processor status."""
        processor = PredictionProcessor()
        status = processor.get_status()
        assert "active" in status
        assert status["active"] is True
        assert "stats" in status

    def test_create_prediction_processor(self):
        """Test factory function."""
        processor = create_prediction_processor()
        assert isinstance(processor, PredictionProcessor)

    def test_create_prediction_processor_with_config(self):
        """Test factory function with config."""
        config = {"test": "value"}
        processor = create_prediction_processor(config)
        assert processor.config == config


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.processors.prediction_processor", "--cov-report=term-missing"])

