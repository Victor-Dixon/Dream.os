"""
Status Resetter Module
======================

Safely resets agent status.json files after snapshot generation.

Protocol: CYCLE_SNAPSHOT_SYSTEM v1.0
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-08
V2 Compliant: Yes (<400 lines)

<!-- SSOT Domain: tools -->
"""

from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ResetResult:
    """Outcome of resetting a single agent status file."""

    success: bool
    error: Optional[str] = None
    backup_file: Optional[Path] = None
    archived_data: Dict[str, Any] = None


class StatusBackupManager:
    """Manages status.json backups before reset."""

    def __init__(self, workspace_root: Path, retention_days: int = 30) -> None:
        self.backup_dir = workspace_root / "reports" / "cycle_snapshots" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.retention_days = retention_days

    def backup_status(self, agent_id: str, status_file: Path) -> Path:
        """Create backup of status.json before reset."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"{agent_id}_status_{timestamp}.json"
        shutil.copy(status_file, backup_file)
        logger.info("Backed up %s status to %s", agent_id, backup_file)
        return backup_file

    def cleanup_old_backups(self) -> int:
        """Remove backups older than retention period."""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        removed = 0
        for backup_file in self.backup_dir.glob("*.json"):
            if datetime.fromtimestamp(backup_file.stat().st_mtime) < cutoff:
                backup_file.unlink()
                removed += 1
        if removed:
            logger.info("Cleaned up %s old backups", removed)
        return removed


class StatusValidator:
    """Validates status.json structure and content."""

    REQUIRED_FIELDS = {"agent_id", "agent_name", "status", "fsm_state", "current_phase"}

    @staticmethod
    def validate_status_json(status: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate status.json structure and content."""
        errors = []
        missing = StatusValidator.REQUIRED_FIELDS - status.keys()
        if missing:
            errors.append(f"Missing required fields: {', '.join(sorted(missing))}")

        try:
            json.dumps(status)
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"Invalid JSON structure: {exc}")

        if "agent_id" in status and not isinstance(status["agent_id"], str):
            errors.append("agent_id must be string")

        if "cycle_count" in status and not isinstance(status["cycle_count"], int):
            errors.append("cycle_count must be integer")

        return not errors, errors


def filter_completed_items(items: List[Any]) -> Tuple[List[Any], List[Any]]:
    """Filter items into completed and active buckets."""
    completed = []
    active = []
    completion_markers = ("✅", "🟡", "⏳")

    for item in items:
        if isinstance(item, str) and item.startswith(completion_markers):
            completed.append(item)
        else:
            active.append(item)

    return completed, active


