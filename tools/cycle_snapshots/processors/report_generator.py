"""
Report Generator
================

Generates markdown report from snapshot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines where possible)

<!-- SSOT Domain: tools -->
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def format_agent_section(agent_id: str, agent_data: Dict[str, Any]) -> str:
    """
    Format agent accomplishments section.
    
    Args:
        agent_id: Agent ID (e.g., "Agent-1")
        agent_data: Agent accomplishments data
    
    Returns:
        Formatted markdown section
    """
    lines = [f"### {agent_id}: {agent_data.get('agent_name', 'Unknown')}"]
    lines.append("")
    
    # Mission
    mission = agent_data.get("current_mission")
    if mission:
        lines.append(f"**Mission:** {mission}")
        lines.append("")
    
    # Completed Tasks
    completed_tasks = agent_data.get("completed_tasks", [])
    if completed_tasks:
        lines.append("**Completed Tasks:**")
        for task in completed_tasks[:10]:  # Limit to 10 for readability
            if isinstance(task, str):
                lines.append(f"- {task}")
            else:
                lines.append(f"- {task}")
        if len(completed_tasks) > 10:
            lines.append(f"- *... and {len(completed_tasks) - 10} more*")
        lines.append("")
    
    # Achievements
    achievements = agent_data.get("achievements", [])
    if achievements:
        lines.append("**Achievements:**")
        for achievement in achievements[:5]:  # Limit to 5
            lines.append(f"- {achievement}")
        if len(achievements) > 5:
            lines.append(f"- *... and {len(achievements) - 5} more*")
        lines.append("")
    
    # Current Tasks
    current_tasks = agent_data.get("current_tasks", [])
    if current_tasks:
        lines.append("**Active Tasks:**")
        for task in current_tasks[:5]:  # Limit to 5
            if isinstance(task, str):
                lines.append(f"- {task}")
            else:
                lines.append(f"- {task}")
        if len(current_tasks) > 5:
            lines.append(f"- *... and {len(current_tasks) - 5} more*")
        lines.append("")
    
    return "\n".join(lines)


def format_metrics_section(metrics: Dict[str, Any]) -> str:
    """
    Format project metrics section.
    
    Args:
        metrics: Project metrics dictionary
    
    Returns:
        Formatted markdown section
    """
    lines = ["## 📊 Project Metrics", ""]
    
    # Summary
    lines.append("### Summary")
    lines.append(f"- **Total Agents:** {metrics.get('total_agents', 0)}")
    lines.append(f"- **Completed Tasks:** {metrics.get('total_completed_tasks', 0)}")
    lines.append(f"- **Achievements:** {metrics.get('total_achievements', 0)}")
    lines.append(f"- **Active Tasks:** {metrics.get('active_tasks_count', 0)}")
    lines.append("")
    
    # Git Activity
    git_commits = metrics.get("git_commits", 0)
    if git_commits > 0:
        lines.append("### Git Activity")
        lines.append(f"- **Commits:** {git_commits}")
        lines.append(f"- **Files Changed:** {metrics.get('git_files_changed', 0)}")
        lines.append("")
    
    # Task Log Metrics
    task_log_metrics = metrics.get("task_log_metrics", {})
    if task_log_metrics:
        lines.append("### Task Log Metrics")
        inbox_count = task_log_metrics.get("inbox_count", 0)
        this_week_count = task_log_metrics.get("this_week_count", 0)
        if inbox_count > 0 or this_week_count > 0:
            lines.append(f"- **Inbox Tasks:** {inbox_count}")
            lines.append(f"- **This Week Tasks:** {this_week_count}")
            lines.append("")
    
    return "\n".join(lines)


def generate_markdown_report(snapshot: Dict[str, Any]) -> str:
    """
    Generate complete markdown report from snapshot.
    
    Args:
        snapshot: Snapshot dictionary (from CycleSnapshot.to_dict())
    
    Returns:
        Complete markdown report string
    """
    lines = []
    
    # Header
    metadata = snapshot.get("snapshot_metadata", {})
    cycle_num = metadata.get("cycle", 0)
    date_str = metadata.get("date", datetime.now().isoformat())
    
    lines.append(f"# Cycle Snapshot - Cycle {cycle_num}")
    lines.append("")
    lines.append(f"**Date:** {date_str}")
    lines.append(f"**Previous Cycle:** {metadata.get('previous_cycle', 'N/A')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Executive Summary
    lines.append("## 📋 Executive Summary")
    lines.append("")
    agent_accomplishments = snapshot.get("agent_accomplishments", {})
    project_metrics = snapshot.get("project_metrics", {})
    
    lines.append(
        f"This snapshot captures the state of {project_metrics.get('total_agents', 0)} "
        f"active agents with {project_metrics.get('total_completed_tasks', 0)} completed tasks "
        f"and {project_metrics.get('total_achievements', 0)} achievements."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Agent Accomplishments
    lines.append("## 👥 Agent Accomplishments")
    lines.append("")
    
    for agent_id, agent_data in agent_accomplishments.items():
        lines.append(format_agent_section(agent_id, agent_data))
        lines.append("---")
        lines.append("")
    
    # Project Metrics
    lines.append(format_metrics_section(project_metrics))
    lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Generated by Cycle Snapshot System*")
    
    return "\n".join(lines)

