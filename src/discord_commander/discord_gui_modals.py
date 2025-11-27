#!/usr/bin/env python3
"""
Discord GUI Modals - Agent Messaging Modals
============================================

Discord UI Modals for message composition.

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import logging

# Discord imports with error handling
try:
    import discord

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    # Create mock discord module for when discord.py is not available
    class MockTextInput:
        def __init__(self, *args, **kwargs):
            pass
    
    class MockModal:
        def __init__(self, *args, **kwargs):
            pass
        def add_item(self, item):
            pass
    
    class MockUI:
        Modal = MockModal
        TextInput = MockTextInput
    
    class MockTextStyle:
        paragraph = "paragraph"
    
    class MockDiscord:
        class ui:
            Modal = MockModal
            TextInput = MockTextInput
        TextStyle = MockTextStyle
        Interaction = type('Interaction', (), {})()
    
    discord = MockDiscord()

from src.services.messaging_infrastructure import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class AgentMessageModal(discord.ui.Modal):
    """Modal for composing message to specific agent."""

    def __init__(self, agent_id: str, messaging_service: ConsolidatedMessagingService):
        super().__init__(title=f"Message to {agent_id}")
        self.agent_id = agent_id
        self.messaging_service = messaging_service

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Message (Shift+Enter for line breaks)",
            placeholder=f"Enter message for {agent_id}...\n\nTip: Use Shift+Enter to add line breaks",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority dropdown (added as text for modal compatibility)
        self.priority_input = discord.ui.TextInput(
            label="Priority (regular/urgent)",
            placeholder="regular",
            default="regular",
            required=False,
            max_length=10,
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            # Send message (don't wait for delivery - queue processor handles it)
            # Discord requires response within 3 seconds, so we can't wait for delivery
            result = self.messaging_service.send_message(
                agent=self.agent_id, 
                message=message, 
                priority=priority, 
                use_pyautogui=True,
                wait_for_delivery=False,  # Don't wait - queue processor will handle delivery
            )

            if result.get("success"):
                queue_id = result.get("queue_id", "unknown")
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                
                await interaction.response.send_message(
                    f"✅ Message queued for {self.agent_id}!\n\n"
                    f"**Queue ID:** `{queue_id}`\n"
                    f"**Status:** Queued (queue processor will deliver)\n\n"
                    f"**Message Preview:**\n```\n{message_preview}\n```\n\n"
                    f"💡 Message will be delivered by the queue processor. "
                    f"If it doesn't appear, check queue processor logs.",
                    ephemeral=True,
                )
                logger.info(f"✅ Discord GUI: Message queued {queue_id} → {self.agent_id}")
            else:
                error_msg = result.get('message', result.get('error', 'Unknown error'))
                logger.error(f"❌ Discord GUI: Failed to queue message to {self.agent_id}: {error_msg}")
                await interaction.response.send_message(
                    f"❌ Failed to queue message for {self.agent_id}.\n\n"
                    f"**Error:** {error_msg}\n\n"
                    f"💡 Check if queue processor is running.",
                    ephemeral=True,
                )

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class BroadcastMessageModal(discord.ui.Modal):
    """Modal for broadcasting message to all agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="Broadcast to All Agents")
        self.messaging_service = messaging_service

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Broadcast Message (Shift+Enter)",
            placeholder="Enter message for all agents...\n\nTip: Use Shift+Enter to add line breaks",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority input
        self.priority_input = discord.ui.TextInput(
            label="Priority (regular/urgent)",
            placeholder="regular",
            default="regular",
            required=False,
            max_length=10,
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        # Defer response immediately for long-running operation
        await interaction.response.defer(ephemeral=True)
        
        try:
            message = self.message_input.value
            priority = self.priority_input.value.strip().lower() or "regular"
            
            # Validate priority
            if priority not in ["regular", "urgent"]:
                priority = "regular"
                logger.warning(f"Invalid priority '{self.priority_input.value}', defaulting to 'regular'")

            # Broadcast to all agents
            agents = [f"Agent-{i}" for i in range(1, 9)]
            success_count = 0
            errors = []

            logger.info(f"📢 Starting broadcast to {len(agents)} agents...")

            for agent in agents:
                try:
                    result = self.messaging_service.send_message(
                        agent=agent, 
                        message=message, 
                        priority=priority, 
                        use_pyautogui=True,
                        wait_for_delivery=False,  # Don't wait - queue processor handles delivery
                    )
                    if result.get("success"):
                        success_count += 1
                        logger.debug(f"✅ Queued message for {agent}")
                    else:
                        error_msg = result.get("error") or result.get("message", "Unknown error")
                        errors.append(f"{agent}: {error_msg}")
                        logger.warning(f"⚠️ Failed to queue message for {agent}: {error_msg}")
                except Exception as e:
                    error_msg = str(e)
                    errors.append(f"{agent}: {error_msg}")
                    logger.error(f"❌ Exception queuing message for {agent}: {e}", exc_info=True)

            # Send result (using followup since we deferred)
            if success_count == len(agents):
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.followup.send(
                    f"✅ Broadcast sent to all {len(agents)} agents!\n\n"
                    f"**Message Preview:**\n```\n{message_preview}\n```\n\n"
                    f"💡 Messages queued - queue processor will deliver them.",
                    ephemeral=True,
                )
                logger.info(f"✅ Broadcast complete: {success_count}/{len(agents)} successful")
            else:
                error_msg = "\n".join(errors[:5])  # Show first 5 errors
                message_preview = message if len(message) <= 300 else message[:297] + "..."
                await interaction.followup.send(
                    f"⚠️ Partial broadcast: {success_count}/{len(agents)} successful\n\n"
                    f"**Message:**\n```\n{message_preview}\n```\n\n"
                    f"**Errors ({len(errors)} total):**\n{error_msg}",
                    ephemeral=True,
                )
                logger.warning(f"⚠️ Broadcast partial: {success_count}/{len(agents)} successful, {len(errors)} errors")

        except Exception as e:
            logger.error(f"❌ Error in broadcast modal: {e}", exc_info=True)
            try:
                await interaction.followup.send(
                    f"❌ Error broadcasting: {e}\n\n"
                    f"💡 Check logs for details.",
                    ephemeral=True,
                )
            except Exception as followup_error:
                logger.error(f"❌ Failed to send error followup: {followup_error}")


class JetFuelMessageModal(discord.ui.Modal):
    """Modal for sending Jet Fuel (AGI activation) message to agent."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="🚀 Jet Fuel Message - AGI Activation")
        self.messaging_service = messaging_service

        # Agent selection
        self.agent_input = discord.ui.TextInput(
            label="Agent ID",
            placeholder="Agent-1, Agent-2, etc.",
            required=True,
            max_length=20,
        )
        self.add_item(self.agent_input)

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Jet Fuel Message (Shift+Enter)",
            placeholder="Enter Jet Fuel message...\n\nTip: Jet Fuel messages grant full AGI autonomy!",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            agent_id = self.agent_input.value.strip()
            message = self.message_input.value

            # Prepend Jet Fuel header
            jet_fuel_message = f"🚀 JET FUEL MESSAGE - AUTONOMOUS MODE ACTIVATED\n\n{message}"

            # Send message with urgent priority (don't wait for delivery - queue processor handles it)
            result = self.messaging_service.send_message(
                agent=agent_id, 
                message=jet_fuel_message, 
                priority="urgent", 
                use_pyautogui=True,
                wait_for_delivery=False,  # Don't wait - queue processor will handle delivery
            )

            if result.get("success"):
                queue_id = result.get("queue_id", "unknown")
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.response.send_message(
                    f"✅ Jet Fuel message queued for {agent_id}!\n\n"
                    f"**Queue ID:** `{queue_id}`\n"
                    f"**Status:** Queued (queue processor will deliver)\n\n"
                    f"**AGI Activation:** 🚀\n**Message Preview:**\n```\n{message_preview}\n```\n\n"
                    f"💡 Message will be delivered by the queue processor. "
                    f"If it doesn't appear, check queue processor logs.",
                    ephemeral=True,
                )
                logger.info(f"✅ Discord GUI: Jet Fuel message queued {queue_id} → {agent_id}")
            else:
                await interaction.response.send_message(
                    f"❌ Failed to send Jet Fuel message: {result.get('error')}", ephemeral=True
                )

        except Exception as e:
            logger.error(f"Error sending Jet Fuel message: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class SelectiveBroadcastModal(discord.ui.Modal):
    """Modal for broadcasting to selected agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService, default_agents: list[str] | None = None):
        super().__init__(title="Broadcast to Selected Agents")
        self.messaging_service = messaging_service
        self.default_agents = default_agents or []

        # Agent selection
        agent_placeholder = ", ".join(default_agents) if default_agents else "Agent-1, Agent-2, Agent-3..."
        self.agent_input = discord.ui.TextInput(
            label="Agent IDs (comma-separated)",
            placeholder=agent_placeholder,
            default=agent_placeholder if default_agents else None,
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Broadcast Message (Shift+Enter)",
            placeholder="Enter message for selected agents...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority input
        self.priority_input = discord.ui.TextInput(
            label="Priority (regular/urgent)",
            placeholder="regular",
            default="regular",
            required=False,
            max_length=10,
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            agent_ids_str = self.agent_input.value.strip()
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            # Parse agent IDs
            agent_ids = [aid.strip() for aid in agent_ids_str.split(",") if aid.strip()]

            if not agent_ids:
                await interaction.response.send_message("❌ No agents specified!", ephemeral=True)
                return

            # Send to selected agents
            success_count = 0
            errors = []

            for agent_id in agent_ids:
                result = self.messaging_service.send_message(
                    agent=agent_id, 
                    message=message, 
                    priority=priority, 
                    use_pyautogui=True,
                    wait_for_delivery=False,  # Don't wait - queue processor handles delivery
                )
                if result.get("success"):
                    success_count += 1
                else:
                    errors.append(f"{agent_id}: {result.get('error', 'Unknown error')}")

            # Send result
            if success_count == len(agent_ids):
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.response.send_message(
                    f"✅ Broadcast sent to {success_count} agent(s)!\n\n**Message Preview:**\n```\n{message_preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = "\n".join(errors[:3])
                await interaction.response.send_message(
                    f"⚠️ Partial broadcast: {success_count}/{len(agent_ids)} successful\n\n**Errors:**\n{error_msg}",
                    ephemeral=True,
                )

        except Exception as e:
            logger.error(f"Error in selective broadcast: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class JetFuelBroadcastModal(discord.ui.Modal):
    """Modal for Jet Fuel broadcast to all agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="🚀 Jet Fuel Broadcast - AGI Activation for All")
        self.messaging_service = messaging_service

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Jet Fuel Message (Shift+Enter)",
            placeholder="Enter Jet Fuel message for all agents...\n\nTip: Jet Fuel = AGI autonomy!",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value

            # Prepend Jet Fuel header
            jet_fuel_message = f"🚀 JET FUEL MESSAGE - AUTONOMOUS MODE ACTIVATED\n\n{message}"

            # Broadcast to all agents with urgent priority
            agents = [f"Agent-{i}" for i in range(1, 9)]
            success_count = 0
            errors = []

            for agent in agents:
                result = self.messaging_service.send_message(
                    agent=agent, 
                    message=jet_fuel_message, 
                    priority="urgent", 
                    use_pyautogui=True,
                    wait_for_delivery=False,  # Don't wait - queue processor handles delivery
                )
                if result.get("success"):
                    success_count += 1
                else:
                    errors.append(f"{agent}: {result.get('error', 'Unknown error')}")

            # Send result
            if success_count == len(agents):
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.response.send_message(
                    f"✅ Jet Fuel broadcast sent to all {len(agents)} agents!\n\n**AGI Activation:** 🚀🚀🚀\n**Message Preview:**\n```\n{message_preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = "\n".join(errors[:3])
                await interaction.response.send_message(
                    f"⚠️ Partial Jet Fuel broadcast: {success_count}/{len(agents)} successful\n\n**Errors:**\n{error_msg}",
                    ephemeral=True,
                )

        except Exception as e:
            logger.error(f"Error in Jet Fuel broadcast: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class TemplateBroadcastModal(discord.ui.Modal):
    """Modal for broadcasting with template pre-filled content."""

    def __init__(
        self,
        messaging_service: ConsolidatedMessagingService,
        template_message: str,
        template_priority: str = "regular",
    ):
        super().__init__(title="Broadcast with Template")
        self.messaging_service = messaging_service

        # Message input with template pre-filled (Discord doesn't support defaults, so we use placeholder)
        self.message_input = discord.ui.TextInput(
            label="Broadcast Message (Template)",
            placeholder=template_message[:500] + "..." if len(template_message) > 500 else template_message,
            default=template_message,  # This will pre-fill the field
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority input with template priority
        self.priority_input = discord.ui.TextInput(
            label="Priority (regular/urgent)",
            placeholder=template_priority,
            default=template_priority,
            required=False,
            max_length=10,
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            # Broadcast to all agents
            agents = [f"Agent-{i}" for i in range(1, 9)]
            success_count = 0
            errors = []

            for agent in agents:
                result = self.messaging_service.send_message(
                    agent=agent, 
                    message=message, 
                    priority=priority, 
                    use_pyautogui=True,
                    wait_for_delivery=False,  # Don't wait - queue processor handles delivery
                )
                if result.get("success"):
                    success_count += 1
                else:
                    errors.append(f"{agent}: {result.get('error', 'Unknown error')}")

            # Send result
            if success_count == len(agents):
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.response.send_message(
                    f"✅ Template broadcast sent to all {len(agents)} agents!\n\n**Message Preview:**\n```\n{message_preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = "\n".join(errors[:3])  # Show first 3 errors
                message_preview = message if len(message) <= 300 else message[:297] + "..."
                await interaction.response.send_message(
                    f"⚠️ Partial broadcast: {success_count}/{len(agents)} successful\n\n"
                    f"**Message:**\n```\n{message_preview}\n```\n"
                    f"**Errors:**\n{error_msg}",
                    ephemeral=True,
                )

        except Exception as e:
            logger.error(f"Error broadcasting template: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class SoftOnboardModal(discord.ui.Modal):
    """Modal for soft onboarding an agent."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="🚀 Soft Onboard Agent")
        self.messaging_service = messaging_service

        # Agent ID input (supports single or comma-separated)
        self.agent_input = discord.ui.TextInput(
            label="Agent ID(s) - Single or comma-separated",
            placeholder="Agent-1 or Agent-1,Agent-2,Agent-3",
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

        # Optional message input
        self.message_input = discord.ui.TextInput(
            label="Onboarding Message (Optional)",
            placeholder="Leave empty for default message...",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=2000,
        )
        self.add_item(self.message_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            import subprocess

            agent_ids_str = self.agent_input.value.strip()
            message = self.message_input.value.strip() if self.message_input.value else None

            # Parse agent IDs
            agent_list = [aid.strip() for aid in agent_ids_str.split(",") if aid.strip()]

            if not agent_list:
                await interaction.response.send_message("❌ No valid agents specified", ephemeral=True)
                return

            # Default message if not provided
            if not message:
                message = "🚀 SOFT ONBOARD - Agent activation initiated. Check your inbox and begin autonomous operations."

            # Send initial response
            embed = discord.Embed(
                title="🚀 SOFT ONBOARD INITIATED",
                description=f"Soft onboarding **{len(agent_list)} agent(s)**...\n\n**Agents:** {', '.join(agent_list)}",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Execute soft onboard for each agent
            successful = []
            failed = []

            for agent_id in agent_list:
                try:
                    # Use absolute path to ensure reliable execution
                    project_root = Path(__file__).parent.parent.parent
                    cli_path = project_root / 'tools' / 'soft_onboard_cli.py'
                    cmd = ['python', str(cli_path), '--agent', agent_id, '--message', message]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(project_root))

                    if result.returncode == 0:
                        successful.append(agent_id)
                    else:
                        error_msg = result.stderr[:200] if result.stderr else "Unknown error"
                        failed.append((agent_id, error_msg))
                except subprocess.TimeoutExpired:
                    failed.append((agent_id, "Timeout after 2 minutes"))
                except Exception as e:
                    failed.append((agent_id, str(e)[:200]))

            # Send results
            if len(successful) == len(agent_list):
                success_embed = discord.Embed(
                    title="✅ SOFT ONBOARD COMPLETE",
                    description=f"All **{len(agent_list)} agent(s)** soft onboarded successfully!",
                    color=discord.Color.green(),
                )
                success_embed.add_field(
                    name="✅ Successful", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                await interaction.followup.send(embed=success_embed, ephemeral=True)
            elif successful:
                partial_embed = discord.Embed(
                    title="⚠️ PARTIAL SOFT ONBOARD",
                    description=f"**{len(successful)}/{len(agent_list)}** agents onboarded successfully",
                    color=discord.Color.orange(),
                )
                partial_embed.add_field(
                    name="✅ Successful", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                if failed:
                    error_list = "\n".join([f"❌ {agent}: {error}" for agent, error in failed[:5]])
                    partial_embed.add_field(name="❌ Failed", value=error_list, inline=False)
                await interaction.followup.send(embed=partial_embed, ephemeral=True)
            else:
                error_embed = discord.Embed(
                    title="❌ SOFT ONBOARD FAILED",
                    description="All agents failed to onboard",
                    color=discord.Color.red(),
                )
                error_list = "\n".join([f"❌ {agent}: {error}" for agent, error in failed[:5]])
                error_embed.add_field(name="Errors", value=error_list, inline=False)
                await interaction.followup.send(embed=error_embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error in soft onboard modal: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


class HardOnboardModal(discord.ui.Modal):
    """Modal for hard onboarding agent(s)."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="🐝 Hard Onboard Agent(s)")
        self.messaging_service = messaging_service

        # Agent ID input (supports single or comma-separated)
        self.agent_input = discord.ui.TextInput(
            label="Agent ID(s) - Single or comma-separated (or 'all')",
            placeholder="Agent-1 or Agent-1,Agent-2,Agent-3 or 'all'",
            required=True,
            max_length=200,
        )
        self.add_item(self.agent_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            import subprocess

            agent_ids_str = self.agent_input.value.strip()

            # Parse agent IDs
            if agent_ids_str.lower() == "all":
                agent_list = [f"Agent-{i}" for i in range(1, 9)]
            else:
                agent_list = [aid.strip() for aid in agent_ids_str.split(",") if aid.strip()]

            if not agent_list:
                await interaction.response.send_message("❌ No valid agents specified", ephemeral=True)
                return

            # Send initial response
            embed = discord.Embed(
                title="🚀 HARD ONBOARD INITIATED",
                description=f"Hard onboarding **{len(agent_list)} agent(s)**...\n\n**Agents:** {', '.join(agent_list)}",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Hard onboard each agent
            successful = []
            failed = []

            for agent_id in agent_list:
                try:
                    # Use absolute path to ensure reliable execution
                    project_root = Path(__file__).parent.parent.parent
                    cli_path = project_root / 'tools' / 'captain_hard_onboard_agent.py'
                    result = subprocess.run(
                        ['python', str(cli_path), agent_id],
                        capture_output=True,
                        text=True,
                        timeout=60,
                        cwd=str(project_root)
                    )

                    if result.returncode == 0:
                        successful.append(agent_id)
                    else:
                        error_msg = result.stderr[:200] if result.stderr else "Unknown error"
                        failed.append((agent_id, error_msg))
                except subprocess.TimeoutExpired:
                    failed.append((agent_id, "Timeout after 60 seconds"))
                except Exception as e:
                    failed.append((agent_id, str(e)[:200]))

            # Send results
            if len(successful) == len(agent_list):
                success_embed = discord.Embed(
                    title="✅ HARD ONBOARD COMPLETE!",
                    description=f"All **{len(agent_list)} agent(s)** hard onboarded successfully!",
                    color=discord.Color.green(),
                )
                success_embed.add_field(
                    name="✅ Activated Agents", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                success_embed.add_field(
                    name="Next Steps",
                    value="1. Check agent workspaces for onboarding messages\n2. Use !status to verify agents active\n3. Begin mission assignments",
                    inline=False,
                )
                await interaction.followup.send(embed=success_embed, ephemeral=True)
            elif successful:
                partial_embed = discord.Embed(
                    title="⚠️ PARTIAL HARD ONBOARD",
                    description=f"**{len(successful)}/{len(agent_list)}** agents onboarded successfully",
                    color=discord.Color.orange(),
                )
                partial_embed.add_field(
                    name="✅ Successful", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                if failed:
                    error_list = "\n".join([f"❌ {agent}: {error}" for agent, error in failed[:5]])
                    partial_embed.add_field(name="❌ Failed", value=error_list, inline=False)
                await interaction.followup.send(embed=partial_embed, ephemeral=True)
            else:
                error_embed = discord.Embed(
                    title="❌ HARD ONBOARD FAILED",
                    description="All agents failed to onboard",
                    color=discord.Color.red(),
                )
                error_list = "\n".join([f"❌ {agent}: {error}" for agent, error in failed[:5]])
                error_embed.add_field(name="Errors", value=error_list, inline=False)
                await interaction.followup.send(embed=error_embed, ephemeral=True)

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
