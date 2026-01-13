#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

File Share Commands - Discord Bot
=================================

Share repository files directly from Discord with safe path checks.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-11
License: MIT
"""

from pathlib import Path
import logging

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

logger = logging.getLogger(__name__)


if DISCORD_AVAILABLE:
    class FileShareCommands(commands.Cog):
        """Discord commands for sending repository files as attachments."""

        def __init__(self, bot):
            self.bot = bot
            self.project_root = Path(__file__).parent.parent.parent.resolve()
            self.max_bytes = 7_500_000  # Discord hard limit buffer (8MB default)

        @commands.command(name="sharefile", aliases=["sendfile", "file"])
        async def share_file(self, ctx: commands.Context, *, relative_path: str):
            """
            Share a repository file as a Discord attachment.

            Usage: !sharefile path/to/file.ext
            """
            try:
                clean_path = relative_path.strip().lstrip("/").replace("\\", "/")
                target_path = (self.project_root / clean_path).resolve()

                # Safety: ensure path is inside repo
                if not str(target_path).startswith(str(self.project_root)):
                    await ctx.send("❌ Path is outside the repository.")
                    return

                if not target_path.exists() or not target_path.is_file():
                    await ctx.send(f"❌ File not found: `{clean_path}`")
                    return

                size = target_path.stat().st_size
                if size > self.max_bytes:
                    await ctx.send(
                        f"⚠️ File too large for Discord upload ({size/1_000_000:.2f} MB > 7.5 MB).\n"
                        f"Path: `{clean_path}`"
                    )
                    return

                await ctx.send(
                    content=f"📄 `{clean_path}`",
                    file=discord.File(target_path),
                )
            except Exception as e:
                logger.error(f"Error sharing file: {e}", exc_info=True)
                await ctx.send(f"❌ Error sharing file: {e}")


async def setup(bot):
    """Setup function for discord.py cog loading."""
    if DISCORD_AVAILABLE:
        await bot.add_cog(FileShareCommands(bot))
    else:
        return

