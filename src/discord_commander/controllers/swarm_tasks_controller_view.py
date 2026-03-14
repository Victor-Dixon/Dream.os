#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Swarm Tasks Controller - WOW FACTOR Dedicated Controller
=========================================================

Dedicated, standalone controller for swarm tasks and directives display.
Complete GUI interface for real-time task tracking with pagination support.

WOW FACTOR Features:
- Real-time task dashboard
- Full task details (no truncation)
- Pagination for long task lists
- Priority filtering
- Live refresh capability

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-01-27
Status: ✅ WOW FACTOR CONTROLLER
"""

import json
import logging
from pathlib import Path
from typing import Any

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

from ..services.messaging.service_adapters import ConsolidatedMessagingService

logger = logging.getLogger(__name__)

# Discord limits
MAX_EMBED_LENGTH = 6000  # Total embed character limit
MAX_FIELD_VALUE = 1024  # Per field value limit
MAX_FIELDS = 25  # Max fields per embed
MAX_MESSAGE_LENGTH = 2000  # Regular message limit


class SwarmTasksControllerView(discord.ui.View):
    """
    Dedicated Swarm Tasks Controller - WOW FACTOR Standalone Interface.

    Complete task monitoring system in one view:
    - Real-time task dashboard
    - Full task details (no truncation via pagination)
    - Priority filtering
    - Live refresh
    - Pagination controls
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService | None = None):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.messaging_service = messaging_service
        self.workspace_path = Path("agent_workspaces")
        self.current_page = 0
        self.filter_priority = None

        # Navigation buttons - Row 0
        self.prev_btn = discord.ui.Button(
            label="◀ Previous",
            style=discord.ButtonStyle.secondary,
            custom_id="tasks_prev",
            row=0,
            disabled=True,
        )
        self.prev_btn.callback = self.on_previous
        self.add_item(self.prev_btn)

        self.refresh_btn = discord.ui.Button(
            label="Refresh",
            style=discord.ButtonStyle.primary,
            emoji="🔄",
            custom_id="tasks_refresh",
            row=0,
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

        self.next_btn = discord.ui.Button(
            label="Next ▶",
            style=discord.ButtonStyle.secondary,
            custom_id="tasks_next",
            row=0,
        )
        self.next_btn.callback = self.on_next
        self.add_item(self.next_btn)

        # Filter buttons - Row 1
        self.filter_all_btn = discord.ui.Button(
            label="All",
            style=discord.ButtonStyle.primary,
            emoji="📋",
            custom_id="tasks_filter_all",
            row=1,
        )
        self.filter_all_btn.callback = self.on_filter_all
        self.add_item(self.filter_all_btn)

        self.filter_critical_btn = discord.ui.Button(
            label="Critical",
            style=discord.ButtonStyle.danger,
            emoji="🔴",
            custom_id="tasks_filter_critical",
            row=1,
        )
        self.filter_critical_btn.callback = self.on_filter_critical
        self.add_item(self.filter_critical_btn)

        self.filter_high_btn = discord.ui.Button(
            label="High",
            style=discord.ButtonStyle.primary,
            emoji="🟠",
            custom_id="tasks_filter_high",
            row=1,
        )
        self.filter_high_btn.callback = self.on_filter_high
        self.add_item(self.filter_high_btn)

    async def on_previous(self, interaction: discord.Interaction):
        """Go to previous page."""
        try:
            if self.current_page > 0:
                self.current_page -= 1
                embeds = self._create_tasks_embeds()
                await self._update_message(interaction, embeds)
        except Exception as e:
            logger.error(f"Error going to previous page: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error: {e}")

    async def on_next(self, interaction: discord.Interaction):
        """Go to next page."""
        try:
            embeds = self._create_tasks_embeds()
            if self.current_page < len(embeds) - 1:
                self.current_page += 1
                await self._update_message(interaction, embeds)
        except Exception as e:
            logger.error(f"Error going to next page: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error: {e}")

    async def on_refresh(self, interaction: discord.Interaction):
        """Refresh tasks display."""
        try:
            self.current_page = 0
            embeds = self._create_tasks_embeds()
            await self._update_message(interaction, embeds)
        except Exception as e:
            logger.error(f"Error refreshing tasks: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error: {e}")

    async def on_filter_all(self, interaction: discord.Interaction):
        """Show all priorities."""
        try:
            self.filter_priority = None
            self.current_page = 0
            embeds = self._create_tasks_embeds()
            await self._update_message(interaction, embeds)
        except Exception as e:
            logger.error(f"Error filtering all: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error: {e}")

    async def on_filter_critical(self, interaction: discord.Interaction):
        """Show only critical priority."""
        try:
            self.filter_priority = "CRITICAL"
            self.current_page = 0
            embeds = self._create_tasks_embeds()
            await self._update_message(interaction, embeds)
        except Exception as e:
            logger.error(f"Error filtering critical: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error: {e}")

    async def on_filter_high(self, interaction: discord.Interaction):
        """Show only high priority."""
        try:
            self.filter_priority = "HIGH"
            self.current_page = 0
            embeds = self._create_tasks_embeds()
            await self._update_message(interaction, embeds)
        except Exception as e:
            logger.error(f"Error filtering high: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error: {e}")

    async def _update_message(self, interaction: discord.Interaction, embeds: list[discord.Embed]):
        """Update message with current page and button states."""
        try:
            # Update button states
            self.prev_btn.disabled = self.current_page == 0
            self.next_btn.disabled = self.current_page >= len(embeds) - 1

            # Send or edit message
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    embed=embeds[self.current_page], view=self, ephemeral=True
                )
            else:
                await interaction.edit_original_response(
                    embed=embeds[self.current_page], view=self
                )
        except Exception as e:
            logger.error(f"Error updating message: {e}", exc_info=True)
            await self._send_error(interaction, f"❌ Error updating: {e}")

    async def _send_error(self, interaction: discord.Interaction, message: str):
        """Send error message with proper response handling."""
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(message, ephemeral=True)
            else:
                await interaction.followup.send(message, ephemeral=True)
        except Exception as followup_error:
            logger.error(
                f"Error sending error message: {followup_error}", exc_info=True)

    def _create_tasks_embeds(self) -> list[discord.Embed]:
        """Create paginated embeds for tasks (handles long content)."""
        agents_data = self._load_all_agent_statuses()

        # Filter by priority if set
        if self.filter_priority:
            agents_data = [
                a for a in agents_data
                if a.get("mission_priority", "").upper() == self.filter_priority.upper()
            ]

        # Sort by priority
        priority_order = {"CRITICAL": 0, "HIGH": 1,
                          "ACTIVE": 2, "MEDIUM": 3, "LOW": 4}
        sorted_agents = sorted(
            agents_data,
            key=lambda x: priority_order.get(
                x.get("mission_priority", "MEDIUM"), 5)
        )

        # Split into pages (max 4 agents per page to avoid truncation)
        agents_per_page = 4
        pages = []

        for i in range(0, len(sorted_agents), agents_per_page):
            page_agents = sorted_agents[i:i + agents_per_page]
            embed = self._create_page_embed(
                page_agents, i // agents_per_page + 1, len(sorted_agents), agents_data)
            pages.append(embed)

        # If no pages, create empty page
        if not pages:
            embed = discord.Embed(
                title="🐝 SWARM TASKS & DIRECTIVES DASHBOARD",
                description="**No tasks found** (filtered or no active agents)",
                color=0x2ECC71,
                timestamp=discord.utils.utcnow(),
            )
            pages.append(embed)

        return pages

    def _calculate_embed_size(self, embed: discord.Embed) -> int:
        """Calculate total character count of embed."""
        size = 0
        if embed.title:
            size += len(embed.title)
        if embed.description:
            size += len(embed.description)
        if embed.footer and embed.footer.text:
            size += len(embed.footer.text)
        for field in embed.fields:
            size += len(field.name) + len(field.value)
        return size

    def _create_page_embed(self, agents: list[dict], page_num: int, total_agents: int, all_agents_data: list[dict]) -> discord.Embed:
        """Create a single page embed with full task details."""
        embed = discord.Embed(
            title="🐝 SWARM TASKS & DIRECTIVES DASHBOARD",
            description="**Current missions across all agents** 🚀",
            color=0x2ECC71,
            timestamp=discord.utils.utcnow(),
        )

        # Track embed size to prevent exceeding 6000 char limit
        base_size = self._calculate_embed_size(embed)
        safe_limit = MAX_EMBED_LENGTH - 500  # Leave 500 char buffer for footer and formatting

        # Add agent tasks with FULL details (no truncation)
        for agent in agents:
            agent_id = agent.get("agent_id", "Unknown")
            mission = agent.get("current_mission", "No active mission")
            tasks = agent.get("current_tasks", [])
            priority = agent.get("mission_priority", "MEDIUM")

            # Priority emoji
            priority_emoji = {
                "CRITICAL": "🔴",
                "HIGH": "🟠",
                "ACTIVE": "🟢",
                "MEDIUM": "🟡",
                "LOW": "⚪"
            }.get(priority, "🔵")

            # Format tasks with FULL content (split into multiple fields if needed)
            if tasks:
                # Create task list with full content
                task_parts = []
                current_part = ""

                for task in tasks:
                    task_line = f"• {task}\n"
                    # If adding this task would exceed field limit, start new field
                    if len(current_part) + len(task_line) > MAX_FIELD_VALUE - 50:
                        if current_part:
                            task_parts.append(current_part.strip())
                        current_part = task_line
                    else:
                        current_part += task_line

                if current_part:
                    task_parts.append(current_part.strip())

                # Add first task part as main field
                if task_parts:
                    field_name = f"{priority_emoji} {agent_id} - {priority}"
                    field_value = f"**Mission:** {mission}\n\n**Tasks:**\n{task_parts[0]}"
                    
                    # Check if adding this field would exceed limit
                    current_size = self._calculate_embed_size(embed)
                    if current_size + len(field_name) + len(field_value) > safe_limit:
                        # Truncate tasks if needed
                        task_lines = task_parts[0].split('\n')
                        if len(task_lines) > 5:
                            truncated = '\n'.join(task_lines[:5])
                            field_value = f"**Mission:** {mission}\n\n**Tasks:**\n{truncated}\n... (showing 5 of {len(tasks)} tasks)"
                        else:
                            # Truncate field value itself if still too long
                            max_value_size = safe_limit - current_size - len(field_name) - 100
                            if len(field_value) > max_value_size:
                                field_value = field_value[:max_value_size-20] + "\n... (truncated)"
                            # If still can't fit, skip remaining agents
                            if current_size + len(field_name) + len(field_value) > safe_limit:
                                break
                    
                    embed.add_field(
                        name=field_name,
                        value=field_value,
                        inline=False
                    )

                    # Add additional task parts as continuation fields (if space allows)
                    for i, part in enumerate(task_parts[1:], 1):
                        current_size = self._calculate_embed_size(embed)
                        continuation_name = f"  └─ {agent_id} (continued)"
                        continuation_size = len(continuation_name) + len(part)
                        
                        if current_size + continuation_size > safe_limit:
                            # Truncate continuation if possible
                            max_part_size = safe_limit - current_size - len(continuation_name) - 50
                            if max_part_size > 100:
                                part = part[:max_part_size] + "\n... (truncated)"
                                continuation_size = len(continuation_name) + len(part)
                            
                            # If still can't fit, skip this and remaining continuation fields
                            if current_size + continuation_size > safe_limit:
                                break
                        
                        embed.add_field(
                            name=continuation_name,
                            value=part,
                            inline=False
                        )
                else:
                    embed.add_field(
                        name=f"{priority_emoji} {agent_id} - {priority}",
                        value=f"**Mission:** {mission}\n\n**Tasks:** No tasks listed",
                        inline=False
                    )
            else:
                field_name = f"{priority_emoji} {agent_id} - {priority}"
                field_value = f"**Mission:** {mission}\n\n**Tasks:** No specific tasks listed"
                
                # Check if adding this field would exceed limit
                current_size = self._calculate_embed_size(embed)
                if current_size + len(field_name) + len(field_value) > safe_limit:
                    # Skip remaining agents if we're at limit
                    break
                
                embed.add_field(
                    name=field_name,
                    value=field_value,
                    inline=False
                )

        # Add footer with pagination and statistics
        all_agents = self._load_all_agent_statuses()
        if self.filter_priority:
            filtered_agents = [a for a in all_agents if a.get(
                "mission_priority", "").upper() == self.filter_priority.upper()]
        else:
            filtered_agents = all_agents
        total_tasks = sum(len(a.get("current_tasks", []))
                          for a in filtered_agents)
        active_agents = sum(1 for a in all_agents if a.get(
            "status") == "ACTIVE_AGENT_MODE")

        footer_text = f"🐝 {active_agents}/8 agents active • {total_tasks} total tasks"
        if len(agents) < total_agents:
            footer_text += f" • Page {page_num} of {(total_agents + 3) // 4}"
        footer_text += " • WE ARE SWARM"

        embed.set_footer(text=footer_text)
        
        # Final validation - ensure embed doesn't exceed limit
        final_size = self._calculate_embed_size(embed)
        if final_size > MAX_EMBED_LENGTH:
            logger.warning(f"Embed size {final_size} exceeds limit {MAX_EMBED_LENGTH}, truncating footer")
            # Truncate footer if needed
            max_footer = MAX_EMBED_LENGTH - (final_size - len(footer_text))
            if max_footer > 50:
                embed.set_footer(text=footer_text[:max_footer-3] + "...")
            else:
                embed.set_footer(text="🐝 SWARM")
        
        return embed

    def _load_all_agent_statuses(self) -> list[dict[str, Any]]:
        """Load status for all agents."""
        agents = []

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status_file = self.workspace_path / agent_id / "status.json"

            if not status_file.exists():
                continue

            try:
                with open(status_file, "r", encoding="utf-8") as f:
                    status = json.load(f)
                    agents.append(status)
            except Exception as e:
                logger.warning(f"Could not load status for {agent_id}: {e}")

        return agents

    def create_initial_embed(self) -> discord.Embed:
        """Create initial embed for first display."""
        embeds = self._create_tasks_embeds()
        return embeds[0] if embeds else discord.Embed(title="🐝 SWARM TASKS", description="Loading...")


__all__ = ["SwarmTasksControllerView"]