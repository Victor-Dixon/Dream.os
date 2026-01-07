"""
Modal Specializations - Agent Cellphone V2
==========================================

SSOT Domain: discord

Specialized base classes for common Discord modal patterns.

Features:
- Onboarding modal base class
- Broadcast modal base class
- Template modal base class
- Common submission handlers

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, _ = get_mock_discord()
    discord = mock_discord

from .discord_gui_modals_base import BaseMessageModal

logger = logging.getLogger(__name__)

class OnboardingModalBase(discord.ui.Modal if DISCORD_AVAILABLE else object):
    """Base class for onboarding-related modals."""

    def __init__(self, title: str, messaging_service):
        super().__init__(title=title)
        self.messaging_service = messaging_service

        # Common agent selection input
        self.agent_input = discord.ui.TextInput(
            label="Agent ID(s)",
            placeholder="Agent-1, Agent-2, or 'all'",
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

        # Optional custom message input
        self.message_input = discord.ui.TextInput(
            label="Custom Message (Optional)",
            placeholder="Leave empty for default message...",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=2000,
        )
        self.add_item(self.message_input)

    def parse_agent_list(self, agent_input: str) -> List[str]:
        """Parse agent list from input string."""
        if not agent_input or agent_input.lower() == "all":
            return [f"Agent-{i}" for i in range(1, 9)]
        else:
            # Parse comma-separated list
            raw_list = [aid.strip() for aid in agent_input.split(",") if aid.strip()]
            # Validate agent IDs
            valid_agents = []
            for agent_id in raw_list:
                if agent_id.startswith("Agent-") and len(agent_id) >= 7:
                    try:
                        agent_num = int(agent_id[6:])  # Extract number after "Agent-"
                        if 1 <= agent_num <= 8:
                            valid_agents.append(agent_id)
                    except ValueError:
                        continue
                elif agent_id in [f"Agent-{i}" for i in range(1, 9)]:
                    valid_agents.append(agent_id)

            return list(set(valid_agents))  # Remove duplicates

    def get_default_message(self) -> str:
        """Get default message - override in subclasses."""
        return "Default onboarding message"

    async def execute_onboarding(self, agent_list: List[str], custom_message: Optional[str] = None):
        """Execute onboarding logic - override in subclasses."""
        raise NotImplementedError

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission with common onboarding flow."""
        try:
            agent_input = self.agent_input.value.strip()
            custom_message = self.message_input.value.strip() if self.message_input.value else None

            agent_list = self.parse_agent_list(agent_input)

            if not agent_list:
                await interaction.response.send_message(
                    "❌ No valid agent IDs provided. Use format: Agent-1, Agent-2, or 'all'",
                    ephemeral=True
                )
                return

            # Show processing message
            await interaction.response.send_message(
                f"🚀 Processing onboarding for {len(agent_list)} agent(s)...",
                ephemeral=True
            )

            # Execute onboarding
            result = await self.execute_onboarding(agent_list, custom_message)

            # Send success message
            success_msg = f"✅ Successfully onboarded {len(agent_list)} agent(s):\n"
            success_msg += "\n".join(f"• {agent}" for agent in agent_list[:5])
            if len(agent_list) > 5:
                success_msg += f"\n... and {len(agent_list) - 5} more"

            await interaction.followup.send(success_msg, ephemeral=True)

        except Exception as e:
            logger.error(f"Onboarding modal error: {e}")
            await interaction.followup.send(
                f"❌ Onboarding failed: {str(e)}",
                ephemeral=True
            )

