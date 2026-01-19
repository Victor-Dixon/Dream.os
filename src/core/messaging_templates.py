"""
Messaging Templates - Rendering Helpers
======================================

SSOT-backed rendering for unified messages.

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from .messaging_models import MessageCategory, UnifiedMessage, UnifiedMessageTag, UnifiedMessageType
from .messaging_template_texts import MESSAGE_TEMPLATES, format_d2a_payload
from .messaging_templates_data.coordination_texts import SWARM_COORDINATION_TEXT
from .messaging_templates_data.cycle_texts import AGENT_OPERATING_CYCLE_TEXT, CYCLE_CHECKLIST_TEXT
from .messaging_templates_data.policy_texts import (
    D2A_REPORT_FORMAT,
    DISCORD_REPORTING_POLICY,
    DISCORD_RESPONSE_POLICY,
)


def _resolve_category(message: UnifiedMessage) -> MessageCategory:
    if message.category is not None:
        return message.category
    if message.message_type == UnifiedMessageType.BROADCAST:
        return MessageCategory.S2A
    return MessageCategory.S2A


def _base_tokens(message: UnifiedMessage) -> Dict[str, Any]:
    now = datetime.now().isoformat(timespec="seconds")
    return {
        "sender": message.sender,
        "recipient": message.recipient,
        "priority": message.priority.value if hasattr(message.priority, "value") else str(message.priority),
        "message_id": message.message_id,
        "timestamp": message.timestamp.isoformat() if hasattr(message.timestamp, "isoformat") else now,
        "context": message.content,
        "content": message.content,
    }


def _render_s2a(message: UnifiedMessage, template_key: str) -> str:
    tokens = _base_tokens(message)
    tokens.update(
        {
            "operating_cycle": AGENT_OPERATING_CYCLE_TEXT,
            "cycle_checklist": CYCLE_CHECKLIST_TEXT.format(agent_id=message.recipient),
            "swarm_coordination": SWARM_COORDINATION_TEXT,
            "discord_reporting": DISCORD_REPORTING_POLICY,
            "mode": message.metadata.get("mode", "HARD"),
            "actions": message.metadata.get("actions", "- Follow onboarding checklist."),
        }
    )
    template = MESSAGE_TEMPLATES[MessageCategory.S2A][template_key]
    return template.format(**tokens)


def _render_d2a(message: UnifiedMessage) -> str:
    tokens = _base_tokens(message)
    payload = format_d2a_payload(message.metadata)
    tokens.update(
        {
            "interpretation": payload["interpretation"],
            "actions": payload["actions"],
            "discord_response_policy": payload.get("discord_response_policy", DISCORD_RESPONSE_POLICY),
            "d2a_report_format": payload.get("d2a_report_format", D2A_REPORT_FORMAT),
            "fallback": payload["fallback"],
        }
    )
    return MESSAGE_TEMPLATES[MessageCategory.D2A].format(**tokens)


def _render_c2a(message: UnifiedMessage) -> str:
    tokens = _base_tokens(message)
    tokens.update(
        {
            "task": message.metadata.get("task", message.content),
            "deliverable": message.metadata.get("deliverable", "Provide evidence-backed update."),
            "eta": message.metadata.get("eta", "Next cycle"),
            "swarm_coordination": SWARM_COORDINATION_TEXT,
            "cycle_checklist": CYCLE_CHECKLIST_TEXT.format(agent_id=message.recipient),
            "discord_reporting": DISCORD_REPORTING_POLICY,
        }
    )
    return MESSAGE_TEMPLATES[MessageCategory.C2A].format(**tokens)


def _render_a2a(message: UnifiedMessage) -> str:
    tokens = _base_tokens(message)
    tokens.update(
        {
            "agent_id": message.metadata.get("agent_id", message.recipient),
            "ask": message.metadata.get("ask", message.content),
            "context": message.metadata.get("context", ""),
            "coordination_rationale": message.metadata.get(
                "coordination_rationale", "To leverage parallel processing and accelerate completion"
            ),
            "expected_contribution": message.metadata.get(
                "expected_contribution", "Domain expertise and parallel execution"
            ),
            "coordination_timeline": message.metadata.get(
                "coordination_timeline", "ASAP - coordination needed to maintain momentum"
            ),
            "next_step": message.metadata.get(
                "next_step",
                "Reply via messaging_cli with ACCEPT/DECLINE, ETA, and a 2–3 bullet plan.",
            ),
            "fallback": message.metadata.get(
                "fallback", "If blocked: send blocker + proposed fix + owner."
            ),
        }
    )
    return MESSAGE_TEMPLATES[MessageCategory.A2A].format(**tokens)


def render_message(message: UnifiedMessage) -> str:
    """
    Render a UnifiedMessage using SSOT templates.

    Args:
        message: UnifiedMessage instance

    Returns:
        Rendered template string.
    """
    category = _resolve_category(message)
    if category == MessageCategory.S2A:
        template_key = "CONTROL"
        if UnifiedMessageTag.ONBOARDING in message.tags or message.message_type == UnifiedMessageType.ONBOARDING:
            template_key = "ONBOARDING"
        return _render_s2a(message, template_key)
    if category == MessageCategory.D2A:
        return _render_d2a(message)
    if category == MessageCategory.C2A:
        return _render_c2a(message)
    if category == MessageCategory.A2A:
        return _render_a2a(message)
    return message.content
