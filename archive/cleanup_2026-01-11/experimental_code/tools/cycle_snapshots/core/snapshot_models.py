"""
Snapshot Models for Cycle Snapshot System
========================================

Data models and type definitions for snapshots.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, classes <200 lines)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


@dataclass
class SnapshotMetadata:
    """Metadata for a cycle snapshot."""
    cycle_number: int
    snapshot_version: str = "0.1.0"
    generated_at: datetime = field(default_factory=datetime.now)
    system: str = "Cycle Snapshot System"
    purpose: str = "Central nervous system data collection for swarm coordination"


@dataclass
class AgentStatus:
    """Status data for a single agent."""
    agent_id: str
    agent_name: str
    status: str
    fsm_state: str
    current_phase: str
    last_updated: datetime
    current_mission: str = ""
    mission_priority: str = "NORMAL"
    current_tasks: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)


@dataclass
class TaskMetrics:
    """Metrics extracted from MASTER_TASK_LOG.md."""
    total_tasks: int = 0
    completed_tasks: int = 0
    in_progress_tasks: int = 0
    pending_tasks: int = 0
    blocked_tasks: int = 0
    high_priority_tasks: int = 0
    completion_rate: float = 0.0
    agent_assignments: Dict[str, int] = field(default_factory=dict)


@dataclass
class GitMetrics:
    """Metrics from git activity analysis."""
    total_commits: int = 0
    unique_authors: int = 0
    commits_per_day: float = 0.0
    agent_contributions: Dict[str, int] = field(default_factory=dict)
    most_active_agent: Optional[str] = None


@dataclass
class ProjectState:
    """Overall project state summary."""
    active_agents: int = 0
    total_agents: int = 8
    task_completion_rate: float = 0.0
    commits_per_day: float = 0.0
    project_health: str = "unknown"  # excellent, good, fair, needs_attention
    cycle_velocity: str = "unknown"  # high, medium, low


@dataclass
class CycleSnapshot:
    """Complete cycle snapshot data structure."""
    metadata: SnapshotMetadata
    project_state: ProjectState
    agent_status: Dict[str, AgentStatus] = field(default_factory=dict)
    task_metrics: TaskMetrics = field(default_factory=TaskMetrics)
    git_metrics: GitMetrics = field(default_factory=GitMetrics)
    mcp_data: Dict[str, Any] = field(default_factory=dict)
    collected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary for JSON serialization."""
        return {
            "metadata": {
                "cycle_number": self.metadata.cycle_number,
                "snapshot_version": self.metadata.snapshot_version,
                "generated_at": self.metadata.generated_at.isoformat(),
                "system": self.metadata.system,
                "purpose": self.metadata.purpose
            },
            "project_state": {
                "active_agents": self.project_state.active_agents,
                "total_agents": self.project_state.total_agents,
                "task_completion_rate": self.project_state.task_completion_rate,
                "commits_per_day": self.project_state.commits_per_day,
                "project_health": self.project_state.project_health,
                "cycle_velocity": self.project_state.cycle_velocity
            },
            "agent_status": {k: v.__dict__ for k, v in self.agent_status.items()},
            "task_metrics": self.task_metrics.__dict__,
            "git_metrics": self.git_metrics.__dict__,
            "mcp_data": self.mcp_data,
            "collected_at": self.collected_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CycleSnapshot':
        """Create snapshot from dictionary."""
        metadata = SnapshotMetadata(**data["metadata"])

        # Convert ISO strings back to datetime
        metadata.generated_at = datetime.fromisoformat(metadata.generated_at)

        project_state = ProjectState(**data["project_state"])

        agent_status = {}
        for k, v in data["agent_status"].items():
            # Convert last_updated back to datetime
            if "last_updated" in v:
                v["last_updated"] = datetime.fromisoformat(v["last_updated"])
            agent_status[k] = AgentStatus(**v)

        task_metrics = TaskMetrics(**data["task_metrics"])
        git_metrics = GitMetrics(**data["git_metrics"])
        mcp_data = data["mcp_data"]
        collected_at = datetime.fromisoformat(data["collected_at"])

        return cls(
            metadata=metadata,
            project_state=project_state,
            agent_status=agent_status,
            task_metrics=task_metrics,
            git_metrics=git_metrics,
            mcp_data=mcp_data,
            collected_at=collected_at
        )