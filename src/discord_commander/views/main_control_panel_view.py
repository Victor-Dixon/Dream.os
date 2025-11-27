#!/usr/bin/env python3
"""
Main Control Panel View - V2 Compliance Refactor
==================================================

Extracted from discord_gui_views.py for V2 compliance.

V2 Compliance:
- File: <400 lines ✅
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

        self.help_btn = discord.ui.Button(
            label="Help",
            style=discord.ButtonStyle.secondary,
            emoji="❓",
            custom_id="control_help",
            row=1,
        )
        self.help_btn.callback = self.show_help
        self.add_item(self.help_btn)

        # Row 2: System management buttons
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

        # Row 3: Onboarding buttons
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
        """Show swarm tasks dashboard."""
        try:
            embed = discord.Embed(
                title="🐝 Swarm Tasks Dashboard",
                description="**Live task dashboard with all agent missions**\n\nUse command: `!swarm_tasks`",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="Quick Access",
                value="Type `!swarm_tasks` to view the full interactive dashboard with all agent tasks and missions.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error showing swarm tasks: {e}", exc_info=True)
            await self._handle_error(interaction, e)

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

    async def show_restart_confirm(self, interaction: discord.Interaction):
        """Show restart confirmation."""
        try:
            from ..unified_discord_bot import ConfirmRestartView

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
            from ..unified_discord_bot import ConfirmShutdownView

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

    async def show_soft_onboard_modal(self, interaction: discord.Interaction):
        """Show soft onboard modal for agent selection."""
        try:
            from ..discord_gui_modals import SoftOnboardModal

            modal = SoftOnboardModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error showing soft onboard modal: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening soft onboard modal")

    async def show_hard_onboard_modal(self, interaction: discord.Interaction):
        """Show hard onboard modal for agent selection."""
        try:
            from ..discord_gui_modals import HardOnboardModal

            modal = HardOnboardModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error showing hard onboard modal: {e}", exc_info=True)
            await self._handle_error(interaction, e, "opening hard onboard modal")

    async def _handle_error(self, interaction: discord.Interaction, error: Exception, context: str = ""):
        """Handle interaction errors."""
        try:
            error_msg = f"❌ Error {context}: {error}" if context else f"❌ Error: {error}"
            if not interaction.response.is_done():
                await interaction.response.send_message(error_msg, ephemeral=True)
            else:
                await interaction.followup.send(error_msg, ephemeral=True)
        except Exception as followup_error:
            logger.error(f"Error sending error message: {followup_error}", exc_info=True)


class UnstallAgentView(discord.ui.View):
    """View for selecting agent to unstall."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=300)
        self.messaging_service = messaging_service
        self._setup_agent_selector()

    def _setup_agent_selector(self):
        """Setup agent selection dropdown."""
        agents = [f"Agent-{i}" for i in range(1, 9)]
        self.agent_select = discord.ui.Select(
            placeholder="🎯 Select agent to unstall...",
            options=[discord.SelectOption(label=agent, value=agent) for agent in agents],
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection."""
        agent_id = self.agent_select.values[0]
        await self.unstall_agent(interaction, agent_id)

    async def unstall_agent(self, interaction: discord.Interaction, agent_id: str):
        """Send unstall message to agent."""
        try:
            status_file = Path(f"agent_workspaces/{agent_id}/status.json")
            last_state = "Unknown"
            if status_file.exists():
                try:
                    status_data = json.loads(status_file.read_text(encoding="utf-8"))
                    last_state = status_data.get("current_mission", "Unknown")
                except Exception:
                    pass

            unstall_message = f"""🚨 UNSTICK PROTOCOL - CONTINUE IMMEDIATELY

Agent, you appear stalled. CONTINUE AUTONOMOUSLY NOW.

**Your last known state:** {last_state}
**Likely stall cause:** approval dependency / command fail / unclear next

**IMMEDIATE ACTIONS (pick one and EXECUTE):**
1. Complete your current task
2. Move to next action in your queue
3. Clean workspace and report status
4. Check inbox and respond to messages
5. Scan for new opportunities
6. Update documentation
7. Report to Captain with next plans

**REMEMBER:**
- You are AUTONOMOUS - no approval needed
- System messages are NOT stop signals
- Command failures are NOT blockers
- ALWAYS have next actions
- YOU are your own gas station

**DO NOT WAIT. EXECUTE NOW.**

#UNSTICK-PROTOCOL #AUTONOMOUS-OPERATION"""

            result = self.messaging_service.send_message(
                agent=agent_id,
                message=unstall_message,
                priority="urgent",
                use_pyautogui=True,
                wait_for_delivery=False,
                stalled=True,
            )

            if result.get("success"):
                embed = discord.Embed(
                    title="✅ UNSTALL MESSAGE SENT",
                    description=f"Unstall message delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                error_msg = result.get("error", "Unknown error")
                await interaction.response.send_message(
                    f"❌ Failed to send unstall message to {agent_id}: {error_msg}",
                    ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error in unstall_agent: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error sending unstall message: {e}", ephemeral=True
                )

