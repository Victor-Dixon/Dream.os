#!/usr/bin/env python3
"""
Gas Decision Stage - Determine Gas Sending
=========================================

Stage 2: Determine if gas should be sent based on progress and FSM state.
"""

from typing import List
from ..core.models import AgentState, PipelineAgent


def update_fsm_state(agent: PipelineAgent, progress: float) -> None:
    """Update agent's FSM state based on progress."""
    if progress == 0:
        agent.state = AgentState.IDLE
    elif progress < 25:
        agent.state = AgentState.STARTING
    elif progress < 95:
        agent.state = AgentState.EXECUTING
    elif progress < 100:
        agent.state = AgentState.COMPLETING
    else:
        agent.state = AgentState.COMPLETE


def should_send_gas(agent: PipelineAgent, progress: float) -> List[str]:
    """
    Determine if gas should be sent and to whom.

    Returns: List of reasons to send gas
    """
    reasons = []

    # 75-80% mark (primary handoff)
    if 75 <= progress < 80 and not agent.gas_sent_at_75:
        reasons.append("PRIMARY_HANDOFF_75_PERCENT")

    # 90% mark (safety backup)
    if 90 <= progress < 95 and not agent.gas_sent_at_90:
        reasons.append("SAFETY_BACKUP_90_PERCENT")

    # 100% mark (completion)
    if progress >= 100 and not agent.gas_sent_at_100:
        reasons.append("COMPLETION_100_PERCENT")

    return reasons