class BroadcastModalBase(BaseMessageModal):
    """Base class for broadcast messaging modals."""

    def __init__(self, title: str, messaging_service, broadcast_type: str = "broadcast"):
        super().__init__(
            title=title,
            messaging_service=messaging_service,
            message_placeholder="Enter broadcast message...",
            include_priority=True
        )
        self.broadcast_type = broadcast_type

    def get_target_agents(self) -> List[str]:
        """Get list of target agents for broadcast - override in subclasses."""
        return [f"Agent-{i}" for i in range(1, 9)]

    async def on_submit(self, interaction: discord.Interaction):
        """Handle broadcast submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            target_agents = self.get_target_agents()

            if not target_agents:
                await interaction.response.send_message(
                    "❌ No target agents available for broadcast",
                    ephemeral=True
                )
                return

            # Show processing message
            await interaction.response.send_message(
                f"📡 Broadcasting to {len(target_agents)} agent(s)...",
                ephemeral=True
            )

            # Send to each agent
            success_count = 0
            for agent_id in target_agents:
                try:
                    result = self._send_to_agent(
                        agent_id=agent_id,
                        message=message,
                        priority=priority,
                        category=self.broadcast_type
                    )
                    if result:
                        success_count += 1
                except Exception as e:
                    logger.warning(f"Failed to send to {agent_id}: {e}")

            # Send result message
            if success_count == len(target_agents):
                result_msg = f"✅ Broadcast sent successfully to all {len(target_agents)} agents"
            else:
                result_msg = f"⚠️ Broadcast sent to {success_count}/{len(target_agents)} agents"

            await interaction.followup.send(result_msg, ephemeral=True)

        except Exception as e:
            logger.error(f"Broadcast modal error: {e}")
            await interaction.followup.send(
                f"❌ Broadcast failed: {str(e)}",
                ephemeral=True
            )

class TemplateModalBase(discord.ui.Modal if DISCORD_AVAILABLE else object):
    """Base class for template-based messaging modals."""

    def __init__(self, title: str, messaging_service, template_name: str):
        super().__init__(title=title)
        self.messaging_service = messaging_service
        self.template_name = template_name

        # Template variables input
        self.variables_input = discord.ui.TextInput(
            label="Template Variables (JSON)",
            placeholder='{"name": "Agent-1", "task": "analysis"}',
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=1000,
        )
        self.add_item(self.variables_input)

        # Agent selection
        self.agent_input = discord.ui.TextInput(
            label="Target Agent(s)",
            placeholder="Agent-1, Agent-2, or 'all'",
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

    def get_template_message(self, variables: Dict[str, Any]) -> str:
        """Get formatted template message - override in subclasses."""
        return f"Template message for {self.template_name}"

    async def on_submit(self, interaction: discord.Interaction):
        """Handle template submission."""
        try:
            agent_input = self.agent_input.value.strip()
            variables_str = self.variables_input.value.strip() if self.variables_input.value else "{}"

            # Parse variables
            try:
                variables = eval(variables_str) if variables_str else {}
                if not isinstance(variables, dict):
                    raise ValueError("Variables must be a JSON object")
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Invalid variables JSON: {str(e)}",
                    ephemeral=True
                )
                return

            # Parse agents
            if agent_input.lower() == "all":
                target_agents = [f"Agent-{i}" for i in range(1, 9)]
            else:
                target_agents = [aid.strip() for aid in agent_input.split(",") if aid.strip()]

            if not target_agents:
                await interaction.response.send_message(
                    "❌ No valid agent IDs provided",
                    ephemeral=True
                )
                return

            # Generate message from template
            message = self.get_template_message(variables)

            # Show processing message
            await interaction.response.send_message(
                f"📝 Sending template message to {len(target_agents)} agent(s)...",
                ephemeral=True
            )

            # Send to agents
            success_count = 0
            for agent_id in target_agents:
                try:
                    # Use base modal send method if available, otherwise direct send
                    if hasattr(self, '_send_to_agent'):
                        result = self._send_to_agent(
                            agent_id=agent_id,
                            message=message,
                            priority="regular",
                            category="text"
                        )
                    else:
                        # Direct messaging service call
                        result = await self.messaging_service.send_message(
                            sender="Discord-Bot",
                            recipient=agent_id,
                            message=message,
                            priority="regular",
                            category="text"
                        )
                    if result:
                        success_count += 1
                except Exception as e:
                    logger.warning(f"Failed to send template to {agent_id}: {e}")

            # Send result
            result_msg = f"✅ Template sent to {success_count}/{len(target_agents)} agents"
            await interaction.followup.send(result_msg, ephemeral=True)

        except Exception as e:
            logger.error(f"Template modal error: {e}")
            await interaction.followup.send(
                f"❌ Template sending failed: {str(e)}",
                ephemeral=True
            )