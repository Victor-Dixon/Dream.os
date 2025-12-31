"""
Agent Status Library
===================

Unified library for reading and monitoring agent status.json files.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes

<!-- SSOT Domain: core -->
"""

from .reader import (
    AgentStatusReader,
    read_agent_status,
    read_all_agent_status,
)
from .cache import StatusCache
from .watcher import StatusFileWatcher, create_watcher
from .aggregator import SwarmStateAggregator, aggregate_swarm_state

__all__ = [
    "AgentStatusReader",
    "read_agent_status",
    "read_all_agent_status",
    "StatusCache",
    "StatusFileWatcher",
    "create_watcher",
    "SwarmStateAggregator",
    "aggregate_swarm_state",
]

