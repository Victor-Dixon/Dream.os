#!/usr/bin/env python3
"""
Messaging Template Dispatcher
=============================

SSOT helper for selecting the correct template based on:
- category (S2A/D2A/C2A/A2A)
- tags
- message_type
- optional explicit template_key override

Goal:
- eliminate template drift
/- prevent ack-loop regressions (S2A no-reply posture is baked into templates)
- ensure Agent Operating Cycle is always injected for S2A

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

from typing import Any, Optional

from .messaging_models import MessageCategory, UnifiedMessage, UnifiedMessageTag, UnifiedMessageType
from .messaging_template_texts import (
    AGENT_OPERATING_CYCLE_TEXT,
    CYCLE_CHECKLIST_TEXT,
    DISCORD_REPORTING_TEXT,
    MESSAGE_TEMPLATES,
    SWARM_COORDINATION_TEXT,
    format_d2a_payload,
)


# -----------------------------------------
# S2A Template Keys (canonical)
# -----------------------------------------
S2A_KEYS = {
    "CONTROL",
    "SWARM_PULSE",
    "ONBOARDING",  # Unified onboarding template
    "HARD_ONBOARDING",  # DEPRECATED: Use ONBOARDING with mode="HARD"
    "SOFT_ONBOARDING",  # DEPRECATED: Use ONBOARDING with mode="SOFT"
    "PASSDOWN",
    "TELEPHONE_STATUS_GAME",
    "TASK_CYCLE",
    "FSM_UPDATE",
    "DEBATE_CYCLE",
    "CYCLE_V2",
}

# Priority-ordered tag routing: first match wins.
S2A_TAG_ROUTING = [
    (UnifiedMessageTag.ONBOARDING, "ONBOARDING"),  # unified onboarding template
    (UnifiedMessageTag.WRAPUP, "PASSDOWN"),
    (UnifiedMessageTag.SYSTEM, "CONTROL"),
    (UnifiedMessageTag.COORDINATION, "TASK_CYCLE"),  # system coordination = cycle tasks
]

# MessageType hinting for S2A when tags are missing.
S2A_TYPE_ROUTING = {
    UnifiedMessageType.ONBOARDING: "ONBOARDING",  # unified onboarding template
    UnifiedMessageType.SYSTEM_TO_AGENT: "CONTROL",
    UnifiedMessageType.MULTI_AGENT_REQUEST: "CONTROL",
    UnifiedMessageType.BROADCAST: "CONTROL",
}


def _safe_get_s2a_template(template_key: str) -> str:
    templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
    return templates.get(template_key) or templates.get("CONTROL") or ""


def _infer_s2a_template_key(msg: UnifiedMessage) -> str:
    """Infer S2A template key from tags and message_type."""
    tag_set = set(msg.tags or [])
    for tag, key in S2A_TAG_ROUTING:
        if tag in tag_set:
            return key
    hinted = S2A_TYPE_ROUTING.get(msg.message_type)
    if hinted:
        return hinted
    return "CONTROL"


def format_s2a_message(template_key: str, **kwargs: Any) -> str:
    """Public S2A formatter: always injects operating cycle."""
    template = _safe_get_s2a_template(template_key)
    kwargs.setdefault("operating_cycle", AGENT_OPERATING_CYCLE_TEXT)
    kwargs.setdefault("cycle_checklist", CYCLE_CHECKLIST_TEXT)
    kwargs.setdefault("discord_reporting", DISCORD_REPORTING_TEXT)
    kwargs.setdefault("swarm_coordination", SWARM_COORDINATION_TEXT)
    # Ensure all required base fields are present
    kwargs.setdefault("priority", "normal")
    kwargs.setdefault("message_id", "msg_unknown")
    kwargs.setdefault("timestamp", "")
    kwargs.setdefault("sender", "SYSTEM")
    kwargs.setdefault("recipient", "Agent-1")
    kwargs.setdefault("context", "")
    kwargs.setdefault("actions", "")
    kwargs.setdefault("fallback", "Escalate to Captain.")
    # ONBOARDING template requires mode and footer fields
    if template_key == "ONBOARDING":
        kwargs.setdefault("mode", "HARD")  # Default to HARD if not specified
        kwargs.setdefault("footer", "")  # Default to no footer
    return template.format(**kwargs)


def dispatch_template_key(
    msg: UnifiedMessage,
    explicit_key: Optional[str] = None,
) -> str:
    """
    Decide which template key to use.
    - If explicit_key is provided and valid for the category, use it.
    - Otherwise infer based on category + tags + type.
    """
    if msg.category == MessageCategory.S2A:
        if explicit_key and explicit_key in S2A_KEYS:
            return explicit_key
        return _infer_s2a_template_key(msg)

    # Non-S2A categories usually have a single template string
    return explicit_key or "DEFAULT"


DEVLOG_FOOTER = (
    "\n\nDocumentation\n"
    "- Update status.json\n"
    "- Post Discord devlog for completed actions\n"
)

WORKFLOWS_FOOTER = (
    "\n\nCore workflows\n"
    "- Claim task: python src/services/messaging_cli.py --agent <agent> --get-next-task\n"
    "- Send message: python src/services/messaging_cli.py --agent <agent> -m \"Context + actions\"\n"
    "- Post devlog: python tools/devlog_manager.py --agent <agent> --message \"What changed / evidence / links\"\n"
    "- Commit with agent flag: git commit -m \"agent-<n>: short description\"\n"
)


def render_message(
    msg: UnifiedMessage,
    *,
    template_key: Optional[str] = None,
    include_devlog: bool = False,
    include_workflows: bool = False,
    **payload: Any,
) -> str:
    """
    Render a message using canonical templates.

    Expected payload fields vary by category/template.
    This function standardizes common header fields.
    """
    base = {
        "sender": msg.sender,
        "recipient": msg.recipient,
        "priority": getattr(msg.priority, "value", str(msg.priority)),
        "message_id": msg.message_id,
        "timestamp": msg.timestamp,
        "content": msg.content,  # Required for D2A template
    }
    base.update(payload)

    # Provide safe defaults to avoid KeyErrors in templates
    base.setdefault("context", "")
    base.setdefault("actions", "")
    base.setdefault("fallback", "Escalate to Captain.")
    base.setdefault("cycle_checklist", CYCLE_CHECKLIST_TEXT)
    base.setdefault("discord_reporting", DISCORD_REPORTING_TEXT)
    base.setdefault("swarm_coordination", SWARM_COORDINATION_TEXT)
    
    # C2A template defaults
    base.setdefault("task", base.get("actions", "Complete assigned task"))
    base.setdefault("deliverable", base.get("actions", "Complete assigned deliverable"))
    base.setdefault("eta", "TBD")
    
    # A2A template defaults
    base.setdefault("ask", base.get("actions", "Coordination request"))
    base.setdefault("next_step", base.get("actions", "Proceed with coordination"))
    
    # CYCLE_V2 template defaults
    base.setdefault("mission", base.get("context", "Complete assigned mission"))
    base.setdefault("dod", "Definition of Done: Complete task with evidence")
    base.setdefault("ssot_constraint", "Maintain SSOT compliance")
    base.setdefault("v2_constraint", "Follow V2 compliance standards")
    base.setdefault("touch_surface", "Minimal - only necessary files")
    base.setdefault("validation_required", "Run tests and verify changes")
    base.setdefault("priority_level", base.get("priority", "normal"))
    base.setdefault("handoff_expectation", "Report completion with evidence")

    category = getattr(msg, "category", None)

    # If older code hasn't added msg.category yet, infer from types:
    if category is None:
        if msg.message_type in (
            UnifiedMessageType.SYSTEM_TO_AGENT,
            UnifiedMessageType.ONBOARDING,
            UnifiedMessageType.MULTI_AGENT_REQUEST,
            UnifiedMessageType.BROADCAST,
        ):
            category = MessageCategory.S2A
        elif msg.message_type == UnifiedMessageType.CAPTAIN_TO_AGENT:
            category = MessageCategory.C2A
        elif msg.message_type == UnifiedMessageType.AGENT_TO_AGENT:
            category = MessageCategory.A2A
        elif msg.message_type == UnifiedMessageType.BROADCAST:
            category = MessageCategory.S2A  # BROADCAST is S2A
        else:
            category = MessageCategory.D2A

    # S2A: use sub-templates
    if category == MessageCategory.S2A:
        key = dispatch_template_key(msg, explicit_key=template_key)
        rendered = format_s2a_message(key, **base)
        if include_devlog:
            rendered += DEVLOG_FOOTER
        if include_workflows:
            rendered += WORKFLOWS_FOOTER
        return rendered

    # D2A/C2A/A2A: single-string templates
    tpl = MESSAGE_TEMPLATES.get(category)
    if isinstance(tpl, str):
        # Ensure required fields for D2A template are present
        if category == MessageCategory.D2A:
            base = format_d2a_payload(base)
        rendered = tpl.format(**base)
        if include_devlog:
            rendered += DEVLOG_FOOTER
        if include_workflows:
            rendered += WORKFLOWS_FOOTER
        return rendered

    # Fallback to S2A control if nothing matches (safety net)
    default = _safe_get_s2a_template("CONTROL")
    base.setdefault("context", "")
    base.setdefault("actions", "")
    base.setdefault("fallback", "Escalate to Captain.")
    base.setdefault("operating_cycle", AGENT_OPERATING_CYCLE_TEXT)
    rendered = default.format(**base)
    if include_devlog:
        rendered += DEVLOG_FOOTER
    if include_workflows:
        rendered += WORKFLOWS_FOOTER
    return rendered


__all__ = [
    "dispatch_template_key",
    "render_message",
    "format_s2a_message",
    "S2A_KEYS",
]

