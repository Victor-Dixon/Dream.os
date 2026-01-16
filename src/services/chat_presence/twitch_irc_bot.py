#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

DEPRECATED: Twitch IRC Bot
==========================

⚠️  THIS IMPLEMENTATION HAS BEEN DEPRECATED ⚠️

The Twitch IRC bot has been deprecated in favor of the EventSub webhook server.
Please use: src.services.chat_presence.twitch_eventsub_server

Reason: EventSub provides more reliable integration with Twitch services,
especially for channel point redemptions and other events.

Old functionality:
- IRC bot implementation for Twitch chat integration

V2 Compliant: Modular IRC bot
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
Deprecated: 2026-01-15 (Replaced by EventSub server)
"""

import logging
import re
import time
from typing import Any, Callable, Optional

try:
    import irc.bot
    import irc.client
    IRC_AVAILABLE = True
except ImportError:
    IRC_AVAILABLE = False
    irc = None

from .twitch_exceptions import TwitchConnectionError, TwitchMessageError

logger = logging.getLogger(__name__)


class TwitchIRCBot(irc.bot.SingleServerIRCBot if IRC_AVAILABLE else object):
    """IRC bot for Twitch chat integration."""

    def __init__(self,
                 username: str,
                 token: str,
                 channel: str,
                 message_handler: Optional[Callable] = None,
                 connection_handler: Optional[Callable] = None):
        """Initialize the IRC bot."""
        if not IRC_AVAILABLE:
            raise TwitchConnectionError("IRC library not available")

        # Remove # from channel name if present
        channel = channel.lstrip('#')

        # IRC server details for Twitch
        server = "irc.chat.twitch.tv"
        port = 6667

        # Initialize the bot
        super().__init__(
            [(server, port, f"oauth:{token}")],
            username,
            username
        )

        self.channel = f"#{channel}"
        self.username = username
        self.message_handler = message_handler
        self.connection_handler = connection_handler
        self.connected = False
        self.last_ping = time.time()

        logger.info(f"Twitch IRC Bot initialized for channel {self.channel}")

    def on_welcome(self, connection, event):
        """Handle welcome event (successful connection)."""
        try:
            logger.info(f"Connected to Twitch IRC as {self.username}")
            self.connected = True

            # Join the channel
            connection.join(self.channel)
            logger.info(f"Joined channel {self.channel}")

            # Notify connection handler
            if self.connection_handler:
                self.connection_handler("connected", self.channel)

        except Exception as e:
            logger.error(f"Welcome event error: {e}")
            raise TwitchConnectionError(f"Failed to join channel: {e}")

    def on_join(self, connection, event):
        """Handle channel join event."""
        logger.info(f"Successfully joined {event.target}")
        if self.connection_handler:
            self.connection_handler("joined", event.target)

    def on_disconnect(self, connection, event):
        """Handle disconnection event."""
        logger.warning("Disconnected from Twitch IRC")
        self.connected = False
        if self.connection_handler:
            self.connection_handler("disconnected", None)

    def on_pubmsg(self, connection, event):
        """Handle public messages."""
        try:
            message = event.arguments[0]
            username = event.source.split('!')[0]

            # Skip bot's own messages
            if username.lower() == self.username.lower():
                return

            logger.debug(f"Received message from {username}: {message}")

            # Notify message handler
            if self.message_handler:
                self.message_handler(username, message, self.channel)

        except Exception as e:
            logger.error(f"Message handling error: {e}")
            raise TwitchMessageError(f"Failed to process message: {e}")

    def send_message(self, message: str) -> bool:
        """Send a message to the channel."""
        try:
            if not self.connected:
                logger.warning("Not connected, cannot send message")
                return False

            # Rate limiting check (basic)
            current_time = time.time()
            if current_time - self.last_ping < 1.5:  # Twitch rate limit
                time.sleep(1.5 - (current_time - self.last_ping))

            self.connection.privmsg(self.channel, message)
            self.last_ping = time.time()

            logger.debug(f"Sent message to {self.channel}: {message}")
            return True

        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if bot is connected."""
        return self.connected

    def disconnect_gracefully(self):
        """Disconnect from IRC gracefully."""
        try:
            if self.connected:
                self.disconnect()
                logger.info("Gracefully disconnected from Twitch IRC")
        except Exception as e:
            logger.error(f"Error during graceful disconnect: {e}")


__all__ = ["TwitchIRCBot"]