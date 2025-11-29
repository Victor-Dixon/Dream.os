#!/usr/bin/env python3
"""
Unit Tests for Batch Analytics Engine
=====================================

Comprehensive tests for batch_analytics_engine.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import pytest
from src.core.analytics.engines.batch_analytics_engine import (
    BatchAnalyticsEngine,
    create_batch_analytics_engine
)


class TestBatchAnalyticsEngine:
    """Tests for BatchAnalyticsEngine."""

    def test_initialization(self):
        """Test batch engine initialization."""
        engine = BatchAnalyticsEngine()
        assert engine.config == {}
        assert engine.queue == []
        assert engine.stats["batches_processed"] == 0
        assert engine.stats["total_items"] == 0

    def test_initialization_with_config(self):
        """Test batch engine initialization with config."""
        config = {"batch_size": 100}
        engine = BatchAnalyticsEngine(config)
        assert engine.config == config

    def test_process_batch_empty(self):
        """Test batch processing with empty data."""
        engine = BatchAnalyticsEngine()
        result = engine.process_batch([])
        assert "error" in result
        assert result["error"] == "No data provided"

    def test_process_batch_with_data(self):
        """Test batch processing with valid data."""
        engine = BatchAnalyticsEngine()
        data = [
            {"id": 1, "value": 10},
            {"id": 2, "value": 20},
            {"id": 3, "value": 30},
        ]
        result = engine.process_batch(data)
        assert "processed_items" in result
        assert "metrics" in result
        assert result["batch_size"] == 3
        assert "timestamp" in result

    def test_process_batch_updates_stats(self):
        """Test that batch processing updates stats."""
        engine = BatchAnalyticsEngine()
        data = [{"id": 1, "value": 10}, {"id": 2, "value": 20}]
        engine.process_batch(data)
        assert engine.stats["batches_processed"] == 1
        assert engine.stats["total_items"] == 2

    def test_process_batch_multiple_batches(self):
        """Test processing multiple batches."""
        engine = BatchAnalyticsEngine()
        batch1 = [{"id": 1, "value": 10}]
        batch2 = [{"id": 2, "value": 20}, {"id": 3, "value": 30}]
        
        engine.process_batch(batch1)
        engine.process_batch(batch2)
        
        assert engine.stats["batches_processed"] == 2
        assert engine.stats["total_items"] == 3

    def test_process_batch_exception_handling(self):
        """Test batch processing exception handling."""
        engine = BatchAnalyticsEngine()
        # Data that might cause exception
        result = engine.process_batch(None)
        assert "error" in result

    def test_process_items(self):
        """Test _process_items method."""
        engine = BatchAnalyticsEngine()
        data = [{"id": 1, "value": 10}, {"id": 2, "value": 20}]
        processed = engine._process_items(data)
        assert len(processed) == 2
        assert all("original" in item for item in processed)
        assert all("processed" in item for item in processed)

    def test_process_items_empty(self):
        """Test _process_items with empty data."""
        engine = BatchAnalyticsEngine()
        processed = engine._process_items([])
        assert processed == []

    def test_process_items_non_dict(self):
        """Test _process_items with non-dict items."""
        engine = BatchAnalyticsEngine()
        data = [{"id": 1}, "not a dict", {"id": 2}]
        processed = engine._process_items(data)
        # Should only process dict items
        assert len(processed) == 2

    def test_process_items_exception_handling(self):
        """Test _process_items exception handling."""
        engine = BatchAnalyticsEngine()
        # Data that might cause exception
        processed = engine._process_items(None)
        assert processed == []

    def test_calculate_metrics(self):
        """Test _calculate_metrics method."""
        engine = BatchAnalyticsEngine()
        processed = [
            {"original": {"id": 1}, "processed": True},
            {"original": {"id": 2}, "processed": True},
        ]
        metrics = engine._calculate_metrics(processed)
        assert "items_processed" in metrics
        assert metrics["items_processed"] == 2
        assert "success_rate" in metrics
        assert "timestamp" in metrics

    def test_calculate_metrics_empty(self):
        """Test _calculate_metrics with empty processed."""
        engine = BatchAnalyticsEngine()
        metrics = engine._calculate_metrics([])
        assert metrics["items_processed"] == 0

    def test_calculate_metrics_exception_handling(self):
        """Test _calculate_metrics exception handling."""
        engine = BatchAnalyticsEngine()
        metrics = engine._calculate_metrics(None)
        assert metrics == {}

    def test_get_stats(self):
        """Test getting engine statistics."""
        engine = BatchAnalyticsEngine()
        engine.process_batch([{"id": 1}, {"id": 2}])
        stats = engine.get_stats()
        assert stats["batches_processed"] == 1
        assert stats["total_items"] == 2
        assert "timestamp" in stats

    def test_clear_stats(self):
        """Test clearing statistics."""
        engine = BatchAnalyticsEngine()
        engine.process_batch([{"id": 1}])
        assert engine.stats["batches_processed"] == 1
        engine.clear_stats()
        assert engine.stats["batches_processed"] == 0
        assert engine.stats["total_items"] == 0

    def test_get_status(self):
        """Test getting engine status."""
        engine = BatchAnalyticsEngine()
        status = engine.get_status()
        assert "active" in status
        assert status["active"] is True
        assert "queue_size" in status
        assert "batches_processed" in status
        assert "timestamp" in status

    def test_get_status_with_processed_batches(self):
        """Test get_status after processing batches."""
        engine = BatchAnalyticsEngine()
        engine.process_batch([{"id": 1}])
        status = engine.get_status()
        assert status["batches_processed"] == 1


class TestFactoryFunction:
    """Tests for factory function."""

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
        assert engine.config == config


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.engines.batch_analytics_engine", "--cov-report=term-missing"])


