"""
Discord UI Components - Agent Cellphone V2
==========================================

SSOT Domain: discord

Shared Discord UI components for navigation, embeds, and interactive elements.

Features:
- Navigation button classes
- Embed formatting utilities
- Modal and view components
- Consistent styling and branding

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Any, Optional, Dict, List

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

logger = logging.getLogger(__name__)

class NavigationButton(discord.ui.Button if DISCORD_AVAILABLE else object):
    """Base navigation button class."""

    def __init__(self, label: str, style: discord.ButtonStyle = discord.ButtonStyle.primary,
                 emoji: Optional[str] = None, **kwargs):
        super().__init__(label=label, style=style, emoji=emoji, **kwargs)

class PreviousButton(NavigationButton):
    """Previous page/chapter button."""

    def __init__(self):
        super().__init__(label="Previous", style=discord.ButtonStyle.secondary, emoji="⬅️")

class NextButton(NavigationButton):
    """Next page/chapter button."""

    def __init__(self):
        super().__init__(label="Next", style=discord.ButtonStyle.primary, emoji="➡️")

class JumpButton(NavigationButton):
    """Jump to specific page/chapter button."""

    def __init__(self):
        super().__init__(label="Jump", style=discord.ButtonStyle.secondary, emoji="🔢")

class SearchButton(NavigationButton):
    """Search/filter button."""

    def __init__(self):
        super().__init__(label="Search", style=discord.ButtonStyle.success, emoji="🔍")

class BackButton(NavigationButton):
    """Back to main menu button."""

    def __init__(self):
        super().__init__(label="Back", style=discord.ButtonStyle.danger, emoji="🏠")

class GoldmineButton(NavigationButton):
    """Goldmine discoveries button."""

    def __init__(self):
        super().__init__(label="Goldmines", style=discord.ButtonStyle.success, emoji="💎")

class BaseNavigationView(discord.ui.View if DISCORD_AVAILABLE else object):
    """Base class for navigation views with common functionality."""

    def __init__(self, current_page: int = 1, total_pages: int = 1, timeout: float = 300.0):
        super().__init__(timeout=timeout)
        self.current_page = current_page
        self.total_pages = total_pages
        self._update_buttons()

    def _update_buttons(self):
        """Update button states based on current page."""
        self.clear_items()

        # Add navigation buttons
        prev_btn = PreviousButton()
        prev_btn.disabled = self.current_page <= 1
        self.add_item(prev_btn)

        next_btn = NextButton()
        next_btn.disabled = self.current_page >= self.total_pages
        self.add_item(next_btn)

        # Add utility buttons
        self.add_item(JumpButton())
        self.add_item(SearchButton())
        self.add_item(BackButton())

    async def _handle_navigation(self, interaction: discord.Interaction, direction: int):
        """Handle navigation button clicks."""
        new_page = self.current_page + direction
        if 1 <= new_page <= self.total_pages:
            self.current_page = new_page
            self._update_buttons()
            await self._update_display(interaction)
        else:
            await interaction.response.send_message("Invalid page number!", ephemeral=True)

    async def _update_display(self, interaction: discord.Interaction):
        """Update the display after navigation. Override in subclasses."""
        await interaction.response.edit_message(view=self)

class EmbedFormatter:
    """Utility class for formatting Discord embeds consistently."""

    @staticmethod
    def create_base_embed(title: str, description: str = "", color: int = 0x3498db) -> discord.Embed:
        """Create a base embed with consistent styling."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Agent Cellphone V2", icon_url=None)
        return embed

    @staticmethod
    def add_field(embed: discord.Embed, name: str, value: str, inline: bool = False):
        """Add a field to an embed with length validation."""
        if len(value) > 1024:
            value = value[:1021] + "..."
        embed.add_field(name=name, value=value, inline=inline)

    @staticmethod
    def add_repository_info(embed: discord.Embed, repo_data: Dict[str, Any]):
        """Add repository information to an embed."""
        name = repo_data.get("name", "Unknown")
        description = repo_data.get("description", "No description available")
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        language = repo_data.get("language", "Unknown")

        embed.add_field(name="Repository", value=f"**{name}**", inline=False)
        embed.add_field(name="Description", value=description[:500] + "..." if len(description) > 500 else description, inline=False)
        embed.add_field(name="⭐ Stars", value=str(stars), inline=True)
        embed.add_field(name="🍴 Forks", value=str(forks), inline=True)
        embed.add_field(name="💻 Language", value=language, inline=True)

        # Add URL if available
        if "url" in repo_data:
            embed.add_field(name="🔗 Link", value=repo_data["url"], inline=False)

    @staticmethod
    def create_navigation_embed(current_page: int, total_pages: int, title: str,
                              description: str = "") -> discord.Embed:
        """Create an embed with navigation information."""
        embed = EmbedFormatter.create_base_embed(
            title=f"{title} (Page {current_page}/{total_pages})",
            description=description
        )

        # Add navigation info
        nav_info = f"Use the buttons below to navigate between pages."
        if total_pages > 1:
            nav_info += f"\n\n**Current:** Page {current_page} of {total_pages}"

        embed.add_field(name="📖 Navigation", value=nav_info, inline=False)
        return embed

    @staticmethod
    def create_goldmine_embed(goldmine_data: Dict[str, Any], index: int,
                            total: int) -> discord.Embed:
        """Create an embed for goldmine discoveries."""
        title = goldmine_data.get("title", "Goldmine Discovery")
        description = goldmine_data.get("description", "")
        category = goldmine_data.get("category", "General")
        priority = goldmine_data.get("priority", "Medium")

        # Color based on priority
        color_map = {
            "High": 0xe74c3c,    # Red
            "Medium": 0xf39c12,  # Orange
            "Low": 0x27ae60      # Green
        }
        color = color_map.get(priority, 0x3498db)

        embed = EmbedFormatter.create_base_embed(
            title=f"💎 {title} ({index + 1}/{total})",
            description=description,
            color=color
        )

        embed.add_field(name="🏷️ Category", value=category, inline=True)
        embed.add_field(name="⚡ Priority", value=priority, inline=True)

        if "repository" in goldmine_data:
            embed.add_field(name="📁 Repository", value=goldmine_data["repository"], inline=False)

        return embed

