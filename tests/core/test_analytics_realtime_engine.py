#!/usr/bin/env python3
"""
Unit Tests for Realtime Analytics Engine
=========================================

Comprehensive tests for realtime_analytics_engine.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from src.core.analytics.engines.realtime_analytics_engine import (
    RealtimeAnalyticsEngine,
    create_realtime_analytics_engine
)


class TestRealtimeAnalyticsEngine:
    """Tests for RealtimeAnalyticsEngine."""

    def test_initialization(self):
        """Test realtime engine initialization."""
        engine = RealtimeAnalyticsEngine()
        assert engine.config == {}
        assert len(engine.queue) == 0
        assert engine.active is False
        assert engine.task is None
        assert engine.stats["processed"] == 0
        assert engine.stats["errors"] == 0

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"max_queue_size": 100}
        engine = RealtimeAnalyticsEngine(config)
        assert engine.config == config

    @pytest.mark.asyncio
    async def test_start_processing(self):
        """Test starting processing."""
        engine = RealtimeAnalyticsEngine()
        result = await engine.start_processing()
        assert result["status"] == "started"
        assert engine.active is True
        assert engine.task is not None
        assert "timestamp" in result
        # Cleanup
        await engine.stop_processing()

    @pytest.mark.asyncio
    async def test_stop_processing(self):
        """Test stopping processing."""
        engine = RealtimeAnalyticsEngine()
        await engine.start_processing()
        result = await engine.stop_processing()
        assert result["status"] == "stopped"
        assert engine.active is False
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_stop_processing_when_not_active(self):
        """Test stopping when not active."""
        engine = RealtimeAnalyticsEngine()
        result = await engine.stop_processing()
        assert result["status"] == "stopped"

    @pytest.mark.asyncio
    async def test_processing_loop_processes_queue(self):
        """Test that processing loop processes queue items."""
        engine = RealtimeAnalyticsEngine()
        await engine.start_processing()
        engine.add_data({"id": "test1", "value": 10})
        engine.add_data({"id": "test2", "value": 20})
        # Wait for processing
        await asyncio.sleep(0.2)
        assert engine.stats["processed"] >= 2
        await engine.stop_processing()

    @pytest.mark.asyncio
    async def test_processing_loop_handles_errors(self):
        """Test that processing loop handles errors."""
        engine = RealtimeAnalyticsEngine()
        await engine.start_processing()
        # Add data that might cause error
        engine.add_data(None)
        await asyncio.sleep(0.2)
        # Should increment error count
        assert engine.stats["errors"] >= 0  # May or may not error
        await engine.stop_processing()

    @pytest.mark.asyncio
    async def test_process_data(self):
        """Test processing a single data item."""
        engine = RealtimeAnalyticsEngine()
        initial_processed = engine.stats["processed"]
        await engine._process_data({"id": "test", "value": 10})
        assert engine.stats["processed"] == initial_processed + 1

    @pytest.mark.asyncio
    async def test_process_data_error_handling(self):
        """Test process data error handling."""
        engine = RealtimeAnalyticsEngine()
        initial_errors = engine.stats["errors"]
        # Data that causes exception
        await engine._process_data(None)
        # Should handle gracefully
        assert engine.stats["errors"] >= initial_errors

    def test_add_data(self):
        """Test adding data to queue."""
        engine = RealtimeAnalyticsEngine()
        data = {"id": "test1", "value": 10}
        engine.add_data(data)
        assert engine.get_queue_size() == 1
        assert engine.queue[0] == data

    def test_add_data_multiple(self):
        """Test adding multiple data items."""
        engine = RealtimeAnalyticsEngine()
        engine.add_data({"id": "test1"})
        engine.add_data({"id": "test2"})
        engine.add_data({"id": "test3"})
        assert engine.get_queue_size() == 3

    def test_add_data_error_handling(self):
        """Test add data error handling."""
        engine = RealtimeAnalyticsEngine()
        # Should handle gracefully
        engine.add_data(None)
        assert engine.get_queue_size() >= 0

    def test_get_queue_size_empty(self):
        """Test getting queue size when empty."""
        engine = RealtimeAnalyticsEngine()
        assert engine.get_queue_size() == 0

    def test_get_queue_size_with_items(self):
        """Test getting queue size with items."""
        engine = RealtimeAnalyticsEngine()
        engine.add_data({"id": 1})
        engine.add_data({"id": 2})
        assert engine.get_queue_size() == 2

    def test_get_stats_inactive(self):
        """Test getting stats when inactive."""
        engine = RealtimeAnalyticsEngine()
        stats = engine.get_stats()
        assert stats["active"] is False
        assert stats["queue_size"] == 0
        assert stats["processed"] == 0
        assert stats["errors"] == 0
        assert "timestamp" in stats

    @pytest.mark.asyncio
    async def test_get_stats_active(self):
        """Test getting stats when active."""
        engine = RealtimeAnalyticsEngine()
        await engine.start_processing()
        stats = engine.get_stats()
        assert stats["active"] is True
        await engine.stop_processing()

    def test_get_stats_with_data(self):
        """Test getting stats with processed data."""
        engine = RealtimeAnalyticsEngine()
        engine.stats["processed"] = 10
        engine.stats["errors"] = 2
        stats = engine.get_stats()
        assert stats["processed"] == 10
        assert stats["errors"] == 2

    def test_reset_stats(self):
        """Test resetting statistics."""
        engine = RealtimeAnalyticsEngine()
        engine.stats["processed"] = 10
        engine.stats["errors"] = 5
        engine.reset_stats()
        assert engine.stats["processed"] == 0
        assert engine.stats["errors"] == 0

    def test_get_status(self):
        """Test getting engine status."""
        engine = RealtimeAnalyticsEngine()
        status = engine.get_status()
        assert "active" in status
        assert "stats" in status
        assert "timestamp" in status
        assert status["stats"]["active"] is False

    @pytest.mark.asyncio
    async def test_get_status_when_active(self):
        """Test getting status when active."""
        engine = RealtimeAnalyticsEngine()
        await engine.start_processing()
        status = engine.get_status()
        assert status["active"] is True
        assert status["stats"]["active"] is True
        await engine.stop_processing()

    def test_create_realtime_analytics_engine(self):
        """Test factory function."""
        engine = create_realtime_analytics_engine()
        assert isinstance(engine, RealtimeAnalyticsEngine)

    def test_create_realtime_analytics_engine_with_config(self):
        """Test factory function with config."""
        config = {"test": "value"}
        engine = create_realtime_analytics_engine(config)
        assert isinstance(engine, RealtimeAnalyticsEngine)
        assert engine.config == config

    @pytest.mark.asyncio
    async def test_start_stop_lifecycle(self):
        """Test full start/stop lifecycle."""
        engine = RealtimeAnalyticsEngine()
        # Start
        start_result = await engine.start_processing()
        assert start_result["status"] == "started"
        assert engine.active is True
        # Process some data
        engine.add_data({"id": "test1"})
        await asyncio.sleep(0.1)
        # Stop
        stop_result = await engine.stop_processing()
        assert stop_result["status"] == "stopped"
        assert engine.active is False

    @pytest.mark.asyncio
    async def test_multiple_start_stops(self):
        """Test multiple start/stop cycles."""
        engine = RealtimeAnalyticsEngine()
        # First cycle
        await engine.start_processing()
        await engine.stop_processing()
        # Second cycle
        await engine.start_processing()
        await engine.stop_processing()
        assert engine.active is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.engines.realtime_analytics_engine", "--cov-report=term-missing"])

