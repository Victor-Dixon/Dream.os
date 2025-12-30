#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Startup Helpers
===============

Helper functions for bot startup operations.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import discord

logger = logging.getLogger(__name__)


def get_priority_emoji(priority: str) -> str:
    """Get emoji for priority level."""
    if priority == "HIGH":
        return "🔴"
    elif priority == "MEDIUM":
        return "🟡"
    else:
        return "🟢"


def add_snapshot_fields(embed: "discord.Embed", snapshot: dict, logger: logging.Logger) -> None:
    """Add snapshot fields to embed."""
    if snapshot["active_agents"]:
        _add_active_agents_field(embed, snapshot)

    if snapshot["recent_activity"]:
        _add_recent_activity_field(embed, snapshot)

    if snapshot["current_focus"]:
        _add_current_focus_field(embed, snapshot)


def _add_active_agents_field(embed: "discord.Embed", snapshot: dict) -> None:
    """Add active agents field to embed."""
    active_list = []
    for agent in snapshot["active_agents"][:5]:
        priority_emoji = get_priority_emoji(agent["priority"])
        active_list.append(
            f"{priority_emoji} **{agent['id']}** ({agent['phase']}): {agent['mission']}"
        )
    if len(snapshot["active_agents"]) > 5:
        active_list.append(f"... and {len(snapshot['active_agents']) - 5} more")
    embed.add_field(
        name=f"📊 Current Work Snapshot ({snapshot['engagement_rate']:.0f}% Engagement)",
        value="\n".join(active_list) if active_list else "No active agents",
        inline=False,
    )


def _add_recent_activity_field(embed: "discord.Embed", snapshot: dict) -> None:
    """Add recent activity field to embed."""
    activity_text = "\n".join(snapshot["recent_activity"][:3])
    if len(snapshot["recent_activity"]) > 3:
        activity_text += f"\n... and {len(snapshot['recent_activity']) - 3} more"
    embed.add_field(
        name="✅ Recent Activity",
        value=activity_text[:1024],
        inline=False,
    )


def _add_current_focus_field(embed: "discord.Embed", snapshot: dict) -> None:
    """Add current focus field to embed."""
    focus_text = "\n".join(snapshot["current_focus"][:3])
    if len(snapshot["current_focus"]) > 3:
        focus_text += f"\n... and {len(snapshot['current_focus']) - 3} more"
    embed.add_field(
        name="🎯 Current Focus",
        value=focus_text[:1024],
        inline=False,
    )


def add_system_info_fields(embed: "discord.Embed", bot) -> None:
    """Add system info fields to embed."""
    _add_system_status_field(embed)
    _add_control_panel_field(embed)
    _add_messaging_fields(embed)
    _add_swarm_showcase_field(embed)
    _add_github_book_field(embed)
    _add_diagram_commands_field(embed)
    _add_git_commands_field(embed)
    _add_system_info_field(embed, bot)


def _add_system_status_field(embed: "discord.Embed") -> None:
    """Add system status field."""
    embed.add_field(
        name="✅ System Status",
        value="All systems operational • 3 command modules loaded • Enhanced activity monitoring active!",
        inline=False,
    )


def _add_control_panel_field(embed: "discord.Embed") -> None:
    """Add control panel field."""
    embed.add_field(
        name="🎛️ Interactive Control Panel (PREFERRED - NO COMMANDS NEEDED!)",
        value=(
            "• `!control` (or `!panel`, `!menu`) - Open main control panel\n"
            "• **ALL features accessible via buttons**\n"
            "• **No commands needed - just click buttons!**\n"
            "• Tasks, Status, GitHub Book, Roadmap, Excellence, Overview, Goldmines, Templates, Mermaid, Monitor, Help - ALL via buttons!"
        ),
        inline=False,
    )


def _add_messaging_fields(embed: "discord.Embed") -> None:
    """Add messaging fields."""
    embed.add_field(
        name="📨 Messaging (GUI-Driven)",
        value=(
            "• `!gui` - Open messaging interface\n"
            "• Or use **Message Agent** button in control panel\n"
            "• Entry fields for custom messages"
        ),
        inline=False,
    )

    embed.add_field(
        name="📨 Text Commands (Legacy)",
        value=(
            "• `!message <agent> <msg>` - Direct agent message\n"
            "• `!broadcast <msg>` - Broadcast to all agents\n"
            "• `!bump <1-8> [1-8]...` - Bump agents (click + shift+backspace)\n"
            "• `!agents` - List all agents"
        ),
        inline=False,
    )


def _add_swarm_showcase_field(embed: "discord.Embed") -> None:
    """Add swarm showcase field."""
    embed.add_field(
        name="🐝 Swarm Showcase (ALL ACCESSIBLE VIA BUTTONS!)",
        value=(
            "• **Tasks** button = `!swarm_tasks` - Live task dashboard\n"
            "• **Roadmap** button = `!swarm_roadmap` - Strategic roadmap\n"
            "• **Excellence** button = `!swarm_excellence` - Lean Excellence campaign\n"
            "• **Overview** button = `!swarm_overview` - Complete swarm status\n"
            "• `!swarm_profile` - Swarm collective profile (identity, stats, achievements)"
        ),
        inline=False,
    )


def _add_github_book_field(embed: "discord.Embed") -> None:
    """Add GitHub book field."""
    embed.add_field(
        name="📚 GitHub Book Viewer (ACCESSIBLE VIA BUTTONS!)",
        value=(
            "• **GitHub Book** button = `!github_book [chapter]` - Interactive book navigation\n"
            "• **Goldmines** button = `!goldmines` - High-value pattern showcase\n"
            "• `!book_stats` - Comprehensive statistics"
        ),
        inline=False,
    )


def _add_diagram_commands_field(embed: "discord.Embed") -> None:
    """Add diagram commands field."""
    embed.add_field(
        name="📊 Diagram Commands",
        value=(
            "• `!mermaid <diagram_code>` - Render Mermaid diagram\n"
            "• Example: `!mermaid graph TD; A-->B; B-->C;`"
        ),
        inline=False,
    )


def _add_git_commands_field(embed: "discord.Embed") -> None:
    """Add git commands field."""
    embed.add_field(
        name="🔧 Git Commands",
        value=(
            "• `!git_push \"message\"` - Push project to GitHub\n"
            "• `!push \"Your commit message\"` - Alias for git_push"
        ),
        inline=False,
    )


def _add_system_info_field(embed: "discord.Embed", bot) -> None:
    """Add system info field."""
    embed.add_field(
        name="🤖 System Info",
        value=(
            f"**Guilds:** {len(bot.guilds)} | **Latency:** {round(bot.latency * 1000, 2)}ms\n"
            f"**Modules:** Messaging, Swarm Showcase, GitHub Book\n"
            f"**Status:** 🟢 All systems operational"
        ),
        inline=False,
    )

