"""
Agent Status Monitor Integration for Technical Debt
====================================================

Connects technical debt system to agent status monitor for intelligent task assignment.

Features:
- Agent capability matching for debt tasks
- Priority-based task assignment
- Status tracking integration
- Load balancing across agents

<!-- SSOT Domain: integration -->
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

from ..debt_tracker import TechnicalDebtTracker

# Import with proper path resolution
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))
from src.core.agent_status.aggregator import SwarmStateAggregator

logger = logging.getLogger(__name__)


class AgentStatusDebtIntegration:
    """
    Integrates technical debt system with agent status monitor.

    Enables intelligent assignment of debt reduction tasks based on:
    - Agent capabilities and expertise
    - Current workload and availability
    - Task priority and complexity
    - Historical performance
    """

    def __init__(self, debt_tracker: Optional[TechnicalDebtTracker] = None):
        """Initialize integration."""
        self.debt_tracker = debt_tracker or TechnicalDebtTracker()
        self.status_aggregator = SwarmStateAggregator()
        self.agent_capabilities = self._load_agent_capabilities()

    def _load_agent_capabilities(self) -> Dict[str, List[str]]:
        """Load agent capabilities for debt task assignment."""
        # Map agents to their technical debt reduction capabilities
        return {
            "Agent-1": ["integration", "architecture", "api", "refactoring"],
            "Agent-2": ["architecture", "design", "planning", "documentation"],
            "Agent-3": ["infrastructure", "deployment", "operations", "devops"],
            "Agent-4": ["testing", "validation", "qa", "automation"],
            "Agent-5": ["analytics", "reporting", "business_intelligence", "data"],
            "Agent-6": ["coordination", "communication", "messaging", "routing"],
            "Agent-7": ["web", "frontend", "ui", "user_experience"],
            "Agent-8": ["qa", "validation", "compliance", "system_integration"]
        }

    def get_available_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get agents available for debt task assignment."""
        try:
            swarm_state = self.status_aggregator.aggregate_swarm_state()
            available_agents = {}

            for agent_id, agent_data in swarm_state.get("agents", {}).items():
                # Check if agent is active and not overloaded
                if agent_data.get("status") == "active":
                    current_tasks = len(agent_data.get("current_tasks", []))
                    max_capacity = 3  # Max concurrent tasks per agent

                    if current_tasks < max_capacity:
                        available_agents[agent_id] = {
                            "capacity_remaining": max_capacity - current_tasks,
                            "capabilities": self.agent_capabilities.get(agent_id, []),
                            "current_workload": current_tasks,
                            "expertise_score": self._calculate_expertise_score(agent_id)
                        }

            return available_agents

        except Exception as e:
            logger.error(f"Failed to get available agents: {e}")
            return {}

    def _calculate_expertise_score(self, agent_id: str) -> float:
        """Calculate agent's expertise score for debt tasks."""
        # Simple scoring based on agent role and historical performance
        base_scores = {
            "Agent-1": 0.9,  # Integration specialist
            "Agent-2": 0.8,  # Architecture specialist
            "Agent-3": 0.9,  # Infrastructure specialist
            "Agent-4": 0.8,  # QA specialist
            "Agent-5": 0.8,  # Analytics specialist
            "Agent-6": 0.7,  # Coordination specialist
            "Agent-7": 0.7,  # Web specialist
            "Agent-8": 0.8   # QA/Integration specialist
        }
        return base_scores.get(agent_id, 0.6)

    def assign_debt_tasks(self) -> Dict[str, Any]:
        """
        Assign available debt tasks to agents based on capabilities and availability.

        Returns:
            Assignment results with tasks assigned and agents updated
        """
        try:
            # Get pending debt tasks
            pending_tasks = self._get_pending_debt_tasks()
            if not pending_tasks:
                return {"status": "no_tasks", "message": "No pending debt tasks"}

            # Get available agents
            available_agents = self.get_available_agents()
            if not available_agents:
                return {"status": "no_agents", "message": "No agents available for assignment"}

            assignments = []
            unassigned_tasks = []

            for task in pending_tasks:
                assigned_agent = self._find_best_agent_for_task(task, available_agents)

                if assigned_agent:
                    # Assign task to agent
                    assignment = self._assign_task_to_agent(task, assigned_agent)
                    assignments.append(assignment)

                    # Update agent capacity
                    available_agents[assigned_agent]["capacity_remaining"] -= 1
                else:
                    unassigned_tasks.append(task)

            return {
                "status": "completed",
                "assignments": assignments,
                "unassigned_tasks": unassigned_tasks,
                "total_tasks": len(pending_tasks),
                "assigned_count": len(assignments)
            }

        except Exception as e:
            logger.error(f"Debt task assignment failed: {e}")
            return {"status": "error", "message": str(e)}

    def _get_pending_debt_tasks(self) -> List[Dict[str, Any]]:
        """Get pending technical debt tasks."""
        debt_data = self.debt_tracker.debt_data
        pending_tasks = []

        for category_name, category_data in debt_data.get("categories", {}).items():
            pending_count = len(category_data.get("pending", []))
            if pending_count > 0:
                pending_tasks.append({
                    "category": category_name,
                    "pending_count": pending_count,
                    "priority": self._get_category_priority(category_name),
                    "required_capabilities": self._get_category_capabilities(category_name)
                })

        return pending_tasks

    def _get_category_priority(self, category: str) -> str:
        """Get priority level for debt category."""
        priority_map = {
            "file_deletion": "LOW",
            "integration": "HIGH",
            "implementation": "MEDIUM",
            "review": "MEDIUM",
            "output_flywheel": "HIGH",
            "test_validation": "MEDIUM",
            "todo_fixme": "LOW"
        }
        return priority_map.get(category, "MEDIUM")

    def _get_category_capabilities(self, category: str) -> List[str]:
        """Get required capabilities for debt category."""
        capability_map = {
            "file_deletion": ["infrastructure", "operations"],
            "integration": ["integration", "architecture", "api"],
            "implementation": ["integration", "refactoring"],
            "review": ["qa", "validation", "testing"],
            "output_flywheel": ["integration", "architecture"],
            "test_validation": ["qa", "validation", "testing"],
            "todo_fixme": ["coordination", "documentation"]
        }
        return capability_map.get(category, ["general"])

    def _find_best_agent_for_task(self, task: Dict[str, Any], available_agents: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """Find best agent for a debt task."""
        required_caps = task.get("required_capabilities", [])
        best_agent = None
        best_score = 0

        for agent_id, agent_data in available_agents.items():
            if agent_data["capacity_remaining"] <= 0:
                continue

            # Calculate match score
            agent_caps = agent_data.get("capabilities", [])
            capability_match = len(set(required_caps) & set(agent_caps)) / len(required_caps) if required_caps else 0.5

            expertise_score = agent_data.get("expertise_score", 0.5)
            capacity_score = agent_data["capacity_remaining"] / 3.0  # Normalize capacity

            total_score = (capability_match * 0.5) + (expertise_score * 0.3) + (capacity_score * 0.2)

            if total_score > best_score:
                best_score = total_score
                best_agent = agent_id

        return best_agent if best_score > 0.3 else None  # Minimum threshold

    def _assign_task_to_agent(self, task: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
        """Assign a debt task to an agent."""
        return {
            "task": task,
            "assigned_agent": agent_id,
            "timestamp": self.debt_tracker.debt_data.get("last_updated", ""),
            "priority": task.get("priority", "MEDIUM"),
            "capabilities_matched": task.get("required_capabilities", [])
        }

    def get_assignment_recommendations(self) -> Dict[str, Any]:
        """
        Get recommendations for debt task assignments without actually assigning.

        Returns:
            Recommendations for manual review and assignment
        """
        try:
            pending_tasks = self._get_pending_debt_tasks()
            available_agents = self.get_available_agents()

            recommendations = []

            for task in pending_tasks:
                best_agent = self._find_best_agent_for_task(task, available_agents.copy())
                if best_agent:
                    recommendations.append({
                        "task": task,
                        "recommended_agent": best_agent,
                        "confidence": "high",
                        "reasoning": f"Agent {best_agent} has matching capabilities and availability"
                    })

            return {
                "status": "success",
                "recommendations": recommendations,
                "total_tasks": len(pending_tasks),
                "recommended_count": len(recommendations)
            }

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return {"status": "error", "message": str(e)}