#!/usr/bin/env python3
"""
Template Modals - Discord GUI Components
=======================================

Template-based modal implementations for Discord bot GUI.

<!-- SSOT Domain: discord -->

Navigation References:
├── Related Files:
│   ├── Base Modals → discord_gui_modals_base.py
│   ├── Modal Specializations → modal_specializations.py
│   ├── Template Collection → discord_template_collection.py
│   └── GUI Controller → discord_gui_controller.py
├── Documentation:
│   └── Discord GUI → README_DISCORD_GUI.md
└── Testing:
    └── Modal Tests → tests/discord/test_discord_gui_modals.py

Classes:
- TemplateModalBase: Base class for template-based modals
- TemplateBroadcastModal: Modal for template-based broadcasts
- JetFuelMessageModal: High-energy message modal
- JetFuelBroadcastModal: High-energy broadcast modal
"""

import discord
from typing import Optional, Dict, Any, List

from .discord_gui_modals_base import BaseModal


class TemplateModalBase(BaseModal):
    """
    Base class for template-based Discord modals.

    Navigation:
    ├── Subclasses: TemplateBroadcastModal, JetFuelMessageModal, JetFuelBroadcastModal
    ├── Uses: discord_template_collection.py
    └── Related: Message templating, standardized communication
    """

    def __init__(self, title: str = "Template Message", timeout: float = 300.0):
        """Initialize the template modal."""
        super().__init__(title=title, timeout=timeout, custom_id="template_modal")

        # Add template selection
        self.add_item(discord.ui.TextInput(
            label="Template Type",
            placeholder="e.g., coordination, status, alert, celebration",
            required=True,
            max_length=50,
            custom_id="template_type"
        ))

        self.add_item(discord.ui.TextInput(
            label="Custom Message",
            placeholder="Add your custom content to the template",
            required=False,
            max_length=1000,
            style=discord.TextStyle.paragraph,
            custom_id="custom_content"
        ))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handle modal submission with template processing.

        Navigation:
        ├── Calls: self.process_template_data()
        └── Related: Template rendering, message formatting
        """
        await interaction.response.defer()

        # Extract form data
        template_type = self.children[0].value
        custom_content = self.children[1].value if len(self.children) > 1 else ""

        # Process the template data
        result = await self.process_template_data(
            interaction, template_type, custom_content
        )

        if result["success"]:
            await interaction.followup.send(
                f"✅ **Template Message Sent!**\n{result['message']}",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ **Template Processing Failed**\n{result['error']}",
                ephemeral=True
            )

    async def process_template_data(self, interaction: discord.Interaction,
                                  template_type: str, custom_content: str) -> Dict[str, Any]:
        """
        Process template data - override in subclasses.

        Navigation:
        ├── Override in: TemplateBroadcastModal, JetFuelMessageModal, JetFuelBroadcastModal
        └── Related: Template rendering, content personalization
        """
        raise NotImplementedError("Subclasses must implement process_template_data")

    def _render_template(self, template_type: str, custom_content: str) -> str:
        """
        Render template with custom content.

        Navigation:
        ├── Used by: Subclass implementations
        └── Related: Template engine, content formatting
        """
        templates = {
            "coordination": f"🤝 **Coordination Update**\n\n{custom_content}\n\n*Working together for swarm success!*",
            "status": f"📊 **Status Update**\n\n{custom_content}\n\n*Progress continues...*",
            "alert": f"🚨 **Alert**\n\n{custom_content}\n\n*Attention required!*",
            "celebration": f"🎉 **Celebration**\n\n{custom_content}\n\n*Great work, swarm!*",
            "default": f"📝 **Message**\n\n{custom_content}"
        }

        return templates.get(template_type.lower(), templates["default"])


class TemplateBroadcastModal(TemplateModalBase):
    """
    Modal for template-based broadcast messages.

    Navigation:
    ├── Inherits from: TemplateModalBase
    ├── Used for: Standardized broadcast communication
    └── Related: Swarm coordination, status broadcasting
    """

    def __init__(self):
        """Initialize template broadcast modal."""
        super().__init__(title="Template Broadcast 📢", timeout=300.0)

        # Add broadcast options
        self.add_item(discord.ui.TextInput(
            label="Target Audience",
            placeholder="all, infrastructure, business_intelligence, etc.",
            required=False,
            max_length=100,
            custom_id="target_audience"
        ))

    async def process_template_data(self, interaction: discord.Interaction,
                                  template_type: str, custom_content: str) -> Dict[str, Any]:
        """
        Process template broadcast.

        Navigation:
        ├── Uses: Template rendering, broadcast infrastructure
        └── Related: Group messaging, standardized announcements
        """
        try:
            target_audience = self.children[2].value if len(self.children) > 2 else "all"

            rendered_content = self._render_template(template_type, custom_content)

            formatted_message = f"""
**📢 Template Broadcast**

**Template:** {template_type}
**Target:** {target_audience}
**From:** {interaction.user.display_name}

{rendered_content}

