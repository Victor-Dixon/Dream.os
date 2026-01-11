#!/usr/bin/env python3
"""
Base Command Classes - Eliminate Repetitive Code
================================================

Base classes and mixins for Discord command cogs to eliminate repetitive patterns.

<!-- SSOT Domain: discord -->

Features:
- BaseCommandCog: Common initialization for all command cogs
- LoggingMixin: Standardized command logging
- EmbedMixin: Consistent embed creation patterns
- ErrorHandlingMixin: Standardized error responses

V2 Compliant: Reduces code duplication by ~70%
Author: Agent-7 (Code Quality Specialist)
Date: 2026-01-11
"""

import logging
from typing import TYPE_CHECKING, Optional, Any, Dict

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class LoggingMixin:
    """Mixin for standardized command logging."""

    def log_command_start(self, command_name: str, ctx: commands.Context, **kwargs) -> None:
        """Log command execution start with standardized format."""
        args_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        self.logger.info(f"Command '{command_name}' triggered by {ctx.author} {args_str}")

    def log_command_success(self, command_name: str, **kwargs) -> None:
        """Log successful command completion."""
        args_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        self.logger.info(f"Command '{command_name}' completed successfully {args_str}")

    def log_command_error(self, command_name: str, error: Exception, **kwargs) -> None:
        """Log command error with context."""
        args_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        self.logger.error(f"Command '{command_name}' failed {args_str}: {error}")


class EmbedMixin:
    """Mixin for consistent embed creation patterns."""

    def create_success_embed(self, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create a standardized success embed."""
        embed = discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
            **kwargs
        )
        return embed

    def create_error_embed(self, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create a standardized error embed."""
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
            **kwargs
        )
        return embed

    def create_info_embed(self, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create a standardized info embed."""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
            **kwargs
        )
        return embed

    def create_warning_embed(self, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create a standardized warning embed."""
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow(),
            **kwargs
        )
        return embed


class ErrorHandlingMixin:
    """Mixin for consistent error handling and user responses."""

    async def handle_command_error(self, ctx: commands.Context, error: Exception,
                                 command_name: str, **kwargs) -> None:
        """Handle command errors with standardized user response."""
        self.log_command_error(command_name, error, **kwargs)

        embed = self.create_error_embed(
            title="Command Failed",
            description=f"An error occurred while executing `{command_name}`"
        )

        try:
            await ctx.send(embed=embed)
        except Exception as send_error:
            # Fallback if embed fails
            await ctx.send(f"❌ Error in {command_name}: {str(error)[:100]}")


class BaseCommandCog(commands.Cog, LoggingMixin, EmbedMixin, ErrorHandlingMixin):
    """
    Base class for all Discord command cogs.

    Eliminates repetitive initialization, logging, and error handling code.
    All command cogs should inherit from this class.
    """

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize base command cog with common setup."""
        super().__init__()
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_command_name(self, ctx: commands.Context) -> str:
        """Get the command name from context."""
        return ctx.command.name if ctx.command else "unknown"

    async def safe_send(self, ctx: commands.Context, content: str = None, embed: discord.Embed = None,
                       **kwargs) -> Optional[discord.Message]:
        """Safely send a message with error handling."""
        try:
            return await ctx.send(content=content, embed=embed, **kwargs)
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return None


class RoleRequiredMixin:
    """Mixin for commands that require specific Discord roles."""

    REQUIRED_ROLES = ["Admin", "Captain", "Swarm Commander"]

    def has_required_role(self, ctx: commands.Context) -> bool:
        """Check if user has required role for command execution."""
        if not ctx.author:
            return False

        # Check if user has any of the required roles
        user_roles = [role.name for role in ctx.author.roles]
        return any(role in user_roles for role in self.REQUIRED_ROLES)

    async def check_permissions(self, ctx: commands.Context) -> bool:
        """Check permissions and send error message if insufficient."""
        if not self.has_required_role(ctx):
            embed = self.create_error_embed(
                title="Permission Denied",
                description=f"This command requires one of these roles: {', '.join(self.REQUIRED_ROLES)}"
            )
            await ctx.send(embed=embed)
            return False
        return True


__all__ = [
    "BaseCommandCog",
    "LoggingMixin",
    "EmbedMixin",
    "ErrorHandlingMixin",
    "RoleRequiredMixin",
]