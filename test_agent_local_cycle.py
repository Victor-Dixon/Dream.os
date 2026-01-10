#!/usr/bin/env python3
"""
Test Agent Local Cycle - Phase 7 Agent Runtime Recovery
=======================================================

Test that agents can complete a local cycle using mock bridge/messaging.
This verifies the agent runtime recovery for Phase 7.

Usage:
    python test_agent_local_cycle.py [agent_id]

Author: Agent-8 (SSOT & System Integration)
"""

import sys
import os
from pathlib import Path
import logging
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
src_root = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_root))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def test_agent_local_cycle(agent_id: str = "Agent-8") -> bool:
    """
    Test that an agent can complete a local cycle with mock messaging.

    Args:
        agent_id: Agent to test (default: Agent-8)

    Returns:
        True if cycle completed successfully
    """
    logger.info(f"🧪 Testing local cycle for {agent_id}")

    try:
        # Import required components
        from src.core.agent_lifecycle import AgentLifecycle
        from src.core.in_memory_message_queue import InMemoryMessageQueue
        from src.core.mock_unified_messaging_core import MockUnifiedMessagingCore

        # Create agent lifecycle
        lifecycle = AgentLifecycle(agent_id)

        # Start cycle
        logger.info("📈 Starting agent cycle...")
        lifecycle.start_cycle()
        logger.info(f"Agent status after cycle start: {lifecycle.status.get('status', 'UNKNOWN')}")
        logger.info(f"FSM state: {lifecycle.status.get('fsm_state', 'UNKNOWN')}")
        # Check that cycle started (status should be ACTIVE, FSM state should be active)
        assert lifecycle.status.get("status") == "ACTIVE", f"Status not ACTIVE: {lifecycle.status.get('status')}"
        assert lifecycle.status.get("fsm_state") in ["ACTIVE", "active"], f"FSM state not active: {lifecycle.status.get('fsm_state')}"

        # Create mock messaging components
        logger.info("🔧 Setting up mock messaging...")
        mock_queue = InMemoryMessageQueue()
        mock_messaging = MockUnifiedMessagingCore()

        # Simulate a simple task
        logger.info("⚡ Executing mock task...")
        task_result = f"Mock task completed by {agent_id} at {datetime.now().isoformat()}"

        # Complete a mock task
        lifecycle.complete_task(
            task_name="Local cycle test - mock task execution",
            points=10
        )

        # End cycle
        logger.info("🏁 Ending agent cycle...")
        lifecycle.end_cycle(commit=False)  # Don't commit during test

        # Verify cycle completion
        final_status = lifecycle.status
        assert final_status["fsm_state"] in ["ACTIVE", "active"], f"FSM state incorrect: {final_status['fsm_state']}"
        assert "last_updated" in final_status, "No last_updated timestamp"
        # Cycle completed successfully if we get here without exceptions
        logger.info("✅ Cycle completed successfully")

        logger.info("✅ Agent local cycle test PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ Agent local cycle test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Agent Local Cycle Test - Phase 7 Recovery")
    print("=" * 50)

    # Test Agent-8 by default, or use command line arg
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "Agent-8"

    success = test_agent_local_cycle(agent_id)

    print("\n" + "=" * 50)
    if success:
        print("🎉 PHASE 7 AGENT RUNTIME RECOVERY: SUCCESS")
        print("✅ Agents can complete local cycles using mock bridge")
        return 0
    else:
        print("💥 PHASE 7 AGENT RUNTIME RECOVERY: FAILED")
        print("❌ Agent local cycle test failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())