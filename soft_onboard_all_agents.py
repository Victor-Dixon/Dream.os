#!/usr/bin/env python3
"""
Soft Onboard All Agents Script
==============================

Script to soft onboard all agents in the system (Agent-1 through Agent-8).
Uses the unified soft onboarding service to perform 6-step soft onboarding
protocol for each agent sequentially.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-11
"""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.soft_onboarding_service import soft_onboard_multiple_agents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function to soft onboard all agents."""
    logger.info("🚀 Starting soft onboarding for all agents...")

    # Define all agents (Agent-1 through Agent-8)
    all_agents = [f"Agent-{i}" for i in range(1, 9)]
    logger.info(f"📋 Agents to onboard: {', '.join(all_agents)}")

    # Create agent tuples with None for messages (use defaults)
    agents_tuples = [(agent, None) for agent in all_agents]

    try:
        # Execute soft onboarding for all agents
        logger.info("🎯 Initiating soft onboarding protocol for all agents...")
        results = soft_onboard_multiple_agents(
            agents_tuples,
            role=None,  # Use default roles
            generate_cycle_report=True  # Generate accomplishments report after onboarding
        )

        # Analyze results
        successful = [agent for agent, success in results.items() if success]
        failed = [agent for agent, success in results.items() if not success]

        logger.info("📊 Soft onboarding results:")
        logger.info(f"✅ Successful: {len(successful)} agents - {', '.join(successful)}")
        if failed:
            logger.error(f"❌ Failed: {len(failed)} agents - {', '.join(failed)}")
            return 1
        else:
            logger.info("🎉 All agents successfully soft onboarded!")
            return 0

    except Exception as e:
        logger.error(f"❌ Soft onboarding execution failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())