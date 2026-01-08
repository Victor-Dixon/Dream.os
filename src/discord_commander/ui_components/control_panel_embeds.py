#!/usr/bin/env python3
"""
Control Panel Embed Factory - V2 Compliance Extraction
======================================================

Extracted embed generation logic from main_control_panel_view.py for V2 compliance.

<!-- SSOT Domain: discord -->

Navigation References:
├── Main View → src/discord_commander/views/main_control_panel_view.py
├── Embed Factory → src/discord_commander/embed_factory.py
├── UI Components → src/discord_commander/ui_components/control_panel_buttons.py

Features:
- Centralized embed creation for control panel views
- Consistent styling and theming
- Reusable embed templates
- Error handling and fallbacks

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: V2 Compliance Refactoring
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


class ControlPanelEmbedFactory:
    """
    Factory for creating control panel embeds with consistent styling.

    Extracts embed generation logic from main control panel view for V2 compliance.
    """

    # Standard colors for different embed types
    COLORS = {
        'success': discord.Color.green(),
        'error': discord.Color.red(),
        'warning': discord.Color.orange(),
        'info': discord.Color.blue(),
        'primary': discord.Color.blurple(),
        'secondary': discord.Color.greyple(),
        'danger': discord.Color.red(),
    }

    @staticmethod
    def create_monitor_status_embed(is_running: bool, interval: int = 15) -> 'discord.Embed':
        """Create monitor status embed."""
        status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
        status_color = ControlPanelEmbedFactory.COLORS['success'] if is_running else ControlPanelEmbedFactory.COLORS['error']

        embed = discord.Embed(
            title="📊 Status Change Monitor",
            description=f"**Status:** {status_text}\n**Check Interval:** {interval} seconds\n\nUse buttons below to start/stop the monitor.",
            color=status_color,
        )

        embed.set_footer(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        return embed

    @staticmethod
    def create_monitor_action_embed(action: str, success: bool, message: str = None) -> 'discord.Embed':
        """Create monitor action result embed."""
        title = f"📊 Monitor {action.title()}"
        color = ControlPanelEmbedFactory.COLORS['success'] if success else ControlPanelEmbedFactory.COLORS['error']

        description = message or f"✅ Monitor {action}{'d' if not action.endswith('e') else 'd'} successfully!" if success else f"❌ Failed to {action} monitor."

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )

        return embed

    @staticmethod
    def create_confirmation_embed(action: str, description: str, warning: str = None) -> 'discord.Embed':
        """Create confirmation embed for dangerous actions."""
        embed = discord.Embed(
            title=f"⚠️ Confirm {action.title()}",
            description=description,
            color=ControlPanelEmbedFactory.COLORS['warning'],
        )

        if warning:
            embed.add_field(
                name="⚠️ Warning",
                value=warning,
                inline=False,
            )

        embed.add_field(
            name="Confirmation Required",
            value="This action cannot be undone. Use the buttons below to confirm or cancel.",
            inline=False,
        )

        return embed

    @staticmethod
    def create_restart_embed() -> 'discord.Embed':
        """Create restart confirmation embed."""
        embed = discord.Embed(
            title="🔄 Restart Requested",
            description="Bot will shutdown and restart. Continue?",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )
        return embed

    @staticmethod
    def create_restart_success_embed() -> 'discord.Embed':
        """Create restart success embed."""
        embed = discord.Embed(
            title="🔄 Bot Restarting",
            description="Shutting down... Will be back in 5-10 seconds!",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )
        return embed

    @staticmethod
    def create_shutdown_embed() -> 'discord.Embed':
        """Create shutdown confirmation embed."""
        embed = discord.Embed(
            title="🛑 Shutdown Requested",
            description="Are you sure you want to shutdown the bot?",
            color=ControlPanelEmbedFactory.COLORS['danger'],
        )
        return embed

    @staticmethod
    def create_shutdown_success_embed() -> 'discord.Embed':
        """Create shutdown success embed."""
        embed = discord.Embed(
            title="👋 Bot Shutting Down",
            description="Gracefully closing connections...",
            color=ControlPanelEmbedFactory.COLORS['warning'],
        )
        return embed

    @staticmethod
    def create_unstall_embed() -> 'discord.Embed':
        """Create unstall agent embed."""
        embed = discord.Embed(
            title="🚨 Unstall Agent",
            description="Select an agent to send unstall message",
            color=ControlPanelEmbedFactory.COLORS['warning'],
        )
        return embed

    @staticmethod
    def create_bump_embed() -> 'discord.Embed':
        """Create bump agents embed."""
        embed = discord.Embed(
            title="👆 Bump Agents",
            description="Select agents to bump in the channel",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )
        return embed

    @staticmethod
    def create_templates_embed() -> 'discord.Embed':
        """Create broadcast templates embed."""
        embed = discord.Embed(
            title="📝 Broadcast Templates",
            description="Select a template to send a pre-configured message",
            color=ControlPanelEmbedFactory.COLORS['primary'],
        )

        embed.add_field(
            name="Available Templates",
            value="• Swarm Updates\n• Status Reports\n• Coordination Messages\n• Achievement Announcements",
            inline=False,
        )

        return embed

    @staticmethod
    def create_mermaid_embed() -> 'discord.Embed':
        """Create Mermaid diagram embed."""
        embed = discord.Embed(
            title="🌊 Mermaid Diagram",
            description="**Create Mermaid diagrams**\n\nUse command: `!mermaid <diagram_code>`",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )

        embed.add_field(
            name="Example",
            value="`!mermaid graph TD; A-->B; B-->C;`",
            inline=False,
        )

        embed.add_field(
            name="Supported Types",
            value="• Flowcharts\n• Sequence diagrams\n• Gantt charts\n• State diagrams",
            inline=False,
        )

        return embed

    @staticmethod
    def create_mermaid_fallback_embed() -> 'discord.Embed':
        """Create Mermaid diagram fallback embed when modal not available."""
        embed = discord.Embed(
            title="🌊 Mermaid Diagram",
            description="**Create Mermaid diagrams**\n\nUse command: `!mermaid <diagram_code>`",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )

        embed.add_field(
            name="Example",
            value="`!mermaid graph TD; A-->B; B-->C;`",
            inline=False,
        )

        return embed

    @staticmethod
    def create_obs_embed() -> 'discord.Embed':
        """Create observations embed."""
        embed = discord.Embed(
            title="👁️ Observations",
            description="**Observations feature**\n\nThis feature is being implemented.",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )

        embed.add_field(
            name="Status",
            value="Feature in development",
            inline=False,
        )

        embed.add_field(
            name="Coming Soon",
            value="• Real-time activity monitoring\n• Pattern recognition\n• Automated insights",
            inline=False,
        )

        return embed

    @staticmethod
    def create_pieces_embed() -> 'discord.Embed':
        """Create pieces embed."""
        embed = discord.Embed(
            title="🧩 Pieces",
            description="**Pieces feature**\n\nThis feature is being implemented.",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )

        embed.add_field(
            name="Status",
            value="Feature in development",
            inline=False,
        )

        embed.add_field(
            name="Coming Soon",
            value="• Modular component system\n• Dynamic assembly\n• Reusable parts",
            inline=False,
        )

        return embed

    @staticmethod
    def create_error_embed(error_type: str, message: str, details: str = None) -> 'discord.Embed':
        """Create error embed."""
        embed = discord.Embed(
            title=f"❌ {error_type}",
            description=message,
            color=ControlPanelEmbedFactory.COLORS['error'],
        )

        if details:
            embed.add_field(
                name="Details",
                value=details,
                inline=False,
            )

        embed.set_footer(text=f"Error occurred at: {datetime.now().strftime('%H:%M:%S')}")

        return embed

    @staticmethod
    def create_success_embed(title: str, message: str) -> 'discord.Embed':
        """Create success embed."""
        embed = discord.Embed(
            title=f"✅ {title}",
            description=message,
            color=ControlPanelEmbedFactory.COLORS['success'],
        )

        return embed

    @staticmethod
    def create_info_embed(title: str, message: str, fields: List[Dict[str, Any]] = None) -> 'discord.Embed':
        """Create informational embed."""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=message,
            color=ControlPanelEmbedFactory.COLORS['info'],
        )

        if fields:
            for field in fields:
                embed.add_field(
                    name=field.get('name', 'Field'),
                    value=field.get('value', ''),
                    inline=field.get('inline', False),
                )

        return embed

    @staticmethod
    def create_help_embed() -> 'discord.Embed':
        """Create help embed."""
        embed = discord.Embed(
            title="❓ Control Panel Help",
            description="**Main Control Panel Overview**\n\nThis panel provides access to all bot management and monitoring functions.",
            color=ControlPanelEmbedFactory.COLORS['primary'],
        )

        embed.add_field(
            name="📊 Agent Status",
            value="Monitor and manage all agents in the swarm",
            inline=True,
        )

        embed.add_field(
            name="💬 Messaging",
            value="Send messages and coordinate with agents",
            inline=True,
        )

        embed.add_field(
            name="🎪 Showcase",
            value="View agent capabilities and achievements",
            inline=True,
        )

        embed.add_field(
            name="🐝 Tasks",
            value="View and manage swarm tasks",
            inline=True,
        )

        embed.add_field(
            name="📚 GitHub Book",
            value="Browse repository documentation",
            inline=True,
        )

        embed.add_field(
            name="🗺️ Roadmap",
            value="View development roadmap and milestones",
            inline=True,
        )

        embed.add_field(
            name="🔄 System Controls",
            value="Restart, shutdown, and monitor bot status",
            inline=False,
        )

        embed.set_footer(text="Use the buttons below to navigate different functions")

        return embed

    @staticmethod
    def create_swarm_tasks_error_embed() -> 'discord.Embed':
        """Create swarm tasks error embed."""
        embed = discord.Embed(
            title="🐝 Swarm Tasks Dashboard",
            description="**Error loading interactive dashboard**\n\nYou can use command: `!swarm_tasks`",
            color=ControlPanelEmbedFactory.COLORS['warning'],
        )
        return embed

    @staticmethod
    def create_github_book_fallback_embed() -> 'discord.Embed':
        """Create GitHub book fallback embed."""
        embed = discord.Embed(
            title="📚 GitHub Book Viewer",
            description="**Interactive book navigation with chapters**\n\nUse command: `!github_book [chapter]`",
            color=ControlPanelEmbedFactory.COLORS['info'],
        )
        embed.add_field(
            name="Available Chapters",
            value="• Architecture Overview\n• Implementation Guide\n• API Reference\n• Best Practices",
            inline=False,
        )
        return embed

    @staticmethod
    def create_all_commands_embed() -> 'discord.Embed':
        """Create all commands embed."""
        embed = discord.Embed(
            title="📋 All Available Commands",
            description=(
                "**🎯 IMPORTANT: All commands are accessible via buttons in the Control Panel!**\n\n"
                "**Use `!control` (or `!panel`, `!menu`) to open the Control Panel with all buttons.**\n\n"
                "Commands listed below are for reference - buttons are preferred."
            ),
            color=ControlPanelEmbedFactory.COLORS['secondary'],
        )

        embed.add_field(
            name="📨 Messaging Commands",
            value="`!msg <agent> <message>` - Send message to agent\n"
                  "`!broadcast <message>` - Send to all agents\n"
                  "`!status` - Show swarm status",
            inline=False,
        )

        embed.add_field(
            name="🎪 Showcase Commands",
            value="`!showcase` - View agent achievements\n"
                  "`!roadmap` - Development roadmap\n"
                  "`!goldmines` - Success highlights",
            inline=False,
        )

        embed.add_field(
            name="🔧 System Commands",
            value="`!restart` - Restart bot\n"
                  "`!shutdown` - Shutdown bot\n"
                  "`!monitor` - Status monitor controls",
            inline=False,
        )

        embed.set_footer(text="Control Panel buttons provide the full interactive experience")

        return embed


class EmbedTemplateManager:
    """
    Manages embed templates for consistent styling across the application.

    Provides reusable templates and ensures brand consistency.
    """

    @staticmethod
    def apply_standard_footer(embed: 'discord.Embed', timestamp: bool = True) -> 'discord.Embed':
        """Apply standard footer to embed."""
        footer_text = "Agent Cellphone V2"
        if timestamp:
            footer_text += f" | {datetime.now().strftime('%H:%M:%S')}"

        embed.set_footer(text=footer_text)
        return embed

    @staticmethod
    def apply_timestamp(embed: 'discord.Embed') -> 'discord.Embed':
        """Add timestamp to embed."""
        embed.timestamp = datetime.now()
        return embed

    @staticmethod
    def apply_author(embed: 'discord.Embed', name: str, icon_url: str = None) -> 'discord.Embed':
        """Add author to embed."""
        embed.set_author(name=name, icon_url=icon_url)
        return embed

    @staticmethod
    def apply_thumbnail(embed: 'discord.Embed', url: str) -> 'discord.Embed':
        """Add thumbnail to embed."""
        embed.set_thumbnail(url=url)
        return embed

    @staticmethod
    def apply_image(embed: 'discord.Embed', url: str) -> 'discord.Embed':
        """Add image to embed."""
        embed.set_image(url=url)
        return embed


# Convenience functions for backward compatibility
def create_monitor_embed(is_running: bool, interval: int = 15):
    """Backward compatibility function."""
    return ControlPanelEmbedFactory.create_monitor_status_embed(is_running, interval)


def create_error_embed(title: str, message: str):
    """Backward compatibility function."""
    return ControlPanelEmbedFactory.create_error_embed(title, message, None)


def create_success_embed(title: str, message: str):
    """Backward compatibility function."""
    return ControlPanelEmbedFactory.create_success_embed(title, message)