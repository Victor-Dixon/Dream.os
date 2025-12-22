"""
System Control Commands
=======================

System control commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Thea session management, control panel, shutdown, and restart commands.

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import logging
import subprocess
import sys
import time
from pathlib import Path

import discord
from discord.ext import commands

from src.discord_commander.views import ConfirmRestartView, ConfirmShutdownView

logger = logging.getLogger(__name__)


class SystemControlCommands(commands.Cog):
    """System control commands for bot management."""

    def __init__(self, bot, gui_controller):
        """Initialize system control commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="thea", aliases=["thea-refresh"], description="Ensure Thea session (headless keepalive, interactive only if needed)")
    async def thea(self, ctx: commands.Context, force: str = ""):
        """
        Ensure Thea session with self-throttling keepalive.
        Usage: !thea [force]
        - Default: headless refresh if stale; interactive fallback if headless fails.
        - force: bypass throttle (set any value to force refresh).
        """
        allow_interactive = True
        min_interval = 0 if force else self.bot.thea_min_interval_minutes
        await ctx.send("🔄 Ensuring Thea session (headless)...")
        success = await self.bot.ensure_thea_session(allow_interactive=allow_interactive, min_interval_minutes=min_interval)
        if success:
            await ctx.send("✅ Thea session is healthy (cookies saved).")
        else:
            await ctx.send("❌ Thea session failed. Try again to trigger interactive login.")

    @commands.command(name="control", aliases=["panel", "menu"], description="Open main control panel")
    async def control_panel(self, ctx: commands.Context):
        """Open main interactive control panel."""
        try:
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="🎛️ SWARM CONTROL PANEL",
                description="**Complete Interactive Control Interface**\n\nUse buttons below to access all features:",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="📨 Messaging",
                value="Message individual agents or broadcast to all",
                inline=True,
            )
            embed.add_field(
                name="📊 Monitoring",
                value="View swarm status and task dashboards",
                inline=True,
            )
            embed.add_field(
                name="📚 Content",
                value="Access GitHub book and documentation",
                inline=True,
            )

            embed.set_footer(
                text="🐝 WE. ARE. SWARM. ⚡ Interactive GUI-Driven Control")
            await ctx.send(embed=embed, view=control_view)

        except Exception as e:
            self.logger.error(f"Error opening control panel: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    async def shutdown_cmd(self, ctx: commands.Context):
        """Gracefully shutdown the Discord bot."""
        try:
            # Confirmation embed
            embed = discord.Embed(
                title="🛑 Shutdown Requested",
                description="Are you sure you want to shutdown the bot?",
                color=discord.Color.red(),
            )

            # Create confirmation view
            view = ConfirmShutdownView()
            message = await ctx.send(embed=embed, view=view)

            # Wait for user confirmation (30 second timeout)
            await view.wait()

            if view.confirmed:
                # Announce shutdown
                shutdown_embed = discord.Embed(
                    title="👋 Bot Shutting Down",
                    description="Gracefully closing connections...",
                    color=discord.Color.orange(),
                )
                await ctx.send(embed=shutdown_embed)

                # Log shutdown
                self.logger.info("🛑 Shutdown command received - closing bot")

                # Close bot gracefully
                await self.bot.close()
            else:
                await message.edit(content="❌ Shutdown cancelled", embed=None, view=None)
        except Exception as e:
            self.logger.error(f"Error in shutdown command: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="startdiscord", aliases=["start_discord", "start"], description="Start the Discord bot and queue processor")
    async def startdiscord_cmd(self, ctx: commands.Context):
        """Start the Discord bot and message queue processor."""
        try:
            project_root = Path(__file__).parent.parent.parent.parent
            start_script = project_root / "tools" / "start_discord_system.py"

            if not start_script.exists():
                embed = discord.Embed(
                    title="❌ Failed to Start Discord Bot",
                    description=f"Start script not found: `{start_script}`",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                self.logger.error(f"Start script not found: {start_script}")
                return

            # Check if bot is already running
            if self.bot.is_ready():
                embed = discord.Embed(
                    title="ℹ️ Bot Already Running",
                    description="Discord bot is already running and connected!",
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=embed)
                return

            # Announce start
            embed = discord.Embed(
                title="🚀 Starting Discord System",
                description=(
                    "Starting Discord bot and message queue processor...\n"
                    "• Bot process will start\n"
                    "• Queue processor will start\n"
                    "• Both will run in background\n\n"
                    "Please wait a few seconds..."
                ),
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)

            # Start the system
            try:
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

                success_embed = discord.Embed(
                    title="✅ Discord System Started",
                    description=(
                        "Discord bot and queue processor started successfully!\n"
                        "• Bot should connect in a few seconds\n"
                        "• Queue processor is running\n"
                        "• Message delivery enabled"
                    ),
                    color=discord.Color.green(),
                )
                await ctx.send(embed=success_embed)
                self.logger.info("✅ Discord system started via !startdiscord command")

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Failed to Start Discord Bot",
                    description=f"Error starting Discord system: `{e}`",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=error_embed)
                self.logger.error(f"Error starting Discord system: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"Error in startdiscord command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="restart", description="Restart the Discord bot (true restart - fresh process)")
    async def restart_cmd(self, ctx: commands.Context):
        """Restart the Discord bot with a true process restart (kills current process, starts fresh)."""
        try:
            # Confirmation embed
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

            # Create confirmation view
            view = ConfirmRestartView()
            message = await ctx.send(embed=embed, view=view)

            # Wait for user confirmation (30 second timeout)
            await view.wait()

            if view.confirmed:
                # Announce restart
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

                # Log restart
                self.logger.info(
                    "🔄 True restart command received - killing process and starting fresh")

                # Perform true restart: spawn new process, then exit current
                self._perform_true_restart()

                # Close bot (will exit after new process starts)
                await self.bot.close()
            else:
                await message.edit(content="❌ Restart cancelled", embed=None, view=None)
        except Exception as e:
            self.logger.error(f"Error in restart command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    def _perform_true_restart(self):
        """Perform true restart: spawn fresh process for bot + queue processor, then exit current."""
        try:
            project_root = Path(__file__).parent.parent.parent
            # Use start_discord_system.py to start BOTH bot + queue processor
            # This ensures messages can be sent (queue processor is required)
            start_script = project_root / "tools" / "start_discord_system.py"

            if not start_script.exists():
                self.logger.error(f"Start script not found: {start_script}")
                return False

            # Spawn new process to start bot + queue processor fresh
            # This ensures all code is reloaded from disk (no module cache)
            # AND ensures message queue processor is running (required for message delivery)
            if sys.platform == 'win32':
                # Windows: Use CREATE_NEW_CONSOLE to run in separate window
                subprocess.Popen(
                    [sys.executable, str(start_script)],
                    cwd=str(project_root),
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Unix-like: use nohup or screen
                subprocess.Popen(
                    [sys.executable, str(start_script)],
                    cwd=str(project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )

            # Give new process a moment to start
            time.sleep(2)

            self.logger.info(
                "✅ New bot + queue processor processes spawned - current process will exit")
            return True

        except Exception as e:
            self.logger.error(
                f"Error performing true restart: {e}", exc_info=True)
            return False


