#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Jet Fuel Optimizer - Gas Timing Optimization
===========================================

Optimizes gas timing based on agent velocity and performance.
"""

from typing import Tuple
from src.swarm_brain.swarm_memory import SwarmMemory

from .pipeline import AutoGasPipelineSystem
from ..stages.progress_monitor import read_agent_status


class JetFuelOptimizer:
    """
    💡 SOPHISTICATED SOLUTION: Not just gas, but JET FUEL!

    Analyzes agent performance → Optimizes gas timing → Predicts needs → Prevents stalls!
    """

    def __init__(self, pipeline: AutoGasPipelineSystem):
        self.pipeline = pipeline
        self.swarm_memory = SwarmMemory(agent_id='JetFuelOptimizer')
        self.agent_velocity = {}  # Track agent speed
        self.agent_quality = {}   # Track agent quality

    def analyze_agent_velocity(self, agent_id: str) -> float:
        """
        Calculate agent's execution velocity (repos per cycle).

        Fast agents: Get gas earlier (70% instead of 75%)
        Slow agents: Get gas later (85% to ensure they're really close)
        """
        status = read_agent_status(agent_id, self.pipeline.workspace_path)
        if not status:
            return 1.0  # Default velocity

        # Calculate based on timestamp patterns
        last_updated = status.get('last_updated', '')
        # Parse completed_tasks timestamps...
        # (Simplified for now - return default)

        return 1.0  # repos per cycle

    def predict_optimal_gas_timing(self, agent_id: str) -> Tuple[float, float, float]:
        """
        🧠 PREDICTIVE GAS TIMING

        Instead of fixed 75%, 90%, 100%:
        - Analyze agent velocity
        - Predict when they'll finish
        - Send gas EARLIER for fast agents
        - Send gas LATER for methodical agents

        Returns: (primary%, safety%, completion%) optimized for agent
        """
        velocity = self.analyze_agent_velocity(agent_id)

        if velocity > 1.5:  # Fast agent
            return (70.0, 85.0, 100.0)  # Send earlier!
        elif velocity < 0.7:  # Methodical agent
            return (80.0, 92.0, 100.0)  # Send later (they're thorough)
        else:  # Average agent
            return (75.0, 90.0, 100.0)  # Standard timing

    def create_jet_fuel_message(self, agent_id: str, next_agent: str, progress: float) -> str:
        """
        💎 JET FUEL vs Regular Gas

        Jet fuel includes:
        - Context from previous agent's learnings
        - Resources needed for upcoming work
        - Quality standards to apply
        - Expected completion time
        - Strategic priorities

        Result: Next agent starts with EVERYTHING they need!
        """
        # Get learnings from current agent
        learnings = self._get_agent_learnings(agent_id)

        # Get resources for next agent
        resources = self._get_recommended_resources(next_agent)

        next_agent_info = self.pipeline.agents.get(next_agent)
        repos_assigned = next_agent_info.repos_assigned if next_agent_info else (
            0, 0)

        # Build JET FUEL message (not just gas!)
        message = f"""🚀 JET FUEL DELIVERY: {next_agent}!

AUTOMATED PIPELINE HANDOFF:
- Previous agent: {agent_id} ({progress:.1f}% complete)
- Your mission: {repos_assigned}

🔥 JET FUEL INCLUDES:

📚 LEARNINGS FROM {agent_id}:
{learnings}

🛠️ RESOURCES FOR YOUR MISSION:
{resources}

📊 QUALITY STANDARDS:
- Use: docs/standards/REPO_ANALYSIS_STANDARD_AGENT6.md
- Target: 90% hidden value discovery rate
- Method: 6-phase framework
- Send gas at 75-80% to keep pipeline flowing!

⏱️ EXPECTED COMPLETION:
- Start: NOW
- Send gas to next: At 75-80%
- Complete: Within X cycles

🎯 STRATEGIC PRIORITIES:
- Find JACKPOTS (mission-solving discoveries)
- Discover professional patterns
- Map integration opportunities
- Maintain pipeline (send gas early!)

This is JET FUEL - not just gas, but everything you need to EXCEL! 🚀

AUTO-DELIVERED BY PIPELINE SYSTEM - PERPETUAL MOTION ENGAGED!
"""

        return message

    def _get_agent_learnings(self, agent_id: str) -> str:
        """Extract key learnings from agent's completed work."""
        # Query Swarm Brain for agent's recent learnings
        results = self.swarm_memory.search_swarm_knowledge(
            f"{agent_id} repo analysis")

        if results:
            # Summarize top 3 learnings
            return "- " + "\n- ".join([r.get('content', '')[:100] for r in results[:3]])

        return "- Pattern > Content\n- Architecture > Features\n- Professional > Popular"

    def _get_recommended_resources(self, agent_id: str) -> str:
        """Get recommended resources for next agent."""
        return f"""- Swarm Brain: memory.search_swarm_knowledge('hidden value')
- Analysis Standard: docs/standards/REPO_ANALYSIS_STANDARD_AGENT6.md
- Pipeline Protocol: docs/protocols/PROMPTS_ARE_GAS_PIPELINE_PROTOCOL.md
- Agent-6 Examples: agent_workspaces/Agent-6/devlogs/"""
