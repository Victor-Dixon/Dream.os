"""
Agent Status Collector for Cycle Snapshot System
===============================================

Collects agent status.json files safely for cycle snapshots.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, functions <30 lines)
"""

import logging
from pathlib import Path
from typing import Dict, Optional, Any

from src.core.agent_status.reader import AgentStatusReader

logger = logging.getLogger(__name__)


def collect_all_agent_status(workspace_root: Path) -> Dict[str, Dict]:
    """
    Collect status.json files from all agents safely.

    Args:
        workspace_root: Path to workspace root directory

    Returns:
        Dict mapping agent_id to status data
    """
    reader = AgentStatusReader(workspace_root)
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
    reader = AgentStatusReader(workspace_root)

    try:
        status = reader.read_status(agent_id)
        if status:
            return status
        else:
            logger.warning(f"No status file found for {agent_id}")
            return None
    except Exception as e:
        logger.error(f"Error collecting status for {agent_id}: {e}")
        return None


def validate_status_json(status: Dict) -> bool:
    """
    Validate status.json structure and required fields.

    Args:
        status: Status data to validate

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["agent_id", "agent_name", "status", "fsm_state", "current_phase"]

    try:
        # Check required fields exist
        for field in required_fields:
            if field not in status:
                logger.error(f"Missing required field '{field}' in status.json")
                return False

        # Validate agent_id format
        agent_id = status.get("agent_id", "")
        if not agent_id.startswith("Agent-") or not agent_id[6:].isdigit():
            logger.error(f"Invalid agent_id format: {agent_id}")
            return False

        # Validate status field
        valid_statuses = ["ACTIVE_AGENT_MODE", "IDLE", "ERROR"]
        if status.get("status") not in valid_statuses:
            logger.warning(f"Unexpected status value: {status.get('status')}")

        # Validate FSM state
        valid_fsm_states = ["ACTIVE", "IDLE", "ERROR", "UNKNOWN"]
        if status.get("fsm_state") not in valid_fsm_states:
            logger.warning(f"Unexpected FSM state: {status.get('fsm_state')}")

        return True

    except Exception as e:
        logger.error(f"Status validation error: {e}")
        return False