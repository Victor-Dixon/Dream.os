#!/usr/bin/env python3
"""
Twitch Chat Bridge
==================

Connects to Twitch IRC and handles:
- Receiving chat messages
- Sending agent responses
- Command routing

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import asyncio
import logging
import re
from typing import Callable, Optional

try:
    import irc.bot
    import irc.client
    IRC_AVAILABLE = True
except ImportError:
    IRC_AVAILABLE = False

logger = logging.getLogger(__name__)


class TwitchChatBridge:
    """
    Twitch IRC bridge for chat presence.

    Connects to Twitch IRC and routes messages to/from agents.
    """

    def __init__(
        self,
        username: str,
        oauth_token: str,
        channel: str,
        on_message: Optional[Callable[[dict], None]] = None,
    ):
        """
        Initialize Twitch chat bridge.

        Args:
            username: Twitch bot username
            oauth_token: Twitch OAuth token (oauth:xxxxx format)
            channel: Twitch channel name (without #)
            on_message: Callback for incoming messages
        """
        if not IRC_AVAILABLE:
            raise ImportError(
                "irc library required. Install with: pip install irc"
            )

        self.username = username
        self.oauth_token = oauth_token
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.on_message = on_message
        self.bot = None
        self.running = False

    async def connect(self) -> bool:
        """
        Connect to Twitch IRC.

        Returns:
            True if connected successfully
        """
        try:
            logger.info(f"🔌 Connecting to Twitch IRC as {self.username}")

            # Create IRC bot
            self.bot = TwitchIRCBot(
                server_list=[("irc.chat.twitch.tv", 6667)],
                nickname=self.username,
                realname=self.username,
                channel=self.channel,
                on_message=self._handle_message,
            )

            # Set OAuth token
            self.bot.connection.password = self.oauth_token

            # Connect
            self.bot.start()
            self.running = True

            logger.info(f"✅ Connected to Twitch channel: {self.channel}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to Twitch: {e}")
            return False

    def _handle_message(self, message_data: dict) -> None:
        """
        Handle incoming chat message.

        Args:
            message_data: Message data dictionary
        """
        if self.on_message:
            try:
                if asyncio.iscoroutinefunction(self.on_message):
                    asyncio.create_task(self.on_message(message_data))
                else:
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"Error in message callback: {e}", exc_info=True)

    async def send_message(self, message: str) -> bool:
        """
        Send message to Twitch chat.

        Args:
            message: Message to send

        Returns:
            True if sent successfully
        """
        if not self.bot or not self.running:
            logger.warning("⚠️ Not connected to Twitch")
            return False

        try:
            # Twitch IRC message format
            self.bot.connection.privmsg(self.channel, message)
            logger.info(f"📤 Sent to Twitch: {message[:50]}...")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    async def send_as_agent(self, agent_id: str, message: str) -> bool:
        """
        Send message as specific agent.

        Args:
            agent_id: Agent identifier
            message: Message content

        Returns:
            True if sent successfully
        """
        # Format message with agent identity
        formatted = f"[{agent_id}] {message}"

        return await self.send_message(formatted)

    def stop(self) -> None:
        """Stop Twitch connection."""
        self.running = False
        if self.bot:
            try:
                self.bot.connection.quit("Agent system shutdown")
                logger.info("🔌 Disconnected from Twitch")
            except Exception:
                pass


class TwitchIRCBot(irc.bot.SingleServerIRCBot):
    """IRC bot implementation for Twitch."""

    def __init__(
        self,
        server_list: list,
        nickname: str,
        realname: str,
        channel: str,
        on_message: Optional[Callable[[dict], None]] = None,
    ):
        """
        Initialize Twitch IRC bot.

        Args:
            server_list: List of (host, port) tuples
            nickname: Bot nickname
            realname: Bot realname
            channel: Channel to join
            on_message: Message callback
        """
        super().__init__(server_list, nickname, realname)
        self.channel = channel
        self.on_message = on_message

    def on_welcome(self, connection, event) -> None:
        """Called when bot connects to IRC."""
        logger.info("✅ Connected to Twitch IRC")
        # Join channel
        connection.join(self.channel)
        logger.info(f"📺 Joined channel: {self.channel}")

    def on_join(self, connection, event) -> None:
        """Called when bot joins channel."""
        logger.info(f"✅ Joined {event.target}")

    def on_pubmsg(self, connection, event) -> None:
        """
        Called when public message received.

        Args:
            connection: IRC connection
            event: IRC event
        """
        # Parse Twitch message
        message_text = event.arguments[0] if event.arguments else ""
        username = event.source.nick

        # Skip bot's own messages
        if username == self.connection.get_nickname():
            return

        # Extract Twitch-specific metadata
        tags = {}
        if hasattr(event, "tags"):
            tags = event.tags

        message_data = {
            "username": username,
            "message": message_text,
            "channel": self.channel,
            "timestamp": event.timestamp if hasattr(event, "timestamp") else None,
            "tags": tags,
            "raw_event": event,
        }

        # Call callback
        if self.on_message:
            try:
                if asyncio.iscoroutinefunction(self.on_message):
                    asyncio.create_task(self.on_message(message_data))
                else:
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"Error in message handler: {e}", exc_info=True)

    def on_privmsg(self, connection, event) -> None:
        """
        Called when private message received.

        Args:
            connection: IRC connection
            event: IRC event
        """
        # Handle private messages similarly
        message_text = event.arguments[0] if event.arguments else ""
        username = event.source.nick

        message_data = {
            "username": username,
            "message": message_text,
            "channel": "PRIVATE",
            "timestamp": None,
            "tags": {},
            "raw_event": event,
        }

        if self.on_message:
            try:
                if asyncio.iscoroutinefunction(self.on_message):
                    asyncio.create_task(self.on_message(message_data))
                else:
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"Error in private message handler: {e}", exc_info=True)


# Alternative: WebSocket-based Twitch connection (modern approach)
class TwitchWebSocketBridge:
    """
    Modern Twitch WebSocket bridge (PubSub/EventSub).

    More reliable than IRC for production use.
    """

    def __init__(
        self,
        client_id: str,
        access_token: str,
        channel_id: str,
        on_message: Optional[Callable[[dict], None]] = None,
    ):
        """
        Initialize WebSocket bridge.

        Args:
            client_id: Twitch API client ID
            access_token: Twitch API access token
            channel_id: Twitch channel ID
            on_message: Message callback
        """
        self.client_id = client_id
        self.access_token = access_token
        self.channel_id = channel_id
        self.on_message = on_message
        self.running = False

    async def connect(self) -> bool:
        """Connect to Twitch WebSocket."""
        # Implementation would use Twitch EventSub WebSocket
        # This is a placeholder for the modern approach
        logger.warning("⚠️ WebSocket bridge not yet implemented, use IRC bridge")
        return False


__all__ = ["TwitchChatBridge", "TwitchIRCBot", "TwitchWebSocketBridge"]




