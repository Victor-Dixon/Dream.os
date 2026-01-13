#!/usr/bin/env python3
"""
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
Main Control Panel View - Discord GUI Components
===============================================

Main control panel view for Discord bot interface.

<<<<<<< HEAD
<!-- SSOT Domain: discord -->

Navigation References:
├── Related Files:
│   ├── GUI Controller → discord_gui_controller.py
│   ├── UI Components → ui_components/
│   ├── Views Package → __init__.py
│   └── Discord Service → discord_service.py
├── Documentation:
│   └── Discord GUI → README_DISCORD_GUI.md
└── Testing:
    └── View Tests → tests/discord/test_discord_views.py

Classes:
- MainControlPanelView: Main control interface for Discord bot
"""

import discord
from typing import Optional, Dict, Any, List

from ..ui_components.control_panel_buttons import ControlPanelButtonFactory
from ..ui_components.control_panel_embeds import ControlPanelEmbedFactory

try:
    import discord
=======
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
<!-- SSOT Domain: discord -->

Navigation References:
├── Related Files:
│   ├── GUI Controller → discord_gui_controller.py
│   ├── UI Components → ui_components/
│   ├── Views Package → __init__.py
│   └── Discord Service → discord_service.py
├── Documentation:
│   └── Discord GUI → README_DISCORD_GUI.md
└── Testing:
    └── View Tests → tests/discord/test_discord_views.py

