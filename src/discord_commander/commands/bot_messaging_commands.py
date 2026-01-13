#!/usr/bin/env python3
"""
<!-- SSOT Domain: messaging -->

<<<<<<< HEAD
<<<<<<< HEAD
Bot Messaging Commands - Main Delegate (Modular V2 Compliance)
============================================================

Main entry point for bot messaging commands.
Uses modular command handlers for maintainability and V2 compliance.

V2 Compliant: <100 lines, modular architecture
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
=======
Bot Messaging Commands
======================
=======
Bot Messaging Commands - Main Delegate (Modular V2 Compliance)
============================================================
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

Main entry point for bot messaging commands.
Uses modular command handlers for maintainability and V2 compliance.

V2 Compliant: <100 lines, modular architecture
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
<<<<<<< HEAD
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

<<<<<<< HEAD
import discord
from discord.ext import commands

# Import modular command handlers
from .messaging_monitor_commands import MessagingMonitorCommands
from .messaging_core_commands import MessagingCoreCommands
from .profile_commands import ProfileCommands
from .utility_commands import UtilityCommands
from .system_control_commands import SystemControlCommands
=======
try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

<<<<<<< HEAD
from src.core.config.timeout_constants import TimeoutConstants
from src.discord_commander.discord_gui_controller import DiscordGUIController
from src.discord_commander.views import ConfirmShutdownView, ConfirmRestartView
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
# Import modular command handlers
from .messaging_monitor_commands import MessagingMonitorCommands
from .messaging_core_commands import MessagingCoreCommands
from .profile_commands import ProfileCommands
from .utility_commands import UtilityCommands
from .system_control_commands import SystemControlCommands
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):
<<<<<<< HEAD
<<<<<<< HEAD
    """Main messaging commands cog that includes all modular handlers."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize messaging commands with modular handlers."""
        super().__init__()
=======
    """Commands for agent messaging."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: DiscordGUIController):
        """Initialize messaging commands."""
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    """Main messaging commands cog that includes all modular handlers."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize messaging commands with modular handlers."""
        commands.Cog.__init__(self)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        # Initialize modular command handlers
        self.monitor_commands = MessagingMonitorCommands(bot)
        self.core_commands = MessagingCoreCommands(bot, gui_controller)
        self.profile_commands = ProfileCommands(bot)
        self.utility_commands = UtilityCommands(bot, gui_controller)
        self.system_commands = SystemControlCommands(bot)
<<<<<<< HEAD

        self.logger.info("✅ Messaging Commands initialized with modular architecture")

    # Delegate commands to modular handlers
    @commands.command(name="monitor", description="Control status change monitor")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def monitor(self, ctx: commands.Context, action: str = "status"):
        """Delegate to monitor commands."""
        await self.monitor_commands.monitor(ctx, action)
=======
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
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        self.logger.info("✅ Messaging Commands initialized with modular architecture")

    # Delegate commands to modular handlers
    @commands.command(name="monitor", description="Control status change monitor")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def monitor(self, ctx: commands.Context, action: str = "status"):
<<<<<<< HEAD
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        """Delegate to monitor commands."""
        await self.monitor_commands.monitor(ctx, action)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    @commands.command(name="message", description="Send message to agent")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delegate to core commands."""
        await self.core_commands.message(ctx, agent_id, message)
=======
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        """Delegate to core commands."""
        await self.core_commands.message(ctx, agent_id, message)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    @commands.command(name="broadcast", description="Broadcast to all agents")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def broadcast(self, ctx: commands.Context, *, message: str):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delegate to core commands."""
        await self.core_commands.broadcast(ctx, message)

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Delegate to utility commands."""
        await self.utility_commands.mermaid(ctx, diagram_code)

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Delegate to utility commands."""
        await self.utility_commands.help_cmd(ctx)

    @commands.command(name="commands", description="List all registered commands")
    async def list_commands(self, ctx: commands.Context):
        """Delegate to utility commands."""
        await self.utility_commands.list_commands(ctx)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.aria_profile(ctx)

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.carmyn_profile(ctx)
=======
        """Broadcast message to all agents."""
        self.logger.info(f"Command 'broadcast' triggered by {ctx.author}")
        try:
            success = await self.gui_controller.broadcast_message(
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )
=======
        """Delegate to core commands."""
        await self.core_commands.broadcast(ctx, message)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Delegate to utility commands."""
        await self.utility_commands.mermaid(ctx, diagram_code)

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Delegate to utility commands."""
        await self.utility_commands.help_cmd(ctx)

    @commands.command(name="commands", description="List all registered commands")
    async def list_commands(self, ctx: commands.Context):
<<<<<<< HEAD
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        """Delegate to utility commands."""
        await self.utility_commands.list_commands(ctx)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.aria_profile(ctx)

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.carmyn_profile(ctx)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def shutdown_cmd(self, ctx: commands.Context):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delegate to system commands."""
        await self.system_commands.shutdown_cmd(ctx)
=======
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        """Delegate to system commands."""
        await self.system_commands.shutdown_cmd(ctx)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    @commands.command(name="restart", description="Restart the Discord bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def restart_cmd(self, ctx: commands.Context):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delegate to system commands."""
        await self.system_commands.restart_cmd(ctx)


__all__ = ["MessagingCommands"]
=======
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
=======
        """Delegate to system commands."""
        await self.system_commands.restart_cmd(ctx)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1


<<<<<<< HEAD
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
__all__ = ["MessagingCommands"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
