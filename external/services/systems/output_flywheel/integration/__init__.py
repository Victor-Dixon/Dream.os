"""
Output Flywheel Integration Module
==================================

Provides integration hooks for agents to automatically generate artifacts
from work sessions.
"""

from systems.output_flywheel.integration.agent_session_hooks import (
    AgentSessionHook,
    end_of_session_hook,
)

__all__ = ["AgentSessionHook", "end_of_session_hook"]

