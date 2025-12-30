#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Systems Inventory Discord Commands
==================================

Discord commands for viewing the complete systems inventory:
- !systems_inventory - View complete systems inventory
- !systems_list - List all systems with descriptions
- !tools_list - List all tools
- !services_list - List all services

Author: Agent-4 (Captain)
Date: 2025-12-06
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Any, List, Dict

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class SystemsInventoryCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Discord commands for viewing systems inventory.
    
    Commands:
    - !systems_inventory - Complete systems inventory view
    - !systems_list - List all systems with descriptions
    - !tools_list - List all tools
    - !services_list - List all services
    """

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.inventory = None
        self._load_inventory()

    def _load_inventory(self):
        """Load systems inventory."""
        try:
            from tools.swarm_system_inventory import SwarmSystemInventory
            
            inventory = SwarmSystemInventory()
            inventory.scan_all_tools()
            inventory.scan_all_systems()
            inventory.scan_all_services()
            inventory.scan_all_agents()
            inventory.scan_integrations()
            
            self.inventory = inventory
            self.logger.info("✅ Systems inventory loaded")
        except Exception as e:
            self.logger.error(f"Error loading inventory: {e}")
            self.inventory = None

    @commands.command(name="systems_inventory", aliases=["inventory", "sys_inv", "what_do_we_have"])
    async def show_systems_inventory(self, ctx: commands.Context):
        """Display complete systems inventory with all systems, tools, services."""
        try:
            if not self.inventory:
                self._load_inventory()
            
            if not self.inventory:
                await ctx.send("❌ Error loading systems inventory")
                return

            embed = discord.Embed(
                title="🐝 SWARM SYSTEMS INVENTORY",
                description="**Complete catalog of all systems, tools, and services**",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            # Summary
            embed.add_field(
                name="📊 Summary",
                value=(
                    f"**Tools**: {len(self.inventory.tools)}\n"
                    f"**Systems**: {len(self.inventory.systems)}\n"
                    f"**Services**: {len(self.inventory.services)}\n"
                    f"**Agents**: {len(self.inventory.agents)}\n"
                    f"**Integrations**: {len(self.inventory.integrations)}"
                ),
                inline=False
            )

            # Systems with descriptions
            systems_text = self._format_systems()
            if systems_text:
                from src.discord_commander.utils.message_chunking import chunk_field_value
                chunks = chunk_field_value(systems_text)
                embed.add_field(
                    name="⚙️ Systems",
                    value=chunks[0],
                    inline=False
                )
                # Add additional chunks if needed
                for i, chunk in enumerate(chunks[1:], 2):
                    embed.add_field(
                        name=f"⚙️ Systems (continued {i}/{len(chunks)})",
                        value=chunk,
                        inline=False
                    )

            embed.set_footer(text="💡 Use !systems_list for detailed system descriptions")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error showing systems inventory: {e}", exc_info=True)
            await ctx.send(f"❌ Error displaying systems inventory: {e}")

    @commands.command(name="systems_list", aliases=["systems", "list_systems"])
    async def list_systems(self, ctx: commands.Context):
        """List all systems with detailed descriptions."""
        try:
            if not self.inventory:
                self._load_inventory()
            
            if not self.inventory:
                await ctx.send("❌ Error loading systems inventory")
                return

            systems = self.inventory.systems
            
            if not systems:
                await ctx.send("❌ No systems found")
                return

            embed = discord.Embed(
                title="⚙️ SWARM SYSTEMS - Detailed List",
                description=f"**{len(systems)} systems cataloged**",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )

            # Format each system with description
            for system in systems[:10]:  # Show first 10
                system_name = system.get("name", system.get("id", "Unknown"))
                system_path = system.get("path", "N/A")
                
                # Get description from README if available
                description = self._get_system_description(system)
                
                embed.add_field(
                    name=f"🔧 {system_name}",
                    value=(
                        f"**Path**: `{system_path}`\n"
                        f"**Description**: {description}\n"
                        f"**Type**: {system.get('type', 'system')}"
                    ),
                    inline=False
                )

            if len(systems) > 10:
                embed.set_footer(text=f"Showing 10 of {len(systems)} systems. Use !systems_inventory for full list.")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error listing systems: {e}", exc_info=True)
            await ctx.send(f"❌ Error listing systems: {e}")

    def _format_systems(self) -> str:
        """Format systems list for display."""
        if not self.inventory or not self.inventory.systems:
            return "No systems found"
        
        systems_text = []
        for system in self.inventory.systems[:5]:  # Show top 5 in summary
            name = system.get("name", system.get("id", "Unknown"))
            systems_text.append(f"• **{name}**")
        
        if len(self.inventory.systems) > 5:
            systems_text.append(f"... and {len(self.inventory.systems) - 5} more")
        
        return "\n".join(systems_text) if systems_text else "No systems found"

    def _get_system_description(self, system: Dict[str, Any]) -> str:
        """Get system description from README or default."""
        system_path = Path(system.get("path", ""))
        if not system_path.exists():
            # Try to get from system dict
            return system.get("description", "No description available")
        
        # Check for README.md
        readme_path = system_path / "README.md"
        if readme_path.exists():
            try:
                readme_content = readme_path.read_text(encoding="utf-8")
                # Extract first paragraph or objective section
                lines = readme_content.split("\n")
                
                # Look for OBJECTIVE or PURPOSE section
                for i, line in enumerate(lines):
                    if "OBJECTIVE" in line.upper() or "PURPOSE" in line.upper():
                        # Get next few lines
                        desc_lines = []
                        for j in range(i + 1, min(i + 5, len(lines))):
                            if lines[j].strip() and not lines[j].startswith("#"):
                                desc_lines.append(lines[j].strip())
                        if desc_lines:
                            desc = " ".join(desc_lines[:3])  # First 3 lines
                            return desc[:200] if len(desc) > 200 else desc
                
                # Fallback: first non-empty line after title
                for line in lines[5:15]:
                    if line.strip() and not line.startswith("#") and len(line.strip()) > 20:
                        return line.strip()[:200]  # First 200 chars
                
                # Last fallback: use first line if available
                if lines and len(lines[0].strip()) > 10:
                    return lines[0].strip()[:200]
            except Exception as e:
                self.logger.debug(f"Error reading README: {e}")
        
        # Try to get from system dict
        return system.get("description", "System description not available")

    @commands.command(name="tools_list", aliases=["tools", "list_tools"])
    async def list_tools(self, ctx: commands.Context, limit: int = 20):
        """List all tools (limit: 1-50, default: 20)."""
        try:
            if not self.inventory:
                self._load_inventory()
            
            if not self.inventory:
                await ctx.send("❌ Error loading systems inventory")
                return

            tools = self.inventory.tools[:min(limit, 50)]
            
            embed = discord.Embed(
                title="🛠️ SWARM TOOLS",
                description=f"**{len(self.inventory.tools)} total tools** (showing {len(tools)})",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow(),
            )

            # Group tools by category or show top tools
            tools_text = []
            for tool in tools:
                name = tool.get("name", tool.get("id", "Unknown"))
                desc = tool.get("description", "No description")[:100]
                tools_text.append(f"• **{name}**: {desc}")

            from src.discord_commander.utils.message_chunking import chunk_field_value
            tools_content = "\n".join(tools_text)
            chunks = chunk_field_value(tools_content)
            
            embed.add_field(
                name="Tools",
                value=chunks[0],
                inline=False
            )

            if len(chunks) > 1:
                for i, chunk in enumerate(chunks[1:], 2):
                    embed.add_field(
                        name=f"Tools (continued {i}/{len(chunks)})",
                        value=chunk,
                        inline=False
                    )

            if len(self.inventory.tools) > limit:
                embed.set_footer(text=f"Showing {limit} of {len(self.inventory.tools)} tools. Use !tools_list <number> to see more.")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error listing tools: {e}", exc_info=True)
            await ctx.send(f"❌ Error listing tools: {e}")

    @commands.command(name="services_list", aliases=["services", "list_services"])
    async def list_services(self, ctx: commands.Context):
        """List all services."""
        try:
            if not self.inventory:
                self._load_inventory()
            
            if not self.inventory:
                await ctx.send("❌ Error loading systems inventory")
                return

            services = self.inventory.services[:20]  # Show first 20
            
            embed = discord.Embed(
                title="🔧 SWARM SERVICES",
                description=f"**{len(self.inventory.services)} total services** (showing {len(services)})",
                color=discord.Color.purple(),
                timestamp=discord.utils.utcnow(),
            )

            services_text = []
            for service in services:
                name = service.get("name", service.get("id", "Unknown"))
                services_text.append(f"• **{name}**")

            from src.discord_commander.utils.message_chunking import chunk_field_value
            services_content = "\n".join(services_text)
            chunks = chunk_field_value(services_content)
            
            embed.add_field(
                name="Services",
                value=chunks[0],
                inline=False
            )

            if len(chunks) > 1:
                for i, chunk in enumerate(chunks[1:], 2):
                    embed.add_field(
                        name=f"Services (continued {i}/{len(chunks)})",
                        value=chunk,
                        inline=False
                    )

            if len(self.inventory.services) > 20:
                embed.set_footer(text=f"Showing 20 of {len(self.inventory.services)} services.")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error listing services: {e}", exc_info=True)
            await ctx.send(f"❌ Error listing services: {e}")


def setup(bot):
    """Setup function for discord.py cog loading."""
    if DISCORD_AVAILABLE:
        bot.add_cog(SystemsInventoryCommands(bot))
        logger.info("✅ Systems Inventory commands loaded")
    else:
        logger.warning("⚠️ Discord not available - SystemsInventoryCommands not loaded")

