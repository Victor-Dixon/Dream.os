"""
Snapshot Aggregator for Cycle Snapshot System
============================================

Aggregates all collected data into unified snapshot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: tools -->
"""

import logging
from datetime import datetime
from typing import Dict, Any

from ..core.snapshot_models import ProjectState

logger = logging.getLogger(__name__)


def aggregate_snapshot(all_data: Dict[str, Dict], cycle_num: int = 1) -> Dict[str, Any]:
    """
    Aggregate all collected data into unified snapshot.

    Args:
        all_data: Dict containing all collected data sources

    Returns:
        Unified snapshot dictionary
    """
    snapshot_metadata = generate_snapshot_metadata(cycle_num)

    project_state = generate_project_state(all_data.get("metrics", {}))

    # Build the complete snapshot
    snapshot = {
        "snapshot_metadata": snapshot_metadata,
        "project_state": project_state,
        "agent_status": all_data.get("agent_status", {}),
        "task_metrics": all_data.get("task_metrics", {}),
        "git_activity": all_data.get("git_activity", {}),
        "mcp_data": all_data.get("mcp_data", {}),
        "collected_at": datetime.now().isoformat()
    }

    return snapshot


def generate_snapshot_metadata(cycle_num: int) -> Dict[str, Any]:
    """
    Generate metadata for the snapshot.

    Args:
        cycle_num: Current cycle number

    Returns:
        Snapshot metadata dictionary
    """
    return {
        "cycle_number": cycle_num,
        "snapshot_version": "0.1.0",
        "generated_at": datetime.now().isoformat(),
        "system": "Cycle Snapshot System",
        "purpose": "Central nervous system data collection for swarm coordination"
    }


def generate_project_state(metrics: Dict) -> ProjectState:
    """
    Generate project state summary from metrics.

    Args:
        metrics: Combined metrics from all data sources

    Returns:
        Project state summary
    """
    # Extract key metrics
    agent_status = metrics.get("agent_status", {})
    task_metrics = metrics.get("task_metrics", {})
    git_metrics = metrics.get("git_metrics", {})

    # Calculate project health indicators
    active_agents = sum(1 for status in agent_status.values()
                       if isinstance(status, dict) and status.get("status") in ["ACTIVE_AGENT_MODE", "active"])

    task_completion_rate = task_metrics.get("completion_rate", 0)
    commits_per_day = git_metrics.get("commits_per_day", 0)

    # Determine project health
    if task_completion_rate > 80 and active_agents >= 6:
        health = "excellent"
    elif task_completion_rate > 60 and active_agents >= 4:
        health = "good"
    elif task_completion_rate > 40 or active_agents >= 2:
        health = "fair"
    else:
        health = "needs_attention"

    return ProjectState(
        active_agents=active_agents,
        total_agents=8,
        task_completion_rate=task_completion_rate,
        commits_per_day=commits_per_day,
        project_health=health,
        cycle_velocity=calculate_velocity_indicator(task_metrics, git_metrics)
    )


def calculate_velocity_indicator(task_metrics: Dict, git_metrics: Dict) -> str:
    """
    Calculate a simple velocity indicator.

    Args:
        task_metrics: Task-related metrics
        git_metrics: Git-related metrics

    Returns:
        Velocity indicator string
    """
    completion_rate = task_metrics.get("completion_rate", 0)
    commits_per_day = git_metrics.get("commits_per_day", 0)

    # Simple velocity calculation
    velocity_score = (completion_rate * 0.6) + (min(commits_per_day * 10, 40) * 0.4)

    if velocity_score > 70:
        return "high"
    elif velocity_score > 40:
        return "medium"
    else:
        return "low"
