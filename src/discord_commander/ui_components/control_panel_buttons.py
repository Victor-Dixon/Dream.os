#!/usr/bin/env python3
"""
Control Panel UI Components - V2 Compliance Extraction
======================================================

Extracted UI components from main_control_panel_view.py for V2 compliance.

<!-- SSOT Domain: discord -->

Navigation References:
├── Main View → src/discord_commander/views/main_control_panel_view.py
├── UI Components → src/discord_commander/discord_ui_components.py
├── Embed Factory → src/discord_commander/embed_factory.py

Features:
- Reusable button components for control panels
- Consistent styling and behavior
- Callback management
- Row-based layout organization

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: V2 Compliance Refactoring
"""

import logging
from typing import Optional, Callable, Any, Dict, List
from dataclasses import dataclass

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


@dataclass
class ButtonConfig:
    """Configuration for a Discord UI button."""
    label: str
    style: 'discord.ButtonStyle'
    emoji: str
    custom_id: str
    row: int
    callback: Optional[Callable] = None
    disabled: bool = False
    url: Optional[str] = None


class ControlPanelButtonFactory:
    """
    Factory for creating control panel buttons with consistent styling.

    Extracts button creation logic from main control panel view for V2 compliance.
    """

    @staticmethod
    def create_monitor_buttons() -> List['discord.ui.Button']:
        """Create monitor control buttons (Start, Stop, Refresh)."""
        buttons = []

        # Start Monitor button
        start_btn = discord.ui.Button(
            label="Start Monitor",
            style=discord.ButtonStyle.success,
            emoji="▶️",
            custom_id="monitor_start",
            row=0,
        )

        # Stop Monitor button
        stop_btn = discord.ui.Button(
            label="Stop Monitor",
            style=discord.ButtonStyle.danger,
            emoji="⏸️",
            custom_id="monitor_stop",
            row=0,
        )

        # Refresh button
        refresh_btn = discord.ui.Button(
            label="Refresh Status",
            style=discord.ButtonStyle.secondary,
            emoji="🔄",
            custom_id="monitor_refresh",
            row=0,
        )

        buttons.extend([start_btn, stop_btn, refresh_btn])
        return buttons

    @staticmethod
    def create_main_control_buttons() -> List['discord.ui.Button']:
        """Create main control panel buttons organized by rows."""

        buttons = []

        # Row 0: Primary actions
        agent_status_btn = discord.ui.Button(
            label="Agent Status",
            style=discord.ButtonStyle.primary,
            emoji="📊",
            custom_id="control_agent_status",
            row=0,
        )

        messaging_btn = discord.ui.Button(
            label="Messaging",
            style=discord.ButtonStyle.primary,
            emoji="💬",
            custom_id="control_messaging",
            row=0,
        )

        showcase_btn = discord.ui.Button(
            label="Showcase",
            style=discord.ButtonStyle.primary,
            emoji="🎪",
            custom_id="control_showcase",
            row=0,
        )

        buttons.extend([agent_status_btn, messaging_btn, showcase_btn])

        # Row 1: Secondary actions
        swarm_tasks_btn = discord.ui.Button(
            label="Tasks",
            style=discord.ButtonStyle.primary,
            emoji="🐝",
            custom_id="control_swarm_tasks",
            row=1,
        )

        github_book_btn = discord.ui.Button(
            label="GitHub Book",
            style=discord.ButtonStyle.primary,
            emoji="📚",
            custom_id="control_github_book",
            row=1,
        )

        roadmap_btn = discord.ui.Button(
            label="Roadmap",
            style=discord.ButtonStyle.primary,
            emoji="🗺️",
            custom_id="control_roadmap",
            row=1,
        )

        excellence_btn = discord.ui.Button(
            label="Excellence",
            style=discord.ButtonStyle.primary,
            emoji="🏆",
            custom_id="control_excellence",
            row=1,
        )

        help_btn = discord.ui.Button(
            label="Help",
            style=discord.ButtonStyle.secondary,
            emoji="❓",
            custom_id="control_help",
            row=1,
        )

        buttons.extend([swarm_tasks_btn, github_book_btn, roadmap_btn, excellence_btn, help_btn])

        # Row 2: System management buttons
        restart_btn = discord.ui.Button(
            label="Restart Bot",
            style=discord.ButtonStyle.danger,
            emoji="🔄",
            custom_id="control_restart",
            row=2,
        )

        shutdown_btn = discord.ui.Button(
            label="Shutdown Bot",
            style=discord.ButtonStyle.danger,
            emoji="🛑",
            custom_id="control_shutdown",
            row=2,
        )

        unstall_btn = discord.ui.Button(
            label="Unstall Agent",
            style=discord.ButtonStyle.danger,
            emoji="🚨",
            custom_id="control_unstall",
            row=2,
        )

        bump_btn = discord.ui.Button(
            label="Bump Agents",
            style=discord.ButtonStyle.secondary,
            emoji="👆",
            custom_id="control_bump",
            row=2,
        )

        commands_btn = discord.ui.Button(
            label="All Commands",
            style=discord.ButtonStyle.secondary,
            emoji="📋",
            custom_id="control_commands",
            row=2,
        )

        buttons.extend([restart_btn, shutdown_btn, unstall_btn, bump_btn, commands_btn])

        # Row 3: Onboarding and additional showcase buttons
        soft_onboard_btn = discord.ui.Button(
            label="Soft Onboard",
            style=discord.ButtonStyle.success,
            emoji="🚀",
            custom_id="control_soft_onboard",
            row=3,
        )

        hard_onboard_btn = discord.ui.Button(
            label="Hard Onboard",
            style=discord.ButtonStyle.success,
            emoji="🐝",
            custom_id="control_hard_onboard",
            row=3,
        )

        overview_btn = discord.ui.Button(
            label="Overview",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="control_overview",
            row=3,
        )

        goldmines_btn = discord.ui.Button(
            label="Goldmines",
            style=discord.ButtonStyle.primary,
            emoji="💎",
            custom_id="control_goldmines",
            row=3,
        )

        buttons.extend([soft_onboard_btn, hard_onboard_btn, overview_btn, goldmines_btn])

        # Row 4: Additional tools and utilities
        templates_btn = discord.ui.Button(
            label="Templates",
            style=discord.ButtonStyle.primary,
            emoji="📝",
            custom_id="control_templates",
            row=4,
        )

        mermaid_btn = discord.ui.Button(
            label="Mermaid",
            style=discord.ButtonStyle.primary,
            emoji="🌊",
            custom_id="control_mermaid",
            row=4,
        )

        monitor_btn = discord.ui.Button(
            label="Monitor",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="control_monitor",
            row=4,
        )

        obs_btn = discord.ui.Button(
            label="Observations",
            style=discord.ButtonStyle.secondary,
            emoji="👁️",
            custom_id="control_obs",
            row=4,
        )

        pieces_btn = discord.ui.Button(
            label="Pieces",
            style=discord.ButtonStyle.secondary,
            emoji="🧩",
            custom_id="control_pieces",
            row=4,
        )

        buttons.extend([templates_btn, mermaid_btn, monitor_btn, obs_btn, pieces_btn])

        return buttons

    @staticmethod
    def create_confirmation_buttons(action_type: str) -> List['discord.ui.Button']:
        """Create confirmation buttons for dangerous actions."""

        confirm_btn = discord.ui.Button(
            label=f"Confirm {action_type}",
            style=discord.ButtonStyle.danger,
            emoji="✅",
            custom_id=f"confirm_{action_type.lower()}",
            row=0,
        )

        cancel_btn = discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.secondary,
            emoji="❌",
            custom_id=f"cancel_{action_type.lower()}",
            row=0,
        )

        return [confirm_btn, cancel_btn]

    @staticmethod
