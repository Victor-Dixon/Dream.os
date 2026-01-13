#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord GUI Modals Base - Common Modal Functionality
====================================================

Base classes and utilities for Discord UI modals.

Author: Agent-6 (Coordination & Communication Specialist) - V2 Compliance Refactor
License: MIT
"""

import logging
from typing import Optional

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.core.messaging_models_core import MessageCategory
from src.services.messaging_infrastructure import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class BaseModal(discord.ui.Modal):
    """
    Base modal class for Discord UI components.

    Navigation:
    ├── Subclasses: OnboardingModalBase, BroadcastModalBase, TemplateModalBase
    ├── Used by: Modal specializations
    └── Related: Discord UI framework, modal lifecycle
    """

    def __init__(self, title: str, timeout: float = 300.0, custom_id: Optional[str] = None):
        """Initialize the base modal."""
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        """Handle modal errors."""
        logger.error(f"Modal error in {self.__class__.__name__}: {error}")
        try:
            await interaction.response.send_message(
                f"❌ An error occurred: {str(error)}", ephemeral=True
            )
        except discord.InteractionResponded:
            await interaction.followup.send(
                f"❌ An error occurred: {str(error)}", ephemeral=True
            )


class BaseMessageModal(discord.ui.Modal):
    """Base modal for message composition with common functionality."""

    def __init__(
        self,
        title: str,
        messaging_service: ConsolidatedMessagingService,
        message_label: str = "Message (Shift+Enter for line breaks)",
        message_placeholder: str = "Enter message...",
        include_priority: bool = True,
        include_agent_selection: bool = False,
    ):
        super().__init__(title=title)
        self.messaging_service = messaging_service

        # Agent selection (if needed)
        if include_agent_selection:
            self.agent_input = discord.ui.TextInput(
                label="Agent ID",
                placeholder="Agent-1, Agent-2, etc.",
                required=True,
                max_length=200,
            )
            self.add_item(self.agent_input)

        # Message input
        self.message_input = discord.ui.TextInput(
            label=message_label,
            placeholder=message_placeholder,
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority input (if needed)
        if include_priority:
            self.priority_input = discord.ui.TextInput(
                label="Priority (regular/urgent)",
                placeholder="regular",
                default="regular",
                required=False,
                max_length=10,
            )
            self.add_item(self.priority_input)

    def _get_message_preview(self, message: str, max_length: int = 500) -> str:
        """Get message preview with length limit."""
        return message if len(message) <= max_length else message[:max_length - 3] + "..."

    def _send_to_agent(
        self,
        agent_id: str,
        message: str,
        priority: str = "regular",
        jet_fuel: bool = False,
        discord_user=None,
    ) -> dict:
        """Send message to single agent."""
        if jet_fuel:
            message = f"🚀 JET FUEL MESSAGE - AUTONOMOUS MODE ACTIVATED\n\n{message}"
            priority = "urgent"

        sender = (
            f"Discord User ({getattr(discord_user, 'name', '')})"
            if discord_user
            else "Discord GUI"
        )
        discord_user_id = str(getattr(discord_user, "id", "")) if discord_user else None

        return self.messaging_service.send_message(
            agent=agent_id,
            message=message,
            priority=priority,
            use_pyautogui=True,
            discord_user_id=discord_user_id,
            apply_template=True,
            message_category=MessageCategory.D2A,
            sender=sender,
        )

    def _send_jet_fuel_message(
        self,
        target: str,
        message: str,
        priority: str = "urgent",
        discord_user=None,
    ) -> dict:
        """Send Jet Fuel coordination message."""
        jet_fuel_message = f"🚀 JET FUEL COORDINATION - AUTONOMOUS MODE ACTIVATED\n\n{message}"

        sender = (
            f"Discord User ({getattr(discord_user, 'name', '')})"
            if discord_user
            else "Discord GUI"
        )
        discord_user_id = str(getattr(discord_user, "id", "")) if discord_user else None

        return self.messaging_service.send_message(
            agent=target,
            message=jet_fuel_message,
            priority=priority,
            use_pyautogui=True,
            discord_user_id=discord_user_id,
            apply_template=True,
            message_category=MessageCategory.D2A,
            sender=sender,
        )

    def _broadcast_to_agents(
        self,
        agents: list[str],
        message: str,
        priority: str = "regular",
        jet_fuel: bool = False,
        discord_user=None,
    ) -> tuple[int, list[str]]:
        """Broadcast message to multiple agents. Returns (success_count, errors)."""
        if jet_fuel:
            message = f"🚀 JET FUEL MESSAGE - AUTONOMOUS MODE ACTIVATED\n\n{message}"
            priority = "urgent"

        success_count = 0
        errors = []

        for agent in agents:
            result = self._send_to_agent(
                agent,
                message,
                priority,
                jet_fuel=False,
                discord_user=discord_user,
            )
            if result.get("success"):
                success_count += 1
            else:
                errors.append(f"{agent}: {result.get('error')}")

        return success_count, errors

    def _get_all_agents(self) -> list[str]:
        """Get list of all agent IDs."""
        return [f"Agent-{i}" for i in range(1, 9)]

    def _format_error_message(self, errors: list[str], max_errors: int = 3) -> str:
        """Format error message list."""
        return "\n".join(errors[:max_errors])

    async def _handle_submit(self, interaction: discord.Interaction, target: str, message_type: str):
        """Handle modal submission for messages."""
        try:
            message = self.message_input.value
            priority = getattr(self, 'priority_input', None)
            priority = priority.value if priority else "regular"

            preview = self._get_message_preview(message)

            if message_type == "agent":
                result = self._send_to_agent(target, message, priority, discord_user=interaction.user)
                if result.get("success"):
                    await interaction.response.send_message(
                        f"✅ Message sent to {target}!\n📝 Preview: {preview}", ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Failed to send message to {target}: {result.get('error', 'Unknown error')}",
                        ephemeral=True
                    )
            elif message_type == "broadcast":
                agents = self._get_all_agent_ids()
                success_count, errors = self._broadcast_to_agents(agents, message, priority, discord_user=interaction.user)
                if success_count > 0:
                    await interaction.response.send_message(
                        f"✅ Broadcast sent to {success_count} agents!\n📝 Preview: {preview}", ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Broadcast failed: {self._format_error_message(errors)}", ephemeral=True
                    )
            elif message_type == "jetfuel":
                # Jet Fuel specific handling
                result = self._send_jet_fuel_message(target, message, priority, discord_user=interaction.user)
                if result.get("success"):
                    await interaction.response.send_message(
                        f"🚀 Jet Fuel coordination sent!\n📝 Preview: {preview}", ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Jet Fuel coordination failed: {result.get('error', 'Unknown error')}",
                        ephemeral=True
                    )

        except Exception as e:
            logger.error(f"Modal submit error: {e}")
            await interaction.response.send_message(
                f"❌ An error occurred: {str(e)}", ephemeral=True
            )

    async def _handle_mermaid_submit(self, interaction: discord.Interaction):
        """Handle Mermaid diagram modal submission."""
        try:
            diagram_code = self.message_input.value

            # Basic validation
            if not diagram_code.strip():
                await interaction.response.send_message("❌ Please enter Mermaid diagram code.", ephemeral=True)
                return

            # For now, just acknowledge - full Mermaid rendering would need additional setup
            await interaction.response.send_message(
                f"📊 Mermaid diagram submitted!\n```\n{diagram_code[:500]}{'...' if len(diagram_code) > 500 else ''}\n```",
                ephemeral=True
            )

        except Exception as e:
            logger.error(f"Mermaid modal error: {e}")
            await interaction.response.send_message(
                f"❌ Failed to process Mermaid diagram: {str(e)}", ephemeral=True
            )


__all__ = ["BaseMessageModal"]

