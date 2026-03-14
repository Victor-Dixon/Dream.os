#!/usr/bin/env python3
"""
Discord GUI Modals Base
=======================

<!-- SSOT Domain: discord -->
"""

from __future__ import annotations

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:  # pragma: no cover - handled in tests via mocks
    DISCORD_AVAILABLE = False
    discord = None


class BaseModal(discord.ui.Modal if DISCORD_AVAILABLE else object):
    """Base modal providing shared initialization."""

    def __init__(self, title: str, timeout: float = 300.0, custom_id: str | None = None):
        if DISCORD_AVAILABLE:
            super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        else:
            self.title = title
            self.timeout = timeout
            self.custom_id = custom_id


__all__ = ["BaseModal"]
