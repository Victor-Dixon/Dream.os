#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

import asyncio
import logging
import threading
from typing import Any, Callable

try:
    import irc.bot
    IRC_AVAILABLE = True
except ImportError:
    IRC_AVAILABLE = False
    irc = None

logger = logging.getLogger(__name__)


class TwitchBridgeError(Exception):
    """Base Twitch bridge error."""


class TwitchAuthError(TwitchBridgeError):
    """Authentication error."""


class TwitchConnectionError(TwitchBridgeError):
    """Connection error."""


class TwitchMessageError(TwitchBridgeError):
    """Message error."""


class TwitchReconnectError(TwitchBridgeError):
    """Reconnect error."""


class TwitchIRCBot:
    """Minimal IRC bot for tests."""

    def __init__(
        self,
        server_list: list[tuple[str, int]],
        nickname: str,
        realname: str,
        channel: str,
        on_message: Callable[[dict[str, Any]], Any] | None = None,
        oauth_token: str | None = None,
    ) -> None:
        self.server_list = server_list
        self.nickname = nickname
        self.realname = realname
        self.channel = channel
        self.on_message = on_message
        self.oauth_token = oauth_token
        self.connection = None
        self.bridge_instance: "TwitchChatBridge" | None = None

    def on_pubmsg(self, connection: Any, event: Any) -> None:
        nickname = connection.get_nickname() if connection else None
        if event.source.nick == nickname:
            return
        message_data = {
            "username": event.source.nick,
            "message": event.arguments[0] if event.arguments else "",
            "channel": self.channel,
            "tags": getattr(event, "tags", {}) or {},
        }
        if self.on_message:
            self.on_message(message_data)

    def on_disconnect(self, connection: Any, event: Any) -> None:
        reason = " ".join(getattr(event, "arguments", []) or [])
        if "authentication" in reason.lower() and self.bridge_instance:
            self.bridge_instance.connected = False

    def on_error(self, connection: Any, event: Any) -> None:
        reason = " ".join(getattr(event, "arguments", []) or [])
        if "password" in reason.lower() and self.bridge_instance:
            self.bridge_instance.connected = False

    def on_notice(self, connection: Any, event: Any) -> None:
        reason = " ".join(getattr(event, "arguments", []) or [])
        if "authentication" in reason.lower() and self.bridge_instance:
            self.bridge_instance.connected = False


class TwitchWebSocketBridge:
    """Placeholder for WebSocket bridge."""

    def __init__(self) -> None:
        self.connected = False


class TwitchChatBridge:
    """Lightweight Twitch chat bridge for tests."""

    def __init__(
        self,
        username: str,
        oauth_token: str,
        channel: str,
        on_message: Callable[[dict[str, Any]], Any] | None,
    ) -> None:
        self.username = username
        self.oauth_token = oauth_token
        self.channel = self._normalize_channel(channel)
        self.on_message = on_message
        self.bot: TwitchIRCBot | None = None
        self.running = False
        self.connected = False
        self._has_sent_online_message = False
        self._stop_event = threading.Event()
        self._reconnect_attempt = 0
        self._reconnect_thread: threading.Thread | None = None

    @staticmethod
    def _normalize_channel(channel: str) -> str:
        if not channel:
            return channel
        return channel if channel.startswith("#") else f"#{channel}"

    async def connect(self) -> bool:
        if not self.username:
            raise TwitchConnectionError("Username is required")
        if not self.oauth_token:
            raise TwitchAuthError("OAuth token is required")
        if not self.channel:
            raise TwitchConnectionError("Channel is required")
        if not IRC_AVAILABLE:
            raise TwitchConnectionError("IRC library not available")

        if self.bot is None:
            self.bot = TwitchIRCBot(
                server_list=[("irc.chat.twitch.tv", 6667)],
                nickname=self.username,
                realname=self.username,
                channel=self.channel,
                on_message=self.on_message,
                oauth_token=self.oauth_token,
            )
            self.bot.bridge_instance = self

        self.running = True
        self.connected = True

        def _run():
            return None

        self._reconnect_thread = threading.Thread(target=_run, daemon=True)
        self._reconnect_thread.start()
        return True

    def stop(self) -> None:
        self.running = False
        self.connected = False
        self._stop_event.set()
        if self._reconnect_thread and hasattr(self._reconnect_thread, "join"):
            self._reconnect_thread.join(timeout=1)

    async def send_message(self, message: str | None) -> bool:
        if not message:
            return False
        if len(message) > 500:
            message = message[:500]
        if not self.running or not self.connected:
            return False
        if not self.bot or not getattr(self.bot, "connection", None):
            return False
        try:
            self.bot.connection.privmsg(self.channel, message)
            return True
        except ConnectionError:
            self.connected = False
            return False

    def _handle_message(self, message_data: Any) -> None:
        if not isinstance(message_data, dict):
            return
        if "username" not in message_data or "message" not in message_data:
            return
        if not self.on_message:
            return
        try:
            if asyncio.iscoroutinefunction(self.on_message):
                asyncio.create_task(self.on_message(message_data))
            else:
                self.on_message(message_data)
        except Exception:
            logger.exception("Message callback failed")


__all__ = [
    "TwitchBridgeError",
    "TwitchAuthError",
    "TwitchConnectionError",
    "TwitchMessageError",
    "TwitchReconnectError",
    "TwitchChatBridge",
    "TwitchIRCBot",
    "TwitchWebSocketBridge",
]
