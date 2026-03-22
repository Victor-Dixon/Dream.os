#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-messaging-templates
# @registry docs/recovery/recovery_registry.yaml#src-core-messaging-templates

"""UnifiedMessage renderer backed by canonical template registry."""

from __future__ import annotations

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
from .messaging_templates_data.policy_texts import (
    D2A_REPORT_FORMAT,
    DISCORD_REPORTING_POLICY,
    DISCORD_RESPONSE_POLICY,
    PREFERRED_REPLY_FORMAT,
)
from .messaging_templates_data.registry import build_message_templates

MESSAGE_TEMPLATES = build_message_templates()
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
    if UnifiedMessageTag.ONBOARDING in (message.tags or []):
        return "HARD_ONBOARDING"
    if message.message_type == UnifiedMessageType.ONBOARDING:
        return "HARD_ONBOARDING"
    return "CONTROL"


def _infer_category(message: UnifiedMessage) -> MessageCategory:
    if message.category:
        return message.category
    if message.message_type in {UnifiedMessageType.BROADCAST, UnifiedMessageType.SYSTEM_TO_AGENT}:
        return MessageCategory.S2A
    if message.message_type == UnifiedMessageType.HUMAN_TO_AGENT:
        return MessageCategory.D2A
    if message.message_type == UnifiedMessageType.CAPTAIN_TO_AGENT:
        return MessageCategory.C2A
    if message.message_type == UnifiedMessageType.AGENT_TO_AGENT:
        return MessageCategory.A2A
    return MessageCategory.S2A


def format_s2a_message(template_key: str, **kwargs: Any) -> str:
    s2a_templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
    selected = "ONBOARDING" if template_key == "HARD_ONBOARDING" else template_key
    template = s2a_templates.get(selected, s2a_templates.get("CONTROL", "{context}"))
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
        "fallback": kwargs.get("fallback", "Ask for clarification only if blocked."),
        "footer": kwargs.get("footer", ""),
        "fsm_state": kwargs.get("fsm_state", "UNKNOWN"),
        "current_mission": kwargs.get("current_mission", "Not specified"),
        "time_since_update": kwargs.get("time_since_update", "unknown"),
        "next_task": kwargs.get("next_task", "No task assigned"),
        "task_priority": kwargs.get("task_priority", "normal"),
        "task_points": kwargs.get("task_points", "0"),
        "task_status": kwargs.get("task_status", "unassigned"),
    }
    return template.format(**payload)


def render_message(message: UnifiedMessage, **kwargs: Any) -> str:
    """Render UnifiedMessage for S2A, D2A, C2A and A2A flows."""
    category = _infer_category(message)
    metadata = message.metadata or {}

    if category == MessageCategory.S2A:
        key = dispatch_template_key(message, explicit_key=kwargs.get("template_key"))
        return format_s2a_message(
            key,
            sender=message.sender,
            recipient=message.recipient,
            priority=getattr(message.priority, "value", message.priority),
            message_id=message.message_id,
            timestamp=_format_timestamp(message.timestamp),
            context=kwargs.get("context", message.content),
            actions=kwargs.get("actions", metadata.get("actions", "")),
        )

    if category == MessageCategory.D2A:
        template = MESSAGE_TEMPLATES[MessageCategory.D2A]
        interpretation = kwargs.get("interpretation", metadata.get("interpretation", "Interpret and execute."))
        actions = kwargs.get("actions", metadata.get("actions", "Provide a concrete plan and run validation."))
        fallback = kwargs.get("fallback", metadata.get("fallback", "Ask for clarification only if blocked."))
        rendered = template.format(
            content=_escape_format(kwargs.get("content", message.content)),
            interpretation=interpretation,
            actions=actions,
            discord_response_policy=kwargs.get("discord_response_policy", DISCORD_RESPONSE_POLICY),
            preferred_reply_format=kwargs.get("preferred_reply_format", PREFERRED_REPLY_FORMAT),
            d2a_report_format=kwargs.get("d2a_report_format", D2A_REPORT_FORMAT),
            fallback=fallback,
        )
        header = f"[HEADER] D2A DISCORD INTAKE\nFrom: {message.sender}\nTo: {message.recipient}\n\n"
        workflows = "\nCore workflows: intake → interpret → execute → report" if kwargs.get("include_workflows") else ""
        return f"{header}{rendered}{workflows}"

    if category == MessageCategory.C2A:
        template = MESSAGE_TEMPLATES[MessageCategory.C2A]
        rendered = template.format(
            recipient=message.recipient,
            task=_escape_format(kwargs.get("task", message.content)),
            context=_escape_format(kwargs.get("context", metadata.get("context", message.content))),
            swarm_coordination=kwargs.get("swarm_coordination", SWARM_COORDINATION_TEXT),
            cycle_checklist=kwargs.get("cycle_checklist", CYCLE_CHECKLIST_TEXT),
            discord_reporting=kwargs.get("discord_reporting", DISCORD_REPORTING_POLICY),
            deliverable=kwargs.get("deliverable", metadata.get("deliverable", "Ship requested change with validation evidence.")),
            eta=kwargs.get("eta", metadata.get("eta", "next cycle")),
        )
        return f"[HEADER] C2A CAPTAIN DIRECTIVE\nFrom: {message.sender}\nTo: {message.recipient}\n\n{rendered}"

    if category == MessageCategory.A2A:
        template = MESSAGE_TEMPLATES[MessageCategory.A2A]
        next_step = kwargs.get("next_step", metadata.get("next_step", "Proceed with suggested approach."))
        rendered = template.format(
            ask=_escape_format(kwargs.get("ask", message.content)),
            context=_escape_format(kwargs.get("context", metadata.get("context", "Coordination requested."))),
            coordination_rationale=kwargs.get("coordination_rationale", metadata.get("coordination_rationale", "Parallelize work via domain pairing.")),
            expected_contribution=kwargs.get("expected_contribution", metadata.get("expected_contribution", "Provide implementation support and review.")),
            coordination_timeline=kwargs.get("coordination_timeline", metadata.get("coordination_timeline", "ASAP")),
            message_id=message.message_id,
            sender=message.sender,
        )
        return f"{rendered}\nNext Step: {next_step}\n"

    return f"[HEADER] {category.value.upper()}\n{_escape_format(message.content)}"


__all__ = ["MESSAGE_TEMPLATES", "dispatch_template_key", "format_s2a_message", "render_message", "S2A_KEYS"]
