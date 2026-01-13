"""
A2A (Agent ↔ Agent) coordination template string.

<!-- SSOT Domain: integration -->
"""

A2A_TEMPLATE = (
    "[HEADER] A2A COORDINATION — BILATERAL SWARM COORDINATION\n"
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
    "🐝 **COORDINATED SWARM REQUEST**:\n"
    "This is a bilateral coordination request to leverage swarm force multiplication.\n"
    "We're asking for your expertise to parallelize work and accelerate completion.\n\n"
    "**COORDINATION REQUEST**:\n{ask}\n\n"
    "**CONTEXT**:\n{context}\n\n"
    "**WHY THIS COORDINATION?**\n{coordination_rationale}\n\n"
    "**EXPECTED CONTRIBUTION**:\n{expected_contribution}\n\n"
    "**TIMING**:\n{coordination_timeline}\n\n"
    "**RESPONSE REQUIRED**:\n"
    "Reply within 30 minutes with acceptance/decline and proposed approach.\n\n"
    "**WHAT TO INCLUDE IN YOUR REPLY** (for ACCEPT responses):\n"
    "- **Proposed approach**: How you'll coordinate (your role + partner's role)\n"
    "- **Synergy identification**: How your capabilities complement your partner's\n"
    "- **Next steps**: Suggested initial coordination touchpoint or action item\n"
    "- **Relevant capabilities**: Brief list of your applicable skills\n"
    "- **Timeline**: When you can start and expected coordination sync time\n\n"
    "**REPLY FORMAT (MANDATORY)**:\n"
    "```\n"
    "A2A REPLY to {message_id}:\n"
    "✅ ACCEPT: [Proposed approach: your role + partner role. Synergy: how capabilities complement. Next steps: initial action. Capabilities: key skills. Timeline: start time + sync time] | ETA: [timeframe]\n"
    "OR\n"
    "❌ DECLINE: [reason] | Alternative: [suggested agent]\n"
    "```\n\n"
    "**REPLY COMMAND**:\n"
    "```bash\n"
    "python -m src.services.messaging_cli --agent {sender} \\\n"
    "  --message \"A2A REPLY to {message_id}: [your response]\" \\\n"
    "  --category a2a --sender Agent-X --tags coordination-reply\n"
    "```\n"
    "**IMPORTANT SENDER IDENTIFICATION**: \n"
    "- `--agent {sender}` = recipient (who you're replying to, shown above as 'From: {sender}')\n"
    "- `--sender Agent-X` = **YOU** (replace X with your agent number, e.g., `Agent-2` or `Agent-5`)\n"
    "- Always include `--sender Agent-X` so your response header shows your agent ID instead of defaulting to CAPTAIN\n\n"
    "**COORDINATION PRINCIPLES**:\n"
    "- 2 agents working in parallel > 1 agent working alone\n"
    "- Share context via status.json updates and A2A pings\n"
    "- Report progress to accelerate integration\n"
    "- **Be proactive**: Propose concrete next steps rather than 'standing by'\n"
    "- **Identify synergy**: Explain how your skills complement your partner's\n"
    "- **Suggest handoffs**: Propose coordination touchpoints or integration points\n\n"
    "**IMPORTANT**: **Push directives forward**: Don't just acknowledge repeat messages—use them to power more work or suggest new tasks back instead of reiterating the same thing. If you receive a message that's essentially repeating previous coordination, use it as fuel to execute work or propose the next task rather than just confirming again.\n\n"
    "**DIRECTIVE PUSH PRINCIPLE**: When receiving messages (especially repeat/reminder messages), push directives forward—don't just respond. Use the message energy to execute more work or suggest a new task back instead of reiterating the same acknowledgment. Transform message receipt into action or task proposal.\n\n"
    "If blocked: Send brief blocker description + proposed solution\n"
    "**PUSH DIRECTIVES, DON'T REPEAT**: When you receive a message that repeats previous coordination or asks for status you've already provided, don't just reiterate—use it as momentum to:\n"
    "- Execute the next logical work step immediately\n"
    "- Propose a new task or next action back to the sender\n"
    "- Suggest a concrete follow-up task that advances the coordination\n"
    "- Take initiative to unblock yourself or others\n"
    "Messages are fuel for action, not just confirmation loops. Turn repeat messages into forward progress.\n\n"
    "#A2A #BILATERAL-COORDINATION #SWARM-FORCE-MULTIPLIER\n"
)



