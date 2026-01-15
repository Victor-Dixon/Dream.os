#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Broadcast Controller - WOW FACTOR Dedicated Controller
======================================================

Dedicated, standalone controller for broadcasting messages.
Complete GUI interface for swarm-wide messaging.

WOW FACTOR Features:
- Custom broadcast message entry
- Agent selection (all or subset)
- Priority selection
- Broadcast templates
- Real-time delivery status

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-01-27
Status: ✅ WOW FACTOR CONTROLLER
"""

import logging

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_infrastructure import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class BroadcastControllerView(discord.ui.View):
    """
    Dedicated Broadcast Controller - WOW FACTOR Standalone Interface.
    
    Complete broadcast system in one view:
    - Custom message entry
    - Agent selection (all or subset)
    - Priority selection
    - Broadcast templates
    - Delivery tracking
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED * 2)
        self.messaging_service = messaging_service

        # Broadcast action buttons - Row 0 (max 5 per row)
        self.broadcast_all_btn = discord.ui.Button(
            label="Broadcast to All",
            style=discord.ButtonStyle.primary,
            emoji="📢",
            custom_id="broadcast_all",
            row=0,
        )
        self.broadcast_all_btn.callback = self.on_broadcast_all
        self.add_item(self.broadcast_all_btn)

        self.broadcast_select_btn = discord.ui.Button(
            label="Select Agents",
            style=discord.ButtonStyle.primary,
            emoji="🎯",
            custom_id="broadcast_select",
            row=0,
        )
        self.broadcast_select_btn.callback = self.on_broadcast_select
        self.add_item(self.broadcast_select_btn)

        self.jet_fuel_broadcast_btn = discord.ui.Button(
            label="Jet Fuel Broadcast",
            style=discord.ButtonStyle.danger,
            emoji="🚀",
            custom_id="broadcast_jet_fuel",
            row=0,
        )
        self.jet_fuel_broadcast_btn.callback = self.on_jet_fuel_broadcast
        self.add_item(self.jet_fuel_broadcast_btn)

        self.templates_btn = discord.ui.Button(
            label="Templates",
            style=discord.ButtonStyle.secondary,
            emoji="📋",
            custom_id="broadcast_templates",
            row=0,
        )
        self.templates_btn.callback = self.on_templates
        self.add_item(self.templates_btn)

    async def on_broadcast_all(self, interaction: discord.Interaction):
        """Open broadcast modal for all agents."""
        try:
            from ...discord_commander.discord_gui_modals_v2 import BroadcastMessageModal

            modal = BroadcastMessageModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening broadcast modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_broadcast_select(self, interaction: discord.Interaction):
        """Open agent selector for custom broadcast."""
        try:
            from ...discord_commander.discord_gui_modals_v2 import SelectiveBroadcastModal

            modal = SelectiveBroadcastModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening selective broadcast modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_jet_fuel_broadcast(self, interaction: discord.Interaction):
        """Open Jet Fuel broadcast modal."""
        try:
            from ...discord_commander.discord_gui_modals_v2 import JetFuelBroadcastModal

            modal = JetFuelBroadcastModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening Jet Fuel broadcast modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_templates(self, interaction: discord.Interaction):
        """Show interactive broadcast templates organized by mode."""
        try:
            from .broadcast_templates_view import BroadcastTemplatesView
            
            view = BroadcastTemplatesView(self.messaging_service)
            embed = view.create_templates_embed()
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing templates: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    def create_broadcast_embed(self) -> discord.Embed:
        """Create broadcast controller embed."""
        embed = discord.Embed(
            title="📢 BROADCAST CONTROLLER - WOW FACTOR",
            description="**Complete Swarm Broadcast System**\n\nSend messages to all or selected agents instantly.",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="🎯 Broadcast Options",
            value=(
                "• **📢 Broadcast to All** → All 8 agents\n"
                "• **🎯 Select Agents** → Choose specific agents\n"
                "• **🚀 Jet Fuel Broadcast** → AGI activation for all\n"
                "• **📋 Templates** → Quick message templates"
            ),
            inline=False,
        )

        embed.add_field(
            name="💡 Entry Fields",
            value=(
                "• **Custom Message** - Up to 2000 characters\n"
                "• **Priority** - Regular or Urgent\n"
                "• **Shift+Enter** - Line breaks ✨\n"
                "• **Instant Delivery** - PyAutoGUI to all agents"
            ),
            inline=False,
        )

        embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Powerful Broadcast Control")
        return embed


__all__ = ["BroadcastControllerView"]

