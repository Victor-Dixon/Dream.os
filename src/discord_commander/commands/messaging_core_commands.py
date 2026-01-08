#!/usr/bin/env python3
"""
Messaging Core Commands - Modular V2 Compliance
===============================================

Core messaging commands (direct message, broadcast) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular core messaging commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
from typing import TYPE_CHECKING

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


class MessagingCoreCommands(commands.Cog):
    """Core messaging commands (direct messaging and broadcasting)."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize core messaging commands."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="message", description="Send message to agent")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):
        """Send direct message to agent."""
        self.logger.info(f"Command 'message' triggered by {ctx.author} to {agent_id}")
        try:
            success = await self.gui_controller.send_message(
                agent_id=agent_id,
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(name="Message", value=message_chunks[0], inline=False)
                if len(message_chunks) > 1:
                    for i, chunk in enumerate(message_chunks[1:], 2):
                        embed.add_field(
                            name=f"Message (continued {i}/{len(message_chunks)})",
                            value=chunk,
                            inline=False
                        )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Failed to send message to {agent_id}")
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="broadcast", description="Broadcast to all agents")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def broadcast(self, ctx: commands.Context, *, message: str):
        """Broadcast message to all agents."""
        self.logger.info(f"Command 'broadcast' triggered by {ctx.author}")
        try:
            success = await self.gui_controller.broadcast_message(
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Delivered to all agents",
                    color=discord.Color.green(),
                )
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(name="Message", value=message_chunks[0], inline=False)
                if len(message_chunks) > 1:
                    for i, chunk in enumerate(message_chunks[1:], 2):
                        embed.add_field(
                            name=f"Message (continued {i}/{len(message_chunks)})",
                            value=chunk,
                            inline=False
                        )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Failed to broadcast message")
        except Exception as e:
            self.logger.error(f"Error broadcasting: {e}")
            await ctx.send(f"❌ Error: {e}")


__all__ = ["MessagingCoreCommands"]