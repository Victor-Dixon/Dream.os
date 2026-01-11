"""
Base Command Classes - Reduce Code Repetition
===========================================

Base classes and mixins for Discord command cogs to eliminate repetitive initialization code.

V2 Compliance: DRY principle, base class pattern
Author: Agent-6 - Gaming & Entertainment Specialist
"""

import logging
import functools
from typing import TYPE_CHECKING, List

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    discord = None
    commands = None
    DISCORD_AVAILABLE = False

if TYPE_CHECKING:
    from ..unified_discord_bot import UnifiedDiscordBot
    from ..gui.discord_gui_controller import DiscordGUIController


class DiscordCommandMixin:
    """Mixin class providing common Discord command functionality."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize command mixin with common attributes."""
        super().__init__()
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        """Get the logger for this command class."""
        return self.logger


class RoleDecorators:
    """Common role-based decorators for Discord commands."""

    @staticmethod
    def admin_only():
        """Decorator for commands requiring Admin role only."""
        def decorator(func):
            func.__requires_roles__ = ["Admin", "Captain", "Swarm Commander"]
            return func
        return decorator

    @staticmethod
    def admin_or_captain():
        """Decorator for commands requiring Admin or Captain role."""
        def decorator(func):
            func.__requires_roles__ = ["Admin", "Captain", "Swarm Commander"]
            return func
        return decorator

    @staticmethod
    def agent_or_higher():
        """Decorator for commands requiring Agent or higher role."""
        def decorator(func):
            func.__requires_roles__ = ["Agent", "Admin", "Captain", "Swarm Commander"]
            return func
        return decorator

    @staticmethod
    def everyone():
        """Decorator for commands available to everyone."""
        def decorator(func):
            func.__requires_roles__ = []
            return func
        return decorator


class BaseDiscordCog(DiscordCommandMixin):
    """Base class for all Discord cogs with common initialization."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize base Discord cog."""
        super().__init__(bot, gui_controller)


class CommandRegistry:
    """Registry for managing Discord command cogs."""

    def __init__(self):
        self._cog_classes = []
        self._cog_instances = []

    def register_cog_class(self, cog_class):
        """Register a cog class for automatic instantiation."""
        if cog_class not in self._cog_classes:
            self._cog_classes.append(cog_class)
        return cog_class

    def get_registered_cogs(self):
        """Get all registered cog classes."""
        return self._cog_classes.copy()

    def create_instances(self, bot: "UnifiedDiscordBot"):
        """Create instances of all registered cogs."""
        self._cog_instances = create_cog_instances(bot, self._cog_classes)
        return self._cog_instances

    def get_instances(self):
        """Get created cog instances."""
        return self._cog_instances.copy()


# Global registry instance
command_registry = CommandRegistry()


def register_cog(cog_class):
    """Decorator to register a cog class with the global registry."""
    command_registry.register_cog_class(cog_class)
    return cog_class


# Define command_template conditionally based on discord availability
if DISCORD_AVAILABLE:
    def command_template(error_handling: bool = True, log_command: bool = True):
        """
        Decorator template for Discord commands that eliminates repetitive code.

        Args:
            error_handling: Whether to wrap command in try/catch
            log_command: Whether to log command execution
        """
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(self, ctx: commands.Context, *args, **kwargs):
                command_name = func.__name__

                # Log command if enabled
                if log_command:
                    extra_info = ""
                    if args:
                        extra_info += f"args={args}"
                    if kwargs:
                        if extra_info:
                            extra_info += ", "
                        extra_info += f"kwargs={kwargs}"
                    self.log_command(ctx, command_name, extra_info)

                # Execute with error handling if enabled
                if error_handling:
                    try:
                        return await func(self, ctx, *args, **kwargs)
                    except Exception as e:
                        await self.handle_command_error(ctx, e, command_name)
                else:
                    return await func(self, ctx, *args, **kwargs)

            return wrapper
        return decorator
else:
    # Stub decorator when discord is not available
    def command_template(error_handling: bool = True, log_command: bool = True):
        def decorator(func):
            return func
        return decorator


# Only define EmbedBuilder if discord is available
if DISCORD_AVAILABLE:
    class EmbedBuilder:
        """Utility class for building Discord embeds with consistent styling."""

        @staticmethod
        def status_embed(title: str, status: str, description: str = "",
                        color = discord.Color.blue()) -> discord.Embed:
            """Create a status embed."""
            embed = discord.Embed(
                title=title,
                description=description,
                color=color
            )
            embed.add_field(name="Status", value=status, inline=False)
            return embed

        @staticmethod
        def list_embed(title: str, items: List[str], description: str = "",
                      color: "discord.Color" = discord.Color.blue()) -> "discord.Embed":
            """Create an embed with a list of items."""
            embed = discord.Embed(
                title=title,
                description=description,
                color=color
            )

            if items:
                item_list = "\n".join(f"• {item}" for item in items[:10])  # Limit to 10 items
                if len(items) > 10:
                    item_list += f"\n... and {len(items) - 10} more"
                embed.add_field(name="Items", value=item_list, inline=False)
            else:
                embed.add_field(name="Items", value="No items found", inline=False)

            return embed

        @staticmethod
        def progress_embed(title: str, current: int, total: int, description: str = "",
                          color = discord.Color.blue()) -> discord.Embed:
            """Create a progress embed."""
            percentage = (current / total * 100) if total > 0 else 0
            progress_bar = EmbedBuilder._create_progress_bar(percentage)

            embed = discord.Embed(
                title=title,
                description=description,
                color=color
            )
            embed.add_field(
                name="Progress",
                value=f"{progress_bar}\n{current}/{total} ({percentage:.1f}%)",
                inline=False
            )
            return embed

        @staticmethod
        def _create_progress_bar(percentage: float, length: int = 10) -> str:
            """Create a visual progress bar."""
            filled = int(length * percentage / 100)
            bar = "█" * filled + "░" * (length - filled)
            return f"`{bar}`"


# Convenience functions for bot lifecycle
def create_cog_instances(bot: "UnifiedDiscordBot", cog_classes: list) -> list:
    """Create cog instances with common parameters.

    Args:
        bot: The Discord bot instance
        cog_classes: List of cog classes to instantiate

    Returns:
        List of instantiated cog objects
    """
    return [cog_class(bot, bot.gui_controller) for cog_class in cog_classes]


async def register_cogs(bot: "UnifiedDiscordBot", cogs: list):
    """Register multiple cogs with the bot.

    Args:
        bot: The Discord bot instance
        cogs: List of cog instances to register
    """
    for cog in cogs:
        await bot.add_cog(cog)