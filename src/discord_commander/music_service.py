"""
Music Service - Agent Cellphone V2
==================================

SSOT Domain: discord

Core music service functionality for YouTube audio download and playback.

Features:
- YouTube audio download using yt-dlp
- Audio file caching and management
- Voice channel connection handling
- Audio playback coordination

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import asyncio
import logging
import os
import re
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import discord
    from discord import FFmpegPCMAudio
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    FFmpegPCMAudio = None

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    yt_dlp = None

logger = logging.getLogger(__name__)

class MusicService:
    """
    Service for downloading and playing music from YouTube.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path("cache/music")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.current_voice_client: Optional[discord.VoiceClient] = None
        self.current_song: Optional[Dict[str, Any]] = None

        # yt-dlp configuration
        self.ytdl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.cache_dir / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

    def extract_song_title(self, content: str) -> str:
        """
        Extract song title from Discord message content.

        Args:
            content: Raw message content

        Returns:
            Cleaned song title
        """
        # Remove command prefix and clean up
        content = content.strip()

        # Handle different command formats
        patterns = [
            r'^!music\s*(.+)',
            r'^!play\s*(.+)',
            r'^music\s*(.+)',
            r'^play\s*(.+)'
        ]

        for pattern in patterns:
            match = re.match(pattern, content, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove extra whitespace and quotes
                title = re.sub(r'\s+', ' ', title)
                title = title.strip('"\'')
                return title

        # Fallback: return content as-is if no pattern matches
        return content.strip()

    async def download_youtube_audio(self, query: str) -> Optional[Path]:
        """
        Download audio from YouTube based on search query.

        Args:
            query: Search query or URL

        Returns:
            Path to downloaded audio file, or None if failed
        """
        if not YT_DLP_AVAILABLE:
            logger.error("yt-dlp not available for YouTube download")
            return None

        try:
            # Clean query for filename
            safe_query = re.sub(r'[^\w\s-]', '', query)[:50]
            filename = f"{safe_query}.mp3"
            output_path = self.cache_dir / filename

            # Check cache first
            if output_path.exists():
                logger.info(f"Using cached audio: {filename}")
                return output_path

            # Download with yt-dlp
            with yt_dlp.YoutubeDL(self.ytdl_opts) as ydl:
                # Search for video if not a URL
                if not query.startswith(('http://', 'https://')):
                    query = f"ytsearch1:{query}"

                info = ydl.extract_info(query, download=True)

                if 'entries' in info:
                    # Search result
                    video_info = info['entries'][0]
                else:
                    # Direct URL
                    video_info = info

                # Get the actual filename
                title = video_info.get('title', 'unknown')
                safe_title = re.sub(r'[^\w\s-]', '', title)[:50]
                actual_path = self.cache_dir / f"{safe_title}.mp3"

                if actual_path.exists():
                    logger.info(f"Successfully downloaded: {title}")
                    return actual_path
                else:
                    logger.error(f"Download failed - file not found: {actual_path}")
                    return None

        except Exception as e:
            logger.error(f"YouTube download failed for '{query}': {e}")
            return None

    async def join_voice_channel(self, ctx) -> bool:
        """
        Join the voice channel of the command author.

        Args:
            ctx: Discord command context

        Returns:
            True if successfully joined, False otherwise
        """
        if not DISCORD_AVAILABLE:
            return False

        try:
            if ctx.author.voice is None:
                await ctx.send("❌ You must be in a voice channel to play music!")
                return False

            voice_channel = ctx.author.voice.channel

            if ctx.voice_client is not None:
                # Already in a voice channel
                if ctx.voice_client.channel == voice_channel:
                    return True
                else:
                    # Move to new channel
                    await ctx.voice_client.move_to(voice_channel)
                    return True
            else:
                # Join new channel
                self.current_voice_client = await voice_channel.connect()
                return True

        except Exception as e:
            logger.error(f"Failed to join voice channel: {e}")
            await ctx.send(f"❌ Failed to join voice channel: {e}")
            return False

    async def play_music(self, ctx, audio_path: Path) -> bool:
        """
        Play audio file in voice channel.

        Args:
            ctx: Discord command context
            audio_path: Path to audio file

        Returns:
            True if playback started successfully
        """
        if not DISCORD_AVAILABLE or not audio_path.exists():
            return False

        try:
            voice_client = ctx.voice_client
            if voice_client is None:
                logger.error("No voice client available")
                return False

            # Create audio source
            audio_source = FFmpegPCMAudio(str(audio_path))

            # Play audio
            voice_client.play(audio_source)

            # Store current song info
            self.current_song = {
                'path': audio_path,
                'title': audio_path.stem,
                'ctx': ctx
            }

            logger.info(f"Started playing: {audio_path.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to play music: {e}")
            await ctx.send(f"❌ Failed to play music: {e}")
            return False

    async def stop_music(self, ctx) -> bool:
        """
        Stop current music playback.

        Args:
            ctx: Discord command context

        Returns:
            True if stopped successfully
        """
        try:
            voice_client = ctx.voice_client
            if voice_client and voice_client.is_playing():
                voice_client.stop()
                self.current_song = None
                logger.info("Music playback stopped")
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to stop music: {e}")
            return False

    async def disconnect_voice(self, ctx) -> bool:
        """
        Disconnect from voice channel.

        Args:
            ctx: Discord command context

        Returns:
            True if disconnected successfully
        """
        try:
            voice_client = ctx.voice_client
            if voice_client:
                await voice_client.disconnect()
                self.current_voice_client = None
                self.current_song = None
                logger.info("Disconnected from voice channel")
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to disconnect from voice: {e}")
            return False

    def get_current_song_info(self) -> Optional[Dict[str, Any]]:
        """Get information about currently playing song."""
        return self.current_song

    def cleanup_cache(self, max_age_hours: int = 24) -> int:
        """
        Clean up old cached audio files.

        Args:
            max_age_hours: Maximum age of files to keep

        Returns:
            Number of files removed
        """
        import time

        removed_count = 0
        cutoff_time = time.time() - (max_age_hours * 3600)

        try:
            for audio_file in self.cache_dir.glob("*.mp3"):
                if audio_file.stat().st_mtime < cutoff_time:
                    audio_file.unlink()
                    removed_count += 1

            logger.info(f"Cleaned up {removed_count} old audio files")
            return removed_count

        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")
            return 0

# Global music service instance
music_service = MusicService()

__all__ = ["MusicService", "music_service"]