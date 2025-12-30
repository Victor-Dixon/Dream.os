#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Bump Agent View - Agent Selection for Bumping
============================================

Interactive view for selecting agents to bump (click chat input + shift+backspace).

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-11-30
"""

import logging
from pathlib import Path
import sys
from src.core.config.timeout_constants import TimeoutConstants

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)


class BumpAgentView(discord.ui.View):
    """View for selecting agents to bump."""
    
    def __init__(self):
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.selected_agents = []
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup agent selection buttons."""
        # Create buttons for each agent (1-8)
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            # Determine row (4 buttons per row)
            row = (i - 1) // 4
            
            btn = discord.ui.Button(
                label=f"Agent-{i}",
                style=discord.ButtonStyle.secondary,
                emoji="👆",
                custom_id=f"bump_agent_{i}",
                row=row,
            )
            btn.callback = self._create_agent_callback(i)
            self.add_item(btn)
        
        # Add action buttons at the bottom
        self.bump_selected_btn = discord.ui.Button(
            label="Bump Selected",
            style=discord.ButtonStyle.primary,
            emoji="✅",
            custom_id="bump_selected",
            row=2,
        )
        self.bump_selected_btn.callback = self.bump_selected
        self.add_item(self.bump_selected_btn)
        
        self.bump_all_btn = discord.ui.Button(
            label="Bump All",
            style=discord.ButtonStyle.success,
            emoji="🚀",
            custom_id="bump_all",
            row=2,
        )
        self.bump_all_btn.callback = self.bump_all
        self.add_item(self.bump_all_btn)
        
        self.clear_btn = discord.ui.Button(
            label="Clear Selection",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️",
            custom_id="bump_clear",
            row=2,
        )
        self.clear_btn.callback = self.clear_selection
        self.add_item(self.clear_btn)
    
    def _create_agent_callback(self, agent_num: int):
        """Create callback for agent button."""
        async def callback(interaction: discord.Interaction):
            agent_id = f"Agent-{agent_num}"
            if agent_num in self.selected_agents:
                self.selected_agents.remove(agent_num)
                status = "❌ Removed"
            else:
                self.selected_agents.append(agent_num)
                status = "✅ Added"
            
            # Update button style to show selection
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.custom_id == f"bump_agent_{agent_num}":
                    if agent_num in self.selected_agents:
                        item.style = discord.ButtonStyle.success
                    else:
                        item.style = discord.ButtonStyle.secondary
                    break
            
            # Update embed to show current selection
            embed = self._create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        
        return callback
    
    async def bump_selected(self, interaction: discord.Interaction):
        """Bump selected agents."""
        if not self.selected_agents:
            await interaction.response.send_message(
                "❌ No agents selected. Please select agents to bump.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        # Import and call bump function
        try:
            from tools.agent_bump_script import bump_agents_by_number
            
            results = bump_agents_by_number(self.selected_agents)
            
            # Create result embed
            success_count = sum(1 for r in results.values() if r)
            total_count = len(results)
            
            if success_count == total_count:
                color = discord.Color.green()
                title = f"✅ Successfully Bumped {success_count} Agent(s)"
            elif success_count > 0:
                color = discord.Color.orange()
                title = f"⚠️ Partially Successful: {success_count}/{total_count}"
            else:
                color = discord.Color.red()
                title = f"❌ Failed to Bump Agents"
            
            embed = discord.Embed(
                title=title,
                description=f"Bumped {success_count}/{total_count} agent(s)",
                color=color,
            )
            
            # Add results for each agent
            for agent_id, success in results.items():
                status = "✅" if success else "❌"
                embed.add_field(
                    name=f"{status} {agent_id}",
                    value="Success" if success else "Failed",
                    inline=True,
                )
            
            embed.set_footer(text="Agent Bump Script | Click + Shift+Backspace")
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error bumping agents: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Error bumping agents: {str(e)}",
                ephemeral=True
            )
    
    async def bump_all(self, interaction: discord.Interaction):
        """Bump all agents (1-8)."""
        await interaction.response.defer()
        
        try:
            from tools.agent_bump_script import bump_agents_by_number
            
            all_agents = list(range(1, 9))
            results = bump_agents_by_number(all_agents)
            
            # Create result embed
            success_count = sum(1 for r in results.values() if r)
            total_count = len(results)
            
            if success_count == total_count:
                color = discord.Color.green()
                title = f"✅ Successfully Bumped All {success_count} Agents"
            elif success_count > 0:
                color = discord.Color.orange()
                title = f"⚠️ Partially Successful: {success_count}/{total_count}"
            else:
                color = discord.Color.red()
                title = f"❌ Failed to Bump Agents"
            
            embed = discord.Embed(
                title=title,
                description=f"Bumped {success_count}/{total_count} agent(s)",
                color=color,
            )
            
            # Add results for each agent
            for agent_id, success in results.items():
                status = "✅" if success else "❌"
                embed.add_field(
                    name=f"{status} {agent_id}",
                    value="Success" if success else "Failed",
                    inline=True,
                )
            
            embed.set_footer(text="Agent Bump Script | Click + Shift+Backspace")
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error bumping all agents: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Error bumping agents: {str(e)}",
                ephemeral=True
            )
    
    async def clear_selection(self, interaction: discord.Interaction):
        """Clear agent selection."""
        self.selected_agents = []
        
        # Reset all button styles
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.custom_id and item.custom_id.startswith("bump_agent_"):
                item.style = discord.ButtonStyle.secondary
        
        embed = self._create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    def _create_embed(self) -> discord.Embed:
        """Create embed showing current selection."""
        embed = discord.Embed(
            title="👆 Bump Agents",
            description="Select agents to bump (click chat input + shift+backspace)",
            color=discord.Color.blue(),
        )
        
        if self.selected_agents:
            selected_list = ", ".join([f"Agent-{n}" for n in sorted(self.selected_agents)])
            embed.add_field(
                name="Selected Agents",
                value=selected_list,
                inline=False,
            )
        else:
            embed.add_field(
                name="Selected Agents",
                value="None selected",
                inline=False,
            )
        
        embed.add_field(
            name="Instructions",
            value=(
                "1. Click agent buttons to select/deselect\n"
                "2. Click 'Bump Selected' to bump chosen agents\n"
                "3. Click 'Bump All' to bump all 8 agents\n"
                "4. Click 'Clear Selection' to reset"
            ),
            inline=False,
        )
        
        embed.set_footer(text="Agent Bump Script | Click + Shift+Backspace")
        
        return embed

