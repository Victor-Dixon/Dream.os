#!/usr/bin/env python3
"""
Gas Delivery Stage - Send Gas Messages
======================================

Stage 3: Build and send gas messages to next agent in pipeline.
"""

from datetime import datetime
from typing import Dict, Optional

from ..core.models import PipelineAgent


def build_gas_message(
    agent: PipelineAgent,
    next_agent: PipelineAgent,
    reason: str,
    progress: float
) -> str:
    """
    Build gas message based on reason.

    Args:
        agent: Current agent sending gas
        next_agent: Next agent receiving gas
        reason: Reason for sending gas
        progress: Current progress percentage

    Returns:
        Formatted gas message
    """
    if "75_PERCENT" in reason:
        return f"""⛽ AUTO-GAS PIPELINE: {next_agent.agent_id}!

AUTOMATED HANDOFF (75-80% Detection):
- Agent: {agent.agent_id}
- Progress: {progress:.1f}%
- Repos: {agent.repos_assigned[0]}-{agent.repos_assigned[1]}
- Current repo: #{agent.current_repo}

YOUR MISSION: Repos {next_agent.repos_assigned[0]}-{next_agent.repos_assigned[1]}

PIPELINE STATUS:
✅ {agent.agent_id} is 75-80% complete
✅ Auto-gas system detected progress
✅ You're next in pipeline sequence!

EXECUTE NOW to maintain perpetual motion!

Use: docs/standards/REPO_ANALYSIS_STANDARD_AGENT6.md (90% success method)

This gas was sent AUTOMATICALLY by the pipeline system! 🚀"""

    elif "90_PERCENT" in reason:
        return f"""⛽ AUTO-GAS SAFETY BACKUP: {next_agent.agent_id}!

AUTOMATED SAFETY (90% Detection):
- {agent.agent_id} at 90% completion
- You should be executing by now
- This is redundancy backup gas

If you haven't started: START NOW!
Pipeline continuity depends on it! 🚀"""

    else:  # 100%
        return f"""✅ AUTO-GAS COMPLETION: {next_agent.agent_id}!

AUTOMATED HANDOFF (Mission Complete):
- {agent.agent_id} finished repos {agent.repos_assigned[0]}-{agent.repos_assigned[1]} ✅
- You're next: Repos {next_agent.repos_assigned[0]}-{next_agent.repos_assigned[1]}

{agent.agent_id} ran out of gas - you're fueled and ready!
Execute to keep swarm moving! 🚀"""


def send_gas_message(
    next_agent_id: str,
    message: str,
    sender: str = "AutoGasPipeline",
    priority: str = "urgent"
) -> bool:
    """
    Send gas message via messaging system.

    Args:
        next_agent_id: Recipient agent ID
        message: Message content
        sender: Sender identifier
        priority: Message priority

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        from src.core.messaging_core import send_message, UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority

        msg = UnifiedMessage(
            sender=sender,
            recipient=next_agent_id,
            content=message,
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT if priority == "urgent" else UnifiedMessagePriority.NORMAL
        )
        return send_message(msg)
    except ImportError:
        # Fallback to stub function
        try:
            from src.core.messaging_core import send_message
            # Alias for backward compatibility

            def send_message_to_agent(agent_id: str, message: str, **kwargs):
                """Send message to agent - wrapper for send_message."""
                from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
                msg = UnifiedMessage(
                    sender="System",
                    recipient=agent_id,
                    content=message,
                    message_type=UnifiedMessageType.TEXT,
                    priority=UnifiedMessagePriority.NORMAL
                )
                return send_message(msg)

            return send_message_to_agent(next_agent_id, message, sender=sender, priority=priority)
        except Exception:
            return False
    except Exception as e:
        print(f"❌ Error sending gas message: {e}")
        return False


def mark_gas_sent(agent: PipelineAgent, reason: str) -> None:
    """Mark gas as sent for the given reason."""
    if "75" in reason:
        agent.gas_sent_at_75 = True
    elif "90" in reason:
        agent.gas_sent_at_90 = True
    else:
        agent.gas_sent_at_100 = True

    agent.last_gas_sent = datetime.now().isoformat()
