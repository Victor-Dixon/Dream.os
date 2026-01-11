"""
Systems Inventory Commands V2 - Agent Cellphone V2
=================================================

SSOT Domain: discord

Refactored Discord systems inventory commands using service architecture.

Features:
- Complete systems inventory display
- Tools and services listing
- Inventory statistics and summaries
- Formatted Discord embeds

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Optional

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

from .inventory_service import inventory_service

logger = logging.getLogger(__name__)

class SystemsInventoryCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Discord commands for viewing systems inventory.
    """

    def __init__(self, bot):
        self.bot = bot
        self.inventory_service = inventory_service

    @commands.command(name="systems_inventory", aliases=["inventory", "sys_inv", "what_do_we_have"])
    async def show_systems_inventory(self, ctx: commands.Context):
        """
        Display complete systems inventory with statistics.

        Usage: !systems_inventory

        Shows:
        - Complete systems list with status
        - Inventory statistics
        - Tools and services overview
        """
        try:
            # Get inventory stats
            stats = self.inventory_service.get_inventory_stats()

            embed = discord.Embed(
                title="🏗️ Systems Inventory - Complete Overview",
                description="**Agent Cellphone V2 - Complete Systems Inventory**",
                color=discord.Color.blue()
            )

            # Statistics fields
            embed.add_field(
                name="📊 Statistics",
                value=f"**Systems:** {stats['total_systems']} ({stats['active_systems']} active)\n"
                      f"**Tools:** {stats['total_tools']}\n"
                      f"**Services:** {stats['total_services']} ({stats['active_services']} running)",
                inline=True
            )

            embed.add_field(
                name="📅 Version Info",
                value=f"**Version:** {stats['version']}\n"
                      f"**Updated:** {stats['last_updated'][:10] if stats['last_updated'] else 'Unknown'}",
                inline=True
            )

            # Systems overview
            systems_overview = self.inventory_service.format_systems_overview()
            if len(systems_overview) > 1024:
                systems_overview = systems_overview[:1020] + "..."

            embed.add_field(
                name="🏗️ Systems Overview",
                value=systems_overview or "No systems found",
                inline=False
            )

            # Quick actions
            embed.add_field(
                name="🔍 Quick Access",
                value="• `!systems_list` - Detailed systems list\n"
                      "• `!tools_list` - All tools\n"
                      "• `!services_list` - All services",
                inline=False
            )

            embed.set_footer(text=f"Requested by {ctx.author.display_name} | Use specific commands for detailed views")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error showing systems inventory: {e}")
            embed = discord.Embed(
                title="❌ Error Loading Inventory",
                description=f"Failed to load systems inventory: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="systems_list", aliases=["systems", "list_systems"])
    async def list_systems(self, ctx: commands.Context):
        """
        List all systems with detailed descriptions.

        Usage: !systems_list

        Shows each system with its description, category, and status.
        """
        try:
            systems = self.inventory_service.get_systems_list()

            if not systems:
                embed = discord.Embed(
                    title="📋 Systems List",
                    description="No systems found in inventory",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title=f"📋 Systems List ({len(systems)} systems)",
                description="Detailed list of all systems in the inventory",
                color=discord.Color.green()
            )

            # Group systems by category for better organization
            categories = {}
            for system in systems:
                category = system.get("category", "Uncategorized")
                if category not in categories:
                    categories[category] = []
                categories[category].append(system)

            # Add fields for each category
            for category, systems_list in categories.items():
                field_value = ""
                for system in systems_list[:5]:  # Limit per category
                    status_emoji = "🟢" if system["status"] == "active" else "🟡" if system["status"] == "maintenance" else "🔴"
                    field_value += f"{status_emoji} **{system['name']}**\n"
                    field_value += f"└ {system['description'][:80]}{'...' if len(system['description']) > 80 else ''}\n\n"

                if field_value:
                    if len(field_value) > 1024:
                        field_value = field_value[:1020] + "..."
                    embed.add_field(
                        name=f"📁 {category} ({len(systems_list)})",
                        value=field_value,
                        inline=False
                    )

            embed.set_footer(text=f"Total: {len(systems)} systems | Use !systems_inventory for overview")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error listing systems: {e}")
            await ctx.send(f"❌ Error listing systems: {e}")

    @commands.command(name="tools_list", aliases=["tools", "list_tools"])
    async def list_tools(self, ctx: commands.Context, limit: int = 20):
        """
        List all available tools.

        Usage: !tools_list [limit]

        Args:
            limit: Maximum number of tools to show (default: 20)

        Examples:
            !tools_list
            !tools_list 50
        """
        try:
            # Validate limit
            if limit < 1 or limit > 100:
                limit = 20

            tools_list = self.inventory_service.format_tools_list(limit)

            embed = discord.Embed(
                title=f"🛠️ Tools Inventory ({len(self.inventory_service.get_tools_list()) if limit >= len(self.inventory_service.get_tools_list()) else f'{limit}+'})",
                description="List of all available tools and utilities",
                color=discord.Color.purple()
            )

            # Split into chunks if too long for Discord
            if len(tools_list) > 4000:
                chunks = [tools_list[i:i+4000] for i in range(0, len(tools_list), 4000)]
                embed.add_field(
                    name="🛠️ Tools (Part 1)",
                    value=chunks[0],
                    inline=False
                )
                for i, chunk in enumerate(chunks[1:], 2):
                    embed.add_field(
                        name=f"🛠️ Tools (Part {i})",
                        value=chunk,
                        inline=False
                    )
            else:
                embed.add_field(
                    name="🛠️ Available Tools",
                    value=tools_list or "No tools found in inventory",
                    inline=False
                )

            embed.set_footer(text=f"Showing up to {limit} tools | Use higher limit to see more")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            await ctx.send(f"❌ Error listing tools: {e}")

    @commands.command(name="services_list", aliases=["services", "list_services"])
    async def list_services(self, ctx: commands.Context):
        """
        List all available services with their status.

        Usage: !services_list

        Shows all services with their current status and descriptions.
        """
        try:
            services_list = self.inventory_service.format_services_list()

            embed = discord.Embed(
                title=f"⚙️ Services Inventory ({len(self.inventory_service.get_services_list())} services)",
                description="List of all available services and their status",
                color=discord.Color.teal()
            )

            if len(services_list) > 4000:
                # Split into chunks
                chunks = [services_list[i:i+4000] for i in range(0, len(services_list), 4000)]
                for i, chunk in enumerate(chunks, 1):
                    embed.add_field(
                        name=f"⚙️ Services (Part {i})",
                        value=chunk,
                        inline=False
                    )
            else:
                embed.add_field(
                    name="⚙️ Available Services",
                    value=services_list or "No services found in inventory",
                    inline=False
                )

            embed.set_footer(text=f"Requested by {ctx.author.display_name} | Status indicators: 🟢 Running, 🟡 Stopped, 🔴 Error")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error listing services: {e}")
            await ctx.send(f"❌ Error listing services: {e}")

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(SystemsInventoryCommands(bot))