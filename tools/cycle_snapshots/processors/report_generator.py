"""
Report Generator for Cycle Snapshot System
=========================================

Generates human-readable markdown reports from snapshot data.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-08
V2 Compliant: Yes (<400 lines)

<!-- SSOT Domain: tools -->
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def format_agent_section(agent_id: str, agent_data: Dict[str, Any]) -> str:
    """Format a markdown section for a single agent."""
    name = agent_data.get("agent_name", "Unknown")
    mission = agent_data.get("current_mission", "")
    completed = agent_data.get("completed_tasks", [])
    achievements = agent_data.get("achievements", [])
    current_tasks = agent_data.get("current_tasks", [])

    lines = [f"### {agent_id} — {name}"]
    if mission:
        lines.append(f"**Mission:** {mission}")

    if current_tasks:
        lines.append("**Current Tasks:**")
        lines.extend([f"- {task}" for task in current_tasks])

    if completed:
        lines.append("**Completed Tasks:**")
        lines.extend([f"- {task}" for task in completed])

    if achievements:
        lines.append("**Achievements:**")
        lines.extend([f"- {achievement}" for achievement in achievements])

    return "\n".join(lines)


def format_metrics_section(project_state: Dict[str, Any], task_metrics: Dict[str, Any], git_metrics: Dict[str, Any]) -> str:
    """Format a markdown section summarizing metrics."""
    lines = ["## Project Metrics"]
    lines.append(f"- Active agents: {project_state.get('active_agents', 0)}")
    lines.append(f"- Task completion rate: {project_state.get('task_completion_rate', 0):.2f}%")
    lines.append(f"- Commits per day: {project_state.get('commits_per_day', 0)}")
    lines.append(f"- Project health: {project_state.get('project_health', 'unknown')}")
    lines.append(f"- Cycle velocity: {project_state.get('cycle_velocity', 'unknown')}")

    lines.append("\n### Task Metrics")
    lines.append(f"- Total tasks: {task_metrics.get('total_tasks', 0)}")
    lines.append(f"- Completed tasks: {task_metrics.get('completed_tasks', 0)}")
    lines.append(f"- In-progress tasks: {task_metrics.get('in_progress_tasks', 0)}")
    lines.append(f"- Blocked tasks: {task_metrics.get('blocked_tasks', 0)}")

    lines.append("\n### Git Metrics")
    lines.append(f"- Total commits: {git_metrics.get('total_commits', 0)}")
    lines.append(f"- Unique authors: {git_metrics.get('unique_authors', 0)}")
    lines.append(f"- Most active agent: {git_metrics.get('most_active_agent') or 'N/A'}")

    return "\n".join(lines)


def generate_markdown_report(snapshot: Dict[str, Any]) -> str:
    """Generate a markdown report from snapshot data."""
    metadata = snapshot.get("snapshot_metadata", {})
    cycle_number = metadata.get("cycle_number", "Unknown")
    generated_at = metadata.get("generated_at")
    if generated_at:
        try:
            generated_at = datetime.fromisoformat(generated_at).isoformat()
        except ValueError:
            pass

    header_lines = [f"# Cycle Snapshot — Cycle {cycle_number}"]
    if generated_at:
        header_lines.append(f"Generated at: {generated_at}")

    project_state = snapshot.get("project_state", {})
    task_metrics = snapshot.get("task_metrics", {})
    git_metrics = snapshot.get("git_activity", {}).get("metrics", {})

    report_sections: List[str] = ["\n".join(header_lines)]
    report_sections.append(format_metrics_section(project_state, task_metrics, git_metrics))

    agent_status = snapshot.get("agent_status", {})
    if agent_status:
        report_sections.append("## Agent Updates")
        for agent_id, data in agent_status.items():
            report_sections.append(format_agent_section(agent_id, data))
    else:
        report_sections.append("## Agent Updates\nNo agent status data available.")

    reset_status = metadata.get("reset_status")
    if reset_status:
        report_sections.append("## Status Reset Summary")
        report_sections.append(f"- Agents reset: {', '.join(reset_status.get('agents_reset', [])) or 'None'}")
        report_sections.append(
            f"- Agents failed: {', '.join(reset_status.get('agents_failed', [])) or 'None'}"
        )

    return "\n\n".join(report_sections)
