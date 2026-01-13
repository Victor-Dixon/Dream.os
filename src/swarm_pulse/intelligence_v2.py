"""
Intelligence V2 - Agent Cellphone V2
====================================

SSOT Domain: swarm_brain

Refactored swarm intelligence interface using service architecture.

Features:
- Partnership suggestion algorithms
- Intelligent routing and coordination
- Collaboration pattern detection
- Coordination efficiency analysis

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

from typing import Dict, List, Optional

from .intelligence_service import intelligence_service
from .models import PulseEvent

# ============================================================================
# CORE FUNCTIONS - Simplified Interface
# ============================================================================

def suggest_partnerships(
    event: PulseEvent,
    *,
    top_k: int = 3,
    threshold: float = 0.6,
) -> List:
    """
    Suggest bilateral partnerships based on event content.

    Args:
        event: Pulse event to analyze
        top_k: Number of suggestions to return
        threshold: Similarity threshold for suggestions

    Returns:
        List of partnership suggestions
    """
    return intelligence_service.suggest_partnerships(
        event=event,
        top_k=top_k,
        threshold=threshold
    )

def route_with_intelligence(
    event: PulseEvent,
    available_agents: List[str]
) -> List[str]:
    """
    Route events to agents using intelligence-based decisions.

    Args:
        event: Event to route
        available_agents: List of available agent IDs

    Returns:
        Ordered list of agent IDs for routing
    """
    return intelligence_service.route_with_intelligence(
        event=event,
        available_agents=available_agents
    )

def detect_collaboration_patterns(events: List[PulseEvent]) -> List:
    """
    Detect collaboration patterns in pulse events.

    Args:
        events: List of pulse events to analyze

    Returns:
        List of detected collaboration patterns
    """
    return intelligence_service.detect_collaboration_patterns(events=events)

def analyze_coordination_efficiency(agent_id: Optional[str] = None):
    """
    Analyze coordination efficiency for agents.

    Args:
        agent_id: Specific agent to analyze, or None for all

    Returns:
        Coordination metrics
    """
    return intelligence_service.analyze_coordination_efficiency(agent_id=agent_id)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_intelligence_config() -> Dict:
    """
    Get current intelligence configuration.

    Returns:
        Intelligence configuration dictionary
    """
    return intelligence_service.config

def update_intelligence_config(updates: Dict) -> None:
    """
    Update intelligence configuration.

    Args:
        updates: Configuration updates to apply
    """
    intelligence_service.config.update(updates)

def reset_intelligence_cache() -> None:
    """
    Reset any cached intelligence data.
    """
    # Intelligence service doesn't currently have caching,
    # but this provides a hook for future cache management
    pass

# Export all functions for backward compatibility
__all__ = [
    "suggest_partnerships",
    "route_with_intelligence",
    "detect_collaboration_patterns",
    "analyze_coordination_efficiency",
    "get_intelligence_config",
    "update_intelligence_config",
    "reset_intelligence_cache"
]