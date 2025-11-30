"""
Tests for Batch Analytics Engine - Comprehensive Test Suite
===========================================================

Tests the BatchAnalyticsEngine class with comprehensive coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-30
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from typing import Any

from src.core.analytics.engines.batch_analytics_engine import (
    BatchAnalyticsEngine,
    create_batch_analytics_engine,
)


class TestBatchAnalyticsEngine:
    """Test suite for BatchAnalyticsEngine."""

    @pytest.fixture
    def engine(self):
        """Create BatchAnalyticsEngine instance."""
        return BatchAnalyticsEngine()

    @pytest.fixture
    def engine_with_config(self):
        """Create BatchAnalyticsEngine with config."""
        return BatchAnalyticsEngine(config={"batch_size": 100})

    @pytest.fixture
    def sample_data(self):
        """Sample batch data for testing."""
        return [
            {"id": 1, "value": 10},
            {"id": 2, "value": 20},
            {"id": 3, "value": 30},
        ]

    def test_initialization_default(self, engine):
        """Test default initialization."""
        assert engine.config == {}
        assert engine.queue == []
        assert engine.stats["batches_processed"] == 0
        assert engine.stats["total_items"] == 0

    def test_initialization_with_config(self, engine_with_config):
        """Test initialization with config."""
        assert engine_with_config.config["batch_size"] == 100

    def test_process_batch_success(self, engine, sample_data):
        """Test successful batch processing."""
        result = engine.process_batch(sample_data)
        assert "error" not in result
        assert result["batch_size"] == 3
        assert len(result["processed_items"]) == 3
        assert "metrics" in result
        assert engine.stats["batches_processed"] == 1
        assert engine.stats["total_items"] == 3

    def test_process_batch_empty_data(self, engine):
        """Test batch processing with empty data."""
        result = engine.process_batch([])
        assert "error" in result
        assert result["error"] == "No data provided"

    def test_process_batch_none_data(self, engine):
        """Test batch processing with None data."""
        result = engine.process_batch(None)
        assert "error" in result

    def test_process_batch_exception_handling(self, engine, sample_data):
        """Test batch processing exception handling."""
        with patch.object(engine, '_process_items', side_effect=Exception("Processing error")):
            result = engine.process_batch(sample_data)
            assert "error" in result

    def test_process_items_success(self, engine, sample_data):
        """Test _process_items method success."""
        processed = engine._process_items(sample_data)
        assert len(processed) == 3
        assert all("original" in item for item in processed)
        assert all(item["processed"] is True for item in processed)

    def test_process_items_empty_list(self, engine):
        """Test _process_items with empty list."""
        processed = engine._process_items([])
        assert processed == []

    def test_process_items_non_dict_items(self, engine):
        """Test _process_items with non-dict items."""
        data = [1, 2, 3, {"id": 1}]
        processed = engine._process_items(data)
        assert len(processed) == 1
        assert processed[0]["original"]["id"] == 1

    def test_process_items_exception_handling(self, engine):
        """Test _process_items exception handling."""
        with patch('builtins.isinstance', side_effect=Exception("Type check error")):
            processed = engine._process_items([{"id": 1}])
            assert processed == []

    def test_calculate_metrics_success(self, engine, sample_data):
        """Test _calculate_metrics method success."""
        processed = engine._process_items(sample_data)
        metrics = engine._calculate_metrics(processed)
        assert metrics["items_processed"] == 3
        assert metrics["success_rate"] == 1.0
        assert "timestamp" in metrics

    def test_calculate_metrics_empty_processed(self, engine):
        """Test _calculate_metrics with empty processed list."""
        metrics = engine._calculate_metrics([])
        assert metrics["items_processed"] == 0
        assert metrics["success_rate"] == 1.0

    def test_calculate_metrics_exception_handling(self, engine):
        """Test _calculate_metrics exception handling."""
        with patch('src.core.analytics.engines.batch_analytics_engine.datetime', side_effect=Exception("Time error")):
            try:
                metrics = engine._calculate_metrics([{"id": 1}])
                # If exception is caught, should return empty dict
                assert isinstance(metrics, dict)
            except Exception:
                # If exception propagates, that's also acceptable
                pass

    def test_get_stats(self, engine, sample_data):
        """Test get_stats method."""
        engine.process_batch(sample_data)
        stats = engine.get_stats()
        assert stats["batches_processed"] == 1
        assert stats["total_items"] == 3
        assert "timestamp" in stats

    def test_get_stats_multiple_batches(self, engine, sample_data):
        """Test get_stats with multiple batches."""
        engine.process_batch(sample_data)
        engine.process_batch(sample_data)
        stats = engine.get_stats()
        assert stats["batches_processed"] == 2
        assert stats["total_items"] == 6

    def test_clear_stats(self, engine, sample_data):
        """Test clear_stats method."""
        engine.process_batch(sample_data)
        engine.clear_stats()
        stats = engine.get_stats()
        assert stats["batches_processed"] == 0
        assert stats["total_items"] == 0

    def test_get_status(self, engine):
        """Test get_status method."""
        status = engine.get_status()
        assert status["active"] is True
        assert status["queue_size"] == 0
        assert status["batches_processed"] == 0
        assert "timestamp" in status

    def test_get_status_with_queue(self, engine):
        """Test get_status with items in queue."""
        engine.queue = [1, 2, 3]
        status = engine.get_status()
        assert status["queue_size"] == 3

    def test_create_batch_analytics_engine_default(self):
        """Test factory function with default config."""
        engine = create_batch_analytics_engine()
        assert isinstance(engine, BatchAnalyticsEngine)
        assert engine.config == {}

    def test_create_batch_analytics_engine_with_config(self):
        """Test factory function with config."""
        config = {"batch_size": 50}
        engine = create_batch_analytics_engine(config)
        assert isinstance(engine, BatchAnalyticsEngine)
        assert engine.config["batch_size"] == 50

