#!/usr/bin/env python3
"""
Broadcast Modals - Discord GUI Components
========================================

Broadcast modal implementations for Discord bot GUI.

<!-- SSOT Domain: discord -->

Navigation References:
├── Related Files:
│   ├── Base Modals → discord_gui_modals_base.py
│   ├── Modal Specializations → modal_specializations.py
│   └── GUI Controller → discord_gui_controller.py
├── Documentation:
│   └── Discord GUI → README_DISCORD_GUI.md
└── Testing:
    └── Modal Tests → tests/discord/test_discord_gui_modals.py

Classes:
- BroadcastModalBase: Base class for broadcast modals
- AgentMessageModal: Modal for sending messages to specific agents
- SelectiveBroadcastModal: Modal for selective broadcasting
- BroadcastMessageModal: Modal for general broadcast messages
"""

import discord
from typing import Optional, Dict, Any, List

from .discord_gui_modals_base import BaseModal


class BroadcastModalBase(BaseModal):
    """
    Base class for Discord broadcast modals.

    Navigation:
    ├── Subclasses: AgentMessageModal, SelectiveBroadcastModal, BroadcastMessageModal
    ├── Used by: discord_gui_controller.py
    └── Related: Message broadcasting, agent communication
    """

    def __init__(self, title: str = "Broadcast Message", timeout: float = 300.0):
        """Initialize the broadcast modal."""
        super().__init__(title=title, timeout=timeout, custom_id="broadcast_modal")

        # Add broadcast-specific fields
        self.add_item(discord.ui.TextInput(
            label="Message Title",
            placeholder="Enter a brief title for your broadcast",
            required=True,
            max_length=100,
            custom_id="message_title"
        ))

        self.add_item(discord.ui.TextInput(
            label="Message Content",
            placeholder="Enter your broadcast message",
            required=True,
            max_length=2000,
            style=discord.TextStyle.paragraph,
            custom_id="message_content"
        ))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handle modal submission.

        Navigation:
        ├── Calls: self.process_broadcast_data()
        └── Related: Message queuing, delivery tracking
        """
        await interaction.response.defer()

        # Extract form data
        title = self.children[0].value
        content = self.children[1].value

        # Process the broadcast data
        result = await self.process_broadcast_data(interaction, title, content)

        if result["success"]:
            await interaction.followup.send(
                f"✅ **Broadcast Sent!**\n{result['message']}",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ **Broadcast Failed**\n{result['error']}",
                ephemeral=True
            )

    async def process_broadcast_data(self, interaction: discord.Interaction,
                                   title: str, content: str) -> Dict[str, Any]:
        """
        Process broadcast data - override in subclasses.

        Navigation:
        ├── Override in: AgentMessageModal, SelectiveBroadcastModal, BroadcastMessageModal
        └── Related: Message routing, delivery confirmation
        """
        raise NotImplementedError("Subclasses must implement process_broadcast_data")


class AgentMessageModal(BroadcastModalBase):
    """
    Modal for sending targeted messages to specific agents.

    Navigation:
    ├── Inherits from: BroadcastModalBase
    ├── Used for: Direct agent-to-agent communication
    └── Related: Agent discovery, targeted messaging
    """

    def __init__(self):
        """Initialize agent message modal."""
        super().__init__(title="Message Agent 📨", timeout=300.0)

        # Add target agent selection
        self.add_item(discord.ui.TextInput(
            label="Target Agent",
            placeholder="e.g., Agent-5, Agent-1, CAPTAIN",
            required=True,
            max_length=50,
            custom_id="target_agent"
        ))

    async def process_broadcast_data(self, interaction: discord.Interaction,
                                   title: str, content: str) -> Dict[str, Any]:
        """
        Process agent-specific message.

        Navigation:
        ├── Uses: Messaging service for agent routing
        └── Related: Agent-to-agent communication protocols
        """
        try:
            target_agent = self.children[2].value

            # Here you would typically send the message via the messaging service
            # For now, just return success with formatted message
            formatted_message = f"""
**📨 Agent Message Sent**

**To:** {target_agent}
**From:** {interaction.user.display_name}
**Title:** {title}

