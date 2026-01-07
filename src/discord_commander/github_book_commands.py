"""
GitHub Book Commands - Agent Cellphone V2
=========================================

SSOT Domain: git

Discord commands for GitHub repository analysis book display.

Features:
- Interactive book navigation
- Chapter-based repository browsing
- Goldmine discovery showcase
- Search and filtering capabilities

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Any, Optional

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

from .github_book_data import GitHubBookData
from .discord_ui_components import (
    BaseNavigationView, EmbedFormatter, ModalHandler,
    PreviousButton, NextButton, JumpButton, SearchButton,
    BackButton, GoldmineButton
)

logger = logging.getLogger(__name__)

class GitHubBookNavigationView(BaseNavigationView):
    """Navigation view for GitHub book display."""

    def __init__(self, cog, chapter_data: dict, current_page: int = 1):
        self.cog = cog
        self.chapter_data = chapter_data
        self.repositories = chapter_data.get("repositories", [])
        self.total_pages = len(self.repositories)

        super().__init__(current_page=current_page, total_pages=self.total_pages)

        # Add goldmine button if available
        if cog.data_loader.get_processed_data().get("navigation", {}).get("has_goldmines"):
            self.add_item(GoldmineButton())

    async def _update_display(self, interaction: discord.Interaction):
        """Update the repository display."""
        if self.current_page <= len(self.repositories):
            repo = self.repositories[self.current_page - 1]
            embed = EmbedFormatter.create_base_embed(
                title=f"{self.chapter_data['title']} - Page {self.current_page}",
                description=f"Repository {self.current_page} of {self.total_pages}"
            )
            EmbedFormatter.add_repository_info(embed, repo)

            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("Invalid page!", ephemeral=True)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_navigation(interaction, -1)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_navigation(interaction, 1)

    @discord.ui.button(label="Jump", style=discord.ButtonStyle.secondary, emoji="🔢")
    async def jump_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ModalHandler.show_jump_modal(
            interaction,
            self.total_pages,
            self._handle_jump
        )

    @discord.ui.button(label="Search", style=discord.ButtonStyle.success, emoji="🔍")
    async def search_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ModalHandler.show_search_modal(
            interaction,
            self._handle_search
        )

    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, emoji="🏠")
    async def back_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.show_book_menu(interaction)

    @discord.ui.button(label="Goldmines", style=discord.ButtonStyle.success, emoji="💎")
    async def goldmine_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.show_goldmines(interaction)

    async def _handle_jump(self, interaction: discord.Interaction, page_num: int):
        """Handle jump to specific page."""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            self._update_buttons()
            await self._update_display(interaction)
        else:
            await interaction.response.send_message(
                f"Page number must be between 1 and {self.total_pages}!",
                ephemeral=True
            )

    async def _handle_search(self, interaction: discord.Interaction, query: str):
        """Handle repository search."""
        results = self.cog.data_loader.search_repositories(query)

        if not results:
            await interaction.response.send_message(
                f"No repositories found matching '{query}'",
                ephemeral=True
            )
            return

        # Show search results
        embed = EmbedFormatter.create_base_embed(
            title=f"🔍 Search Results for '{query}'",
            description=f"Found {len(results)} repositories"
        )

        for i, result in enumerate(results[:5]):  # Show first 5 results
            repo = result["repository"]
            name = repo.get("name", "Unknown")
            stars = repo.get("stars", 0)
            embed.add_field(
                name=f"{i+1}. {name}",
                value=f"⭐ {stars} stars | Chapter {result['chapter']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

class GitHubBookCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Discord commands for GitHub book display and navigation.
    """

    def __init__(self, bot):
        self.bot = bot
        self.data_loader = GitHubBookData()

    @commands.command(name="github_book", aliases=["book", "gb"])
    async def github_book(self, ctx):
        """Display the GitHub analysis book with interactive navigation."""
        await self.show_book_menu(ctx)

    async def show_book_menu(self, ctx_or_interaction):
        """Show the main book menu."""
        data = self.data_loader.get_processed_data()
        navigation = data.get("navigation", {})
        metadata = data.get("metadata", {})

        embed = EmbedFormatter.create_base_embed(
            title="📖 GitHub Analysis Book",
            description="Interactive repository analysis and discovery showcase"
        )

        embed.add_field(
            name="📊 Analysis Summary",
            value=f"**{metadata.get('total_repos', 0)}** repositories analyzed",
            inline=True
        )

        embed.add_field(
            name="📚 Chapters",
            value=str(navigation.get('total_chapters', 0)),
            inline=True
        )

        embed.add_field(
            name="💎 Goldmines",
            value=str(len(data.get('goldmines', []))),
            inline=True
        )

        embed.add_field(
            name="🎯 Navigation",
            value="Use buttons below to explore chapters and discoveries",
            inline=False
        )

        # Create menu view
        view = BookMenuView(self)
        await ctx_or_interaction.response.send_message(embed=embed, view=view)

    async def show_chapter(self, ctx_or_interaction, chapter_number: int):
        """Show a specific chapter."""
        chapter_data = self.data_loader.get_chapter_data(chapter_number)

        if not chapter_data:
            await ctx_or_interaction.response.send_message(
                f"Chapter {chapter_number} not found!",
                ephemeral=True
            )
            return

        # Show first repository in chapter
        view = GitHubBookNavigationView(self, chapter_data, current_page=1)

        embed = EmbedFormatter.create_base_embed(
            title=chapter_data['title'],
            description=f"Chapter {chapter_number} - {chapter_data['category']}"
        )

        repositories = chapter_data.get("repositories", [])
        if repositories:
            repo = repositories[0]
            EmbedFormatter.add_repository_info(embed, repo)

        await ctx_or_interaction.response.send_message(embed=embed, view=view)

    async def show_goldmines(self, ctx_or_interaction):
        """Show goldmine discoveries."""
        data = self.data_loader.get_processed_data()
        goldmines = data.get("goldmines", [])

        if not goldmines:
            await ctx_or_interaction.response.send_message(
                "No goldmine discoveries found!",
                ephemeral=True
            )
            return

        # Show first goldmine
        view = GoldmineNavigationView(self, goldmines, current_page=1)
        embed = EmbedFormatter.create_goldmine_embed(goldmines[0], 0, len(goldmines))

        await ctx_or_interaction.response.send_message(embed=embed, view=view)

