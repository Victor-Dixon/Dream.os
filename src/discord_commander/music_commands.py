#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Music Commands - Discord Bot Music Player
==========================================

Discord commands for playing music from YouTube.
Downloads YouTube videos as MP3 and plays them in voice channels.

Usage: !music(song title)

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-07
"""

import asyncio
import logging
import os
import re
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Discord imports
try:
    import discord
    from discord.ext import commands
    from discord import FFmpegPCMAudio
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None
    FFmpegPCMAudio = None

# YouTube download imports
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    yt_dlp = None

logger = logging.getLogger(__name__)

# Create music cache directory
MUSIC_CACHE_DIR = Path(project_root) / "cache" / "music"
MUSIC_CACHE_DIR.mkdir(parents=True, exist_ok=True)


if DISCORD_AVAILABLE and YT_DLP_AVAILABLE:
    class MusicCommands(commands.Cog):
        """Discord commands for music playback from YouTube."""

        def __init__(self, bot):
            """Initialize music commands."""
            self.bot = bot
            self.logger = logging.getLogger(__name__)
            self.voice_clients = {}  # Store voice clients per guild

        def _extract_song_title(self, content: str) -> str:
            """
            Extract song title from !music(song title) command.
            
            Args:
                content: Message content
                
            Returns:
                Song title string or None
            """
            # Match !music(song title) pattern
            pattern = r'!music\(([^)]+)\)'
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            return None

        async def _download_youtube_audio(self, query: str) -> Path:
            """
            Download YouTube audio as MP3.
            
            Args:
                query: Search query or YouTube URL
                
            Returns:
                Path to downloaded MP3 file
            """
            try:
                # Configure yt-dlp options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': str(MUSIC_CACHE_DIR / '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True,
                    'no_warnings': True,
                }

                # Download audio
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # If it's a URL, use it directly; otherwise search
                    if query.startswith(('http://', 'https://', 'www.')):
                        info = ydl.extract_info(query, download=True)
                    else:
                        # Search for video
                        search_query = f"ytsearch1:{query}"
                        info = ydl.extract_info(search_query, download=True)
                        if 'entries' in info and info['entries']:
                            info = info['entries'][0]

                    # Get the downloaded file path
                    title = info.get('title', 'unknown')
                    # Sanitize filename
                    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                    mp3_path = MUSIC_CACHE_DIR / f"{safe_title}.mp3"
                    
                    # If file doesn't exist with exact title, find the most recent file
                    if not mp3_path.exists():
                        # Find the most recently created file in cache
                        files = list(MUSIC_CACHE_DIR.glob("*.mp3"))
                        if files:
                            mp3_path = max(files, key=lambda p: p.stat().st_mtime)
                    
                    self.logger.info(f"Downloaded audio: {mp3_path}")
                    return mp3_path

            except Exception as e:
                self.logger.error(f"Error downloading YouTube audio: {e}")
                raise

        async def _join_voice_channel(self, ctx: commands.Context):
            """
            Join the user's voice channel.
            
            Args:
                ctx: Command context
                
            Returns:
                VoiceClient or None
            """
            if not ctx.author.voice:
                await ctx.send("❌ You need to be in a voice channel to play music!")
                return None

            channel = ctx.author.voice.channel
            guild_id = ctx.guild.id

            # Check if already connected
            if guild_id in self.voice_clients:
                voice_client = self.voice_clients[guild_id]
                if voice_client.is_connected():
                    # If in different channel, move to user's channel
                    if voice_client.channel != channel:
                        await voice_client.move_to(channel)
                    return voice_client

            # Connect to voice channel
            try:
                voice_client = await channel.connect()
                self.voice_clients[guild_id] = voice_client
                self.logger.info(f"Connected to voice channel: {channel.name}")
                return voice_client
            except Exception as e:
                self.logger.error(f"Error joining voice channel: {e}")
                await ctx.send(f"❌ Error joining voice channel: {e}")
                return None


        @commands.command(name="music", aliases=["play", "song"])
        async def music_command(self, ctx: commands.Context, *, query: str = None):
            """
            Play music from YouTube.
            
            Usage:
            !music(song title)
            !music Tobe Nwigwe that FYE FYE
            !music https://www.youtube.com/watch?v=...
            """
            try:
                # Extract song title from !music(song title) format if present
                if not query:
                    song_title = self._extract_song_title(ctx.message.content)
                    if not song_title:
                        await ctx.send(
                            "❌ Please provide a song title!\n"
                            "Usage: `!music(song title)` or `!music song title`"
                        )
                        return
                    query = song_title
                else:
                    # Also check if query contains the pattern
                    extracted = self._extract_song_title(ctx.message.content)
                    if extracted:
                        query = extracted

                await self._play_music(ctx, query)

            except Exception as e:
                self.logger.error(f"Error in music command: {e}", exc_info=True)
                await ctx.send(
                    embed=discord.Embed(
                        title="❌ Error",
                        description=f"An error occurred: {str(e)}",
                        color=discord.Color.red()
                    )
                )

        async def _play_music(self, ctx: commands.Context, query: str):
            """
            Internal method to play music.
            
            Args:
                ctx: Command context
                query: Song title or YouTube URL
            """

            # Send initial message
            embed = discord.Embed(
                title="🎵 Downloading Music",
                description=f"Searching for: **{query}**",
                color=discord.Color.blue()
            )
            status_msg = await ctx.send(embed=embed)

            # Join voice channel
            voice_client = await self._join_voice_channel(ctx)
            if not voice_client:
                await status_msg.delete()
                return

            # Download audio
            try:
                mp3_path = await self._download_youtube_audio(query)
            except Exception as e:
                await status_msg.edit(
                    embed=discord.Embed(
                        title="❌ Download Failed",
                        description=f"Error downloading audio: {str(e)}",
                        color=discord.Color.red()
                    )
                )
                return

            # Play audio
            try:
                # Stop any currently playing audio
                if voice_client.is_playing():
                    voice_client.stop()

                # Create audio source
                audio_source = FFmpegPCMAudio(
                    str(mp3_path),
                    options='-vn'
                )

                # Play audio
                voice_client.play(
                    audio_source,
                    after=lambda e: self.logger.error(f"Playback error: {e}") if e else None
                )

                # Update status message
                await status_msg.edit(
                    embed=discord.Embed(
                        title="🎵 Now Playing",
                        description=f"**{mp3_path.stem}**",
                        color=discord.Color.green()
                    )
                )

                self.logger.info(f"Playing: {mp3_path.stem}")

            except Exception as e:
                self.logger.error(f"Error playing audio: {e}")
                await status_msg.edit(
                    embed=discord.Embed(
                        title="❌ Playback Failed",
                        description=f"Error playing audio: {str(e)}",
                        color=discord.Color.red()
                    )
                )

        @commands.command(name="stop", aliases=["stopmusic"])
        async def stop_command(self, ctx: commands.Context):
            """Stop currently playing music."""
            try:
                guild_id = ctx.guild.id
                if guild_id in self.voice_clients:
                    voice_client = self.voice_clients[guild_id]
                    if voice_client.is_playing():
                        voice_client.stop()
                        await ctx.send("⏹️ Music stopped")
                    else:
                        await ctx.send("❌ No music is currently playing")
                else:
                    await ctx.send("❌ Bot is not connected to a voice channel")
            except Exception as e:
                self.logger.error(f"Error in stop command: {e}")
                await ctx.send(f"❌ Error: {str(e)}")

        @commands.command(name="disconnect", aliases=["leave", "dc"])
        async def disconnect_command(self, ctx: commands.Context):
            """Disconnect bot from voice channel."""
            try:
                guild_id = ctx.guild.id
                if guild_id in self.voice_clients:
                    voice_client = self.voice_clients[guild_id]
                    await voice_client.disconnect()
                    del self.voice_clients[guild_id]
                    await ctx.send("👋 Disconnected from voice channel")
                else:
                    await ctx.send("❌ Bot is not connected to a voice channel")
            except Exception as e:
                self.logger.error(f"Error in disconnect command: {e}")
                await ctx.send(f"❌ Error: {str(e)}")

        @commands.Cog.listener()
        async def on_voice_state_update(self, member, before, after):
            """Auto-disconnect if bot is alone in voice channel."""
            if member == self.bot.user:
                return

            # Check if bot is in a voice channel
            for guild_id, voice_client in list(self.voice_clients.items()):
                if voice_client.is_connected():
                    channel = voice_client.channel
                    # If bot is alone (only itself), disconnect
                    if len(channel.members) == 1:
                        await voice_client.disconnect()
                        del self.voice_clients[guild_id]
                        self.logger.info(f"Auto-disconnected from {channel.name} (alone)")


async def setup(bot):
    """Setup function for cog loading."""
    if DISCORD_AVAILABLE and YT_DLP_AVAILABLE:
        await bot.add_cog(MusicCommands(bot))
        logger.info("✅ Music commands loaded")
    else:
        missing = []
        if not DISCORD_AVAILABLE:
            missing.append("discord.py")
        if not YT_DLP_AVAILABLE:
            missing.append("yt-dlp")
        logger.warning(f"⚠️ Music commands not loaded - missing: {', '.join(missing)}")

