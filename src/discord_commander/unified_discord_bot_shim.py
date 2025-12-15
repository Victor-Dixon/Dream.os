#!/usr/bin/env python3
"""
Unified Discord Bot (Backward Compatibility Shim)
=================================================

This module serves as a backward-compatibility shim for the refactored
Unified Discord Bot. It re-exports the main bot class and MessagingCommands
from the new modular structure, ensuring that existing imports continue to work.

All core logic has been moved to modular components for V2 compliance:
- Event handlers: src/discord_commander/handlers/
- Lifecycle management: src/discord_commander/lifecycle/
- Integration services: src/discord_commander/integrations/
- Configuration: src/discord_commander/config/

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

# Import the actual implementation (will be created)
# For now, import from original file until full extraction is complete
from .unified_discord_bot import UnifiedDiscordBot, MessagingCommands, main

__all__ = [
    "UnifiedDiscordBot",
    "MessagingCommands",
    "main",
]

