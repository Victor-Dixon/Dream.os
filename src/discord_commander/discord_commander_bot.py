#!/usr/bin/env python3
"""
Discord Commander Bot - Single V2 Compliant Command Center
===========================================================

Main bot setup with service loading. Commands in separate modules.
V2 Compliant: Core bot <400 lines, commands split logically.

Author: Agent-5 (Business Intelligence & Co-Captain)
Consolidated: 2025-11-05
Renamed: 2025-11-17 (unified_discord_bot.py → discord_commander_bot.py)
Architecture: Main bot + unified commands modules
"""

import asyncio
import importlib.util
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import discord
from discord.ext import commands

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not required, env vars can be set manually

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class UnifiedSwarmBot(commands.Bot):
    """Single unified Discord bot for all swarm operations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_reader = None
        self.messaging_controller = None
        self.pulse_subscriber = None
        self._load_services()

    def _load_services(self):
        """Load all required services."""
        try:
            # Status reader
            spec = importlib.util.spec_from_file_location(
                "status_reader", Path(__file__).parent / "status_reader.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.status_reader = module.StatusReader()

            # Messaging controller
            from src.discord_commander.messaging_controller import DiscordMessagingController
            from src.services.direct_messaging_service import DirectMessagingService

            self.messaging_controller = DiscordMessagingController(DirectMessagingService())

            # Pulse subscriber (optional)
            try:
                from src.discord_commander.pulse_subscriber import (
                    DiscordPulseSubscriber,
                    set_subscriber,
                )

                self.pulse_subscriber = DiscordPulseSubscriber(self)
                set_subscriber(self.pulse_subscriber)
            except Exception as e:
                logger.warning(f"Pulse subscriber not available: {e}")

        except Exception as e:
            logger.warning(f"Service loading issue: {e}")

    async def on_ready(self):
        """Bot startup handler."""
        logger.info(f"✅ Unified Discord Bot connected as {self.user}")

        # Start pulse subscriber if available
        if self.pulse_subscriber:
            channel_id_str = os.getenv("DISCORD_CHANNEL_ID")
            if channel_id_str:
                try:
                    channel_id = int(channel_id_str)
                    self.pulse_subscriber.configure(channel_id)
                    await self.pulse_subscriber.start()
                    logger.info(f"✅ Pulse subscriber active (channel: {channel_id})")
                except Exception as e:
                    logger.warning(f"Pulse start failed: {e}")

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="swarm intelligence 🤖"
            )
        )

        # Send startup notification
        await self._send_startup_notification()

    async def _send_startup_notification(self):
        """Send startup notification to first available channel."""
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    embed = discord.Embed(
                        title="🤖 UNIFIED SWARM BOT ONLINE",
                        description="**Single V2 Compliant Command Center** - All systems operational!",
                        color=discord.Color.from_rgb(102, 126, 234),
                        timestamp=datetime.utcnow(),
                    )
                    embed.add_field(
                        name="⚡ Core Commands",
                        value=(
                            "**Messaging:** `!message Agent-X <text>` | `!broadcast <text>`\n"
                            "**Status:** `!quick` | `!agents`\n"
                            "**Website:** `!website` | `!analytics 7` | `!performance`\n"
                            "**Sessions:** `!session`\n"
                            "**Help:** `!help`"
                        ),
                        inline=False,
                    )
                    embed.set_footer(text="Type !help for complete command reference")
                    await channel.send(embed=embed)
                    logger.info(f"📢 Startup notification sent to {guild.name}")
                    return


async def setup_unified_bot():
    """Setup and run the unified Discord bot."""
    # Bot setup
    intents = discord.Intents.default()
    intents.message_content = True

    bot = UnifiedSwarmBot(
        command_prefix="!",
        intents=intents,
        help_command=None,  # We provide custom help
    )

    # Load all command modules
    await load_unified_commands(bot)

    # Start bot
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN not found!")
        print("SETUP: Set DISCORD_BOT_TOKEN in .env file")
        return

    try:
        logger.info("🚀 Starting Unified Discord Bot...")
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("❌ Invalid Discord bot token!")
    except Exception as e:
        logger.error(f"❌ Bot startup error: {e}")
        raise


async def load_unified_commands(bot):
    """Load all unified command modules."""
    try:
        # Core messaging commands
        from .unified_messaging_commands import UnifiedMessagingCommands

        await bot.add_cog(UnifiedMessagingCommands(bot))
        logger.info("✅ Messaging commands loaded")

        # Status and info commands
        from .unified_status_commands import UnifiedStatusCommands

        await bot.add_cog(UnifiedStatusCommands(bot))
        logger.info("✅ Status commands loaded")

        # Website monitoring commands
        from .website_monitoring_commands import WebsiteMonitoringCommands

        await bot.add_cog(WebsiteMonitoringCommands(bot))
        logger.info("✅ Website monitoring commands loaded")

        # Session commands (basic implementation)
        from .unified_session_commands import UnifiedSessionCommands

        await bot.add_cog(UnifiedSessionCommands(bot))
        logger.info("✅ Session commands loaded")

        # Onboarding commands (soft, hard, start)
        from .unified_onboarding_commands import UnifiedOnboardingCommands

        await bot.add_cog(UnifiedOnboardingCommands(bot))
        logger.info("✅ Onboarding commands loaded")

        # Help command
        from .unified_help_commands import UnifiedHelpCommands

        await bot.add_cog(UnifiedHelpCommands(bot))
        logger.info("✅ Help commands loaded")

        # Cycle planner commands
        from .cycle_planner_commands import CyclePlannerCommands

        await bot.add_cog(CyclePlannerCommands(bot))
        logger.info("✅ Cycle planner commands loaded")

        # Monitoring commands (RESUME protocol, agent monitoring)
        from .monitoring_commands import setup as setup_monitoring

        await setup_monitoring(bot)
        logger.info("✅ Monitoring commands loaded (!resume, !monitor)")

        # Controller command (unified interface)
        from .controller_commands import setup as setup_controller

        await setup_controller(bot)
        logger.info("✅ Controller command loaded (!controller)")

        # Swarm coordination commands (!swarm, !agent, !gas, !inbox)
        try:
            from .swarm_coordination_commands import setup as setup_swarm

            await setup_swarm(bot)
            logger.info("✅ Swarm coordination commands loaded (!swarm, !agent, !gas, !inbox)")
        except Exception as e:
            logger.warning(f"⚠️ Swarm coordination commands not available: {e}")

        # Options framework commands (!options, !greeks, !signals, !performance)
        try:
            from .options_framework_commands import setup as setup_options

            await setup_options(bot)
            logger.info("✅ Options framework commands loaded (!options, !greeks, !signals, !performance)")
        except Exception as e:
            logger.warning(f"⚠️ Options framework commands not available: {e}")

        # Automation commands (!obs, !pieces, etc.)
        try:
            from .automation_commands import AutomationCommands

            await bot.add_cog(AutomationCommands(bot))
            logger.info("✅ Automation commands loaded (!obs, !pieces)")
        except Exception as e:
            logger.warning(f"⚠️ Automation commands not available: {e}")

        # Passdown commands (!passdown, !extract)
        try:
            from .passdown_commands import PassdownCommands

            await bot.add_cog(PassdownCommands(bot))
            logger.info("✅ Passdown commands loaded (!passdown, !extract)")
        except Exception as e:
            logger.warning(f"⚠️ Passdown commands not available: {e}")

        # Interactive commands (!agent_interact, !swarm_status)
        try:
            from .interactive_commands import InteractiveCommands

            await bot.add_cog(InteractiveCommands(bot, bot.messaging_controller))
            logger.info("✅ Interactive commands loaded (!agent_interact, !swarm_status)")
        except Exception as e:
            logger.warning(f"⚠️ Interactive commands not available: {e}")

        # Kanban board commands (!kanban, !tasks)
        try:
            from .kanban_board import KanbanCommands

            await bot.add_cog(KanbanCommands(bot))
            logger.info("✅ Kanban commands loaded (!kanban, !tasks)")
        except Exception as e:
            logger.warning(f"⚠️ Kanban commands not available: {e}")

        # Pulse commands (!pulse_status, !pulse_tail, !pulse_agents)
        try:
            from .pulse_commands import PulseCommands

            await bot.add_cog(PulseCommands(bot))
            logger.info("✅ Pulse commands loaded (!pulse_status, !pulse_tail, !pulse_agents)")
        except Exception as e:
            logger.warning(f"⚠️ Pulse commands not available: {e}")

        # GitHub Book commands (!github_book, !goldmines, !book_stats)
        try:
            from .github_book_viewer import GitHubBookCommands

            await bot.add_cog(GitHubBookCommands(bot))
            logger.info("✅ GitHub Book commands loaded (!github_book, !goldmines, !book_stats)")
        except Exception as e:
            logger.warning(f"⚠️ GitHub Book commands not available: {e}")

        logger.info("🎯 All unified command modules loaded successfully")

    except Exception as e:
        logger.error(f"❌ Command loading error: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(setup_unified_bot())
    except KeyboardInterrupt:
        logger.info("👋 Unified bot shutdown complete")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)
