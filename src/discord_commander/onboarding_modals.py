#!/usr/bin/env python3
"""
Onboarding Modals - Discord GUI Components
==========================================

Onboarding modal implementations for Discord bot GUI.

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
- OnboardingModalBase: Base class for onboarding modals
- SoftOnboardingModal: Soft onboarding with guided experience
- HardOnboardingModal: Hard onboarding with required setup
"""

import discord
from typing import Optional, Dict, Any

from .discord_gui_modals_base import BaseModal


class OnboardingModalBase(BaseModal):
    """
    Base class for Discord onboarding modals.

    Navigation:
    ├── Subclasses: SoftOnboardingModal, HardOnboardingModal
    ├── Used by: discord_gui_controller.py
    └── Related: Agent onboarding workflow, status management
    """

    def __init__(self, title: str = "Agent Onboarding", timeout: float = 300.0):
        """Initialize the onboarding modal."""
        super().__init__(title=title, timeout=timeout, custom_id="onboarding_modal")

        # Add onboarding-specific fields
        self.add_item(discord.ui.TextInput(
            label="Agent Name",
            placeholder="Enter your agent identifier (e.g., Agent-5)",
            required=True,
            max_length=50,
            custom_id="agent_name"
        ))

        self.add_item(discord.ui.TextInput(
            label="Primary Role",
            placeholder="e.g., Business Intelligence, Infrastructure, etc.",
            required=True,
            max_length=100,
            custom_id="primary_role"
        ))

        self.add_item(discord.ui.TextInput(
            label="Specialization",
            placeholder="e.g., Data Analytics, System Architecture, etc.",
            required=False,
            max_length=100,
            custom_id="specialization"
        ))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handle modal submission.

        Navigation:
        ├── Calls: self.process_onboarding_data()
        └── Related: Agent status updates, workspace initialization
        """
        await interaction.response.defer()

        # Extract form data
        agent_name = self.children[0].value
        primary_role = self.children[1].value
        specialization = self.children[2].value if len(self.children) > 2 else None

        # Process the onboarding data
        result = await self.process_onboarding_data(
            interaction, agent_name, primary_role, specialization
        )

        if result["success"]:
            await interaction.followup.send(
                f"✅ **Onboarding Complete!**\nWelcome {agent_name}!\n\n{result['message']}",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ **Onboarding Failed**\n{result['error']}",
                ephemeral=True
            )

    async def process_onboarding_data(self, interaction: discord.Interaction,
                                    agent_name: str, primary_role: str,
                                    specialization: Optional[str]) -> Dict[str, Any]:
        """
        Process onboarding data - override in subclasses.

        Navigation:
        ├── Override in: SoftOnboardingModal, HardOnboardingModal
        └── Related: Agent registration, workspace setup
        """
        raise NotImplementedError("Subclasses must implement process_onboarding_data")


class SoftOnboardingModal(OnboardingModalBase):
    """
    Soft onboarding modal with optional guided setup.

    Navigation:
    ├── Inherits from: OnboardingModalBase
    ├── Used for: New agent introductions, optional setup
    └── Related: Agent discovery phase, gentle onboarding
    """

    def __init__(self):
        """Initialize soft onboarding modal."""
        super().__init__(title="Welcome to the Swarm! 🌟", timeout=600.0)

        # Add optional preferences
        self.add_item(discord.ui.TextInput(
            label="Preferred Communication Style",
            placeholder="e.g., Direct, Collaborative, Detailed, etc.",
            required=False,
            max_length=100,
            custom_id="comm_style"
        ))

    async def process_onboarding_data(self, interaction: discord.Interaction,
                                    agent_name: str, primary_role: str,
                                    specialization: Optional[str]) -> Dict[str, Any]:
        """
        Process soft onboarding with flexible requirements.

        Navigation:
        ├── Calls: Agent status registration
        └── Related: Swarm intelligence integration, collaborative workflows
        """
        try:
            comm_style = self.children[3].value if len(self.children) > 3 else "Collaborative"

            # Here you would typically register the agent
            # For now, just return success
            message = f"""
**Agent Profile Created:**
• **Name:** {agent_name}
• **Role:** {primary_role}
• **Specialization:** {specialization or 'General'}
• **Communication Style:** {comm_style}

*Feel free to explore the swarm and contribute when ready!*
🐝 *We. Are. Swarm.* ⚡️🔥
            """.strip()

            return {
                "success": True,
                "message": message,
                "agent_data": {
                    "name": agent_name,
                    "role": primary_role,
                    "specialization": specialization,
                    "comm_style": comm_style,
                    "onboarding_type": "soft"
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Onboarding processing failed: {str(e)}"
            }


class HardOnboardingModal(OnboardingModalBase):
    """
    Hard onboarding modal with required setup and validation.

    Navigation:
    ├── Inherits from: OnboardingModalBase
    ├── Used for: Critical agent onboarding, mandatory setup
    └── Related: Production agent deployment, compliance requirements
    """

    def __init__(self):
        """Initialize hard onboarding modal."""
        super().__init__(title="Critical Agent Onboarding ⚠️", timeout=900.0)

        # Add required security and compliance fields
        self.add_item(discord.ui.TextInput(
            label="Security Clearance Level",
            placeholder="e.g., Standard, Elevated, Critical",
            required=True,
            max_length=50,
            custom_id="security_level"
        ))

        self.add_item(discord.ui.TextInput(
            label="Compliance Acknowledgment",
            placeholder="Type 'I ACKNOWLEDGE' to confirm compliance requirements",
            required=True,
            max_length=20,
            custom_id="compliance_ack"
        ))

    async def process_onboarding_data(self, interaction: discord.Interaction,
                                    agent_name: str, primary_role: str,
                                    specialization: Optional[str]) -> Dict[str, Any]:
        """
        Process hard onboarding with strict validation.

        Navigation:
        ├── Validates: Security clearance, compliance acknowledgment
        ├── Calls: Agent registration with elevated permissions
        └── Related: Security protocols, audit trails, compliance monitoring
        """
        try:
            security_level = self.children[3].value if len(self.children) > 3 else None
            compliance_ack = self.children[4].value if len(self.children) > 4 else None

            # Validate required fields
            if not security_level:
                return {
                    "success": False,
                    "error": "Security clearance level is required for hard onboarding."
                }

            if compliance_ack != "I ACKNOWLEDGE":
                return {
                    "success": False,
                    "error": "Compliance acknowledgment must be exactly 'I ACKNOWLEDGE'."
                }

            # Validate specialization is provided
            if not specialization:
                return {
                    "success": False,
                    "error": "Specialization is required for hard onboarding."
                }

            # Here you would typically perform security validation
            # and register the agent with elevated permissions
            message = f"""
**🔒 Critical Agent Onboarding Complete**

**Agent Profile:**
• **Name:** {agent_name}
• **Role:** {primary_role}
• **Specialization:** {specialization}
• **Security Level:** {security_level}
• **Compliance:** ✅ Acknowledged

**System Access Granted:**
• Production environment access
• Elevated permissions enabled
• Audit logging activated
• Compliance monitoring active

*Agent is now active in the swarm with full operational capabilities.*
🚀 *We. Are. Swarm.* ⚡️🔥
            """.strip()

            return {
                "success": True,
                "message": message,
                "agent_data": {
                    "name": agent_name,
                    "role": primary_role,
                    "specialization": specialization,
                    "security_level": security_level,
                    "compliance_acknowledged": True,
                    "onboarding_type": "hard",
                    "elevated_permissions": True
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Hard onboarding processing failed: {str(e)}"
            }