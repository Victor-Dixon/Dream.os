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
from src.core.config.timeout_constants import TimeoutConstants

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

            result = self._send_to_agent(
                self.agent_id,
                message,
                priority,
                discord_user=interaction.user,
            )

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
                agents,
                message,
                priority,
                discord_user=interaction.user,
            )

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

            result = self._send_to_agent(
                agent_id,
                message,
                jet_fuel=True,
                discord_user=interaction.user,
            )

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
                agent_ids,
                message,
                priority,
                discord_user=interaction.user,
            )

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
                agents,
                message,
                jet_fuel=True,
                discord_user=interaction.user,
            )

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


class SoftOnboardModal(discord.ui.Modal):
    """Modal for soft onboarding agent(s)."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="🚀 Soft Onboard Agent(s)")
        self.messaging_service = messaging_service

        # Agent selection
        self.agent_input = discord.ui.TextInput(
            label="Agent ID(s)",
            placeholder="Agent-1, Agent-1,Agent-2,Agent-3, or 'all'",
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

        # Optional custom message
        self.message_input = discord.ui.TextInput(
            label="Onboarding Message (Optional)",
            placeholder="Leave empty for default message, or enter custom onboarding message...",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=2000,
        )
        self.add_item(self.message_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            import subprocess
            from pathlib import Path

            agent_ids = self.agent_input.value.strip()
            custom_message = self.message_input.value.strip() if self.message_input.value else None

            # Get project root
            project_root = Path(__file__).parent.parent.parent
            cli_path = project_root / 'tools' / 'soft_onboard_cli.py'

            # Default message
            default_message = "🚀 SOFT ONBOARD - Agent activation initiated. Check your inbox and begin autonomous operations."
            message = custom_message if custom_message else default_message

            # Parse agent list
            if not agent_ids or agent_ids.lower() == "all":
                agent_list = [f"Agent-{i}" for i in range(1, 9)]
                agents_str = ','.join(agent_list)
            else:
                # Parse comma-separated list
                raw_list = [aid.strip() for aid in agent_ids.split(",") if aid.strip()]
                agent_list = []
                for aid in raw_list:
                    if aid.isdigit():
                        agent_list.append(f"Agent-{aid}")
                    elif aid.lower().startswith("agent-"):
                        agent_list.append(aid)
                    else:
                        agent_list.append(aid)
                agents_str = ','.join(agent_list)

            # Send initial response
            await interaction.response.defer(ephemeral=True)

            # Execute soft onboarding
            if len(agent_list) == 1:
                cmd = ['python', str(cli_path), '--agent', agent_list[0], '--message', message]
            else:
                cmd = ['python', str(cli_path), '--agents', agents_str, '--message', message, '--generate-cycle-report']

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_EXTENDED,
                cwd=str(project_root)
            )

            # Send results
            if result.returncode == 0:
                embed = discord.Embed(
                    title="✅ SOFT ONBOARD COMPLETE",
                    description=f"Soft onboarding initiated for **{len(agent_list)} agent(s)**",
                    color=discord.Color.green(),
                )
                embed.add_field(
                    name="Agents",
                    value=', '.join(agent_list),
                    inline=False
                )
                if result.stdout:
                    # Extract summary from output
                    output_lines = result.stdout.split('\n')
                    summary = '\n'.join([line for line in output_lines if '✅' in line or '❌' in line][:5])
                    if summary:
                        embed.add_field(name="Status", value=summary[:500], inline=False)
            else:
                error_msg = result.stderr[:500] if result.stderr else result.stdout[:500] if result.stdout else "Unknown error"
                embed = discord.Embed(
                    title="❌ SOFT ONBOARD FAILED",
                    description=f"Failed to soft onboard agents",
                    color=discord.Color.red(),
                )
                embed.add_field(name="Error", value=error_msg, inline=False)

            await interaction.followup.send(embed=embed, ephemeral=True)

        except subprocess.TimeoutExpired:
            await interaction.followup.send(
                "❌ Soft onboarding timed out after 5 minutes", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error in soft onboard modal: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


class MermaidModal(discord.ui.Modal):
    """Modal for creating Mermaid diagrams."""

    def __init__(self):
        super().__init__(title="🌊 Create Mermaid Diagram")
        self.diagram_input = discord.ui.TextInput(
            label="Mermaid Diagram Code",
            placeholder="graph TD; A-->B; B-->C;",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.diagram_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            diagram_code = self.diagram_input.value.strip()
            
            # Remove code block markers if present
            if diagram_code.startswith("```mermaid"):
                diagram_code = diagram_code[10:]
            elif diagram_code.startswith("```"):
                diagram_code = diagram_code[3:]
            if diagram_code.endswith("```"):
                diagram_code = diagram_code[:-3]
            diagram_code = diagram_code.strip()
            
            # Create embed with mermaid code
            embed = discord.Embed(
                title="🌊 Mermaid Diagram",
                description="Mermaid diagram code:",
                color=discord.Color.blue(),
            )
            
            # Send mermaid code in code block
            mermaid_block = f"```mermaid\n{diagram_code}\n```"
            
            # Discord has a 2000 character limit per message
            if len(mermaid_block) > 1900:
                await interaction.response.send_message(
                    "❌ Mermaid diagram too long. Please shorten it.",
                    ephemeral=True
                )
                return
            
            embed.add_field(
                name="Diagram Code",
                value=mermaid_block,
                inline=False,
            )
            
            embed.set_footer(text="Note: Discord may not render Mermaid natively. Use external tools for visualization.")
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error creating mermaid diagram: {e}", exc_info=True)
            await interaction.response.send_message(
                f"❌ Error creating diagram: {e}",
                ephemeral=True
            )


class HardOnboardModal(discord.ui.Modal):
    """Modal for hard onboarding agent(s)."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="🚀 Hard Onboard Agent(s)")
        self.messaging_service = messaging_service

        # Agent selection
        self.agent_input = discord.ui.TextInput(
            label="Agent ID(s)",
            placeholder="Agent-1, Agent-1,Agent-2,Agent-3, or 'all'",
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            from pathlib import Path
            from src.services.hard_onboarding_service import hard_onboard_agent

            agent_ids = self.agent_input.value.strip()

            # Parse agent list
            if not agent_ids or agent_ids.lower() == "all":
                agent_list = [f"Agent-{i}" for i in range(1, 9)]
            else:
                # Parse comma-separated list
                raw_list = [aid.strip() for aid in agent_ids.split(",") if aid.strip()]
                agent_list = []
                for aid in raw_list:
                    if aid.isdigit():
                        agent_list.append(f"Agent-{aid}")
                    elif aid.lower().startswith("agent-"):
                        agent_list.append(aid)
                    else:
                        agent_list.append(aid)

            # Send initial response
            await interaction.response.defer(ephemeral=True)

            # Get project root for loading onboarding messages
            project_root = Path(__file__).parent.parent.parent

            # Execute hard onboarding for each agent
            successful = []
            failed = []

            for agent_id in agent_list:
                try:
                    # Load onboarding message from agent's workspace
                    onboarding_file = project_root / "agent_workspaces" / agent_id / "HARD_ONBOARDING_MESSAGE.md"

                    if onboarding_file.exists():
                        onboarding_message = onboarding_file.read_text(encoding="utf-8")
                    else:
                        # Use default onboarding message if file doesn't exist
                        onboarding_message = f"""🚨 HARD ONBOARD - {agent_id}

**Status**: RESET & ACTIVATE
**Protocol**: Complete session reset

**YOUR MISSION**: Resume autonomous operations immediately.

**NEXT ACTIONS**:
1. Check your inbox for assignments
2. Update your status.json
3. Resume autonomous execution
4. Post devlog when work complete

**WE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀**"""

                    # Execute hard onboarding
                    success = hard_onboard_agent(
                        agent_id=agent_id,
                        onboarding_message=onboarding_message,
                        role=None
                    )

                    if success:
                        successful.append(agent_id)
                    else:
                        failed.append((agent_id, "Hard onboarding service returned False"))
                except Exception as e:
                    failed.append((agent_id, str(e)[:200]))

            # Send results
            if len(successful) == len(agent_list):
                embed = discord.Embed(
                    title="✅ HARD ONBOARD COMPLETE",
                    description=f"All **{len(agent_list)} agent(s)** hard onboarded successfully!",
                    color=discord.Color.green(),
                )
                embed.add_field(
                    name="Activated Agents",
                    value="\n".join([f"✅ {agent}" for agent in successful]),
                    inline=False
                )
            elif successful:
                embed = discord.Embed(
                    title="⚠️ PARTIAL HARD ONBOARD",
                    description=f"**{len(successful)}/{len(agent_list)}** agents onboarded successfully",
                    color=discord.Color.orange(),
                )
                embed.add_field(
                    name="✅ Successful",
                    value="\n".join([f"✅ {agent}" for agent in successful]),
                    inline=False
                )
                if failed:
                    error_list = "\n".join([f"❌ {agent}: {error}" for agent, error in failed[:5]])
                    embed.add_field(name="❌ Failed", value=error_list, inline=False)
            else:
                embed = discord.Embed(
                    title="❌ HARD ONBOARD FAILED",
                    description="All agents failed to onboard",
                    color=discord.Color.red(),
                )
                error_list = "\n".join([f"❌ {agent}: {error}" for agent, error in failed[:5]])
                embed.add_field(name="Errors", value=error_list, inline=False)

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error in hard onboard modal: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


__all__ = [
    "AgentMessageModal",
    "BroadcastMessageModal",
    "JetFuelMessageModal",
    "SelectiveBroadcastModal",
    "JetFuelBroadcastModal",
    "TemplateBroadcastModal",
    "SoftOnboardModal",
    "HardOnboardModal",
]
