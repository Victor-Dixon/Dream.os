"""
Command Base Classes - Agent Cellphone V2
=========================================

SSOT Domain: discord

Base classes for Discord command implementations.

Features:
- Common command functionality
- Error handling utilities
- Response formatting helpers
- Agent validation methods

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Optional, Dict, Any, List

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

logger = logging.getLogger(__name__)

class BaseDiscordCommand:
    """Base class for Discord commands with common functionality."""

    def __init__(self, bot=None, messaging_controller=None):
        self.bot = bot
        self.messaging_controller = messaging_controller

    async def _safe_send(self, ctx_or_interaction, content: str = None, embed: discord.Embed = None,
                        ephemeral: bool = False) -> bool:
        """Safely send a message with error handling."""
        try:
            if hasattr(ctx_or_interaction, 'response'):  # Interaction
                if ephemeral:
                    await ctx_or_interaction.response.send_message(
                        content=content, embed=embed, ephemeral=True
                    )
                else:
                    await ctx_or_interaction.response.send_message(
                        content=content, embed=embed
                    )
            else:  # Context
                await ctx_or_interaction.send(content=content, embed=embed)
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False

    def _safe_display_name(self, ctx_or_interaction) -> str:
        """Get safe display name from context or interaction."""
        try:
            if hasattr(ctx_or_interaction, 'user'):  # Interaction
                return ctx_or_interaction.user.display_name
            else:  # Context
                return ctx_or_interaction.author.display_name
        except Exception:
            return "Unknown User"

    def _validate_agent_id(self, agent_id: str) -> bool:
        """Validate agent ID format."""
        if not agent_id.startswith("Agent-"):
            return False
        try:
            agent_num = int(agent_id[6:])  # Extract number after "Agent-"
            return 1 <= agent_num <= 8
        except (ValueError, IndexError):
            return False

    def _parse_agent_list(self, agent_input: str) -> List[str]:
        """Parse comma-separated agent list."""
        if agent_input.lower() == "all":
            return [f"Agent-{i}" for i in range(1, 9)]

        raw_list = [aid.strip() for aid in agent_input.split(",") if aid.strip()]
        valid_agents = []

        for agent_id in raw_list:
            if self._validate_agent_id(agent_id):
                valid_agents.append(agent_id)

        return valid_agents

    def _create_error_embed(self, title: str, description: str,
                           color: int = 0xe74c3c) -> discord.Embed:
        """Create a standardized error embed."""
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        return embed

    def _create_success_embed(self, title: str, description: str,
                             color: int = 0x27ae60) -> discord.Embed:
        """Create a standardized success embed."""
        embed = discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        return embed

    def _create_info_embed(self, title: str, description: str = "",
                          color: int = 0x3498db) -> discord.Embed:
        """Create a standardized info embed."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Agent Cellphone V2")
        return embed

class MessagingCommandBase(BaseDiscordCommand):
    """Base class for messaging-related commands."""

    async def _send_agent_message(self, agent_id: str, message: str,
                                 priority: str = "regular") -> Dict[str, Any]:
        """Send message to specific agent."""
        try:
            if not self.messaging_controller:
                return {"success": False, "error": "Messaging controller not available"}

            result = await self.messaging_controller.send_agent_message(
                agent_id=agent_id,
                message=message,
                priority=priority,
                sender="Discord-Bot"
            )

            return {"success": result is not None, "result": result}

        except Exception as e:
            logger.error(f"Failed to send message to {agent_id}: {e}")
            return {"success": False, "error": str(e)}

    async def _broadcast_message(self, message: str, agent_list: List[str] = None,
                                priority: str = "regular") -> Dict[str, Any]:
        """Broadcast message to multiple agents."""
        try:
            if not self.messaging_controller:
                return {"success": False, "error": "Messaging controller not available"}

            if agent_list is None:
                agent_list = [f"Agent-{i}" for i in range(1, 9)]

            results = []
            for agent_id in agent_list:
                result = await self._send_agent_message(agent_id, message, priority)
                results.append({"agent": agent_id, "success": result["success"]})

            success_count = sum(1 for r in results if r["success"])
            return {
                "success": success_count > 0,
                "total": len(results),
                "successful": success_count,
                "results": results
            }

        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
            return {"success": False, "error": str(e)}

class StatusCommandBase(BaseDiscordCommand):
    """Base class for status-related commands."""

    def _get_agent_statuses(self) -> List[Dict[str, Any]]:
        """Get status data for all agents."""
        # This would typically load from agent workspaces
        # For now, return mock data structure
        statuses = []
        for i in range(1, 9):
            statuses.append({
                "agent_id": f"Agent-{i}",
                "name": f"Agent-{i}",
                "status": "ACTIVE_AGENT_MODE",
                "current_mission": f"Mission for Agent-{i}",
                "completed_tasks": i * 2,
                "active_tasks": i,
                "last_updated": "2026-01-07T01:00:00Z"
            })
        return statuses

    def _format_agent_status(self, status: Dict[str, Any]) -> str:
        """Format agent status for display."""
        agent_id = status.get('agent_id', 'Unknown')
        status_val = status.get('status', 'Unknown')
        mission = status.get('mission', 'No mission')
        completed = status.get('completed_tasks', 0)
        active = status.get('active_tasks', 0)

        status_emoji = "🟢" if status_val == "ACTIVE_AGENT_MODE" else "🔴"

        return (
            f"{status_emoji} **{agent_id}**\n"
            f"├─ Status: {status_val}\n"
            f"├─ Mission: {mission}\n"
            f"├─ Tasks: ✅ {completed} | 🔄 {active}\n"
            f"└─ Updated: {status.get('last_updated', 'Unknown')[:19]}"
        )

    def _create_status_embed(self, agent_statuses: List[Dict[str, Any]]) -> discord.Embed:
        """Create status overview embed."""
        embed = self._create_info_embed(
            title="🤖 Swarm Status Overview",
            description=f"Status of {len(agent_statuses)} agents in the swarm"
        )

        active_count = sum(1 for s in agent_statuses if s.get('status') == 'ACTIVE_AGENT_MODE')
        total_tasks = sum(s.get('completed_tasks', 0) for s in agent_statuses)

        embed.add_field(
            name="📊 Summary",
            value=f"**Active Agents:** {active_count}/{len(agent_statuses)}\n**Total Tasks Completed:** {total_tasks}",
            inline=False
        )

        # Add individual agent statuses
        for status in agent_statuses[:6]:  # Show first 6 agents
            embed.add_field(
                name=f"Agent {status['agent_id']}",
                value=self._format_agent_status(status),
                inline=True
            )

        if len(agent_statuses) > 6:
            embed.add_field(
                name="...",
                value=f"And {len(agent_statuses) - 6} more agents",
                inline=False
            )

        return embed