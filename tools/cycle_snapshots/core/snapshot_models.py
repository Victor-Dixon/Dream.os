# Header-Variant: full
# Owner: Dream.OS
# Purpose: snapshot models.
# SSOT: docs/recovery/recovery_registry.yaml#tools-cycle-snapshots-core-snapshot-models
# @registry docs/recovery/recovery_registry.yaml#tools-cycle-snapshots-core-snapshot-models

"""
Snapshot Models for Cycle Snapshot System
========================================

Data models and type definitions for snapshots.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, classes <200 lines)

<!-- SSOT Domain: tools -->
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


@dataclass
class SnapshotMetadata:
    """Metadata for a cycle snapshot."""

    cycle_number: int
    workspace_root: str = ""
    previous_cycle: int | None = None
    snapshot_version: str = "0.1.0"
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentAccomplishments:
    """Accomplishments summary for an agent in a cycle snapshot."""

    agent_id: str
    agent_name: str = "Unknown Agent"
    completed_tasks: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    current_tasks: List[str] = field(default_factory=list)
    current_mission: str = ""
    mission_priority: str = "NORMAL"


@dataclass
class ProjectMetrics:
    """Top-level numeric metrics for snapshot reports."""

    total_agents: int = 0
    total_completed_tasks: int = 0
    total_achievements: int = 0
    active_tasks_count: int = 0
    git_commits: int = 0
    git_files_changed: int = 0
    productivity_indicators: Dict[str, float] = field(default_factory=dict)


@dataclass
class CycleSnapshot:
    """Complete cycle snapshot data structure used by phase 1 tests."""

    metadata: SnapshotMetadata
    agent_accomplishments: List[AgentAccomplishments] = field(default_factory=list)
    project_metrics: ProjectMetrics = field(default_factory=ProjectMetrics)
    task_log: Dict[str, Any] = field(default_factory=dict)
    git_activity: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary for report generation."""
        return {
            "snapshot_metadata": {
                "cycle": self.metadata.cycle_number,
                "date": self.metadata.generated_at.isoformat(),
                "previous_cycle": self.metadata.previous_cycle,
            },
            "agent_accomplishments": {
                item.agent_id: {
                    "agent_id": item.agent_id,
                    "agent_name": item.agent_name,
                    "current_mission": item.current_mission,
                    "mission_priority": item.mission_priority,
                    "completed_tasks": item.completed_tasks,
                    "achievements": item.achievements,
                    "current_tasks": item.current_tasks,
                }
                for item in self.agent_accomplishments
            },
            "project_metrics": self.project_metrics.__dict__,
            "task_log": self.task_log,
            "git_activity": self.git_activity,
        }
