#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord Event Handlers
======================

Handles all Discord bot event handlers (on_ready, on_message, etc.).

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import logging
import os
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

import discord

from .message_processing_helpers import (
    parse_message_format,
    validate_recipient,
    build_devlog_command,
    create_unified_message,
    handle_message_result,
)
from ..discord_event_bridge import get_discord_event_bridge

logger = logging.getLogger(__name__)


class DiscordEventHandlers:
    """Handles Discord bot event handlers."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        """Initialize event handlers."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.event_bridge = get_discord_event_bridge(bot)

    async def handle_on_ready(self) -> None:
        """Handle bot ready event."""
        try:
            # Update connection health
            self.bot.connection_healthy = True
            self.bot.last_heartbeat = time.time()

            # Prevent duplicate startup messages on reconnection
            if not hasattr(self.bot, '_startup_sent'):
                self.logger.info(
                    f"✅ Discord Commander Bot ready: {self.bot.user}")
                self.logger.info(f"📊 Guilds: {len(self.bot.guilds)}")

                # Initialize status change monitor
                try:
                    await self._initialize_status_monitor()
                except Exception as e:
                    self.logger.error(
                        f"❌ Error initializing status monitor: {e}", exc_info=True)
                    # Continue startup even if status monitor fails

                self.logger.info(
                    f"🤖 Latency: {round(self.bot.latency * 1000, 2)}ms")

                # Set bot presence
                try:
                    await self.bot.change_presence(
                        activity=discord.Activity(
                            type=discord.ActivityType.watching, name="the swarm 🐝")
                    )
                except Exception as e:
                    self.logger.error(
                        f"❌ Error setting bot presence: {e}", exc_info=True)
                    # Continue startup even if presence fails

                # Optional: auto-refresh Thea cookies headless on startup if env set
                if os.getenv("THEA_AUTO_REFRESH", "0") == "1":
                    try:
                        await self.bot.ensure_thea_session(
                            allow_interactive=False,
                            min_interval_minutes=self.bot.thea_min_interval_minutes
                        )
                    except Exception as e:
                        self.logger.error(
                            f"❌ Error ensuring Thea session: {e}", exc_info=True)
                        # Continue startup even if Thea session fails

                # Initialize event bridge
                try:
                    await self.event_bridge.initialize()
                    self.logger.info("✅ Discord event bridge initialized")
                except Exception as e:
                    self.logger.error(
                        f"❌ Error initializing event bridge: {e}", exc_info=True)
                    # Continue startup even if event bridge fails

                # Send startup message with control panel (only once)
                try:
                    await self.bot.send_startup_message()
                except Exception as e:
                    self.logger.error(
                        f"❌ Error sending startup message: {e}", exc_info=True)
                    # Continue startup even if startup message fails

                self.bot._startup_sent = True
            else:
                # Reconnection - just log, don't spam startup message
                self.logger.info(f"🔄 Discord Bot reconnected: {self.bot.user}")
        except Exception as e:
            self.logger.error(
                f"❌ Critical error in handle_on_ready: {e}", exc_info=True)
            # Don't re-raise - let bot continue running

    async def _initialize_status_monitor(self) -> None:
        """Initialize status change monitor."""
        try:
            from src.discord_commander.status_change_monitor import setup_status_monitor

            # Initialize scheduler for integration
            scheduler = None
            try:
                from src.orchestrators.overnight.scheduler import TaskScheduler
                scheduler = TaskScheduler()
                self.logger.info("✅ Task scheduler initialized")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not initialize scheduler: {e}")

            # Create status monitor with scheduler integration
            self.bot.status_monitor = setup_status_monitor(
                self.bot, self.bot.channel_id, scheduler=scheduler)

            # Wire scheduler to status monitor (bidirectional)
            if scheduler and self.bot.status_monitor:
                scheduler.status_monitor = self.bot.status_monitor
                self.logger.info("✅ Scheduler-StatusMonitor integration wired")

            # Auto-start status monitor
            if self.bot.status_monitor:
                try:
                    self.bot.status_monitor.start_monitoring()
                    self.logger.info("✅ Status change monitor started (auto)")
                except Exception as e:
                    self.logger.warning(
                        f"⚠️ Could not auto-start status monitor: {e}")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not start status monitor: {e}")

    async def handle_on_message(self, message: discord.Message) -> None:
        """Handle incoming messages with developer prefix mapping."""
        # Don't process bot's own messages
        if message.author == self.bot.user:
            return

        # Publish message to event bus first
        try:
            metadata = {
                'channel_id': str(message.channel.id),
                'channel_name': getattr(message.channel, 'name', 'unknown'),
                'author_id': str(message.author.id),
                'author_name': message.author.display_name,
                'guild_id': str(message.guild.id) if message.guild else None,
                'guild_name': message.guild.name if message.guild else None,
                'timestamp': message.created_at.isoformat(),
                'has_attachments': len(message.attachments) > 0,
                'is_reply': message.reference is not None
            }

            # Publish to event bridge
            await self.event_bridge.process_incoming_discord_message(
                message_content=message.content,
                author=message.author.display_name,
                channel=getattr(message.channel, 'name', str(message.channel.id)),
                message_id=str(message.id)
            )

        except Exception as e:
            self.logger.error(f"Error publishing message to event bridge: {e}")
            # Continue processing even if event bridge fails

        # Handle !music(song title) format before command processing
        content = message.content.strip()
        if content.lower().startswith('!music('):
            import re
            pattern = r'!music\(([^)]+)\)'
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                song_title = match.group(1).strip()
                message.content = f"!music {song_title}"

        # Process commands first
        await self.bot.process_commands(message)

        # Process D2A messages
        await self._process_d2a_message(message)

    async def _process_d2a_message(self, message: discord.Message) -> None:
        """Process D2A formatted messages."""
        content = message.content.strip()

        # Supported prefixes
        supported_prefixes = ('[D2A]', '[CHRIS]', '[ARIA]',
                              '[VICTOR]', '[CARYMN]', '[CHARLES]')

        # Check if message starts with a supported prefix
        has_prefix = any(content.startswith(prefix)
                         for prefix in supported_prefixes)

        # Also check for simple "Agent-X" format
        simple_format = content.split('\n')[0].strip().startswith('Agent-')

        if not (has_prefix or simple_format):
            return

        try:
            # Get developer prefix from Discord user ID
            developer_prefix = self.bot._get_developer_prefix(
                str(message.author.id))

            # Parse message format
            recipient, message_content, message_prefix = parse_message_format(
                content, has_prefix, developer_prefix)

            # Validate recipient
            if not await validate_recipient(message, recipient, self.logger):
                return

            # Send message to agent
            await self._send_message_to_agent(message, recipient, message_content, message_prefix)

        except Exception as e:
            self.logger.error(
                f"❌ Error processing message: {e}", exc_info=True)
            await message.add_reaction("❌")

    async def _send_message_to_agent(
        self, message: discord.Message, recipient: str,
        message_content: str, message_prefix: str
    ) -> None:
        """Send message to agent via MessageCoordinator."""
        from src.core.messaging_models_core import (
            UnifiedMessage,
            MessageCategory,
            UnifiedMessageType,
            UnifiedMessagePriority,
        )
        from src.core.messaging_templates import render_message
        from src.services.messaging_infrastructure import MessageCoordinator
        import uuid
        from datetime import datetime

        # Build per-agent devlog command
        devlog_command = build_devlog_command(recipient)

        # Create and render message
        msg = create_unified_message(message, recipient, message_content)
        rendered_message = render_message(msg, devlog_command=devlog_command)

        self.logger.info(
            f"📨 Processing {message_prefix} message: {recipient} - {message_content[:50]}...")

        # Queue message for PyAutoGUI delivery
        result = MessageCoordinator.send_to_agent(
            agent=recipient,
            message=rendered_message,
            priority="regular",
            use_pyautogui=True,
            message_category=MessageCategory.D2A,
        )

        # Handle result
        await handle_message_result(message, result, recipient, message_prefix, self.logger)

    async def handle_on_disconnect(self) -> None:
        """Handle bot disconnection."""
        self.bot.connection_healthy = False
        self.logger.warning(
            "⚠️ Discord Bot disconnected - will attempt to reconnect")
        # Reset startup flag on disconnect
        if hasattr(self.bot, '_startup_sent'):
            delattr(self.bot, '_startup_sent')

    async def handle_on_resume(self) -> None:
        """Handle bot reconnection after disconnect."""
        self.bot.connection_healthy = True
        self.bot.last_heartbeat = time.time()
        self.logger.info(
            "✅ Discord Bot reconnected successfully after disconnect")

    async def handle_on_socket_raw_receive(self, msg) -> None:
        """Track connection health via socket activity."""
        self.bot.last_heartbeat = time.time()
        if not self.bot.connection_healthy:
            self.bot.connection_healthy = True
            self.logger.debug("🔄 Connection health restored")

    async def handle_on_error(self, event: str, *args, **kwargs) -> None:
        """Handle errors in event handlers."""
        self.logger.error(f"❌ Error in event {event}: {args}", exc_info=True)
        # Don't close bot on errors - let it try to recover


