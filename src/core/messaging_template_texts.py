#!/usr/bin/env python3
"""
Messaging Template Texts - Core Layer
====================================

SSOT-backed template storage and formatting helpers.

<!-- SSOT Domain: integration -->

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

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
)
from .messaging_templates_data.registry import build_message_templates


MESSAGE_TEMPLATES = build_message_templates()


def format_d2a_payload(payload: Dict[str, Any]) -> Dict[str, str]:
    """
    Format Discord-to-Agent payload with SSOT defaults.

    Args:
        payload: Payload data

    Returns:
        Payload dict with required D2A template fields.
    """
    return {
        "interpretation": payload.get("interpretation", "Interpret the request and summarize intent."),
        "actions": payload.get("actions", "Propose concrete actions with evidence."),
        "discord_response_policy": payload.get("discord_response_policy", DISCORD_RESPONSE_POLICY),
        "d2a_report_format": payload.get("d2a_report_format", D2A_REPORT_FORMAT),
        "fallback": payload.get("fallback", "If clarification needed: ask one precise question."),
    }


def format_s2a_message(message: str, **kwargs: Any) -> str:
    """
    Format System-to-Agent message using the CONTROL template.

    Args:
        message: Base message
        **kwargs: Additional formatting parameters

    Returns:
        Formatted message string
    """
    template = MESSAGE_TEMPLATES[MessageCategory.S2A]["CONTROL"]
    now = datetime.now().isoformat(timespec="seconds")
    return template.format(
        sender=kwargs.get("sender", "SYSTEM"),
        recipient=kwargs.get("recipient", "Agent-1"),
        priority=kwargs.get("priority", "regular"),
        message_id=kwargs.get("message_id", "unknown"),
        timestamp=kwargs.get("timestamp", now),
        context=message,
        operating_cycle=AGENT_OPERATING_CYCLE_TEXT,
        cycle_checklist=CYCLE_CHECKLIST_TEXT.format(agent_id=kwargs.get("recipient", "Agent-1")),
        swarm_coordination=SWARM_COORDINATION_TEXT,
        discord_reporting=DISCORD_REPORTING_POLICY,
    )
