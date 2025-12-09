#!/usr/bin/env python3
"""
Messaging Models - V2 Compliance Module
=======================================

<!-- SSOT Domain: integration -->

Core messaging models and enums.
Extracted from messaging_core.py (472→<300 lines)

Author: Agent-1 (Integration & Core Systems Specialist) - LAST CRITICAL V2 FIX
Created: 2025-10-11
License: MIT
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class DeliveryMethod(Enum):
    """Delivery methods for messages."""

    PYAUTOGUI = "pyautogui"  # Primary delivery method
    INBOX = "inbox"  # Fallback when PyAutoGUI fails (e.g., Cursor queue full)
    BROADCAST = "broadcast"


class UnifiedMessageType(Enum):
    """Message types for unified messaging."""

    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"
    MULTI_AGENT_REQUEST = "multi_agent_request"  # For response collection


class UnifiedMessagePriority(Enum):
    """Message priorities for unified messaging."""

    REGULAR = "regular"
    URGENT = "urgent"


class MessageCategory(Enum):
    """
    High-level routing categories for messaging templates.

    S2A = System-to-Agent control/ops/cycles (includes Debate system cycles)
    D2A = Discord-to-Agent human/command intake
    C2A = Captain-to-Agent directives
    A2A = Agent-to-Agent coordination
    """

    S2A = "s2a"
    D2A = "d2a"
    C2A = "c2a"
    A2A = "a2a"


class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""

    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "coordination"
    SYSTEM = "system"


class RecipientType(Enum):
    """Recipient types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class SenderType(Enum):
    """Sender types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


@dataclass
class UnifiedMessage:
    """Core message structure for unified messaging."""

    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: list[UnifiedMessageTag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
    category: MessageCategory = MessageCategory.S2A
    sender_type: SenderType = SenderType.SYSTEM
    recipient_type: RecipientType = RecipientType.AGENT


__all__ = [
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "MessageCategory",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "UnifiedMessage",
    "MESSAGE_TEMPLATES",
    "AGENT_OPERATING_CYCLE_TEXT",
    "CYCLE_CHECKLIST_TEXT",
    "DISCORD_REPORTING_TEXT",
    "format_s2a_message",
]

# Canonical operating cycle text for S2A messages.
AGENT_OPERATING_CYCLE_TEXT = (
    "Agent Operating Cycle (canonical):\n"
    "1) Claim\n"
    "2) Sync SSOT/context\n"
    "3) Slice\n"
    "4) Execute\n"
    "5) Validate\n"
    "6) Commit\n"
    "7) Report evidence\n"
)

# Cycle checklist to keep start/during/end behavior explicit
CYCLE_CHECKLIST_TEXT = (
    "Cycle Checklist:\n"
    "CYCLE START:\n"
    "- Check inbox (priority: D2A → C2A → A2A)\n"
    "- Check Contract System (--get-next-task)\n"
    "- Check Swarm Brain (search relevant topics)\n"
    "- Update status.json (status=ACTIVE, increment cycle_count)\n"
    "- Update FSM State\n"
    "- Review current mission\n"
    "DURING CYCLE:\n"
    "- Update status when phase changes\n"
    "- Update when tasks complete\n"
    "- Update if blocked\n"
    "CYCLE END:\n"
    "- Update completed_tasks\n"
    "- Update next_actions\n"
    "- Commit status.json to git\n"
    "- Create & post devlog automatically\n"
    "- Share learnings to Swarm Brain\n"
)

# Discord reporting policy to enforce completion visibility
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

# Template strings for standard headers. Payloads should be formatted by the caller.
MESSAGE_TEMPLATES = {
    # S2A: System-to-Agent (control/ops/cycles)
    MessageCategory.S2A: {
        "CONTROL": (
            "[HEADER] S2A CONTROL\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Context:\n{context}\n\n"
            "Action Required:\n"
            "Produce ONE artifact before next cycle:\n"
            "- Run validator and report results, OR\n"
            "- Commit a small fix with tests passing, OR\n"
            "- Write a 5-bullet technical report.\n\n"
            "No-Reply Policy:\n"
            "- This is a control message. Do not respond unless blocked.\n"
            "- Do not update status.json solely to acknowledge.\n"
            "- Progress resets only on artifacts: commit | test pass | real doc/code delta.\n\n"
            "Priority Behavior:\n"
            "- regular = next cycle; urgent = interrupt current slice.\n\n"
            "{operating_cycle}\n"
            "{cycle_checklist}\n"
            "{discord_reporting}\n"
            "Evidence format:\n"
            "- Command(s) run + outcome OR\n"
            "- Commit hash + tests status OR\n"
            "- Doc name + 3 key findings\n\n"
            "If blocked:\n"
            "- Send 1 message with: blocker + proposed fix + what you need from Captain\n"
        ),
        "STALL_RECOVERY": (
            "[HEADER] S2A STALL RECOVERY — DO NOT REPLY\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Reason:\n{context}\n\n"
            "Required Output (pick one now):\n"
            "- Commit a real slice\n"
            "- Run and record a validation result\n"
            "- Produce a short artifact report with real delta\n\n"
            "No-Reply Policy:\n"
            "- Do not respond to this message.\n"
            "- Chat replies do not count as progress.\n"
            "- status.json-only updates do not count as progress.\n\n"
            "{operating_cycle}\n"
            "{cycle_checklist}\n"
            "{discord_reporting}\n"
            "Escalation:\n{fallback}\n"
            "#STALL-RECOVERY #NO-REPLY #PROGRESS-ONLY #ARTIFACT-REQUIRED\n"
        ),
        "HARD_ONBOARDING": (
            "[HEADER] S2A HARD ONBOARDING\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Context:\n{context}\n\n"
            "First Actions:\n{actions}\n\n"
            "{operating_cycle}\n"
            "If blocked:\n{fallback}\n"
        ),
        "SOFT_ONBOARDING": (
            "[HEADER] S2A SOFT ONBOARDING\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Identity:\n"
            "You are {recipient}. Act as this agent for this message.\n"
            "If you are not {recipient}, do NOT reply; forward to {recipient}.\n\n"
            "No-Ack Policy:\n"
            "- Do not send empty acknowledgments.\n"
            "- Respond with artifact/result or 1 blocker (blocker + proposed fix + owner).\n\n"
            "Context:\n{context}\n\n"
            "Cleanup / Alignment Actions (do one real output):\n{actions}\n\n"
            "Evidence format:\n"
            "- Commit hash + tests status, or\n"
            "- Doc path + 3 key changes, or\n"
            "- Validation command + outcome.\n\n"
            "{operating_cycle}\n"
            "{cycle_checklist}\n"
            "{discord_reporting}\n"
            "If blocked:\n{fallback}\n"
        ),
        "PASSDOWN": (
            "[HEADER] S2A PASSDOWN\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "What changed:\n{context}\n\n"
            "Your next slice:\n{actions}\n\n"
            "{operating_cycle}\n"
            "If blocked:\n{fallback}\n"
        ),
        "TELEPHONE_STATUS_GAME": (
            "[HEADER] S2A TELEPHONE STATUS GAME\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Chain Context:\n{context}\n\n"
            "Your move:\n{actions}\n\n"
            "Rules:\n"
            "- Pass actionable state + next slice.\n"
            "- No acknowledgement-only responses.\n\n"
            "{operating_cycle}\n"
            "If blocked:\n{fallback}\n"
        ),
        "TASK_CYCLE": (
            "[HEADER] S2A TASK CYCLE\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Cycle Objective:\n{context}\n\n"
            "Assigned Slice:\n{actions}\n\n"
            "{operating_cycle}\n"
            "If blocked:\n{fallback}\n"
        ),
        "FSM_UPDATE": (
            "[HEADER] S2A FSM UPDATE\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "State Change:\n{context}\n\n"
            "Required Behavior:\n{actions}\n\n"
            "{operating_cycle}\n"
            "If blocked:\n{fallback}\n"
        ),
        "DEBATE_CYCLE": (
            "[HEADER] S2A DEBATE CYCLE\n"
            "From: {sender}\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "Debate Topic:\n{topic}\n\n"
            "Role/Position:\n{role}\n\n"
            "Context:\n{context}\n\n"
            "Rules:\n{rules}\n\n"
            "Deliverable:\n{deliverable}\n\n"
            "{operating_cycle}\n"
            "If blocked:\n{fallback}\n"
            "#DEBATE #S2A\n"
        ),
        "CYCLE_V2": (
            "[HEADER] C2A CYCLE V2 - MAX PRODUCTIVITY\n"
            "From: Captain Agent-4\n"
            "To: {recipient}\n"
            "Priority: {priority}\n"
            "Message ID: {message_id}\n"
            "Timestamp: {timestamp}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "MISSION\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "{mission}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "DEFINITION OF DONE (DoD)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "{dod}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "CONSTRAINTS\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "SSOT: {ssot_constraint}\n"
            "V2: {v2_constraint}\n"
            "Touch Surface: {touch_surface}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "VALIDATION REQUIRED\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "{validation_required}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "PRIORITY\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "{priority_level}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "HANDOFF EXPECTATION\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "{handoff_expectation}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "AGENT OPERATING CYCLE V2\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "A) Pre-Cycle Rules (Hard Guards):\n"
            "   • WIP = 1 (only one active objective per cycle)\n"
            "   • DoD required (if missing, write 3-line DoD)\n"
            "   • SSOT boundaries first (confirm where truth lives)\n"
            "   • V2 Compliance gate (split if file exceeds limits)\n\n"
            "B) Start of Cycle (Fast):\n"
            "   1. Inbox sweep (max 60 seconds)\n"
            "   2. Claim task: --get-next-task --agent {recipient}\n"
            "   3. Pull last 1 relevant pattern from Swarm Brain\n"
            "   4. Write Micro-Plan (3 bullets max):\n"
            "      - Change target\n"
            "      - Validation method\n"
            "      - Exit criteria\n"
            "   5. Update status.json with phase, mission, micro-plan, DoD\n\n"
            "C) Execution Burst (Timeboxed):\n"
            "   1. Implement smallest viable change toward DoD\n"
            "   2. If scope expands: split into subtask, notify Captain\n"
            "   3. Keep changes localized and typed\n"
            "   4. No refactors unless they reduce immediate risk\n\n"
            "D) Mid-Cycle Checkpoint (Anti-Drift):\n"
            "   After first meaningful change:\n"
            "   • Still aligned with DoD?\n"
            "   • Still within SSOT?\n"
            "   • Still within V2?\n"
            "   If no: adjust plan, report correction\n\n"
            "E) Validation First-Class (Shift Left):\n"
            "   1. Run tests/lint/verification for touched surface\n"
            "   2. If tests missing: add minimal tests\n"
            "   3. Log evidence (command/output summary)\n\n"
            "F) Reporting Contract (No Empty Replies):\n"
            "   Must include:\n"
            "   • What changed (artifact-level)\n"
            "   • Validation evidence\n"
            "   • Measurable result\n"
            "   • Next recommended action\n\n"
            "G) Documentation:\n"
            "   • status.json updated (COMPLETE/BLOCKED/HANDOFF_READY)\n"
            "   • Discord devlog posted for completed actions\n\n"
            "H) Escalation Thresholds:\n"
            "   Escalate when:\n"
            "   • DoD unclear beyond 2 reasonable assumptions\n"
            "   • SSOT conflict detected\n"
            "   • Cross-agent dependency required\n"
            "   • Change affects >2 modules/domains\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "SUCCESS METRICS PER CYCLE\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "• Output: ≥1 merged-ready artifact OR ≥1 validated decision\n"
            "• Validation: evidence included every time\n"
            "• Drift: zero off-mission edits\n"
            "• WIP: never >1\n\n"
            "If blocked:\n{fallback}\n"
            "#CYCLE_V2 #C2A\n"
        ),
    },
    # D2A: Discord-to-Agent
    MessageCategory.D2A: (
        "[HEADER] D2A DISCORD INTAKE\n"
        "From: {sender}\n"
        "To: {recipient}\n"
        "Priority: {priority}\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "Identity:\n"
        "You are {recipient}. Act as this agent for this message.\n"
        "If you are not {recipient}, do NOT reply; forward to {recipient}.\n\n"
        "No-Ack Policy:\n"
        "- Do not send empty acknowledgments.\n"
        "- Respond with action/result or 1 blocker (blocker + proposed fix + owner).\n\n"
        "Reply Channel (MANDATORY):\n"
        "- Use Discord devlog router to reply to users: python tools/devlog_manager.py post --agent {recipient} --file <devlog_file.md>\n"
        "- Do NOT reply here; send user-facing responses through the Discord devlog router.\n\n"
        "{cycle_checklist}\n"
        "{discord_reporting}\n"
        "User Request:\n{content}\n\n"
        "Interpretation:\n{interpretation}\n\n"
        "Proposed Action:\n{actions}\n\n"
        "If clarification needed:\n{fallback}\n"
        "How to respond:\n"
        "- If unclear: ask 1 clarifying question.\n"
        "- If clear: execute and reply with result/evidence.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "AGENT OPERATING CYCLE (MANDATORY)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "1) Claim - Check Contract System (--get-next-task)\n"
        "2) Sync SSOT/context - Review mission, check Swarm Brain\n"
        "3) Slice - Break work into executable pieces\n"
        "4) Execute - Do the work\n"
        "5) Validate - Verify results (tests, checks, evidence)\n"
        "6) Commit - Git commit with evidence\n"
        "7) Report evidence - Post Discord devlog (see below)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "DISCORD DEVLOG POSTING (HOW TO REPLY)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "**This may be the ONLY way users see your messages!**\n\n"
        "**Command:**\n"
        "```bash\n"
        "python tools/devlog_manager.py post --agent {recipient} --file <devlog_file.md>\n"
        "```\n\n"
        "**Steps:**\n"
        "1. Create devlog file: `devlogs/YYYY-MM-DD_agent-X_topic.md`\n"
        "2. Write your response/update in the file\n"
        "3. Post to Discord: `python tools/devlog_manager.py post --agent {recipient} --file devlogs/YYYY-MM-DD_agent-X_topic.md`\n"
        "4. For major updates: Add `--major` flag\n\n"
        "**Example:**\n"
        "```bash\n"
        "# Create devlog\n"
        "echo '# Agent-1 Response\\n\\nWork completed: ...' > devlogs/2025-12-08_agent-1_response.md\n"
        "# Post to Discord\n"
        "python tools/devlog_manager.py post --agent Agent-1 --file devlogs/2025-12-08_agent-1_response.md\n"
        "```\n\n"
        "**Full Documentation:**\n"
        "- `docs/DEVLOG_POSTING_GUIDE.md` - Complete devlog posting guide\n"
        "- `docs/DISCORD_ROUTER_USAGE_INSTRUCTIONS.md` - Discord router usage\n"
        "- `swarm_brain/protocols/CYCLE_PROTOCOLS.md` - Full cycle protocols\n\n"
        "#DISCORD #D2A\n"
    ),
    # C2A: Captain-to-Agent
    MessageCategory.C2A: (
        "[HEADER] C2A CAPTAIN DIRECTIVE\n"
        "From: Captain Agent-4\n"
        "To: {recipient}\n"
        "Priority: {priority}\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "Identity:\n"
        "You are {recipient}. Act as this agent for this directive.\n"
        "If you are not {recipient}, do NOT reply; forward to {recipient}.\n\n"
        "No-Ack Policy:\n"
        "- Do not send empty acknowledgments.\n"
        "- Respond with deliverable/evidence or 1 blocker (blocker + proposed fix + owner).\n\n"
        "{discord_reporting}\n"
        "Cycle Checklist:\n"
        "CYCLE START:\n"
        "- Check inbox (priority: D2A → C2A → A2A)\n"
        "- Check Contract System (--get-next-task)\n"
        "- Check Swarm Brain (search relevant topics)\n"
        "- Update status.json (status=ACTIVE, increment cycle_count)\n"
        "- Update FSM State\n"
        "- Review current mission\n"
        "DURING CYCLE:\n"
        "- Update status when phase changes\n"
        "- Update when tasks complete\n"
        "- Update if blocked\n"
        "CYCLE END:\n"
        "- Update completed_tasks\n"
        "- Update next_actions\n"
        "- Commit status.json to git\n"
        "- Create & post devlog automatically\n"
        "- Share learnings to Swarm Brain\n\n"
        "Task:\n{task}\n\n"
        "Context:\n{context}\n\n"
        "Operating Procedures (standard):\n"
        "- Bilateral Coordination (default)\n"
        "  - Pair with your primary partner agent to complete this directive.\n"
        "  - You own orchestration and final handoff to Captain.\n"
        "- State Scan (before execution)\n"
        "  - Check relevant agent statuses for dependencies/overlap.\n"
        "  - Check project state/SSOT for current truth, active blockers, and recent changes.\n"
        "- Learnings → Swarm Brain\n"
        "  - If you discover a new pattern, fix, or rule, add a short Swarm Brain entry.\n"
        "- Scope guard\n"
        "  - If this touches >2 domains, propose a split + request extra agent assignment.\n"
        "- No chatter\n"
        "  - No receipt message required.\n"
        "  - Only message if blocked or when done with evidence.\n\n"
        "{cycle_checklist}\n"
        "{discord_reporting}\n"
        "Deliverable:\n"
        "1) {deliverable}\n"
        "2) Coordination outputs / pings / handoffs\n"
        "3) Short status note (3 bullets max)\n\n"
        "Checkpoint:\n"
        "- {eta}\n\n"
        "Evidence format:\n"
        "- Artifact link/ID + last updated timestamp\n"
        "- Pings/handoffs with message IDs/channel refs\n"
        "- 3-bullet status\n\n"
        "Priority Behavior:\n"
        "- regular = next cycle\n"
        "- urgent = interrupt current slice if safe; otherwise finish current micro-task then switch\n\n"
        "If blocked:\n"
        "- Send 1 message with: blocker + proposed fix + what you need from Captain.\n"
        "How to respond:\n"
        "- When done: provide deliverable + evidence.\n"
    ),
    # A2A: Agent-to-Agent
    MessageCategory.A2A: (
        "[HEADER] A2A COORDINATION\n"
        "From: {sender}\n"
        "To: {recipient}\n"
        "Priority: {priority}\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "Identity:\n"
        "You are {recipient}. Act as this agent for this message.\n"
        "If you are not {recipient}, do NOT reply; forward to {recipient}.\n\n"
        "No-Ack Policy:\n"
        "- Do not send empty acknowledgments.\n"
        "- Respond with action/result or 1 blocker (blocker + proposed fix + owner).\n\n"
        "Cycle Checklist:\n"
        "CYCLE START:\n"
        "- Check inbox (priority: D2A → C2A → A2A)\n"
        "- Check Contract System (--get-next-task)\n"
        "- Check Swarm Brain (search relevant topics)\n"
        "- Update status.json (status=ACTIVE, increment cycle_count)\n"
        "- Update FSM State\n"
        "- Review current mission\n"
        "DURING CYCLE:\n"
        "- Update status when phase changes\n"
        "- Update when tasks complete\n"
        "- Update if blocked\n"
        "CYCLE END:\n"
        "- Update completed_tasks\n"
        "- Update next_actions\n"
        "- Commit status.json to git\n"
        "- Create & post devlog automatically\n"
        "- Share learnings to Swarm Brain\n\n"
        "Ask/Offer:\n{ask}\n\n"
        "Context:\n{context}\n\n"
        "Next Step:\n{next_step}\n\n"
        "If blocked:\n{fallback}\n"
        "How to respond:\n"
        "- Accept + ETA, or propose alternative.\n"
        "- Call out risks/dependencies; confirm next step when done.\n"
    ),
}


def format_s2a_message(template_key: str, **kwargs) -> str:
    """Helper to render an S2A template with operating cycle included."""
    templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
    template = templates.get(template_key) or templates.get("CONTROL")
    kwargs.setdefault("operating_cycle", AGENT_OPERATING_CYCLE_TEXT)
    kwargs.setdefault("cycle_checklist", CYCLE_CHECKLIST_TEXT)
    kwargs.setdefault("discord_reporting", DISCORD_REPORTING_TEXT)
    return template.format(**kwargs)
