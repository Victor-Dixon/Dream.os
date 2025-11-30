#!/usr/bin/env python3
"""
Unit Tests for Analytics Coordinator
====================================
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.core.analytics.coordinators.analytics_coordinator import AnalyticsCoordinator


class TestAnalyticsCoordinator:
    """Tests for AnalyticsCoordinator."""

    def test_initialization(self):
        """Test coordinator initialization."""
        coordinator = AnalyticsCoordinator()
        assert coordinator.config == {}
        assert coordinator.active is False
        assert coordinator.engines == {}
        assert coordinator.callbacks == {}

    def test_register_engine(self):
        """Test registering an analytics engine."""
        coordinator = AnalyticsCoordinator()
        mock_engine = MagicMock()
        coordinator.register_engine("test_engine", mock_engine)
        assert "test_engine" in coordinator.engines
        assert coordinator.engines["test_engine"] == mock_engine

    def test_register_callback(self):
        """Test registering a callback."""
        coordinator = AnalyticsCoordinator()
        mock_callback = MagicMock()
        coordinator.register_callback("test_event", mock_callback)
        assert "test_event" in coordinator.callbacks

    @pytest.mark.asyncio
    async def test_start_processing(self):
        """Test starting analytics processing."""
        coordinator = AnalyticsCoordinator()
        result = await coordinator.start_processing()
        assert coordinator.active is True
        assert result["status"] == "started"

    @pytest.mark.asyncio
    async def test_stop_processing(self):
        """Test stopping analytics processing."""
        coordinator = AnalyticsCoordinator()
        await coordinator.start_processing()
        result = await coordinator.stop_processing()
        assert coordinator.active is False
        assert result["status"] == "stopped"

    @pytest.mark.asyncio
    async def test_process_data(self):
        """Test processing analytics data."""
        coordinator = AnalyticsCoordinator()
        mock_engine = MagicMock()
        mock_engine.process = AsyncMock(return_value={"result": "test"})
        coordinator.register_engine("test", mock_engine)
        
        result = await coordinator.process_data({"type": "test", "data": "value"})
        assert result["processed"] is True
        assert "test_result" in result

    def test_get_status(self):
        """Test getting coordinator status."""
        coordinator = AnalyticsCoordinator()
        coordinator.register_engine("test", MagicMock())
        status = coordinator.get_status()
        assert "active" in status
        assert "engines" in status
        assert "test" in status["engines"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

