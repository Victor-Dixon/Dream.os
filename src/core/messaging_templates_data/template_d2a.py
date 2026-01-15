"""
D2A (Discord → Agent) template string.

<!-- SSOT Domain: integration -->
"""

D2A_TEMPLATE = (
    "Origin:\n"
    "- Discord → Agent intake\n\n"
    "User Message:\n"
    "{content}\n\n"
    "Interpretation (agent):\n"
    "{interpretation}\n\n"
    "Proposed Action:\n"
    "{actions}\n\n"
    "Operating Cycle (fast reminder):\n"
    "1) Claim → 2) Sync → 3) Slice → 4) Execute → 5) Validate → 6) Commit → 7) Report evidence\n"
    "- No chat-only replies; status.json-only updates do NOT count as progress.\n"
    "- Report with artifact/validation/delegation in Discord.\n\n"
    "{discord_response_policy}\n"
    "{d2a_report_format}\n"
    "Devlog Command (for recipient):\n"
    "\n"
    "Note: Tool automatically truncates content >1900 chars for Discord. Full devlog saved in workspace.\n\n"
    "If clarification needed:\n"
    "{fallback}\n"
    "#DISCORD #D2A\n"
)