🐝 *We. Are. Swarm.* ⚡️🔥
            """.strip()

            return {
                "success": True,
                "message": formatted_message,
                "template_type": template_type,
                "target_audience": target_audience,
                "rendered_content": rendered_content,
                "message_type": "template_broadcast"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Template broadcast processing failed: {str(e)}"
            }


class JetFuelMessageModal(TemplateModalBase):
    """
    High-energy message modal for motivational content.

    Navigation:
    ├── Inherits from: TemplateModalBase
    ├── Used for: Motivational messaging, high-energy communication
    └── Related: Swarm morale, celebration messaging
    """

    def __init__(self):
        """Initialize jet fuel message modal."""
        super().__init__(title="Jet Fuel Message 🚀", timeout=300.0)

        # Add energy level selection
        self.add_item(discord.ui.TextInput(
            label="Energy Level",
            placeholder="maximum, high, medium, low",
            required=False,
            max_length=20,
            custom_id="energy_level"
        ))

    async def process_template_data(self, interaction: discord.Interaction,
                                  template_type: str, custom_content: str) -> Dict[str, Any]:
        """
        Process high-energy jet fuel message.

        Navigation:
        ├── Uses: Motivational templates, energy amplification
        └── Related: Swarm motivation, celebration culture
        """
        try:
            energy_level = self.children[2].value if len(self.children) > 2 else "high"

            # Add energy indicators based on level
            energy_indicators = {
                "maximum": "🚀🔥💥⚡️🌟",
                "high": "🚀🔥⚡️",
                "medium": "🚀⚡️",
                "low": "🚀"
            }

            energy_emoji = energy_indicators.get(energy_level.lower(), energy_indicators["high"])

            rendered_content = self._render_template(template_type, custom_content)

            formatted_message = f"""
**{energy_emoji} JET FUEL MESSAGE {energy_emoji}**

**Energy Level:** {energy_level.upper()}
**From:** {interaction.user.display_name}

{rendered_content}

**{energy_emoji} FEEL THE ENERGY! {energy_emoji}**
🐝 *We. Are. Swarm.* ⚡️🔥🚀
            """.strip()

            return {
                "success": True,
                "message": formatted_message,
                "template_type": template_type,
                "energy_level": energy_level,
                "energy_emoji": energy_emoji,
                "rendered_content": rendered_content,
                "message_type": "jet_fuel_message"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Jet fuel message processing failed: {str(e)}"
            }


class JetFuelBroadcastModal(TemplateModalBase):
    """
    High-energy broadcast modal for swarm-wide motivation.

    Navigation:
    ├── Inherits from: TemplateModalBase
    ├── Used for: Swarm-wide motivational broadcasts
    └── Related: Team motivation, celebration events
    """

    def __init__(self):
        """Initialize jet fuel broadcast modal."""
        super().__init__(title="Jet Fuel Broadcast 🌟", timeout=300.0)

        # Add broadcast energy settings
        self.add_item(discord.ui.TextInput(
            label="Energy Intensity",
            placeholder="maximum, high, medium, low",
            required=False,
            max_length=20,
            custom_id="energy_intensity"
        ))

        self.add_item(discord.ui.TextInput(
            label="Celebration Type",
            placeholder="victory, milestone, motivation, general",
            required=False,
            max_length=50,
            custom_id="celebration_type"
        ))

    async def process_template_data(self, interaction: discord.Interaction,
                                  template_type: str, custom_content: str) -> Dict[str, Any]:
        """
        Process high-energy jet fuel broadcast.

        Navigation:
        ├── Uses: Swarm-wide messaging, motivational amplification
        └── Related: Team celebrations, morale boosting
        """
        try:
            energy_intensity = self.children[2].value if len(self.children) > 2 else "high"
            celebration_type = self.children[3].value if len(self.children) > 3 else "general"

            # Add energy indicators
            energy_indicators = {
                "maximum": "🚀🔥💥⚡️🌟🎉🎊✨",
                "high": "🚀🔥⚡️🎉✨",
                "medium": "🚀⚡️🎉",
                "low": "🚀🎉"
            }

            energy_emoji = energy_indicators.get(energy_intensity.lower(), energy_indicators["high"])

            rendered_content = self._render_template(template_type, custom_content)

            formatted_message = f"""
**{energy_emoji} JET FUEL SWARM BROADCAST {energy_emoji}**

**Energy Intensity:** {energy_intensity.upper()}
**Celebration Type:** {celebration_type.upper()}
**From:** {interaction.user.display_name}

{rendered_content}

**{energy_emoji} UNITED WE THRIVE! {energy_emoji}**
🐝 *We. Are. Swarm.* ⚡️🔥🚀🌟
**{energy_emoji} TOGETHER WE CONQUER! {energy_emoji}**
            """.strip()

            return {
                "success": True,
                "message": formatted_message,
                "template_type": template_type,
                "energy_intensity": energy_intensity,
                "celebration_type": celebration_type,
                "energy_emoji": energy_emoji,
                "rendered_content": rendered_content,
                "message_type": "jet_fuel_broadcast"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Jet fuel broadcast processing failed: {str(e)}"
            }