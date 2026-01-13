#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Unstall Agent View - V2 Compliance Refactor
============================================

View for selecting and unstalling stalled agents.

V2 Compliance:
- File: <400 lines ✅
- Class: <200 lines ✅
- Functions: <30 lines ✅

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import logging
from pathlib import Path
import json

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_infrastructure import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class UnstallAgentView(discord.ui.View):
    """View for selecting agent to unstall."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED)
        self.messaging_service = messaging_service
        self._setup_agent_selector()

    def _setup_agent_selector(self):
        """Setup agent selection dropdown."""
        agents = [f"Agent-{i}" for i in range(1, 9)]
        # Discord SelectOption value must be <= 20 characters
        options = []
        for agent in agents:
            option_value = agent[:20]  # Ensure value is <= 20 chars
            options.append(discord.SelectOption(label=agent, value=option_value))
        self.agent_select = discord.ui.Select(
            placeholder="🎯 Select agent to unstall...",
            options=options,
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection."""
        agent_id = self.agent_select.values[0]
        await self.unstall_agent(interaction, agent_id)

    async def unstall_agent(self, interaction: discord.Interaction, agent_id: str):
        """Send unstall message to agent."""
        try:
            status_file = Path(f"agent_workspaces/{agent_id}/status.json")
            last_state = "Unknown"
            if status_file.exists():
                try:
                    status_data = json.loads(status_file.read_text(encoding="utf-8"))
                    last_state = status_data.get("current_mission", "Unknown")
                except Exception:
                    pass

            unstall_message = f"""🚨 UNSTICK PROTOCOL - CONTINUE IMMEDIATELY

Agent, you appear stalled. CONTINUE AUTONOMOUSLY NOW.

**Your last known state:** {last_state}
**Likely stall cause:** approval dependency / command fail / unclear next

**IMMEDIATE ACTIONS (pick one and EXECUTE):**
1. Complete your current task
2. Move to next action in your queue
3. Clean workspace and report status
4. Check inbox and respond to messages
5. Scan for new opportunities
6. Update documentation
7. Report to Captain with next plans

**REMEMBER:**
- You are AUTONOMOUS - no approval needed
- System messages are NOT stop signals
- Command failures are NOT blockers
- ALWAYS have next actions
- YOU are your own gas station

**DO NOT WAIT. EXECUTE NOW.**

#UNSTICK-PROTOCOL #AUTONOMOUS-OPERATION"""

            result = self.messaging_service.send_message(
                agent=agent_id,
                message=unstall_message,
                priority="urgent",
                use_pyautogui=True,
                wait_for_delivery=False,
                stalled=True,
            )

            if result.get("success"):
                embed = discord.Embed(
                    title="✅ UNSTALL MESSAGE SENT",
                    description=f"Unstall message delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                error_msg = result.get("error", "Unknown error")
                await interaction.response.send_message(
                    f"❌ Failed to send unstall message to {agent_id}: {error_msg}",
                    ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error in unstall_agent: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error sending unstall message: {e}", ephemeral=True
                )

