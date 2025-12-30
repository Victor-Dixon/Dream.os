"""
<!-- SSOT Domain: discord -->

Discord Event Handlers
======================

Event handlers for Discord bot events (on_ready, on_message, etc.).

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from .discord_event_handlers import (
    DiscordEventHandlers,
    handle_on_ready,
    handle_on_message,
    handle_on_disconnect,
    handle_on_resume,
    handle_on_socket_raw_receive,
    handle_on_error,
)

__all__ = [
    "DiscordEventHandlers",
    "handle_on_ready",
    "handle_on_message",
    "handle_on_disconnect",
    "handle_on_resume",
    "handle_on_socket_raw_receive",
    "handle_on_error",
]

