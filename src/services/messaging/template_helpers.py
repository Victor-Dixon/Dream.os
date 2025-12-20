#!/usr/bin/env python3
"""
Template Helpers - Messaging Infrastructure
==========================================

<!-- SSOT Domain: integration -->

Helper functions for message template application.
Extracted from message_formatters.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority
from src.core.messaging_models_core import MessageCategory, MESSAGE_TEMPLATES, format_d2a_payload


def build_d2a_payload(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Build D2A payload from metadata."""
    return {
        k: v
        for k, v in {
            "interpretation": meta.get("interpretation"),
            "actions": meta.get("actions"),
            "fallback": meta.get("fallback"),
            "discord_response_policy": meta.get("discord_response_policy"),
            "d2a_report_format": meta.get("d2a_report_format"),
        }.items()
        if v is not None
    }


def format_d2a_template(
    tmpl: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    message: str,
    now: str,
    d2a_meta: Dict[str, Any],
) -> str:
    """Format D2A template with metadata."""
    return tmpl.format(
        sender=sender,
        recipient=recipient,
        priority=priority.value,
        message_id=message_id,
        timestamp=now,
        content=message,
        interpretation=d2a_meta["interpretation"],
        actions=d2a_meta["actions"],
        discord_response_policy=d2a_meta["discord_response_policy"],
        d2a_report_format=d2a_meta["d2a_report_format"],
        fallback=d2a_meta["fallback"],
    )


def prepare_d2a_template(
    tmpl: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    message: str,
    now: str,
    meta: Dict[str, Any],
) -> str:
    """Prepare D2A template with proper payload formatting."""
    d2a_payload = build_d2a_payload(meta)
    d2a_meta = format_d2a_payload(d2a_payload)
    try:
        result = format_d2a_template(
            tmpl, sender, recipient, priority, message_id, message, now, d2a_meta)
        return validate_d2a_result(result, message, d2a_meta)
    except Exception:
        return message


def validate_d2a_result(result: str, message: str, d2a_meta: Dict[str, Any]) -> str:
    """Validate and fix D2A template result to prevent message duplication."""
    message_count = result.count(message)
    if message_count > 1:
        user_message_section = "User Message:\n"
        if user_message_section in result:
            section_start = result.find(
                user_message_section) + len(user_message_section)
            section_end = result.find("\n\n", section_start)
            if section_end == -1:
                section_end = len(result)
            content_section = result[section_start:section_end]
            if message in content_section:
                if result.endswith(message):
                    result = result[:-len(message)].rstrip()
                if f"Proposed Action:\n{message}" in result:
                    result = result.replace(
                        f"Proposed Action:\n{message}",
                        f"Proposed Action:\n{d2a_meta['actions']}"
                    )
    return result


def prepare_a2a_template(
    tmpl: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    message: str,
    now: str,
    meta: Dict[str, Any],
) -> str:
    """Prepare A2A template with ask/context/next_step/fallback."""
    return tmpl.format(
        sender=sender,
        recipient=recipient,
        priority=priority.value,
        message_id=message_id,
        timestamp=now,
        agent_id=meta.get("agent_id", recipient),
        ask=meta.get("ask", message),
        context=meta.get("context", ""),
        coordination_rationale=meta.get("coordination_rationale", "To leverage parallel processing and accelerate completion"),
        expected_contribution=meta.get("expected_contribution", "Domain expertise and parallel execution"),
        coordination_timeline=meta.get("coordination_timeline", "ASAP - coordination needed to maintain momentum"),
        next_step=meta.get(
            "next_step",
            "Reply via messaging_cli with ACCEPT/DECLINE, ETA, and a 2–3 bullet plan, "
            "then update status.json and MASTER_TASK_LOG.md.",
        ),
        fallback=meta.get(
            "fallback", "If blocked: send blocker + proposed fix + owner."),
    )


def prepare_default_template(
    tmpl: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    message: str,
    now: str,
) -> str:
    """Prepare default template (non-D2A, non-A2A)."""
    return tmpl.format(
        sender=sender,
        recipient=recipient,
        priority=priority.value,
        message_id=message_id,
        timestamp=now,
        content=message,
    )
