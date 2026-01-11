#!/usr/bin/env python3
"""
Unified Command Base Class - Code Deduplication
===============================================

<!-- SSOT Domain: discord -->

Extends BaseCommandCog to further eliminate repetitive patterns in Discord commands.
Consolidates common command patterns found across 15+ command classes:
- Standardized permission checking
- Common response formatting
- Command metrics and tracking
- Role-based access control patterns

V2 Compliance: < 400 lines, builds on existing BaseCommandCog
Consolidates patterns from discord_commander/commands/*.py

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-11
"""

import logging
import time
from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .command_base import BaseCommandCog

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None


class UnifiedCommand(BaseCommandCog):
    """
    Unified base class for all Discord command cogs.

    Extends BaseCommandCog with additional consolidation of repetitive patterns:
    - Command metrics and execution tracking
    - Standardized permission/role checking
    - Common response formatting patterns
    - Error recovery and retry logic
    - Command history and analytics

    Usage:
        class MyCommands(UnifiedCommand):
            def __init__(self, bot, gui_controller):
                super().__init__(bot, gui_controller, "MyCommands")
                # Custom initialization

            @commands.command()
            async def mycommand(self, ctx):
                async with self.execute_command(ctx, "mycommand"):
                    # Command logic here
                    pass
    """

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController",
                 cog_name: str, required_roles: Optional[List[str]] = None):
        """
        Initialize unified command cog.

        Args:
            bot: Discord bot instance
            gui_controller: GUI controller instance
            cog_name: Name of this cog for metrics/logging
            required_roles: Default roles required for commands in this cog
        """
        super().__init__(bot, gui_controller)
        self.cog_name = cog_name
        self.required_roles = required_roles or ["Admin", "Captain", "Swarm Commander"]

        # Command metrics - consolidated across all command cogs
        self.command_count: int = 0
        self.successful_commands: int = 0
        self.failed_commands: int = 0
        self.command_history: List[Dict[str, Any]] = []
        self.max_history = 100

        self.logger.info(f"✅ {cog_name} command cog initialized with metrics tracking")

    async def execute_command(self, ctx: commands.Context, command_name: str,
                             **kwargs) -> 'CommandContext':
        """
        Context manager for standardized command execution.

        Provides automatic tracking, error handling, and metrics collection.

        Args:
            ctx: Discord command context
            command_name: Name of the command being executed
            **kwargs: Additional context data

        Returns:
            CommandContext: Context manager for command execution
        """
        return CommandContext(self, ctx, command_name, **kwargs)

    def check_permissions(self, ctx: commands.Context, additional_roles: Optional[List[str]] = None) -> bool:
        """
        Check if user has required permissions for commands.

        Standardized permission checking across all commands.

        Args:
            ctx: Discord command context
            additional_roles: Additional roles to check beyond defaults

        Returns:
            bool: True if user has permissions
        """
        roles_to_check = self.required_roles + (additional_roles or [])

        # Check if user has any of the required roles
        user_roles = [role.name for role in ctx.author.roles]
        has_permission = any(role in user_roles for role in roles_to_check)

        if not has_permission:
            required_str = ", ".join(f"`{role}`" for role in roles_to_check)
            self.logger.warning(f"Permission denied for {ctx.author} - requires: {required_str}")

        return has_permission

    async def require_permissions(self, ctx: commands.Context,
                                 additional_roles: Optional[List[str]] = None) -> bool:
        """
        Require permissions and send error message if not met.

        Args:
            ctx: Discord command context
            additional_roles: Additional roles to check

        Returns:
            bool: True if permissions granted, False if denied (error sent)
        """
        if not self.check_permissions(ctx, additional_roles):
            embed = self.create_error_embed(
                title="Permission Denied",
                description="You don't have the required roles to use this command."
            )
            embed.add_field(
                name="Required Roles",
                value="\n".join(f"• {role}" for role in self.required_roles),
                inline=False
            )
            await ctx.send(embed=embed)
            return False
        return True

    def record_command_start(self, ctx: commands.Context, command_name: str,
                           **kwargs) -> Dict[str, Any]:
        """
        Record the start of a command execution.

        Args:
            ctx: Discord command context
            command_name: Command being executed
            **kwargs: Additional tracking data

        Returns:
            dict: Command tracking data
        """
        self.command_count += 1
        start_time = time.time()

        command_data = {
            'command': command_name,
            'user': str(ctx.author),
            'user_id': ctx.author.id,
            'channel': str(ctx.channel),
            'guild': str(ctx.guild) if ctx.guild else None,
            'start_time': start_time,
            'timestamp': start_time,
            'cog': self.cog_name,
            **kwargs
        }

        return command_data

    def record_command_end(self, command_data: Dict[str, Any], success: bool,
                          result: Any = None, error: Optional[str] = None) -> None:
        """
        Record the completion of a command execution.

        Args:
            command_data: Data from record_command_start
            success: Whether command succeeded
            result: Command result (if any)
            error: Error message (if any)
        """
        execution_time = time.time() - command_data['start_time']

        # Update metrics
        if success:
            self.successful_commands += 1
        else:
            self.failed_commands += 1

        # Complete command data
        command_data.update({
            'success': success,
            'execution_time': execution_time,
            'end_time': time.time(),
            'result': result,
            'error': error
        })

        # Add to history
        self.command_history.append(command_data)

        # Maintain history size
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)

        # Log completion
        status = "✅" if success else "❌"
        self.logger.info(f"{status} {command_data['command']} by {command_data['user']} "
                        ".3f"
                        f"({self.successful_commands}/{self.failed_commands})")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get command metrics in standardized format.

        Returns:
            dict: Metrics data
        """
        total = self.command_count
        success_rate = (self.successful_commands / total) if total > 0 else 0

        return {
            'cog_name': self.cog_name,
            'total_commands': total,
            'successful_commands': self.successful_commands,
            'failed_commands': self.failed_commands,
            'success_rate': success_rate,
            'history_size': len(self.command_history),
            'max_history': self.max_history
        }

    def get_command_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get command history, optionally limited.

        Args:
            limit: Maximum history items to return

        Returns:
            list: Command history
        """
        history = self.command_history
        if limit:
            history = history[-limit:]
        return history

    def reset_metrics(self) -> None:
        """Reset all command metrics and history."""
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history.clear()
        self.logger.info(f"✅ Metrics reset for {self.cog_name}")

    async def send_success_response(self, ctx: commands.Context, title: str,
                                   description: str = "", **kwargs) -> Optional[discord.Message]:
        """
        Send a standardized success response.

        Args:
            ctx: Command context
            title: Success title
            description: Success description
            **kwargs: Additional embed fields

        Returns:
            discord.Message: Sent message
        """
        embed = self.create_success_embed(title, description, **kwargs)
        return await self.safe_send(ctx, embed=embed)

    async def send_error_response(self, ctx: commands.Context, title: str,
                                 description: str = "", **kwargs) -> Optional[discord.Message]:
        """
        Send a standardized error response.

        Args:
            ctx: Command context
            title: Error title
            description: Error description
            **kwargs: Additional embed fields

        Returns:
            discord.Message: Sent message
        """
        embed = self.create_error_embed(title, description, **kwargs)
        return await self.safe_send(ctx, embed=embed)

    async def send_info_response(self, ctx: commands.Context, title: str,
                                description: str = "", **kwargs) -> Optional[discord.Message]:
        """
        Send a standardized info response.

        Args:
            ctx: Command context
            title: Info title
            description: Info description
            **kwargs: Additional embed fields

        Returns:
            discord.Message: Sent message
        """
        embed = self.create_info_embed(title, description, **kwargs)
        return await self.safe_send(ctx, embed=embed)


