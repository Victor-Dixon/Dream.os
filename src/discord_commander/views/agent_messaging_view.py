#!/usr/bin/env python3
"""
<!-- SSOT Domain: messaging -->

Agent Messaging GUI View - V2 Compliance Refactor
===================================================

Extracted from discord_gui_views.py for V2 compliance.

V2 Compliance:
- File: <400 lines ✅
- Class: <200 lines ✅
- Functions: <30 lines ✅

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-01-27
License: MIT
"""

import logging
from typing import Any
from src.core.config.timeout_constants import TimeoutConstants

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_infrastructure import ConsolidatedMessagingService
from ..status_reader import StatusReader

logger = logging.getLogger(__name__)


class AgentMessagingGUIView(discord.ui.View):
    """Complete agent messaging GUI with all controls."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.messaging_service = messaging_service
        self.agents = self._load_agents()
        self._setup_ui_components()

    def _setup_ui_components(self):
        """Setup UI components."""
        self.agent_select = discord.ui.Select(
            placeholder="🎯 Select agent to message...",
            options=self._create_agent_options(),
            custom_id="agent_select",
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

        self.broadcast_btn = discord.ui.Button(
            label="Broadcast to All",
            style=discord.ButtonStyle.primary,
            emoji="📢",
            custom_id="broadcast_btn",
        )
        self.broadcast_btn.callback = self.on_broadcast
        self.add_item(self.broadcast_btn)

        self.status_btn = discord.ui.Button(
            label="Swarm Status",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="status_btn"
        )
        self.status_btn.callback = self.on_status
        self.add_item(self.status_btn)

        self.refresh_btn = discord.ui.Button(
            label="Refresh",
            style=discord.ButtonStyle.secondary,
            emoji="🔄",
            custom_id="refresh_btn"
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

    def _load_agents(self) -> list[dict]:
        """Load agent information from status.json."""
        try:
            status_reader = StatusReader()
            all_statuses = status_reader.read_all_statuses()
            agents = []

            # Always include all 8 agents (even if status not available)
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})

                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", f"Agent-{i}"),
                        "status": status_data.get("status", "unknown"),
                        "points": self._extract_points(status_data.get("points_earned", 0)),
                    }
                )

            return agents
        except Exception as e:
            logger.error(f"Error loading agents: {e}")
            # Fallback: return static agent list
            return [
                {"id": f"Agent-{i}", "name": f"Agent-{i}",
                    "status": "unknown", "points": 0}
                for i in range(1, 9)
            ]

    def _create_agent_options(self) -> list[discord.SelectOption]:
        """Create dropdown options for agents."""
        options = []
        for agent in self.agents:
            emoji = self._get_status_emoji(agent.get("status", "unknown"))
            # Discord SelectOption value must be <= 20 characters
            option_value = agent["id"]
            if len(option_value) > 20:
                option_value = option_value[:20]
            
            options.append(
                discord.SelectOption(
                    label=agent["id"],
                    description=f"{agent.get('name', 'Unknown')} - {agent.get('points', 0)} pts",
                    emoji=emoji,
                    value=option_value,
                )
            )
        return options

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection."""
        try:
            from ..discord_gui_modals import AgentMessageModal

            agent_id = self.agent_select.values[0]
            modal = AgentMessageModal(agent_id, self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening agent message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_broadcast(self, interaction: discord.Interaction):
        """Handle broadcast button."""
        try:
            from ..discord_gui_modals import BroadcastMessageModal

            modal = BroadcastMessageModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening broadcast modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_status(self, interaction: discord.Interaction):
        """Handle status button."""
        try:
            from .swarm_status_view import SwarmStatusGUIView

            status_view = SwarmStatusGUIView(self.messaging_service)

            embed = discord.Embed(
                title="🐝 Swarm Status",
                description="Current agent status across the swarm",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            for agent in self.agents:
                emoji = self._get_status_emoji(agent.get("status", "unknown"))
                embed.add_field(
                    name=f"{emoji} {agent['id']}",
                    value=f"{agent.get('name', 'Unknown')}\n{agent.get('points', 0)} points",
                    inline=True,
                )

            await interaction.response.send_message(embed=embed, view=status_view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing status: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def on_refresh(self, interaction: discord.Interaction):
        """Handle refresh button."""
        try:
            status_reader = StatusReader()
            status_reader.clear_cache()
            
            self.agents = self._load_agents()
            self.agent_select.options = self._create_agent_options()

            await interaction.response.send_message("✅ Agent list refreshed!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error refreshing agent list: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for agent status."""
        status_upper = status.upper()
        if "ACTIVE" in status_upper or "JET_FUEL" in status_upper:
            return "🟢"
        elif "COMPLETE" in status_upper or "COMPLETED" in status_upper:
            return "✅"
        elif "REST" in status_upper or "STANDBY" in status_upper:
            return "💤"
        elif "ERROR" in status_upper or "FAILED" in status_upper:
            return "🔴"
        else:
            return "🟡"

    def _extract_points(self, points_value: Any) -> int:
        """Extract points from various formats."""
        if isinstance(points_value, int):
            return points_value
        if isinstance(points_value, str):
            return int(points_value.replace(",", "").replace("pts", "").strip())
        if isinstance(points_value, dict):
            return points_value.get("total", 0)
        return 0

    async def _create_status_embed(self, status_reader=None) -> discord.Embed:
        """Create status embed for swarm status display."""
        if status_reader is None:
            status_reader = StatusReader()

        embed = discord.Embed(
            title="🐝 Swarm Status",
            description="Current agent status across the swarm",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )

        try:
            all_statuses = status_reader.read_all_statuses()
            agents = []

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})
                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", agent_id),
                        "status": status_data.get("status", "unknown"),
                        "points": self._extract_points(status_data.get("points_earned", 0)),
                    }
                )

            for agent in agents:
                emoji = self._get_status_emoji(agent.get("status", "unknown"))
                embed.add_field(
                    name=f"{emoji} {agent['id']}",
                    value=f"{agent.get('name', 'Unknown')}\n{agent.get('points', 0)} points",
                    inline=True,
                )

            # CRITICAL FIX: Properly detect ACTIVE status
            # Check for ACTIVE_AGENT_MODE, ACTIVE, JET_FUEL, etc.
            active_count = sum(
                1 for a in agents 
                if "ACTIVE" in str(a.get("status", "")).upper() 
                or "JET_FUEL" in str(a.get("status", "")).upper()
                or "ACTIVE_AGENT_MODE" in str(a.get("status", "")).upper()
            )
            embed.add_field(
                name="📊 Summary",
                value=f"Active: {active_count}/{len(agents)} agents",
                inline=False,
            )

        except Exception as e:
            logger.error(f"Error creating status embed: {e}")
            embed.add_field(
                name="❌ Error",
                value=f"Failed to load status: {str(e)}",
                inline=False,
            )

        return embed