class ModalHandler:
    """Utility class for handling Discord modals."""

    @staticmethod
    async def show_jump_modal(interaction: discord.Interaction, max_pages: int,
                            callback_function):
        """Show a modal for jumping to a specific page."""

        class JumpModal(discord.ui.Modal if DISCORD_AVAILABLE else object):
            page_input = discord.ui.TextInput(
                label="Page Number",
                placeholder=f"Enter page number (1-{max_pages})",
                required=True,
                min_length=1,
                max_length=len(str(max_pages))
            )

            def __init__(self):
                super().__init__(title=f"Jump to Page (1-{max_pages})")

            async def on_submit(self, interaction: discord.Interaction):
<<<<<<< HEAD
                """Handle page jump submission and validation.

                Args:
                    interaction: The Discord interaction event.
                """
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                try:
                    page_num = int(self.page_input.value)
                    if 1 <= page_num <= max_pages:
                        await callback_function(interaction, page_num)
                    else:
                        await interaction.response.send_message(
                            f"Page number must be between 1 and {max_pages}!",
                            ephemeral=True
                        )
                except ValueError:
                    await interaction.response.send_message(
                        "Please enter a valid page number!",
                        ephemeral=True
                    )

        modal = JumpModal()
        await interaction.response.send_modal(modal)

    @staticmethod
    async def show_search_modal(interaction: discord.Interaction, callback_function):
        """Show a modal for search input."""

        class SearchModal(discord.ui.Modal if DISCORD_AVAILABLE else object):
            search_input = discord.ui.TextInput(
                label="Search Query",
                placeholder="Enter search terms...",
                required=True,
                max_length=100
            )

            def __init__(self):
                super().__init__(title="Search Repositories")

            async def on_submit(self, interaction: discord.Interaction):
<<<<<<< HEAD
                """Handle repository search submission and processing.

                Args:
                    interaction: The Discord interaction event.
                """
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
                query = self.search_input.value.strip()
                if query:
                    await callback_function(interaction, query)
                else:
                    await interaction.response.send_message(
                        "Please enter a search query!",
                        ephemeral=True
                    )

        modal = SearchModal()
        await interaction.response.send_modal(modal)

# Export key classes for easy importing
__all__ = [
    "NavigationButton",
    "PreviousButton",
    "NextButton",
    "JumpButton",
    "SearchButton",
    "BackButton",
    "GoldmineButton",
    "BaseNavigationView",
    "EmbedFormatter",
    "ModalHandler"
]