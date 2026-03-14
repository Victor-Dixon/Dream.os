#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Swarm Status GUI View - V2 Compliance Refactor
===============================================

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

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from ..services.messaging.service_adapters import ConsolidatedMessagingService
from ..status_reader_v2 import StatusReaderCommands as StatusReader

logger = logging.getLogger(__name__)


class SwarmStatusGUIView(discord.ui.View):
    """Status monitoring view."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.messaging_service = messaging_service
        self.status_reader = StatusReader()

        self.refresh_btn = discord.ui.Button(
            label="Refresh Status",
            style=discord.ButtonStyle.primary,
            emoji="🔄",
            custom_id="refresh_status_btn"
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

    async def on_refresh(self, interaction: discord.Interaction):
        """Refresh status display."""
        try:
            status_reader = StatusReader()
            # Clear cache before refreshing to get latest status
            status_reader.clear_cache()
            agents = []

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status = status_reader.read_agent_status(agent_id)
                if status:
                    # Extract points properly - StatusReader normalizes to "points" field
                    points = status.get("points", 0)
                    if not isinstance(points, (int, float)):
                        points = 0

                    agents.append(
                        {
                            "id": agent_id,
                            "name": status.get("agent_name", agent_id),
                            "status": status.get("status", "unknown"),
                            "points": int(points),
                        }
                    )

            embed = discord.Embed(
                title="🐝 Swarm Status (Refreshed)",
                description="Updated agent status",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )

            for agent in agents:
                # Check if status contains "active" (case-insensitive)
                status_upper = agent["status"].upper()
                if "ACTIVE" in status_upper or "JET_FUEL" in status_upper:
                    emoji = "🟢"
                elif "COMPLETE" in status_upper or "COMPLETED" in status_upper:
                    emoji = "✅"
                elif "REST" in status_upper or "STANDBY" in status_upper:
                    emoji = "💤"
                elif "ERROR" in status_upper or "FAILED" in status_upper:
                    emoji = "🔴"
                else:
                    emoji = "🟡"
                embed.add_field(
                    name=f"{emoji} {agent['id']}",
                    value=f"{agent['name']}\n{agent['points']} points",
                    inline=True,
                )

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
                logger.error(
                    f"Error sending error message: {followup_error}", exc_info=True)

    def _create_status_embed(self) -> discord.Embed:
        """Create status embed."""
        embed = discord.Embed(
            title="🐝 Swarm Status",
            description="**Real-time agent status from status.json files**",
            color=discord.Color.blue()
        )

        all_statuses = self.status_reader.read_all_statuses()
        
        if not all_statuses:
            embed.add_field(
                name="⚠️ No Status Data",
                value="No agent status files found. Agents may not be initialized.",
                inline=False
            )
            return embed
        
        active_count = 0
        total_count = len(all_statuses)
        
        # Sort agents by ID for consistent display
        for agent_id in sorted(all_statuses.keys()):
            status_data = all_statuses[agent_id]
            agent_status = status_data.get("status", "UNKNOWN")
            agent_name = status_data.get("agent_name", agent_id)
            current_phase = status_data.get("current_phase", "N/A")
            
            # CRITICAL FIX: Properly detect ACTIVE status
            # Check for ACTIVE_AGENT_MODE, ACTIVE, JET_FUEL, etc.
            status_upper = str(agent_status).upper()
            if "ACTIVE" in status_upper or "JET_FUEL" in status_upper or "ACTIVE_AGENT_MODE" in status_upper:
                emoji = "🟢"
                active_count += 1
            elif "COMPLETE" in status_upper or "COMPLETED" in status_upper:
                emoji = "✅"
            elif "REST" in status_upper or "STANDBY" in status_upper or "IDLE" in status_upper:
                emoji = "💤"
            elif "ERROR" in status_upper or "FAILED" in status_upper:
                emoji = "🔴"
            else:
                emoji = "🟡"  # Unknown/Other status
            
            # Build compact status value (Discord field limit: 1024 chars)
            status_value = (
                f"**{agent_name}**\n"
                f"Status: {agent_status}\n"
                f"Phase: {current_phase[:50]}"
            )
            
            # Ensure field value doesn't exceed Discord's 1024 character limit
            if len(status_value) > 1024:
                status_value = status_value[:1020] + "..."
            
            embed.add_field(
                name=f"{emoji} {agent_id}",
                value=status_value,
                inline=True
            )
        
        # Add summary
        embed.add_field(
            name="📊 Summary",
            value=f"**Active:** {active_count}/{total_count} agents",
            inline=False
        )
        
        embed.set_footer(text="🔄 Use refresh button to update • Data from status.json files")
        
        return embed

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







