#!/usr/bin/env python3
"""SSOT-backed messaging template text helpers."""

from __future__ import annotations

from typing import Any

from .messaging_models import MessageCategory
from .messaging_templates_data.policy_texts import (
    DISCORD_RESPONSE_POLICY,
    PREFERRED_REPLY_FORMAT,
)
from .messaging_templates_data.registry import build_message_templates

MESSAGE_TEMPLATES = build_message_templates()


def format_d2a_payload(payload: dict[str, Any]) -> str:
    """Format D2A metadata string using canonical policy text."""
    interpretation = payload.get("interpretation", "Interpret and execute.")
    actions = payload.get("actions", "Provide a concrete plan and run validation.")
    fallback = payload.get("fallback", "Ask for clarification only if blocked.")
    return (
        f"interpretation={interpretation}\n"
        f"actions={actions}\n"
        f"policy={DISCORD_RESPONSE_POLICY}\n"
        f"format={PREFERRED_REPLY_FORMAT}\n"
        f"fallback={fallback}"
    )


def format_s2a_message(message: str, **kwargs: Any) -> str:
    """Render an S2A message via the canonical registry."""
    templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
    template_key = kwargs.get("template_key", "CONTROL")
    template = templates.get(template_key, templates.get("CONTROL", "{context}"))
    payload = {
        "sender": kwargs.get("sender", "SYSTEM"),
        "recipient": kwargs.get("recipient", "Agent"),
        "priority": kwargs.get("priority", "regular"),
        "message_id": kwargs.get("message_id", "unknown"),
        "timestamp": kwargs.get("timestamp", "unknown"),
        "context": message,
        "actions": kwargs.get("actions", ""),
        "operating_cycle": kwargs.get("operating_cycle", ""),
        "cycle_checklist": kwargs.get("cycle_checklist", ""),
        "swarm_coordination": kwargs.get("swarm_coordination", ""),
        "discord_reporting": kwargs.get("discord_reporting", ""),
        "mode": kwargs.get("mode", "HARD"),
        "fallback": kwargs.get("fallback", ""),
        "footer": kwargs.get("footer", ""),
        "fsm_state": kwargs.get("fsm_state", "UNKNOWN"),
    }
    return template.format(**payload)
