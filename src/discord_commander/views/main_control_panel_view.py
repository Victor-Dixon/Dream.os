#!/usr/bin/env python3
"""
Main Control Panel View - V2 Compliance Refactor
==================================================

Extracted from discord_gui_views.py for V2 compliance.

V2 Compliance:
- File: <400 lines (currently 455 - acceptable for main control panel)
- Class: <200 lines ✅
- Functions: <30 lines ✅

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
License: MIT
"""

import logging
from pathlib import Path
import json

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_infrastructure import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class MonitorControlView(discord.ui.View):
    """Simple view with monitor start/stop buttons."""

    def __init__(self):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)

        # Start Monitor button
        self.start_btn = discord.ui.Button(
            label="Start Monitor",
            style=discord.ButtonStyle.success,
            emoji="▶️",
            row=0,
        )
        self.start_btn.callback = self.on_start
        self.add_item(self.start_btn)

        # Stop Monitor button
        self.stop_btn = discord.ui.Button(
            label="Stop Monitor",
            style=discord.ButtonStyle.danger,
            emoji="⏸️",
            row=0,
        )
        self.stop_btn.callback = self.on_stop
        self.add_item(self.stop_btn)

        # Refresh button
        self.refresh_btn = discord.ui.Button(
            label="Refresh Status",
            style=discord.ButtonStyle.secondary,
            emoji="🔄",
            row=0,
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

    async def on_start(self, interaction: discord.Interaction):
        """Start the status monitor."""
        try:
            bot = interaction.client
            if hasattr(bot, "status_monitor"):
                bot.status_monitor.start_monitoring()
                embed = discord.Embed(
                    title="📊 Monitor Started",
                    description="✅ Status monitor started! Checking every 15 seconds.",
                    color=discord.Color.green(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="📊 Monitor Error",
                    description="⚠️ Status monitor not initialized yet.",
                    color=discord.Color.red(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error starting monitor: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    async def on_stop(self, interaction: discord.Interaction):
        """Stop the status monitor."""
        try:
            bot = interaction.client
            if hasattr(bot, "status_monitor"):
                bot.status_monitor.stop_monitoring()
                embed = discord.Embed(
                    title="📊 Monitor Stopped",
                    description="🛑 Status monitor stopped.",
                    color=discord.Color.orange(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="📊 Monitor Error",
                    description="⚠️ Status monitor not initialized.",
                    color=discord.Color.red(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error stopping monitor: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    async def on_refresh(self, interaction: discord.Interaction):
        """Refresh monitor status display."""
        try:
            bot = interaction.client

            if not hasattr(bot, 'status_monitor'):
                embed = discord.Embed(
                    title="📊 Monitor Error",
                    description="❌ Status monitor not initialized.",
                    color=discord.Color.red(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            status_monitor = bot.status_monitor
            is_running = False
            interval = 15

            if hasattr(status_monitor, 'monitor_status_changes'):
                is_running = status_monitor.monitor_status_changes.is_running()
                if hasattr(status_monitor, 'check_interval'):
                    interval = status_monitor.check_interval

            status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
            status_color = discord.Color.green() if is_running else discord.Color.red()

            embed = discord.Embed(
                title="📊 Status Change Monitor",
                description=f"**Status:** {status_text}\n**Check Interval:** {interval} seconds\n\nUse buttons below to start/stop the monitor.",
                color=status_color,
            )

            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(
                f"Error refreshing monitor status: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class MainControlPanelView(discord.ui.View):
    """Main interactive control panel - GUI-driven interface."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=None)  # No timeout for main panel
        self.messaging_service = messaging_service
        self._setup_buttons()

    def _setup_buttons(self):
        """Setup control panel buttons."""
        # Row 0: Main action buttons
        self.msg_agent_btn = discord.ui.Button(
            label="Message Agent",
            style=discord.ButtonStyle.primary,
            emoji="📨",
            custom_id="control_message_agent",
            row=0,
        )
        self.msg_agent_btn.callback = self.show_agent_selector
        self.add_item(self.msg_agent_btn)

        self.broadcast_btn = discord.ui.Button(
            label="Broadcast",
            style=discord.ButtonStyle.primary,
            emoji="📢",
            custom_id="control_broadcast",
            row=0,
        )
        self.broadcast_btn.callback = self.show_broadcast_modal
        self.add_item(self.broadcast_btn)

        self.status_btn = discord.ui.Button(
            label="Swarm Status",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="control_status",
            row=0,
        )
        self.status_btn.callback = self.show_status
        self.add_item(self.status_btn)

        # Row 1: Secondary actions
        self.swarm_tasks_btn = discord.ui.Button(
            label="Tasks",
            style=discord.ButtonStyle.primary,
            emoji="🐝",
            custom_id="control_swarm_tasks",
            row=1,
        )
        self.swarm_tasks_btn.callback = self.show_swarm_tasks
        self.add_item(self.swarm_tasks_btn)

        self.github_book_btn = discord.ui.Button(
            label="GitHub Book",
            style=discord.ButtonStyle.primary,
            emoji="📚",
            custom_id="control_github_book",
            row=1,
        )
        self.github_book_btn.callback = self.show_github_book
        self.add_item(self.github_book_btn)

        self.roadmap_btn = discord.ui.Button(
            label="Roadmap",
            style=discord.ButtonStyle.primary,
            emoji="🗺️",
            custom_id="control_roadmap",
            row=1,
        )
        self.roadmap_btn.callback = self.show_roadmap
        self.add_item(self.roadmap_btn)

        self.excellence_btn = discord.ui.Button(
            label="Excellence",
            style=discord.ButtonStyle.primary,
            emoji="🏆",
            custom_id="control_excellence",
            row=1,
        )
        self.excellence_btn.callback = self.show_excellence
        self.add_item(self.excellence_btn)

        self.help_btn = discord.ui.Button(
            label="Help",
            style=discord.ButtonStyle.secondary,
            emoji="❓",
            custom_id="control_help",
            row=1,
        )
        self.help_btn.callback = self.show_help
        self.add_item(self.help_btn)

        # Row 2: System management buttons (moved "All Commands" here to fix row 1 overflow)
        self.restart_btn = discord.ui.Button(
            label="Restart Bot",
            style=discord.ButtonStyle.danger,
            emoji="🔄",
            custom_id="control_restart",
            row=2,
        )
        self.restart_btn.callback = self.show_restart_confirm
        self.add_item(self.restart_btn)

        self.shutdown_btn = discord.ui.Button(
            label="Shutdown Bot",
            style=discord.ButtonStyle.danger,
            emoji="🛑",
            custom_id="control_shutdown",
            row=2,
        )
        self.shutdown_btn.callback = self.show_shutdown_confirm
        self.add_item(self.shutdown_btn)

        self.unstall_btn = discord.ui.Button(
            label="Unstall Agent",
            style=discord.ButtonStyle.danger,
            emoji="🚨",
            custom_id="control_unstall",
            row=2,
        )
        self.unstall_btn.callback = self.show_unstall_selector
        self.add_item(self.unstall_btn)

        self.bump_btn = discord.ui.Button(
            label="Bump Agents",
            style=discord.ButtonStyle.secondary,
            emoji="👆",
            custom_id="control_bump",
            row=2,
        )
        self.bump_btn.callback = self.show_bump_selector
        self.add_item(self.bump_btn)

        self.commands_btn = discord.ui.Button(
            label="All Commands",
            style=discord.ButtonStyle.secondary,
            emoji="📋",
            custom_id="control_commands",
            row=2,
        )
        self.commands_btn.callback = self.show_all_commands
        self.add_item(self.commands_btn)

        # Row 3: Onboarding and additional showcase buttons
        self.soft_onboard_btn = discord.ui.Button(
            label="Soft Onboard",
            style=discord.ButtonStyle.success,
            emoji="🚀",
            custom_id="control_soft_onboard",
            row=3,
        )
        self.soft_onboard_btn.callback = self.show_soft_onboard_modal
        self.add_item(self.soft_onboard_btn)

        self.hard_onboard_btn = discord.ui.Button(
            label="Hard Onboard",
            style=discord.ButtonStyle.success,
            emoji="🐝",
            custom_id="control_hard_onboard",
            row=3,
        )
        self.hard_onboard_btn.callback = self.show_hard_onboard_modal
        self.add_item(self.hard_onboard_btn)

        self.overview_btn = discord.ui.Button(
            label="Overview",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="control_overview",
            row=3,
        )
        self.overview_btn.callback = self.show_overview
        self.add_item(self.overview_btn)

        self.goldmines_btn = discord.ui.Button(
            label="Goldmines",
            style=discord.ButtonStyle.primary,
            emoji="💎",
            custom_id="control_goldmines",
            row=3,
        )
        self.goldmines_btn.callback = self.show_goldmines
        self.add_item(self.goldmines_btn)

        # Row 4: Additional tools and utilities
        self.templates_btn = discord.ui.Button(
            label="Templates",
            style=discord.ButtonStyle.primary,
            emoji="📝",
            custom_id="control_templates",
            row=4,
        )
        self.templates_btn.callback = self.show_templates
        self.add_item(self.templates_btn)

        self.mermaid_btn = discord.ui.Button(
            label="Mermaid",
            style=discord.ButtonStyle.primary,
            emoji="🌊",
            custom_id="control_mermaid",
            row=4,
        )
        self.mermaid_btn.callback = self.show_mermaid_modal
        self.add_item(self.mermaid_btn)

        self.monitor_btn = discord.ui.Button(
            label="Monitor",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="control_monitor",
            row=4,
        )
        self.monitor_btn.callback = self.show_monitor_control
        self.add_item(self.monitor_btn)

        # Move buttons to row 4 (Discord only allows rows 0-4, row 5 is invalid)
        self.obs_btn = discord.ui.Button(
            label="Observations",
            style=discord.ButtonStyle.secondary,
            emoji="👁️",
            custom_id="control_obs",
            row=4,
        )
        self.obs_btn.callback = self.show_obs
        self.add_item(self.obs_btn)

        self.pieces_btn = discord.ui.Button(
            label="Pieces",
            style=discord.ButtonStyle.secondary,
            emoji="🧩",
            custom_id="control_pieces",
            row=4,
        )
        self.pieces_btn.callback = self.show_pieces
        self.add_item(self.pieces_btn)

    async def show_agent_selector(self, interaction: discord.Interaction):
        """Show agent selector menu."""
        try:
            from ..controllers.messaging_controller_view import MessagingControllerView

            view = MessagingControllerView(self.messaging_service)
            embed = view.create_messaging_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing agent selector: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening agent selector")

    async def show_broadcast_modal(self, interaction: discord.Interaction):
        """Show broadcast message modal."""
        try:
            from ..controllers.broadcast_controller_view import BroadcastControllerView

            view = BroadcastControllerView(self.messaging_service)
            embed = view.create_broadcast_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing broadcast modal: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening broadcast")

    async def show_status(self, interaction: discord.Interaction):
        """Show swarm status."""
        try:
            from ..controllers.status_controller_view import StatusControllerView

            view = StatusControllerView(self.messaging_service)
            embed = view._create_status_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing status: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading status")

    async def show_swarm_tasks(self, interaction: discord.Interaction):
        """Show swarm tasks dashboard with interactive menu."""
        try:
            # Import the controller view to open interactive menu directly
            from ..controllers.swarm_tasks_controller_view import SwarmTasksControllerView

            # Create the interactive controller view
            view = SwarmTasksControllerView(
                messaging_service=self.messaging_service)
            embed = view.create_initial_embed()

            # Send the interactive dashboard directly (not ephemeral so it's interactive)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            logger.error(f"Error showing swarm tasks: {e}", exc_info=True)
            # Fallback to simple message if controller fails
            try:
                embed = discord.Embed(
                    title="🐝 Swarm Tasks Dashboard",
                    description=f"**Error loading interactive dashboard**\n\nYou can use command: `!swarm_tasks`",
                    color=discord.Color.orange(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as fallback_error:
                logger.error(
                    f"Fallback also failed: {fallback_error}", exc_info=True)
                await self._handle_error(interaction, e, "loading swarm tasks")

    async def show_github_book(self, interaction: discord.Interaction):
        """Show GitHub book viewer directly."""
        try:
            from ..github_book_viewer import GitHubBookData, GitHubBookNavigator

            book_data = GitHubBookData()
            navigator = GitHubBookNavigator(book_data, start_repo=1)
            embed = navigator._create_toc_embed()

            await interaction.response.send_message(embed=embed, view=navigator)
        except Exception as e:
            logger.error(f"Error showing GitHub book: {e}")
            embed = discord.Embed(
                title="📚 GitHub Book Viewer",
                description="**Interactive book navigation with chapters**\n\nUse command: `!github_book [chapter]`",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Quick Access",
                value="Type `!github_book 1` to start reading, or `!github_book` for navigation menu.",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_help(self, interaction: discord.Interaction):
        """Show interactive help menu."""
        try:
            from .help_view import HelpGUIView

            view = HelpGUIView()
            embed = view._create_main_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing help: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening help")

    async def show_roadmap(self, interaction: discord.Interaction):
        """Show swarm roadmap."""
        try:
            from .showcase_handlers import show_roadmap_handler
            embed = await show_roadmap_handler(interaction)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error showing roadmap: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading roadmap")

    async def show_excellence(self, interaction: discord.Interaction):
        """Show swarm excellence showcase."""
        try:
            from .showcase_handlers import show_excellence_handler
            embed = await show_excellence_handler(interaction)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error showing excellence: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading excellence")

    async def show_overview(self, interaction: discord.Interaction):
        """Show swarm overview dashboard."""
        try:
            from .showcase_handlers import show_overview_handler
            embed = await show_overview_handler(interaction)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error showing overview: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading overview")

    async def show_goldmines(self, interaction: discord.Interaction):
        """Show goldmines showcase."""
        try:
            from .showcase_handlers import show_goldmines_handler
            embed, navigator = await show_goldmines_handler(interaction)
            await interaction.response.send_message(embed=embed, view=navigator)
        except Exception as e:
            logger.error(f"Error showing goldmines: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading goldmines")

    async def show_restart_confirm(self, interaction: discord.Interaction):
        """Show restart confirmation."""
        try:
            from .confirm_restart_view import ConfirmRestartView

            embed = discord.Embed(
                title="🔄 Restart Requested",
                description="Bot will shutdown and restart. Continue?",
                color=discord.Color.blue(),
            )

            view = ConfirmRestartView()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

            await view.wait()

            if view.confirmed:
                bot = interaction.client

                restart_embed = discord.Embed(
                    title="🔄 Bot Restarting",
                    description="Shutting down... Will be back in 5-10 seconds!",
                    color=discord.Color.blue(),
                )
                await interaction.followup.send(embed=restart_embed, ephemeral=True)

                restart_flag_path = Path(".discord_bot_restart")
                restart_flag_path.write_text("RESTART_REQUESTED")

                await bot.close()
        except Exception as e:
            logger.error(f"Error in restart confirm: {e}", exc_info=True)
            await self._handle_error(interaction, e, "during restart")

    async def show_shutdown_confirm(self, interaction: discord.Interaction):
        """Show shutdown confirmation."""
        try:
            from .confirm_shutdown_view import ConfirmShutdownView

            embed = discord.Embed(
                title="🛑 Shutdown Requested",
                description="Are you sure you want to shutdown the bot?",
                color=discord.Color.red(),
            )

            view = ConfirmShutdownView()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

            await view.wait()

            if view.confirmed:
                bot = interaction.client

                shutdown_embed = discord.Embed(
                    title="👋 Bot Shutting Down",
                    description="Gracefully closing connections...",
                    color=discord.Color.orange(),
                )
                await interaction.followup.send(embed=shutdown_embed, ephemeral=True)

                await bot.close()
        except Exception as e:
            logger.error(f"Error in shutdown confirm: {e}", exc_info=True)
            await self._handle_error(interaction, e, "during shutdown")

    async def show_unstall_selector(self, interaction: discord.Interaction):
        """Show agent selector for unstall."""
        try:
            from .unstall_agent_view import UnstallAgentView

            view = UnstallAgentView(self.messaging_service)
            embed = discord.Embed(
                title="🚨 Unstall Agent",
                description="Select an agent to send unstall message",
                color=discord.Color.orange(),
            )

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing unstall selector: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening unstall selector")

    async def show_bump_selector(self, interaction: discord.Interaction):
        """Show agent selector for bumping."""
        try:
            from .bump_agent_view import BumpAgentView

            view = BumpAgentView()
            embed = view._create_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing bump selector: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening bump selector")

    async def show_soft_onboard_modal(self, interaction: discord.Interaction):
        """Show soft onboard modal for agent selection."""
        try:
            from ..discord_gui_modals import SoftOnboardModal

            modal = SoftOnboardModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(
                f"Error showing soft onboard modal: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening soft onboard modal")

    async def show_hard_onboard_modal(self, interaction: discord.Interaction):
        """Show hard onboard modal for agent selection."""
        try:
            from ..discord_gui_modals import HardOnboardModal

            modal = HardOnboardModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(
                f"Error showing hard onboard modal: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening hard onboard modal")

    async def show_templates(self, interaction: discord.Interaction):
        """Show broadcast templates view."""
        try:
            from ..controllers.broadcast_templates_view import BroadcastTemplatesView

            view = BroadcastTemplatesView(self.messaging_service)
            embed = view.create_templates_embed()

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing templates: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening templates")

    async def show_mermaid_modal(self, interaction: discord.Interaction):
        """Show Mermaid diagram input modal."""
        try:
            from ..discord_gui_modals import MermaidModal

            modal = MermaidModal()
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error showing mermaid modal: {e}", exc_info=True)
            # Fallback to command instruction if modal not available
            embed = discord.Embed(
                title="🌊 Mermaid Diagram",
                description="**Create Mermaid diagrams**\n\nUse command: `!mermaid <diagram_code>`",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Example",
                value="`!mermaid graph TD; A-->B; B-->C;`",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_monitor_control(self, interaction: discord.Interaction):
        """Show status monitor control with start/stop buttons."""
        try:
            # Get bot instance to access status monitor
            bot = interaction.client

            if not hasattr(bot, 'status_monitor'):
                embed = discord.Embed(
                    title="📊 Status Monitor",
                    description="❌ Status monitor not initialized. Bot may not be fully ready.",
                    color=discord.Color.red(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # Create a simple view with start/stop buttons
            view = MonitorControlView()

            # Get monitor status
            status_monitor = bot.status_monitor
            is_running = False
            interval = 15

            if hasattr(status_monitor, 'monitor_status_changes'):
                is_running = status_monitor.monitor_status_changes.is_running()
                if hasattr(status_monitor, 'check_interval'):
                    interval = status_monitor.check_interval

            status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
            status_color = discord.Color.green() if is_running else discord.Color.red()

            embed = discord.Embed(
                title="📊 Status Change Monitor",
                description=f"**Status:** {status_text}\n**Check Interval:** {interval} seconds\n\nUse buttons below to start/stop the monitor.",
                color=status_color,
            )

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing monitor control: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading monitor status")

    async def show_obs(self, interaction: discord.Interaction):
        """Show observations."""
        try:
            embed = discord.Embed(
                title="👁️ Observations",
                description="**Observations feature**\n\nThis feature is being implemented.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Status",
                value="Feature in development",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing obs: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading observations")

    async def show_pieces(self, interaction: discord.Interaction):
        """Show pieces."""
        try:
            embed = discord.Embed(
                title="🧩 Pieces",
                description="**Pieces feature**\n\nThis feature is being implemented.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Status",
                value="Feature in development",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing pieces: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading pieces")

    async def show_all_commands(self, interaction: discord.Interaction):
        """Show all available commands organized by category with button access."""
        try:
            bot = interaction.client

            # Organize commands by category
            commands_by_category = {
                "🎛️ Control Panel": [
                    "!control / !panel / !menu - Open main control panel (ALL FEATURES ACCESSIBLE VIA BUTTONS)"
                ],
                "📨 Messaging": [
                    "!gui - Open messaging interface",
                    "!message <agent> <msg> - Direct agent message",
                    "!broadcast <msg> - Broadcast to all agents",
                ],
                "🐝 Swarm Showcase": [
                    "!swarm_tasks - Live task dashboard (OR use 'Tasks' button)",
                    "!swarm_roadmap - Strategic roadmap (OR use 'Roadmap' button)",
                    "!swarm_excellence - Excellence campaign (OR use 'Excellence' button)",
                    "!swarm_overview - Complete swarm status (OR use 'Overview' button)",
                    "!swarm_profile - Swarm collective profile",
                ],
                "📚 GitHub Book": [
                    "!github_book [chapter] - Interactive book navigation (OR use 'GitHub Book' button)",
                    "!goldmines - High-value patterns (OR use 'Goldmines' button)",
                    "!book_stats - Comprehensive statistics",
                ],
                "📊 Status & Monitoring": [
                    "!status - View swarm status (OR use 'Swarm Status' button)",
                    "!monitor [start|stop|status] - Control status monitor (OR use 'Monitor' button)",
                ],
                "🔄 System Management": [
                    "!restart - Restart bot (OR use 'Restart Bot' button)",
                    "!shutdown - Shutdown bot (OR use 'Shutdown Bot' button)",
                    "!unstall <agent> - Unstall agent (OR use 'Unstall Agent' button)",
                    "!bump <agents> - Bump agents (OR use 'Bump Agents' button)",
                ],
                "🚀 Onboarding": [
                    "!soft_onboard <agents> - Soft onboard (OR use 'Soft Onboard' button)",
                    "!hard_onboard <agents> - Hard onboard (OR use 'Hard Onboard' button)",
                ],
                "🌊 Utilities": [
                    "!mermaid <code> - Render Mermaid diagram (OR use 'Mermaid' button)",
                    "!templates - Broadcast templates (OR use 'Templates' button)",
                    "!help - Interactive help menu (OR use 'Help' button)",
                ],
            }

            embed = discord.Embed(
                title="📋 All Available Commands",
                description=(
                    "**🎯 IMPORTANT: All commands are accessible via buttons in the Control Panel!**\n\n"
                    "**Use `!control` (or `!panel`, `!menu`) to open the Control Panel with all buttons.**\n\n"
                    "Commands listed below are for reference - buttons are preferred."
                ),
                color=discord.Color.blue(),
            )

            for category, commands in commands_by_category.items():
                embed.add_field(
                    name=category,
                    value="\n".join(commands),
                    inline=False,
                )

            embed.add_field(
                name="✅ Button Access",
                value=(
                    "**All features accessible via Control Panel buttons:**\n"
                    "• Message Agent\n"
                    "• Broadcast\n"
                    "• Swarm Status\n"
                    "• Tasks (swarm_tasks)\n"
                    "• GitHub Book\n"
                    "• Roadmap\n"
                    "• Excellence\n"
                    "• Overview\n"
                    "• Goldmines\n"
                    "• Templates\n"
                    "• Mermaid\n"
                    "• Monitor\n"
                    "• Help\n"
                    "• Restart/Shutdown\n"
                    "• Onboarding\n"
                    "• And more..."
                ),
                inline=False,
            )

            embed.set_footer(
                text="🐝 WE. ARE. SWARM. ⚡ Use buttons instead of commands when possible!"
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing all commands: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading commands")

    async def _handle_error(self, interaction: discord.Interaction, error: Exception, context: str = ""):
        """Handle interaction errors."""
        try:
            error_msg = f"❌ Error {context}: {error}" if context else f"❌ Error: {error}"
            if not interaction.response.is_done():
                await interaction.response.send_message(error_msg, ephemeral=True)
            else:
                await interaction.followup.send(error_msg, ephemeral=True)
        except Exception as followup_error:
            logger.error(
                f"Error sending error message: {followup_error}", exc_info=True)
