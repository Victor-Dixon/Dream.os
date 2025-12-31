"""
Data Collector Module
=====================

Collects agent status data from all agent workspaces.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-30
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_agent_status(agent_id: str, workspace_root: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Load status for a specific agent.
    
    Args:
        agent_id: Agent ID (e.g., "1", "2", "3")
        workspace_root: Root workspace path (defaults to current directory)
    
    Returns:
        Agent status dict or None if not found
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    
    status_file = workspace_root / "agent_workspaces" / f"Agent-{agent_id}" / "status.json"
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️  Warning: Could not load status for Agent-{agent_id}: {e}")
        return None


def collect_all_agent_status(workspace_root: Optional[Path] = None, agent_ids: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """
    Collect status from all active agents.
    
    Args:
        workspace_root: Root workspace path (defaults to current directory)
        agent_ids: List of agent IDs to collect (defaults to 1-8)
    
    Returns:
        Dict mapping agent_id to status data
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    
    if agent_ids is None:
        agent_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]
    
    agents = {}
    
    for agent_id in agent_ids:
        status = load_agent_status(agent_id, workspace_root)
        if status:
            agents[f"Agent-{agent_id}"] = status
    
    return agents


def calculate_totals(agents: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    """
    Calculate aggregate statistics from agent data.
    
    Args:
        agents: Dict of agent_id -> status data
    
    Returns:
        Dict with totals: agents, completed_tasks, achievements, active_tasks
    """
    total_agents = len(agents)
    total_completed_tasks = sum(len(status.get('completed_tasks', [])) for status in agents.values())
    total_achievements = sum(len(status.get('achievements', [])) for status in agents.values())
    
    # Count active tasks
    active_tasks = []
    for agent_id, status in agents.items():
        tasks = status.get('current_tasks', [])
        if isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, dict) and task.get('status') in ['in_progress', 'active', 'coordination_active']:
                    active_tasks.append({
                        'agent': agent_id,
                        'task': task.get('task', 'Unknown'),
                        'status': task.get('status', 'Unknown')
                    })
    
    return {
        'total_agents': total_agents,
        'total_completed_tasks': total_completed_tasks,
        'total_achievements': total_achievements,
        'active_tasks_count': len(active_tasks),
        'active_tasks': active_tasks
    }

