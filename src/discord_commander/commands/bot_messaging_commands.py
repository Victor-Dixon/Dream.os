#!/usr/bin/env python3
"""
<!-- SSOT Domain: messaging -->



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unified_discord_bot import UnifiedDiscordBot


# Import modular command handlers
from .messaging_monitor_commands import MessagingMonitorCommands
from .messaging_core_commands import MessagingCoreCommands
from .profile_commands import ProfileCommands
from .utility_commands import UtilityCommands
from .system_control_commands import SystemControlCommands


logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):

    """Main messaging commands cog that includes all modular handlers."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller):
        """Initialize messaging commands with modular handlers."""
        commands.Cog.__init__(self)

        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)


        """Delegate to monitor commands."""
        await self.monitor_commands.monitor(ctx, action)


    @commands.command(name="message", description="Send message to agent")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):

        """Delegate to core commands."""
        await self.core_commands.message(ctx, agent_id, message)


    @commands.command(name="broadcast", description="Broadcast to all agents")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def broadcast(self, ctx: commands.Context, *, message: str):

        """Delegate to utility commands."""
        await self.utility_commands.list_commands(ctx)

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.aria_profile(ctx)

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Delegate to profile commands."""
        await self.profile_commands.carmyn_profile(ctx)


    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def shutdown_cmd(self, ctx: commands.Context):

        """Delegate to system commands."""
        await self.system_commands.shutdown_cmd(ctx)


    @commands.command(name="restart", description="Restart the Discord bot")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def restart_cmd(self, ctx: commands.Context):

__all__ = ["MessagingCommands"]

