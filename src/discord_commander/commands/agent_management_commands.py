"""
<!-- SSOT Domain: discord -->

Agent Management Commands
=========================

Agent management commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Self-healing system commands.

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import asyncio
import logging

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)



    """Agent management commands for system health."""

    def __init__(self, bot, gui_controller):
        """Initialize agent management commands."""
        self.bot = bot
        self.gui_controller = gui_controller

    async def heal(self, ctx: commands.Context, action: str = "status", agent_id: str = None):
        """
        Self-healing system commands.

        Usage:
        !heal status - Show healing statistics
        !heal check - Immediately check and heal all stalled agents
        !heal stats [Agent-X] - Show detailed stats for agent (or all agents)
        !heal cancel_count [Agent-X] - Show terminal cancellation count today
        """
        self.logger.info(f"Command 'heal' triggered by {ctx.author} with args: action={action}, agent_id={agent_id}")



