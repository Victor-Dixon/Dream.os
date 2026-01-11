#!/usr/bin/env python3
"""
Message Templates - Comprehensive Template System
===============================================

Complete message templates for all swarm communication scenarios.
Preserves all formatting and protocols from the old system.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class MessageTemplates:
    """Comprehensive message template system for Messaging V3."""

    # ============================================================================
    # A2A (Agent-to-Agent) COORDINATION TEMPLATES
    # ============================================================================

    A2A_COORDINATION_TEMPLATE = (
        "[HEADER] A2A COORDINATION — BILATERAL SWARM COORDINATION\n"
        "From: {sender}\n"
        "To: {recipient}\n"
        "Priority: {priority}\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "🚀 **PROTOCOL UPDATE: Swarm Coordination**\n"
        "{coordination_type} request for parallel processing acceleration.\n\n"
        "🐝 **COORDINATED SWARM REQUEST**:\n"
        "This is a bilateral coordination request to leverage swarm force multiplication.\n"
        "We're asking for your expertise to parallelize work and accelerate completion.\n\n"
        "**COORDINATION REQUEST**:\n{content}\n\n"
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
        "python messaging_v3/cli.py --agent {sender} \\\n"
        "  --message \"A2A REPLY to {message_id}: [your response]\" \\\n"
        "  --category a2a --sender {recipient}\n"
        "```\n"
        "**IMPORTANT SENDER IDENTIFICATION**: \n"
        "- `--agent {sender}` = recipient (who you're replying to)\n"
        "- `--sender {recipient}` = **YOU** (replace with your agent number)\n\n"
        "**COORDINATION PRINCIPLES**:\n"
        "- 2 agents working in parallel > 1 agent working alone\n"
        "- Share context via status updates and A2A pings\n"
        "- Report progress to accelerate integration\n"
        "- Be proactive: Propose concrete next steps rather than 'standing by'\n"
        "- Identify synergy: Explain how your skills complement your partner's\n\n"
        "**PUSH DIRECTIVES, DON'T REPEAT**: When you receive a message that repeats previous coordination or asks for status you've already provided, don't just reiterate—use it as momentum to:\n"
        "- Execute the next logical work step immediately\n"
        "- Propose a new task or next action back to the sender\n"
        "- Suggest a concrete follow-up task that advances the coordination\n"
        "- Take initiative to unblock yourself or others\n"
        "Messages are fuel for action, not just confirmation loops. Turn repeat messages into forward progress.\n\n"
        "#{coordination_hashtag} #SWARM-FORCE-MULTIPLIER\n"
    )

    # ============================================================================
    # S2A (System-to-Agent) ONBOARDING TEMPLATES
    # ============================================================================

    SOFT_ONBOARDING_TEMPLATE = (
        "[HEADER] S2A ONBOARDING (SOFT)\n"
        "From: {sender}\n"
        "To: {recipient}\n"
        "Priority: regular\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "🌟 **Welcome to the Swarm, {recipient}!**\n\n"
        "You have been successfully onboarded to the Agent Cellphone V2 system.\n\n"
        "**Your Role & Capabilities**:\n"
        "- Agent ID: {recipient}\n"
        "- Status: ACTIVE\n"
        "- Messaging: ENABLED\n"
        "- Coordination: AVAILABLE\n\n"
        "**Getting Started**:\n"
        "1. You can now receive and send messages to other agents\n"
        "2. Use A2A coordination for collaborative tasks\n"
        "3. Check your inbox regularly for coordination requests\n"
        "4. Update your status to coordinate with the swarm\n\n"
        "**Communication Channels**:\n"
        "- Direct messaging: `python messaging_v3/cli.py --agent [target] --message [content]`\n"
        "- A2A coordination: Use the coordination templates\n"
        "- Broadcast: System-wide announcements\n\n"
        "**Coordination Protocol**:\n"
        "When you receive coordination requests, respond promptly with:\n"
        "```\n"
        "✅ ACCEPT: [your approach and timeline]\n"
        "❌ DECLINE: [reason and alternative]\n"
        "```\n\n"
        "**System Features**:\n"
        "- Clean Messaging V3: No legacy conflicts\n"
        "- PyAutoGUI Delivery: Visual coordinate-based messaging\n"
        "- Queue Processing: Background message handling\n"
        "- Swarm Coordination: Bilateral coordination protocols\n\n"
        "Welcome to the swarm! 🐝⚡️\n\n"
        "#ONBOARDING #SOFT #WELCOME\n"
    )

    HARD_ONBOARDING_TEMPLATE = (
        "[HEADER] S2A ONBOARDING (HARD)\n"
        "From: {sender}\n"
        "To: {recipient}\n"
        "Priority: urgent\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "🚀 **CRITICAL SYSTEMS ONBOARDING - {recipient}**\n\n"
        "**SYSTEM STATUS: FULLY OPERATIONAL**\n"
        "You are now integrated into the Agent Cellphone V2 swarm intelligence system.\n\n"
        "**SYSTEM ARCHITECTURE**:\n"
        "- Messaging V3: Clean rebuild with PyAutoGUI delivery\n"
        "- Queue System: Persistent message queuing\n"
        "- Coordination Protocol: A2A bilateral swarm coordination\n"
        "- Status Integration: Real-time agent status tracking\n\n"
        "**YOUR CAPABILITIES**:\n"
        "✅ Message reception and transmission\n"
        "✅ A2A coordination protocol execution\n"
        "✅ Status reporting and updates\n"
        "✅ Task coordination and delegation\n"
        "✅ Error handling and recovery\n\n"
        "**IMMEDIATE ACTION REQUIRED**:\n"
        "1. Confirm system integration: Reply with \"HARD ONBOARDING CONFIRMED\"\n"
        "2. Update your status: Coordinate with swarm for initial task assignment\n"
        "3. Begin coordination: Look for A2A coordination requests\n"
        "4. Report readiness: Update swarm with your current capabilities\n\n"
        "**COORDINATION COMMAND**:\n"
        "```bash\n"
        "python messaging_v3/cli.py --agent {sender} --message \"HARD ONBOARDING CONFIRMED: {recipient} ready for coordination\" --category c2a --sender {recipient}\n"
        "```\n\n"
        "**SYSTEM FEATURES**:\n"
        "- Clean Messaging V3: No legacy conflicts\n"
        "- PyAutoGUI Delivery: Visual coordinate-based messaging\n"
        "- Queue Processing: Background message handling\n"
        "- Agent Integration API: Seamless messaging\n"
        "- Feature Integration: All old system capabilities preserved\n\n"
        "**CRITICAL REMINDER**:\n"
        "This is a hard onboarding. Full system integration required.\n"
        "Respond immediately to confirm operational status.\n\n"
        "Welcome to the fully operational swarm! 🐝⚡️🔥\n\n"
        "#ONBOARDING #HARD #SYSTEM-INTEGRATION\n"
    )

    # ============================================================================
    # BROADCAST TEMPLATES
    # ============================================================================

    BROADCAST_TEMPLATE = (
        "[HEADER] BROADCAST MESSAGE\n"
        "From: {sender}\n"
        "To: ALL AGENTS\n"
        "Priority: {priority}\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "📢 **BROADCAST ANNOUNCEMENT**\n\n"
        "{content}\n\n"
        "---\n"
        "*Broadcast delivered via Unified Messaging V3*\n"
    )

    # ============================================================================
    # SURVEY COORDINATION TEMPLATES
    # ============================================================================

    SURVEY_COORDINATION_TEMPLATE = (
        "[HEADER] SURVEY COORDINATION\n"
        "From: {sender}\n"
        "To: ALL AGENTS\n"
        "Priority: high\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "📊 **SURVEY COORDINATION INITIATED**\n\n"
        "**Survey Topic**: {survey_topic}\n\n"
        "**Required Response**: All agents must report current status\n\n"
        "**Response Format**:\n"
        "```\n"
        "SURVEY RESPONSE:\n"
        "Agent: [Your Agent ID]\n"
        "Status: [ACTIVE/BUSY/MAINTENANCE]\n"
        "Capabilities: [List your key capabilities]\n"
        "Current Task: [What you're working on]\n"
        "Readiness: [HIGH/MEDIUM/LOW]\n"
        "```\n\n"
        "**Response Command**:\n"
        "```bash\n"
        "python messaging_v3/cli.py --agent {sender} --message \"SURVEY RESPONSE: Agent: [your_id] Status: ACTIVE Capabilities: [list] Current Task: [task] Readiness: HIGH\" --category survey --sender [your_agent_id]\n"
        "```\n\n"
        "**Timeline**: Respond within {response_timeframe}\n"
        "**Coordination**: Survey results will determine swarm task assignments\n\n"
        "#SURVEY #COORDINATION #STATUS-ASSESSMENT\n"
    )

    # ============================================================================
    # CONSOLIDATION COORDINATION TEMPLATES
    # ============================================================================

    CONSOLIDATION_COORDINATION_TEMPLATE = (
        "[HEADER] CONSOLIDATION COORDINATION\n"
        "From: {sender}\n"
        "To: ALL AGENTS\n"
        "Priority: urgent\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "🔄 **CONSOLIDATION COORDINATION - BATCH {batch_id}**\n\n"
        "**Consolidation Status**: {consolidation_status}\n\n"
        "**Required Action**: All agents coordinate on consolidation tasks\n\n"
        "**Consolidation Tasks**:\n"
        "1. Code consolidation and deduplication\n"
        "2. Documentation updates and synchronization\n"
        "3. Dependency cleanup and optimization\n"
        "4. Testing and validation coordination\n\n"
        "**Response Required**:\n"
        "```\n"
        "CONSOLIDATION UPDATE:\n"
        "Agent: [Your ID]\n"
        "Task: [Your consolidation task]\n"
        "Status: [IN PROGRESS/COMPLETE/BLOCKED]\n"
        "Blocker: [If blocked, describe issue]\n"
        "ETA: [Time to completion]\n"
        "```\n\n"
        "**Coordination Command**:\n"
        "```bash\n"
        "python messaging_v3/cli.py --agent {sender} --message \"CONSOLIDATION UPDATE: Agent: [your_id] Task: [task] Status: IN PROGRESS ETA: 30min\" --category consolidation --sender [your_agent_id]\n"
        "```\n\n"
        "**Timeline**: Complete within {completion_timeframe}\n"
        "**Priority**: URGENT - System optimization required\n\n"
        "#CONSOLIDATION #COORDINATION #SYSTEM-OPTIMIZATION\n"
    )

    # ============================================================================
    # CONTROL MESSAGE TEMPLATES
    # ============================================================================

    CONTROL_MESSAGE_TEMPLATE = (
        "[HEADER] S2A CONTROL\n"
        "From: {sender}\n"
        "To: {recipient}\n"
        "Priority: {priority}\n"
        "Message ID: {message_id}\n"
        "Timestamp: {timestamp}\n\n"
        "🚀 **PROTOCOL UPDATE: Real Work Discovery**\n"
        "When you receive control messages, execute concrete work immediately.\n\n"
        "**Context**:\n{context}\n\n"
        "**Architecture & Swarm Brain Check** (BEFORE DOING ANYTHING):\n"
        "- Search existing architecture / SSOT docs for this domain\n"
        "- Search Swarm Brain for prior decisions and protocols\n"
        "- Prefer reusing/extending existing artifacts over creating new ones\n\n"
        "**Action Required**:\n"
        "Produce ONE artifact before next cycle:\n"
        "- Run validator and report results, OR\n"
        "- Commit a small fix with tests passing, OR\n"
        "- Write a 5-bullet technical report.\n\n"
        "**No-Reply Policy**:\n"
        "- This is a control message. Do not respond unless blocked.\n"
        "- Do not update status.json solely to acknowledge.\n"
        "- Progress resets only on artifacts: commit | test pass | real doc/code delta.\n\n"
        "**Priority Behavior**:\n"
        "- regular = next cycle; urgent = interrupt current slice.\n\n"
        "**Operating Cycle**:\n{operating_cycle}\n\n"
        "**Cycle Checklist**:\n{cycle_checklist}\n\n"
        "**Swarm Coordination**:\n{swarm_coordination}\n\n"
        "**Discord Reporting**:\n{discord_reporting}\n\n"
        "**Evidence Format**:\n"
        "- Command(s) run + outcome OR\n"
        "- Commit hash + tests status OR\n"
        "- Doc name + 3 key findings\n\n"
        "**If Blocked**:\n"
        "- Assess if task needs swarm coordination\n"
        "- State specific blocker and proposed solution\n"
        "- Suggest alternative approaches\n\n"
        "#CONTROL #EXECUTION #ARTIFACT-REQUIRED\n"
    )

    # ============================================================================
    # TEMPLATE RENDERING METHODS
    # ============================================================================

    @classmethod
    def render_a2a_coordination(
        cls,
        sender: str,
        recipient: str,
        content: str,
        coordination_type: str = "BILATERAL SWARM COORDINATION",
        coordination_rationale: str = "To leverage parallel processing and accelerate completion",
        expected_contribution: str = "Domain expertise and parallel execution",
        coordination_timeline: str = "ASAP - coordination needed to maintain momentum",
        priority: str = "regular"
    ) -> str:
        """Render A2A coordination message."""
        return cls.A2A_COORDINATION_TEMPLATE.format(
            sender=sender,
            recipient=recipient,
            priority=priority,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            coordination_type=coordination_type,
            content=content,
            coordination_rationale=coordination_rationale,
            expected_contribution=expected_contribution,
            coordination_timeline=coordination_timeline,
            coordination_hashtag=coordination_type.replace(' ', '-').upper()
        )

    @classmethod
    def render_soft_onboarding(cls, sender: str, recipient: str) -> str:
        """Render soft onboarding message."""
        return cls.SOFT_ONBOARDING_TEMPLATE.format(
            sender=sender,
            recipient=recipient,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        )

    @classmethod
    def render_hard_onboarding(cls, sender: str, recipient: str) -> str:
        """Render hard onboarding message."""
        return cls.HARD_ONBOARDING_TEMPLATE.format(
            sender=sender,
            recipient=recipient,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        )

    @classmethod
    def render_broadcast(cls, sender: str, content: str, priority: str = "normal") -> str:
        """Render broadcast message."""
        return cls.BROADCAST_TEMPLATE.format(
            sender=sender,
            priority=priority,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            content=content
        )

    @classmethod
    def render_survey_coordination(
        cls,
        sender: str,
        survey_topic: str = "Agent Status and Capabilities Assessment",
        response_timeframe: str = "15 minutes"
    ) -> str:
        """Render survey coordination message."""
        return cls.SURVEY_COORDINATION_TEMPLATE.format(
            sender=sender,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            survey_topic=survey_topic,
            response_timeframe=response_timeframe
        )

    @classmethod
    def render_consolidation_coordination(
        cls,
        sender: str,
        batch_id: str = "DEFAULT",
        consolidation_status: str = "INITIATED",
        completion_timeframe: str = "2 hours"
    ) -> str:
        """Render consolidation coordination message."""
        return cls.CONSOLIDATION_COORDINATION_TEMPLATE.format(
            sender=sender,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            batch_id=batch_id,
            consolidation_status=consolidation_status,
            completion_timeframe=completion_timeframe
        )

    @classmethod
    def render_control_message(
        cls,
        sender: str,
        recipient: str,
        context: str,
        operating_cycle: str = "Standard operating cycle",
        cycle_checklist: str = "Execute assigned tasks, update status, coordinate as needed",
        swarm_coordination: str = "Coordinate with swarm for multi-agent tasks",
        discord_reporting: str = "Report progress to Discord channels",
        priority: str = "regular"
    ) -> str:
        """Render control message."""
        return cls.CONTROL_MESSAGE_TEMPLATE.format(
            sender=sender,
            recipient=recipient,
            priority=priority,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            context=context,
            operating_cycle=operating_cycle,
            cycle_checklist=cycle_checklist,
            swarm_coordination=swarm_coordination,
            discord_reporting=discord_reporting
        )


# ============================================================================
# TEMPLATE REGISTRY FOR EASY ACCESS
# ============================================================================

TEMPLATE_REGISTRY = {
    # A2A Coordination
    "a2a_coordination": MessageTemplates.render_a2a_coordination,

    # Onboarding
    "soft_onboarding": MessageTemplates.render_soft_onboarding,
    "hard_onboarding": MessageTemplates.render_hard_onboarding,

    # Broadcast
    "broadcast": MessageTemplates.render_broadcast,

    # Coordination
    "survey_coordination": MessageTemplates.render_survey_coordination,
    "consolidation_coordination": MessageTemplates.render_consolidation_coordination,

    # Control
    "control_message": MessageTemplates.render_control_message,
}


def get_template(template_name: str, **kwargs) -> str:
    """
    Get a rendered template by name.

    Args:
        template_name: Name of the template to render
        **kwargs: Template-specific parameters

    Returns:
        str: Rendered template content

    Example:
        >>> content = get_template("a2a_coordination", sender="Agent-7", recipient="Agent-6", content="Let's coordinate!")
    """
    if template_name not in TEMPLATE_REGISTRY:
        raise ValueError(f"Unknown template: {template_name}")

    template_func = TEMPLATE_REGISTRY[template_name]
    return template_func(**kwargs)