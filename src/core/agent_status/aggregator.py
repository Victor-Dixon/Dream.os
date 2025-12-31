"""
Agent Status Aggregator
=======================

Swarm state aggregation from all agent status.json files.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: core -->
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from .reader import AgentStatusReader, read_all_agent_status

logger = logging.getLogger(__name__)


class SwarmStateAggregator:
    """
    Aggregates agent status.json files into unified swarm state.
    
    Pure utility - no Discord dependencies, uses unified reader library.
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize swarm state aggregator.
        
        Args:
            workspace_root: Root workspace path (defaults to current directory)
        """
        if workspace_root is None:
            workspace_root = Path.cwd()
        self.workspace_root = Path(workspace_root)
        self.reader = AgentStatusReader(workspace_root=workspace_root)
    
    def aggregate_swarm_state(
        self,
        agent_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Aggregate complete swarm state from all agents.
        
        Args:
            agent_ids: List of agent IDs to aggregate (default: Agent-1 through Agent-8)
        
        Returns:
            Swarm state dictionary with agents, metrics, and summary
        """
        if agent_ids is None:
            agent_ids = [f"Agent-{i}" for i in range(1, 9)]
        
        swarm_state: Dict[str, Any] = {
            "agents": {},
            "active_missions": [],
            "completed_today": [],
            "total_points": 0,
            "summary": {},
        }
        
        try:
            # Read all agent statuses using unified reader
            all_statuses = read_all_agent_status(
                workspace_root=self.workspace_root,
                agent_ids=agent_ids
            )
            
            for agent_id, status in all_statuses.items():
                swarm_state["agents"][agent_id] = status
                
                # Track active missions
                mission = status.get("current_mission", "")
                if mission and "COMPLETE" not in mission.upper():
                    swarm_state["active_missions"].append({
                        "agent": agent_id,
                        "mission": mission,
                        "priority": status.get("mission_priority", "NORMAL")
                    })
                
                # Sum points
                points = status.get("points_earned", 0)
                if isinstance(points, (int, float)):
                    swarm_state["total_points"] += points
                
                # Track completed tasks today
                completed = status.get("completed_tasks", [])
                if completed:
                    swarm_state["completed_today"].extend([
                        {"agent": agent_id, "task": task}
                        for task in completed[-5:]  # Last 5 per agent
                    ])
            
            # Generate summary
            swarm_state["summary"] = self._generate_summary(swarm_state)
        
        except Exception as e:
            logger.error(f"Error aggregating swarm state: {e}")
            swarm_state["error"] = str(e)
        
        return swarm_state
    
    def _generate_summary(self, swarm_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate swarm state summary.
        
        Args:
            swarm_state: Aggregated swarm state
        
        Returns:
            Summary dictionary
        """
        return {
            "total_agents": len(swarm_state["agents"]),
            "active_missions_count": len(swarm_state["active_missions"]),
            "total_points": swarm_state["total_points"],
            "completed_tasks_count": len(swarm_state["completed_today"]),
            "agents_by_status": self._count_by_status(swarm_state["agents"]),
        }
    
    def _count_by_status(self, agents: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """
        Count agents by status.
        
        Args:
            agents: Dictionary of agent statuses
        
        Returns:
            Dictionary mapping status to count
        """
        status_counts: Dict[str, int] = {}
        for agent_status in agents.values():
            status = agent_status.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def get_active_missions(self) -> List[Dict[str, Any]]:
        """
        Get list of active missions across all agents.
        
        Returns:
            List of active mission dictionaries
        """
        swarm_state = self.aggregate_swarm_state()
        return swarm_state.get("active_missions", [])
    
    def get_agent_summary(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get summary for a specific agent.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1")
        
        Returns:
            Agent summary dictionary or None
        """
        status = self.reader.read_status(agent_id)
        if not status:
            return None
        
        return {
            "agent_id": agent_id,
            "agent_name": status.get("agent_name", "Unknown"),
            "status": status.get("status", "UNKNOWN"),
            "current_mission": status.get("current_mission", ""),
            "mission_priority": status.get("mission_priority", "NORMAL"),
            "cycle_count": status.get("cycle_count", 0),
            "completed_tasks_count": len(status.get("completed_tasks", [])),
            "current_tasks_count": len(status.get("current_tasks", [])),
            "points_earned": status.get("points_earned", 0),
        }


def aggregate_swarm_state(
    workspace_root: Optional[Path] = None,
    agent_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function to aggregate swarm state.
    
    Args:
        workspace_root: Root workspace path
        agent_ids: List of agent IDs to aggregate
    
    Returns:
        Swarm state dictionary
    """
    aggregator = SwarmStateAggregator(workspace_root=workspace_root)
    return aggregator.aggregate_swarm_state(agent_ids=agent_ids)

