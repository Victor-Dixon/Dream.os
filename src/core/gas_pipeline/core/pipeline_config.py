#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Pipeline Configuration - Pipeline Setup
=======================================

Configuration and setup for gas pipeline system.
"""

from typing import Dict, Tuple, Optional
from ..core.models import PipelineAgent


def get_default_pipeline_config() -> list[tuple[str, Tuple[int, int], Optional[str]]]:
    """
    Get default pipeline configuration.

    Returns:
        List of (agent_id, repos_assigned, next_agent) tuples
    """
    return [
        ("Agent-1", (1, 10), "Agent-2"),
        ("Agent-2", (11, 20), "Agent-3"),
        ("Agent-3", (21, 30), "Agent-5"),
        ("Agent-5", (31, 40), "Agent-6"),
        ("Agent-6", (41, 50), "Agent-7"),
        ("Agent-7", (51, 60), "Agent-8"),
        ("Agent-8", (61, 70), "Agent-4"),
        ("Agent-4", (71, 75), None),  # Mission complete
    ]


def setup_pipeline_agents(
    config: list[tuple[str, Tuple[int, int], Optional[str]]]
) -> Dict[str, PipelineAgent]:
    """
    Initialize pipeline with agent assignments.

    Args:
        config: Pipeline configuration

    Returns:
        Dictionary of agent_id -> PipelineAgent
    """
    agents: Dict[str, PipelineAgent] = {}

    for agent_id, repos, next_agent in config:
        agents[agent_id] = PipelineAgent(
            agent_id=agent_id,
            repos_assigned=repos,
            next_agent=next_agent
        )

    return agents
