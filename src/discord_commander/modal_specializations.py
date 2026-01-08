"""
Modal Specializations - Agent Cellphone V2
==========================================

SSOT Domain: discord

Centralized imports for all Discord modal specializations.
All specialized modal implementations have been extracted to dedicated modules for V2 compliance.

Features:
- Onboarding modals (onboarding_modals.py)
- Broadcast modals (broadcast_modals.py)
- Template modals (template_modals.py)
- Mermaid diagram modals (mermaid_modals.py)

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Import all specialized modal classes
from .onboarding_modals import (
    OnboardingModalBase,
    SoftOnboardingModal,
    HardOnboardingModal
)

from .broadcast_modals import (
    BroadcastModalBase,
    AgentMessageModal,
    SelectiveBroadcastModal,
    BroadcastMessageModal
)

from .template_modals import (
    TemplateModalBase,
    TemplateBroadcastModal,
    JetFuelMessageModal,
    JetFuelBroadcastModal
)

# Legacy aliases for backward compatibility
class MermaidModal:
    """Placeholder for mermaid modal - to be implemented."""
    pass

__all__ = [
    # Onboarding modals
    "OnboardingModalBase",
    "SoftOnboardingModal",
    "HardOnboardingModal",

    # Broadcast modals
    "BroadcastModalBase",
    "AgentMessageModal",
    "SelectiveBroadcastModal",
    "BroadcastMessageModal",

    # Template modals
    "TemplateModalBase",
    "TemplateBroadcastModal",
    "JetFuelMessageModal",
    "JetFuelBroadcastModal",

    # Legacy compatibility
    "MermaidModal"
]

# All modal implementations have been extracted to specialized modules for V2 compliance