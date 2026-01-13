#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Gas Pipeline Models - Data Models
==================================

Data models for gas pipeline system (AgentState, PipelineAgent).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class AgentState(Enum):
    """FSM states for gas pipeline."""
    IDLE = "idle"
    STARTING = "starting"
    EXECUTING = "executing"
    COMPLETING = "completing"
    COMPLETE = "complete"
    OUT_OF_GAS = "out_of_gas"


@dataclass
class PipelineAgent:
    """Agent in the gas pipeline."""
    agent_id: str
    repos_assigned: Tuple[int, int]  # (start, end) e.g. (1, 10)
    next_agent: Optional[str]
    current_repo: int = 0
    state: AgentState = AgentState.IDLE
    last_gas_sent: Optional[str] = None
    gas_sent_at_75: bool = False
    gas_sent_at_90: bool = False
    gas_sent_at_100: bool = False
