#!/usr/bin/env python3
"""
Discord GUI Modals - Agent Messaging Modals
============================================

Discord UI Modals for message composition.

V2 Compliance: Refactored to use base classes (762L → <300L target)

Author: Agent-6 (Coordination & Communication Specialist) - V2 Compliance Refactor
Original: Agent-7 (Repository Cloning Specialist)
License: MIT
"""

import logging

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_infrastructure import ConsolidatedMessagingService
from .discord_gui_modals_base import BaseMessageModal

logger = logging.getLogger(__name__)


class AgentMessageModal(BaseMessageModal):
    """Modal for composing message to specific agent."""

    def __init__(self, agent_id: str, messaging_service: ConsolidatedMessagingService):
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

            result = self._send_to_agent(self.agent_id, message, priority)

            if result.get("success"):
                preview = self._get_message_preview(message)
                await interaction.response.send_message(
                    f"✅ Message sent to {self.agent_id}!\n\n**Message Preview:**\n```\n{preview}\n```",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"❌ Failed to send message: {result.get('error')}", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class BroadcastMessageModal(BaseMessageModal):
    """Modal for broadcasting message to all agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(
            title="Broadcast to All Agents",
            messaging_service=messaging_service,
            message_label="Broadcast Message (Shift+Enter)",
            message_placeholder="Enter message for all agents...\n\nTip: Use Shift+Enter to add line breaks",
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"
            agents = self._get_all_agents()

            success_count, errors = self._broadcast_to_agents(
                agents, message, priority)

            if success_count == len(agents):
                preview = self._get_message_preview(message)
                await interaction.response.send_message(
                    f"✅ Broadcast sent to all {len(agents)} agents!\n\n**Message Preview:**\n```\n{preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = self._format_error_message(errors)
                preview = self._get_message_preview(message, 300)
                await interaction.response.send_message(
                    f"⚠️ Partial broadcast: {success_count}/{len(agents)} successful\n\n"
                    f"**Message:**\n```\n{preview}\n```\n**Errors:**\n{error_msg}",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error(f"Error broadcasting: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class JetFuelMessageModal(BaseMessageModal):
    """Modal for sending Jet Fuel (AGI activation) message to agent."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(
            title="🚀 Jet Fuel Message - AGI Activation",
            messaging_service=messaging_service,
            message_label="Jet Fuel Message (Shift+Enter)",
            message_placeholder="Enter Jet Fuel message...\n\nTip: Jet Fuel messages grant full AGI autonomy!",
            include_priority=False,
            include_agent_selection=True,
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            agent_id = self.agent_input.value.strip()
            message = self.message_input.value

            result = self._send_to_agent(agent_id, message, jet_fuel=True)

            if result.get("success"):
                preview = self._get_message_preview(message)
                await interaction.response.send_message(
                    f"✅ Jet Fuel message sent to {agent_id}!\n\n**AGI Activation:** 🚀\n**Message Preview:**\n```\n{preview}\n```",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"❌ Failed to send Jet Fuel message: {result.get('error')}", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error sending Jet Fuel message: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class SelectiveBroadcastModal(BaseMessageModal):
    """Modal for broadcasting to selected agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService, default_agents: list[str] | None = None):
        agent_placeholder = ", ".join(
            default_agents) if default_agents else "Agent-1, Agent-2, Agent-3..."
        super().__init__(
            title="Broadcast to Selected Agents",
            messaging_service=messaging_service,
            message_placeholder="Enter message for selected agents...",
            include_agent_selection=True,
        )
        self.default_agents = default_agents or []
        self.agent_input.placeholder = agent_placeholder
        if default_agents:
            self.agent_input.default = agent_placeholder

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            agent_ids_str = self.agent_input.value.strip()
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            agent_ids = [aid.strip()
                         for aid in agent_ids_str.split(",") if aid.strip()]

            if not agent_ids:
                await interaction.response.send_message("❌ No agents specified!", ephemeral=True)
                return

            success_count, errors = self._broadcast_to_agents(
                agent_ids, message, priority)

            if success_count == len(agent_ids):
                preview = self._get_message_preview(message)
                await interaction.response.send_message(
                    f"✅ Broadcast sent to {success_count} agent(s)!\n\n**Message Preview:**\n```\n{preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = self._format_error_message(errors)
                await interaction.response.send_message(
                    f"⚠️ Partial broadcast: {success_count}/{len(agent_ids)} successful\n\n**Errors:**\n{error_msg}",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error(f"Error in selective broadcast: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class JetFuelBroadcastModal(BaseMessageModal):
    """Modal for Jet Fuel broadcast to all agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(
            title="🚀 Jet Fuel Broadcast - AGI Activation for All",
            messaging_service=messaging_service,
            message_label="Jet Fuel Message (Shift+Enter)",
            message_placeholder="Enter Jet Fuel message for all agents...\n\nTip: Jet Fuel = AGI autonomy!",
            include_priority=False,
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            agents = self._get_all_agents()

            success_count, errors = self._broadcast_to_agents(
                agents, message, jet_fuel=True)

            if success_count == len(agents):
                preview = self._get_message_preview(message)
                await interaction.response.send_message(
                    f"✅ Jet Fuel broadcast sent to all {len(agents)} agents!\n\n**AGI Activation:** 🚀🚀🚀\n**Message Preview:**\n```\n{preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = self._format_error_message(errors)
                await interaction.response.send_message(
                    f"⚠️ Partial Jet Fuel broadcast: {success_count}/{len(agents)} successful\n\n**Errors:**\n{error_msg}",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error(f"Error in Jet Fuel broadcast: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class TemplateBroadcastModal(BaseMessageModal):
    """Modal for broadcasting with template pre-filled content."""

    def __init__(
        self,
        messaging_service: ConsolidatedMessagingService,
        template_message: str,
        template_priority: str = "regular",
    ):
        super().__init__(
            title="Broadcast with Template",
            messaging_service=messaging_service,
            message_label="Broadcast Message (Template)",
            message_placeholder=template_message[:500] + "..." if len(
                template_message) > 500 else template_message,
        )
        self.message_input.default = template_message
        self.priority_input.default = template_priority

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"
            agents = self._get_all_agents()

            success_count, errors = self._broadcast_to_agents(
                agents, message, priority)

            if success_count == len(agents):
                preview = self._get_message_preview(message)
                await interaction.response.send_message(
                    f"✅ Template broadcast sent to all {len(agents)} agents!\n\n**Message Preview:**\n```\n{preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = self._format_error_message(errors)
                preview = self._get_message_preview(message, 300)
                await interaction.response.send_message(
                    f"⚠️ Partial broadcast: {success_count}/{len(agents)} successful\n\n"
                    f"**Message:**\n```\n{preview}\n```\n**Errors:**\n{error_msg}",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error(f"Error broadcasting template: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


__all__ = [
    "AgentMessageModal",
    "BroadcastMessageModal",
    "JetFuelMessageModal",
    "SelectiveBroadcastModal",
    "JetFuelBroadcastModal",
    "TemplateBroadcastModal",
]
