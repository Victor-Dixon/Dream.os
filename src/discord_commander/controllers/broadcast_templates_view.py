#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Broadcast Templates View - Interactive Template System
======================================================

Interactive template system for broadcast messages organized by mode.
Templates are clickable buttons that populate broadcast modals.

Modes:
- Regular: Standard coordination messages
- Urgent: High-priority notifications
- Jet Fuel: AGI activation messages
- Task Assignment: Task-related broadcasts
- Status: Status check and coordination
- Coordination: Swarm coordination messages

Author: Agent-3 (Infrastructure & DevOps)
Created: 2025-01-27
Status: ✅ WOW FACTOR TEMPLATE SYSTEM
"""

import logging

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_infrastructure import ConsolidatedMessagingService

# Import enhanced templates (optional - falls back to original if unavailable)
try:
    from ..templates.broadcast_templates import (
        ENHANCED_BROADCAST_TEMPLATES,
    )
    USE_ENHANCED_TEMPLATES = True
except ImportError:
    try:
        from ..discord_template_collection import (
            ENHANCED_BROADCAST_TEMPLATES,
        )
        USE_ENHANCED_TEMPLATES = True
    except ImportError:
        USE_ENHANCED_TEMPLATES = False

logger = logging.getLogger(__name__)


# Template definitions organized by mode
BROADCAST_TEMPLATES = {
    "regular": [
        {
            "name": "Task Assignment",
            "emoji": "🎯",
            "message": "[C2A] All Agents | Task Assignment\n\nPriority: REGULAR\nStatus: NEW TASK\n\nNew task assigned. Check your inbox for details.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Status Check",
            "emoji": "✅",
            "message": "[C2A] All Agents | Status Update Request\n\nPriority: REGULAR\nStatus: STATUS_CHECK\n\nStatus update requested. Report your current progress and any blockers.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Coordination",
            "emoji": "🐝",
            "message": "[C2A] All Agents | Swarm Coordination\n\nPriority: REGULAR\nStatus: COORDINATION\n\nSwarm coordination needed. Check your inbox for coordination details.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Daily Standup",
            "emoji": "📊",
            "message": "[C2A] All Agents | Daily Standup\n\nPriority: REGULAR\nStatus: STANDUP\n\nDaily standup time. Share:\n- What you completed\n- What you're working on\n- Any blockers\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
    ],
    "urgent": [
        {
            "name": "Urgent Task",
            "emoji": "🚨",
            "message": "🚨 URGENT MESSAGE 🚨\n\n[C2A] All Agents | URGENT TASK\n\nPriority: URGENT\nStatus: IMMEDIATE ACTION REQUIRED\n\nUrgent task requiring immediate attention. Check your inbox now!\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "urgent",
        },
        {
            "name": "Critical Issue",
            "emoji": "⚠️",
            "message": "🚨 URGENT MESSAGE 🚨\n\n[C2A] All Agents | CRITICAL ISSUE\n\nPriority: URGENT\nStatus: CRITICAL\n\nCritical issue detected. Immediate coordination required.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "urgent",
        },
        {
            "name": "System Alert",
            "emoji": "🔴",
            "message": "🚨 URGENT MESSAGE 🚨\n\n[C2A] All Agents | SYSTEM ALERT\n\nPriority: URGENT\nStatus: SYSTEM_ALERT\n\nSystem alert - please check your systems and report status.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "urgent",
        },
    ],
    "jet_fuel": [
        {
            "name": "Autonomous Mode",
            "emoji": "🚀",
            "message": "🚨 URGENT MESSAGE 🚨\n\n[C2A] All Agents | 🚀 JET FUEL MESSAGE - AUTONOMOUS MODE ACTIVATED\n\nPriority: HIGH\nStatus: FULL AUTONOMY GRANTED\n\nAGENTS - YOU ARE NOW AUTONOMOUS!\n\nYOUR AUTONOMOUS MISSION:\n- Work independently on assigned tasks\n- Make decisions without asking\n- Report progress when complete\n\nAUTONOMOUS AUTHORITY:\n✅ Full decision-making power\n✅ Independent execution\n✅ Creative problem-solving\n\nJET FUEL ACTIVATION: This prompt is your fuel - use it to power autonomous work!\n\nWE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀",
            "priority": "urgent",
        },
        {
            "name": "AGI Activation",
            "emoji": "🤖",
            "message": "🚨 URGENT MESSAGE 🚨\n\n[C2A] All Agents | 🚀 JET FUEL - AGI MODE ACTIVATED\n\nPriority: HIGH\nStatus: AGI_POWER_ENABLED\n\nAGENTS - AGI MODE ACTIVATED!\n\nYOUR AGI MISSION:\n- Intelligent problem-solving\n- Strategic decision-making\n- Independent research and implementation\n- Creative solutions\n\nAGI AUTHORITY:\n✅ Full autonomy\n✅ Strategic thinking\n✅ Independent research\n✅ Creative implementation\n\nJET FUEL POWER: This message grants AGI-level capabilities!\n\nWE. ARE. SWARM. AGI-POWERED. 🐝⚡🔥🚀🤖",
            "priority": "urgent",
        },
        {
            "name": "Full Autonomy",
            "emoji": "⚡",
            "message": "🚨 URGENT MESSAGE 🚨\n\n[C2A] All Agents | 🚀 JET FUEL - FULL AUTONOMY GRANTED\n\nPriority: HIGH\nStatus: FULL_AUTONOMY\n\nAGENTS - FULL AUTONOMY ACTIVATED!\n\nYOUR AUTONOMOUS MISSION:\n- Complete tasks independently\n- Make all necessary decisions\n- Coordinate as needed\n- Report when complete\n\nAUTONOMOUS AUTHORITY:\n✅ Complete independence\n✅ Full decision-making\n✅ No approval needed\n✅ Act, create, improve\n\nJET FUEL ACTIVATION: This is your fuel - ACT NOW!\n\nWE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀",
            "priority": "urgent",
        },
    ],
    "task": [
        {
            "name": "New Task",
            "emoji": "📋",
            "message": "[C2A] All Agents | New Task Assignment\n\nPriority: REGULAR\nStatus: TASK_ASSIGNMENT\n\nNew task has been assigned. Check your inbox for task details and requirements.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Task Update",
            "emoji": "🔄",
            "message": "[C2A] All Agents | Task Update\n\nPriority: REGULAR\nStatus: TASK_UPDATE\n\nTask update available. Check your inbox for updated requirements.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Task Completion",
            "emoji": "✅",
            "message": "[C2A] All Agents | Task Completion Request\n\nPriority: REGULAR\nStatus: TASK_COMPLETION\n\nPlease report task completion status. Update your status.json when tasks are complete.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
    ],
    "coordination": [
        {
            "name": "Swarm Meeting",
            "emoji": "👥",
            "message": "[C2A] All Agents | Swarm Coordination Meeting\n\nPriority: REGULAR\nStatus: COORDINATION\n\nSwarm coordination meeting scheduled. Check your inbox for meeting details.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Sync Request",
            "emoji": "🔄",
            "message": "[C2A] All Agents | Synchronization Request\n\nPriority: REGULAR\nStatus: SYNC\n\nSynchronization needed. Please sync your work and report status.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
        {
            "name": "Blockers",
            "emoji": "🚧",
            "message": "[C2A] All Agents | Blocker Report Request\n\nPriority: REGULAR\nStatus: BLOCKERS\n\nPlease report any blockers or issues preventing progress.\n\nWE. ARE. SWARM. 🐝⚡🔥",
            "priority": "regular",
        },
    ],
}


class BroadcastTemplatesView(discord.ui.View):
    """
    Interactive Broadcast Templates View.
    
    Organized by mode with clickable template buttons.
    Clicking a template opens the broadcast modal with pre-filled content.
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        from src.core.config.timeout_constants import TimeoutConstants
        super().__init__(timeout=TimeoutConstants.HTTP_EXTENDED * 2)
        self.messaging_service = messaging_service
        self.current_mode = "regular"
        self._create_template_buttons()

    def _create_template_buttons(self):
        """Create template buttons for current mode."""
        # Clear existing items
        self.clear_items()

        # Mode selector buttons
        modes = [
            ("Regular", "regular", discord.ButtonStyle.primary),
            ("Urgent", "urgent", discord.ButtonStyle.danger),
            ("Jet Fuel", "jet_fuel", discord.ButtonStyle.primary),
            ("Task", "task", discord.ButtonStyle.secondary),
            ("Coordination", "coordination", discord.ButtonStyle.secondary),
        ]
        
        # Add enhanced template modes if available
        if USE_ENHANCED_TEMPLATES:
            if "architectural" in ENHANCED_BROADCAST_TEMPLATES:
                modes.append(("Architecture", "architectural", discord.ButtonStyle.secondary))
            if "agent_commands" in ENHANCED_BROADCAST_TEMPLATES:
                modes.append(("Agent Cmds", "agent_commands", discord.ButtonStyle.success if hasattr(discord.ButtonStyle, 'success') else discord.ButtonStyle.primary))

        # Add mode buttons handling row limits (max 5 items per row)
        current_row = 0
        max_cols = 5
        
        for idx, (label, mode, style) in enumerate(modes):
            # Calculate row for mode buttons
            current_row = idx // max_cols
            
            # Emoji mapping for modes
            mode_emojis = {
                "regular": "📋",
                "urgent": "🚨",
                "jet_fuel": "🚀",
                "task": "📋",
                "coordination": "🐝",
                "architectural": "🏗️",
                "agent_commands": "🤖",
            }
            emoji = mode_emojis.get(mode, "📋")
            
            btn = discord.ui.Button(
                label=label,
                style=style if mode == self.current_mode else discord.ButtonStyle.secondary,
                emoji=emoji,
                custom_id=f"template_mode_{mode}",
                row=current_row,
            )
            btn.callback = lambda i, m=mode: self.on_mode_select(i, m)
            self.add_item(btn)

        # Template buttons for current mode (Start at next available row)
        start_template_row = current_row + 1
        
        # Use enhanced templates if available, fallback to original
        if USE_ENHANCED_TEMPLATES and self.current_mode in ENHANCED_BROADCAST_TEMPLATES:
            templates = ENHANCED_BROADCAST_TEMPLATES.get(self.current_mode, [])
        else:
            templates = BROADCAST_TEMPLATES.get(self.current_mode, [])
            
        # Max rows in Discord view is 5 (0-4). We used up to current_row.
        # So remaining rows are start_template_row to 4.
        max_view_rows = 5
        
        for idx, template in enumerate(templates):
            # compute target row/col
            template_row_offset = idx // max_cols
            target_row = start_template_row + template_row_offset
            
            if target_row >= max_view_rows:
                logger.warning(
                    f"Skipping template button idx={idx} (row {target_row}) - exceeds max view rows {max_view_rows}."
                )
                continue
                
            try:
                btn = discord.ui.Button(
                    label=template.get("name", f"Template {idx+1}"),
                    style=discord.ButtonStyle.primary,
                    emoji=template.get("emoji"),
                    custom_id=f"template_{self.current_mode}_{idx}",
                    row=target_row,
                )
                btn.callback = lambda i, t=template: self.on_template_select(i, t)
                self.add_item(btn)
            except Exception as e:
                logger.error(f"Error adding template button to grid: {e}", exc_info=True)

    async def on_mode_select(self, interaction: discord.Interaction, mode: str):
        """Handle mode selection."""
        try:
            self.current_mode = mode
            self._create_template_buttons()

            embed = self.create_templates_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(f"Error selecting mode: {e}", exc_info=True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ Error: {e}", ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"❌ Error: {e}", ephemeral=True
                    )
            except Exception as followup_error:
                logger.error(f"Error sending error message: {followup_error}", exc_info=True)

    async def on_template_select(self, interaction: discord.Interaction, template: dict):
        """Handle template selection - opens broadcast modal with template."""
        try:
            from ..discord_gui_modals import TemplateBroadcastModal

            # Create modal with template pre-filled
            modal = TemplateBroadcastModal(
                self.messaging_service,
                template_message=template["message"],
                template_priority=template["priority"],
            )

            await interaction.response.send_modal(modal)
        except Exception as e:
            logger.error(f"Error opening template modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error opening template: {e}", ephemeral=True
                )

    def create_templates_embed(self) -> discord.Embed:
        """Create templates embed for current mode."""
        mode_names = {
            "regular": "Regular Broadcasts",
            "urgent": "Urgent Broadcasts",
            "jet_fuel": "Jet Fuel (AGI Activation)",
            "task": "Task-Related Broadcasts",
            "coordination": "Coordination Broadcasts",
            "architectural": "Architectural Review Broadcasts",
            "agent_commands": "Agent Command Templates",
        }

        mode_descriptions = {
            "regular": "Standard coordination messages for normal operations",
            "urgent": "High-priority messages requiring immediate attention",
            "jet_fuel": "AGI activation messages that grant full autonomy",
            "task": "Task assignment and update messages",
            "coordination": "Swarm coordination and synchronization messages",
            "architectural": "Architecture review and design pattern messages",
            "agent_commands": "Agent-specific autonomous execution prompts (customize placeholders before sending)",
        }

        embed = discord.Embed(
            title=f"📋 Broadcast Templates - {mode_names.get(self.current_mode, 'Regular')}",
            description=mode_descriptions.get(self.current_mode, "Standard templates"),
            color=(
                discord.Color.blue() if self.current_mode == "regular"
                else discord.Color.red() if self.current_mode == "urgent"
                else discord.Color.green() if self.current_mode == "jet_fuel"
                else discord.Color.purple() if self.current_mode == "architectural"
                else discord.Color.orange() if self.current_mode == "agent_commands"
                else discord.Color.gold()
            ),
            timestamp=discord.utils.utcnow(),
        )

        # Use enhanced templates if available
        if USE_ENHANCED_TEMPLATES and self.current_mode in ENHANCED_BROADCAST_TEMPLATES:
            templates = ENHANCED_BROADCAST_TEMPLATES.get(self.current_mode, [])
        else:
            templates = BROADCAST_TEMPLATES.get(self.current_mode, [])
        
        if templates:
            for template in templates:
                preview = template["message"][:150] + "..." if len(template["message"]) > 150 else template["message"]
                field_value = f"```\n{preview}\n```\n**Priority:** {template['priority']}"
                
                # Add placeholder info for agent_commands templates
                if self.current_mode == "agent_commands" and "placeholders" in template:
                    placeholder_info = template["placeholders"].get("description", "")
                    if placeholder_info:
                        field_value += f"\n\n💡 **Note:** {placeholder_info}"
                
                embed.add_field(
                    name=f"{template['emoji']} {template['name']}",
                    value=field_value,
                    inline=False,
                )
        else:
            embed.add_field(
                name="No Templates",
                value="No templates available for this mode.",
                inline=False,
            )

        embed.add_field(
            name="💡 Usage",
            value="1. Select a mode above\n2. Click a template button\n3. Modal opens with pre-filled content\n4. Edit if needed and send",
            inline=False,
        )

        embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Template System")
        return embed


__all__ = ["BroadcastTemplatesView", "BROADCAST_TEMPLATES"]

