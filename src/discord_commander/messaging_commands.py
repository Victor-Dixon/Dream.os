#!/usr/bin/env python3
"""
Messaging Commands (Compatibility Shim)
=======================================

<!-- SSOT Domain: discord -->

Provides backward-compatible import path for MessagingCommands.
"""

from .messaging_commands_v2 import MessagingCommands

__all__ = ["MessagingCommands"]
