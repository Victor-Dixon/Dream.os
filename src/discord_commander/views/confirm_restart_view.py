#!/usr/bin/env python3
"""
Confirm Restart View - Discord UI Component
============================================

<!-- SSOT Domain: web -->

Confirmation view for Discord bot restart command.

Author: Agent-7 (Web Development Specialist) - V2 Refactoring
License: MIT
"""

import discord
import logging
from src.core.config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class ConfirmRestartView(discord.ui.View):
    """Confirmation view for restart command."""

    def __init__(self):
        super().__init__(timeout=TimeoutConstants.HTTP_DEFAULT)
        self.confirmed = False

    @discord.ui.button(label="Confirm Restart", emoji="🔄", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm restart button."""
        try:
            self.confirmed = True
            await interaction.response.send_message("✅ Restart confirmed", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in restart confirm: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    @discord.ui.button(label="Cancel", emoji="❌", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel restart button."""
        try:
            self.confirmed = False
            await interaction.response.send_message("❌ Cancelled", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in restart cancel: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )


