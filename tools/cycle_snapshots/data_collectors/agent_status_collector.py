"""
Agent Status Collector
======================

Collects agent status.json files safely.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: tools -->
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)


def validate_status_json(status: Dict[str, Any]) -> bool:
    """
    Validate status.json structure and content.
    
    Args:
        status: Status dictionary to validate
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["agent_id", "agent_name", "status"]
    
    for field in required_fields:
        if field not in status:
            logger.warning(f"Missing required field in status.json: {field}")
            return False
    
    # Validate JSON is serializable
    try:
        json.dumps(status)
    except (TypeError, ValueError) as e:
        logger.error(f"Status JSON not serializable: {e}")
        return False
    
    return True


def collect_agent_status(
    agent_id: str,
    workspace_root: Path
) -> Optional[Dict[str, Any]]:
    """
    Collect status for a specific agent.
    
    Args:
        agent_id: Agent ID (e.g., "Agent-1", "Agent-2")
        workspace_root: Root workspace path
    
    Returns:
        Agent status dict or None if not found/invalid
    """
    status_file = workspace_root / "agent_workspaces" / agent_id / "status.json"
    
    if not status_file.exists():
        logger.debug(f"Status file not found for {agent_id}: {status_file}")
        return None
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        if not validate_status_json(status):
            logger.warning(f"Invalid status.json for {agent_id}")
            return None
        
        return status
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {agent_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading status for {agent_id}: {e}")
        return None


def collect_all_agent_status(
    workspace_root: Path,
    agent_ids: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Collect status from all active agents.
    
    Args:
        workspace_root: Root workspace path
        agent_ids: List of agent IDs to collect (defaults to Agent-1 through Agent-8)
    
    Returns:
        Dict mapping agent_id to status data
    """
    if agent_ids is None:
        agent_ids = [f"Agent-{i}" for i in range(1, 9)]
    
    agents = {}
    
    for agent_id in agent_ids:
        status = collect_agent_status(agent_id, workspace_root)
        if status:
            agents[agent_id] = status
    
    return agents

