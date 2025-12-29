<!-- SSOT Domain: core -->
"""
Core Messaging Commands
=======================

Core messaging commands extracted from unified_discord_bot.py for V2 compliance.
Handles: GUI, message sending, broadcast, status, and monitor commands.

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class CoreMessagingCommands(commands.Cog):
    """Core messaging commands for agent communication."""

    def __init__(self, bot, gui_controller):
        """Initialize core messaging commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="gui", description="Open messaging GUI")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def gui(self, ctx: commands.Context):
        """Open interactive messaging GUI."""
        self.logger.info(f"Command 'gui' triggered by {ctx.author}")
        try:
            embed = discord.Embed(
                title="🤖 Agent Messaging Control Panel",
                description="Use the controls below to interact with the swarm",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="📋 Instructions",
                value=(
                    "1. Select an agent from dropdown to send message\n"
                    "2. Click 'Broadcast' to message all agents\n"
                    "3. Click 'Status' to view swarm status\n"
                    "4. Click 'Refresh' to reload agent list"
                ),
                inline=False,
            )

            view = self.gui_controller.create_main_gui()
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error opening GUI: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="status", description="View swarm status. Use '!status refresh' to force update.")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def status(self, ctx: commands.Context, *, args: str = ""):
        """View swarm status. Use '!status refresh' to force immediate update."""
        self.logger.info(f"Command 'status' triggered by {ctx.author} with args={args}")
        try:
            # Force refresh if requested
            if args.lower() == "refresh":
                from ..status_reader import StatusReader
                status_reader = StatusReader()
                status_reader.clear_cache()
                await ctx.send("🔄 Status cache cleared - refreshing...", delete_after=3)

            view = self.gui_controller.create_status_gui()

            # Import status reader to create embed
            from src.discord_commander.status_reader import StatusReader

            status_reader = StatusReader()

            # Create status embed
            main_view = self.gui_controller.create_main_gui()
            embed = await main_view._create_status_embed(status_reader)

            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error showing status: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="monitor", description="Control status change monitor. Usage: !monitor [start|stop|status] (manual start via control panel)")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def monitor(self, ctx: commands.Context, action: str = "status"):
        """Control status change monitor."""
        self.logger.info(f"Command 'monitor' triggered by {ctx.author} with action={action}")
        try:
            action = action.lower()

            if not hasattr(self, 'status_monitor'):
                await ctx.send("❌ Status monitor not initialized. Bot may not be fully ready.")
                return

            if action == "start":
                if hasattr(self.status_monitor, 'monitor_status_changes'):
                    if self.status_monitor.monitor_status_changes.is_running():
                        await ctx.send("✅ Status monitor is already running!")
                    else:
                        self.status_monitor.start_monitoring()
                        await ctx.send("✅ Status monitor started! Checking every 15 seconds.")
                else:
                    self.status_monitor.start_monitoring()
                    await ctx.send("✅ Status monitor started! Checking every 15 seconds.")

            elif action == "stop":
                if hasattr(self.status_monitor, 'monitor_status_changes'):
                    if self.status_monitor.monitor_status_changes.is_running():
                        self.status_monitor.stop_monitoring()
                        await ctx.send("🛑 Status monitor stopped.")
                    else:
                        await ctx.send("⚠️ Status monitor is not running.")
                else:
                    await ctx.send("⚠️ Status monitor is not running.")

            elif action == "status":
                if hasattr(self.status_monitor, 'monitor_status_changes'):
                    is_running = self.status_monitor.monitor_status_changes.is_running()
                    status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
                    interval = self.status_monitor.check_interval

                    # Add manual-start note to description
                    description = f"**Status:** {status_text}"
                    description += "\n**Start/stop via Control Panel button or !monitor start/stop**"
                    description += f"\n**Check Interval:** {interval} seconds"

                    embed = discord.Embed(
                        title="📊 Status Change Monitor",
                        description=description,
                        color=0x27AE60 if is_running else 0xE74C3C,
                        timestamp=discord.utils.utcnow()
                    )

                    # Show tracking info
                    if hasattr(self.status_monitor, 'last_modified'):
                        tracked_agents = len(self.status_monitor.last_modified)
                        embed.add_field(
                            name="Tracked Agents",
                            value=f"{tracked_agents}/8 agents",
                            inline=True
                        )

                    embed.set_footer(
                        text="Use Control Panel button or !monitor stop/start to control the monitor")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("⚠️ Status monitor not initialized.")

            else:
                await ctx.send("❌ Invalid action. Use: `!monitor [stop|status]` (monitor auto-starts with bot)")

        except Exception as e:
            self.logger.error(f"Error in monitor command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="message", description="Send message to agent")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):
        """Send direct message to agent."""
        self.logger.info(f"Command 'message' triggered by {ctx.author} to {agent_id}")
        try:
            success = await self.gui_controller.send_message(
                agent_id=agent_id,
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                # Use chunking utility to avoid truncation
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(
                    name="Message", value=message_chunks[0], inline=False)
                # If message was chunked, send additional parts
                if len(message_chunks) > 1:
                    for i, chunk in enumerate(message_chunks[1:], 2):
                        embed.add_field(
                            name=f"Message (continued {i}/{len(message_chunks)})",
                            value=chunk,
                            inline=False
                        )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Failed to send message to {agent_id}")

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="broadcast", description="Broadcast to all agents")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def broadcast(self, ctx: commands.Context, *, message: str):
        """Broadcast message to all agents."""
        self.logger.info(f"Command 'broadcast' triggered by {ctx.author}")
        try:
            success = await self.gui_controller.broadcast_message(
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Delivered to all agents",
                    color=discord.Color.green(),
                )
                # Use chunking utility to avoid truncation
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(
                    name="Message", value=message_chunks[0], inline=False)
                # If message was chunked, send additional parts
                if len(message_chunks) > 1:
                    for i, chunk in enumerate(message_chunks[1:], 2):
                        embed.add_field(
                            name=f"Message (continued {i}/{len(message_chunks)})",
                            value=chunk,
                            inline=False
                        )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Failed to broadcast message")

        except Exception as e:
            self.logger.error(f"Error broadcasting: {e}")
            await ctx.send(f"❌ Error: {e}")


