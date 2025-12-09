#!/usr/bin/env python3
"""
Carmyn Profile View - Interactive Profile Controller
=====================================================

Interactive Discord view for !carmyn command - showcases Carmyn's profile
with beautiful buttons and embeds, matching Aria's style!

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


class CarmynProfileView(discord.ui.View):
    """Interactive profile view for Carmyn with multiple sections."""
    
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
            title="👋 About Carmyn",
            description="**Hey there! I'm Carmyn!** ✨",
            color=0xFF69B4  # Hot pink
        )
        embed.add_field(
            name="Who I Am",
            value="Featured DJ specializing in **R&B**, **Dance**, and **Jazz** music! 🎵\nStill learning and growing as an artist - always improving! 🎶",
            inline=False
        )
        embed.add_field(
            name="My Music",
            value="🎵 R&B • 💃 Dance • 🎷 Jazz",
            inline=False
        )
        embed.add_field(
            name="My Mission",
            value="Creating amazing music and sharing it with the world! 🌟",
            inline=False
        )
        embed.set_footer(text="Use the buttons below to explore more!")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="My Music",
        style=discord.ButtonStyle.primary,
        emoji="🎵",
        row=0
    )
    async def music_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show music section."""
        embed = discord.Embed(
            title="🎵 Carmyn's Music",
            description="Check out my music specializations!",
            color=0x9370DB  # Medium purple
        )
        embed.add_field(
            name="🎵 R&B",
            value="Smooth vibes and soulful beats that make you feel the groove",
            inline=False
        )
        embed.add_field(
            name="💃 Dance",
            value="Get the party moving with energetic dance tracks!",
            inline=False
        )
        embed.add_field(
            name="🎷 Jazz",
            value="Classic and contemporary jazz that soothes the soul",
            inline=False
        )
        embed.set_footer(text="More music coming soon! 🎉")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label="My Website",
        style=discord.ButtonStyle.primary,
        emoji="🌐",
        row=0
    )
    async def website_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show website section."""
        embed = discord.Embed(
            title="🌐 Carmyn's Website",
            description="Connect with me online!",
            color=0x00D9FF  # Cyan
        )
        embed.add_field(
            name="🌟 Prism Blossom",
            value="[Visit my website](https://prismblossom.online/carmyn)\n\nCheck out my music, mixes, and updates!",
            inline=False
        )
        embed.add_field(
            name="🌐 SouthWest Secret",
            value="[Visit the site](https://prismblossom.online)\n\nMore amazing content coming soon!",
            inline=False
        )
        embed.add_field(
            name="📱 Status",
            value="🟢 Active & Creating",
            inline=False
        )
        embed.set_footer(text="Check back soon for new mixes and updates! 🎶")
        
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
            title="🎉 Fun Facts About Carmyn",
            description="Get to know me better!",
            color=0xFF1493  # Deep pink
        )
        embed.add_field(
            name="🌟 Quick Facts",
            value=(
                "🎤 **Role:** Featured DJ\n"
                "🌟 **Status:** Rising Star\n"
                "📈 **Growth:** Always Learning!\n"
                "💖 **Vibe:** Positive & Creative"
            ),
            inline=False
        )
        embed.add_field(
            name="💡 Current Focus",
            value="Creating amazing mixes and growing as an artist!",
            inline=False
        )
        embed.add_field(
            name="🎯 Goals",
            value="Keep creating, keep learning, keep sharing the music!",
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
            description="Ways to connect with Carmyn!",
            color=0xFFD700  # Gold
        )
        embed.add_field(
            name="💬 Discord",
            value="You're already here! Just ping me! 👋",
            inline=False
        )
        embed.add_field(
            name="🌐 Website",
            value="Visit [prismblossom.online/carmyn](https://prismblossom.online/carmyn) for updates!",
            inline=False
        )
        embed.add_field(
            name="🤝 Collaboration",
            value="Always open to working on music projects together!",
            inline=False
        )
        embed.set_footer(text="Let's create something amazing! 🎶")
        
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
            from .carmyn_message_agent8_modal import CarmynMessageAgent8Modal
            
            modal = CarmynMessageAgent8Modal()
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening Agent-8 message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error opening message form: {e}",
                    ephemeral=True
                )
    
    @discord.ui.button(
        label="✨ Special: Carmyn's Secret",
        style=discord.ButtonStyle.success,
        emoji="🎁",
        row=2
    )
    async def special_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Special personalized button for Carmyn!"""
        embed = discord.Embed(
            title="🎁 Carmyn's Special Secret!",
            description="**You found the special button!** ✨",
            color=0xFF1493  # Deep pink
        )
        embed.add_field(
            name="🌟 You're Awesome!",
            value=(
                "Carmyn, you're doing amazing things!\n\n"
                "• Creating incredible music 🎵\n"
                "• Growing as an artist 🎤\n"
                "• Sharing your talent with the world 🌟\n"
                "• Making everyone proud! 👨‍👧\n\n"
                "**Keep being awesome!** 💖"
            ),
            inline=False
        )
        embed.add_field(
            name="🎵 Music Surprise",
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
            title="🌟 CARMYN 🌟",
            description="**Featured DJ • Music Artist • Rising Star**\n\n*Welcome to Carmyn's space!*\n\nUse the buttons below to explore different sections!",
            color=0xFF69B4  # Hot pink - matching her website theme
        )
        embed.set_thumbnail(url="https://prismblossom.online/wp-content/uploads/2024/12/carmyn-profile.png")
        embed.add_field(
            name="🎵 About",
            value="DJ specializing in R&B, Dance, and Jazz!",
            inline=True
        )
        embed.add_field(
            name="🌟 Status",
            value="Active & Creating!",
            inline=True
        )
        embed.add_field(
            name="💖 Fun Fact",
            value="I love making people dance!",
            inline=True
        )
        embed.set_footer(text="Click the buttons to explore more! • Made with ❤️ by Dad & the Swarm • Try the 'Message Agent-8' button! 💬")
        
        return embed


async def create_carmyn_profile_command(interaction: discord.Interaction):
    """Create and send the Carmyn profile view."""
    view = CarmynProfileView()
    embed = view._create_main_embed()
    
    await interaction.response.send_message(embed=embed, view=view)
