#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

<<<<<<< HEAD
<<<<<<< HEAD
Twitch Chat Bridge - Main Entry Point
======================================

Main entry point for Twitch chat integration.
Imports and re-exports modular components for backward compatibility.

V2 Compliance: <50 lines, modular architecture
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

# Import modular components
from .twitch_exceptions import (
    TwitchBridgeError,
    TwitchAuthError,
    TwitchConnectionError,
    TwitchMessageError,
    TwitchReconnectError
)

from .twitch_chat_bridge import TwitchChatBridge
from .twitch_irc_bot import TwitchIRCBot
from .twitch_websocket_bridge import TwitchWebSocketBridge

# Re-export for backward compatibility
__all__ = [
=======
Twitch Chat Bridge
==================
=======
Twitch Chat Bridge - Main Entry Point
======================================
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

Main entry point for Twitch chat integration.
Imports and re-exports modular components for backward compatibility.

V2 Compliance: <50 lines, modular architecture
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

# Import modular components
from .twitch_exceptions import (
    TwitchBridgeError,
    TwitchAuthError,
    TwitchConnectionError,
    TwitchMessageError,
    TwitchReconnectError
)

from .twitch_chat_bridge import TwitchChatBridge
from .twitch_irc_bot import TwitchIRCBot
from .twitch_websocket_bridge import TwitchWebSocketBridge

# Re-export for backward compatibility
__all__ = [
<<<<<<< HEAD
    "TwitchChatBridge",
    "TwitchIRCBot",
    "TwitchWebSocketBridge",
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    "TwitchBridgeError",
    "TwitchAuthError",
    "TwitchConnectionError",
    "TwitchMessageError",
    "TwitchReconnectError",
<<<<<<< HEAD
<<<<<<< HEAD
    "TwitchChatBridge",
    "TwitchIRCBot",
    "TwitchWebSocketBridge"
]
=======
]
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    "TwitchChatBridge",
    "TwitchIRCBot",
    "TwitchWebSocketBridge"
]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
