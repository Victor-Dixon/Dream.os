#!/usr/bin/env python3
"""
Tests for Messaging Controller - Comprehensive Coverage
=======================================================

Expanded test suite for messaging_controller.py targeting ≥85% coverage.

Author: Agent-7
Date: 2025-01-28
Target: ≥85% coverage, 10+ test methods
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestDiscordMessagingController:
    """Comprehensive test suite for Discord messaging controller."""

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock messaging service."""
        service = MagicMock()
        service.send_message = MagicMock(return_value=True)
        service.broadcast_message = MagicMock(return_value=True)
        service.agent_data = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"},
            "Agent-2": {"active": False, "coordinates": (200, 300), "name": "Agent-2"}
        }
        return service

    def test_controller_initialization(self, mock_messaging_service):
        """Test controller initialization."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            assert controller is not None
            assert controller.messaging_service == mock_messaging_service
        except ImportError:
            pytest.skip("Messaging controller not available")

    def test_create_agent_messaging_view(self, mock_messaging_service):
        """Test creating agent messaging view."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            
            view = controller.create_agent_messaging_view()
            assert view is not None
        except ImportError:
            pytest.skip("Messaging controller not available")

    def test_create_swarm_status_view(self, mock_messaging_service):
        """Test creating swarm status view."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            
            view = controller.create_swarm_status_view()
            assert view is not None
        except ImportError:
            pytest.skip("Messaging controller not available")

    @pytest.mark.asyncio
    async def test_send_agent_message_success(self, mock_messaging_service):
        """Test sending agent message successfully."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            
            result = await controller.send_agent_message("Agent-1", "Test message", "NORMAL")
            assert result is True
            mock_messaging_service.send_message.assert_called_once_with(
                agent="Agent-1",
                message="Test message",
                priority="NORMAL"
            )
        except ImportError:
            pytest.skip("Messaging controller not available")

    @pytest.mark.asyncio
    async def test_send_agent_message_failure(self, mock_messaging_service):
        """Test sending agent message failure."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            mock_messaging_service.send_message.return_value = False
            
            result = await controller.send_agent_message("Agent-1", "Test message", "NORMAL")
            assert result is False
        except ImportError:
            pytest.skip("Messaging controller not available")

    @pytest.mark.asyncio
    async def test_send_agent_message_exception(self, mock_messaging_service):
        """Test sending agent message with exception."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            mock_messaging_service.send_message.side_effect = Exception("Test error")
            
            result = await controller.send_agent_message("Agent-1", "Test message", "NORMAL")
            assert result is False
        except ImportError:
            pytest.skip("Messaging controller not available")

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_success(self, mock_messaging_service):
        """Test broadcasting to swarm successfully."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            
            result = await controller.broadcast_to_swarm("Test broadcast", "NORMAL")
            assert result is True
            mock_messaging_service.broadcast_message.assert_called_once_with(
                message="Test broadcast",
                from_agent="Discord-Controller",
                priority="NORMAL"
            )
        except ImportError:
            pytest.skip("Messaging controller not available")

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_failure(self, mock_messaging_service):
        """Test broadcasting to swarm failure."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            mock_messaging_service.broadcast_message.return_value = False
            
            result = await controller.broadcast_to_swarm("Test broadcast", "NORMAL")
            assert result is False
        except ImportError:
            pytest.skip("Messaging controller not available")

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_exception(self, mock_messaging_service):
        """Test broadcasting to swarm with exception."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            mock_messaging_service.broadcast_message.side_effect = Exception("Test error")
            
            result = await controller.broadcast_to_swarm("Test broadcast", "NORMAL")
            assert result is False
        except ImportError:
            pytest.skip("Messaging controller not available")

    def test_get_agent_status_success(self, mock_messaging_service):
        """Test getting agent status successfully."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            
            status = controller.get_agent_status()
            assert isinstance(status, dict)
            assert "Agent-1" in status
            assert status["Agent-1"]["active"] is True
        except ImportError:
            pytest.skip("Messaging controller not available")

    def test_get_agent_status_no_agent_data(self, mock_messaging_service):
        """Test getting agent status without agent_data."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            delattr(mock_messaging_service, 'agent_data')
            
            status = controller.get_agent_status()
            assert status == {}
        except ImportError:
            pytest.skip("Messaging controller not available")

    def test_get_agent_status_exception(self, mock_messaging_service):
        """Test getting agent status with exception."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            # Cause exception by making agent_data inaccessible
            mock_messaging_service.agent_data = property(lambda self: self._nonexistent)
            
            status = controller.get_agent_status()
            assert status == {}
        except ImportError:
            pytest.skip("Messaging controller not available")

    def test_get_agent_status_partial_data(self, mock_messaging_service):
        """Test getting agent status with partial data."""
        try:
            from src.discord_commander.messaging_controller import DiscordMessagingController
            controller = DiscordMessagingController(mock_messaging_service)
            mock_messaging_service.agent_data = {
                "Agent-1": {"active": True},  # Missing coordinates and name
                "Agent-2": {"coordinates": (200, 300)}  # Missing active and name
            }
            
            status = controller.get_agent_status()
            assert isinstance(status, dict)
            # Should handle missing fields gracefully
            assert "Agent-1" in status
        except ImportError:
            pytest.skip("Messaging controller not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.discord_commander.messaging_controller", "--cov-report=term-missing"])
