"""
Unified Discord Test Utilities
==============================

SSOT for Discord mocking in tests. Consolidates all Discord mock patterns
into reusable utilities.

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-07
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, Mock
from typing import Any, Dict, Optional

# Ensure project root is in path for imports
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def setup_discord_mocks():
    """
    Setup Discord module mocks before importing Discord-related code.
    
    This must be called BEFORE importing any Discord modules in test files.
    
    Usage:
        from tests.utils.discord_test_utils import setup_discord_mocks
        
        setup_discord_mocks()  # Call BEFORE imports
        
        from src.discord_commander.some_module import SomeClass
    """
    # Force mock setup - always replace with mocks for testing
    # Create a proper Cog class that can be inherited from
    class MockCog:
        """Mock Cog class for testing."""
        def __init__(self, *args, **kwargs):
            pass
    
    mock_discord = MagicMock()
    mock_discord.Client = MagicMock()
    mock_discord.Embed = MagicMock()
    mock_discord.Color = MagicMock()
    mock_discord.Color.green = MagicMock()
    mock_discord.Color.red = MagicMock()
    mock_discord.Color.blue = MagicMock()
    mock_discord.ui = MagicMock()
    mock_discord.ui.View = MagicMock()
    mock_discord.ui.Modal = MagicMock()
    mock_discord.ui.Button = MagicMock()
    mock_discord.ui.Select = MagicMock()
    mock_discord.Activity = MagicMock()
    mock_discord.ActivityType = MagicMock()
    mock_discord.utils = MagicMock()
    mock_discord.utils.utcnow = MagicMock()
    mock_discord.Intents = MagicMock()
    mock_discord.Intents.default = MagicMock(return_value=MagicMock())
    sys.modules['discord'] = mock_discord
    
    mock_ext = MagicMock()
    sys.modules['discord.ext'] = mock_ext
    
    mock_commands = MagicMock()
    mock_commands.Bot = MagicMock()
    mock_commands.Cog = MockCog
    mock_commands.Context = MagicMock()
    sys.modules['discord.ext.commands'] = mock_commands


def create_mock_discord_bot(
    display_name: str = "TestBot",
    user_id: int = 123456789,
    guilds: Optional[list] = None
) -> MagicMock:
    """
    Create a mock Discord bot instance.
    
    Args:
        display_name: Bot display name
        user_id: Bot user ID
        guilds: List of mock guilds (optional)
    
    Returns:
        Mock Discord bot instance
    """
    bot = MagicMock()
    bot.user = MagicMock()
    bot.user.display_name = display_name
    bot.user.id = user_id
    bot.guilds = guilds or []
    return bot


def create_mock_discord_context(
    user_display_name: str = "TestUser",
    user_id: int = 987654321,
    channel_id: int = 111222333
) -> AsyncMock:
    """
    Create a mock Discord context (commands.Context).
    
    Args:
        user_display_name: User display name
        user_id: User ID
        channel_id: Channel ID
    
    Returns:
        Mock Discord context
    """
    ctx = AsyncMock()
    ctx.user = MagicMock()
    ctx.user.display_name = user_display_name
    ctx.user.id = user_id
    ctx.channel = MagicMock()
    ctx.channel.id = channel_id
    ctx.send = AsyncMock()
    ctx.message = MagicMock()
    ctx.message.channel = ctx.channel
    return ctx


def create_mock_discord_interaction(
    user_display_name: str = "TestUser",
    user_id: int = 987654321
) -> AsyncMock:
    """
    Create a mock Discord interaction.
    
    Args:
        user_display_name: User display name
        user_id: User ID
    
    Returns:
        Mock Discord interaction
    """
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.display_name = user_display_name
    interaction.user.id = user_id
    interaction.response = AsyncMock()
    interaction.response.is_done = MagicMock(return_value=False)
    interaction.response.send_message = AsyncMock()
    interaction.followup = AsyncMock()
    interaction.followup.send = AsyncMock()
    return interaction


def create_mock_messaging_service(
    service_class: Optional[Any] = None,
    send_message_return: Any = {"success": True},
    broadcast_message_return: Any = True,
    agent_data: Optional[Dict] = None
) -> MagicMock:
    """
    Create a mock messaging service.
    
    Args:
        service_class: Service class to spec (optional)
        send_message_return: Return value for send_message
        broadcast_message_return: Return value for broadcast_message
        agent_data: Agent data dictionary (optional)
    
    Returns:
        Mock messaging service
    """
    if service_class:
        service = MagicMock(spec=service_class)
    else:
        service = MagicMock()
    
    service.send_message = MagicMock(return_value=send_message_return)
    service.broadcast_message = MagicMock(return_value=broadcast_message_return)
    
    if agent_data:
        service.agent_data = agent_data
    else:
        # Default agent data
        service.agent_data = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"},
            "Agent-2": {"active": False, "coordinates": (300, 400), "name": "Agent-2"},
            "Agent-3": {"active": True, "coordinates": (500, 600), "name": "Agent-3"},
            "Agent-4": {"active": True, "coordinates": (700, 800), "name": "Agent-4"},
            "Agent-5": {"active": False, "coordinates": (900, 1000), "name": "Agent-5"},
            "Agent-6": {"active": True, "coordinates": (1100, 1200), "name": "Agent-6"},
            "Agent-7": {"active": True, "coordinates": (1300, 1400), "name": "Agent-7"},
            "Agent-8": {"active": False, "coordinates": (1500, 1600), "name": "Agent-8"}
        }
    
    return service


def create_mock_messaging_controller(
    send_agent_message_return: bool = True,
    broadcast_to_swarm_return: bool = True,
    get_agent_status_return: Optional[Dict] = None
) -> MagicMock:
    """
    Create a mock messaging controller.
    
    Args:
        send_agent_message_return: Return value for send_agent_message
        broadcast_to_swarm_return: Return value for broadcast_to_swarm
        get_agent_status_return: Return value for get_agent_status (optional)
    
    Returns:
        Mock messaging controller
    """
    # Use MagicMock as base, not AsyncMock, to avoid issues with non-async methods
    controller = MagicMock()
    controller.send_agent_message = AsyncMock(return_value=send_agent_message_return)
    controller.broadcast_to_swarm = AsyncMock(return_value=broadcast_to_swarm_return)
    controller.create_agent_messaging_view = MagicMock(return_value=MagicMock())
    controller.create_swarm_status_view = MagicMock(return_value=MagicMock())
    
    if get_agent_status_return is None:
        get_agent_status_return = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"},
            "Agent-2": {"active": False, "coordinates": (300, 400), "name": "Agent-2"}
        }
    controller.get_agent_status = MagicMock(return_value=get_agent_status_return)
    
    return controller


def create_mock_discord_embed(
    title: str = "Test Embed",
    description: str = "Test Description",
    color: int = 0x3498DB
) -> MagicMock:
    """
    Create a mock Discord embed.
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color
    
    Returns:
        Mock Discord embed
    """
    embed = MagicMock()
    embed.title = title
    embed.description = description
    embed.color = color
    embed.fields = []
    embed.add_field = MagicMock()
    embed.set_footer = MagicMock()
    embed.set_author = MagicMock()
    return embed


def create_mock_discord_view() -> MagicMock:
    """
    Create a mock Discord view.
    
    Returns:
        Mock Discord view
    """
    view = MagicMock()
    view.add_item = MagicMock()
    view.remove_item = MagicMock()
    return view


def create_mock_discord_modal() -> MagicMock:
    """
    Create a mock Discord modal.
    
    Returns:
        Mock Discord modal
    """
    modal = MagicMock()
    modal.add_item = MagicMock()
    return modal

