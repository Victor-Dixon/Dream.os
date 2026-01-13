#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Status Controller - WOW FACTOR Dedicated Controller
===================================================

Dedicated, standalone controller for swarm status monitoring.
Complete GUI interface for real-time status tracking.

WOW FACTOR Features:
- Real-time agent status
- Points and mission tracking
- Live refresh capability
- Status filters
- Detailed agent views

<<<<<<< HEAD
V2 Consolidated: Uses SSOT base classes for standardized patterns
Author: Agent-6 (Coordination & Communication Specialist)
SSOT Migration: Agent-8 (System Integration)
Date: 2026-01-12
=======
Author: Agent-6 (Coordination & Communication Specialist)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
Created: 2025-01-27
Status: ✅ WOW FACTOR CONTROLLER
"""

<<<<<<< HEAD
# SSOT Import Standardization - eliminates redundant typing imports
from src.core.base.import_standardization import logging, Any
from src.core.base.service_base import BaseService
from src.core.base.error_handling import ErrorHandler, error_context
=======
import logging
from typing import Any
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

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


class StatusControllerView(discord.ui.View):
    """
    Dedicated Status Controller - WOW FACTOR Standalone Interface.
    
    Complete status monitoring system in one view:
    - Real-time agent status
    - Points and mission tracking
    - Live refresh
    - Status filters
    - Detailed agent information
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.messaging_service = messaging_service
        self.status_reader = StatusReader()

        # Status action buttons - Row 0 (max 5 per row)
        self.refresh_btn = discord.ui.Button(
            label="Refresh Status",
            style=discord.ButtonStyle.primary,
            emoji="🔄",
            custom_id="status_refresh",
            row=0,
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

        self.filter_active_btn = discord.ui.Button(
            label="Active Only",
            style=discord.ButtonStyle.primary,  # Fixed: success doesn't exist, use primary
            emoji="🟢",
            custom_id="status_filter_active",
            row=0,
        )
        self.filter_active_btn.callback = self.on_filter_active
        self.add_item(self.filter_active_btn)

        self.filter_idle_btn = discord.ui.Button(
            label="Idle Agents",
            style=discord.ButtonStyle.secondary,
            emoji="🟡",
            custom_id="status_filter_idle",
            row=0,
        )
        self.filter_idle_btn.callback = self.on_filter_idle
        self.add_item(self.filter_idle_btn)

        self.message_idle_btn = discord.ui.Button(
            label="Message Idle",
            style=discord.ButtonStyle.danger,
            emoji="⛽",
            custom_id="status_message_idle",
            row=0,
        )
        self.message_idle_btn.callback = self.on_message_idle
        self.add_item(self.message_idle_btn)

        # Status Monitor Controls (row 1)
        self.monitor_start_btn = discord.ui.Button(
            label="Start Monitor",
            style=discord.ButtonStyle.success,
            emoji="▶️",
            custom_id="status_monitor_start",
            row=1,
        )
        self.monitor_start_btn.callback = self.on_monitor_start
        self.add_item(self.monitor_start_btn)

        self.monitor_stop_btn = discord.ui.Button(
            label="Stop Monitor",
            style=discord.ButtonStyle.secondary,
            emoji="⏸️",
            custom_id="status_monitor_stop",
            row=1,
        )
        self.monitor_stop_btn.callback = self.on_monitor_stop
        self.add_item(self.monitor_stop_btn)

    async def on_refresh(self, interaction: discord.Interaction):
        """Refresh status display."""
        try:
            embed = self._create_status_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(f"Error refreshing status: {e}", exc_info=True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ Error refreshing status: {e}", ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"❌ Error refreshing status: {e}", ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending error message: {followup_error}", exc_info=True)

    async def on_filter_active(self, interaction: discord.Interaction):
        """Show only active agents."""
        try:
            embed = self._create_status_embed(filter_status="active")
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(f"Error filtering active agents: {e}", exc_info=True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ Error: {e}", ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"❌ Error: {e}", ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending error message: {followup_error}", exc_info=True)

    async def on_filter_idle(self, interaction: discord.Interaction):
        """Show only idle agents."""
        try:
            embed = self._create_status_embed(filter_status="idle")
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(f"Error filtering idle agents: {e}", exc_info=True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ Error: {e}", ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"❌ Error: {e}", ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending error message: {followup_error}", exc_info=True)

    async def on_message_idle(self, interaction: discord.Interaction):
        """Send gas message to idle agents."""
        try:
            all_statuses = self.status_reader.read_all_statuses()
            idle_agents = []

            for agent_id in [f"Agent-{i}" for i in range(1, 9)]:
                status_data = all_statuses.get(agent_id, {})
                status = status_data.get("status", "").lower()
                
                if status == "idle" or not status_data.get("current_task"):
                    idle_agents.append(agent_id)

            if not idle_agents:
                await interaction.response.send_message(
                    "✅ No idle agents found! All agents are active!", ephemeral=True
                )
                return

            # Open broadcast modal for idle agents
            from ...discord_commander.discord_gui_modals import SelectiveBroadcastModal

            modal = SelectiveBroadcastModal(self.messaging_service, default_agents=idle_agents)
            await interaction.response.send_modal(modal)

        except Exception as e:
            logger.error(f"Error messaging idle agents: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    async def on_monitor_start(self, interaction: discord.Interaction):
        """Start the status monitor via UI control."""
        try:
            bot = interaction.client
            if hasattr(bot, "status_monitor"):
                bot.status_monitor.start_monitoring()
                await interaction.response.send_message(
                    "✅ Status monitor started (15s interval).", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "⚠️ Status monitor not initialized yet.", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error starting monitor: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    async def on_monitor_stop(self, interaction: discord.Interaction):
        """Stop the status monitor via UI control."""
        try:
            bot = interaction.client
            if hasattr(bot, "status_monitor"):
                bot.status_monitor.stop_monitoring()
                await interaction.response.send_message(
                    "🛑 Status monitor stopped.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "⚠️ Status monitor not initialized.", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error stopping monitor: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    def _create_status_embed(self, filter_status: str | None = None) -> discord.Embed:
        """Create status embed with optional filtering."""
        try:
            all_statuses = self.status_reader.read_all_statuses()
            agents = []

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})

                agent_status = status_data.get("status", "unknown").lower()
                
                # Apply filter
                if filter_status and agent_status != filter_status:
                    continue

                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", agent_id),
                        "status": agent_status,
                        "points": self._extract_points(status_data.get("points_earned", 0)),
                        "mission": status_data.get("current_mission", "No mission")[:50],
                        "task": status_data.get("current_tasks", [""])[0][:40] if status_data.get("current_tasks") else "None",
                    }
                )

            # Create embed
            title = "📊 STATUS CONTROLLER - WOW FACTOR"
            if filter_status:
                title += f" ({filter_status.upper()} only)"
            
            embed = discord.Embed(
                title=title,
                description="**Real-Time Swarm Status Monitoring**\n\nLive agent status with points and mission tracking.",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )

            # Add agent status fields
            for agent in agents:
                emoji = self._get_status_emoji(agent["status"])
                embed.add_field(
                    name=f"{emoji} {agent['id']}",
                    value=(
                        f"**{agent['name']}**\n"
                        f"📊 {agent['points']} pts\n"
                        f"🎯 {agent['mission']}\n"
                        f"⚡ {agent['task']}"
                    ),
                    inline=True,
                )

            # Add summary
            active_count = sum(1 for a in agents if a["status"] == "active")
            idle_count = sum(1 for a in agents if a["status"] == "idle")
            total_points = sum(a["points"] for a in agents)

            embed.add_field(
                name="📊 Summary",
                value=(
                    f"**Active**: {active_count} | **Idle**: {idle_count} | **Total**: {len(agents)}/8\n"
                    f"**Total Points**: {total_points:,}"
                ),
                inline=False,
            )

            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Live Status Monitoring")
            return embed

        except Exception as e:
            logger.error(f"Error creating status embed: {e}")
            embed = discord.Embed(
                title="❌ Status Error",
                description=f"Failed to load status: {str(e)}",
                color=discord.Color.red(),
            )
            return embed

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


__all__ = ["StatusControllerView"]

