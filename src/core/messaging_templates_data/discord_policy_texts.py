"""
Discord reporting policy and D2A helper texts (static).

<!-- SSOT Domain: integration -->
"""

# Discord reporting policy to enforce completion visibility (for S2A/C2A)
DISCORD_REPORTING_TEXT = (
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "DISCORD REPORTING POLICY — CRITICAL VISIBILITY\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "I may not be at the computer. Discord is the primary visibility channel.\n\n"
    "Your completion report MUST be posted to Discord when a task slice finishes.\n\n"
    "When to post:\n"
    "[ ] After completing a slice with a real artifact\n"
    "[ ] After a meaningful commit\n"
    "[ ] After validation/test results\n"
    "[ ] When blocked (post blocker + next step)\n\n"
    "What to include:\n"
    "- Task\n"
    "- Actions Taken\n"
    "- Commit Message (if code touched)\n"
    "- Status (✅ done or 🟡 blocked + next step)\n"
    "- Artifact path(s) if relevant\n\n"
    "Do not send acknowledgment-only messages.\n"
    "The Discord post is the completion handshake.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "HOW TO POST TO DISCORD (EXACT COMMAND)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "**Command:**\n"
    "```bash\n"
    "python tools/devlog_manager.py post --agent {recipient} --file <devlog_file.md>\n"
    "```\n\n"
    "**Steps:**\n"
    "1. Create a markdown file: `devlogs/YYYY-MM-DD_agent-X_topic.md`\n"
    "2. Write your completion report in the file\n"
    "3. Run the command above, replacing:\n"
    "   - `{recipient}` with your agent ID (e.g., Agent-1)\n"
    "   - `<devlog_file.md>` with your file path\n\n"
    "**Example:**\n"
    "```bash\n"
    "# Create devlog file\n"
    "echo '# Task Complete\\n\\nActions: ...' > devlogs/2025-12-08_agent-1_task_complete.md\n"
    "# Post to Discord\n"
    "python tools/devlog_manager.py post --agent Agent-1 --file devlogs/2025-12-08_agent-1_task_complete.md\n"
    "```\n\n"
    "**This may be the ONLY way users see your messages!**\n"
)

# D2A (Discord → Agent) response policy - lightweight and human-first
D2A_RESPONSE_POLICY_TEXT = (
    "Discord Response Policy:\n"
    "- This message originated from Discord.\n"
    "- Reply in Discord with your status/answer when you act on this.\n"
    "- Discord is the visibility channel; status-only or chat-only replies do NOT count.\n"
    "- Include evidence: artifact/validation/delegation. Keep replies short and high-signal.\n"
)

# D2A preferred reply format - compact reminder
D2A_REPORT_FORMAT_TEXT = (
    "Preferred Reply Format (short):\n"
    "- Task\n"
    "- Actions Taken\n"
    "- Commit Message (if code touched)\n"
    "- Status (✅ done or 🟡 blocked + next step)\n"
)



