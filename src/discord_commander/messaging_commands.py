"""
Discord Messaging Commands - Legacy Compatibility
=================================================

SSOT adapter for test and legacy command imports.

<!-- SSOT Domain: communication -->
"""

from __future__ import annotations

import logging
from typing import Iterable

import discord
from discord.ext import commands

from .messaging_controller import DiscordMessagingController

VALID_PRIORITIES = {"NORMAL", "HIGH", "CRITICAL"}


class MessagingCommands(commands.Cog):
    """Legacy messaging command surface for Discord."""

    def __init__(self, bot, messaging_controller: DiscordMessagingController):
        super().__init__()
        self.bot = bot
        self.messaging_controller = messaging_controller
        self.logger = logging.getLogger(__name__)

    def _normalize_priority(self, priority: str | None) -> str:
        if priority and priority.upper() in VALID_PRIORITIES:
            return priority.upper()
        return "NORMAL"

    def _success_embed(self, title: str, description: str) -> discord.Embed:
        return discord.Embed(title=f"✅ {title}", description=description, color=discord.Color.green())

    def _error_embed(self, title: str, description: str) -> discord.Embed:
        return discord.Embed(title=f"❌ {title}", description=description, color=discord.Color.red())

    @commands.command(name="message_agent", aliases=["msg"])
    async def message_agent(
        self, ctx: commands.Context, agent_id: str, message: str, priority: str = "NORMAL"
    ) -> None:
        """Send a message to a specific agent."""
        normalized_priority = self._normalize_priority(priority)
        try:
            success = await self.messaging_controller.send_agent_message(
                agent_id=agent_id, message=message, priority=normalized_priority
            )
            if success:
                embed = self._success_embed("Message Sent", f"Message sent to {agent_id}.")
            else:
                embed = self._error_embed("Message Failed", f"Failed to send message to {agent_id}.")
            await ctx.send(embed=embed)
        except Exception as exc:
            self.logger.exception("Error sending agent message: %s", exc)
            await ctx.send(embed=self._error_embed("Error", "An error occurred while sending the message."))

    @commands.command(name="agent_interact", aliases=["interact"])
    async def agent_interact(self, ctx: commands.Context) -> None:
        """Create the agent messaging interface."""
        try:
            view = self.messaging_controller.create_agent_messaging_view()
            await ctx.send(view=view)
        except Exception as exc:
            self.logger.exception("Error creating messaging interface: %s", exc)
            await ctx.send(content="Error creating interface. Please try again.")

    @commands.command(name="swarm_status", aliases=["status"])
    async def swarm_status(self, ctx: commands.Context) -> None:
        """Display current swarm status."""
        try:
            view = self.messaging_controller.create_swarm_status_view()
            embed = None
            if hasattr(view, "_create_status_embed"):
                embed = await view._create_status_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as exc:
            self.logger.exception("Error creating status view: %s", exc)
            await ctx.send(content="Error creating status view. Please try again.")

    @commands.command(name="broadcast", aliases=["bc"])
    async def broadcast(
        self, ctx: commands.Context, message: str, priority: str = "NORMAL"
    ) -> None:
        """Broadcast a message to all agents."""
        normalized_priority = self._normalize_priority(priority)
        try:
            success = await self.messaging_controller.broadcast_to_swarm(
                message=message, priority=normalized_priority
            )
            if success:
                embed = self._success_embed("Broadcast Sent", "Broadcast sent to swarm.")
            else:
                embed = self._error_embed("Broadcast Failed", "Failed to broadcast message.")
            await ctx.send(embed=embed)
        except Exception as exc:
            self.logger.exception("Error broadcasting message: %s", exc)
            await ctx.send(embed=self._error_embed("Error", "An error occurred while broadcasting."))

    @commands.command(name="agent_list", aliases=["agents"])
    async def agent_list(self, ctx: commands.Context) -> None:
        """List available agents."""
        try:
            agents = self.messaging_controller.get_agent_status()
            if not agents:
                await ctx.send(embed=self._error_embed("No Agents Found", "No agents available."))
                return
            embed = discord.Embed(
                title="🤖 Available Agents",
                description="Current swarm agents",
                color=discord.Color.blue(),
            )
            for agent_id, info in agents.items():
                status = "Active" if info.get("active") else "Inactive"
                embed.add_field(name=agent_id, value=status, inline=True)
            await ctx.send(embed=embed)
        except Exception as exc:
            self.logger.exception("Error listing agents: %s", exc)
            await ctx.send(embed=self._error_embed("Error", "Unable to list agents."))


__all__ = ["MessagingCommands"]
