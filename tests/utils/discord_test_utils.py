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
        """Mock Cog class for testing that properly supports inheritance."""

        def __init__(self, *args, **kwargs):
            """Initialize mock Cog - store args/kwargs if needed."""
            # Use object.__setattr__ to directly set attributes in __dict__
            # This ensures attributes are properly stored and accessible
            object.__setattr__(self, '_args', args)
            object.__setattr__(self, '_kwargs', kwargs)
            # Allow attributes to be set dynamically
            # Use list() to avoid StopIteration when iterating over kwargs
            for key, value in list(kwargs.items()):
                if not key.startswith('_'):
                    object.__setattr__(self, key, value)

        def __setattr__(self, name, value):
            """Store attributes using object.__setattr__ to ensure proper storage."""
            # Always use object.__setattr__ to store directly in __dict__
            object.__setattr__(self, name, value)

        def __getattr__(self, name):
            """Only called when attribute doesn't exist - create a mock for undefined attributes."""
            # __getattr__ is only called when attribute is not found via normal lookup
            # This means the attribute wasn't found in __dict__, so create a mock
            if name.startswith('_'):
                raise AttributeError(
                    f"'{type(self).__name__}' object has no attribute '{name}'")
            # Create a mock for undefined attributes
            mock_attr = MagicMock()
            object.__setattr__(self, name, mock_attr)
            return mock_attr

        def __iter__(self):
            """Prevent StopIteration in iteration contexts."""
            # Return empty iterator
            return iter([])

        def __contains__(self, item):
            """Prevent StopIteration in 'in' checks."""
            return False

    mock_discord = MagicMock()
    mock_discord.Client = MagicMock()

    # Make Embed work as a class that can be instantiated
    def create_embed(*args, **kwargs):
        """Create a mock Embed instance."""
        embed = MagicMock()
        embed.title = kwargs.get('title', '')
        embed.description = kwargs.get('description', '')
        embed.color = kwargs.get('color', MagicMock())
        embed.fields = []
        embed.add_field = MagicMock()
        embed.timestamp = kwargs.get('timestamp')
        return embed
    mock_discord.Embed = create_embed

    mock_discord.Color = MagicMock()
    mock_discord.Color.green = lambda: MagicMock()
    mock_discord.Color.red = lambda: MagicMock()
    mock_discord.Color.blue = lambda: MagicMock()
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

    # CRITICAL FIX: Use real ModuleType for discord.ext so attribute access works
    from types import ModuleType
    mock_ext = ModuleType('discord.ext')
    sys.modules['discord.ext'] = mock_ext

    # CRITICAL FIX: Use a real ModuleType so class inheritance works correctly
    # MagicMock interferes with class inheritance - when Python does `class X(commands.Cog)`,
    # accessing `commands.Cog` via MagicMock returns a new MagicMock instead of MockCog
    mock_commands = ModuleType('discord.ext.commands')
    mock_commands.Bot = MagicMock()
    mock_commands.Cog = MockCog  # Direct assignment to real module
    mock_commands.Context = MagicMock()

    # Make commands.command a no-op decorator (for tests)
    def noop_command(*args, **kwargs):
        """No-op command decorator for tests."""
        def decorator(func):
            return func
        return decorator
    mock_commands.command = noop_command

    # Make other command decorators no-ops
    def noop_decorator(*args, **kwargs):
        """No-op decorator for command decorators."""
        def decorator(func):
            return func
        return decorator
    mock_commands.has_permissions = noop_decorator
    mock_commands.cooldown = noop_decorator
    mock_commands.check = noop_decorator
    mock_commands.guild_only = noop_decorator

    # Set commands on discord.ext module so `from discord.ext import commands` works
    mock_ext.commands = mock_commands

    # Remove any existing modules from cache to ensure our mocks are used
    for mod_name in ['discord.ext.commands', 'discord.ext']:
        if mod_name in sys.modules:
            del sys.modules[mod_name]
    sys.modules['discord.ext'] = mock_ext
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
    service.broadcast_message = MagicMock(
        return_value=broadcast_message_return)

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
    controller.send_agent_message = AsyncMock(
        return_value=send_agent_message_return)
    controller.broadcast_to_swarm = AsyncMock(
        return_value=broadcast_to_swarm_return)
    controller.create_agent_messaging_view = MagicMock(
        return_value=MagicMock())
    controller.create_swarm_status_view = MagicMock(return_value=MagicMock())

    if get_agent_status_return is None:
        get_agent_status_return = {
            "Agent-1": {"active": True, "coordinates": (100, 200), "name": "Agent-1"},
            "Agent-2": {"active": False, "coordinates": (300, 400), "name": "Agent-2"}
        }
    controller.get_agent_status = MagicMock(
        return_value=get_agent_status_return)

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
