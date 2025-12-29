"""
Agent Management Commands
=========================

Agent management commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Self-healing system commands.

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import asyncio
import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class AgentManagementCommands(commands.Cog):
    """Agent management commands for system health."""

    def __init__(self, bot, gui_controller):
        """Initialize agent management commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="heal", aliases=["self_heal", "healing"], description="Self-healing system commands")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def heal(self, ctx: commands.Context, action: str = "status", agent_id: str = None):
        """
        Self-healing system commands.

        Usage:
        !heal status - Show healing statistics
        !heal check - Immediately check and heal all stalled agents
        !heal stats [Agent-X] - Show detailed stats for agent (or all agents)
        !heal cancel_count [Agent-X] - Show terminal cancellation count today
        """
        self.logger.info(f"Command 'heal' triggered by {ctx.author} with args: action={action}, agent_id={agent_id}")
        try:
            from src.core.agent_self_healing_system import (
                get_self_healing_system,
                heal_stalled_agents_now
            )

            system = get_self_healing_system()

            if action.lower() == "status" or action.lower() == "stats":
                # Show healing statistics
                stats = system.get_healing_stats()

                embed = discord.Embed(
                    title="🏥 Self-Healing System Status",
                    description="Agent stall detection and recovery statistics",
                    color=discord.Color.blue(),
                )

                # Overall stats
                embed.add_field(
                    name="📊 Overall Statistics",
                    value=(
                        f"**Total Actions:** {stats['total_actions']}\n"
                        f"**Success Rate:** {stats['success_rate']:.1f}%\n"
                        f"**Successful:** {stats['successful']}\n"
                        f"**Failed:** {stats['failed']}"
                    ),
                    inline=False
                )

                # Terminal cancellation counts
                cancel_counts = stats.get('terminal_cancellations_today', {})
                cancel_summary = "\n".join([
                    f"{agent}: {count}" for agent, count in cancel_counts.items() if count > 0
                ]) or "None today"

                embed.add_field(
                    name="🛑 Terminal Cancellations (Today)",
                    value=cancel_summary,
                    inline=False
                )

                # Recent actions
                if stats.get('recent_actions'):
                    recent = stats['recent_actions'][-5:]  # Last 5
                    recent_text = "\n".join([
                        f"{'✅' if a['success'] else '❌'} **{a['agent_id']}**: {a['action']}"
                        for a in recent
                    ])
                    embed.add_field(
                        name="🔄 Recent Actions",
                        value=recent_text[:1024],  # Discord limit
                        inline=False
                    )

                await ctx.send(embed=embed)

            elif action.lower() == "check" or action.lower() == "heal":
                # Immediately check and heal stalled agents
                await ctx.send("🔍 Checking for stalled agents and healing...")

                results = await heal_stalled_agents_now()

                embed = discord.Embed(
                    title="🏥 Healing Check Results",
                    description=f"Checked at {results['timestamp']}",
                    color=discord.Color.green(
                    ) if results['stalled_agents_found'] == 0 else discord.Color.orange(),
                )

                embed.add_field(
                    name="📊 Results",
                    value=(
                        f"**Stalled Agents Found:** {results['stalled_agents_found']}\n"
                        f"**Agents Healed:** {len(results['agents_healed'])}\n"
                        f"**Agents Failed:** {len(results['agents_failed'])}"
                    ),
                    inline=False
                )

                if results['agents_healed']:
                    embed.add_field(
                        name="✅ Successfully Healed",
                        value=", ".join(results['agents_healed']),
                        inline=False
                    )

                if results['agents_failed']:
                    embed.add_field(
                        name="❌ Failed to Heal",
                        value=", ".join(results['agents_failed']),
                        inline=False
                    )

                await ctx.send(embed=embed)

            elif action.lower() == "cancel_count" or action.lower() == "cancellations":
                # Show terminal cancellation count
                if agent_id:
                    count = system.get_cancellation_count_today(agent_id)
                    embed = discord.Embed(
                        title=f"🛑 Terminal Cancellations - {agent_id}",
                        description=f"**Today:** {count} cancellation(s)",
                        color=discord.Color.orange() if count > 0 else discord.Color.green(),
                    )
                else:
                    cancel_counts = system.get_healing_stats().get(
                        'terminal_cancellations_today', {})
                    total = sum(cancel_counts.values())
                    embed = discord.Embed(
                        title="🛑 Terminal Cancellations (Today)",
                        description=f"**Total:** {total} cancellation(s) across all agents",
                        color=discord.Color.orange() if total > 0 else discord.Color.green(),
                    )
                    for agent, count in cancel_counts.items():
                        if count > 0:
                            embed.add_field(
                                name=agent, value=str(count), inline=True)

                await ctx.send(embed=embed)

            elif action.lower() == "agent" and agent_id:
                # Show detailed stats for specific agent
                stats = system.get_healing_stats()
                agent_stats = stats['by_agent'].get(agent_id, {})
                cancel_count = system.get_cancellation_count_today(agent_id)

                embed = discord.Embed(
                    title=f"🏥 Agent Healing Stats - {agent_id}",
                    color=discord.Color.blue(),
                )

                embed.add_field(
                    name="📊 Healing Actions",
                    value=(
                        f"**Total:** {agent_stats.get('total', 0)}\n"
                        f"**Successful:** {agent_stats.get('successful', 0)}\n"
                        f"**Failed:** {agent_stats.get('failed', 0)}"
                    ),
                    inline=False
                )

                embed.add_field(
                    name="🛑 Terminal Cancellations",
                    value=f"**Today:** {cancel_count}",
                    inline=False
                )

                await ctx.send(embed=embed)

            else:
                await ctx.send(
                    f"❌ Unknown action: `{action}`\n"
                    f"**Usage:** `!heal [status|check|cancel_count|agent] [Agent-X]`\n"
                    f"**Examples:**\n"
                    f"- `!heal status` - Show overall stats\n"
                    f"- `!heal check` - Immediately heal stalled agents\n"
                    f"- `!heal cancel_count Agent-3` - Show cancellation count\n"
                    f"- `!heal agent Agent-3` - Show agent-specific stats"
                )

        except ImportError as e:
            await ctx.send(f"❌ Self-healing system not available: {e}")
        except Exception as e:
            self.logger.error(f"Error in heal command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")


