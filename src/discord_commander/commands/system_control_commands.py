<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
"""
System Control Commands - Modular V2 Compliance
===============================================

System control commands (shutdown, restart) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular system control commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

import discord
from discord.ext import commands
from .command_base import BaseDiscordCog

logger = logging.getLogger(__name__)


class SystemControlCommands(BaseDiscordCog, commands.Cog):
    """System control commands for bot shutdown and restart."""

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
            start_script = self._get_start_script_path()
            if not start_script.exists():
                self.logger.error(f"Start script not found: {start_script}")
                return False

            self._spawn_restart_process(start_script)
            self._wait_and_log_restart()
            return True
        except Exception as e:
            self.logger.error(f"Error performing true restart: {e}", exc_info=True)
            return False

    def _get_start_script_path(self) -> Path:
        """Get path to the start script."""
        project_root = Path(__file__).parent.parent.parent.parent
        return project_root / "tools" / "start_discord_system.py"

    def _spawn_restart_process(self, start_script: Path) -> None:
        """Spawn the restart process with platform-specific settings."""
        project_root = start_script.parent.parent
        cmd = [sys.executable, str(start_script)]
        kwargs = {
            'cwd': str(project_root),
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL
        }

        if sys.platform == 'win32':
            kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
        else:
            kwargs['start_new_session'] = True

        subprocess.Popen(cmd, **kwargs)

    def _wait_and_log_restart(self) -> None:
        """Wait briefly and log successful restart."""
        import time
        time.sleep(2)
        self.logger.info("✅ New bot + queue processor processes spawned - current process will exit")


__all__ = ["SystemControlCommands"]
=======
=======
#!/usr/bin/env python3
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
"""
System Control Commands - Modular V2 Compliance
===============================================

System control commands (shutdown, restart) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular system control commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
import subprocess
import sys
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

logger = logging.getLogger(__name__)


class SystemControlCommands(commands.Cog):
    """System control commands for bot shutdown and restart."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        """Initialize system control commands."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.logger = logging.getLogger(__name__)

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
            start_script = self._get_start_script_path()
            if not start_script.exists():
                self.logger.error(f"Start script not found: {start_script}")
                return False

            self._spawn_restart_process(start_script)
            self._wait_and_log_restart()
            return True
        except Exception as e:
            self.logger.error(f"Error performing true restart: {e}", exc_info=True)
            return False

    def _get_start_script_path(self) -> Path:
        """Get path to the start script."""
        project_root = Path(__file__).parent.parent.parent.parent
        return project_root / "tools" / "start_discord_system.py"

<<<<<<< HEAD
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    def _spawn_restart_process(self, start_script: Path) -> None:
        """Spawn the restart process with platform-specific settings."""
        project_root = start_script.parent.parent
        cmd = [sys.executable, str(start_script)]
        kwargs = {
            'cwd': str(project_root),
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL
        }

        if sys.platform == 'win32':
            kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
        else:
            kwargs['start_new_session'] = True

        subprocess.Popen(cmd, **kwargs)

    def _wait_and_log_restart(self) -> None:
        """Wait briefly and log successful restart."""
        import time
        time.sleep(2)
        self.logger.info("✅ New bot + queue processor processes spawned - current process will exit")


__all__ = ["SystemControlCommands"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
