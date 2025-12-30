"""
<!-- SSOT Domain: discord -->

Bot Lifecycle Management
========================

Lifecycle management for Discord bot (startup, shutdown, health monitoring).

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from .bot_lifecycle import BotLifecycleManager
from .swarm_snapshot_helpers import get_swarm_snapshot

__all__ = [
    "BotLifecycleManager",
    "get_swarm_snapshot",
]

