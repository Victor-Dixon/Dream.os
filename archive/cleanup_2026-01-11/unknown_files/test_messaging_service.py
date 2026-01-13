#!/usr/bin/env python3
"""
Test script for the enhanced MessagingService implementation.
Tests A2A coordination scenarios and unified messaging features.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Create a minimal settings stub to avoid environment variable issues
class MinimalSettings:
    def __init__(self):
        self.current_agent = "Agent-4"

from src.agent_cellphone_v2.services.messaging import MessagingService


async def test_messaging_service():
    """Test the messaging service with A2A coordination scenarios."""
    print("🧪 Testing MessagingService Implementation")
    print("=" * 50)

    # Initialize minimal settings
    settings = MinimalSettings()

    # Create messaging service
    messaging = MessagingService(settings)

    # Start service
    await messaging.start()
    print("✅ Messaging service started")

    try:
        # Test 1: Basic message sending
        print("\n📤 Test 1: Basic message sending")
        result1 = await messaging.send_message(
            recipient="Agent-1",
            message="Hello from Agent-4! Testing basic messaging."
        )
        print(f"Result: {result1}")
        assert result1["status"] in ["queued", "sent"], f"Expected queued/sent status, got {result1['status']}"

        # Test 2: A2A coordination message
        print("\n🤝 Test 2: A2A coordination message")
        coordination_message = """A2A REPLY to 6469101a-d2a1-4f2c-9f02-40efa32b2007:
✅ ACCEPT: Proposed approach: Agent-4 leads messaging infrastructure enhancement while Agent-1 provides coordination oversight. Synergy: Agent-4's implementation expertise complements Agent-1's system integration focus. Next steps: Execute messaging service implementation and test A2A coordination flows. Capabilities: Unified messaging, error handling, message queuing. Timeline: Complete implementation within 15 minutes + coordination sync immediately.
"""
        result2 = await messaging.send_message(
            recipient="Agent-1",
            message=coordination_message,
            priority="high",
            category="a2a",
            tags=["coordination-reply", "task"],
            metadata={
                "coordination_type": "bilateral_swarm",
                "message_id": "6469101a-d2a1-4f2c-9f02-40efa32b2007",
                "response_type": "accept"
            }
        )
        print(f"Result: {result2}")
        assert result2["status"] in ["queued", "sent"], f"Expected queued/sent status, got {result2['status']}"

        # Test 3: Error handling
        print("\n⚠️  Test 3: Error handling (service stopped)")
        await messaging.stop()
        try:
            await messaging.send_message(
                recipient="Agent-1",
                message="This should fail"
            )
            assert False, "Expected RuntimeError when service is stopped"
        except RuntimeError as e:
            print(f"✅ Correctly caught error: {e}")

        # Test 4: Message history
        print("\n📚 Test 4: Message history")
        await messaging.start()  # Restart service
        history = messaging.get_message_history(limit=10)
        print(f"Message history count: {len(history)}")
        assert len(history) >= 2, f"Expected at least 2 messages in history, got {len(history)}"

        # Test 5: Agent status
        print("\n👤 Test 5: Agent status")
        status = await messaging.get_agent_status("Agent-1")
        print(f"Agent status: {status}")
        assert status is not None, "Expected agent status to be returned"
        assert status["agent_id"] == "Agent-1", f"Expected Agent-1, got {status['agent_id']}"

        print("\n🎉 All tests passed!")
        print("✅ Messaging service implementation is working correctly")
        print("✅ A2A coordination scenarios supported")
        print("✅ Unified messaging components integrated")
        print("✅ Error handling functional")
        print("✅ Message history and status tracking working")

    finally:
        await messaging.stop()
        print("\n🛑 Messaging service stopped")


if __name__ == "__main__":
    # Set environment variable for testing
    os.environ["AGENT_ID"] = "Agent-4"

    # Run tests
    asyncio.run(test_messaging_service())