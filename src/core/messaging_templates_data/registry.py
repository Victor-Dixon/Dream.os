"""
Template registry assembly (Configuration/Data pattern).

This module composes the full MESSAGE_TEMPLATES mapping from smaller, static
pieces so each module stays under V2 size limits.

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

from typing import Any

from ..messaging_models import MessageCategory
from .s2a_templates_core import S2A_TEMPLATES_CORE
from .s2a_templates_misc import S2A_TEMPLATES_MISC
from .template_a2a import A2A_TEMPLATE
from .template_c2a import C2A_TEMPLATE
from .template_d2a import D2A_TEMPLATE


def build_message_templates() -> dict[MessageCategory, Any]:
    """
    Build the canonical MESSAGE_TEMPLATES mapping.

    - S2A is a dict of sub-templates (CONTROL, SWARM_PULSE, ...)
    - D2A/C2A/A2A are single template strings
    """

    s2a = {}
    s2a.update(S2A_TEMPLATES_CORE)
    s2a.update(S2A_TEMPLATES_MISC)

    return {
        MessageCategory.S2A: s2a,
        MessageCategory.D2A: D2A_TEMPLATE,
        MessageCategory.C2A: C2A_TEMPLATE,
        MessageCategory.A2A: A2A_TEMPLATE,
    }


