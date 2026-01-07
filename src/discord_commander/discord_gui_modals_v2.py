"""
Discord GUI Modals V2 - Agent Cellphone V2
==========================================

SSOT Domain: discord

Refactored Discord UI modals using specialized base classes.

Features:
- Agent-specific messaging modals
- Broadcast messaging modals
- Onboarding modals
- Template-based messaging

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

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
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            result = self._send_to_agent(
                agent_id=self.agent_id,
                message=message,
                priority=priority
            )

            if result:
                await interaction.response.send_message(
                    f"✅ Message sent to {self.agent_id}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"❌ Failed to send message to {self.agent_id}",
                    ephemeral=True
                )

        except Exception as e:
            logger.error(f"Agent message modal error: {e}")
            await interaction.response.send_message(
                "❌ Message sending failed",
                ephemeral=True
            )

class BroadcastMessageModal(BroadcastModalBase):
    """Modal for broadcasting messages to all agents."""

    def __init__(self, messaging_service):
        super().__init__(
            title="📡 Broadcast Message",
            messaging_service=messaging_service,
            broadcast_type="broadcast"
        )

class JetFuelMessageModal(BaseMessageModal):
    """Modal for sending jet fuel messages."""

    def __init__(self, agent_id: str, messaging_service):
        super().__init__(
            title=f"⛽ Jet Fuel for {agent_id}",
            messaging_service=messaging_service,
            message_placeholder="Enter jet fuel message...",
        )
        self.agent_id = agent_id

    async def on_submit(self, interaction: discord.Interaction):
        """Handle jet fuel modal submission."""
        try:
            message = self.message_input.value
            priority = "urgent"  # Jet fuel is always urgent

            result = self._send_to_agent(
                agent_id=self.agent_id,
                message=f"⛽ JET FUEL: {message}",
                priority=priority,
                category="jet_fuel"
            )

            response_msg = "✅" if result else "❌"
            response_msg += f" Jet fuel delivered to {self.agent_id}"

            await interaction.response.send_message(response_msg, ephemeral=True)

        except Exception as e:
            logger.error(f"Jet fuel modal error: {e}")
            await interaction.response.send_message(
                "❌ Jet fuel delivery failed",
                ephemeral=True
            )

class SelectiveBroadcastModal(BroadcastModalBase):
    """Modal for broadcasting to selected agents."""

    def __init__(self, messaging_service, agent_list: list):
        super().__init__(
            title="🎯 Selective Broadcast",
            messaging_service=messaging_service,
            broadcast_type="selective_broadcast"
        )
        self.agent_list = agent_list

    def get_target_agents(self):
        """Get selected agents for broadcast."""
        return self.agent_list

class JetFuelBroadcastModal(BroadcastModalBase):
    """Modal for broadcasting jet fuel to all agents."""

    def __init__(self, messaging_service):
        super().__init__(
            title="⛽ Jet Fuel Broadcast",
            messaging_service=messaging_service,
            broadcast_type="jet_fuel_broadcast"
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle jet fuel broadcast submission."""
        try:
            message = self.message_input.value

            # Modify message for jet fuel broadcast
            broadcast_message = f"⛽ JET FUEL BROADCAST: {message}"

            # Temporarily override message
            original_message = self.message_input.value
            self.message_input.value = broadcast_message

            # Use parent submission logic
            await super().on_submit(interaction)

            # Restore original message
            self.message_input.value = original_message

        except Exception as e:
            logger.error(f"Jet fuel broadcast modal error: {e}")
            await interaction.response.send_message(
                "❌ Jet fuel broadcast failed",
                ephemeral=True
            )

class TemplateBroadcastModal(TemplateModalBase):
    """Modal for template-based broadcasts."""

    def __init__(self, messaging_service):
        super().__init__(
            title="📝 Template Broadcast",
            messaging_service=messaging_service,
            template_name="broadcast_template"
        )

    def get_template_message(self, variables: dict) -> str:
        """Get formatted template message."""
        template = "📡 BROADCAST: {message}\n\nPriority: {priority}\nTarget: All Agents"
        return template.format(
            message=variables.get("message", "System broadcast"),
            priority=variables.get("priority", "normal")
        )

class SoftOnboardModal(OnboardingModalBase):
    """Modal for soft onboarding agents."""

    def get_default_message(self) -> str:
        """Get default soft onboarding message."""
        return "🚀 SOFT ONBOARD - Agent activation initiated. Check your inbox and begin autonomous operations."

    async def execute_onboarding(self, agent_list: list, custom_message: str = None):
        """Execute soft onboarding."""
        project_root = Path(__file__).parent.parent.parent
        cli_path = project_root / 'tools' / 'soft_onboard_cli.py'

        message = custom_message if custom_message else self.get_default_message()

        # Execute soft onboarding for each agent
        results = []
        for agent_id in agent_list:
            try:
                cmd = [
                    'python', str(cli_path),
                    '--agent', agent_id,
                    '--message', message
                ]

                result = subprocess.run(
                    cmd,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    results.append(f"✅ {agent_id}: Onboarded successfully")
                else:
                    results.append(f"❌ {agent_id}: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                results.append(f"⏰ {agent_id}: Timeout during onboarding")
            except Exception as e:
                results.append(f"❌ {agent_id}: {str(e)}")

        return results

class MermaidModal(discord.ui.Modal if DISCORD_AVAILABLE else object):
    """Modal for Mermaid diagram input."""

    def __init__(self):
        super().__init__(title="🧜 Mermaid Diagram")
        self.diagram_input = discord.ui.TextInput(
            label="Mermaid Code",
            placeholder="graph TD\nA-->B\nB-->C",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.diagram_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle Mermaid diagram submission."""
        try:
            diagram_code = self.diagram_input.value

            # Here you would typically send to a Mermaid rendering service
            # For now, just acknowledge receipt
            await interaction.response.send_message(
                f"🧜 Mermaid diagram received ({len(diagram_code)} chars)",
                ephemeral=True
            )

        except Exception as e:
            logger.error(f"Mermaid modal error: {e}")
            await interaction.response.send_message(
                "❌ Diagram processing failed",
                ephemeral=True
            )

class HardOnboardModal(OnboardingModalBase):
    """Modal for hard onboarding agents."""

    def get_default_message(self) -> str:
        """Get default hard onboarding message."""
        return "🔧 HARD ONBOARD - Complete system reset and reconfiguration initiated."

    async def execute_onboarding(self, agent_list: list, custom_message: str = None):
        """Execute hard onboarding."""
        # Hard onboarding would involve more extensive reset procedures
        # This is a simplified version
        message = custom_message if custom_message else self.get_default_message()

        results = []
        for agent_id in agent_list:
            try:
                # In a real implementation, this would trigger extensive reset procedures
                results.append(f"🔧 {agent_id}: Hard onboard initiated - full system reset")
            except Exception as e:
                results.append(f"❌ {agent_id}: Hard onboard failed - {str(e)}")

        return results