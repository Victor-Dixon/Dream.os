#!/usr/bin/env python3
"""
Event-Driven Commands - Hybrid System Integration
================================================

Discord commands that respond to system events and enable swarm coordination.

<!-- SSOT Domain: discord -->

Features:
- Event-driven command responses
- System status monitoring
- Swarm coordination commands
- Real-time event notifications

Author: Agent-2 (Architecture & Design Specialist)
Date: 2026-01-12
Phase: Phase 6 - Infrastructure Optimization
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unified_discord_bot import UnifiedDiscordBot

import discord
from discord.ext import commands

from .command_base import DiscordCommandMixin, RoleDecorators
from ..discord_event_bridge import get_discord_event_bridge
from ...core.infrastructure.phase2_coordination_events import get_phase2_coordination

logger = logging.getLogger(__name__)


class EventDrivenCommands(commands.Cog, DiscordCommandMixin):
    """Discord commands that integrate with the event-driven system."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize event-driven commands."""
        commands.Cog.__init__(self)
        DiscordCommandMixin.__init__(self)
        self.bot = bot
        self.gui_controller = gui_controller
        self.event_bridge = get_discord_event_bridge(bot)
        self.phase2_coordination = get_phase2_coordination()

    @commands.command(name="event-status", description="Check event system status")
    @RoleDecorators.admin_only()
    async def event_status(self, ctx: commands.Context):
        """Check the current status of the event-driven system."""
        self.log_command_trigger(ctx, "event-status")

        try:
            embed = self.create_base_embed("🔄 Event System Status")

            # Get bridge status
            bridge_status = await self.event_bridge.get_bridge_status()

            embed.add_field(
                name="🔗 Bridge Status",
                value=f"Enabled: {'✅' if bridge_status['enabled'] else '❌'}",
                inline=True
            )

            embed.add_field(
                name="📡 Active Subscriptions",
                value=str(bridge_status['active_subscriptions']),
                inline=True
            )

            embed.add_field(
                name="⚙️ Message Processors",
                value=str(bridge_status['registered_processors']),
                inline=True
            )

            embed.add_field(
                name="🖥️ Event Bus Connected",
                value="✅" if bridge_status['event_bus_connected'] else "❌",
                inline=True
            )

            embed.add_field(
                name="🤖 Discord Bot Connected",
                value="✅" if bridge_status['discord_bot_connected'] else "❌",
                inline=True
            )

            # Get event bus metrics if available
            try:
                event_bus = self.event_bridge.event_bus
                if hasattr(event_bus, 'metrics'):
                    metrics = event_bus.metrics.get_metrics()
                    embed.add_field(
                        name="📊 Events Published",
                        value=str(metrics.get('events_published', 0)),
                        inline=True
                    )
                    embed.add_field(
                        name="📈 Delivery Rate",
                        value=f"{metrics.get('delivery_success_rate', 0):.1%}",
                        inline=True
                    )
                    embed.add_field(
                        name="⚡ Processing Rate",
                        value=f"{metrics.get('processing_success_rate', 0):.1%}",
                        inline=True
                    )
            except Exception as e:
                logger.error(f"Error getting event bus metrics: {e}")

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "event-status")

    @commands.command(name="swarm-status", description="Check swarm coordination status")
    @RoleDecorators.admin_only()
    async def swarm_status(self, ctx: commands.Context):
        """Check the current swarm coordination status."""
        self.log_command_trigger(ctx, "swarm-status")

        try:
            embed = self.create_base_embed("🐝 Swarm Coordination Status")

            # Get system status from event bus
            try:
                status = await self.event_bridge.event_bus.get_queue_status()

                embed.add_field(
                    name="📊 Active Subscriptions",
                    value=str(status.get('active_subscriptions', 0)),
                    inline=True
                )

                embed.add_field(
                    name="🔄 Active Subscribers",
                    value=str(status.get('active_subscribers', 0)),
                    inline=True
                )

                uptime = status.get('uptime_seconds', 0)
                hours = int(uptime // 3600)
                minutes = int((uptime % 3600) // 60)
                embed.add_field(
                    name="⏱️ Uptime",
                    value=f"{hours}h {minutes}m",
                    inline=True
                )

                # Add metrics if available
                if 'metrics' in status:
                    metrics = status['metrics']
                    embed.add_field(
                        name="📈 Publish Rate/sec",
                        value=f"{metrics.get('publish_rate_per_second', 0):.1f}",
                        inline=True
                    )

            except Exception as e:
                logger.error(f"Error getting queue status: {e}")
                embed.add_field(
                    name="❌ Status Error",
                    value="Unable to retrieve swarm status",
                    inline=False
                )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "swarm-status")

    @commands.command(name="trigger-event", description="Manually trigger a system event")
    @RoleDecorators.admin_only()
    async def trigger_event(self, ctx: commands.Context, event_type: str, *, event_data: str = "{}"):
        """Manually trigger a system event for testing."""
        self.log_command_trigger(ctx, "trigger-event")

        try:
            # Parse event data
            try:
                import json
                data = json.loads(event_data)
            except json.JSONDecodeError:
                await ctx.send("❌ Invalid JSON format for event data")
                return

            # Publish system event
            event_id = await self.event_bridge.publish_system_event(
                event_type=event_type,
                event_data=data
            )

            embed = self.create_base_embed("⚡ Event Triggered")
            embed.add_field(
                name="📝 Event Type",
                value=event_type,
                inline=True
            )
            embed.add_field(
                name="🆔 Event ID",
                value=event_id[:8] + "...",
                inline=True
            )
            embed.add_field(
                name="📊 Data",
                value=str(data)[:500] + ("..." if len(str(data)) > 500 else ""),
                inline=False
            )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "trigger-event")

    @commands.command(name="event-history", description="Show recent event history")
    @RoleDecorators.admin_only()
    async def event_history(self, ctx: commands.Context, limit: int = 5):
        """Show recent event history from the system."""
        self.log_command_trigger(ctx, "event-history")

        try:
            embed = self.create_base_embed("📚 Recent Event History")

            # Get recent events from event bus metrics
            try:
                metrics = self.event_bridge.event_bus.metrics.get_metrics()
                recent_events = metrics.get('recent_events', [])

                if recent_events:
                    for i, event in enumerate(recent_events[-limit:]):
                        embed.add_field(
                            name=f"Event {i+1}: {event.get('event_type', 'unknown')}",
                            value=f"• Type: {event.get('event_type', 'unknown')}\n• Timestamp: {event.get('timestamp', 'unknown')[:19]}",
                            inline=False
                        )
                else:
                    embed.add_field(
                        name="📝 No Recent Events",
                        value="No events in recent history",
                        inline=False
                    )

                embed.add_field(
                    name="📊 Summary",
                    value=f"Total Published: {metrics.get('events_published', 0)}\nDelivered: {metrics.get('events_delivered', 0)}\nFailed: {metrics.get('events_failed', 0)}",
                    inline=False
                )

            except Exception as e:
                logger.error(f"Error getting event history: {e}")
                embed.add_field(
                    name="❌ History Error",
                    value="Unable to retrieve event history",
                    inline=False
                )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "event-history")

    @commands.command(name="coordination-ping", description="Send coordination ping to swarm")
    @RoleDecorators.admin_only()
    async def coordination_ping(self, ctx: commands.Context, *, message: str):
        """Send a coordination ping to the swarm via events."""
        self.log_command_trigger(ctx, "coordination-ping")

        try:
            # Create coordination event
            coord_data = {
                'message': message,
                'initiator': ctx.author.display_name,
                'channel': ctx.channel.name,
                'timestamp': discord.utils.utcnow().isoformat(),
                'ping_type': 'coordination'
            }

            # Publish coordination event
            event_id = await self.event_bridge.publish_system_event(
                event_type="swarm:coordination:ping",
                event_data=coord_data
            )

            embed = self.create_base_embed("📡 Coordination Ping Sent")
            embed.add_field(
                name="📝 Message",
                value=message[:500] + ("..." if len(message) > 500 else ""),
                inline=False
            )
            embed.add_field(
                name="🆔 Event ID",
                value=event_id[:8] + "...",
                inline=True
            )
            embed.add_field(
                name="👤 Initiator",
                value=ctx.author.display_name,
                inline=True
            )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "coordination-ping")

    @commands.command(name="system-health", description="Show system health dashboard")
    @RoleDecorators.admin_only()
    async def system_health(self, ctx: commands.Context):
        """Show comprehensive system health dashboard."""
        self.log_command_trigger(ctx, "system-health")

        try:
            embed = self.create_base_embed("🏥 System Health Dashboard")

            # Event system health
            try:
                bridge_status = await self.event_bridge.get_bridge_status()
                event_bus_health = self.event_bridge.event_bus.metrics.get_health_status()

                health_status = "🟢 Healthy"
                if event_bus_health['status'] == 'warning':
                    health_status = "🟡 Warning"
                elif event_bus_health['status'] == 'unhealthy':
                    health_status = "🔴 Unhealthy"

                embed.add_field(
                    name="🔄 Event System",
                    value=health_status,
                    inline=True
                )

                embed.add_field(
                    name="📊 Delivery Success",
                    value=f"{event_bus_health.get('delivery_success_rate', 0):.1%}",
                    inline=True
                )

                embed.add_field(
                    name="⚡ Error Rate",
                    value=f"{event_bus_health.get('error_rate', 0):.1%}",
                    inline=True
                )

            except Exception as e:
                logger.error(f"Error getting system health: {e}")
                embed.add_field(
                    name="❌ Health Check Failed",
                    value="Unable to retrieve system health",
                    inline=False
                )

            # Discord bot health
            embed.add_field(
                name="🤖 Discord Bot",
                value="🟢 Connected" if self.bot.connection_healthy else "🔴 Disconnected",
                inline=True
            )

            embed.add_field(
                name="📡 Latency",
                value=f"{round(self.bot.latency * 1000, 1)}ms" if self.bot.latency else "Unknown",
                inline=True
            )

            embed.add_field(
                name="🖥️ Active Guilds",
                value=str(len(self.bot.guilds)),
                inline=True
            )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "system-health")

    @commands.command(name="phase2-status", description="Check Phase 2 coordination status")
    @RoleDecorators.admin_only()
    async def phase2_status(self, ctx: commands.Context):
        """Check the current Phase 2 coordination status."""
        self.log_command_trigger(ctx, "phase2-status")

        try:
            embed = self.create_base_embed("📊 Phase 2 Coordination Status")

            # Get Phase 2 coordination status
            try:
                phase2_status = await self.phase2_coordination.get_phase2_status()

                embed.add_field(
                    name="📈 Phase 2 Events",
                    value=str(phase2_status.get('phase2_events_total', 0)),
                    inline=True
                )

                embed.add_field(
                    name="🤝 Active Coordinations",
                    value=str(phase2_status.get('active_coordinations', 0)),
                    inline=True
                )

                embed.add_field(
                    name="🔗 Event Bus",
                    value="🟢 Connected" if phase2_status.get('event_bus_healthy') else "🔴 Disconnected",
                    inline=True
                )

                embed.add_field(
                    name="📡 Discord Bridge",
                    value="🟢 Active" if phase2_status.get('discord_bridge_active') else "🔴 Inactive",
                    inline=True
                )

            except Exception as e:
                logger.error(f"Error getting Phase 2 status: {e}")
                embed.add_field(
                    name="❌ Status Error",
                    value="Unable to retrieve Phase 2 coordination status",
                    inline=False
                )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "phase2-status")

    @commands.command(name="phase2-progress", description="Report Phase 2 progress")
    @RoleDecorators.admin_only()
    async def phase2_progress(self, ctx: commands.Context, task: str, progress_percent: float, *, status: str = "in_progress"):
        """Report Phase 2 progress for your assigned tasks."""
        self.log_command_trigger(ctx, "phase2-progress")

        try:
            # Extract agent ID from context (assuming format like "Agent-2")
            agent_id = ctx.author.display_name
            if not agent_id.startswith("Agent-"):
                # Try to get from nickname or fallback
                agent_id = "Agent-Unknown"

            # Validate progress percentage
            if not (0.0 <= progress_percent <= 100.0):
                await ctx.send("❌ Progress must be between 0.0 and 100.0")
                return

            # Convert to decimal
            progress_decimal = progress_percent / 100.0

            # Publish progress event
            event_id = await self.phase2_coordination.publish_phase2_progress(
                agent_id=agent_id,
                task=task,
                progress=progress_decimal,
                status=status
            )

            embed = self.create_base_embed("📊 Phase 2 Progress Reported")
            embed.add_field(
                name="👤 Agent",
                value=agent_id,
                inline=True
            )
            embed.add_field(
                name="📝 Task",
                value=task,
                inline=True
            )
            embed.add_field(
                name="📈 Progress",
                value=f"{progress_percent:.1f}%",
                inline=True
            )
            embed.add_field(
                name="📊 Status",
                value=status,
                inline=True
            )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "phase2-progress")

    @commands.command(name="phase2-coordinate", description="Coordinate Phase 2 action with other agents")
    @RoleDecorators.admin_only()
    async def phase2_coordinate(self, ctx: commands.Context, target_agents: str, *, action: str):
        """Coordinate a Phase 2 action with other agents."""
        self.log_command_trigger(ctx, "phase2-coordinate")

        try:
            # Parse target agents (comma-separated)
            agent_list = [agent.strip() for agent in target_agents.split(',') if agent.strip()]

            if not agent_list:
                await ctx.send("❌ Please specify at least one target agent")
                return

            # Validate agent format
            for agent in agent_list:
                if not agent.startswith("Agent-"):
                    await ctx.send(f"❌ Invalid agent format: {agent}. Use format: Agent-X")
                    return

            # Get coordinating agent
            coordinating_agent = ctx.author.display_name
            if not coordinating_agent.startswith("Agent-"):
                coordinating_agent = "Agent-Unknown"

            # Publish coordination event
            event_id = await self.phase2_coordination.coordinate_agents(
                coordinating_agent=coordinating_agent,
                target_agents=agent_list,
                action=action
            )

            embed = self.create_base_embed("🤝 Phase 2 Coordination Sent")
            embed.add_field(
                name="👤 Coordinator",
                value=coordinating_agent,
                inline=True
            )
            embed.add_field(
                name="🎯 Target Agents",
                value=', '.join(agent_list),
                inline=True
            )
            embed.add_field(
                name="📝 Action",
                value=action,
                inline=False
            )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "phase2-coordinate")

    @commands.command(name="phase2-complete", description="Report Phase 2 task completion")
    @RoleDecorators.admin_only()
    async def phase2_complete(self, ctx: commands.Context, task: str, success: bool = True):
        """Report Phase 2 task completion."""
        self.log_command_trigger(ctx, "phase2-complete")

        try:
            # Get agent ID
            agent_id = ctx.author.display_name
            if not agent_id.startswith("Agent-"):
                agent_id = "Agent-Unknown"

            # Publish completion event
            event_id = await self.phase2_coordination.publish_completion(
                agent_id=agent_id,
                task=task,
                success=success
            )

            embed = self.create_base_embed("✅ Phase 2 Completion Reported")
            embed.add_field(
                name="👤 Agent",
                value=agent_id,
                inline=True
            )
            embed.add_field(
                name="📝 Task",
                value=task,
                inline=True
            )
            embed.add_field(
                name="📊 Result",
                value="Success" if success else "Failed",
                inline=True
            )

            self.add_user_footer(embed, ctx)
            await ctx.send(embed=embed)

        except Exception as e:
            await self.handle_command_error(ctx, e, "phase2-complete")


async def setup(bot):
    """Setup function for Discord cog loading."""
    await bot.add_cog(EventDrivenCommands(bot, bot.gui_controller))