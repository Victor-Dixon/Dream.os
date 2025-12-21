#!/usr/bin/env python3
"""
Self-Healing Helpers
====================

Helper utilities for self-healing system:
- Cancellation tracking management
- Coordinate loading
- Healing history management

<!-- SSOT Domain: infrastructure -->

V2 Compliance: <300 lines | Author: Agent-3 | Date: 2025-12-15
"""

import json
import logging
from datetime import date
from pathlib import Path
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def load_agent_coordinates() -> Dict[str, Tuple[int, int]]:
    """Load agent chat input coordinates from SSOT."""
    coordinates: Dict[str, Tuple[int, int]] = {}
    try:
        coord_file = Path("cursor_agent_coords.json")
        if coord_file.exists():
            data = json.loads(coord_file.read_text(encoding="utf-8"))
            for agent_id, info in data.get("agents", {}).items():
                coords = info.get("chat_input_coordinates")
                if coords and len(coords) == 2:
                    coordinates[agent_id] = (coords[0], coords[1])
            logger.info(f"Loaded coordinates for {len(coordinates)} agents")
    except Exception as e:
        logger.error(f"Error loading coordinates: {e}")
    return coordinates


def load_cancellation_tracking() -> Dict[str, Dict[str, int]]:
    """Load terminal cancellation tracking data."""
    tracking_file = Path(
        "agent_workspaces/.terminal_cancellation_tracking.json")
    try:
        if tracking_file.exists():
            with open(tracking_file, 'r') as f:
                data = json.load(f)
                today = date.today().isoformat()
                return {
                    agent_id: {today: counts.get(today, 0)}
                    for agent_id, counts in data.items()
                    if today in counts
                }
        return {}
    except Exception as e:
        logger.error(f"Error loading cancellation tracking: {e}")
        return {}


def save_cancellation_tracking(counts: Dict[str, Dict[str, int]]) -> None:
    """Save terminal cancellation tracking data."""
    tracking_file = Path(
        "agent_workspaces/.terminal_cancellation_tracking.json")
    try:
        tracking_file.parent.mkdir(parents=True, exist_ok=True)
        with open(tracking_file, 'w') as f:
            json.dump(counts, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving cancellation tracking: {e}")


def record_cancellation(
    counts: Dict[str, Dict[str, int]],
    agent_id: str
) -> int:
    """Record terminal cancellation and return count for today."""
    today = date.today().isoformat()
    if agent_id not in counts:
        counts[agent_id] = {}
    if today not in counts[agent_id]:
        counts[agent_id][today] = 0
    counts[agent_id][today] += 1
    save_cancellation_tracking(counts)
    return counts[agent_id][today]


def get_cancellation_count_today(
    counts: Dict[str, Dict[str, int]],
    agent_id: str
) -> int:
    """Get terminal cancellation count for agent today."""
    today = date.today().isoformat()
    return counts.get(agent_id, {}).get(today, 0)


def calculate_healing_stats(
    healing_history: list,
    recovery_attempts: Dict[str, int],
    agent_ids: list,
    get_cancel_count: callable,
) -> Dict[str, any]:
    """Calculate healing statistics."""
    successful = sum(1 for a in healing_history if a.success)
    failed = sum(1 for a in healing_history if not a.success)

    by_agent: Dict[str, Dict[str, int]] = {}
    for action in healing_history:
        if action.agent_id not in by_agent:
            by_agent[action.agent_id] = {
                "total": 0, "successful": 0, "failed": 0}
        by_agent[action.agent_id]["total"] += 1
        if action.success:
            by_agent[action.agent_id]["successful"] += 1
        else:
            by_agent[action.agent_id]["failed"] += 1

    cancellation_counts = {
        agent_id: get_cancel_count(agent_id)
        for agent_id in agent_ids
    }

    return {
        "total_actions": len(healing_history),
        "successful": successful,
        "failed": failed,
        "success_rate": (successful / len(healing_history) * 100) if healing_history else 0.0,
        "by_agent": by_agent,
        "recovery_attempts": recovery_attempts.copy(),
        "terminal_cancellations_today": cancellation_counts,
        "recent_actions": [
            {
                "agent_id": a.agent_id,
                "action": a.action_type,
                "reason": a.reason,
                "success": a.success,
                "timestamp": a.timestamp.isoformat(),
            }
            for a in healing_history[-10:]
        ],
    }
