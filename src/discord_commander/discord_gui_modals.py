#!/usr/bin/env python3
"""
Discord GUI Modals - Agent Cellphone V2
======================================

SSOT Domain: discord

Refactored entry point for Discord modal functionality.
All core logic has been extracted into specialized base classes and focused implementations.

Features:
- Agent messaging modals (discord_gui_modals_v2.py)
- Specialized modal base classes (modal_specializations.py)
- Common modal utilities (discord_gui_modals_base.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export all modal classes for backward compatibility
from .discord_gui_modals_v2 import (
    AgentMessageModal,
    BroadcastMessageModal,
    JetFuelMessageModal,
    SelectiveBroadcastModal,
    JetFuelBroadcastModal,
    TemplateBroadcastModal,
    SoftOnboardModal,
    MermaidModal,
    HardOnboardModal,
)

# Re-export base classes
from .discord_gui_modals_base import BaseMessageModal
from .modal_specializations import OnboardingModalBase, BroadcastModalBase, TemplateModalBase

__all__ = [
    # Modal classes
    "AgentMessageModal",
    "BroadcastMessageModal",
    "JetFuelMessageModal",
    "SelectiveBroadcastModal",
    "JetFuelBroadcastModal",
    "TemplateBroadcastModal",
    "SoftOnboardModal",
    "MermaidModal",
    "HardOnboardModal",
    # Base classes
    "BaseMessageModal",
    "OnboardingModalBase",
    "BroadcastModalBase",
    "TemplateModalBase",
]