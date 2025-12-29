#!/usr/bin/env python3
"""
Bot Messaging Commands
======================

Discord commands for agent messaging (extracted from unified_discord_bot.py).

This module contains the MessagingCommands Cog that was previously embedded
in unified_discord_bot.py. Extracted for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

from src.core.config.timeout_constants import TimeoutConstants
from src.discord_commander.discord_gui_controller import DiscordGUIController
from src.discord_commander.views import ConfirmShutdownView, ConfirmRestartView

logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):
    """Commands for agent messaging."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: DiscordGUIController):
        """Initialize messaging commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="thea", aliases=["thea-refresh"], description="Ensure Thea session")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def thea(self, ctx: commands.Context, force: str = ""):
        """Ensure Thea session with self-throttling keepalive."""
        self.logger.info(f"Command 'thea' triggered by {ctx.author}")
        allow_interactive = True
        min_interval = 0 if force else self.bot.thea_min_interval_minutes
        await ctx.send("🔄 Ensuring Thea session (headless)...")
        success = await self.bot.ensure_thea_session(
            allow_interactive=allow_interactive, min_interval_minutes=min_interval)
        if success:
            await ctx.send("✅ Thea session is healthy (cookies saved).")
        else:
            await ctx.send("❌ Thea session failed. Try again to trigger interactive login.")

    @commands.command(name="control", aliases=["panel", "menu"], description="Open main control panel")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def control_panel(self, ctx: commands.Context):
        """Open main interactive control panel."""
        self.logger.info(f"Command 'control_panel' triggered by {ctx.author}")
        try:
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="🎛️ SWARM CONTROL PANEL",
                description="**Complete Interactive Control Interface**\n\nUse buttons below to access all features:",
                color=discord.Color.blue(),
            )
            embed.add_field(name="📨 Messaging", value="Message individual agents or broadcast to all", inline=True)
            embed.add_field(name="📊 Monitoring", value="View swarm status and task dashboards", inline=True)
            embed.add_field(name="📚 Content", value="Access GitHub book and documentation", inline=True)
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Interactive GUI-Driven Control")
            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error opening control panel: {e}")
            await ctx.send(f"❌ Error: {e}")

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

    @commands.command(name="status", description="View swarm status")
    async def status(self, ctx: commands.Context, *, args: str = ""):
        """View swarm status. Use '!status refresh' to force update."""
        try:
            if args.lower() == "refresh":
                from src.discord_commander.status_reader import StatusReader
                status_reader = StatusReader()
                status_reader.clear_cache()
                await ctx.send("🔄 Status cache cleared - refreshing...", delete_after=3)

            view = self.gui_controller.create_status_gui()
            from src.discord_commander.status_reader import StatusReader
            status_reader = StatusReader()
            main_view = self.gui_controller.create_main_gui()
            embed = await main_view._create_status_embed(status_reader)
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing status: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="monitor", description="Control status change monitor")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def monitor(self, ctx: commands.Context, action: str = "status"):
        """Control status change monitor."""
        self.logger.info(f"Command 'monitor' triggered by {ctx.author} with action={action}")
        try:
            action = action.lower()
            if not hasattr(self.bot, 'status_monitor'):
                await ctx.send("❌ Status monitor not initialized. Bot may not be fully ready.")
                return

            if action == "start":
                await self._handle_monitor_start(ctx)
            elif action == "stop":
                await self._handle_monitor_stop(ctx)
            elif action == "status":
                await self._handle_monitor_status(ctx)
            else:
                await ctx.send("❌ Invalid action. Use: `!monitor [stop|status]`")
        except Exception as e:
            self.logger.error(f"Error in monitor command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    async def _handle_monitor_start(self, ctx: commands.Context) -> None:
        """Handle monitor start action."""
        if hasattr(self.bot.status_monitor, 'monitor_status_changes'):
            if self.bot.status_monitor.monitor_status_changes.is_running():
                await ctx.send("✅ Status monitor is already running!")
            else:
                self.bot.status_monitor.start_monitoring()
                await ctx.send("✅ Status monitor started! Checking every 15 seconds.")
        else:
            self.bot.status_monitor.start_monitoring()
            await ctx.send("✅ Status monitor started! Checking every 15 seconds.")

    async def _handle_monitor_stop(self, ctx: commands.Context) -> None:
        """Handle monitor stop action."""
        if hasattr(self.bot.status_monitor, 'monitor_status_changes'):
            if self.bot.status_monitor.monitor_status_changes.is_running():
                self.bot.status_monitor.stop_monitoring()
                await ctx.send("🛑 Status monitor stopped.")
            else:
                await ctx.send("⚠️ Status monitor is not running.")
        else:
            await ctx.send("⚠️ Status monitor is not running.")

    async def _handle_monitor_status(self, ctx: commands.Context) -> None:
        """Handle monitor status action."""
        if hasattr(self.bot.status_monitor, 'monitor_status_changes'):
            is_running = self.bot.status_monitor.monitor_status_changes.is_running()
            status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
            interval = self.bot.status_monitor.check_interval

            description = f"**Status:** {status_text}"
            description += "\n**Start/stop via Control Panel button or !monitor start/stop**"
            description += f"\n**Check Interval:** {interval} seconds"

            embed = discord.Embed(
                title="📊 Status Change Monitor",
                description=description,
                color=0x27AE60 if is_running else 0xE74C3C,
                timestamp=discord.utils.utcnow()
            )

            if hasattr(self.bot.status_monitor, 'last_modified'):
                tracked_agents = len(self.bot.status_monitor.last_modified)
                embed.add_field(name="Tracked Agents", value=f"{tracked_agents}/8 agents", inline=True)

            embed.set_footer(text="Use Control Panel button or !monitor stop/start to control the monitor")
            await ctx.send(embed=embed)
        else:
            await ctx.send("⚠️ Status monitor not initialized.")

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
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(name="Message", value=message_chunks[0], inline=False)
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

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Render Mermaid diagram code."""
        try:
            diagram_code = self._clean_mermaid_code(diagram_code)
            embed = discord.Embed(
                title="📊 Mermaid Diagram",
                description="Mermaid diagram code:",
                color=discord.Color.blue(),
            )
            mermaid_block = f"```mermaid\n{diagram_code}\n```"

            if len(mermaid_block) > 1900:
                await ctx.send("❌ Mermaid diagram too long. Please shorten it.")
                return

            embed.add_field(name="Diagram Code", value=mermaid_block, inline=False)
            embed.set_footer(text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering")
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error rendering mermaid: {e}")
            await ctx.send(f"❌ Error rendering mermaid diagram: {e}")

    def _clean_mermaid_code(self, diagram_code: str) -> str:
        """Clean mermaid code block markers."""
        diagram_code = diagram_code.strip()
        if diagram_code.startswith("```mermaid"):
            diagram_code = diagram_code[10:]
        elif diagram_code.startswith("```"):
            diagram_code = diagram_code[3:]
        if diagram_code.endswith("```"):
            diagram_code = diagram_code[:-3]
        return diagram_code.strip()

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
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(name="Message", value=message_chunks[0], inline=False)
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

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Show interactive help menu with navigation buttons."""
        try:
            from src.discord_commander.views import HelpGUIView
            view = HelpGUIView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView
            view = AriaProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !aria command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.carmyn_profile_view import CarmynProfileView
            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="commands", description="List all registered commands")
    async def list_commands(self, ctx: commands.Context):
        """List all registered bot commands - redirects to Control Panel button view."""
        try:
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="📋 All Commands - Use Control Panel Buttons!",
                description=(
                    "**🎯 All commands are accessible via buttons in the Control Panel!**\n\n"
                    "**Click the buttons below to access all features:**\n"
                    "• **Tasks** button = `!swarm_tasks`\n"
                    "• **Swarm Status** button = `!status`\n"
                    "• **GitHub Book** button = `!github_book`\n"
                    "• **Roadmap** button = `!swarm_roadmap`\n"
                    "• **Excellence** button = `!swarm_excellence`\n"
                    "• **Overview** button = `!swarm_overview`\n"
                    "• **Goldmines** button = `!goldmines`\n"
                    "• **Templates** button = `!templates`\n"
                    "• **Mermaid** button = `!mermaid`\n"
                    "• **Monitor** button = `!monitor`\n"
                    "• **Help** button = `!help`\n"
                    "• **All Commands** button = This view\n\n"
                    "**No need to type commands - just click buttons!**"
                ),
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="💡 Quick Access",
                value="Type `!control` (or `!panel`, `!menu`) to open Control Panel anytime!",
                inline=False,
            )
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!")
            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def shutdown_cmd(self, ctx: commands.Context):
        """Gracefully shutdown the Discord bot."""
        self.logger.info(f"Command 'shutdown' triggered by {ctx.author}")
        try:
            embed = discord.Embed(
                title="🛑 Shutdown Requested",
                description="Are you sure you want to shutdown the bot?",
                color=discord.Color.red(),
            )
            view = ConfirmShutdownView()
            message = await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.confirmed:
                shutdown_embed = discord.Embed(
                    title="👋 Bot Shutting Down",
                    description="Gracefully closing connections...",
                    color=discord.Color.orange(),
                )
                await ctx.send(embed=shutdown_embed)
                self.logger.info("🛑 Shutdown command received - closing bot")
                await self.bot.close()
            else:
                await message.edit(content="❌ Shutdown cancelled", embed=None, view=None)
        except Exception as e:
            self.logger.error(f"Error in shutdown command: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="restart", description="Restart the Discord bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def restart_cmd(self, ctx: commands.Context):
        """Restart the Discord bot with a true process restart."""
        self.logger.info(f"Command 'restart' triggered by {ctx.author}")
        try:
            embed = discord.Embed(
                title="🔄 True Restart Requested",
                description=(
                    "Bot will perform a TRUE restart:\n"
                    "• Current process will be terminated\n"
                    "• Fresh bot + queue processor will start\n"
                    "• All modules reloaded from disk\n"
                    "• Message delivery enabled (queue processor)\n\n"
                    "Continue?"
                ),
                color=discord.Color.blue(),
            )
            view = ConfirmRestartView()
            message = await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.confirmed:
                restart_embed = discord.Embed(
                    title="🔄 Bot Restarting (True Restart)",
                    description=(
                        "Performing true restart...\n"
                        "• Terminating current process\n"
                        "• Starting fresh bot + queue processor\n"
                        "• All modules reloaded from disk\n"
                        "• Will be back in 5-10 seconds!"
                    ),
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=restart_embed)
                self.logger.info("🔄 True restart command received - killing process and starting fresh")
                self._perform_true_restart()
                await self.bot.close()
            else:
                await message.edit(content="❌ Restart cancelled", embed=None, view=None)
        except Exception as e:
            self.logger.error(f"Error in restart command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    def _perform_true_restart(self) -> bool:
        """Perform true restart: spawn fresh process for bot + queue processor."""
        try:
            project_root = Path(__file__).parent.parent.parent.parent
            start_script = project_root / "tools" / "start_discord_system.py"

            if not start_script.exists():
                self.logger.error(f"Start script not found: {start_script}")
                return False

            if sys.platform == 'win32':
                subprocess.Popen(
                    [sys.executable, str(start_script)],
                    cwd=str(project_root),
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                subprocess.Popen(
                    [sys.executable, str(start_script)],
                    cwd=str(project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )

            import time
            time.sleep(2)
            self.logger.info("✅ New bot + queue processor processes spawned - current process will exit")
            return True
        except Exception as e:
            self.logger.error(f"Error performing true restart: {e}", exc_info=True)
            return False

