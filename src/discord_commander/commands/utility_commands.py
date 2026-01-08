#!/usr/bin/env python3
"""
Utility Commands - Modular V2 Compliance
========================================

Utility commands (mermaid, help, commands) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular utility commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class UtilityCommands(commands.Cog):
    """Utility commands for various bot functions."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize utility commands."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Render Mermaid diagram code."""
        try:
            diagram_code = self._clean_mermaid_code(diagram_code)
            embed = discord.Embed(
                title="📊 Mermaid Diagram",
                description="Mermaid diagram code:",
                color=discord.Color.blue(),
            )
            mermaid_block = f"```mermaid\n{diagram_code}\n```"

            if len(mermaid_block) > 1900:
                await ctx.send("❌ Mermaid diagram too long. Please shorten it.")
                return

            embed.add_field(name="Diagram Code", value=mermaid_block, inline=False)
            embed.set_footer(text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering")
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error rendering mermaid: {e}")
            await ctx.send(f"❌ Error rendering mermaid diagram: {e}")

    def _clean_mermaid_code(self, diagram_code: str) -> str:
        """Clean mermaid code block markers."""
        diagram_code = diagram_code.strip()
        if diagram_code.startswith("```mermaid"):
            diagram_code = diagram_code[10:]
        elif diagram_code.startswith("```"):
            diagram_code = diagram_code[3:]
        if diagram_code.endswith("```"):
            diagram_code = diagram_code[:-3]
        return diagram_code.strip()

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Show interactive help menu with navigation buttons."""
        try:
            from src.discord_commander.views import HelpGUIView
            view = HelpGUIView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="commands", description="List all registered commands")
    async def list_commands(self, ctx: commands.Context):
        """List all registered bot commands - redirects to Control Panel button view."""
        try:
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="📋 All Commands - Use Control Panel Buttons!",
                description=(
                    "**🎯 All commands are accessible via buttons in the Control Panel!**\n\n"
                    "**Click the buttons below to access all features:**\n"
                    "• **Tasks** button = `!swarm_tasks`\n"
                    "• **Swarm Status** button = `!status`\n"
                    "• **GitHub Book** button = `!github_book`\n"
                    "• **Roadmap** button = `!swarm_roadmap`\n"
                    "• **Excellence** button = `!swarm_excellence`\n"
                    "• **Overview** button = `!swarm_overview`\n"
                    "• **Goldmines** button = `!goldmines`\n"
                    "• **Templates** button = `!templates`\n"
                    "• **Mermaid** button = `!mermaid`\n"
                    "• **Monitor** button = `!monitor`\n"
                    "• **Help** button = `!help`\n"
                    "• **All Commands** button = This view\n\n"
                    "**No need to type commands - just click buttons!**"
                ),
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="💡 Quick Access",
                value="Type `!control` (or `!panel`, `!menu`) to open Control Panel anytime!",
                inline=False,
            )
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!")
            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await ctx.send(f"❌ Error: {e}")


__all__ = ["UtilityCommands"]