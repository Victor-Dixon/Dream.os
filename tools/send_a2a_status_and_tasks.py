#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Send A2A directives to all agents with two tasks:
1) Update status.json with current focus (enables Discord bot start).
2) Execute a concrete follow-up per domain.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

from src.core.messaging_templates import render_message
from src.core.messaging_models_core import (
    UnifiedMessage,
    MessageCategory,
    UnifiedMessagePriority,
    UnifiedMessageType,
)
from src.services.messaging_infrastructure import MessageCoordinator

DEVLOG_REMINDER = "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"


def send(agent: str, content: str, interpretation: str, actions: str, fallback: str = "If blocked, send blocker + proposed fix + owner.") -> None:
    msg = UnifiedMessage(
        content=content,
        sender="Agent-7",
        recipient=agent,
        priority=UnifiedMessagePriority.REGULAR,
        category=MessageCategory.A2A,
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
    )
    rendered = render_message(
        msg,
        interpretation=interpretation,
        actions=actions + "\n\n" + DEVLOG_REMINDER,
        ask="",  # placeholder to satisfy A2A template fields
        context="",  # placeholder for A2A template fields
        next_step="",  # placeholder for A2A template fields
        fallback=fallback,
    )
    MessageCoordinator.send_to_agent(
        agent=agent,
        message=rendered,
        priority=UnifiedMessagePriority.REGULAR,
        use_pyautogui=True,
        sender="Agent-7",
        message_category=MessageCategory.A2A,
    )


def main():
    tasks = [
        {
            "agent": "Agent-1",
            "content": "Two actions: refresh status and close deployment blockers.",
            "interpretation": "Update status.json with current focus; then push GitHub/PR auth unblock and report.",
            "actions": (
                "1) Update status.json now with current mission, priority, and today’s focus (needed to start Discord bot).\n"
                "2) Finish GitHub auth/PR unblock: verify gh CLI token flow, retry PR creation for pending repos (Case Variations/Trading), and drop a short report with outcomes + remaining blockers."
            ),
        },
        {
            "agent": "Agent-2",
            "content": "Two actions: refresh status and verify web deploy readiness.",
            "interpretation": "Update status.json; then confirm freerideinvestor/prismblossom deployment readiness (architecture/SSOT).",
            "actions": (
                "1) Update status.json now with current mission and today’s slice.\n"
                "2) Review freerideinvestor/prismblossom deployment readiness: confirm architecture/SSOT boundaries intact after recent theme pushes; flag any remaining CSS/functional gaps and hand back a 3-bullet readiness note."
            ),
        },
        {
            "agent": "Agent-3",
            "content": "Two actions: refresh status and support deployment infra.",
            "interpretation": "Update status.json; then validate infrastructure hooks for site deploys and message queue health.",
            "actions": (
                "1) Update status.json now with current mission and today’s focus.\n"
                "2) Infra check: validate WP deploy hooks (SFTP 65002 path, wp-cli path) and message queue processor health; send a 3-line checklist (deploy path ok, wp-cli ok, queue processor running) with any fixes applied."
            ),
        },
        {
            "agent": "Agent-5",
            "content": "Two actions: refresh status and BI verification.",
            "interpretation": "Update status.json; then confirm analytics/BI readiness and outstanding timeout/constants loop closure.",
            "actions": (
                "1) Update status.json now with current mission and today’s slice.\n"
                "2) BI check: confirm unified tools metrics/timeout constants loop closure status and note any remaining debt; share a 3-bullet summary (done, pending, blockers)."
            ),
        },
        {
            "agent": "Agent-6",
            "content": "Two actions: refresh status and coordinate loop closure + Discord bot start.",
            "interpretation": "Update status.json; then coordinate loop closure readiness and confirm Discord bot start precheck.",
            "actions": (
                "1) Update status.json now with current mission and today’s focus (needed to start Discord bot).\n"
                "2) Coordination: confirm loop closure tracker + PR merge tracker are current; give a go/no-go for Discord bot start with any blockers listed."
            ),
        },
        {
            "agent": "Agent-7",
            "content": "Two actions: refresh status and verify freerideinvestor nav cleanup.",
            "interpretation": "Update status.json; then confirm nav cleanup on freerideinvestor (no developer tool links).",
            "actions": (
                "1) Update your status.json with current mission and today’s work.\n"
                "2) Verify freerideinvestor nav: ensure header fallback is removed and only primary menu shows; if cache still shows stale links, rerun purge and capture a before/after note."
            ),
        },
        {
            "agent": "Agent-8",
            "content": "Two actions: refresh status and SSOT/QA sweep post-deploy.",
            "interpretation": "Update status.json; then run a quick SSOT/QA sweep on the recent web deploy changes.",
            "actions": (
                "1) Update status.json now with current mission and today’s slice.\n"
                "2) Run a quick SSOT/QA sweep on freerideinvestor theme updates: confirm no SSOT drift (config/search/query) and note any QA issues; return a 3-bullet finding report."
            ),
        },
    ]

    for t in tasks:
        send(
            agent=t["agent"],
            content=t["content"],
            interpretation=t["interpretation"],
            actions=t["actions"],
        )


if __name__ == "__main__":
    main()

