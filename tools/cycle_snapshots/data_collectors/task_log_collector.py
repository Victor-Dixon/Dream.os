"""
Task Log Collector
==================

Parses MASTER_TASK_LOG.md and extracts task metrics.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: tools -->
"""

import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def extract_task_metrics(task_log_content: str) -> Dict[str, Any]:
    """
    Extract task metrics from MASTER_TASK_LOG.md content.
    
    Args:
        task_log_content: Content of MASTER_TASK_LOG.md
    
    Returns:
        Dict with task metrics
    """
    metrics = {
        "inbox_count": 0,
        "this_week_count": 0,
        "waiting_on_count": 0,
        "parked_count": 0,
        "by_priority": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
        "by_initiative": {},
        "blockers": [],
        "completed_count": 0,
    }
    
    # Count tasks in each section
    sections = {
        "INBOX": r"## 📥 INBOX",
        "THIS WEEK": r"## 📋 THIS WEEK",
        "WAITING ON": r"## ⏸️ WAITING ON",
        "PARKED": r"## 🅿️ PARKED",
    }
    
    current_section = None
    lines = task_log_content.split("\n")
    
    for i, line in enumerate(lines):
        # Detect section headers
        for section_name, pattern in sections.items():
            if re.search(pattern, line, re.IGNORECASE):
                current_section = section_name
                break
        
        # Count tasks in current section
        if current_section and line.strip().startswith("- ["):
            if current_section == "INBOX":
                metrics["inbox_count"] += 1
            elif current_section == "THIS WEEK":
                metrics["this_week_count"] += 1
            elif current_section == "WAITING ON":
                metrics["waiting_on_count"] += 1
            elif current_section == "PARKED":
                metrics["parked_count"] += 1
            
            # Extract priority
            priority_match = re.search(r"\*\*(HIGH|MEDIUM|LOW)\*\*", line)
            if priority_match:
                priority = priority_match.group(1)
                metrics["by_priority"][priority] = metrics["by_priority"].get(priority, 0) + 1
            
            # Extract initiative (if present)
            initiative_match = re.search(r"\[([^\]]+)\]", line)
            if initiative_match:
                initiative = initiative_match.group(1)
                metrics["by_initiative"][initiative] = metrics["by_initiative"].get(initiative, 0) + 1
            
            # Check for blockers
            if "blocker" in line.lower() or "⏸️" in line:
                metrics["blockers"].append(line.strip())
        
        # Count completed tasks
        if line.strip().startswith("- [x]"):
            metrics["completed_count"] += 1
    
    return metrics


def compare_with_previous_snapshot(
    current: Dict[str, Any],
    previous: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compare current task metrics with previous snapshot.
    
    Args:
        current: Current task metrics
        previous: Previous snapshot task metrics (optional)
    
    Returns:
        Dict with comparison results
    """
    if not previous:
        return {
            "new_tasks": current.get("inbox_count", 0),
            "completed_since_last": 0,
            "priority_changes": {},
        }
    
    comparison = {
        "new_tasks": current.get("inbox_count", 0) - previous.get("inbox_count", 0),
        "completed_since_last": current.get("completed_count", 0) - previous.get("completed_count", 0),
        "priority_changes": {},
    }
    
    # Compare priority counts
    for priority in ["HIGH", "MEDIUM", "LOW"]:
        current_count = current.get("by_priority", {}).get(priority, 0)
        previous_count = previous.get("by_priority", {}).get(priority, 0)
        if current_count != previous_count:
            comparison["priority_changes"][priority] = current_count - previous_count
    
    return comparison


def parse_task_log(workspace_root: Path) -> Dict[str, Any]:
    """
    Parse MASTER_TASK_LOG.md and extract task metrics.
    
    Args:
        workspace_root: Root workspace path
    
    Returns:
        Dict with task log data
    """
    task_log_file = workspace_root / "MASTER_TASK_LOG.md"
    
    if not task_log_file.exists():
        logger.warning(f"MASTER_TASK_LOG.md not found: {task_log_file}")
        return {
            "error": "MASTER_TASK_LOG.md not found",
            "metrics": {},
        }
    
    try:
        content = task_log_file.read_text(encoding="utf-8")
        metrics = extract_task_metrics(content)
        
        return {
            "file_path": str(task_log_file),
            "metrics": metrics,
            "timestamp": task_log_file.stat().st_mtime,
        }
    
    except Exception as e:
        logger.error(f"Error parsing MASTER_TASK_LOG.md: {e}")
        return {
            "error": str(e),
            "metrics": {},
        }

