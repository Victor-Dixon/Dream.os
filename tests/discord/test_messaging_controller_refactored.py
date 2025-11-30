#!/usr/bin/env python3
"""
Tests for Messaging Controller Refactored
==========================================

Comprehensive tests for src/discord_commander/messaging_controller_refactored.py

Author: Agent-7 (Web Development Specialist)
Date: 2025-11-30
Target: 80%+ coverage
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestDiscordMessagingController:
    """Test suite for DiscordMessagingController."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library."""
        with patch.dict('sys.modules', {
            'discord': MagicMock(),
            'discord.ext': MagicMock(),
            'discord.ext.commands': MagicMock(),
            'discord.ui': MagicMock()
        }):
            yield

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock ConsolidatedMessagingService."""
        service = MagicMock()
        service.send_message = Mock(return_value=True)
        service.broadcast_message = Mock(return_value=True)
        service.agent_data = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent 1"},
            "Agent-2": {"active": False, "coordinates": (300, 400), "name": "Agent 2"}
        }
        return service

    def test_controller_initialization(self, mock_discord, mock_messaging_service):
        """Test controller initialization."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        controller = DiscordMessagingController(mock_messaging_service)
        assert controller is not None
        assert controller.messaging_service == mock_messaging_service
        assert hasattr(controller, 'logger')

    def test_create_agent_messaging_view(self, mock_discord, mock_messaging_service):
        """Test creating agent messaging view."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        controller = DiscordMessagingController(mock_messaging_service)
        view = controller.create_agent_messaging_view()
        
        assert view is not None
        assert view.messaging_service == mock_messaging_service

    def test_create_swarm_status_view(self, mock_discord, mock_messaging_service):
        """Test creating swarm status view."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        controller = DiscordMessagingController(mock_messaging_service)
        view = controller.create_swarm_status_view()
        
        assert view is not None
        assert view.messaging_service == mock_messaging_service

    @pytest.mark.asyncio
    async def test_send_agent_message_success(self, mock_discord, mock_messaging_service):
        """Test sending message to agent (success)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        controller = DiscordMessagingController(mock_messaging_service)
        result = await controller.send_agent_message("Agent-1", "Test message", priority="NORMAL")
        
        assert result is True
        mock_messaging_service.send_message.assert_called_once_with(
            agent="Agent-1",
            message="Test message",
            priority="NORMAL"
        )

    @pytest.mark.asyncio
    async def test_send_agent_message_failure(self, mock_discord, mock_messaging_service):
        """Test sending message to agent (failure)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        mock_messaging_service.send_message = Mock(side_effect=Exception("Connection error"))
        
        controller = DiscordMessagingController(mock_messaging_service)
        result = await controller.send_agent_message("Agent-1", "Test message", priority="NORMAL")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_success(self, mock_discord, mock_messaging_service):
        """Test broadcasting to swarm (success)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        controller = DiscordMessagingController(mock_messaging_service)
        result = await controller.broadcast_to_swarm("Test broadcast", priority="NORMAL")
        
        assert result is True
        mock_messaging_service.broadcast_message.assert_called_once_with(
            message="Test broadcast",
            from_agent="Discord-Controller",
            priority="NORMAL"
        )

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_failure(self, mock_discord, mock_messaging_service):
        """Test broadcasting to swarm (failure)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        mock_messaging_service.broadcast_message = Mock(side_effect=Exception("Broadcast error"))
        
        controller = DiscordMessagingController(mock_messaging_service)
        result = await controller.broadcast_to_swarm("Test broadcast", priority="NORMAL")
        
        assert result is False

    def test_get_agent_status_success(self, mock_discord, mock_messaging_service):
        """Test getting agent status (success)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        controller = DiscordMessagingController(mock_messaging_service)
        status = controller.get_agent_status()
        
        assert isinstance(status, dict)
        assert "Agent-1" in status
        assert status["Agent-1"]["active"] is True
        assert status["Agent-1"]["coordinates"] == (100, 200)
        assert status["Agent-1"]["name"] == "Agent 1"

    def test_get_agent_status_no_agent_data(self, mock_discord, mock_messaging_service):
        """Test getting agent status (no agent_data)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        delattr(mock_messaging_service, 'agent_data')
        
        controller = DiscordMessagingController(mock_messaging_service)
        status = controller.get_agent_status()
        
        assert status == {}

    def test_get_agent_status_error(self, mock_discord, mock_messaging_service):
        """Test getting agent status (error)."""
        from src.discord_commander.messaging_controller_refactored import DiscordMessagingController
        
        mock_messaging_service.agent_data = None  # Will cause error when iterating
        
        controller = DiscordMessagingController(mock_messaging_service)
        status = controller.get_agent_status()
        
        assert status == {}



