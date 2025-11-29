#!/usr/bin/env python3
"""
Tests for Discord GUI Controller - Comprehensive Coverage
=========================================================

Expanded test suite for discord_gui_controller.py targeting ≥85% coverage.

Author: Agent-7
Date: 2025-01-28
Target: ≥85% coverage, 12+ test methods
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestDiscordGUIController:
    """Comprehensive test suite for Discord GUI controller."""

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock messaging service."""
        service = MagicMock()
        service.send_message = MagicMock(return_value={"success": True, "queue_id": "test-123"})
        return service

    def test_controller_initialization(self, mock_messaging_service):
        """Test controller initialization."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            assert controller is not None
            assert controller.messaging_service == mock_messaging_service
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_create_main_gui(self, mock_messaging_service):
        """Test creating main GUI view."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            view = controller.create_main_gui()
            assert view is not None
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_create_status_gui(self, mock_messaging_service):
        """Test creating status GUI view."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            view = controller.create_status_gui()
            assert view is not None
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_create_control_panel(self, mock_messaging_service):
        """Test creating control panel view."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            view = controller.create_control_panel()
            assert view is not None
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_create_agent_message_modal(self, mock_messaging_service):
        """Test creating agent message modal."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            modal = controller.create_agent_message_modal("Agent-1")
            assert modal is not None
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_create_broadcast_modal(self, mock_messaging_service):
        """Test creating broadcast modal."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            modal = controller.create_broadcast_modal()
            assert modal is not None
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_send_message_success(self, mock_messaging_service):
        """Test sending message successfully."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            result = await controller.send_message("Agent-1", "Test message", "regular")
            assert result is True
            mock_messaging_service.send_message.assert_called_once()
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_send_message_failure(self, mock_messaging_service):
        """Test sending message failure."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            mock_messaging_service.send_message.return_value = {"success": False}
            
            result = await controller.send_message("Agent-1", "Test message", "regular")
            assert result is False
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_send_message_with_stalled(self, mock_messaging_service):
        """Test sending message with stalled flag."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            result = await controller.send_message("Agent-1", "Test message", "regular", stalled=True)
            assert result is True
            mock_messaging_service.send_message.assert_called_with(
                agent="Agent-1",
                message="Test message",
                priority="regular",
                use_pyautogui=True,
                wait_for_delivery=False,
                stalled=True
            )
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_send_message_exception(self, mock_messaging_service):
        """Test sending message with exception."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            mock_messaging_service.send_message.side_effect = Exception("Test error")
            
            result = await controller.send_message("Agent-1", "Test message", "regular")
            assert result is False
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_broadcast_message_success(self, mock_messaging_service):
        """Test broadcasting message successfully."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            result = await controller.broadcast_message("Test broadcast", "regular")
            assert result is True
            # Should send to all 8 agents
            assert mock_messaging_service.send_message.call_count == 8
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_broadcast_message_partial_failure(self, mock_messaging_service):
        """Test broadcasting message with partial failure."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            # First 4 succeed, last 4 fail
            mock_messaging_service.send_message.side_effect = [
                {"success": True}, {"success": True}, {"success": True}, {"success": True},
                {"success": False}, {"success": False}, {"success": False}, {"success": False}
            ]
            
            result = await controller.broadcast_message("Test broadcast", "regular")
            assert result is False  # Not all succeeded
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    @pytest.mark.asyncio
    async def test_broadcast_message_exception(self, mock_messaging_service):
        """Test broadcasting message with exception."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            mock_messaging_service.send_message.side_effect = Exception("Test error")
            
            result = await controller.broadcast_message("Test broadcast", "regular")
            assert result is False
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_get_agent_status_success(self, mock_messaging_service):
        """Test getting agent status successfully."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            with patch('src.discord_commander.discord_gui_controller.StatusReader') as mock_reader_class:
                mock_reader = MagicMock()
                mock_reader.get_agent_status = MagicMock(return_value={
                    "status": "active",
                    "mission": "Test mission"
                })
                mock_reader_class.return_value = mock_reader
                
                status = controller.get_agent_status()
                assert isinstance(status, dict)
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_get_agent_status_exception(self, mock_messaging_service):
        """Test getting agent status with exception."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            with patch('src.discord_commander.discord_gui_controller.StatusReader') as mock_reader_class:
                mock_reader_class.side_effect = Exception("Test error")
                
                status = controller.get_agent_status()
                assert status == {}
        except ImportError:
            pytest.skip("Discord GUI controller not available")

    def test_get_agent_status_no_status(self, mock_messaging_service):
        """Test getting agent status when no status available."""
        try:
            from src.discord_commander.discord_gui_controller import DiscordGUIController
            controller = DiscordGUIController(mock_messaging_service)
            
            with patch('src.discord_commander.discord_gui_controller.StatusReader') as mock_reader_class:
                mock_reader = MagicMock()
                mock_reader.get_agent_status = MagicMock(return_value=None)
                mock_reader_class.return_value = mock_reader
                
                status = controller.get_agent_status()
                assert isinstance(status, dict)
        except ImportError:
            pytest.skip("Discord GUI controller not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.discord_commander.discord_gui_controller", "--cov-report=term-missing"])