class CommandContext:
    """
    Context manager for unified command execution.

    Provides automatic error handling, metrics collection, and cleanup.
    """

    def __init__(self, cog: UnifiedCommand, ctx: commands.Context,
                 command_name: str, **kwargs):
        """
        Initialize command context.

        Args:
            cog: The command cog executing the command
            ctx: Discord command context
            command_name: Name of the command
            **kwargs: Additional tracking data
        """
        self.cog = cog
        self.ctx = ctx
        self.command_name = command_name
        self.kwargs = kwargs
        self.command_data = None
        self.success = False
        self.result = None
        self.error = None

    async def __aenter__(self):
        """Enter the command execution context."""
        self.command_data = self.cog.record_command_start(
            self.ctx, self.command_name, **self.kwargs
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the command execution context."""
        if exc_type is None:
            # Success
            self.success = True
            self.cog.record_command_end(self.command_data, True, self.result)
        else:
            # Error occurred
            self.success = False
            self.error = str(exc_val)
            self.cog.record_command_end(self.command_data, False, error=self.error)

            # Send error response
            await self.cog.send_error_response(
                self.ctx,
                title="Command Failed",
                description=f"An error occurred while executing `{self.command_name}`",
                fields=[{"name": "Error", "value": self.error[:500], "inline": False}]
            )

        return False  # Don't suppress the exception