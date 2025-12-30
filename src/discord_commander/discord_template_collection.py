#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord Template Collection - Enhanced Templates
================================================

Facade module for Discord template collection.
Imports from modular template files for V3 compliance.

V3 Compliance: Facade pattern, delegates to modular templates
Author: Agent-2 (Architecture & Design Specialist)
Created: 2025-01-27
Status: ✅ ENHANCED TEMPLATE COLLECTION
"""

from typing import Any

# Import broadcast templates from separate module
try:
    from .templates.broadcast_templates import ENHANCED_BROADCAST_TEMPLATES
except ImportError:
    # Fallback if templates module not available
    ENHANCED_BROADCAST_TEMPLATES = {}


# ============================================================================
# TEMPLATE UTILITIES
# ============================================================================

def get_template_by_name(template_name: str, mode: str = "regular") -> dict[str, Any] | None:
    """Get template by name from specified mode."""
    templates = ENHANCED_BROADCAST_TEMPLATES.get(mode, [])
    for template in templates:
        if template["name"].lower() == template_name.lower():
            return template
    return None


def get_all_templates() -> dict[str, list[dict[str, Any]]]:
    """Get all enhanced broadcast templates."""
    return ENHANCED_BROADCAST_TEMPLATES


def get_templates_by_mode(mode: str) -> list[dict[str, Any]]:
    """Get all templates for specified mode."""
    return ENHANCED_BROADCAST_TEMPLATES.get(mode, [])


# Note: Embed template functions are in discord_embeds.py
# Import them from there:
# from src.discord_commander.discord_embeds import (
#     create_achievement_embed,
#     create_milestone_embed,
#     create_architectural_review_embed,
#     create_error_embed,
#     create_validation_embed,
#     create_cleanup_embed,
# )


__all__ = [
    "ENHANCED_BROADCAST_TEMPLATES",
    "get_template_by_name",
    "get_all_templates",
    "get_templates_by_mode",
]