# Convenience functions for direct handler access
async def handle_on_ready(bot: "UnifiedDiscordBot") -> None:
    """Handle on_ready event."""
    handler = DiscordEventHandlers(bot)
    await handler.handle_on_ready()


async def handle_on_message(bot: "UnifiedDiscordBot", message: discord.Message) -> None:
    """Handle on_message event."""
    handler = DiscordEventHandlers(bot)
    await handler.handle_on_message(message)


async def handle_on_disconnect(bot: "UnifiedDiscordBot") -> None:
    """Handle on_disconnect event."""
    handler = DiscordEventHandlers(bot)
    await handler.handle_on_disconnect()


async def handle_on_resume(bot: "UnifiedDiscordBot") -> None:
    """Handle on_resume event."""
    handler = DiscordEventHandlers(bot)
    await handler.handle_on_resume()


async def handle_on_socket_raw_receive(bot: "UnifiedDiscordBot", msg) -> None:
    """Handle on_socket_raw_receive event."""
    handler = DiscordEventHandlers(bot)
    await handler.handle_on_socket_raw_receive(msg)


async def handle_on_error(bot: "UnifiedDiscordBot", event: str, *args, **kwargs) -> None:
    """Handle on_error event."""
    handler = DiscordEventHandlers(bot)
    await handler.handle_on_error(event, *args, **kwargs)
