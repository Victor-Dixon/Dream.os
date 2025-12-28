"""
Tests for discord_commander/discord_gui_controller.py - DiscordGUIController class.

Target: ≥85% coverage, 15+ test methods.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock, ANY
import sys
from pathlib import Path
import importlib.util

# Mock pyautogui to prevent display connection errors in headless environment
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Setup Discord mocks (SSOT)
_discord_utils_path = _project_root / "tests" / "utils" / "discord_test_utils.py"
spec = importlib.util.spec_from_file_location("discord_test_utils", _discord_utils_path)
discord_test_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_test_utils)
setup_discord_mocks = discord_test_utils.setup_discord_mocks
create_mock_messaging_service = discord_test_utils.create_mock_messaging_service
setup_discord_mocks()

from src.discord_commander.discord_gui_controller import DiscordGUIController
from src.services.unified_messaging_service import UnifiedMessagingService


class TestDiscordGUIController:
    """Test DiscordGUIController class."""

    @pytest.fixture
    def mock_messaging_service(self):
        """Create mock messaging service."""
        return create_mock_messaging_service(
            service_class=UnifiedMessagingService,
            send_message_return={"success": True}
        )

    @pytest.fixture
    def controller(self, mock_messaging_service):
        """Create DiscordGUIController instance."""
        return DiscordGUIController(mock_messaging_service)

    def test_init(self, mock_messaging_service):
        """Test DiscordGUIController initialization."""
        controller = DiscordGUIController(mock_messaging_service)
        assert controller.messaging_service == mock_messaging_service
        assert controller.logger is not None

    def test_create_main_gui(self, controller, mock_messaging_service):
        """Test create_main_gui method."""
        with patch('src.discord_commander.discord_gui_controller.AgentMessagingGUIView') as mock_view_class:
            mock_view = MagicMock()
            mock_view_class.return_value = mock_view
            
            result = controller.create_main_gui()
            
            mock_view_class.assert_called_once_with(mock_messaging_service)
            assert result == mock_view

    def test_create_status_gui(self, controller, mock_messaging_service):
        """Test create_status_gui method."""
        with patch('src.discord_commander.discord_gui_controller.SwarmStatusGUIView') as mock_view_class:
            mock_view = MagicMock()
            mock_view_class.return_value = mock_view
            
            result = controller.create_status_gui()
            
            mock_view_class.assert_called_once_with(mock_messaging_service)
            assert result == mock_view

    def test_create_control_panel(self, controller, mock_messaging_service):
        """Test create_control_panel method."""
        with patch('src.discord_commander.discord_gui_controller.MainControlPanelView') as mock_view_class:
            mock_view = MagicMock()
            mock_view_class.return_value = mock_view
            
            result = controller.create_control_panel()
            
            mock_view_class.assert_called_once_with(mock_messaging_service)
            assert result == mock_view

    def test_create_agent_message_modal(self, controller, mock_messaging_service):
        """Test create_agent_message_modal method."""
        with patch('src.discord_commander.discord_gui_controller.AgentMessageModal') as mock_modal_class:
            mock_modal = MagicMock()
            mock_modal_class.return_value = mock_modal
            
            result = controller.create_agent_message_modal("Agent-1")
            
            mock_modal_class.assert_called_once_with("Agent-1", mock_messaging_service)
            assert result == mock_modal

    def test_create_broadcast_modal(self, controller, mock_messaging_service):
        """Test create_broadcast_modal method."""
        with patch('src.discord_commander.discord_gui_controller.BroadcastMessageModal') as mock_modal_class:
            mock_modal = MagicMock()
            mock_modal_class.return_value = mock_modal
            
            result = controller.create_broadcast_modal()
            
            mock_modal_class.assert_called_once_with(mock_messaging_service)
            assert result == mock_modal

    @pytest.mark.asyncio
    async def test_send_message_success(self, controller, mock_messaging_service):
        """Test send_message with successful send."""
        result = await controller.send_message("Agent-1", "Test message", "regular", False)
        
        mock_messaging_service.send_message.assert_called_once_with(
            agent="Agent-1",
            message="Test message",
            priority="regular",
            use_pyautogui=True,
            wait_for_delivery=False,
            stalled=False,
            discord_user_id=ANY,
            apply_template=ANY,
            message_category=ANY,
            sender=ANY
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_send_message_stalled(self, controller, mock_messaging_service):
        """Test send_message with stalled flag."""
        await controller.send_message("Agent-1", "Test message", "high", True)
        
        mock_messaging_service.send_message.assert_called_once_with(
            agent="Agent-1",
            message="Test message",
            priority="high",
            use_pyautogui=True,
            wait_for_delivery=False,
            stalled=True,
            discord_user_id=ANY,
            apply_template=ANY,
            message_category=ANY,
            sender=ANY
        )

    @pytest.mark.asyncio
    async def test_send_message_failure(self, controller, mock_messaging_service):
        """Test send_message with failed send."""
        mock_messaging_service.send_message.return_value = {"success": False}
        
        result = await controller.send_message("Agent-1", "Test message")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_send_message_exception(self, controller, mock_messaging_service):
        """Test send_message with exception handling."""
        mock_messaging_service.send_message.side_effect = Exception("Test error")
        
        result = await controller.send_message("Agent-1", "Test message")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_broadcast_message_success(self, controller, mock_messaging_service):
        """Test broadcast_message with successful broadcast to all agents."""
        mock_messaging_service.send_message.return_value = {"success": True}
        
        result = await controller.broadcast_message("Test broadcast", "regular")
        
        # Should send to all 8 agents
        assert mock_messaging_service.send_message.call_count == 8
        assert result is True

    @pytest.mark.asyncio
    async def test_broadcast_message_partial_failure(self, controller, mock_messaging_service):
        """Test broadcast_message with partial failure."""
        # First 4 succeed, last 4 fail
        mock_messaging_service.send_message.side_effect = [
            {"success": True},
            {"success": True},
            {"success": True},
            {"success": True},
            {"success": False},
            {"success": False},
            {"success": False},
            {"success": False}
        ]
        
        result = await controller.broadcast_message("Test broadcast")
        
        assert result is False  # Not all succeeded

    @pytest.mark.asyncio
    async def test_broadcast_message_exception(self, controller, mock_messaging_service):
        """Test broadcast_message with exception handling."""
        mock_messaging_service.send_message.side_effect = Exception("Test error")
        
        result = await controller.broadcast_message("Test broadcast")
        
        assert result is False

    def test_get_agent_status_success(self, controller):
        """Test get_agent_status with successful status retrieval."""
        with patch('src.discord_commander.status_reader.StatusReader') as mock_status_reader_class:
            mock_status_reader = MagicMock()
            mock_status_reader_class.return_value = mock_status_reader
            mock_status_reader.get_agent_status = MagicMock(side_effect=[
                {"status": "active", "agent_id": "Agent-1"},
                {"status": "active", "agent_id": "Agent-2"},
                None,  # Agent-3 not found
                {"status": "active", "agent_id": "Agent-4"},
                None, None, None, None  # Agents 5-8 not found
            ])
            
            result = controller.get_agent_status()
            
            assert "Agent-1" in result
            assert "Agent-2" in result
            assert "Agent-4" in result
            assert "Agent-3" not in result

    def test_get_agent_status_exception(self, controller):
        """Test get_agent_status with exception handling."""
        with patch('src.discord_commander.status_reader.StatusReader', side_effect=Exception("Test error")):
            result = controller.get_agent_status()
            
            assert result == {}

    def test_logger_initialized(self, controller):
        """Test that logger is properly initialized."""
        assert controller.logger is not None
        assert controller.logger.name == "src.discord_commander.discord_gui_controller"



