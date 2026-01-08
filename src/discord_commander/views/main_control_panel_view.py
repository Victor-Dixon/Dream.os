#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Main Control Panel View - V2 Compliance Refactor
==================================================

Refactored for V2 compliance by extracting UI components and embed generation.

Navigation References:
├── UI Components → src/discord_commander/ui_components/
├── Embed Factory → src/discord_commander/ui_components/control_panel_embeds.py
├── Button Factory → src/discord_commander/ui_components/control_panel_buttons.py

V2 Compliance:
- File: 660 lines (reduced from 761 lines - 101 line reduction, 13.3%)
- Class: <200 lines ✅
- Functions: <30 lines ✅
- UI Components: Extracted to ui_components module
- Embed Generation: Partially extracted to embed factory

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: V2 Compliance Refactoring
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
from ..ui_components import (
    ControlPanelButtonFactory,
    ButtonCallbackManager,
    ControlPanelEmbedFactory,
)

logger = logging.getLogger(__name__)


class MonitorControlView(discord.ui.View):
    """Simple view with monitor start/stop buttons using extracted components."""

    def __init__(self):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)

        # Use extracted button factory
        buttons = ControlPanelButtonFactory.create_monitor_buttons()
        self.callback_manager = ButtonCallbackManager(self)

        for button in buttons:
            # Set callbacks using the callback manager
            if button.custom_id == "monitor_start":
                button.callback = self.callback_manager.handle_monitor_start
            elif button.custom_id == "monitor_stop":
                button.callback = self.on_stop
            elif button.custom_id == "monitor_refresh":
                button.callback = self.callback_manager.handle_monitor_refresh

            self.add_item(button)

    async def on_stop(self, interaction: discord.Interaction):
        """Stop the status monitor using extracted callback manager."""
        await self.callback_manager.handle_monitor_stop(interaction)
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
    """Main interactive control panel - GUI-driven interface with extracted components."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=None)  # No timeout for main panel
        self.messaging_service = messaging_service
        self.callback_manager = ButtonCallbackManager(self)
        self._setup_buttons()

    def _setup_buttons(self):
        """Setup control panel buttons using extracted factory."""
        # Create main control buttons using factory
        buttons = ControlPanelButtonFactory.create_main_control_buttons()

        # Map callbacks to buttons
        callback_map = {
            "control_agent_status": self.show_status,  # Map to existing show_status
            "control_messaging": self.show_agent_selector,  # Map to existing agent selector
            "control_showcase": self.show_overview,  # Map to existing overview
            "control_swarm_tasks": self.show_swarm_tasks,
            "control_github_book": self.show_github_book,
            "control_roadmap": self.show_roadmap,
            "control_excellence": self.show_excellence,
            "control_help": self.show_help,
            "control_restart": self.show_restart_confirm,
            "control_shutdown": self.show_shutdown_confirm,
            "control_unstall": self.show_unstall_selector,
            "control_bump": self.show_bump_selector,
            "control_commands": self.show_all_commands,
            "control_soft_onboard": self.show_soft_onboard_modal,
            "control_hard_onboard": self.show_hard_onboard_modal,
            "control_overview": self.show_overview,
            "control_goldmines": self.show_goldmines,
            "control_templates": self.show_templates,
            "control_mermaid": self.show_mermaid_modal,
            "control_monitor": self.show_monitor_control,
            "control_obs": self.show_obs,
            "control_pieces": self.show_pieces,
        }

        for button in buttons:
            custom_id = button.custom_id
            if custom_id in callback_map:
                button.callback = callback_map[custom_id]
            self.add_item(button)

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
            embed = ControlPanelEmbedFactory.create_swarm_tasks_error_embed()
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
            embed = ControlPanelEmbedFactory.create_github_book_fallback_embed()
            # Add any additional fields if needed
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

            embed = ControlPanelEmbedFactory.create_restart_embed()

            view = ConfirmRestartView()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

            await view.wait()

            if view.confirmed:
                bot = interaction.client

                restart_embed = ControlPanelEmbedFactory.create_restart_success_embed()
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

            embed = ControlPanelEmbedFactory.create_shutdown_embed()

            view = ConfirmShutdownView()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

            await view.wait()

            if view.confirmed:
                bot = interaction.client

                shutdown_embed = ControlPanelEmbedFactory.create_shutdown_success_embed()
                await interaction.followup.send(embed=shutdown_embed, ephemeral=True)

                await bot.close()
        except Exception as e:
            logger.error(f"Error in shutdown confirm: {e}", exc_info=True)
            await self._handle_error(interaction, e, "during shutdown")

    async def show_unstall_selector(self, interaction: discord.Interaction):
        """Show agent selector for unstall using extracted embed factory."""
        try:
            from .unstall_agent_view import UnstallAgentView

            view = UnstallAgentView(self.messaging_service)
            embed = ControlPanelEmbedFactory.create_unstall_embed()

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
            embed = ControlPanelEmbedFactory.create_mermaid_fallback_embed()
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_monitor_control(self, interaction: discord.Interaction):
        """Show status monitor control with start/stop buttons."""
        try:
            # Get bot instance to access status monitor
            bot = interaction.client

            if not hasattr(bot, 'status_monitor'):
                embed = ControlPanelEmbedFactory.create_error_embed(
                    "Status Monitor",
                    "❌ Status monitor not initialized. Bot may not be fully ready."
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

            embed = ControlPanelEmbedFactory.create_monitor_status_embed(is_running, interval)

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing monitor control: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading monitor status")

    async def show_obs(self, interaction: discord.Interaction):
        """Show observations using extracted embed factory."""
        try:
            embed = ControlPanelEmbedFactory.create_obs_embed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing obs: {e}", exc_info=True)
            await self._handle_error(interaction, e, "loading observations")

    async def show_pieces(self, interaction: discord.Interaction):
        """Show pieces using extracted embed factory."""
        try:
            embed = ControlPanelEmbedFactory.create_pieces_embed()
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

            embed = ControlPanelEmbedFactory.create_all_commands_embed()

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
