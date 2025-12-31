#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->
Smart Assignment Optimizer - Swarm Brain + Markov Chain
========================================================

Intelligent agent assignment using Swarm Brain knowledge and Markov chain
performance history to optimize violation and task assignments.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-09
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class SmartAssignmentOptimizer:
    """Smart assignment using Swarm Brain + Markov optimizer."""

    def __init__(self):
        """Initialize optimizer with Swarm Brain and Markov chain."""
        try:
            from src.swarm_brain.swarm_memory import SwarmMemory

            self.swarm_memory = SwarmMemory(agent_id="GaslineHub")
        except Exception as e:
            logger.warning(f"Swarm Brain unavailable: {e}")
            self.swarm_memory = None

        # Agent specializations (base knowledge)
        self.agent_specializations = {
            "Agent-1": ["testing", "qa", "integration", "core_systems"],
            "Agent-2": ["architecture", "v2_compliance", "design", "patterns"],
            "Agent-3": ["infrastructure", "monitoring", "devops", "deployment"],
            "Agent-5": ["memory", "performance", "business_intelligence", "analytics"],
            "Agent-6": ["optimization", "planning", "coordination", "communication"],
            "Agent-7": ["web", "frontend", "ui", "web_development"],
            "Agent-8": ["autonomous", "qa", "ssot", "system_integration"],
        }

        # Markov chain state (agent performance history)
        self.markov_chain = self._initialize_markov_chain()

    def _initialize_markov_chain(self) -> Dict[str, Dict[str, float]]:
        """Initialize Markov chain with agent performance probabilities."""
        # Start with equal probabilities, will be updated based on history
        agents = list(self.agent_specializations.keys())
        chain = {}

        for agent in agents:
            chain[agent] = {
                "success_rate": 0.5,  # Default 50% success
                "avg_completion_time": 1.0,  # Normalized time
                "specialization_match": 0.5,  # Default match score
            }

        # Try to load historical data from Swarm Brain
        if self.swarm_memory:
            try:
                history = self.swarm_memory.search_swarm_knowledge(
                    "agent performance history violations"
                )
                # Update chain based on history if available
                # (Simplified - would need more sophisticated parsing)
            except Exception:
                pass

        return chain

    def assign_violations(self, violations: List[Dict]) -> Dict[str, List[Dict]]:
        """Assign violations to agents using smart assignment algorithm."""
        assignments = {}

        # Score each agent for each violation
        for violation in violations:
            best_agent = self._find_best_agent_for_violation(violation)

            if best_agent not in assignments:
                assignments[best_agent] = []
            assignments[best_agent].append(violation)

        # Balance workload (ensure no agent is overloaded)
        assignments = self._balance_workload(assignments, len(violations))

        return assignments

    def _find_best_agent_for_violation(self, violation: Dict) -> str:
        """Find best agent for a violation using scoring algorithm."""
        violation_type = violation.get("type", "unknown").lower()
        violation_file = violation.get("file", "").lower()
        violation_complexity = violation.get("complexity", 0)

        agent_scores = {}

        for agent_id, specializations in self.agent_specializations.items():
            score = 0.0

            # 1. Specialization match (40% weight)
            specialization_score = self._calculate_specialization_match(
                violation_type, violation_file, specializations
            )
            score += specialization_score * 0.4

            # 2. Markov chain performance (30% weight)
            markov_score = self._calculate_markov_score(agent_id, violation_type)
            score += markov_score * 0.3

            # 3. Swarm Brain knowledge (20% weight)
            brain_score = self._calculate_brain_score(agent_id, violation_type)
            score += brain_score * 0.2

            # 4. Current workload (10% weight) - prefer less loaded agents
            workload_score = self._calculate_workload_score(agent_id)
            score += workload_score * 0.1

            agent_scores[agent_id] = score

        # Return agent with highest score
        best_agent = max(agent_scores, key=agent_scores.get)
        logger.debug(
            f"Assigned violation to {best_agent} (score: {agent_scores[best_agent]:.2f})"
        )
        return best_agent

    def _calculate_specialization_match(
        self, violation_type: str, violation_file: str, specializations: List[str]
    ) -> float:
        """Calculate how well agent specializations match violation."""
        match_score = 0.0

        # Check if violation type matches any specialization
        for spec in specializations:
            if spec.lower() in violation_type or violation_type in spec.lower():
                match_score += 0.5
            if spec.lower() in violation_file or violation_file in spec.lower():
                match_score += 0.3

        # Normalize to 0-1
        return min(1.0, match_score)

    def _calculate_markov_score(self, agent_id: str, violation_type: str) -> float:
        """Calculate score based on Markov chain (agent performance history)."""
        if agent_id not in self.markov_chain:
            return 0.5  # Default score

        chain_data = self.markov_chain[agent_id]

        # Combine success rate and specialization match
        score = (
            chain_data["success_rate"] * 0.6
            + chain_data["specialization_match"] * 0.4
        )

        return score

    def _calculate_brain_score(self, agent_id: str, violation_type: str) -> float:
        """Calculate score based on Swarm Brain knowledge."""
        if not self.swarm_memory:
            return 0.5  # Default if Swarm Brain unavailable

        try:
            # Search for agent's past performance on similar violations
            query = f"{agent_id} {violation_type} performance success"
            results = self.swarm_memory.search_swarm_knowledge(query)

            if results:
                # If found in brain, boost score
                return 0.8
            else:
                # No history found, neutral score
                return 0.5
        except Exception:
            return 0.5

    def _calculate_workload_score(self, agent_id: str) -> float:
        """Calculate score based on current agent workload."""
        try:
            from src.discord_commander.status_reader import StatusReader

            status_reader = StatusReader()
            agent_status = status_reader.read_agent_status(agent_id)

            if agent_status:
                current_tasks = len(agent_status.get("current_tasks", []))
                # Prefer agents with fewer current tasks
                # Score decreases as tasks increase
                if current_tasks == 0:
                    return 1.0
                elif current_tasks <= 2:
                    return 0.8
                elif current_tasks <= 5:
                    return 0.5
                else:
                    return 0.2

            return 0.5  # Default if status unavailable
        except Exception:
            return 0.5

    def _balance_workload(
        self, assignments: Dict[str, List[Dict]], total_violations: int
    ) -> Dict[str, List[Dict]]:
        """Balance workload across agents to prevent overload."""
        if not assignments:
            return assignments

        agents = list(assignments.keys())
        avg_per_agent = total_violations / len(agents) if agents else 0
        max_per_agent = int(avg_per_agent * 1.5)  # Allow 50% over average

        # Redistribute if any agent is overloaded
        balanced = {}
        overflow = []

        for agent_id, violations in assignments.items():
            if len(violations) > max_per_agent:
                # Keep max_per_agent, move rest to overflow
                balanced[agent_id] = violations[:max_per_agent]
                overflow.extend(violations[max_per_agent:])
            else:
                balanced[agent_id] = violations

        # Redistribute overflow to less loaded agents
        if overflow:
            for violation in overflow:
                # Find agent with least violations
                least_loaded = min(
                    balanced.keys(), key=lambda a: len(balanced.get(a, []))
                )
                if least_loaded not in balanced:
                    balanced[least_loaded] = []
                balanced[least_loaded].append(violation)

        return balanced


__all__ = ["SmartAssignmentOptimizer"]

