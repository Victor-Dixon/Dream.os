"""
Discord Messaging Controller Views
===================================

Discord UI views for agent messaging and swarm status.
Extracted from messaging_controller.py for preventive optimization.

Features:
- Agent selection and messaging view
- Swarm status monitoring view
- Interactive buttons and dropdowns

Author: Agent-7 (original), Agent-1 (preventive refactor)
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

# Discord imports with error handling
try:
    import discord

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    # Create mock discord module for when discord.py is not available

    class MockView:
        def __init__(self, *args, **kwargs):
            pass

        def add_item(self, item):
            pass

    class MockSelect:
        def __init__(self, *args, **kwargs):
            pass

    class MockButton:
        def __init__(self, *args, **kwargs):
            pass

    class MockSelectOption:
        def __init__(self, *args, **kwargs):
            pass

    class MockUI:
        View = MockView
        Select = MockSelect
        Button = MockButton
        SelectOption = MockSelectOption

    class MockButtonStyle:
        primary = "primary"
        secondary = "secondary"

    class MockDiscord:
        class ui:
            View = MockView
            Select = MockSelect
            Button = MockButton
            SelectOption = MockSelectOption
        SelectOption = MockSelectOption
        ButtonStyle = MockButtonStyle
        Interaction = type('Interaction', (), {})()
        Embed = type('Embed', (), {})()
        Color = type('Color', (), {'blue': lambda: None})()

    discord = MockDiscord()

logger = logging.getLogger(__name__)


class AgentMessagingView(discord.ui.View):
    """Discord view for easy agent messaging."""

    def __init__(self, messaging_service):
        super().__init__(timeout=300)  # 5 minute timeout
        self.messaging_service = messaging_service
        self.agents = self._load_agent_list()

        # Create agent selection dropdown
        self.agent_select = discord.ui.Select(
            placeholder="Select an agent to message...", options=self._create_agent_options()
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

    def _load_agent_list(self) -> list[dict[str, Any]]:
        """Load list of available agents."""
        try:
            # First try to get agent data from messaging service
            if hasattr(self.messaging_service, "agent_data") and self.messaging_service.agent_data:
                agents = []
                for agent_id, agent_info in self.messaging_service.agent_data.items():
                    agents.append(
                        {
                            "id": agent_id,
                            "name": agent_info.get("name", agent_id),
                            "status": agent_info.get("active", False),
                            "coordinates": agent_info.get("coordinates", (0, 0)),
                        }
                    )
                if agents:  # Only return if we got agents
                    return agents

            # Fallback: Use StatusReader to get agents from status.json files
            from .status_reader import StatusReader

            status_reader = StatusReader()
            all_statuses = status_reader.read_all_statuses()

            agents = []
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})
                # CRITICAL FIX: Preserve actual status string, don't convert to boolean
                # This ensures status display works correctly
                actual_status = status_data.get("status", "UNKNOWN")
                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", f"Agent-{i}"),
                        "status": actual_status,  # Preserve status string for proper display
                        "coordinates": status_data.get("coordinate_position", f"({i}, {i})"),
                    }
                )

            return agents

        except Exception as e:
            logger.error(f"Error loading agent list: {e}")
            # Emergency fallback: Return static list
            return [
                {"id": f"Agent-{i}", "name": f"Agent-{i}",
                    "status": True, "coordinates": (i, i)}
                for i in range(1, 9)
            ]

    def _create_agent_options(self) -> list[discord.SelectOption]:
        """Create Discord select options for agents."""
        options = []
        for agent in self.agents:
            # CRITICAL FIX: Check status string properly (not boolean)
            status_str = str(agent.get("status", "UNKNOWN")).upper()
            status_emoji = "🟢" if "ACTIVE" in status_str or "JET_FUEL" in status_str else "🔴"
            # Discord label must be 1-45 characters
            agent_name = agent.get('name', agent['id'])
            # Truncate to fit: emoji (2) + space (1) + name (max 42) = 45
            max_name_length = 42
            truncated_name = agent_name[:max_name_length] if len(
                agent_name) > max_name_length else agent_name
            label = f"{status_emoji} {truncated_name}"
            # Ensure label is at least 1 character (fallback to agent ID if needed)
            if not label or len(label.strip()) == 0:
                label = agent['id'][:45]  # Fallback to agent ID, max 45 chars
            # Final validation: ensure 1-45 characters
            label = label[:45] if len(label) > 45 else label
            if len(label) < 1:
                label = agent['id'][:45]  # Final fallback
            # Discord SelectOption value must be <= 20 characters
            option_value = agent["id"]
            if len(option_value) > 20:
                option_value = option_value[:20]
            
            # Description must be <= 100 characters
            description = f"Agent {agent['id']}"
            if len(description) > 100:
                description = description[:100]
            
            options.append(
                discord.SelectOption(
                    label=label,
                    value=option_value,  # Guaranteed <= 20 characters
                    description=description  # Guaranteed <= 100 characters
                )
            )
        return options

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection."""
        try:
            # Import here to avoid circular dependency
            from .messaging_controller_modals import MessageModal

            selected_agent = interaction.data["values"][0]
            modal = MessageModal(selected_agent, self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(
                f"Error opening agent message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )


class SwarmStatusView(discord.ui.View):
    """Discord view for swarm status monitoring."""

    def __init__(self, messaging_service):
        super().__init__(timeout=300)
        self.messaging_service = messaging_service

        # Refresh button
        self.refresh_button = discord.ui.Button(
            label="🔄 Refresh Status", style=discord.ButtonStyle.primary
        )
        self.refresh_button.callback = self.refresh_status
        self.add_item(self.refresh_button)

        # Broadcast message button
        self.broadcast_button = discord.ui.Button(
            label="📢 Broadcast Message", style=discord.ButtonStyle.secondary
        )
        self.broadcast_button.callback = self.broadcast_message
        self.add_item(self.broadcast_button)
    
    async def create_initial_embed(self) -> discord.Embed:
        """Create initial embed when view is first displayed."""
        return await self._create_status_embed()

    async def refresh_status(self, interaction: discord.Interaction):
        """Refresh swarm status."""
        try:
            # Clear cache before refreshing to get latest status
            from .status_reader import StatusReader
            status_reader = StatusReader()
            status_reader.clear_cache()
            
            embed = await self._create_status_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(f"Error refreshing status: {e}", exc_info=True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ Error refreshing status: {e}", ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"❌ Error refreshing status: {e}", ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(
                    f"Error sending error message: {followup_error}", exc_info=True)

    async def broadcast_message(self, interaction: discord.Interaction):
        """Broadcast message to all agents."""
        try:
            # Import here to avoid circular dependency
            from .messaging_controller_modals import BroadcastModal

            modal = BroadcastModal(self.messaging_service)
            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening broadcast modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    async def _create_status_embed(self) -> discord.Embed:
        """Create status embed from actual status.json files."""
        embed = discord.Embed(
            title="🤖 Swarm Status",
            description="**Real-time agent status from status.json files**",
            color=discord.Color.blue(),
            timestamp=datetime.now(),
        )

        try:
            # Use StatusReader to get actual status from status.json files
            from .status_reader import StatusReader
            
            status_reader = StatusReader()
            all_statuses = status_reader.read_all_statuses()
            
            if not all_statuses:
                embed.add_field(
                    name="⚠️ No Status Data",
                    value="No agent status files found. Agents may not be initialized.",
                    inline=False
                )
                return embed
            
            active_count = 0
            total_count = len(all_statuses)
            
            # Sort agents by ID for consistent display
            for agent_id in sorted(all_statuses.keys()):
                status_data = all_statuses[agent_id]
                agent_status = status_data.get("status", "UNKNOWN")
                agent_name = status_data.get("agent_name", agent_id)
                current_mission = status_data.get("current_mission", "No mission assigned")
                current_tasks = status_data.get("current_tasks", [])
                last_updated = status_data.get("last_updated", "Unknown")
                
                # CRITICAL FIX: Properly detect ACTIVE status
                # Check for ACTIVE_AGENT_MODE, ACTIVE, JET_FUEL, etc.
                status_upper = str(agent_status).upper()
                if "ACTIVE" in status_upper or "JET_FUEL" in status_upper or "ACTIVE_AGENT_MODE" in status_upper:
                    emoji = "🟢"
                    active_count += 1
                elif "COMPLETE" in status_upper or "COMPLETED" in status_upper:
                    emoji = "✅"
                elif "REST" in status_upper or "STANDBY" in status_upper or "IDLE" in status_upper:
                    emoji = "💤"
                elif "ERROR" in status_upper or "FAILED" in status_upper:
                    emoji = "🔴"
                else:
                    emoji = "🟡"  # Unknown/Other status
                
                # Truncate mission and task for display (Discord field value limit: 1024 chars)
                mission_display = current_mission[:80] + "..." if len(current_mission) > 80 else current_mission
                
                # Get first task or summary
                if current_tasks:
                    # Take first task and truncate if needed
                    first_task = current_tasks[0]
                    task_display = first_task[:100] + "..." if len(first_task) > 100 else first_task
                else:
                    task_display = "No active tasks"
                
                # Build status value (keep under 1024 chars per Discord limit)
                status_value = (
                    f"**Role:** {agent_name}\n"
                    f"**Status:** {agent_status}\n"
                    f"**Phase:** {status_data.get('current_phase', 'N/A')[:50]}\n"
                    f"**Mission:** {mission_display}\n"
                    f"**Task:** {task_display}"
                )
                
                # Ensure field value doesn't exceed Discord's 1024 character limit
                if len(status_value) > 1024:
                    status_value = status_value[:1020] + "..."
                
                embed.add_field(
                    name=f"{emoji} {agent_id}",
                    value=status_value,
                    inline=False
                )
            
            # Add summary
            embed.add_field(
                name="📊 Summary",
                value=f"**Active:** {active_count}/{total_count} agents\n**Last Updated:** {last_updated if all_statuses else 'Unknown'}",
                inline=False
            )
            
            embed.set_footer(text="🔄 Use refresh button to update • Data from status.json files")
            
        except Exception as e:
            logger.error(f"Error creating status embed: {e}", exc_info=True)
            embed.add_field(
                name="❌ Error",
                value=f"Failed to load agent status: {str(e)}",
                inline=False
            )

        return embed
