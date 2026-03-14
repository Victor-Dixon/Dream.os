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
    task_log_file = Path(workspace_root) / "MASTER_TASK_LOG.md"

    if not task_log_file.exists():
        return {"error": "MASTER_TASK_LOG.md not found"}

    try:
        content = task_log_file.read_text(encoding="utf-8")
        return {"metrics": extract_task_metrics(content)}
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
    section = ""
    inbox_count = 0
    this_week_count = 0
    completed_count = 0
    by_priority = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for raw_line in task_log_content.splitlines():
        line = raw_line.strip()
        if line.startswith("##"):
            upper = line.upper()
            if "INBOX" in upper:
                section = "INBOX"
            elif "THIS WEEK" in upper:
                section = "THIS_WEEK"
            else:
                section = ""
            continue

        if not line.startswith("- ["):
            continue

        if section == "INBOX":
            inbox_count += 1
        elif section == "THIS_WEEK":
            this_week_count += 1

        if line.lower().startswith("- [x]"):
            completed_count += 1

        for priority in by_priority:
            if f"**{priority}**" in line.upper():
                by_priority[priority] += 1
                break

    return {
        "inbox_count": inbox_count,
        "this_week_count": this_week_count,
        "completed_count": completed_count,
        "by_priority": by_priority,
    }


def compare_with_previous_snapshot(current: Dict, previous: Dict) -> Dict[str, Any]:
    """
    Compare current metrics with previous snapshot.

    Args:
        current: Current task metrics
        previous: Previous task metrics

    Returns:
        Dict with comparison results
    """
    current_priorities = current.get("by_priority", {})
    previous_priorities = previous.get("by_priority", {})

    keys = set(current_priorities.keys()) | set(previous_priorities.keys())
    priority_changes = {
        key: current_priorities.get(key, 0) - previous_priorities.get(key, 0)
        for key in keys
    }

    return {
        "new_tasks": current.get("inbox_count", 0) - previous.get("inbox_count", 0),
        "completed_since_last": (
            current.get("completed_count", 0) - previous.get("completed_count", 0)
        ),
        "priority_changes": priority_changes,
    }
