"""
Tests for discord_commander/messaging_controller.py - DiscordMessagingController class.

Target: ≥85% coverage, 12+ test methods.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Setup Discord mocks (SSOT)
# Import with path handling
import importlib.util
_discord_utils_path = _project_root / "tests" / "utils" / "discord_test_utils.py"
spec = importlib.util.spec_from_file_location("discord_test_utils", _discord_utils_path)
discord_test_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_test_utils)
setup_discord_mocks = discord_test_utils.setup_discord_mocks
create_mock_messaging_service = discord_test_utils.create_mock_messaging_service
setup_discord_mocks()

from src.discord_commander.messaging_controller import DiscordMessagingController
from src.services.messaging_infrastructure import ConsolidatedMessagingService


class TestDiscordMessagingController:
    """Test DiscordMessagingController class."""

    @pytest.fixture
    def mock_messaging_service(self):
        """Create mock messaging service."""
        agent_data = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"},
            "Agent-2": {"active": False, "coordinates": (300, 400), "name": "Agent-2"}
        }
        return create_mock_messaging_service(
            service_class=ConsolidatedMessagingService,
            send_message_return=True,
            broadcast_message_return=True,
            agent_data=agent_data
        )

    @pytest.fixture
    def controller(self, mock_messaging_service):
        """Create DiscordMessagingController instance."""
        return DiscordMessagingController(mock_messaging_service)

    def test_init(self, mock_messaging_service):
        """Test DiscordMessagingController initialization."""
        controller = DiscordMessagingController(mock_messaging_service)
        assert controller.messaging_service == mock_messaging_service
        assert controller.logger is not None

    def test_create_agent_messaging_view(self, controller, mock_messaging_service):
        """Test create_agent_messaging_view method."""
        with patch('src.discord_commander.messaging_controller.MessagingControllerView') as mock_view_class:
            mock_view = MagicMock()
            mock_view_class.return_value = mock_view
            
            result = controller.create_agent_messaging_view()
            
            mock_view_class.assert_called_once_with(mock_messaging_service)
            assert result == mock_view

    def test_create_swarm_status_view(self, controller, mock_messaging_service):
        """Test create_swarm_status_view method."""
        with patch('src.discord_commander.messaging_controller.StatusControllerView') as mock_view_class:
            mock_view = MagicMock()
            mock_view_class.return_value = mock_view
            
            result = controller.create_swarm_status_view()
            
            mock_view_class.assert_called_once_with(mock_messaging_service)
            assert result == mock_view

    @pytest.mark.asyncio
    async def test_send_agent_message_success(self, controller, mock_messaging_service):
        """Test send_agent_message with successful send."""
        result = await controller.send_agent_message("Agent-1", "Test message", "NORMAL")
        
        mock_messaging_service.send_message.assert_called_once_with(
            agent="Agent-1",
            message="Test message",
            priority="NORMAL"
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_send_agent_message_high_priority(self, controller, mock_messaging_service):
        """Test send_agent_message with HIGH priority."""
        await controller.send_agent_message("Agent-1", "Test message", "HIGH")
        
        mock_messaging_service.send_message.assert_called_once_with(
            agent="Agent-1",
            message="Test message",
            priority="HIGH"
        )

    @pytest.mark.asyncio
    async def test_send_agent_message_exception(self, controller, mock_messaging_service):
        """Test send_agent_message with exception handling."""
        mock_messaging_service.send_message.side_effect = Exception("Test error")
        
        result = await controller.send_agent_message("Agent-1", "Test message")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_success(self, controller, mock_messaging_service):
        """Test broadcast_to_swarm with successful broadcast."""
        result = await controller.broadcast_to_swarm("Test broadcast", "NORMAL")
        
        mock_messaging_service.broadcast_message.assert_called_once_with(
            message="Test broadcast",
            from_agent="Discord-Controller",
            priority="NORMAL"
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_broadcast_to_swarm_exception(self, controller, mock_messaging_service):
        """Test broadcast_to_swarm with exception handling."""
        mock_messaging_service.broadcast_message.side_effect = Exception("Test error")
        
        result = await controller.broadcast_to_swarm("Test broadcast")
        
        assert result is False

    def test_get_agent_status_success(self, controller, mock_messaging_service):
        """Test get_agent_status with agent data available."""
        result = controller.get_agent_status()
        
        assert "Agent-1" in result
        assert "Agent-2" in result
        assert result["Agent-1"]["active"] is True
        assert result["Agent-1"]["coordinates"] == (100, 200)
        assert result["Agent-2"]["active"] is False

    def test_get_agent_status_no_agent_data(self, controller, mock_messaging_service):
        """Test get_agent_status when agent_data attribute doesn't exist."""
        delattr(mock_messaging_service, 'agent_data')
        
        result = controller.get_agent_status()
        
        assert result == {}

    def test_get_agent_status_exception(self, controller, mock_messaging_service):
        """Test get_agent_status with exception handling."""
        mock_messaging_service.agent_data = None  # Trigger exception
        
        result = controller.get_agent_status()
        
        assert result == {}

    def test_logger_initialized(self, controller):
        """Test that logger is properly initialized."""
        assert controller.logger is not None
        assert controller.logger.name == "src.discord_commander.messaging_controller"



