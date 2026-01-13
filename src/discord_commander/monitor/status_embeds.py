"""
Status Monitor Embed Factory
============================

<<<<<<< HEAD
<!-- SSOT Domain: discord -->

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
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
<<<<<<< HEAD
        # Ensure status is a dict
        if status is None:
            status = {}

        # Ensure changes is a dict
        if changes is None:
            changes = {}

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
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
<<<<<<< HEAD
        if "status" in changes and isinstance(changes["status"], dict):
            status_change = changes["status"]
            old_val = status_change.get("old", "Unknown")
            new_val = status_change.get("new", "Unknown")
            embed.add_field(
                name="Status Change",
                value=f"`{old_val}` → `{new_val}`",
                inline=False
            )

        if "phase" in changes and isinstance(changes["phase"], dict):
            phase_change = changes["phase"]
            old_val = str(phase_change.get("old", "Unknown"))[:50]
            new_val = str(phase_change.get("new", "Unknown"))[:50]
            embed.add_field(
                name="Phase Change",
                value=f"`{old_val}` → `{new_val}`",
                inline=False
            )

        if "mission" in changes and isinstance(changes["mission"], dict):
            mission_change = changes["mission"]
            old_val = str(mission_change.get("old", "Unknown"))[:50]
            new_val = str(mission_change.get("new", "Unknown"))[:50]
            embed.add_field(
                name="Mission Change",
                value=f"`{old_val}` → `{new_val}`",
=======
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
                inline=False
            )

        if "completed_tasks" in changes:
<<<<<<< HEAD
            completed_tasks = changes.get("completed_tasks", [])
            if completed_tasks and isinstance(completed_tasks, list):
                tasks_list = "\n".join(
                    [f"✅ {str(task)[:80]}" for task in completed_tasks[:5]])
                if len(completed_tasks) > 5:
                    tasks_list += f"\n... and {len(completed_tasks) - 5} more"
                embed.add_field(
                    name="Tasks Completed",
                    value=tasks_list or "None",
                    inline=False
                )

        if "points_earned" in changes:
            points_change = changes["points_earned"]
            if isinstance(points_change, dict):
                points_val = points_change.get("new", points_change.get("old", 0))
            else:
                points_val = points_change
            try:
                points_int = int(points_val)
                embed.add_field(
                    name="Points Earned",
                    value=f"+{points_int} points",
                    inline=True
                )
            except (ValueError, TypeError):
                pass  # Skip if not a valid number
=======
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

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
