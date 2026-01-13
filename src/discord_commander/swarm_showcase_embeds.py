"""
Swarm Showcase Embeds - Agent Cellphone V2
==========================================

SSOT Domain: discord

Embed creation utilities for swarm showcase displays.

Features:
- Task and directive embeds
- Roadmap visualization embeds
- Agent excellence showcase embeds
- Performance overview embeds

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Dict, List, Any

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, _ = get_mock_discord()
    discord = mock_discord

from .discord_ui_components import EmbedFormatter

logger = logging.getLogger(__name__)

class SwarmShowcaseEmbeds:
    """
    Factory class for creating swarm showcase embeds.
    """

    def __init__(self, data_loader):
        self.data_loader = data_loader

    def create_tasks_embed(self) -> discord.Embed:
        """Create embed for tasks and directives dashboard."""
        task_data = self.data_loader.get_task_data()

        embed = EmbedFormatter.create_base_embed(
            title="🎯 Swarm Tasks & Directives Dashboard",
            description="Current active tasks and mission directives across the swarm",
            color=0x3498db
        )

        # Active tasks
        active_tasks = task_data.get('active', [])
        if active_tasks:
            active_text = "\n".join(f"• {task}" for task in active_tasks[:10])
            if len(active_tasks) > 10:
                active_text += f"\n... and {len(active_tasks) - 10} more"
            embed.add_field(
                name=f"📋 Active Tasks ({task_data['total_active']})",
                value=active_text,
                inline=False
            )
        else:
            embed.add_field(
                name="📋 Active Tasks",
                value="No active tasks at this time",
                inline=False
            )

        # Completed today
        completed = task_data.get('completed_today', [])
        if completed:
            completed_text = "\n".join(f"✅ {task}" for task in completed[:5])
            if len(completed) > 5:
                completed_text += f"\n... and {len(completed) - 5} more"
            embed.add_field(
                name=f"✨ Completed Today ({task_data['total_completed']})",
                value=completed_text,
                inline=False
            )

        # Blocked tasks
        blocked = task_data.get('blocked', [])
        if blocked:
            blocked_text = "\n".join(f"🚫 {task}" for task in blocked[:3])
            embed.add_field(
                name=f"⚠️ Blocked Tasks ({len(blocked)})",
                value=blocked_text,
                inline=False
            )

        embed.set_footer(text="Agent Cellphone V2 - Swarm Coordination System")
        return embed

    def create_roadmap_embed(self) -> discord.Embed:
        """Create embed for integration roadmap visualization."""
        roadmap_data = self.data_loader.get_roadmap_data()

        embed = EmbedFormatter.create_base_embed(
            title="🗺️ Swarm Integration Roadmap",
            description="Multi-phase development and integration progress",
            color=0x9b59b6
        )

        # Current focus
        embed.add_field(
            name="🎯 Current Focus",
            value=roadmap_data.get('current_focus', 'No current focus defined'),
            inline=False
        )

        # Next milestone
        embed.add_field(
            name="🏁 Next Milestone",
            value=roadmap_data.get('next_milestone', 'No milestone defined'),
            inline=False
        )

        # Phases
        phases = roadmap_data.get('phases', [])
        for phase in phases:
            phase_name = phase['name']
            status = phase['status']
            completion = phase['completion']
            description = phase['description']

            # Status emoji
            status_emoji = {
                'completed': '✅',
                'in_progress': '🔄',
                'planned': '⏳'
            }.get(status, '❓')

            progress_bar = self._create_progress_bar(completion)

            embed.add_field(
                name=f"{status_emoji} {phase_name}",
                value=f"{description}\n{progress_bar} {completion}%",
                inline=False
            )

        embed.set_footer(text="Agent Cellphone V2 - Development Roadmap")
        return embed

    def create_excellence_embed(self) -> discord.Embed:
        """Create embed for agent excellence showcase."""
        excellence_data = self.data_loader.get_agent_excellence_data()

        embed = EmbedFormatter.create_base_embed(
            title="🏆 Agent Excellence Showcase",
            description="Celebrating outstanding performance across the swarm",
            color=0xf39c12
        )

        # Top performers
        top_agents = excellence_data[:5]  # Show top 5
        for i, agent in enumerate(top_agents, 1):
            medal = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, '🏅')

            agent_info = (
                f"**Mission:** {agent['current_mission']}\n"
                f"**Completed:** {agent['completed_tasks']} tasks\n"
                f"**Status:** {agent['status']}"
            )

            embed.add_field(
                name=f"{medal} {agent['name']} ({agent['agent_id']})",
                value=agent_info,
                inline=False
            )

        # Overall stats
        total_agents = len(excellence_data)
        active_agents = sum(1 for a in excellence_data if a['status'] == 'ACTIVE_AGENT_MODE')
        total_completed = sum(a['completed_tasks'] for a in excellence_data)

        stats = (
            f"**Total Agents:** {total_agents}\n"
            f"**Active Agents:** {active_agents}\n"
            f"**Tasks Completed Today:** {total_completed}"
        )

        embed.add_field(
            name="📊 Swarm Statistics",
            value=stats,
            inline=False
        )

        embed.set_footer(text="Agent Cellphone V2 - Agent Performance Tracking")
        return embed

    def create_overview_embed(self) -> discord.Embed:
        """Create embed for complete swarm status and missions overview."""
        overview_data = self.data_loader.get_overview_data()
        performance = overview_data.get('performance', {})

        embed = EmbedFormatter.create_base_embed(
            title="🌐 Swarm Status & Missions Overview",
            description="Comprehensive view of swarm operations and progress",
            color=0x2ecc71
        )

        # System health
        embed.add_field(
            name="💚 System Health",
            value=f"**Status:** {overview_data.get('system_health', 'Unknown').title()}",
            inline=True
        )

        # Agent statistics
        embed.add_field(
            name="🤖 Agent Status",
            value=(
                f"**Total:** {performance.get('total_agents', 0)}\n"
                f"**Active:** {performance.get('active_agents', 0)}\n"
                f"**Success Rate:** {performance.get('success_rate', 0):.1f}%"
            ),
            inline=True
        )

        # Task statistics
        tasks = overview_data.get('tasks', {})
        embed.add_field(
            name="📋 Task Status",
            value=(
                f"**Active:** {tasks.get('total_active', 0)}\n"
                f"**Completed Today:** {tasks.get('total_completed', 0)}\n"
                f"**Avg Completion:** {performance.get('average_completion', 0):.1f}"
            ),
            inline=True
        )

        # Current missions
        agent_statuses = overview_data.get('agent_statuses', [])
        active_missions = [s for s in agent_statuses if s.get('current_mission')]

        if active_missions:
            missions_text = ""
            for status in active_missions[:3]:  # Show top 3
                agent_id = status.get('agent_id', 'Unknown')
                mission = status.get('current_mission', 'No mission')
                missions_text += f"**{agent_id}:** {mission[:50]}{'...' if len(mission) > 50 else ''}\n"

            embed.add_field(
                name="🎯 Active Missions",
                value=missions_text.strip(),
                inline=False
            )

        # Roadmap status
        roadmap = overview_data.get('roadmap', {})
        current_phase = None
        for phase in roadmap.get('phases', []):
            if phase.get('status') == 'in_progress':
                current_phase = phase
                break

        if current_phase:
            embed.add_field(
                name="🚀 Current Phase",
                value=(
                    f"**{current_phase['name']}**\n"
                    f"{current_phase['description']}\n"
                    f"Progress: {current_phase.get('completion', 0)}%"
                ),
                inline=False
            )

        embed.set_footer(text=f"Agent Cellphone V2 - Last updated: {overview_data.get('timestamp', 'Unknown')[:19]}")
        return embed

    def create_profile_embed(self, agent_id: str) -> discord.Embed:
        """Create embed for specific agent profile."""
        agent_statuses = self.data_loader.get_all_agent_statuses()
        agent_data = next((s for s in agent_statuses if s.get('agent_id') == agent_id), None)

        if not agent_data:
            embed = EmbedFormatter.create_base_embed(
                title=f"🤖 Agent Profile: {agent_id}",
                description="Agent not found or status unavailable",
                color=0xe74c3c
            )
            return embed

        embed = EmbedFormatter.create_base_embed(
            title=f"🤖 Agent Profile: {agent_data.get('agent_name', agent_id)}",
            description=f"Detailed status and performance for {agent_id}",
            color=0x3498db
        )

        # Basic info
        embed.add_field(
            name="📊 Status",
            value=agent_data.get('status', 'Unknown'),
            inline=True
        )

        embed.add_field(
            name="🎯 Current Mission",
            value=agent_data.get('current_mission', 'No active mission'),
            inline=True
        )

        embed.add_field(
            name="⚡ Priority",
            value=agent_data.get('mission_priority', 'Normal'),
            inline=True
        )

        # Task statistics
        completed_tasks = agent_data.get('completed_tasks', [])
        current_tasks = agent_data.get('current_tasks', [])
        achievements = agent_data.get('achievements', [])

        embed.add_field(
            name="✅ Completed Tasks",
            value=str(len(completed_tasks)),
            inline=True
        )

        embed.add_field(
            name="📋 Active Tasks",
            value=str(len(current_tasks)),
            inline=True
        )

        embed.add_field(
            name="🏆 Achievements",
            value=str(len(achievements)),
            inline=True
        )

        # Recent achievements
        if achievements:
            recent_achievements = achievements[-3:]  # Last 3 achievements
            achievements_text = "\n".join(f"• {achievement}" for achievement in recent_achievements)
            embed.add_field(
                name="🎉 Recent Achievements",
                value=achievements_text,
                inline=False
            )

        # Current tasks
        if current_tasks:
            tasks_text = "\n".join(f"• {task}" for task in current_tasks[:3])
            if len(current_tasks) > 3:
                tasks_text += f"\n... and {len(current_tasks) - 3} more"
            embed.add_field(
                name="🎯 Current Tasks",
                value=tasks_text,
                inline=False
            )

        embed.set_footer(text=f"Agent Cellphone V2 - {agent_id} Profile")
        return embed

    def _create_progress_bar(self, percentage: int, length: int = 10) -> str:
        """Create a visual progress bar."""
        filled = int((percentage / 100) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"