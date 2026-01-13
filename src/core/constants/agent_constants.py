#!/usr/bin/env python3
"""
Agent Constants - SSOT for Agent Identifiers
============================================

Provides single source of truth for agent identifiers and roles.
Consolidates duplicate agent list definitions across codebase.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

# All agents in the swarm (ALL possible agents)
# NOTE: Use get_active_agents() from agent_mode_manager for mode-aware active agents
AGENT_LIST = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]

# Agent IDs as tuple for immutability
AGENT_IDS = tuple(AGENT_LIST)

# Agent count (ALL agents)
# NOTE: Use len(get_active_agents()) for mode-aware count
AGENT_COUNT = len(AGENT_LIST)

# Agent roles mapping
AGENT_ROLES = {
    "Agent-1": "Integration & Core Systems",
    "Agent-2": "Architecture & Design",
    "Agent-3": "Infrastructure & DevOps",
    "Agent-4": "Captain (Strategic Oversight)",
    "Agent-5": "Business Intelligence",
    "Agent-6": "Coordination & Communication",
    "Agent-7": "Web Development",
    "Agent-8": "SSOT & System Integration",
}

# Agent coordinates (for PyAutoGUI operations)
AGENT_COORDINATES = {
    "Agent-1": (-1269, 481),
    "Agent-2": (-308, 480),
    "Agent-3": (-1269, 1001),
    "Agent-5": (652, 421),
    "Agent-6": (1612, 469),
    "Agent-7": (653, 940),
    "Agent-8": (1611, 941),
    "Agent-4": (-308, 1000),  # Captain always last
}

# Agent processing order (for bulk operations - DEFAULT 8-agent order)
# NOTE: Use get_processing_order() from agent_mode_manager for mode-aware order
AGENT_PROCESSING_ORDER = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
    "Agent-4",  # Captain always last
]


def get_agent_role(agent_id: str) -> str:
    """Get role for agent ID."""
    return AGENT_ROLES.get(agent_id, "Unknown")


def get_agent_coordinates(agent_id: str) -> tuple[int, int] | None:
    """Get coordinates for agent ID."""
    return AGENT_COORDINATES.get(agent_id)


def is_valid_agent(agent_id: str) -> bool:
    """Check if agent ID is valid."""
    return agent_id in AGENT_LIST


__all__ = [
    "AGENT_LIST",
    "AGENT_IDS",
    "AGENT_COUNT",
    "AGENT_ROLES",
    "AGENT_COORDINATES",
    "AGENT_PROCESSING_ORDER",
    "get_agent_role",
    "get_agent_coordinates",
    "is_valid_agent",
]


