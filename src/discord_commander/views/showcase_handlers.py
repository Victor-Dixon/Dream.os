#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Showcase Handlers - Helper functions for showcase button callbacks
==================================================================

Helper functions for swarm showcase commands (roadmap, excellence, overview, goldmines).

V2 Compliance:
- File: <400 lines ✅
- Functions: <30 lines ✅

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import logging

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


async def show_roadmap_handler(interaction: discord.Interaction) -> discord.Embed:
    """Show swarm roadmap embed."""
    try:
        from ..swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(bot=None)
        return await showcase._create_roadmap_embed()
    except Exception as e:
        logger.error(f"Error creating roadmap embed: {e}", exc_info=True)
        raise


async def show_excellence_handler(interaction: discord.Interaction) -> discord.Embed:
    """Show swarm excellence embed."""
    try:
        from ..swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(bot=None)
        return await showcase._create_excellence_embed()
    except Exception as e:
        logger.error(f"Error creating excellence embed: {e}", exc_info=True)
        raise


async def show_overview_handler(interaction: discord.Interaction) -> discord.Embed:
    """Show swarm overview embed."""
    try:
        from ..swarm_showcase_commands import SwarmShowcaseCommands
        
        showcase = SwarmShowcaseCommands(bot=None)
        return await showcase._create_overview_embed()
    except Exception as e:
        logger.error(f"Error creating overview embed: {e}", exc_info=True)
        raise


async def show_goldmines_handler(interaction: discord.Interaction) -> tuple[discord.Embed, discord.ui.View]:
    """Show goldmines embed and navigator view."""
    try:
        from ..github_book_viewer import GitHubBookData, GitHubBookNavigator
        
        book_data = GitHubBookData()
        navigator = GitHubBookNavigator(book_data)
        embed = navigator._create_goldmines_embed()
        
        return embed, navigator
    except Exception as e:
        logger.error(f"Error creating goldmines embed: {e}", exc_info=True)
        raise

