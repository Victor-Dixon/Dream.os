<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
"""
Profile Commands - Modular V2 Compliance
========================================

Profile display commands (Aria, Carmyn) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular profile commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
=======
=======
#!/usr/bin/env python3
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
"""
Profile Commands - Modular V2 Compliance
========================================

Profile display commands (Aria, Carmyn) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

<<<<<<< HEAD
V2 Compliance: <300 lines, <5 classes, <10 functions
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
V2 Compliant: Modular profile commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
"""

import logging

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

<<<<<<< HEAD
from ...core.base.common_command_base import CommonCommandBase

logger = logging.getLogger(__name__)


class ProfileCommands(CommonCommandBase):
    """Profile display commands for team members."""

    def __init__(self, bot):
        """Initialize profile commands."""
        super().__init__(bot)  # Uses CommonCommandBase for standardized initialization

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView
=======
logger = logging.getLogger(__name__)


class ProfileCommands(commands.Cog):
    """Profile display commands for team members."""

    def __init__(self, bot):
        """Initialize profile commands."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView
<<<<<<< HEAD

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            view = AriaProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !aria command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
<<<<<<< HEAD
<<<<<<< HEAD
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.carmyn_profile_view import CarmynProfileView
=======
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        try:
<<<<<<< HEAD
            from ..views.carmyn_profile_view import CarmynProfileView

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            from src.discord_commander.views.carmyn_profile_view import CarmynProfileView
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

<<<<<<< HEAD
<<<<<<< HEAD

__all__ = ["ProfileCommands"]
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

__all__ = ["ProfileCommands"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
