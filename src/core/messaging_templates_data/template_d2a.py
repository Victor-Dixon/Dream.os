"""
D2A (Discord → Agent) template string.

<!-- SSOT Domain: integration -->
"""

D2A_TEMPLATE = (
    "[HEADER] D2A DISCORD INTAKE\n"
    "From: {sender}\n"
    "To: {recipient}\n"
    "Priority: {priority}\n"
    "Message ID: {message_id}\n"
    "Timestamp: {timestamp}\n\n"
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    "🚀 **PROTOCOL UPDATE: Dumb Messages → Real Work Discovery**\n"
    "When you receive repetitive or 'dumb' coordination messages, don't just acknowledge them. Instead:\n"
    "- Search the codebase for TODO/FIXME items and real work opportunities\n"
    "- Prioritize by strategic impact (AI integration > technical debt > maintenance)\n"
    "- Execute complete implementation with testing and documentation\n"
    "- Make work publicly visible through git commits, devlogs, and blog posts\n"
    "- Transform message receipt into forward momentum, not confirmation loops\n\n"
<<<<<<< HEAD
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
    "{devlog_command}\n"
=======
    "python tools/devlog_poster.py --agent {recipient} --file <devlog_path>\n"
    "Examples:\n"
    "  python tools/devlog_poster.py --agent Agent-1 --file agent_workspaces/Agent-1/devlogs/status.md\n"
    "  python tools/devlog_poster.py --agent Agent-7 --file devlogs/2025-12-26_status.md\n"
    "  python tools/devlog_poster.py --agent Agent-8 --file agent_workspaces/Agent-8/devlogs/DEVLOG_2025-12-26.md\n"
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    "Note: Tool automatically truncates content >1900 chars for Discord. Full devlog saved in workspace.\n\n"
    "If clarification needed:\n"
    "{fallback}\n"
    "#DISCORD #D2A\n"
)



