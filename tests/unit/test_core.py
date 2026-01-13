"""
Unit tests for Agent Cellphone V2 core functionality.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from agent_cellphone_v2 import AgentCoordinator
from agent_cellphone_v2.config import Settings


class TestAgentCoordinator:
    """Test cases for AgentCoordinator."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings()

    @pytest.fixture
    def coordinator(self, settings):
        """Create test coordinator."""
        return AgentCoordinator()

    @pytest.mark.asyncio
    async def test_initialization(self, coordinator):
        """Test coordinator initialization."""
        assert coordinator.coordinator is None
        assert not coordinator.is_running()

    @pytest.mark.asyncio
    async def test_start_stop(self, coordinator):
        """Test starting and stopping the coordinator."""
        # Start
        await coordinator.start()
        assert coordinator.is_running()

        # Stop
        await coordinator.stop()
        assert not coordinator.is_running()

    @pytest.mark.asyncio
    async def test_send_message(self, coordinator):
        """Test sending a message."""
        # Start coordinator first
        await coordinator.start()

        # Send message
        result = await coordinator.send_message("test-agent", "Hello!")

        # Verify result structure
        assert isinstance(result, dict)
        assert "status" in result
        assert result["recipient"] == "test-agent"

        # Clean up
        await coordinator.stop()

    @pytest.mark.asyncio
    async def test_get_status(self, coordinator):
        """Test getting system status."""
        status = await coordinator.get_status()

        assert isinstance(status, dict)
        assert "running" in status
        assert "services" in status
        assert "version" in status