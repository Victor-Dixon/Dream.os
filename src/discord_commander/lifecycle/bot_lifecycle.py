#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Bot Lifecycle Management
========================

Handles bot startup, shutdown, and lifecycle operations.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

import discord

from .startup_helpers import add_snapshot_fields, add_system_info_fields
from .swarm_snapshot_helpers import get_swarm_snapshot

logger = logging.getLogger(__name__)


class BotLifecycleManager:
    """Manages bot lifecycle operations."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        """Initialize lifecycle manager."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    async def setup_hook(self) -> None:
        """Setup hook for bot initialization - load all cogs."""
        try:
            await self._load_approval_commands()
            await self._load_messaging_commands()
            await self._load_swarm_showcase_commands()
            await self._load_github_book_commands()
            await self._load_trading_commands()
            await self._load_webhook_commands()
            await self._load_tools_commands()
            await self._load_file_share_commands()
            await self._load_music_commands()
            self._log_command_summary()
        except Exception as e:
            self.logger.error(f"Error loading commands: {e}", exc_info=True)

    async def _load_approval_commands(self) -> None:
        """Load approval commands cog."""
        try:
            from src.discord_commander.approval_commands import ApprovalCommands
            await self.bot.add_cog(ApprovalCommands(self.bot))
            self.logger.info("✅ Approval commands loaded")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load approval commands: {e}")

    async def _load_messaging_commands(self) -> None:
        """Load messaging commands cogs (V2 compliant modules)."""
        try:
            from src.discord_commander.commands import (
                CoreMessagingCommands,
                SystemControlCommands,
                OnboardingCommands,
                UtilityCommands,
                AgentManagementCommands,
                ProfileCommands,
                PlaceholderCommands,
<<<<<<< HEAD
<<<<<<< HEAD
                MessagingCommands,
            )
            
            await self.bot.add_cog(CoreMessagingCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(SystemControlCommands(self.bot))
            await self.bot.add_cog(OnboardingCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(UtilityCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(AgentManagementCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(ProfileCommands(self.bot))
            await self.bot.add_cog(PlaceholderCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(MessagingCommands(self.bot, self.bot.gui_controller))
            
            # Verify gui and control commands are registered
=======
=======
                MessagingCommands,
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            )
            
            await self.bot.add_cog(CoreMessagingCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(SystemControlCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(OnboardingCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(UtilityCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(AgentManagementCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(ProfileCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(PlaceholderCommands(self.bot, self.bot.gui_controller))
            await self.bot.add_cog(MessagingCommands(self.bot, self.bot.gui_controller))
            
<<<<<<< HEAD
            # Verify gui command is registered
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            # Verify gui and control commands are registered
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            gui_command = self.bot.get_command("gui")
            if gui_command:
                self.logger.info(f"✅ GUI command registered: {gui_command.name}")
            else:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                self.logger.warning("⚠️ GUI command not found after loading messaging commands")

            control_command = self.bot.get_command("control")
            if control_command:
                self.logger.info(f"✅ Control command registered: {control_command.name}")
            else:
                self.logger.warning("⚠️ Control command not found after loading messaging commands")
<<<<<<< HEAD
=======
                self.logger.warning("⚠️ GUI command not found after loading CoreMessagingCommands")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            
            self.logger.info("✅ All messaging command cogs loaded (V2 compliant modules)")
        except Exception as e:
            self.logger.error(f"❌ Error loading messaging commands: {e}", exc_info=True)
            raise

    async def _load_swarm_showcase_commands(self) -> None:
        """Load swarm showcase commands cog."""
        from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
        await self.bot.add_cog(SwarmShowcaseCommands(self.bot))
        self.logger.info("✅ Swarm showcase commands loaded")

    async def _load_github_book_commands(self) -> None:
        """Load GitHub book viewer cog."""
        from src.discord_commander.github_book_viewer import GitHubBookCommands
        await self.bot.add_cog(GitHubBookCommands(self.bot))
        self.logger.info("✅ GitHub Book Viewer loaded - WOW FACTOR READY!")

    async def _load_trading_commands(self) -> None:
        """Load trading commands cog."""
        from src.discord_commander.trading_commands import TradingCommands
        await self.bot.add_cog(TradingCommands(self.bot))
        self.logger.info("✅ Trading commands loaded")

    async def _load_webhook_commands(self) -> None:
        """Load webhook commands cog."""
        from src.discord_commander.webhook_commands import WebhookCommands
        await self.bot.add_cog(WebhookCommands(self.bot))
        self.logger.info("✅ Webhook commands loaded")

    async def _load_tools_commands(self) -> None:
        """Load tools commands cog."""
        try:
            from src.discord_commander.tools_commands import ToolsCommands
            await self.bot.add_cog(ToolsCommands(self.bot))
            self.logger.info("✅ Tools commands loaded")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load tools commands: {e}")

    async def _load_file_share_commands(self) -> None:
        """Load file share commands."""
        try:
            from src.discord_commander.file_share_commands import setup as setup_file_share
            await setup_file_share(self.bot)
            self.logger.info("✅ File share commands loaded")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load file share commands: {e}")

    async def _load_music_commands(self) -> None:
        """Load music commands."""
        try:
            from src.discord_commander.music_commands import setup
            await setup(self.bot)
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load music commands: {e}")

    def _log_command_summary(self) -> None:
        """Log command registration summary."""
        all_commands = [cmd.name for cmd in self.bot.walk_commands()]
        self.logger.info(f"📊 Total commands registered: {len(all_commands)}")
        self.logger.info(f"📋 All commands: {', '.join(sorted(all_commands))}")

    async def send_startup_message(self) -> None:
        """Send startup message to configured channel with swarm work snapshot."""
        try:
            channel = await self._get_startup_channel()
            if not channel:
                return

            # Wait a moment to ensure all status.json files are written/flushed
            # This ensures we get a fresh snapshot, not stale cached data
            await asyncio.sleep(0.5)
            self.logger.info("📊 Generating fresh swarm snapshot...")
            
            snapshot = get_swarm_snapshot(self.logger)
            self.logger.info(f"✅ Fresh snapshot generated: {len(snapshot.get('active_agents', []))} active agents")
            
            snapshot_view, snapshot_embed = self._create_snapshot_view(snapshot)

            embed = self._create_startup_embed(snapshot, snapshot_embed)

            # Send snapshot view if available
            if snapshot_view and snapshot_embed:
                await channel.send(embed=snapshot_embed, view=snapshot_view)

            # Send control panel with startup message
            control_view = self.bot.gui_controller.create_control_panel()
            await channel.send(embed=embed, view=control_view)
            self.logger.info("✅ Startup message with control panel sent successfully")

        except Exception as e:
            self.logger.error(f"Error sending startup message: {e}")

    async def _get_startup_channel(self) -> discord.TextChannel | None:
        """Get channel for startup message."""
        channel = None

        if self.bot.channel_id:
            channel = self.bot.get_channel(self.bot.channel_id)

        if not channel:
            # Find first available text channel
            for guild in self.bot.guilds:
                for text_channel in guild.text_channels:
                    channel = text_channel
                    self.logger.info(f"Using channel: {channel.name} ({channel.id})")
                    break
                if channel:
                    break

        if not channel:
            self.logger.warning("No text channels available for startup message")

        return channel

    def _create_snapshot_view(self, snapshot: dict) -> tuple:
        """Create swarm snapshot view."""
        try:
            from src.discord_commander.views.swarm_snapshot_view import SwarmSnapshotView
            snapshot_view = SwarmSnapshotView(snapshot)
            snapshot_embed = snapshot_view.create_snapshot_embed()
            return snapshot_view, snapshot_embed
        except Exception as e:
            self.logger.warning(f"Could not create snapshot view: {e}")
            return None, None

    def _create_startup_embed(self, snapshot: dict, snapshot_embed) -> discord.Embed:
        """Create startup embed."""
        embed = discord.Embed(
            title="🐝 Discord Commander - SWARM CONTROL CENTER",
            description="**Complete Multi-Agent Command & Showcase System**",
            color=0x3498DB,
            timestamp=discord.utils.utcnow(),
        )

        # Add snapshot fields if no snapshot embed
        if not snapshot_embed:
            add_snapshot_fields(embed, snapshot, self.logger)

        # Add system info fields
        add_system_info_fields(embed, self.bot)

        embed.set_footer(
            text="🐝 WE. ARE. SWARM. ⚡ Every agent is the face of the swarm")

        return embed

    async def close(self) -> None:
        """Clean shutdown."""
        self.logger.info("🛑 Unified Discord Bot shutting down...")
        # Mark as intentional shutdown to prevent reconnection loop
        self.bot._intentional_shutdown = True
        # Note: Actual bot.close() is called by the bot's close() method after this

