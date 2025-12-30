"""
<!-- SSOT Domain: discord -->

Tools Commands - Discord Bot Commands for Toolbelt
==================================================

Discord commands to view and interact with the toolbelt registry.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-06
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

from tools.toolbelt_registry import TOOLS_REGISTRY, ToolRegistry


if DISCORD_AVAILABLE:
    class ToolsCommands(commands.Cog):
        """Discord commands for viewing toolbelt tools."""
        
        def __init__(self, bot):
            """Initialize tools commands."""
            self.bot = bot
            self.registry = ToolRegistry()
        
        @commands.command(name="tools", aliases=["toolbelt", "list-tools"])
        async def list_tools(self, ctx: commands.Context, category: str = None):
            """
            List all tools in the toolbelt registry.
            
            Usage:
            !tools - List all tools
            !tools unified - List only unified tools
            !tools github - List tools matching 'github'
            """
            try:
                all_tools = self.registry.list_tools()
                
                # Filter by category if provided
                if category:
                    category_lower = category.lower()
                    all_tools = [
                        tool for tool in all_tools
                        if category_lower in tool["id"].lower() or 
                           category_lower in tool["name"].lower() or
                           any(category_lower in flag.lower() for flag in tool.get("flags", []))
                    ]
                
                if not all_tools:
                    await ctx.send(f"❌ No tools found matching '{category}'")
                    return
                
                # Group tools for pagination (Discord has 2000 char limit)
                tools_per_page = 10
                total_pages = (len(all_tools) + tools_per_page - 1) // tools_per_page
                
                for page_num in range(total_pages):
                    start_idx = page_num * tools_per_page
                    end_idx = min(start_idx + tools_per_page, len(all_tools))
                    page_tools = all_tools[start_idx:end_idx]
                    
                    embed = discord.Embed(
                        title=f"🔧 Toolbelt Tools" + (f" - {category}" if category else ""),
                        description=f"Page {page_num + 1}/{total_pages} ({len(all_tools)} total tools)",
                        color=discord.Color.blue()
                    )
                    
                    for tool in page_tools:
                        tool_id = tool["id"]
                        name = tool["name"]
                        description = tool.get("description", "No description")
                        flags = ", ".join(tool.get("flags", [])[:3])  # First 3 flags
                        if len(tool.get("flags", [])) > 3:
                            flags += f" (+{len(tool.get('flags', [])) - 3} more)"
                        
                        # Truncate description if too long
                        if len(description) > 100:
                            description = description[:97] + "..."
                        
                        embed.add_field(
                            name=f"`{tool_id}` - {name}",
                            value=f"{description}\n**Flags:** `{flags}`",
                            inline=False
                        )
                    
                    if page_num == 0:
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f"❌ Error listing tools: {str(e)}")
        
        @commands.command(name="tool", aliases=["tool-info", "tool-details"])
        async def tool_details(self, ctx: commands.Context, tool_id: str = None):
            """
            Get detailed information about a specific tool.
            
            Usage:
            !tool unified-captain - Get details for unified-captain
            !tool --scan - Get details for tool with --scan flag
            """
            try:
                if not tool_id:
                    await ctx.send("❌ Please specify a tool ID or flag. Use `!tools` to list all tools.")
                    return
                
                # Try to find tool by ID or flag
                tool_config = None
                found_tool_id = None
                
                # First try by tool ID
                if tool_id in TOOLS_REGISTRY:
                    tool_config = TOOLS_REGISTRY[tool_id]
                    found_tool_id = tool_id
                else:
                    # Try by flag
                    tool_config = self.registry.get_tool_for_flag(tool_id)
                    if tool_config:
                        # Find the tool ID for this config
                        for tid, config in TOOLS_REGISTRY.items():
                            if config == tool_config:
                                found_tool_id = tid
                                break
                
                if not tool_config:
                    # Try partial match
                    matching_tools = [
                        (tid, config) for tid, config in TOOLS_REGISTRY.items()
                        if tool_id.lower() in tid.lower() or
                           tool_id.lower() in config.get("name", "").lower()
                    ]
                    
                    if len(matching_tools) == 1:
                        found_tool_id, tool_config = matching_tools[0]
                    elif len(matching_tools) > 1:
                        # Show matches
                        matches = "\n".join([f"`{tid}`" for tid, _ in matching_tools[:10]])
                        await ctx.send(
                            f"❌ Multiple tools match '{tool_id}':\n{matches}\n\n"
                            f"Use `!tool <exact-id>` to get details."
                        )
                        return
                    else:
                        await ctx.send(f"❌ Tool '{tool_id}' not found. Use `!tools` to list all tools.")
                        return
                
                # Create detailed embed
                embed = discord.Embed(
                    title=f"🔧 {tool_config.get('name', 'Unknown Tool')}",
                    description=tool_config.get("description", "No description available"),
                    color=discord.Color.green()
                )
                
                # Add tool ID
                embed.add_field(name="Tool ID", value=f"`{found_tool_id}`", inline=True)
                
                # Add module
                embed.add_field(name="Module", value=f"`{tool_config.get('module', 'N/A')}`", inline=True)
                
                # Add main function
                embed.add_field(name="Main Function", value=f"`{tool_config.get('main_function', 'main')}`", inline=True)
                
                # Add flags
                flags = tool_config.get("flags", [])
                if flags:
                    flags_str = "\n".join([f"`{flag}`" for flag in flags])
                    embed.add_field(name="Flags", value=flags_str, inline=False)
                
                # Add args passthrough
                args_passthrough = tool_config.get("args_passthrough", True)
                embed.add_field(name="Args Passthrough", value="✅ Yes" if args_passthrough else "❌ No", inline=True)
                
                # Add usage example
                if flags:
                    primary_flag = flags[0]
                    embed.add_field(
                        name="Usage Example",
                        value=f"```bash\npython -m tools.toolbelt {primary_flag} [args]\n```",
                        inline=False
                    )
                
                await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f"❌ Error getting tool details: {str(e)}")
        
        @commands.command(name="unified-tools", aliases=["unified", "consolidated-tools"])
        async def unified_tools(self, ctx: commands.Context):
            """List all unified tools (consolidated tools)."""
            try:
                unified_tools = [
                    tool for tool in self.registry.list_tools()
                    if "unified" in tool["id"].lower()
                ]
                
                if not unified_tools:
                    await ctx.send("❌ No unified tools found")
                    return
                
                embed = discord.Embed(
                    title="🔧 Unified Tools (Consolidated)",
                    description=f"{len(unified_tools)} unified tools consolidating multiple individual tools",
                    color=discord.Color.purple()
                )
                
                for tool in unified_tools:
                    tool_id = tool["id"]
                    name = tool["name"]
                    description = tool.get("description", "No description")
                    flags = ", ".join(tool.get("flags", [])[:2])
                    
                    # Extract consolidation info from description
                    if "consolidates" in description.lower():
                        # Try to extract number
                        import re
                        match = re.search(r'consolidates?\s+(\d+)\+?', description, re.IGNORECASE)
                        if match:
                            count = match.group(1)
                            description = f"Consolidates {count}+ tools"
                    
                    embed.add_field(
                        name=f"`{tool_id}` - {name}",
                        value=f"{description}\n**Flags:** `{flags}`",
                        inline=False
                    )
                
                await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f"❌ Error listing unified tools: {str(e)}")


async def setup(bot):
    """Setup function for discord.py cog loading."""
    if DISCORD_AVAILABLE:
        await bot.add_cog(ToolsCommands(bot))
    else:
        # Return None if Discord not available (cog won't load)
        pass
