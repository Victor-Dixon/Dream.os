#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Swarm Snapshot View - Discord View for Startup Message
======================================================

Interactive Discord View component showing current swarm work snapshot.

V2 Compliance: <300 lines, single responsibility
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-10
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


class SwarmSnapshotView(discord.ui.View):
    """Interactive view showing current swarm work snapshot."""

    def __init__(self, snapshot: Dict):
        """Initialize swarm snapshot view.
        
        Args:
            snapshot: Swarm snapshot data from _get_swarm_snapshot()
        """
        super().__init__(timeout=None)  # No timeout for snapshot
        self.snapshot = snapshot
        self._setup_buttons()

    def _setup_buttons(self):
        """Setup snapshot action buttons."""
        # Refresh button to update snapshot
        refresh_btn = discord.ui.Button(
            label="🔄 Refresh Snapshot",
            style=discord.ButtonStyle.secondary,
            custom_id="snapshot_refresh",
            row=0,
        )
        refresh_btn.callback = self.refresh_snapshot
        self.add_item(refresh_btn)

        # View Details button
        details_btn = discord.ui.Button(
            label="📊 View Details",
            style=discord.ButtonStyle.primary,
            custom_id="snapshot_details",
            row=0,
        )
        details_btn.callback = self.show_details
        self.add_item(details_btn)

    def create_snapshot_embed(self) -> discord.Embed:
        """Create embed from snapshot data."""
        embed = discord.Embed(
            title="🐝 SWARM WORK SNAPSHOT",
            description="**Current Status of Agent Swarm**",
            color=0x3498DB,  # Swarm Blue
            timestamp=discord.utils.utcnow(),
        )

        # Engagement Rate
        engagement = self.snapshot.get("engagement_rate", 0.0)
        engagement_emoji = "🟢" if engagement >= 75 else "🟡" if engagement >= 50 else "🔴"
        embed.add_field(
            name=f"{engagement_emoji} Swarm Engagement",
            value=f"**{engagement:.0f}%** active ({len(self.snapshot.get('active_agents', []))}/8 agents)",
            inline=True,
        )

        # Active Agents
        active_agents = self.snapshot.get("active_agents", [])
        if active_agents:
            agent_list = []
            for agent in active_agents[:8]:  # Show all 8 if available
                priority_emoji = (
                    "🔴" if agent["priority"] == "HIGH"
                    else "🟡" if agent["priority"] == "MEDIUM"
                    else "🟢"
                )
                phase_short = agent["phase"].replace("_", " ").title()[:15]
                mission_short = agent["mission"][:60] + "..." if len(agent["mission"]) > 60 else agent["mission"]
                agent_list.append(
                    f"{priority_emoji} **{agent['id']}** | {phase_short}\n   └ {mission_short}"
                )
            
            embed.add_field(
                name=f"📊 Active Agents ({len(active_agents)})",
                value="\n".join(agent_list) if agent_list else "No active agents",
                inline=False,
            )

        # Recent Activity
        recent_activity = self.snapshot.get("recent_activity", [])
        if recent_activity:
            activity_text = "\n".join(recent_activity[:5])
            if len(recent_activity) > 5:
                activity_text += f"\n... and {len(recent_activity) - 5} more"
            embed.add_field(
                name="✅ Recent Activity",
                value=activity_text[:1024],
                inline=False,
            )

        # Current Focus
        current_focus = self.snapshot.get("current_focus", [])
        if current_focus:
            focus_text = "\n".join(current_focus[:5])
            if len(current_focus) > 5:
                focus_text += f"\n... and {len(current_focus) - 5} more"
            embed.add_field(
                name="🎯 Current Focus",
                value=focus_text[:1024],
                inline=False,
            )

        embed.set_footer(
            text="🐝 WE. ARE. SWARM. ⚡ Click buttons to interact"
        )

        return embed

    async def refresh_snapshot(self, interaction: discord.Interaction):
        """Refresh snapshot button callback."""
        try:
            await interaction.response.defer()
            
            # Re-read snapshot
            snapshot = self._get_swarm_snapshot()
            self.snapshot = snapshot
            
            # Update embed
            embed = self.create_snapshot_embed()
            await interaction.followup.send(embed=embed, view=self, ephemeral=True)
        except Exception as e:
            logger.error(f"Error refreshing snapshot: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error refreshing snapshot: {e}", ephemeral=True
                )

    async def show_details(self, interaction: discord.Interaction):
        """Show detailed snapshot button callback."""
        try:
            active_agents = self.snapshot.get("active_agents", [])
            
            if not active_agents:
                await interaction.response.send_message(
                    "ℹ️ No active agents at this time.", ephemeral=True
                )
                return
            
            # Create detailed embed
            embed = discord.Embed(
                title="📊 Detailed Swarm Status",
                description=f"**{len(active_agents)} Active Agents**",
                color=0x3498DB,
            )
            
            for agent in active_agents:
                priority_emoji = (
                    "🔴" if agent["priority"] == "HIGH"
                    else "🟡" if agent["priority"] == "MEDIUM"
                    else "🟢"
                )
                embed.add_field(
                    name=f"{priority_emoji} {agent['id']}",
                    value=(
                        f"**Phase:** {agent['phase']}\n"
                        f"**Priority:** {agent['priority']}\n"
                        f"**Mission:** {agent['mission']}"
                    ),
                    inline=True,
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing details: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    def _get_swarm_snapshot(self) -> Dict:
        """Get current swarm work snapshot (same as in unified_discord_bot)."""
        snapshot = {
            "active_agents": [],
            "recent_activity": [],
            "current_focus": [],
            "engagement_rate": 0.0,
        }
        
        try:
            workspace_root = Path("agent_workspaces")
            active_count = 0
            total_agents = 8
            
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_file = workspace_root / agent_id / "status.json"
                
                if not status_file.exists():
                    continue
                
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                    
                    agent_status = status.get("status", "")
                    if "ACTIVE" in agent_status.upper():
                        active_count += 1
                        mission = status.get("current_mission", "No active mission")[:80]
                        phase = status.get("current_phase", "Unknown")
                        priority = status.get("mission_priority", "MEDIUM")
                        
                        snapshot["active_agents"].append({
                            "id": agent_id,
                            "mission": mission,
                            "phase": phase,
                            "priority": priority,
                        })
                        
                        completed = status.get("completed_tasks", [])
                        if completed:
                            recent = completed[0][:100] if isinstance(completed[0], str) else str(completed[0])[:100]
                            snapshot["recent_activity"].append(f"{agent_id}: {recent}")
                        
                        current_tasks = status.get("current_tasks", [])
                        if current_tasks:
                            focus = current_tasks[0][:80] if isinstance(current_tasks[0], str) else str(current_tasks[0])[:80]
                            snapshot["current_focus"].append(f"{agent_id}: {focus}")
                
                except Exception as e:
                    logger.debug(f"Error reading status for {agent_id}: {e}")
                    continue
            
            snapshot["engagement_rate"] = (active_count / total_agents * 100) if total_agents > 0 else 0.0
            
        except Exception as e:
            logger.warning(f"Error getting swarm snapshot: {e}")
        
        return snapshot




