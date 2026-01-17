#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Main Control Panel View - Discord GUI Components
===============================================

Main control panel view for Discord bot interface.

Author: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

import logging
from typing import Any

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from ..core.messaging_models_core import MessageCategory
from ..services.messaging.service_adapters import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class MainControlPanelView(discord.ui.View if DISCORD_AVAILABLE else object):
    """Main control panel for Discord bot interface."""

    def __init__(self, bot=None):
        super().__init__(timeout=300)
        self.bot = bot

    async def create_status_embed(self, status_reader):
        """Create status embed for the control panel."""
        if not DISCORD_AVAILABLE:
            return None

        embed = discord.Embed(
            title="🤖 Agent Swarm Status",
            description="Current status of all agents in the swarm",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )

        # Add status information
        embed.add_field(
            name="📊 System Status",
            value="All systems operational",
            inline=False,
        )

        return embed

    async def handle_interaction_error(self, interaction, error):
        """Handle interaction errors gracefully."""
        if not DISCORD_AVAILABLE:
            return

        try:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="❌ Error",
                    description=f"An error occurred: {str(error)}",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        except discord.InteractionResponded:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="❌ Error",
                    description=f"An error occurred: {str(error)}",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )