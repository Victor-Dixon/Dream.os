#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Twitch Bridge Exceptions
========================

Exception classes for Twitch bridge operations.

V2 Compliant: Modular exception handling
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

class TwitchBridgeError(Exception):
    """Base exception for Twitch bridge errors."""
    pass


class TwitchAuthError(TwitchBridgeError):
    """Authentication-related errors."""
    pass


class TwitchConnectionError(TwitchBridgeError):
    """Connection-related errors."""
    pass


class TwitchMessageError(TwitchBridgeError):
    """Message handling errors."""
    pass


class TwitchReconnectError(TwitchBridgeError):
    """Reconnection-related errors."""
    pass


class TwitchConfigError(TwitchBridgeError):
    """Configuration-related errors."""
    pass


__all__ = [
    "TwitchBridgeError",
    "TwitchAuthError",
    "TwitchConnectionError",
    "TwitchMessageError",
    "TwitchReconnectError",
    "TwitchConfigError"
]