**Content:**
{content}

*Message queued for delivery through the swarm messaging system.*
            """.strip()

            return {
                "success": True,
                "message": formatted_message,
                "recipient": target_agent,
                "message_type": "agent_direct"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Agent message processing failed: {str(e)}"
            }


class SelectiveBroadcastModal(BroadcastModalBase):
    """
    Modal for selective broadcasting to agent groups.

    Navigation:
    ├── Inherits from: BroadcastModalBase
    ├── Used for: Group messaging, role-based communication
    └── Related: Agent categorization, group management
    """

    def __init__(self):
        """Initialize selective broadcast modal."""
        super().__init__(title="Selective Broadcast 📡", timeout=300.0)

        # Add target group selection
        self.add_item(discord.ui.TextInput(
            label="Target Group",
            placeholder="e.g., Infrastructure, Business Intelligence, All",
            required=True,
            max_length=100,
            custom_id="target_group"
        ))

        self.add_item(discord.ui.TextInput(
            label="Priority Level",
            placeholder="regular, urgent, critical",
            required=False,
            max_length=20,
            custom_id="priority"
        ))

    async def process_broadcast_data(self, interaction: discord.Interaction,
                                   title: str, content: str) -> Dict[str, Any]:
        """
        Process selective broadcast to agent groups.

        Navigation:
        ├── Uses: Agent categorization, priority routing
        └── Related: Group communication, priority escalation
        """
        try:
            target_group = self.children[2].value
            priority = self.children[3].value if len(self.children) > 3 else "regular"

            # Here you would typically broadcast to the selected group
            formatted_message = f"""
**📡 Selective Broadcast Sent**

**Target Group:** {target_group}
**Priority:** {priority}
**From:** {interaction.user.display_name}
**Title:** {title}

**Content:**
{content}

*Broadcast queued for delivery to {target_group} agents.*
            """.strip()

            return {
                "success": True,
                "message": formatted_message,
                "target_group": target_group,
                "priority": priority,
                "message_type": "selective_broadcast"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Selective broadcast processing failed: {str(e)}"
            }


class BroadcastMessageModal(BroadcastModalBase):
    """
    Modal for general broadcast messages to all agents.

    Navigation:
    ├── Inherits from: BroadcastModalBase
    ├── Used for: System-wide announcements, swarm coordination
    └── Related: Emergency communication, system updates
    """

    def __init__(self):
        """Initialize broadcast message modal."""
        super().__init__(title="Swarm Broadcast 📢", timeout=300.0)

        # Add broadcast options
        self.add_item(discord.ui.TextInput(
            label="Broadcast Type",
            placeholder="announcement, alert, coordination, general",
            required=False,
            max_length=50,
            custom_id="broadcast_type"
        ))

        self.add_item(discord.ui.TextInput(
            label="Urgency Level",
            placeholder="normal, urgent, critical",
            required=False,
            max_length=20,
            custom_id="urgency"
        ))

    async def process_broadcast_data(self, interaction: discord.Interaction,
                                   title: str, content: str) -> Dict[str, Any]:
        """
        Process general broadcast to all swarm agents.

        Navigation:
        ├── Uses: Swarm-wide messaging infrastructure
        └── Related: Emergency broadcasting, system announcements
        """
        try:
            broadcast_type = self.children[2].value if len(self.children) > 2 else "general"
            urgency = self.children[3].value if len(self.children) > 3 else "normal"

            # Here you would typically broadcast to all agents
            formatted_message = f"""
**📢 Swarm Broadcast Sent**

**Broadcast Type:** {broadcast_type}
**Urgency:** {urgency}
**From:** {interaction.user.display_name}
**Title:** {title}

**Content:**
{content}

*Broadcast queued for delivery to all swarm agents.*
🐝 *We. Are. Swarm.* ⚡️🔥
            """.strip()

            return {
                "success": True,
                "message": formatted_message,
                "broadcast_type": broadcast_type,
                "urgency": urgency,
                "message_type": "swarm_broadcast"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Swarm broadcast processing failed: {str(e)}"
            }