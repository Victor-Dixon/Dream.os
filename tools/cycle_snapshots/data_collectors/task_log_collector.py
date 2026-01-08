"""
Task Log Collector for Cycle Snapshot System
===========================================

Parses MASTER_TASK_LOG.md and extracts task metrics.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, functions <30 lines)
"""

import logging
import re
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def parse_task_log(workspace_root: Path) -> Dict[str, Any]:
    """
    Parse MASTER_TASK_LOG.md and extract task data.

    Args:
        workspace_root: Path to workspace root directory

    Returns:
        Dict containing parsed task log data
    """
    task_log_file = workspace_root / "MASTER_TASK_LOG.md"

    if not task_log_file.exists():
        return {"error": "MASTER_TASK_LOG.md not found"}

    try:
        content = task_log_file.read_text(encoding='utf-8')
        return extract_task_metrics(content)
    except Exception as e:
        logger.error(f"Task log parsing failed: {e}")
        return {"error": str(e)}


def extract_task_metrics(task_log_content: str) -> Dict[str, Any]:
    """
    Extract metrics from task log content.

    Args:
        task_log_content: Raw content of MASTER_TASK_LOG.md

    Returns:
        Dict with task metrics and statistics
    """
    metrics = {
        "total_tasks": 0,
        "completed_tasks": 0,
        "in_progress_tasks": 0,
        "pending_tasks": 0,
        "blocked_tasks": 0,
        "high_priority_tasks": 0,
        "agent_assignments": {},
        "completion_rate": 0.0
    }

    # Count tasks by status
    completed_pattern = r'-\s*\[x\]'
    in_progress_pattern = r'-\s*\[ \]'
    pending_pattern = r'-\s*\[ \]'
    blocked_pattern = r'blocked|BLOCKED'

    metrics["completed_tasks"] = len(re.findall(completed_pattern, task_log_content))
    metrics["in_progress_tasks"] = len(re.findall(r'IN PROGRESS|in progress', task_log_content))
    metrics["blocked_tasks"] = len(re.findall(blocked_pattern, task_log_content))

    # Count total tasks (all bullet points that look like tasks)
    task_lines = [line for line in task_log_content.split('\n')
                  if line.strip().startswith('-') and ('pts)' in line or 'HIGH' in line or 'MEDIUM' in line or 'LOW' in line)]
    metrics["total_tasks"] = len(task_lines)

    # Count high priority tasks
    high_priority_pattern = r'HIGH.*pts|pts.*HIGH'
    metrics["high_priority_tasks"] = len(re.findall(high_priority_pattern, task_log_content))

    # Calculate completion rate
    if metrics["total_tasks"] > 0:
        metrics["completion_rate"] = (metrics["completed_tasks"] / metrics["total_tasks"]) * 100

    # Extract agent assignments
    agent_pattern = r'\[([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\]'
    agent_matches = re.findall(agent_pattern, task_log_content)
    for agent in agent_matches:
        if agent in metrics["agent_assignments"]:
            metrics["agent_assignments"][agent] += 1
        else:
            metrics["agent_assignments"][agent] = 1

    return metrics


def compare_with_previous_snapshot(current: Dict, previous: Dict) -> Dict[str, Any]:
    """
    Compare current metrics with previous snapshot.

    Args:
        current: Current task metrics
        previous: Previous task metrics

    Returns:
        Dict with comparison results
    """
    comparison = {
        "tasks_completed_since_last": 0,
        "completion_rate_change": 0.0,
        "new_assignments": {},
        "velocity_trend": "stable"
    }

    if "completed_tasks" in current and "completed_tasks" in previous:
        comparison["tasks_completed_since_last"] = current["completed_tasks"] - previous["completed_tasks"]

    if "completion_rate" in current and "completion_rate" in previous:
        comparison["completion_rate_change"] = current["completion_rate"] - previous["completion_rate"]

        if comparison["completion_rate_change"] > 5:
            comparison["velocity_trend"] = "accelerating"
        elif comparison["completion_rate_change"] < -5:
            comparison["velocity_trend"] = "slowing"

    # Compare agent assignments
    current_assignments = current.get("agent_assignments", {})
    previous_assignments = previous.get("agent_assignments", {})

    for agent, count in current_assignments.items():
        prev_count = previous_assignments.get(agent, 0)
        if count > prev_count:
            comparison["new_assignments"][agent] = count - prev_count

    return comparison