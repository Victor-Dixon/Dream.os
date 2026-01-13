#!/usr/bin/env python3
"""
Messaging Monitor Commands - Modular V2 Compliance
==================================================

Monitor commands extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular monitor commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

<<<<<<< HEAD
import discord
from discord.ext import commands
=======
try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

logger = logging.getLogger(__name__)


class MessagingMonitorCommands(commands.Cog):
    """Monitor-related messaging commands."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        """Initialize monitor commands."""
<<<<<<< HEAD
        super().__init__()
=======
        commands.Cog.__init__(self)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.bot = bot
        self.logger = logging.getLogger(__name__)

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


__all__ = ["MessagingMonitorCommands"]