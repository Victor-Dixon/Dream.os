"""Status Monitor Embed Factory."""

import logging
from datetime import datetime
from typing import Any

import discord

logger = logging.getLogger(__name__)


class StatusEmbedFactory:
    """Factory for creating status monitor embeds."""

    @staticmethod
    def create_status_update_embed(
        agent_id: str,
        status: dict[str, Any],
        changes: dict[str, Any],
    ) -> discord.Embed:
        """Create Discord embed for status update."""
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
            timestamp=datetime.utcnow(),
        )

        for change_key, change_value in changes.items():
            if isinstance(change_value, dict):
                old_val = change_value.get("old", "N/A")
                new_val = change_value.get("new", "N/A")
            else:
                old_val = "N/A"
                new_val = change_value
            embed.add_field(
                name=change_key.replace("_", " ").title(),
                value=f"`{old_val}` → `{new_val}`",
                inline=False,
            )

        current_phase = status.get("current_phase", "N/A")
        current_mission = status.get("current_mission", "No mission")
        embed.add_field(
            name="Current Status",
            value=(
                f"**Phase:** {current_phase[:100]}\n"
                f"**Mission:** {current_mission[:100]}"
            ),
            inline=False,
        )
        embed.set_footer(text=f"Last updated: {status.get('last_updated', 'Unknown')}")
        return embed

    @staticmethod
    def create_resumer_embed(agent_id: str, prompt: str, summary) -> discord.Embed:
        """Create embed for resumer prompt."""
        embed = discord.Embed(
            title=f"🚨 RESUMER PROMPT - {agent_id}",
            description=prompt[:2000],
            color=0xE74C3C,
            timestamp=datetime.utcnow(),
        )

        if getattr(summary, "last_activity", None):
            embed.add_field(
                name="Last Activity",
                value=(
                    f"{summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"({summary.inactivity_duration_minutes:.1f} min ago)"
                ),
                inline=False,
            )

        if getattr(summary, "activity_sources", None):
            embed.add_field(
                name="Activity Sources",
                value=", ".join(summary.activity_sources),
                inline=False,
            )

        embed.set_footer(text="Agent Activity Detector | Multi-Source Monitoring")
        return embed
