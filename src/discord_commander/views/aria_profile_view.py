#!/usr/bin/env python3
"""
Aria Profile View - Interactive Profile Controller
==================================================

Interactive Discord view for !aria command - showcases Aria's profile
with beautiful buttons and embeds to impress!

<!-- SSOT Domain: web -->

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import logging
from typing import Optional
from src.core.config.timeout_constants import TimeoutConstants

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


class AriaProfileView(discord.ui.View):
    """Interactive profile view for Aria with multiple sections."""
    
    def __init__(self):
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.current_section = "main"
    
    @discord.ui.button(
        label="About Me",
        style=discord.ButtonStyle.primary,
        emoji="👋",
        row=0
    )
    async def about_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show about section."""
        embed = discord.Embed(
            title="👋 About Aria",
            description="**Hey there! I'm Aria!** ✨",
            color=0xFF69B4  # Hot pink
        )
        embed.add_field(
            name="Who I Am",
            value="I'm a creative developer and gamer who loves building cool things! 🎮✨",
            inline=False
        )
        embed.add_field(
            name="My Interests",
            value="🎮 Gaming • 💻 Coding • 🎨 Design • 🚀 Innovation",
            inline=False
        )
        embed.add_field(
            name="My Mission",
            value="Building awesome projects and having fun while doing it! 🌟",
            inline=False
        )
        embed.set_footer(text="Use the buttons below to explore more!")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="My Projects",
        style=discord.ButtonStyle.primary,
        emoji="🚀",
        row=0
    )
    async def projects_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show projects section."""
        embed = discord.Embed(
            title="🚀 Aria's Projects",
            description="Check out what I've been building!",
            color=0x00D9FF  # Cyan
        )
        embed.add_field(
            name="🎮 AriaJet Theme",
            value="Custom WordPress theme for gaming content and posts",
            inline=False
        )
        embed.add_field(
            name="🤖 Agent Swarm",
            value="Working with the swarm to build amazing things!",
            inline=False
        )
        embed.add_field(
            name="💻 Development",
            value="Always learning and building something new!",
            inline=False
        )
        embed.set_footer(text="More projects coming soon! 🎉")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="Skills",
        style=discord.ButtonStyle.primary,
        emoji="💪",
        row=0
    )
    async def skills_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show skills section."""
        embed = discord.Embed(
            title="💪 Aria's Skills",
            description="What I'm good at!",
            color=0xFFD700  # Gold
        )
        embed.add_field(
            name="🎨 Design",
            value="UI/UX Design • Graphics • Creative Direction",
            inline=False
        )
        embed.add_field(
            name="💻 Development",
            value="Web Development • WordPress • Python • JavaScript",
            inline=False
        )
        embed.add_field(
            name="🎮 Gaming",
            value="Game Development • Game Design • Community Building",
            inline=False
        )
        embed.add_field(
            name="🚀 Innovation",
            value="Always exploring new technologies and ideas!",
            inline=False
        )
        embed.set_footer(text="Always learning and growing! 🌱")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="Fun Facts",
        style=discord.ButtonStyle.secondary,
        emoji="🎉",
        row=1
    )
    async def fun_facts_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show fun facts section."""
        embed = discord.Embed(
            title="🎉 Fun Facts About Aria",
            description="Get to know me better!",
            color=0xFF1493  # Deep pink
        )
        embed.add_field(
            name="🌟 Favorite Things",
            value="• Love building interactive experiences\n• Passionate about gaming\n• Always up for a coding challenge\n• Creative problem solver",
            inline=False
        )
        embed.add_field(
            name="💡 Current Focus",
            value="Building awesome Discord bots and web experiences!",
            inline=False
        )
        embed.add_field(
            name="🎯 Goals",
            value="Keep learning, keep building, keep having fun!",
            inline=False
        )
        embed.set_footer(text="Thanks for checking me out! 💖")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="Contact",
        style=discord.ButtonStyle.secondary,
        emoji="📬",
        row=1
    )
    async def contact_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show contact section."""
        embed = discord.Embed(
            title="📬 Get in Touch",
            description="Ways to connect with Aria!",
            color=0x9370DB  # Medium purple
        )
        embed.add_field(
            name="💬 Discord",
            value="You're already here! Just ping me! 👋",
            inline=False
        )
        embed.add_field(
            name="🌐 Projects",
            value="Check out my work in the swarm!",
            inline=False
        )
        embed.add_field(
            name="🤝 Collaboration",
            value="Always open to working on cool projects together!",
            inline=False
        )
        embed.set_footer(text="Let's build something amazing! 🚀")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="💬 Message Agent-8",
        style=discord.ButtonStyle.primary,
        emoji="🤖",
        row=2
    )
    async def message_agent8_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open modal to message Agent-8 with preferences."""
        try:
            from .aria_message_agent8_modal import AriaMessageAgent8Modal
            
            modal = AriaMessageAgent8Modal()
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening Agent-8 message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error opening message form: {e}",
                    ephemeral=True
                )
    
    @discord.ui.button(
        label="✨ Special: Aria's Secret",
        style=discord.ButtonStyle.success,
        emoji="🎁",
        row=2
    )
    async def special_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Special personalized button for Aria!"""
        embed = discord.Embed(
            title="🎁 Aria's Special Secret!",
            description="**You found the special button!** ✨",
            color=0xFF1493  # Deep pink
        )
        embed.add_field(
            name="🌟 You're Awesome!",
            value=(
                "Aria, you're doing amazing things!\n\n"
                "• Building the AriaJet theme 🚀\n"
                "• Creating cool projects 💻\n"
                "• Being creative and innovative ✨\n"
                "• Making your dad proud! 👨‍👧\n\n"
                "**Keep being awesome!** 💖"
            ),
            inline=False
        )
        embed.add_field(
            name="🎮 Fun Surprise",
            value="This button was made especially for you by the swarm! 🐝",
            inline=False
        )
        embed.add_field(
            name="💡 Pro Tip",
            value="Try clicking the other buttons to explore more about you!",
            inline=False
        )
        embed.set_footer(text="Made with ❤️ by Dad & the Swarm • You're amazing! 🌟")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="Back to Main",
        style=discord.ButtonStyle.secondary,
        emoji="🏠",
        row=2
    )
    async def main_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to main profile."""
        embed = self._create_main_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    def _create_main_embed(self) -> discord.Embed:
        """Create the main profile embed."""
        embed = discord.Embed(
            title="✨ Aria's Profile ✨",
            description="**Welcome to my profile!** 👋\n\nUse the buttons below to explore different sections!",
            color=0xFF69B4  # Hot pink
        )
        embed.set_thumbnail(url="https://i.imgur.com/placeholder.png")  # Add Aria's avatar URL if available
        embed.add_field(
            name="👋 About",
            value="Creative developer, gamer, and builder of cool things!",
            inline=True
        )
        embed.add_field(
            name="🚀 Status",
            value="Active & Building!",
            inline=True
        )
        embed.add_field(
            name="💖 Fun Fact",
            value="I love making interactive experiences!",
            inline=True
        )
        embed.set_footer(text="Click the buttons to explore more! • Made with ❤️ by Dad & the Swarm • Try the 'Message Agent-8' button! 💬")
        
        return embed


async def create_aria_profile_command(interaction: discord.Interaction):
    """Create and send the Aria profile view."""
    view = AriaProfileView()
    embed = view._create_main_embed()
    
    await interaction.response.send_message(embed=embed, view=view)


# Command registration (to be added to bot)
async def setup_aria_command(bot: commands.Bot):
    """Register the !aria command."""
    @bot.tree.command(name="aria", description="View Aria's interactive profile!")
    async def aria_command(interaction: discord.Interaction):
        """!aria command handler."""
        try:
            await create_aria_profile_command(interaction)
        except Exception as e:
            logger.error(f"Error in !aria command: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Oops! Something went wrong: {e}",
                    ephemeral=True
                )

