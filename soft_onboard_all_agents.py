<<<<<<< HEAD
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
=======
#!/usr/bin/env python3
"""
Soft Onboard All Agents - Swarm Coordination Script
===================================================

Executes soft onboarding protocol for all 8 agents in the swarm.
Uses the refactored soft onboarding service with proper keyboard locking.

Agents: Agent-1 through Agent-8 (as per agent_mode_config.json)
Protocol: 6-step soft onboarding with messaging fallback
Safety: Keyboard control lock prevents interference between agents

Usage: python soft_onboard_all_agents.py
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "src"))

from src.services.onboarding.soft.service import soft_onboard_multiple_agents
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Execute soft onboarding for all agents."""

    print("🚀 SOFT ONBOARDING ALL AGENTS")
    print("=" * 50)

    # Get agent configuration
    try:
        config_path = project_root / "agent_mode_config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)

        current_mode = config.get("current_mode", "8-agent")
        active_agents = config.get("modes", {}).get(current_mode, {}).get("active_agents", [])

        if not active_agents:
            logger.error("❌ No active agents found in configuration")
            return 1

        logger.info(f"📋 Found {len(active_agents)} active agents in mode '{current_mode}': {active_agents}")

    except Exception as e:
        logger.warning(f"⚠️ Could not load config, using default 8-agent configuration: {e}")
        # Fallback to default 8-agent configuration
        active_agents = [f"Agent-{i}" for i in range(1, 9)]

    # Prepare agent list for soft onboarding
    # Each agent gets (agent_id, onboarding_message) tuple
    # Using None for onboarding_message means it will use the default message
    agents_to_onboard = [(agent_id, None) for agent_id in active_agents]

    print(f"🎯 Preparing to soft onboard {len(agents_to_onboard)} agents:")
    for agent_id, _ in agents_to_onboard:
        print(f"  • {agent_id}")

    print("\n⚡ Starting soft onboarding sequence...")
    print("This will execute 6 steps per agent with proper keyboard locking.")
    print("Total time estimate: ~2-3 minutes per agent")
    print()

    try:
        # Execute soft onboarding for all agents
        results = soft_onboard_multiple_agents(
            agents=agents_to_onboard,
            role=None,  # Let agents determine their own roles
            generate_cycle_report=True  # Generate cycle accomplishments report after completion
        )

        # Report results
        print("\n" + "=" * 50)
        print("📊 SOFT ONBOARDING RESULTS")
        print("=" * 50)

        successful = []
        failed = []

        for agent_id, success in results.items():
            if success:
                successful.append(agent_id)
                print(f"✅ {agent_id}: Successfully onboarded")
            else:
                failed.append(agent_id)
                print(f"❌ {agent_id}: Onboarding failed")

        print("\n" + "=" * 50)
        print("🎉 SOFT ONBOARDING COMPLETE")
        print("=" * 50)
        print(f"✅ Successful: {len(successful)} agents")
        print(f"❌ Failed: {len(failed)} agents")
        print(f"📊 Success Rate: {len(successful)}/{len(active_agents)} ({len(successful)/len(active_agents)*100:.1f}%)")

        if successful:
            print(f"\n🟢 Successfully onboarded agents: {', '.join(successful)}")

        if failed:
            print(f"\n🔴 Failed agents: {', '.join(failed)}")
            print("Check logs for failure details and retry individual agents if needed.")

        print("\n📋 Next Steps:")
        print("1. Check agent workspaces for new inbox messages")
        print("2. Verify agent status.json files are updated")
        print("3. Monitor Discord for agent activity reports")
        print("4. Review cycle accomplishments report")

        return 0 if len(failed) == 0 else 1

    except KeyboardInterrupt:
        print("\n⚠️ Soft onboarding interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Soft onboarding failed with error: {e}")
        return 1

if __name__ == "__main__":
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    sys.exit(main())