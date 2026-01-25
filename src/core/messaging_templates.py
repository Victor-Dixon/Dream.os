#!/usr/bin/env python3
"""
Messaging Templates - Core Layer
================================

<!-- SSOT Domain: communication -->

Compatibility layer for message rendering. Provides a stable interface for
rendering core messaging templates while delegating to the canonical template
text sources under messaging_templates_data.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any

from .messaging_models import (
    MessageCategory,
    UnifiedMessage,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from .messaging_templates_data.cycle_texts import (
    AGENT_OPERATING_CYCLE_TEXT,
    CYCLE_CHECKLIST_TEXT,
)
from .messaging_templates_data.coordination_texts import SWARM_COORDINATION_TEXT
from .messaging_templates_data.s2a_templates_core import S2A_TEMPLATES_CORE
from .messaging_templates_data.template_d2a import D2A_TEMPLATE

DISCORD_REPORTING_POLICY = (
    "DISCORD REPORTING POLICY — CRITICAL VISIBILITY\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Discord is the primary visibility channel.\n"
    "Post completion reports with task, actions, and artifacts.\n\n"
)

DISCORD_RESPONSE_POLICY = (
    "Discord Response Policy\n"
    "- Respond with artifacts, validation results, or coordination output.\n"
    "- Avoid acknowledgment-only replies.\n"
)

PREFERRED_REPLY_FORMAT = (
    "Preferred Reply Format\n"
    "- Task: <short description>\n"
    "- Actions Taken: bullet list\n"
    "- Artifacts: exact paths\n"
    "- Status: ✅ done or 🟡 blocked\n"
)

S2A_KEYS = ["CONTROL", "SWARM_PULSE", "HARD_ONBOARDING"]


def _escape_format(value: str) -> str:
    return value.replace("{", "{{").replace("}", "}}")


def _format_timestamp(value: Any) -> str:
    if isinstance(value, str):
        return value
    if not value:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return value.strftime("%Y-%m-%d %H:%M:%S")


def dispatch_template_key(message: UnifiedMessage, explicit_key: str | None = None) -> str:
    if explicit_key:
        return explicit_key
    if message.category != MessageCategory.S2A:
        return "DEFAULT"
    if UnifiedMessageTag.ONBOARDING in (message.tags or []):
        return "HARD_ONBOARDING"
    if message.message_type == UnifiedMessageType.ONBOARDING:
        return "HARD_ONBOARDING"
    return "CONTROL"


def format_s2a_message(template_key: str, **kwargs: Any) -> str:
    template = S2A_TEMPLATES_CORE.get("CONTROL")
    if template_key == "HARD_ONBOARDING":
        template = S2A_TEMPLATES_CORE.get("ONBOARDING", template)
    else:
        template = S2A_TEMPLATES_CORE.get(template_key, template)

    payload = {
        "sender": kwargs.get("sender", "SYSTEM"),
        "recipient": kwargs.get("recipient", "Agent"),
        "priority": kwargs.get("priority", "regular"),
        "message_id": kwargs.get("message_id", "unknown"),
        "timestamp": kwargs.get("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
        "context": _escape_format(kwargs.get("context", "")),
        "actions": kwargs.get("actions", ""),
        "operating_cycle": kwargs.get("operating_cycle", AGENT_OPERATING_CYCLE_TEXT),
        "cycle_checklist": kwargs.get("cycle_checklist", CYCLE_CHECKLIST_TEXT),
        "swarm_coordination": kwargs.get("swarm_coordination", SWARM_COORDINATION_TEXT),
        "discord_reporting": kwargs.get("discord_reporting", DISCORD_REPORTING_POLICY),
        "mode": kwargs.get("mode", "HARD"),
    }
    return template.format(**payload)


def _infer_category(message: UnifiedMessage) -> MessageCategory:
    if message.category:
        return message.category
    message_type = message.message_type
    if message_type in {UnifiedMessageType.BROADCAST, UnifiedMessageType.SYSTEM_TO_AGENT}:
        return MessageCategory.S2A
    if message_type == UnifiedMessageType.HUMAN_TO_AGENT:
        return MessageCategory.D2A
    if message_type == UnifiedMessageType.CAPTAIN_TO_AGENT:
        return MessageCategory.C2A
    if message_type == UnifiedMessageType.AGENT_TO_AGENT:
        return MessageCategory.A2A
    return MessageCategory.S2A


def _render_d2a(message: UnifiedMessage) -> str:
    metadata = message.metadata or {}
    payload = {
        "content": _escape_format(message.content),
        "interpretation": metadata.get("interpretation", "Interpret and execute."),
        "actions": metadata.get("actions", "Provide a concrete plan and run validation."),
        "discord_response_policy": DISCORD_RESPONSE_POLICY,
        "d2a_report_format": PREFERRED_REPLY_FORMAT,
        "fallback": metadata.get("fallback", "Ask for clarification only if blocked."),
    }
    return D2A_TEMPLATE.format(**payload)


def render_message(message: UnifiedMessage, **kwargs: Any) -> str:
    """Render a UnifiedMessage into a template string."""
    category = _infer_category(message)

    if category == MessageCategory.S2A:
        template_key = dispatch_template_key(message, explicit_key=kwargs.get("template_key"))
        return format_s2a_message(
            template_key,
            sender=message.sender,
            recipient=message.recipient,
            priority=getattr(message.priority, "value", message.priority),
            message_id=message.message_id,
            timestamp=_format_timestamp(message.timestamp),
            context=kwargs.get("context", message.content),
            actions=kwargs.get("actions", ""),
        )

    if category == MessageCategory.D2A:
        return _render_d2a(message)

    fallback = {
        "category": category.value,
        "message": asdict(message),
    }
    return f"[HEADER] {category.value.upper()}\n{fallback}"


__all__ = [
    "dispatch_template_key",
    "format_s2a_message",
    "render_message",
    "S2A_KEYS",
]
