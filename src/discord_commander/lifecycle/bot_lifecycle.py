#!/usr/bin/env python3
"""Bot lifecycle management utilities."""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import logging
from typing import TYPE_CHECKING, Iterable

import discord

from .startup_helpers import add_snapshot_fields, add_system_info_fields
from .swarm_snapshot_helpers import get_swarm_snapshot

if TYPE_CHECKING:
    from ..unified_discord_bot import UnifiedDiscordBot

logger = logging.getLogger(__name__)


class BotLifecycleManager:
    """Manages bot lifecycle operations."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    async def setup_hook(self) -> None:
        """Setup hook for bot initialization - load all cogs."""
        await self._load_optional_cogs(
            [
                ("src.discord_commander.approval_commands", "ApprovalCommands"),
                ("src.discord_commander.commands", "CoreMessagingCommands"),
                ("src.discord_commander.commands", "SystemControlCommands"),
                ("src.discord_commander.commands", "OnboardingCommands"),
                ("src.discord_commander.commands", "UtilityCommands"),
                ("src.discord_commander.commands", "AgentManagementCommands"),
                ("src.discord_commander.commands", "ProfileCommands"),
                ("src.discord_commander.commands", "PlaceholderCommands"),
                ("src.discord_commander.swarm_showcase_commands", "SwarmShowcaseCommands"),
                ("src.discord_commander.github_book_viewer", "GitHubBookCommands"),
                ("src.discord_commander.trading_commands", "TradingCommands"),
                ("src.discord_commander.webhook_commands", "WebhookCommands"),
                ("src.discord_commander.tools_commands", "ToolsCommands"),
                ("src.discord_commander.file_share_commands", "FileShareCommands"),
                ("src.discord_commander.music_commands", "MusicCommands"),
            ]
        )
        self._log_command_summary()

    async def _load_optional_cogs(self, cogs: Iterable[tuple[str, str]]) -> None:
        for module_path, class_name in cogs:
            if not importlib.util.find_spec(module_path):
                continue
            module = importlib.import_module(module_path)
            cog_cls = getattr(module, class_name, None)
            if not cog_cls:
                continue
            await self.bot.add_cog(cog_cls(self.bot))
            self.logger.info("✅ Loaded cog: %s", class_name)

    def _log_command_summary(self) -> None:
        command_names = sorted(cmd.name for cmd in self.bot.commands)
        self.logger.info("Loaded %s commands", len(command_names))

    async def send_startup_message(self, channel: discord.TextChannel) -> None:
        """Send startup status message with a swarm snapshot."""
        embed = discord.Embed(
            title="🚀 Dream.OS Bot Online",
            description="Startup sequence complete.",
            color=0x27AE60,
        )
        snapshot = get_swarm_snapshot()
        add_snapshot_fields(embed, snapshot)
        add_system_info_fields(embed)
        await channel.send(embed=embed)

    async def graceful_shutdown(self) -> None:
        """Handle graceful shutdown cleanup."""
        await asyncio.sleep(0)
