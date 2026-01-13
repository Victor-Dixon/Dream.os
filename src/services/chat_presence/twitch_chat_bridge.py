#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Twitch Chat Bridge - Main Interface
====================================

Main interface for Twitch chat integration.
Coordinates IRC and WebSocket bridges.

V2 Compliant: Modular main interface
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import asyncio
import logging
import threading
from typing import Any, Callable, Optional, Dict, List

from .twitch_exceptions import TwitchBridgeError, TwitchConfigError
from .twitch_irc_bot import TwitchIRCBot
from .twitch_websocket_bridge import TwitchWebSocketBridge

logger = logging.getLogger(__name__)


class TwitchChatBridge:
    """Main Twitch chat bridge coordinating IRC and WebSocket connections."""

    def __init__(self,
                 username: str,
                 token: str,
                 channel: str,
                 message_handler: Optional[Callable] = None,
                 connection_handler: Optional[Callable] = None,
                 use_websocket: bool = False):
        """Initialize the Twitch chat bridge."""
        self.username = username
        self.token = token
        self.channel = channel
        self.message_handler = message_handler
        self.connection_handler = connection_handler
        self.use_websocket = use_websocket

        # Bridge instances
        self.irc_bot = None
        self.websocket_bridge = None
        self.connected = False

        # Configuration validation
        self._validate_config()

        logger.info(f"TwitchChatBridge initialized for channel {channel}")

    def _validate_config(self):
        """Validate bridge configuration."""
        if not self.username:
            raise TwitchConfigError("Username is required")

        if not self.token:
            raise TwitchConfigError("Access token is required")

        if not self.channel:
            raise TwitchConfigError("Channel is required")

        # Remove # from channel if present
        self.channel = self.channel.lstrip('#')

    def connect(self) -> bool:
        """Connect to Twitch chat."""
        try:
            if self.use_websocket:
                return asyncio.run(self._connect_websocket())
            else:
                return self._connect_irc()

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def _connect_irc(self) -> bool:
        """Connect using IRC bot."""
        try:
            def message_callback(username: str, message: str, channel: str):
                if self.message_handler:
                    self.message_handler(username, message, channel)

            def connection_callback(status: str, channel: str):
                if status == "connected":
                    self.connected = True
                elif status == "disconnected":
                    self.connected = False

                if self.connection_handler:
                    self.connection_handler(status, channel)

            self.irc_bot = TwitchIRCBot(
                self.username,
                self.token,
                self.channel,
                message_callback,
                connection_callback
            )

            # Start IRC bot in separate thread
            irc_thread = threading.Thread(target=self.irc_bot.start)
            irc_thread.daemon = True
            irc_thread.start()

            # Wait a moment for connection
            import time
            time.sleep(2)

            return self.irc_bot.is_connected()

        except Exception as e:
            logger.error(f"IRC connection failed: {e}")
            return False

    async def _connect_websocket(self) -> bool:
        """Connect using WebSocket bridge."""
        try:
            async def message_callback(username: str, message: str, channel: str):
                if self.message_handler:
                    await self.message_handler(username, message, channel)

            async def connection_callback(status: str, channel: str):
                if status == "connected":
                    self.connected = True
                elif status == "disconnected":
                    self.connected = False

                if self.connection_handler:
                    await self.connection_handler(status, channel)

            self.websocket_bridge = TwitchWebSocketBridge(
                self.token,
                message_callback,
                connection_callback
            )

            connected = await self.websocket_bridge.connect()
            if connected:
                # Start listening in background
                asyncio.create_task(self.websocket_bridge.start_listening())

            return connected

        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from Twitch chat."""
        try:
            if self.use_websocket and self.websocket_bridge:
                asyncio.run(self.websocket_bridge.disconnect())
            elif self.irc_bot:
                self.irc_bot.disconnect_gracefully()

            self.connected = False
            logger.info("Disconnected from Twitch chat")

        except Exception as e:
            logger.error(f"Disconnect error: {e}")

    def send_message(self, message: str) -> bool:
        """Send a message to the channel."""
        try:
            if not self.connected:
                logger.warning("Not connected, cannot send message")
                return False

            if self.use_websocket and self.websocket_bridge:
                return asyncio.run(self.websocket_bridge.send_message(self.channel, message))
            elif self.irc_bot:
                return self.irc_bot.send_message(message)
            else:
                return False

        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if bridge is connected."""
        if self.use_websocket and self.websocket_bridge:
            return self.websocket_bridge.is_connected()
        elif self.irc_bot:
            return self.irc_bot.is_connected()
        else:
            return False

    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information."""
        return {
            "connected": self.is_connected(),
            "channel": self.channel,
            "username": self.username,
            "method": "websocket" if self.use_websocket else "irc",
            "bridge_type": "TwitchWebSocketBridge" if self.use_websocket else "TwitchIRCBot"
        }


__all__ = ["TwitchChatBridge"]