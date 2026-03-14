#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-messaging-template-texts
# @registry docs/recovery/recovery_registry.yaml#src-core-messaging-template-texts

"""
Messaging Template Texts - Core Layer
====================================

SSOT-backed template storage and formatting helpers.

<!-- SSOT Domain: integration -->

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .messaging_models import MessageCategory
from .messaging_templates_data.coordination_texts import SWARM_COORDINATION_TEXT
from .messaging_templates_data.cycle_texts import (
    AGENT_OPERATING_CYCLE_TEXT,
    CYCLE_CHECKLIST_TEXT,
)
from .messaging_templates_data.policy_texts import (
    D2A_REPORT_FORMAT,
    DISCORD_REPORTING_POLICY,
    DISCORD_RESPONSE_POLICY,
    PREFERRED_REPLY_FORMAT,
)
from .messaging_templates_data.registry import build_message_templates

MESSAGE_TEMPLATES = build_message_templates()


def format_d2a_payload(payload: dict[str, Any]) -> dict[str, str]:
    """Format Discord-to-Agent payload with SSOT defaults."""
    return {
        "interpretation": payload.get(
            "interpretation",
            "Interpret the request and summarize intent.",
        ),
        "actions": payload.get(
            "actions",
            "Propose concrete actions with evidence.",
        ),
        "discord_response_policy": payload.get(
            "discord_response_policy",
            DISCORD_RESPONSE_POLICY,
        ),
        "discord_reporting_policy": payload.get(
            "discord_reporting_policy",
            DISCORD_REPORTING_POLICY,
        ),
        "d2a_report_format": payload.get(
            "d2a_report_format",
            D2A_REPORT_FORMAT,
        ),
        "preferred_reply_format": payload.get(
            "preferred_reply_format",
            PREFERRED_REPLY_FORMAT,
        ),
        "fallback": payload.get(
            "fallback",
            "If clarification needed: ask one precise question.",
        ),
    }


def format_s2a_message(message: str, **kwargs: Any) -> str:
    """Render a System-to-Agent message via the canonical registry."""
    templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
    template_key = kwargs.get("template_key", "CONTROL")
    template = templates.get(template_key, templates.get("CONTROL", "{context}"))
    now = datetime.now().isoformat(timespec="seconds")

    payload = {
        "sender": kwargs.get("sender", "SYSTEM"),
        "recipient": kwargs.get("recipient", "Agent-1"),
        "priority": kwargs.get("priority", "regular"),
        "message_id": kwargs.get("message_id", "unknown"),
        "timestamp": kwargs.get("timestamp", now),
        "context": message,
        "actions": kwargs.get("actions", ""),
        "operating_cycle": kwargs.get("operating_cycle", AGENT_OPERATING_CYCLE_TEXT),
        "cycle_checklist": kwargs.get(
            "cycle_checklist",
            CYCLE_CHECKLIST_TEXT.format(
                agent_id=kwargs.get("recipient", "Agent-1")
            ),
        ),
        "swarm_coordination": kwargs.get(
            "swarm_coordination",
            SWARM_COORDINATION_TEXT,
        ),
        "discord_reporting": kwargs.get(
            "discord_reporting",
            DISCORD_REPORTING_POLICY,
        ),
        "mode": kwargs.get("mode", "HARD"),
        "fallback": kwargs.get("fallback", ""),
        "footer": kwargs.get("footer", ""),
        "fsm_state": kwargs.get("fsm_state", "UNKNOWN"),
    }
    return template.format(**payload)
