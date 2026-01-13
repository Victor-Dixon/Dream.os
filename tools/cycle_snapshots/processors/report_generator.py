#!/usr/bin/env python3
"""
Cycle Snapshot Report Generator
===============================

Generates markdown reports from cycle snapshot data.

Author: Agent-8 (Quality Assurance & Testing Specialist)
Created: 2026-01-10
V2 Compliant: Yes
"""

from typing import Dict, Any, List
from datetime import datetime


def generate_markdown_report(snapshot: Dict[str, Any]) -> str:
    """
    Generate complete markdown report from snapshot data.

    Args:
        snapshot: Dictionary containing snapshot data with keys:
            - snapshot_metadata: Dict with cycle, date, previous_cycle
            - agent_accomplishments: Dict of agent data
            - project_metrics: Dict with total_agents, etc.

    Returns:
        Complete markdown report as string
    """
    lines = []

    # Header
    metadata = snapshot.get("snapshot_metadata", {})
    cycle_num = metadata.get("cycle", "Unknown")
    date = metadata.get("date", datetime.now().isoformat())

    lines.append("# Cycle Snapshot Report")
    lines.append("")
    lines.append(f"**Cycle:** {cycle_num}")
    lines.append(f"**Date:** {date}")
    lines.append("")

    # Agent Accomplishments
    agent_data = snapshot.get("agent_accomplishments", {})
    if agent_data:
        lines.append("## Agent Accomplishments")
        lines.append("")

        for agent_id, data in agent_data.items():
            lines.append(format_agent_section(agent_id, data))
            lines.append("")
    else:
        lines.append("## Agent Accomplishments")
        lines.append("")
        lines.append("*No agent data available*")
        lines.append("")

    # Project Metrics
    metrics = snapshot.get("project_metrics", {})
    if metrics:
        lines.append("## Project Metrics")
        lines.append("")
        lines.append(format_metrics_section(metrics))
        lines.append("")

    return "\n".join(lines)


def format_agent_section(agent_id: str, agent_data: Dict[str, Any]) -> str:
    """
    Format agent section for markdown report.

    Args:
        agent_id: Agent identifier (e.g., "Agent-1")
        agent_data: Agent data dictionary

    Returns:
        Formatted markdown section
    """
    lines = []

    agent_name = agent_data.get("agent_name", "Unknown Agent")
    current_mission = agent_data.get("current_mission", "No mission")
    mission_priority = agent_data.get("mission_priority", "Unknown")

    lines.append(f"### {agent_id}: {agent_name}")
    lines.append("")
    lines.append(f"**Mission:** {current_mission}")
    lines.append(f"**Priority:** {mission_priority}")
    lines.append("")

    # Completed Tasks
    completed_tasks = agent_data.get("completed_tasks", [])
    if completed_tasks:
        lines.append("**Completed Tasks:**")
        for task in completed_tasks:
            lines.append(f"- {task}")
        lines.append("")

    # Current Tasks
    current_tasks = agent_data.get("current_tasks", [])
    if current_tasks:
        lines.append("**Current Tasks:**")
        for task in current_tasks:
            lines.append(f"- {task}")
        lines.append("")

    # Achievements
    achievements = agent_data.get("achievements", [])
    if achievements:
        lines.append("**Achievements:**")
        for achievement in achievements:
            lines.append(f"- {achievement}")
        lines.append("")

    return "\n".join(lines)


def format_metrics_section(metrics: Dict[str, Any]) -> str:
    """
    Format metrics section for markdown report.

    Args:
        metrics: Dictionary containing project metrics

    Returns:
        Formatted markdown section
    """
    lines = []

    lines.append("### Project Overview")
    lines.append("")

    # Basic metrics
    total_agents = metrics.get("total_agents", 0)
    total_completed_tasks = metrics.get("total_completed_tasks", 0)
    total_achievements = metrics.get("total_achievements", 0)
    active_tasks_count = metrics.get("active_tasks_count", 0)

    lines.append(f"- **Total Agents:** {total_agents}")
    lines.append(f"- **Completed Tasks:** {total_completed_tasks}")
    lines.append(f"- **Total Achievements:** {total_achievements}")
    lines.append(f"- **Active Tasks:** {active_tasks_count}")
    lines.append("")

    # Git metrics
    git_commits = metrics.get("git_commits", 0)
    git_files_changed = metrics.get("git_files_changed", 0)

    if git_commits > 0 or git_files_changed > 0:
        lines.append("### Git Activity")
        lines.append("")
        lines.append(f"- **Commits:** {git_commits}")
        lines.append(f"- **Files Changed:** {git_files_changed}")
        lines.append("")

    # Productivity indicators
    productivity = metrics.get("productivity_indicators", {})
    if productivity:
        lines.append("### Productivity Indicators")
        lines.append("")
        tasks_per_agent = productivity.get("tasks_per_agent", 0)
        achievements_per_agent = productivity.get("achievements_per_agent", 0)

        lines.append(f"- **Tasks per Agent:** {tasks_per_agent:.1f}")
        lines.append(f"- **Achievements per Agent:** {achievements_per_agent:.1f}")

    return "\n".join(lines)