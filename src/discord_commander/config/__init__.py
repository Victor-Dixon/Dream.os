"""

Bot Configuration
=================

Configuration management for Discord bot.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14

<!-- SSOT Domain: discord -->

SSOT TOOL METADATA
Purpose: Package initialization for Discord bot configuration
Description: Exports BotConfig class and utility functions for Discord configuration management
Usage: import discord_commander.config
Date: 2025-12-30
Tags: discord, config, initialization
"""

from .bot_config import BotConfig, load_discord_user_map, get_developer_prefix

__all__ = [
    "BotConfig",
    "load_discord_user_map",
    "get_developer_prefix",
]

