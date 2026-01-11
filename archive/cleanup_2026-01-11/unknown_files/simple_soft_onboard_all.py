#!/usr/bin/env python3
"""
Simple Soft Onboard All Agents - Direct Execution
=================================================

Direct execution of soft onboarding for all agents without complex imports.
"""

import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Execute soft onboarding for all agents using direct function calls."""

    print("🚀 SIMPLE SOFT ONBOARDING ALL AGENTS")
    print("=" * 50)

    # Load agent configuration directly
    config_path = Path("agent_mode_config.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        current_mode = config.get("current_mode", "8-agent")
        active_agents = config.get("modes", {}).get(current_mode, {}).get("active_agents", [])

        if not active_agents:
            logger.error("❌ No active agents found in configuration")
            return 1

        logger.info(f"📋 Found {len(active_agents)} active agents: {active_agents}")

    except Exception as e:
        logger.error(f"❌ Could not load agent configuration: {e}")
        return 1

    # Import soft onboarding service directly
    try:
        # Add src to path
        project_root = Path(__file__).resolve().parent
        sys.path.insert(0, str(project_root / "src"))

        # Import the function directly
        from services.onboarding.soft.service import soft_onboard_multiple_agents

    except ImportError as e:
        logger.error(f"❌ Could not import soft onboarding service: {e}")
        return 1

    # Prepare agents for onboarding
    agents_to_onboard = [(agent_id, None) for agent_id in active_agents]

    print(f"🎯 Preparing to soft onboard {len(agents_to_onboard)} agents:")
    for agent_id, _ in agents_to_onboard:
        print(f"  • {agent_id}")

    print("\n⚡ Starting soft onboarding sequence...")
    print("This will execute 6 steps per agent with proper keyboard locking.")
    print()

    try:
        # Execute soft onboarding for all agents
        results = soft_onboard_multiple_agents(
            agents=agents_to_onboard,
            role=None,
            generate_cycle_report=True
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
        print(".1f"
        if successful:
            print(f"\n🟢 Successfully onboarded: {', '.join(successful)}")

        if failed:
            print(f"\n🔴 Failed agents: {', '.join(failed)}")

        return 0 if len(failed) == 0 else 1

    except KeyboardInterrupt:
        print("\n⚠️ Soft onboarding interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Soft onboarding failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())