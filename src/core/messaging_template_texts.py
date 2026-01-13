#!/usr/bin/env python3
"""
Messaging Templates & Text - V2 Compliance Module
=================================================

<!-- SSOT Domain: integration -->

Canonical policy text, template strings, and formatting helpers.

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2025-10-11
License: MIT

Refactor note (Phase 2): This module now follows the Configuration/Data pattern.
Large static strings live under `src/core/messaging_templates_data/`.
"""

from __future__ import annotations

from typing import Any

from .messaging_models import MessageCategory
from .messaging_templates_data.coordination_texts import SWARM_COORDINATION_TEXT
from .messaging_templates_data.cycle_texts import AGENT_OPERATING_CYCLE_TEXT, CYCLE_CHECKLIST_TEXT
from .messaging_templates_data.discord_policy_texts import (
    D2A_REPORT_FORMAT_TEXT,
    D2A_RESPONSE_POLICY_TEXT,
    DISCORD_REPORTING_TEXT,
)
from .messaging_templates_data.registry import build_message_templates


# Template strings for standard headers. Payloads should be formatted by the caller.
MESSAGE_TEMPLATES: dict[MessageCategory, Any] = build_message_templates()


def format_d2a_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Format D2A payload with default values."""

    payload.setdefault("interpretation", "Pending agent interpretation.")
    payload.setdefault("actions", "Evaluate request and execute if safe/within scope.")
    payload.setdefault(
        "fallback",
        "Ask for clarification in Discord with one focused question.",
    )
    payload.setdefault("discord_response_policy", D2A_RESPONSE_POLICY_TEXT)
    payload.setdefault("d2a_report_format", D2A_REPORT_FORMAT_TEXT)
<<<<<<< HEAD
    payload.setdefault("devlog_command",
        "python tools/devlog_poster.py --agent {recipient} --file <devlog_path>\n"
        "Examples:\n"
        "  python tools/devlog_poster.py --agent Agent-1 --file agent_workspaces/Agent-1/devlogs/status.md\n"
        "  python tools/devlog_poster.py --agent Agent-7 --file devlogs/2025-12-26_status.md\n"
        "  python tools/devlog_poster.py --agent Agent-8 --file agent_workspaces/Agent-8/devlogs/DEVLOG_2025-12-26.md"
    )
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    return payload


def format_s2a_message(template_key: str, **kwargs: Any) -> str:
    """Helper to render an S2A template with operating cycle included."""

    templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
    template = templates.get(template_key) or templates.get("CONTROL")

    kwargs.setdefault("operating_cycle", AGENT_OPERATING_CYCLE_TEXT)
    kwargs.setdefault("cycle_checklist", CYCLE_CHECKLIST_TEXT)
    kwargs.setdefault("discord_reporting", DISCORD_REPORTING_TEXT)
    kwargs.setdefault("swarm_coordination", SWARM_COORDINATION_TEXT)

    return template.format(**kwargs)


__all__ = [
    "MESSAGE_TEMPLATES",
    "AGENT_OPERATING_CYCLE_TEXT",
    "CYCLE_CHECKLIST_TEXT",
    "SWARM_COORDINATION_TEXT",
    "DISCORD_REPORTING_TEXT",
    "D2A_RESPONSE_POLICY_TEXT",
    "D2A_REPORT_FORMAT_TEXT",
    "format_d2a_payload",
    "format_s2a_message",
]
