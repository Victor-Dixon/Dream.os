"""
<!-- SSOT Domain: discord -->

Compatibility-safe broadcast template registry.

This module is the SSOT-backed import target for enhanced broadcast templates.
Controllers may fall back to legacy template sources when these templates are
absent, so this file must always expose ``ENHANCED_BROADCAST_TEMPLATES``.
"""

ENHANCED_BROADCAST_TEMPLATES = {
    "architectural": [
        {
            "name": "Architecture Review",
            "emoji": "🏗️",
            "message": "[C2A] Architecture Review\n\nPriority: REGULAR\nStatus: DESIGN_REVIEW\n\nPlease review architecture deltas and document decisions in SSOT artifacts.",
            "priority": "regular",
        },
        {
            "name": "Contract Drift Check",
            "emoji": "🧭",
            "message": "[C2A] Contract Drift Check\n\nPriority: REGULAR\nStatus: CONTRACT_GUARD\n\nRun recovery/header validators and report drift findings with exact file references.",
            "priority": "regular",
        },
    ],
    "agent_commands": [
        {
            "name": "Sync Status",
            "emoji": "🤖",
            "message": "[C2A] Agent Command: Sync Status\n\nPriority: REGULAR\nStatus: STATUS_SYNC\n\nAll agents: sync status, blockers, and current repair target in inbox updates.",
            "priority": "regular",
        },
        {
            "name": "Escalate Blocker",
            "emoji": "🚧",
            "message": "[C2A] Agent Command: Escalate Blocker\n\nPriority: URGENT\nStatus: BLOCKER_ESCALATION\n\nEscalate hard blockers with reproduction command and affected contract boundary.",
            "priority": "urgent",
        },
    ],
}
