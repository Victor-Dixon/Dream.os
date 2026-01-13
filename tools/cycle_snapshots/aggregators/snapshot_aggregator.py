"""
Snapshot Aggregator
===================

Aggregates all collected data into unified snapshot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: tools -->
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from ..core.snapshot_models import (
    SnapshotMetadata,
    AgentAccomplishments,
    ProjectMetrics,
    CycleSnapshot,
)

logger = logging.getLogger(__name__)


def generate_snapshot_metadata(
    cycle_num: int,
    workspace_root: Optional[Path] = None,
    previous_cycle: Optional[int] = None,
    previous_timestamp: Optional[datetime] = None
) -> SnapshotMetadata:
    """
    Generate snapshot metadata.
    
    Args:
        cycle_num: Current cycle number
        workspace_root: Root workspace path
        previous_cycle: Previous cycle number (optional)
        previous_timestamp: Previous snapshot timestamp (optional)
    
    Returns:
        SnapshotMetadata instance
    """
    return SnapshotMetadata(
        cycle_number=cycle_num,
        timestamp=datetime.now(),
        previous_cycle=previous_cycle,
        previous_snapshot_timestamp=previous_timestamp,
        workspace_root=str(workspace_root) if workspace_root else None,
    )


def generate_project_state(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate project state summary from metrics.
    
    Args:
        metrics: Project metrics dictionary
    
    Returns:
        Project state dictionary
    """
    return {
        "total_agents": metrics.get("total_agents", 0),
        "total_completed_tasks": metrics.get("total_completed_tasks", 0),
        "total_achievements": metrics.get("total_achievements", 0),
        "active_tasks_count": metrics.get("active_tasks_count", 0),
        "overall_status": "active" if metrics.get("total_agents", 0) > 0 else "inactive",
        "productivity_indicators": {
            "tasks_per_agent": (
                metrics.get("total_completed_tasks", 0) / metrics.get("total_agents", 1)
                if metrics.get("total_agents", 0) > 0
                else 0
            ),
            "achievements_per_agent": (
                metrics.get("total_achievements", 0) / metrics.get("total_agents", 1)
                if metrics.get("total_agents", 0) > 0
                else 0
            ),
        },
    }


def aggregate_snapshot(
    all_data: Dict[str, Dict[str, Any]],
    cycle_num: int,
    workspace_root: Optional[Path] = None,
    previous_cycle: Optional[int] = None,
    previous_timestamp: Optional[datetime] = None
) -> CycleSnapshot:
    """
    Aggregate all collected data into unified snapshot.
    
    Args:
        all_data: Dict with keys: 'agent_status', 'task_log', 'git_activity'
        cycle_num: Current cycle number
        workspace_root: Root workspace path
        previous_cycle: Previous cycle number (optional)
        previous_timestamp: Previous snapshot timestamp (optional)
    
    Returns:
        CycleSnapshot instance
    """
    # Extract data
    agent_status_data = all_data.get("agent_status", {})
    task_log_data = all_data.get("task_log", {})
    git_data = all_data.get("git_activity", {})
    
    # Generate metadata
    metadata = generate_snapshot_metadata(
        cycle_num=cycle_num,
        workspace_root=workspace_root,
        previous_cycle=previous_cycle,
        previous_timestamp=previous_timestamp,
    )
    
    # Process agent accomplishments
    agent_accomplishments = {}
    for agent_id, status in agent_status_data.items():
        agent_accomplishments[agent_id] = AgentAccomplishments(
            agent_id=status.get("agent_id", agent_id),
            agent_name=status.get("agent_name", "Unknown"),
            completed_tasks=status.get("completed_tasks", []),
            achievements=status.get("achievements", []),
            current_tasks=status.get("current_tasks", []),
            current_mission=status.get("current_mission"),
            mission_priority=status.get("mission_priority"),
            cycle_count=status.get("cycle_count"),
        )
    
    # Calculate project metrics
    total_agents = len(agent_accomplishments)
    total_completed_tasks = sum(
        len(acc.completed_tasks) for acc in agent_accomplishments.values()
    )
    total_achievements = sum(
        len(acc.achievements) for acc in agent_accomplishments.values()
    )
    active_tasks_count = sum(
        len(acc.current_tasks) for acc in agent_accomplishments.values()
    )
    
    # Get git metrics
    git_metrics = git_data.get("metrics", {})
    task_log_metrics = task_log_data.get("metrics", {})
    
    project_metrics = ProjectMetrics(
        total_agents=total_agents,
        total_completed_tasks=total_completed_tasks,
        total_achievements=total_achievements,
        active_tasks_count=active_tasks_count,
        git_commits=git_metrics.get("commits", 0),
        git_files_changed=git_metrics.get("files_changed", 0),
        task_log_metrics=task_log_metrics,
    )
    
    # Create snapshot
    snapshot = CycleSnapshot(
        metadata=metadata,
        agent_accomplishments=agent_accomplishments,
        project_metrics=project_metrics,
        raw_data=all_data,
    )
    
    return snapshot

