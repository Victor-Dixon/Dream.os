#!/usr/bin/env python3
"""
<!-- SSOT Domain: messaging -->

Messaging Controller - WOW FACTOR Dedicated Controller
=======================================================

Dedicated, standalone controller for agent messaging.
Complete GUI interface with all messaging features.

WOW FACTOR Features:
- Agent selector dropdown with live status
- Custom message entry modal
- Priority selection
- Real-time agent status indicators
- Broadcast quick access

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-01-27
Status: ✅ WOW FACTOR CONTROLLER
"""

import logging
from typing import Any

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    # Use unified test utilities when discord.py is not available
    from ..test_utils import get_mock_discord
    
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

from src.services.messaging_infrastructure import ConsolidatedMessagingService

from ..status_reader_v2 import StatusReaderCommands as StatusReader

logger = logging.getLogger(__name__)


class MessagingControllerView(discord.ui.View):
    """
    Dedicated Messaging Controller - WOW FACTOR Standalone Interface.
    
    Complete agent messaging system in one view:
    - Agent selector dropdown with live status
    - Custom message composition
    - Priority selection
    - Broadcast capabilities
    - Real-time status monitoring
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED * 2)  # 10 minute timeout
        self.messaging_service = messaging_service
        # Load agents synchronously for initialization (cached, should be fast)
        self.agents = self._load_agents()

        # Agent selection dropdown (WOW FACTOR: Live status indicators!)
        self.agent_select = discord.ui.Select(
            placeholder="🎯 Select agent to message...",
            options=self._create_agent_options(),
            custom_id="messaging_agent_select",
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

        # Quick message buttons (WOW FACTOR: Instant access!) - Row 1
        self.broadcast_btn = discord.ui.Button(
            label="Broadcast to All",
            style=discord.ButtonStyle.primary,
            emoji="📢",
            custom_id="messaging_broadcast",
            row=1,
        )
        self.broadcast_btn.callback = self.on_broadcast
        self.add_item(self.broadcast_btn)

        self.quick_gas_btn = discord.ui.Button(
            label="Jet Fuel Message",
            style=discord.ButtonStyle.danger,
            emoji="🚀",
            custom_id="messaging_jet_fuel",
            row=1,
        )
        self.quick_gas_btn.callback = self.on_jet_fuel_message
        self.add_item(self.quick_gas_btn)

        self.status_btn = discord.ui.Button(
            label="Live Status",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="messaging_status",
            row=1,
        )
        self.status_btn.callback = self.on_status
        self.add_item(self.status_btn)

        self.refresh_btn = discord.ui.Button(
            label="Refresh Agents",
            style=discord.ButtonStyle.secondary,
            emoji="🔄",
            custom_id="messaging_refresh",
            row=1,
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

    async def _load_agents_async(self) -> list[dict]:
        """Load agent information with live status (async version)."""
        try:
            status_reader = StatusReader()
            all_statuses = await status_reader.read_all_statuses_async()
            agents = []

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})

                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", f"Agent-{i}"),
                        "status": status_data.get("status", "unknown"),
                        "points": self._extract_points(status_data.get("points_earned", 0)),
                        "mission": status_data.get("current_mission", "No mission")[:50],
                    }
                )

            return agents
        except Exception as e:
            logger.error(f"Error loading agents: {e}")
            return [
                {"id": f"Agent-{i}", "name": f"Agent-{i}", "status": "unknown", "points": 0, "mission": "Unknown"}
                for i in range(1, 9)
            ]

    def _load_agents(self) -> list[dict]:
        """Load agent information with live status (synchronous version for backward compatibility)."""
        try:
            status_reader = StatusReader()
            all_statuses = status_reader.read_all_statuses()
            agents = []

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})

                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", f"Agent-{i}"),
                        "status": status_data.get("status", "unknown"),
                        "points": self._extract_points(status_data.get("points_earned", 0)),
                        "mission": status_data.get("current_mission", "No mission")[:50],
                    }
                )

            return agents
        except Exception as e:
            logger.error(f"Error loading agents: {e}")
            return [
                {"id": f"Agent-{i}", "name": f"Agent-{i}", "status": "unknown", "points": 0, "mission": "Unknown"}
                for i in range(1, 9)
            ]

    def _create_agent_options(self) -> list[discord.SelectOption]:
        """Create dropdown options with live status indicators."""
        options = []
        for agent in self.agents:
            emoji = self._get_status_emoji(agent.get("status", "unknown"))
            status_text = agent.get("status", "unknown").upper()
            
            # Discord label must be 1-45 characters, description max 100
            label = agent["id"]
            if not label or len(label) < 1:
                label = f"Agent-{agent.get('id', 'Unknown')}"[:45]
            label = label[:45] if len(label) > 45 else label
            
            # Description max 100 characters
            mission = agent.get('mission', '')[:40] if agent.get('mission') else ''
            description = f"{status_text} - {agent.get('points', 0)} pts"
            if mission:
                remaining = 100 - len(description) - 3  # 3 for " - "
                if remaining > 0:
                    description = f"{description} - {mission[:remaining]}"
            description = description[:100] if len(description) > 100 else description
            
            # Discord SelectOption value must be <= 20 characters
            option_value = agent["id"]
            if len(option_value) > 20:
                option_value = option_value[:20]
                logger.warning(f"Truncated SelectOption value for {agent['id']} to {option_value}")
            
            options.append(
                discord.SelectOption(
                    label=label,
                    description=description,
                    emoji=emoji,
                    value=option_value,
                )
            )
        return options

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection - opens custom message modal."""
        try:
            from ...discord_commander.discord_gui_modals_v2 import AgentMessageModal

            agent_id = self.agent_select.values[0]
            modal = AgentMessageModal(agent_id, self.messaging_service)
            
            await interaction.response.send_modal(modal)
        except discord.errors.HTTPException as e:
            # Handle interaction already acknowledged errors
            if "already been acknowledged" in str(e):
                logger.warning(f"Interaction already acknowledged for agent select: {e}")
                # Try to send as followup instead
                try:
                    await interaction.followup.send(
                        f"⚠️ Interaction already processed. Please try selecting an agent again.",
                        ephemeral=True
                    )
                except Exception as followup_error:
                    logger.error(f"Failed to send followup message: {followup_error}")
            else:
                logger.error(f"HTTP error opening agent message modal: {e}", exc_info=True)
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ Error: {e}", ephemeral=True
                    )
        except Exception as e:
            logger.error(f"Error opening agent message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_broadcast(self, interaction: discord.Interaction):
        """Handle broadcast button - opens broadcast modal."""
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

    async def on_jet_fuel_message(self, interaction: discord.Interaction):
        """Handle Jet Fuel message button - opens Jet Fuel modal."""
        try:
            from ...discord_commander.discord_gui_modals_v2 import JetFuelMessageModal

            modal = JetFuelMessageModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening Jet Fuel modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_status(self, interaction: discord.Interaction):
        """Handle status button - shows live swarm status."""
        try:
            from ...discord_commander.controllers.status_controller_view import StatusControllerView

            view = StatusControllerView(self.messaging_service)
            embed = view._create_status_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing status: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_refresh(self, interaction: discord.Interaction):
        """Handle refresh button - reloads agent list."""
        try:
            # Use async version to avoid blocking event loop
            self.agents = await self._load_agents_async()
            self.agent_select.options = self._create_agent_options()

            await interaction.response.send_message("✅ Agent list refreshed with latest status!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error refreshing agent list: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for agent status."""
        status_emojis = {
            "active": "🟢",
            "idle": "🟡",
            "busy": "🔴",
            "offline": "⚫",
            "unknown": "❓",
            "autonomous": "🚀",
            "complete": "✅",
        }
        return status_emojis.get(status.lower(), "❓")

    def _extract_points(self, points_value: Any) -> int:
        """Extract points from various formats."""
        if isinstance(points_value, int):
            return points_value
        if isinstance(points_value, str):
            try:
                return int(points_value.replace(",", "").replace("pts", "").strip())
            except:
                return 0
        if isinstance(points_value, dict):
            return points_value.get("total", 0)
        return 0

    def create_messaging_embed(self) -> discord.Embed:
        """Create messaging controller embed."""
        embed = discord.Embed(
            title="📨 MESSAGING CONTROLLER - WOW FACTOR",
            description="**Complete Agent Messaging System**\n\nSelect agent from dropdown to compose custom message.",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="🎯 Quick Actions",
            value=(
                "• **Select Agent** from dropdown → Opens message modal\n"
                "• **📢 Broadcast** → Message all 8 agents\n"
                "• **🚀 Jet Fuel** → Send AGI activation message\n"
                "• **📊 Live Status** → View swarm status\n"
                "• **🔄 Refresh** → Reload agent list"
            ),
            inline=False,
        )

        embed.add_field(
            name="💡 Entry Fields",
            value=(
                "• **Custom Message** - Up to 2000 characters\n"
                "• **Priority Selection** - Regular or Urgent\n"
                "• **Shift+Enter** - Line breaks ✨\n"
                "• **Instant Delivery** - PyAutoGUI activation"
            ),
            inline=False,
        )

        active_count = sum(1 for a in self.agents if a.get("status", "").lower() == "active")
        embed.add_field(
            name="📊 Swarm Status",
            value=f"**Active**: {active_count}/8 agents | **Total Points**: {sum(a.get('points', 0) for a in self.agents)}",
            inline=False,
        )

        embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Interactive Messaging Controller")
        return embed


__all__ = ["MessagingControllerView"]

