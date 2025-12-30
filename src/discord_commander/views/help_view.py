#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Help GUI View - V2 Compliance Refactor
========================================

Extracted from discord_gui_views.py for V2 compliance.

V2 Compliance:
- File: <400 lines ✅
- Class: <200 lines ✅
- Functions: <30 lines ✅

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
License: MIT
"""

import logging
from src.core.config.timeout_constants import TimeoutConstants

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


class HelpGUIView(discord.ui.View):
    """Interactive help menu with navigation buttons."""

    def __init__(self):
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.current_page = "main"
        self._setup_buttons()

    def _setup_buttons(self):
        """Setup navigation buttons."""
        self.messaging_btn = discord.ui.Button(
            label="Messaging",
            style=discord.ButtonStyle.primary,
            emoji="📨",
            custom_id="help_messaging"
        )
        self.messaging_btn.callback = self.show_messaging
        self.add_item(self.messaging_btn)

        self.swarm_btn = discord.ui.Button(
            label="Swarm",
            style=discord.ButtonStyle.primary,
            emoji="🐝",
            custom_id="help_swarm"
        )
        self.swarm_btn.callback = self.show_swarm
        self.add_item(self.swarm_btn)

        self.github_btn = discord.ui.Button(
            label="GitHub Book",
            style=discord.ButtonStyle.primary,
            emoji="📚",
            custom_id="help_github"
        )
        self.github_btn.callback = self.show_github
        self.add_item(self.github_btn)

        self.gui_btn = discord.ui.Button(
            label="GUI Features",
            style=discord.ButtonStyle.secondary,
            emoji="🎯",
            custom_id="help_gui"
        )
        self.gui_btn.callback = self.show_gui
        self.add_item(self.gui_btn)

        self.back_btn = discord.ui.Button(
            label="Main Menu",
            style=discord.ButtonStyle.secondary,
            emoji="🔙",
            custom_id="help_back"
        )
        self.back_btn.callback = self.show_main
        self.add_item(self.back_btn)

    def _create_main_embed(self) -> discord.Embed:
        """Create main help embed."""
        embed = discord.Embed(
            title="🐝 Discord Commander - Interactive Help",
            description="**Multi-Agent Command & Showcase System**\n\nUse buttons below to navigate help sections:",
            color=0x3498DB,
        )

        embed.add_field(
            name="📋 Quick Navigation",
            value=(
                "📨 **Messaging Commands** - Agent communication\n"
                "🐝 **Swarm Commands** - Task & roadmap features\n"
                "📚 **GitHub Book** - Book viewer commands\n"
                "🎯 **GUI Features** - Interactive interface guide"
            ),
            inline=False,
        )

        embed.add_field(
            name="🚀 Quick Start",
            value=(
                "`!gui` - Open messaging interface\n"
                "`!swarm_tasks` - View task dashboard\n"
                "`!github_book 1` - Read Chapter 1\n"
                "`!help` - Show this menu"
            ),
            inline=False,
        )

        embed.set_footer(
            text="🐝 WE. ARE. SWARM. ⚡ Every agent is the face of the swarm")
        return embed

    def _create_messaging_embed(self) -> discord.Embed:
        """Create messaging commands embed."""
        embed = discord.Embed(
            title="📨 Messaging Commands",
            description="Commands for agent-to-agent communication",
            color=0x3498DB,
        )

        embed.add_field(
            name="Interactive Commands",
            value=(
                "`!gui` - Open interactive messaging GUI\n"
                "• Agent selection dropdown\n"
                "• Message composition modal\n"
                "• Priority selection"
            ),
            inline=False,
        )

        embed.add_field(
            name="Text Commands",
            value=(
                "`!message <agent> <msg>` - Send direct message\n"
                "`!broadcast <msg>` - Broadcast to all agents\n"
                "`!agents` - List all 8 agents"
            ),
            inline=False,
        )

        embed.add_field(
            name="Admin Commands",
            value=(
                "`!shutdown` - Gracefully shutdown bot\n"
                "`!restart` - Restart bot\n"
                "`!git_push \"message\"` - Push changes to GitHub\n"
                "`!push \"message\"` - Alias for git_push"
            ),
            inline=False,
        )

        embed.add_field(
            name="Examples",
            value=(
                "`!message Agent-1 Check your inbox`\n"
                "`!broadcast All agents: Task complete!`\n"
                "`!gui` - Opens dropdown interface"
            ),
            inline=False,
        )

        embed.set_footer(text="Use 🔙 Main Menu to return")
        return embed

    def _create_swarm_embed(self) -> discord.Embed:
        """Create swarm commands embed."""
        embed = discord.Embed(
            title="🐝 Swarm Showcase Commands",
            description="Live task dashboard and strategic roadmap",
            color=0x3498DB,
        )

        embed.add_field(
            name="Task & Roadmap",
            value=(
                "`!swarm_tasks` (or `!tasks`, `!directives`) - Live task dashboard\n"
                "`!swarm_roadmap` (or `!roadmap`, `!plan`) - Strategic roadmap\n"
                "`!swarm_overview` (or `!status`, `!swarm`) - Complete status"
            ),
            inline=False,
        )

        embed.add_field(
            name="Quality & Compliance",
            value=(
                "`!swarm_excellence` (or `!lean`, `!quality`) - V2 compliance status\n"
                "Shows code quality metrics and compliance tracking"
            ),
            inline=False,
        )

        embed.add_field(
            name="Examples",
            value=(
                "`!swarm_tasks` - See all agent missions\n"
                "`!roadmap` - View strategic plan\n"
                "`!status` - Complete swarm overview"
            ),
            inline=False,
        )

        embed.set_footer(text="Use 🔙 Main Menu to return")
        return embed

    def _create_github_embed(self) -> discord.Embed:
        """Create GitHub book commands embed."""
        embed = discord.Embed(
            title="📚 GitHub Book Viewer",
            description="Interactive book navigation with chapters",
            color=0x3498DB,
        )

        embed.add_field(
            name="Book Commands",
            value=(
                "`!github_book [chapter]` - View specific chapter\n"
                "• Interactive navigation buttons\n"
                "• Chapter-by-chapter reading\n"
                "• Previous/Next navigation"
            ),
            inline=False,
        )

        embed.add_field(
            name="Discovery Commands",
            value=(
                "`!goldmines` - High-value pattern discoveries\n"
                "`!book_stats` - Comprehensive book statistics"
            ),
            inline=False,
        )

        embed.add_field(
            name="Examples",
            value=(
                "`!github_book 1` - Read Chapter 1\n"
                "`!github_book` - Start from beginning\n"
                "`!goldmines` - Find high-ROI patterns"
            ),
            inline=False,
        )

        embed.set_footer(text="Use 🔙 Main Menu to return")
        return embed

    def _create_gui_embed(self) -> discord.Embed:
        """Create GUI features embed."""
        embed = discord.Embed(
            title="🎯 GUI Features Guide",
            description="Interactive interface features and usage",
            color=0x3498DB,
        )

        embed.add_field(
            name="Main Messaging GUI (`!gui`)",
            value=(
                "🎯 **Agent Selection** - Dropdown menu for all 8 agents\n"
                "📝 **Message Modal** - Compose messages with priority\n"
                "📢 **Broadcast Button** - Message all agents\n"
                "📊 **Status Button** - View swarm status\n"
                "🔄 **Refresh Button** - Reload agent list"
            ),
            inline=False,
        )

        embed.add_field(
            name="Message Composition Tips",
            value=(
                "• **Shift+Enter** for line breaks ✨\n"
                "• Priority: `regular` or `urgent`\n"
                "• Up to 2000 characters per message\n"
                "• Instant delivery on submit"
            ),
            inline=False,
        )

        embed.add_field(
            name="Status Dashboard",
            value=(
                "• Real-time agent status\n"
                "• Points and mission tracking\n"
                "• Auto-refresh capabilities\n"
                "• Interactive refresh button"
            ),
            inline=False,
        )

        embed.set_footer(text="Use 🔙 Main Menu to return")
        return embed

    async def show_main(self, interaction: discord.Interaction):
        """Show main help menu."""
        try:
            embed = self._create_main_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            self.current_page = "main"
        except Exception as e:
            logger.error(f"Error showing main help: {e}", exc_info=True)
            await self._handle_error(interaction, e)

    async def show_messaging(self, interaction: discord.Interaction):
        """Show messaging commands."""
        try:
            embed = self._create_messaging_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            self.current_page = "messaging"
        except Exception as e:
            logger.error(f"Error showing messaging help: {e}", exc_info=True)
            await self._handle_error(interaction, e)

    async def show_swarm(self, interaction: discord.Interaction):
        """Show swarm commands."""
        try:
            embed = self._create_swarm_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            self.current_page = "swarm"
        except Exception as e:
            logger.error(f"Error showing swarm help: {e}", exc_info=True)
            await self._handle_error(interaction, e)

    async def show_github(self, interaction: discord.Interaction):
        """Show GitHub book commands."""
        try:
            embed = self._create_github_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            self.current_page = "github"
        except Exception as e:
            logger.error(f"Error showing GitHub help: {e}", exc_info=True)
            await self._handle_error(interaction, e)

    async def show_gui(self, interaction: discord.Interaction):
        """Show GUI features."""
        try:
            embed = self._create_gui_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            self.current_page = "gui"
        except Exception as e:
            logger.error(f"Error showing GUI help: {e}", exc_info=True)
            await self._handle_error(interaction, e)

    async def _handle_error(self, interaction: discord.Interaction, error: Exception):
        """Handle interaction errors."""
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {error}", ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"❌ Error: {error}", ephemeral=True
                )
        except Exception as followup_error:
            logger.error(
                f"Error sending error message: {followup_error}", exc_info=True)

