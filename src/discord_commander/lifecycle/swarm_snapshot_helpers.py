#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Swarm Snapshot Helpers
======================

Helper functions for generating swarm snapshots.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import json
import logging
from pathlib import Path


def get_swarm_snapshot(logger: logging.Logger) -> dict:
    """Get current swarm work snapshot."""
    snapshot = {
        "active_agents": [],
        "recent_activity": [],
        "current_focus": [],
        "engagement_rate": 0.0,
    }

    try:
        workspace_root = Path("agent_workspaces")
        active_count = _process_agent_statuses(workspace_root, snapshot, logger)
        snapshot["engagement_rate"] = (active_count / 8 * 100) if active_count > 0 else 0.0
    except Exception as e:
        logger.warning(f"Error getting swarm snapshot: {e}")

    return snapshot


def _process_agent_statuses(workspace_root: Path, snapshot: dict, logger: logging.Logger) -> int:
    """Process all agent status files and update snapshot."""
    active_count = 0
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        status_file = workspace_root / agent_id / "status.json"

        if not status_file.exists():
            continue

        try:
            agent_data = _load_agent_status(status_file, logger)
            if agent_data and agent_data.get("is_active"):
                active_count += 1
                snapshot["active_agents"].append(agent_data["agent_info"])
                if agent_data.get("recent_activity"):
                    snapshot["recent_activity"].append(agent_data["recent_activity"])
                if agent_data.get("current_focus"):
                    snapshot["current_focus"].append(agent_data["current_focus"])
        except Exception as e:
            logger.debug(f"Error reading status for {agent_id}: {e}")
            continue

    return active_count


def _load_agent_status(status_file: Path, logger: logging.Logger) -> dict | None:
    """Load and process agent status file."""
    with open(status_file, 'r', encoding='utf-8') as f:
        status = json.load(f)

    agent_status = status.get("status", "")
    if "ACTIVE" not in agent_status.upper():
        return None

    agent_id = status_file.parent.name
    agent_info = _build_agent_info(agent_id, status)
    recent_activity = _extract_recent_activity(agent_id, status)
    current_focus = _extract_current_focus(agent_id, status)

    return {
        "is_active": True,
        "agent_info": agent_info,
        "recent_activity": recent_activity,
        "current_focus": current_focus,
    }


def _build_agent_info(agent_id: str, status: dict) -> dict:
    """Build agent info dictionary."""
    return {
        "id": agent_id,
        "mission": status.get("current_mission", "No active mission")[:80],
        "phase": status.get("current_phase", "Unknown"),
        "priority": status.get("mission_priority", "MEDIUM"),
    }


def _extract_recent_activity(agent_id: str, status: dict) -> str | None:
    """Extract recent activity from status."""
    completed = status.get("completed_tasks", [])
    if completed:
        recent = completed[0][:100] if isinstance(completed[0], str) else str(completed[0])[:100]
        return f"{agent_id}: {recent}"
    return None


def _extract_current_focus(agent_id: str, status: dict) -> str | None:
    """Extract current focus from status."""
    current_tasks = status.get("current_tasks", [])
    if current_tasks:
        focus = current_tasks[0][:80] if isinstance(current_tasks[0], str) else str(current_tasks[0])[:80]
        return f"{agent_id}: {focus}"
    return None

