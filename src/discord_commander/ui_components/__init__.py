#!/usr/bin/env python3
"""
Discord UI Components Module - V2 Compliance
===========================================

Extracted UI components for V2 compliance and modularity.

<!-- SSOT Domain: discord -->

This module contains:
- Control panel buttons and UI components
- Embed factories for consistent styling
- Reusable UI patterns and templates

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: V2 Compliance Refactoring
"""

from .control_panel_buttons import (
    ControlPanelButtonFactory,
    ButtonCallbackManager,
    create_monitor_buttons,
    create_main_control_buttons,
)

from .control_panel_embeds import (
    ControlPanelEmbedFactory,
    EmbedTemplateManager,
    create_monitor_embed,
    create_error_embed,
    create_success_embed,
)

__all__ = [
    # Button components
    'ControlPanelButtonFactory',
    'ButtonCallbackManager',
    'create_monitor_buttons',
    'create_main_control_buttons',

    # Embed components
    'ControlPanelEmbedFactory',
    'EmbedTemplateManager',
    'create_monitor_embed',
    'create_error_embed',
    'create_success_embed',
]