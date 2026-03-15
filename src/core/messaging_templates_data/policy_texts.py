# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-messaging-templates-data-policy-texts
# @registry docs/recovery/recovery_registry.yaml#src-core-messaging-templates-data-policy-texts

"""Canonical policy text definitions for messaging templates.

<!-- SSOT Domain: communication -->
"""

DISCORD_REPORTING_POLICY = (
    "DISCORD REPORTING POLICY — CRITICAL VISIBILITY\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Discord is the primary visibility channel.\n"
    "Post completion reports with task, actions, and artifacts.\n"
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

D2A_REPORT_FORMAT = (
    "D2A Report Format\n"
    "- Interpretation: concise intent summary\n"
    "- Actions: concrete execution steps\n"
    "- Evidence: artifacts + validation command output\n"
    "- Status: ✅ done or 🟡 blocked\n"
)

__all__ = [
    "DISCORD_REPORTING_POLICY",
    "DISCORD_RESPONSE_POLICY",
    "PREFERRED_REPLY_FORMAT",
    "D2A_REPORT_FORMAT",
]
