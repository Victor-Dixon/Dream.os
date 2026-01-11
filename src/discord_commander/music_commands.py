#!/usr/bin/env python3
"""
Music Commands - Agent Cellphone V2
===================================

SSOT Domain: discord

Refactored entry point for Discord music commands.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- YouTube audio download and playback (music_service.py)
- Voice channel management
- Music control commands (music_commands_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main MusicCommands class for backward compatibility
from .music_commands_v2 import MusicCommands, setup

# Re-export music service for advanced usage
from .music_service import MusicService, music_service


# === V2 FEATURES MERGED ===

"""
Music Commands V2 - Agent Cellphone V2
=====================================

SSOT Domain: discord

Refactored Discord music commands using service architecture.

Features:
- YouTube audio download and playback
- Voice channel management
- Music control commands
- Cache management

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

from .music_service import music_service

logger = logging.getLogger(__name__)

class MusicCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Discord commands for playing music from YouTube.
    """

    def __init__(self, bot):
        self.bot = bot
        self.music_service = music_service

    @commands.command(name="music", aliases=["play", "m"])
    async def music_command(self, ctx: commands.Context, *, query: Optional[str] = None):
        """
        Play music from YouTube.

        Usage:
        !music <song title or URL>
        !play <song title or URL>
        !m <song title or URL>

        Examples:
        !music never gonna give you up
        !play https://www.youtube.com/watch?v=dQw4w9WgXcQ
        """
        if not query:
            embed = discord.Embed(
                title="🎵 Music Player",
                description="Please provide a song title or YouTube URL!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Usage",
                value="`!music <song title>` or `!music <YouTube URL>`",
                inline=False
            )
            await ctx.send(embed=embed)
            return

        # Extract clean song title
        song_title = self.music_service.extract_song_title(f"!music {query}")

        embed = discord.Embed(
            title="🎵 Downloading Music",
            description=f"Searching for: **{song_title}**",
            color=discord.Color.blue()
        )
        status_msg = await ctx.send(embed=embed)

        try:
            # Join voice channel
            if not await self.music_service.join_voice_channel(ctx):
                await status_msg.edit(embed=discord.Embed(
                    title="❌ Cannot Play Music",
                    description="Unable to join your voice channel!",
                    color=discord.Color.red()
                ))
                return

            # Download audio
            audio_path = await self.music_service.download_youtube_audio(song_title)

            if not audio_path:
                await status_msg.edit(embed=discord.Embed(
                    title="❌ Download Failed",
                    description="Could not download the requested song. Please try a different title or URL.",
                    color=discord.Color.red()
                ))
                return

            # Play music
            if await self.music_service.play_music(ctx, audio_path):
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"**{audio_path.stem}**",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Requested by",
                    value=ctx.author.display_name,
                    inline=True
                )
                embed.add_field(
                    name="Voice Channel",
                    value=ctx.author.voice.channel.name if ctx.author.voice else "Unknown",
                    inline=True
                )
                await status_msg.edit(embed=embed)
            else:
                await status_msg.edit(embed=discord.Embed(
                    title="❌ Playback Failed",
                    description="Could not start music playback.",
                    color=discord.Color.red()
                ))

        except Exception as e:
            logger.error(f"Music command error: {e}")
            await status_msg.edit(embed=discord.Embed(
                title="❌ Error",
                description=f"An error occurred: {str(e)}",
                color=discord.Color.red()
            ))

    @commands.command(name="stop", aliases=["s"])
    async def stop_command(self, ctx: commands.Context):
        """
        Stop current music playback.

        Usage: !stop
        """
        try:
            if await self.music_service.stop_music(ctx):
                embed = discord.Embed(
                    title="⏹️ Music Stopped",
                    description="Playback has been stopped.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="ℹ️ No Music Playing",
                    description="There is no music currently playing.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Stop command error: {e}")
            await ctx.send(f"❌ Error stopping music: {e}")

    @commands.command(name="disconnect", aliases=["dc", "leave"])
    async def disconnect_command(self, ctx: commands.Context):
        """
        Disconnect from voice channel.

        Usage: !disconnect or !leave
        """
        try:
            if await self.music_service.disconnect_voice(ctx):
                embed = discord.Embed(
                    title="👋 Disconnected",
                    description="Left the voice channel.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="ℹ️ Not Connected",
                    description="Not currently connected to a voice channel.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Disconnect command error: {e}")
            await ctx.send(f"❌ Error disconnecting: {e}")

    @commands.command(name="nowplaying", aliases=["np", "current"])
    async def now_playing_command(self, ctx: commands.Context):
        """
        Show currently playing song information.

        Usage: !nowplaying or !np
        """
        try:
            song_info = self.music_service.get_current_song_info()

            if song_info:
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"**{song_info['title']}**",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Voice Channel",
                    value=ctx.author.voice.channel.name if ctx.author.voice else "Unknown",
                    inline=True
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="ℹ️ No Music Playing",
                    description="There is no music currently playing.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Now playing command error: {e}")
            await ctx.send(f"❌ Error getting current song: {e}")

    @commands.command(name="cleanup_music", aliases=["clean_music"])
    async def cleanup_music_command(self, ctx: commands.Context):
        """
        Clean up old cached music files.

        Usage: !cleanup_music
        """
        try:
            removed_count = self.music_service.cleanup_cache()

            embed = discord.Embed(
                title="🧹 Music Cache Cleaned",
                description=f"Removed {removed_count} old audio files from cache.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Cleanup command error: {e}")
            await ctx.send(f"❌ Error cleaning cache: {e}")

    # Voice state update handler
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        Handle voice state updates (auto-disconnect when alone).
        """
        if not DISCORD_AVAILABLE:
            return

        try:
            # Only process for our bot
            if member.id != self.bot.user.id:
                return

            # Check if bot was disconnected or moved
            if before.channel is not None and after.channel is None:
                # Bot was disconnected
                self.music_service.current_voice_client = None
                self.music_service.current_song = None
                logger.info("Bot disconnected from voice channel")

            elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                # Bot was moved to different channel
                logger.info(f"Bot moved from {before.channel.name} to {after.channel.name}")

        except Exception as e:
            logger.error(f"Voice state update error: {e}")

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(MusicCommands(bot))