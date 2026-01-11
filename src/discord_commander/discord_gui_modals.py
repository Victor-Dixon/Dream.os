#!/usr/bin/env python3
"""
Discord GUI Modals - Agent Cellphone V2
======================================

SSOT Domain: discord

Refactored entry point for Discord modal functionality.
All core logic has been extracted into specialized base classes and focused implementations.

Features:
- Agent messaging modals (discord_gui_modals_v2.py)
- Specialized modal base classes (modal_specializations.py)
- Common modal utilities (discord_gui_modals_base.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Import all modal classes directly (consolidated from v2)
import logging
from pathlib import Path
import subprocess

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, _ = get_mock_discord()
    discord = mock_discord

from .discord_gui_modals_base import BaseMessageModal
from .modal_specializations import OnboardingModalBase, BroadcastModalBase, TemplateModalBase

logger = logging.getLogger(__name__)

class AgentMessageModal(BaseMessageModal):
    """Modal for composing message to specific agent."""

    def __init__(self, agent_id: str, messaging_service):
        super().__init__(
            title=f"Message to {agent_id}",
            messaging_service=messaging_service,
            message_placeholder=f"Enter message for {agent_id}...\n\nTip: Use Shift+Enter to add line breaks",
        )
        self.agent_id = agent_id

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        await self._handle_submit(interaction, self.agent_id, "agent")

class BroadcastMessageModal(BaseMessageModal):
    """Modal for composing broadcast message to all agents."""

    def __init__(self, messaging_service):
        super().__init__(
            title="Broadcast to All Agents",
            messaging_service=messaging_service,
            message_placeholder="Enter broadcast message to all agents...\n\nTip: Use Shift+Enter to add line breaks",
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        await self._handle_submit(interaction, "all", "broadcast")

class JetFuelMessageModal(BaseMessageModal):
    """Modal for composing Jet Fuel coordination message."""

    def __init__(self, messaging_service):
        super().__init__(
            title="🚀 Jet Fuel Coordination",
            messaging_service=messaging_service,
            message_placeholder="Enter Jet Fuel coordination details...\n\nTip: Use Shift+Enter to add line breaks",
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        await self._handle_submit(interaction, "jetfuel", "jetfuel")

class SelectiveBroadcastModal(BroadcastModalBase):
    """Modal for selective broadcast to specific agents."""

    def __init__(self, messaging_service, available_agents):
        super().__init__(
            title="Selective Broadcast",
            messaging_service=messaging_service,
            available_agents=available_agents,
        )

class JetFuelBroadcastModal(BroadcastModalBase):
    """Modal for Jet Fuel broadcast coordination."""

    def __init__(self, messaging_service, available_agents):
        super().__init__(
            title="🚀 Jet Fuel Broadcast",
            messaging_service=messaging_service,
            available_agents=available_agents,
        )

class TemplateBroadcastModal(TemplateModalBase):
    """Modal for template-based broadcast messaging."""

    def __init__(self, messaging_service, available_agents):
        super().__init__(
            title="Template Broadcast",
            messaging_service=messaging_service,
            available_agents=available_agents,
        )

class SoftOnboardModal(OnboardingModalBase):
    """Modal for soft agent onboarding."""

    def __init__(self, messaging_service):
        super().__init__(
            title="🤝 Soft Agent Onboarding",
            messaging_service=messaging_service,
            onboarding_type="soft",
        )

class MermaidModal(BaseMessageModal):
    """Modal for Mermaid diagram rendering."""

    def __init__(self, messaging_service):
        super().__init__(
            title="📊 Mermaid Diagram",
            messaging_service=messaging_service,
            message_placeholder="Enter Mermaid diagram code...\n\nExample:\ngraph TD;\n    A-->B;\n    A-->C;",
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission for Mermaid diagrams."""
        await self._handle_mermaid_submit(interaction)

class HardOnboardModal(OnboardingModalBase):
    """Modal for hard agent onboarding."""

    def __init__(self, messaging_service):
        super().__init__(
            title="🔧 Hard Agent Onboarding",
            messaging_service=messaging_service,
            onboarding_type="hard",
        )

# Re-export base classes
from .discord_gui_modals_base import BaseMessageModal
from .modal_specializations import OnboardingModalBase, BroadcastModalBase, TemplateModalBase

__all__ = [
    # Modal classes
    "AgentMessageModal",
    "BroadcastMessageModal",
    "JetFuelMessageModal",
    "SelectiveBroadcastModal",
    "JetFuelBroadcastModal",
    "TemplateBroadcastModal",
    "SoftOnboardModal",
    "MermaidModal",
    "HardOnboardModal",
    # Base classes
    "BaseMessageModal",
    "OnboardingModalBase",
    "BroadcastModalBase",
    "TemplateModalBase",
]
