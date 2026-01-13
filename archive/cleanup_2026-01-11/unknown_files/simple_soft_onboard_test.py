#!/usr/bin/env python3
"""
Simple Soft Onboard Test - Test Single Agent
===========================================

Test soft onboarding for a single agent to verify the system works.
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "src"))

from src.services.onboarding.soft.service import soft_onboard_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Test soft onboarding for Agent-1."""

    print("🧪 TESTING SOFT ONBOARDING - SINGLE AGENT")
    print("=" * 50)

    agent_id = "Agent-1"

    print(f"🎯 Testing soft onboarding for {agent_id}")
    print("This will execute 6 steps with proper keyboard locking.")
    print("Estimated time: ~30 seconds")
    print()

    try:
        # Execute soft onboarding for single agent
        success = soft_onboard_agent(agent_id)

        print("\n" + "=" * 50)
        print("📊 SOFT ONBOARDING TEST RESULTS")
        print("=" * 50)

        if success:
            print(f"✅ {agent_id}: Successfully onboarded")
            print("🎉 Soft onboarding system is functional!")
            return 0
        else:
            print(f"❌ {agent_id}: Onboarding failed")
            print("🔧 Check system setup and try again.")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ Soft onboarding test interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Soft onboarding test failed with error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())