Classes:
- MainControlPanelView: Main control interface for Discord bot
"""

import discord
from typing import Optional, Dict, Any, List

from ..ui_components.control_panel_buttons import ControlPanelButtonFactory
from ..ui_components.control_panel_embeds import ControlPanelEmbedFactory

try:
    import discord
<<<<<<< HEAD
    from discord.ext import commands
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

<<<<<<< HEAD
<<<<<<< HEAD

class MainControlPanelView(discord.ui.View if DISCORD_AVAILABLE else object):
    """
    Main control panel view for Discord bot interface.

    Navigation:
    ├── Uses: ControlPanelButtonFactory, ControlPanelEmbedFactory
    ├── Manages: Bot control, agent messaging, monitoring
    └── Related: Discord GUI controller, status monitoring
    """

    def __init__(self, bot=None, timeout: float = 300.0):
        """Initialize the main control panel view."""
        super().__init__(timeout=timeout) if DISCORD_AVAILABLE else super().__init__()
        self.bot = bot

        # Initialize UI components using factories
        self._setup_control_buttons()
        self._setup_monitoring_buttons()

    def _setup_control_buttons(self):
        """
        Setup control buttons using factory.

        Navigation:
        ├── Uses: ControlPanelButtonFactory
        └── Related: Agent messaging, bot control
        """
        # Message agent button
        self.msg_agent_btn = ControlPanelButtonFactory.create_message_agent_button()
        self.add_item(self.msg_agent_btn)

        # Main control button
        self.main_control_btn = ControlPanelButtonFactory.create_main_control_button()
        self.add_item(self.main_control_btn)

        # Status monitor button
        self.monitor_btn = ControlPanelButtonFactory.create_monitor_button()
        self.add_item(self.monitor_btn)

    def _setup_monitoring_buttons(self):
        """
        Setup monitoring buttons using factory.

        Navigation:
        ├── Uses: ControlPanelButtonFactory
        └── Related: System monitoring, status display
        """
        # System status button
        self.status_btn = ControlPanelButtonFactory.create_status_button(
            callback=self.show_system_status
        )
        self.add_item(self.status_btn)

        # Agent status button
        self.agent_status_btn = ControlPanelButtonFactory.create_agent_status_button(
            callback=self.show_agent_status
        )
        self.add_item(self.agent_status_btn)

    async def show_agent_selector(self, interaction: discord.Interaction):
        """
        Show agent selection interface.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Agent messaging workflow
        """
        embed = ControlPanelEmbedFactory.create_agent_selector_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_main_control(self, interaction: discord.Interaction):
        """
        Show main control interface.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Bot management, system control
        """
        embed = ControlPanelEmbedFactory.create_main_control_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def toggle_monitor(self, interaction: discord.Interaction):
        """
        Toggle monitoring status.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Status monitoring, system health
        """
        embed = ControlPanelEmbedFactory.create_monitor_started_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_system_status(self, interaction: discord.Interaction):
        """
        Show system status information.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: System monitoring, health checks
        """
        embed = ControlPanelEmbedFactory.create_system_status_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_agent_status(self, interaction: discord.Interaction):
        """
        Show agent status information.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Agent monitoring, swarm status
        """
        embed = ControlPanelEmbedFactory.create_agent_status_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        """
        Handle view interaction errors.

        Navigation:
        ├── Related: Error handling, user feedback
        └── Uses: Discord interaction error handling
        """
        embed = ControlPanelEmbedFactory.create_error_embed(str(error))
        try:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.InteractionResponded:
            await interaction.followup.send(embed=embed, ephemeral=True)
=======
from src.services.messaging_infrastructure import ConsolidatedMessagingService
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

class MainControlPanelView(discord.ui.View if DISCORD_AVAILABLE else object):
    """
    Main control panel view for Discord bot interface.

    Navigation:
    ├── Uses: ControlPanelButtonFactory, ControlPanelEmbedFactory
    ├── Manages: Bot control, agent messaging, monitoring
    └── Related: Discord GUI controller, status monitoring
    """

    def __init__(self, bot=None, timeout: float = 300.0):
        """Initialize the main control panel view."""
        super().__init__(timeout=timeout) if DISCORD_AVAILABLE else super().__init__()
        self.bot = bot

        # Initialize UI components using factories
        self._setup_control_buttons()
        self._setup_monitoring_buttons()

    def _setup_control_buttons(self):
        """
        Setup control buttons using factory.

        Navigation:
        ├── Uses: ControlPanelButtonFactory
        └── Related: Agent messaging, bot control
        """
        # Message agent button
        self.msg_agent_btn = ControlPanelButtonFactory.create_message_agent_button(
            callback=self.show_agent_selector
        )
        self.add_item(self.msg_agent_btn)

        # Main control button
        self.main_control_btn = ControlPanelButtonFactory.create_main_control_button(
            callback=self.show_main_control
        )
        self.add_item(self.main_control_btn)

        # Status monitor button
        self.monitor_btn = ControlPanelButtonFactory.create_monitor_button(
            callback=self.toggle_monitor
        )
        self.add_item(self.monitor_btn)

    def _setup_monitoring_buttons(self):
        """
        Setup monitoring buttons using factory.

        Navigation:
        ├── Uses: ControlPanelButtonFactory
        └── Related: System monitoring, status display
        """
        # System status button
        self.status_btn = ControlPanelButtonFactory.create_status_button(
            callback=self.show_system_status
        )
        self.add_item(self.status_btn)

        # Agent status button
        self.agent_status_btn = ControlPanelButtonFactory.create_agent_status_button(
            callback=self.show_agent_status
        )
        self.add_item(self.agent_status_btn)

    async def show_agent_selector(self, interaction: discord.Interaction):
        """
        Show agent selection interface.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Agent messaging workflow
        """
        embed = ControlPanelEmbedFactory.create_agent_selector_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_main_control(self, interaction: discord.Interaction):
        """
        Show main control interface.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Bot management, system control
        """
        embed = ControlPanelEmbedFactory.create_main_control_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def toggle_monitor(self, interaction: discord.Interaction):
        """
        Toggle monitoring status.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Status monitoring, system health
        """
        embed = ControlPanelEmbedFactory.create_monitor_started_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_system_status(self, interaction: discord.Interaction):
        """
        Show system status information.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: System monitoring, health checks
        """
        embed = ControlPanelEmbedFactory.create_system_status_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_agent_status(self, interaction: discord.Interaction):
        """
        Show agent status information.

        Navigation:
        ├── Uses: ControlPanelEmbedFactory
        └── Related: Agent monitoring, swarm status
        """
        embed = ControlPanelEmbedFactory.create_agent_status_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        """
        Handle view interaction errors.

        Navigation:
        ├── Related: Error handling, user feedback
        └── Uses: Discord interaction error handling
        """
        embed = ControlPanelEmbedFactory.create_error_embed(str(error))
        try:
            await interaction.response.send_message(embed=embed, ephemeral=True)
<<<<<<< HEAD

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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        except discord.InteractionResponded:
            await interaction.followup.send(embed=embed, ephemeral=True)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
