#!/usr/bin/env python3
"""
Discord Messaging Commands - Agent Cellphone V2
==============================================

SSOT Domain: messaging

Refactored entry point for Discord messaging commands.
All core logic has been extracted into base classes and focused implementations.

Features:
- Messaging command implementations (messaging_commands_v2.py)
- Command base classes (command_base.py)
- Messaging controller integration (messaging_controller.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# MessagingCommands class is defined below - no external import needed

# Re-export base classes for extension
from .command_base import BaseDiscordCommand, MessagingCommandBase, StatusCommandBase


# === V2 FEATURES MERGED ===

"""
Messaging Commands V2 - Agent Cellphone V2
==========================================

SSOT Domain: messaging

Refactored Discord commands for agent messaging using base classes.

Features:
- Agent-to-agent messaging
- Broadcast messaging
- Status monitoring
- Command validation

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

from .command_base import MessagingCommandBase, StatusCommandBase
from .messaging_controller import DiscordMessagingController

logger = logging.getLogger(__name__)

class MessagingCommands(MessagingCommandBase):
    """Refactored Discord commands for agent messaging."""

    def __init__(self, bot, messaging_controller: DiscordMessagingController):
        super().__init__(bot, messaging_controller)

    @commands.command(name="message_agent", aliases=["msg"])
    async def message_agent(self, ctx: commands.Context, agent_id: str, *, message: str):
        """Send a message to a specific agent."""
        if not self._validate_agent_id(agent_id):
            embed = self._create_error_embed(
                "Invalid Agent ID",
                f"'{agent_id}' is not a valid agent ID. Use format: Agent-1, Agent-2, etc."
            )
            await self._safe_send(ctx, embed=embed)
            return

        result = await self._send_agent_message(agent_id, message)

        if result["success"]:
            embed = self._create_success_embed(
                "Message Sent",
                f"Message successfully sent to {agent_id}"
            )
        else:
            embed = self._create_error_embed(
                "Message Failed",
                f"Failed to send message to {agent_id}: {result.get('error', 'Unknown error')}"
            )

        await self._safe_send(ctx, embed=embed)

    @commands.command(name="broadcast", aliases=["bc"])
    async def broadcast(self, ctx: commands.Context, *, message: str):
        """Broadcast a message to all agents."""
        embed = self._create_info_embed(
            "📡 Broadcasting Message",
            f"Sending message to all agents..."
        )
        await self._safe_send(ctx, embed=embed)

        result = await self._broadcast_message(message)

        if result["success"]:
            embed = self._create_success_embed(
                "Broadcast Complete",
                f"Message sent to {result['successful']}/{result['total']} agents"
            )
        else:
            embed = self._create_error_embed(
                "Broadcast Failed",
                f"Failed to broadcast message: {result.get('error', 'Unknown error')}"
            )

        await ctx.send(embed=embed)  # Use followup for results

    @commands.command(name="swarm_status", aliases=["status"])
    async def swarm_status(self, ctx: commands.Context):
        """Display current swarm status."""
        status_cmd = StatusCommandBase(self.bot, self.messaging_controller)
        agent_statuses = status_cmd._get_agent_statuses()
        embed = status_cmd._create_status_embed(agent_statuses)
        await self._safe_send(ctx, embed=embed)

    @commands.command(name="agent_list", aliases=["agents"])
    async def agent_list(self, ctx: commands.Context):
        """List all available agents."""
        embed = self._create_info_embed(
            "🤖 Available Agents",
            "All agents in the swarm:"
        )

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            embed.add_field(
                name=agent_id,
                value="Agent messaging available",
                inline=True
            )

        await self._safe_send(ctx, embed=embed)

    @commands.command(name="agent_command", aliases=["cmd"])
    async def agent_command(self, ctx: commands.Context, agent_id: str, *, command: str):
        """Send a command to a specific agent."""
        if not self._validate_agent_id(agent_id):
            embed = self._create_error_embed(
                "Invalid Agent ID",
                f"'{agent_id}' is not a valid agent ID."
            )
            await self._safe_send(ctx, embed=embed)
            return

        # Format as command message
        command_message = f"🔧 COMMAND: {command}"

        result = await self._send_agent_message(agent_id, command_message, priority="urgent")

        if result["success"]:
            embed = self._create_success_embed(
                "Command Sent",
                f"Command sent to {agent_id}"
            )
        else:
            embed = self._create_error_embed(
                "Command Failed",
                f"Failed to send command to {agent_id}"
            )

        await self._safe_send(ctx, embed=embed)

    @commands.command(name="bump", aliases=["ping"])
    async def bump_command(self, ctx: commands.Context, *agent_numbers: int):
        """Send a bump/ping to specified agents."""
        if not agent_numbers:
            embed = self._create_error_embed(
                "No Agents Specified",
                "Please specify agent numbers: `!bump 1 2 3`"
            )
            await self._safe_send(ctx, embed=embed)
            return

        agent_ids = []
        invalid_numbers = []

        for num in agent_numbers:
            if 1 <= num <= 8:
                agent_ids.append(f"Agent-{num}")
            else:
                invalid_numbers.append(str(num))

        if invalid_numbers:
            embed = self._create_error_embed(
                "Invalid Agent Numbers",
                f"These are not valid agent numbers: {', '.join(invalid_numbers)}"
            )
            await self._safe_send(ctx, embed=embed)
            return

        bump_message = f"🔔 BUMP from {self._safe_display_name(ctx)}"

        embed = self._create_info_embed(
            "🔔 Sending Bumps",
            f"Sending bump notifications to {len(agent_ids)} agent(s)..."
        )
        await self._safe_send(ctx, embed=embed)

        result = await self._broadcast_message(bump_message, agent_ids)

        if result["success"]:
            embed = self._create_success_embed(
                "Bumps Sent",
                f"Bump notifications sent to {result['successful']}/{result['total']} agents"
            )
        else:
            embed = self._create_error_embed(
                "Bumps Failed",
                "Failed to send bump notifications"
            )

        await ctx.send(embed=embed)

    @commands.command(name="help_messaging", aliases=["help"])
    async def help_messaging(self, ctx: commands.Context):
        """Display messaging commands help."""
        embed = self._create_info_embed(
            "💬 Messaging Commands Help",
            "Available commands for agent communication:"
        )

        commands_info = [
            ("`!message_agent <agent> <message>`", "Send message to specific agent"),
            ("`!broadcast <message>`", "Send message to all agents"),
            ("`!swarm_status`", "Show current swarm status"),
            ("`!agent_list`", "List all available agents"),
            ("`!agent_command <agent> <command>`", "Send command to agent"),
            ("`!bump <numbers>`", "Send bump notification to agents"),
            ("`!help_messaging`", "Show this help message")
        ]

        for cmd, desc in commands_info:
            embed.add_field(name=cmd, value=desc, inline=False)

        embed.add_field(
            name="💡 Tips",
            value="• Use Agent-1, Agent-2, etc. for agent IDs\n• Commands are case-sensitive\n• Check `!swarm_status` for agent availability",
            inline=False
        )

        await self._safe_send(ctx, embed=embed)

async def setup(bot):
    """Setup function for Discord cog."""
    messaging_controller = DiscordMessagingController()
    await bot.add_cog(MessagingCommands(bot, messaging_controller))