<<<<<<< HEAD
    def create_message_agent_button() -> 'discord.ui.Button':
        """Create a message agent button."""
        return discord.ui.Button(
            label="Message Agent",
            style=discord.ButtonStyle.secondary,
            emoji="📨",
            custom_id="message_agent",
            row=0
        )

    @staticmethod
    def create_main_control_button() -> 'discord.ui.Button':
        """Create a main control button."""
        return discord.ui.Button(
            label="Main Control",
            style=discord.ButtonStyle.primary,
            emoji="⚙️",
            custom_id="main_control",
            row=0
        )

    @staticmethod
    def create_monitor_button() -> 'discord.ui.Button':
        """Create a monitor button."""
        return discord.ui.Button(
            label="Monitor",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="monitor",
            row=0
        )

    @staticmethod
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    def create_navigation_buttons() -> List['discord.ui.Button']:
        """Create navigation buttons for paginated views."""

        prev_btn = discord.ui.Button(
            label="Previous",
            style=discord.ButtonStyle.secondary,
            emoji="⬅️",
            custom_id="nav_previous",
            row=0,
        )

        next_btn = discord.ui.Button(
            label="Next",
            style=discord.ButtonStyle.secondary,
            emoji="➡️",
            custom_id="nav_next",
            row=0,
        )

        return [prev_btn, next_btn]


class ButtonCallbackManager:
    """
    Manages button callbacks for control panel views.

    Provides centralized callback handling to reduce code duplication.
    """

    def __init__(self, view_instance):
        self.view = view_instance
        self.messaging_service = getattr(view_instance, 'messaging_service', None)

    async def handle_monitor_start(self, interaction: 'discord.Interaction') -> None:
        """Handle monitor start button callback."""
        try:
            bot = interaction.client
            if hasattr(bot, "status_monitor"):
                bot.status_monitor.start_monitoring()
                embed = self._create_success_embed(
                    "📊 Monitor Started",
                    "✅ Status monitor started! Checking every 15 seconds."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = self._create_error_embed(
                    "📊 Monitor Error",
                    "⚠️ Status monitor not initialized yet."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error starting monitor: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    async def handle_monitor_stop(self, interaction: 'discord.Interaction') -> None:
        """Handle monitor stop button callback."""
        try:
            bot = interaction.client
            if hasattr(bot, "status_monitor"):
                bot.status_monitor.stop_monitoring()
                embed = self._create_success_embed(
                    "📊 Monitor Stopped",
                    "⏸️ Status monitor stopped."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = self._create_error_embed(
                    "📊 Monitor Error",
                    "⚠️ Status monitor not available."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error stopping monitor: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    async def handle_monitor_refresh(self, interaction: 'discord.Interaction') -> None:
        """Handle monitor refresh button callback."""
        try:
            bot = interaction.client

            if not hasattr(bot, 'status_monitor'):
                embed = self._create_error_embed(
                    "📊 Status Monitor",
                    "❌ Status monitor not initialized."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # Get current status
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
                description=f"**Status:** {status_text}\n**Check Interval:** {interval} seconds\n\nStatus refreshed successfully.",
                color=status_color,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error refreshing monitor status: {e}", exc_info=True)
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    def _create_success_embed(self, title: str, description: str) -> 'discord.Embed':
        """Create a success embed."""
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green(),
        )

    def _create_error_embed(self, title: str, description: str) -> 'discord.Embed':
        """Create an error embed."""
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.red(),
        )


# Convenience functions for backward compatibility
def create_monitor_buttons():
    """Backward compatibility function."""
    return ControlPanelButtonFactory.create_monitor_buttons()


def create_main_control_buttons():
    """Backward compatibility function."""
    return ControlPanelButtonFactory.create_main_control_buttons()