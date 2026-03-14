# Header-Variant: full
# Owner: Dream.OS
# Purpose: snapshot aggregator.
# SSOT: docs/recovery/recovery_registry.yaml#tools-cycle-snapshots-aggregators-snapshot-aggregator
# @registry docs/recovery/recovery_registry.yaml#tools-cycle-snapshots-aggregators-snapshot-aggregator

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

from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from ..core.snapshot_models import (
    AgentAccomplishments,
    CycleSnapshot,
    ProjectMetrics,
    SnapshotMetadata,
)


def aggregate_snapshot(
    all_data: Dict[str, Dict],
    cycle_num: int = 1,
    workspace_root: Path | str = Path("."),
    previous_cycle: int | None = None,
) -> CycleSnapshot:
    """Aggregate all collected data into a unified CycleSnapshot object."""
    metadata = generate_snapshot_metadata(cycle_num, workspace_root, previous_cycle)

    agent_status = all_data.get("agent_status", {})
    accomplishments = [
        AgentAccomplishments(
            agent_id=agent_id,
            agent_name=data.get("agent_name", "Unknown Agent"),
            completed_tasks=data.get("completed_tasks", []),
            achievements=data.get("achievements", []),
            current_tasks=data.get("current_tasks", []),
            current_mission=data.get("current_mission", ""),
            mission_priority=data.get("mission_priority", "NORMAL"),
        )
        for agent_id, data in agent_status.items()
        if isinstance(data, dict)
    ]

    task_metrics = all_data.get("task_log", {}).get("metrics", {})
    git_metrics = all_data.get("git_activity", {}).get("metrics", {})
    project_metrics = ProjectMetrics(
        total_agents=len(accomplishments),
        total_completed_tasks=sum(len(a.completed_tasks) for a in accomplishments),
        total_achievements=sum(len(a.achievements) for a in accomplishments),
        active_tasks_count=sum(len(a.current_tasks) for a in accomplishments),
        git_commits=git_metrics.get("commits", 0),
        git_files_changed=git_metrics.get("files_changed", 0),
        productivity_indicators=generate_project_state(
            {
                "total_agents": len(accomplishments),
                "total_completed_tasks": sum(len(a.completed_tasks) for a in accomplishments),
                "total_achievements": sum(len(a.achievements) for a in accomplishments),
                "active_tasks_count": sum(len(a.current_tasks) for a in accomplishments),
            }
        ).get("productivity_indicators", {}),
    )

    return CycleSnapshot(
        metadata=metadata,
        agent_accomplishments=accomplishments,
        project_metrics=project_metrics,
        task_log={"metrics": task_metrics},
        git_activity={"metrics": git_metrics},
    )


def generate_snapshot_metadata(
    cycle_num: int,
    workspace_root: Path | str = Path("."),
    previous_cycle: int | None = None,
) -> SnapshotMetadata:
    """Generate metadata for the snapshot."""
    return SnapshotMetadata(
        cycle_number=cycle_num,
        workspace_root=str(workspace_root),
        previous_cycle=previous_cycle,
        generated_at=datetime.now(),
    )


def generate_project_state(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Generate summary state and productivity indicators from metrics."""
    total_agents = metrics.get("total_agents", 0)
    total_completed_tasks = metrics.get("total_completed_tasks", 0)
    total_achievements = metrics.get("total_achievements", 0)
    active_tasks_count = metrics.get("active_tasks_count", 0)

    if total_agents > 0:
        tasks_per_agent = total_completed_tasks / total_agents
        achievements_per_agent = total_achievements / total_agents
    else:
        tasks_per_agent = 0.0
        achievements_per_agent = 0.0

    return {
        "total_agents": total_agents,
        "total_completed_tasks": total_completed_tasks,
        "total_achievements": total_achievements,
        "active_tasks_count": active_tasks_count,
        "productivity_indicators": {
            "tasks_per_agent": round(tasks_per_agent, 2),
            "achievements_per_agent": round(achievements_per_agent, 2),
        },
    }
