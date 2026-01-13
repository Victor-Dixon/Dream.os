#!/usr/bin/env python3
"""
Main Control Panel View - Discord GUI Components
===============================================

Main control panel view for Discord bot interface.

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

from ..ui_components.control_panel_embeds import ControlPanelEmbedFactory

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None


class MessageAgentButton(discord.ui.Button if DISCORD_AVAILABLE else object):
    """Custom button for messaging agents."""

    def __init__(self, view_instance):
        super().__init__(
            label="Message Agent",
            style=discord.ButtonStyle.primary,
            emoji="💬",
            custom_id="message_agent",
            row=0,
        ) if DISCORD_AVAILABLE else super().__init__()
        self.view_instance = view_instance

    async def callback(self, interaction: discord.Interaction):
        """Handle button click."""
        if hasattr(self.view_instance, 'show_agent_selector'):
            await self.view_instance.show_agent_selector(interaction)


class MainControlButton(discord.ui.Button if DISCORD_AVAILABLE else object):
    """Custom button for main control panel."""

    def __init__(self, view_instance):
        super().__init__(
            label="Main Control",
            style=discord.ButtonStyle.primary,
            emoji="🎛️",
            custom_id="main_control",
            row=0,
        ) if DISCORD_AVAILABLE else super().__init__()
        self.view_instance = view_instance

    async def callback(self, interaction: discord.Interaction):
        """Handle button click."""
        if hasattr(self.view_instance, 'show_main_control'):
            await self.view_instance.show_main_control(interaction)


class MonitorButton(discord.ui.Button if DISCORD_AVAILABLE else object):
    """Custom button for monitoring."""

    def __init__(self, view_instance):
        super().__init__(
            label="Monitor",
            style=discord.ButtonStyle.secondary,
            emoji="📊",
            custom_id="monitor",
            row=0,
        ) if DISCORD_AVAILABLE else super().__init__()
        self.view_instance = view_instance

    async def callback(self, interaction: discord.Interaction):
        """Handle button click."""
        if hasattr(self.view_instance, 'toggle_monitor'):
            await self.view_instance.toggle_monitor(interaction)


class StatusButton(discord.ui.Button if DISCORD_AVAILABLE else object):
    """Custom button for system status."""

    def __init__(self, view_instance):
        super().__init__(
            label="Status",
            style=discord.ButtonStyle.secondary,
            emoji="📈",
            custom_id="status",
            row=0,
        ) if DISCORD_AVAILABLE else super().__init__()
        self.view_instance = view_instance

    async def callback(self, interaction: discord.Interaction):
        """Handle button click."""
        if hasattr(self.view_instance, 'show_system_status'):
            await self.view_instance.show_system_status(interaction)


class AgentStatusButton(discord.ui.Button if DISCORD_AVAILABLE else object):
    """Custom button for agent status."""

    def __init__(self, view_instance):
        super().__init__(
            label="Agent Status",
            style=discord.ButtonStyle.primary,
            emoji="👥",
            custom_id="agent_status",
            row=0,
        ) if DISCORD_AVAILABLE else super().__init__()
        self.view_instance = view_instance

    async def callback(self, interaction: discord.Interaction):
        """Handle button click."""
        if hasattr(self.view_instance, 'show_agent_status'):
            await self.view_instance.show_agent_status(interaction)


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
        Setup control buttons using custom button classes.

        Navigation:
        ├── Uses: Custom button classes
        └── Related: Agent messaging, bot control
        """
        # Message agent button
        self.msg_agent_btn = MessageAgentButton(self)
        self.add_item(self.msg_agent_btn)

        # Main control button
        self.main_control_btn = MainControlButton(self)
        self.add_item(self.main_control_btn)

        # Status monitor button
        self.monitor_btn = MonitorButton(self)
        self.add_item(self.monitor_btn)

    def _setup_monitoring_buttons(self):
        """
        Setup monitoring buttons using custom button classes.

        Navigation:
        ├── Uses: Custom button classes
        └── Related: System monitoring, status display
        """
        # System status button
        self.status_btn = StatusButton(self)
        self.add_item(self.status_btn)

        # Agent status button
        self.agent_status_btn = AgentStatusButton(self)
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
