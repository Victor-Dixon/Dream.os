"""
Agent Status Collector for Cycle Snapshot System
===============================================

Collects agent status.json files safely for cycle snapshots.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, functions <30 lines)
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


def collect_all_agent_status(workspace_root: Path) -> Dict[str, Dict]:
    """
    Collect status.json files from all agents safely.

    Args:
        workspace_root: Path to workspace root directory

    Returns:
        Dict mapping agent_id to status data
    """
    all_status = {}

    # Agent mapping from architecture constants
    agents = {
        "Agent-1": "Integration & Core Systems",
        "Agent-2": "Architecture & Design",
        "Agent-3": "Infrastructure & DevOps",
        "Agent-4": "Captain (Strategic Oversight)",
        "Agent-5": "Business Intelligence",
        "Agent-6": "Coordination & Communication",
        "Agent-7": "Web Development",
        "Agent-8": "SSOT & System Integration"
    }

    for agent_id in agents.keys():
        status = collect_agent_status(agent_id, workspace_root)
        if status:
            all_status[agent_id] = status
        else:
            logger.warning(f"Failed to collect status for {agent_id}")
            all_status[agent_id] = {"error": f"Failed to collect status for {agent_id}"}

    return all_status


def collect_agent_status(agent_id: str, workspace_root: Path) -> Optional[Dict]:
    """
    Collect status.json for a specific agent.

    Args:
        agent_id: Agent identifier (e.g., 'Agent-3')
        workspace_root: Path to workspace root directory

    Returns:
        Status data dict or None if collection failed
    """
    status_file = workspace_root / "agent_workspaces" / agent_id / "status.json"

    try:
        if not status_file.exists():
            logger.warning(f"No status file found for {agent_id}")
            return None

        with open(status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)

        # Validate the status data
        if validate_status_json(status):
            return status
        else:
            logger.warning(f"Invalid status.json structure for {agent_id}")
            return None

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in status file for {agent_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error collecting status for {agent_id}: {e}")
        return None


def validate_status_json(status: Dict) -> bool:
    """
    Validate status.json structure and required fields.
    Handles different status.json formats flexibly.

    Args:
        status: Status data to validate

    Returns:
        True if valid, False otherwise
    """
    # Only require agent_id - be flexible with other fields
    if "agent_id" not in status:
        logger.error("Missing required field 'agent_id' in status.json")
        return False

    try:
        # Validate agent_id format
        agent_id = status.get("agent_id", "")
        if not agent_id.startswith("Agent-"):
            logger.error(f"Invalid agent_id format: {agent_id}")
            return False

        # Optional validations with warnings only
        if "status" in status:
            valid_statuses = ["active", "inactive", "onboarding", "ACTIVE_AGENT_MODE", "IDLE", "ERROR"]
            if status.get("status") not in valid_statuses:
                logger.warning(f"Unexpected status value: {status.get('status')}")

        # Log available fields for debugging
        logger.debug(f"Status fields for {agent_id}: {list(status.keys())}")

        return True

    except Exception as e:
        logger.error(f"Status validation error: {e}")
        return False