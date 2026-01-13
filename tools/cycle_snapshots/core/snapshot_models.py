"""
Snapshot Data Models
===================

Core data models for cycle snapshot system.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional


@dataclass
class SnapshotMetadata:
    """Metadata for a cycle snapshot."""
    
    cycle_number: int
    timestamp: datetime
    previous_cycle: Optional[int] = None
    previous_snapshot_timestamp: Optional[datetime] = None
    workspace_root: Optional[str] = None


@dataclass
class AgentAccomplishments:
    """Accomplishments for a single agent."""
    
    agent_id: str
    agent_name: str
    completed_tasks: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    current_tasks: List[str] = field(default_factory=list)
    current_mission: Optional[str] = None
    mission_priority: Optional[str] = None
    cycle_count: Optional[int] = None


@dataclass
class ProjectMetrics:
    """Project-level metrics."""
    
    total_agents: int
    total_completed_tasks: int
    total_achievements: int
    active_tasks_count: int
    git_commits: int = 0
    git_files_changed: int = 0
    task_log_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CycleSnapshot:
    """Complete cycle snapshot structure."""
    
    metadata: SnapshotMetadata
    agent_accomplishments: Dict[str, AgentAccomplishments]
    project_metrics: ProjectMetrics
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary for JSON serialization."""
        return {
            "snapshot_metadata": {
                "cycle": self.metadata.cycle_number,
                "date": self.metadata.timestamp.isoformat(),
                "previous_cycle": self.metadata.previous_cycle,
                "previous_snapshot_timestamp": (
                    self.metadata.previous_snapshot_timestamp.isoformat()
                    if self.metadata.previous_snapshot_timestamp
                    else None
                ),
                "workspace_root": self.metadata.workspace_root,
            },
            "agent_accomplishments": {
                agent_id: {
                    "agent_id": acc.agent_id,
                    "agent_name": acc.agent_name,
                    "completed_tasks": acc.completed_tasks,
                    "achievements": acc.achievements,
                    "current_tasks": acc.current_tasks,
                    "current_mission": acc.current_mission,
                    "mission_priority": acc.mission_priority,
                    "cycle_count": acc.cycle_count,
                }
                for agent_id, acc in self.agent_accomplishments.items()
            },
            "project_metrics": {
                "total_agents": self.project_metrics.total_agents,
                "total_completed_tasks": self.project_metrics.total_completed_tasks,
                "total_achievements": self.project_metrics.total_achievements,
                "active_tasks_count": self.project_metrics.active_tasks_count,
                "git_commits": self.project_metrics.git_commits,
                "git_files_changed": self.project_metrics.git_files_changed,
                "task_log_metrics": self.project_metrics.task_log_metrics,
            },
            "raw_data": self.raw_data,
        }