class BookMenuView(discord.ui.View if DISCORD_AVAILABLE else object):
    """Main book menu navigation."""

    def __init__(self, cog):
        super().__init__(timeout=300.0)
        self.cog = cog

    @discord.ui.button(label="Chapter 1", style=discord.ButtonStyle.primary, emoji="1️⃣")
    async def chapter_1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.show_chapter(interaction, 1)

    @discord.ui.button(label="Goldmines", style=discord.ButtonStyle.success, emoji="💎")
    async def goldmines_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.show_goldmines(interaction)

    @discord.ui.button(label="Summary", style=discord.ButtonStyle.secondary, emoji="📊")
    async def summary_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.show_summary(interaction)

class GoldmineNavigationView(BaseNavigationView):
    """Navigation view for goldmine discoveries."""

    def __init__(self, cog, goldmines: list, current_page: int = 1):
        self.cog = cog
        self.goldmines = goldmines
        super().__init__(current_page=current_page, total_pages=len(goldmines))

    async def _update_display(self, interaction: discord.Interaction):
        """Update the goldmine display."""
        if self.current_page <= len(self.goldmines):
            goldmine = self.goldmines[self.current_page - 1]
            embed = EmbedFormatter.create_goldmine_embed(
                goldmine, self.current_page - 1, len(self.goldmines)
            )
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("Invalid goldmine!", ephemeral=True)

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(GitHubBookCommands(bot))