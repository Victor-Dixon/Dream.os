"""
Status Monitor Embed Factory
============================

Helper module for creating Discord embeds for the Status Monitor.
Extracted from status_change_monitor.py for V2 compliance.
"""

import logging
from datetime import datetime
import discord

logger = logging.getLogger(__name__)

class StatusEmbedFactory:
    """Factory for creating status monitor embeds."""

    @staticmethod
    def create_status_update_embed(agent_id: str, status: dict, changes: dict) -> discord.Embed:
        """Create Discord embed for status update."""
        # Status emoji
        status_val = status.get("status", "UNKNOWN")
        if "ACTIVE" in status_val.upper():
            emoji = "🟢"
            color = 0x27AE60
        elif "COMPLETE" in status_val.upper():
            emoji = "✅"
            color = 0x3498DB
        elif "BLOCKED" in status_val.upper():
            emoji = "🔴"
            color = 0xE74C3C
        else:
            emoji = "🟡"
            color = 0xF39C12

        embed = discord.Embed(
            title=f"{emoji} {agent_id} Status Update",
            description=f"**{status.get('agent_name', 'Agent')}** status changed",
            color=color,
            timestamp=datetime.utcnow()
        )

        # Add change details
        if "status" in changes:
            embed.add_field(
                name="Status Change",
                value=f"`{changes['status']['old']}` → `{changes['status']['new']}`",
                inline=False
            )

        if "phase" in changes:
            embed.add_field(
                name="Phase Change",
                value=f"`{changes['phase']['old'][:50]}` → `{changes['phase']['new'][:50]}`",
                inline=False
            )

        if "mission" in changes:
            embed.add_field(
                name="Mission Change",
                value=f"`{changes['mission']['old'][:50]}` → `{changes['mission']['new'][:50]}`",
                inline=False
            )

        if "completed_tasks" in changes:
            tasks_list = "\n".join(
                [f"✅ {task[:80]}" for task in changes["completed_tasks"][:5]])
            if len(changes["completed_tasks"]) > 5:
                tasks_list += f"\n... and {len(changes['completed_tasks']) - 5} more"
            embed.add_field(
                name="Tasks Completed",
                value=tasks_list or "None",
                inline=False
            )

        if "points_earned" in changes:
            embed.add_field(
                name="Points Earned",
                value=f"+{changes['points_earned']} points",
                inline=True
            )

        # Current status summary
        current_phase = status.get("current_phase", "N/A")
        current_mission = status.get("current_mission", "No mission")
        embed.add_field(
            name="Current Status",
            value=f"**Phase:** {current_phase[:100]}\n**Mission:** {current_mission[:100]}",
            inline=False
        )

        embed.set_footer(
            text=f"Last updated: {status.get('last_updated', 'Unknown')}")

        return embed

    @staticmethod
    def create_resumer_embed(agent_id: str, prompt: str, summary) -> discord.Embed:
        """Create embed for resumer prompt."""
        embed = discord.Embed(
            title=f"🚨 RESUMER PROMPT - {agent_id}",
            description=prompt[:2000],  # Discord embed limit
            color=0xE74C3C,  # Red for urgency
            timestamp=datetime.utcnow()
        )

        # Add activity summary
        if summary.last_activity:
            embed.add_field(
                name="Last Activity",
                value=f"{summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')} ({summary.inactivity_duration_minutes:.1f} min ago)",
                inline=False
            )

        if summary.activity_sources:
            embed.add_field(
                name="Activity Sources",
                value=", ".join(summary.activity_sources),
                inline=False
            )

        embed.set_footer(
            text="Agent Activity Detector | Multi-Source Monitoring")
            
        return embed
