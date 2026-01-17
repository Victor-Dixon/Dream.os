"""
Agent Status Module - Unified Status Reading API
===============================================

<!-- SSOT Domain: core -->

This module provides a unified API for all agent status operations.
Instead of using 4 separate implementations, use the UnifiedStatusReader.

Usage:
    from src.core.agent_status import UnifiedStatusReader

    # Basic usage
    reader = UnifiedStatusReader()
    status = reader.get_agent_status("Agent-1")
    all_statuses = reader.get_all_agent_statuses()
    swarm_state = reader.get_swarm_state()

    # With watching
    reader.watch_status_changes(my_callback)
    reader.start_watching()

Legacy implementations are still available but deprecated:
- StatusFileWatcher -> UnifiedStatusReader
- StatusCache -> UnifiedStatusReader
- AgentStatusReader -> UnifiedStatusReader
- SwarmStateAggregator -> UnifiedStatusReader
"""

from .unified_status_reader import (
    UnifiedStatusReader,
    get_agent_status,
    get_all_agent_statuses,
    get_swarm_state
)

# Legacy imports for backward compatibility (deprecated)
from .watcher import StatusFileWatcher
from .cache import StatusCache
from .reader import AgentStatusReader, read_all_agent_status
from .aggregator import SwarmStateAggregator

__all__ = [
    # New unified API (recommended)
    "UnifiedStatusReader",
    "get_agent_status",
    "get_all_agent_statuses",
    "get_swarm_state",

    # Legacy implementations (deprecated)
    "StatusFileWatcher",
    "StatusCache",
    "AgentStatusReader",
    "SwarmStateAggregator",
    "read_all_agent_status"
]