def filter_completed_coordinations(coordination_status: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Filter coordination status entries into completed and active buckets."""
    completed: Dict[str, Any] = {}
    active: Dict[str, Any] = {}

    for key, value in coordination_status.items():
        if isinstance(value, dict):
            status = str(value.get("status", "")).upper()
            if status in {"COMPLETE", "BLOCKED"}:
                completed[key] = value
            else:
                active[key] = value
        else:
            active[key] = value

    return completed, active


def generate_reset_status(
    current_status: Dict[str, Any],
    snapshot_timestamp: datetime,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Generate reset status.json content and archived data."""
    completed_tasks, active_tasks = filter_completed_items(current_status.get("current_tasks", []))
    completed_actions, active_actions = filter_completed_items(current_status.get("next_actions", []))
    completed_coord, active_coord = filter_completed_coordinations(current_status.get("coordination_status", {}))

    archived_data = {
        "completed_tasks": completed_tasks,
        "completed_next_actions": completed_actions,
        "completed_coordination": completed_coord,
        "achievements": current_status.get("achievements", []),
        "completed_tasks_log": current_status.get("completed_tasks", []),
        "recent_commit": current_status.get("recent_commit"),
        "recent_artifact": current_status.get("recent_artifact"),
    }

    reset_status = {
        "agent_id": current_status.get("agent_id"),
        "agent_name": current_status.get("agent_name"),
        "status": current_status.get("status", "ACTIVE_AGENT_MODE"),
        "fsm_state": current_status.get("fsm_state", "ACTIVE"),
        "current_phase": current_status.get("current_phase", "TASK_EXECUTION"),
        "current_mission": current_status.get("current_mission", ""),
        "mission_priority": current_status.get("mission_priority", "NORMAL"),
        "mission_description": current_status.get("mission_description", ""),
        "cycle_count": current_status.get("cycle_count", 0) + 1,
        "last_updated": snapshot_timestamp.isoformat(),
        "current_tasks": active_tasks,
        "next_actions": active_actions,
        "completed_tasks": [],
        "achievements": [],
        "coordination_status": active_coord,
        "recent_commit": None,
        "recent_artifact": None,
    }

    known_fields = set(reset_status.keys())
    for key, value in current_status.items():
        if key not in known_fields:
            reset_status[key] = value

    return reset_status, archived_data


def reset_agent_status_safely(
    agent_id: str,
    snapshot_data: Dict[str, Any],
    workspace_root: Path,
    snapshot_timestamp: datetime,
) -> ResetResult:
    """Safely reset agent status.json with full error handling."""
    status_file = workspace_root / "agent_workspaces" / agent_id / "status.json"
    if not status_file.exists():
        return ResetResult(False, f"Status file not found: {status_file}")

    backup_manager = StatusBackupManager(workspace_root)
    validator = StatusValidator()

    backup_file: Optional[Path] = None
    try:
        backup_file = backup_manager.backup_status(agent_id, status_file)

        current_status = json.loads(status_file.read_text(encoding="utf-8"))
        valid, errors = validator.validate_status_json(current_status)
        if not valid:
            return ResetResult(False, f"Invalid current status: {', '.join(errors)}", backup_file)

        reset_status, archived_data = generate_reset_status(current_status, snapshot_timestamp)
        valid, errors = validator.validate_status_json(reset_status)
        if not valid:
            return ResetResult(False, f"Invalid reset status: {', '.join(errors)}", backup_file)

        temp_file = status_file.with_suffix(".json.tmp")
        temp_file.write_text(json.dumps(reset_status, indent=2, ensure_ascii=False), encoding="utf-8")
        temp_file.replace(status_file)

        final_status = json.loads(status_file.read_text(encoding="utf-8"))
        valid, errors = validator.validate_status_json(final_status)
        if not valid:
            if backup_file:
                shutil.copy(backup_file, status_file)
            return ResetResult(False, f"Final validation failed: {', '.join(errors)}", backup_file)

        snapshot_data.setdefault("agent_archives", {})[agent_id] = archived_data

        logger.info("Successfully reset %s status", agent_id)
        return ResetResult(True, None, backup_file, archived_data)

    except json.JSONDecodeError as exc:
        if backup_file:
            shutil.copy(backup_file, status_file)
        return ResetResult(False, f"JSON decode error: {exc}", backup_file)

    except Exception as exc:  # pragma: no cover - defensive
        if backup_file:
            shutil.copy(backup_file, status_file)
        logger.error("Reset failed for %s: %s", agent_id, exc)
        return ResetResult(False, str(exc), backup_file)


def reset_all_agent_status(
    snapshot_data: Dict[str, Any],
    workspace_root: Path,
    snapshot_timestamp: datetime,
    agent_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Reset all agent status.json files safely."""
    if agent_ids is None:
        agent_ids = [f"Agent-{i}" for i in range(1, 9)]

    results: Dict[str, Any] = {
        "agents_reset": [],
        "agents_failed": [],
        "reset_timestamp": snapshot_timestamp.isoformat(),
        "reset_errors": [],
        "backup_files": {},
    }

    for agent_id in agent_ids:
        result = reset_agent_status_safely(agent_id, snapshot_data, workspace_root, snapshot_timestamp)
        if result.success:
            results["agents_reset"].append(agent_id)
        else:
            results["agents_failed"].append(agent_id)
            if result.error:
                results["reset_errors"].append({"agent_id": agent_id, "error": result.error})

        if result.backup_file:
            results["backup_files"][agent_id] = str(result.backup_file)

    StatusBackupManager(workspace_root).cleanup_old_backups()
    snapshot_data.setdefault("snapshot_metadata", {})["reset_status"] = results

    return results
