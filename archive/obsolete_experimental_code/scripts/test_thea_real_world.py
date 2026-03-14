#!/usr/bin/env python3
"""
Real-world Thea testing - let's see what actually happens in practice
"""

import time
from src.services.thea.thea_service_coordinator import create_default_thea_coordinator

def test_real_thea_operations():
    """Test Thea in real-world conditions, not just unit tests."""

    print("🧪 REAL-WORLD THEA TESTING - Let's see what actually happens...")
    print("=" * 60)

    # Create the coordinator (this should handle all the DI and setup)
    print("🔧 Creating Thea coordinator...")
    try:
        coordinator = create_default_thea_coordinator()
        print("✅ Coordinator created successfully")
    except Exception as e:
        print(f"❌ Failed to create coordinator: {e}")
        return

    # Test 1: Basic message sending
    print("\n" + "=" * 40)
    print("🧪 TEST 1: Basic message sending")
    print("=" * 40)

    test_message = "Hello Thea, this is a real-world test. Please acknowledge with a simple response."

    try:
        print(f"📤 Sending message: {test_message[:50]}...")

        start_time = time.time()
        result = coordinator.send_message(test_message)
        end_time = time.time()

        print(".2f")
        print(f"Success: {result.success}")

        if result.success:
            print("✅ Message sent successfully!")
            print(f"Response length: {len(result.response.content)} characters")
            print(f"Response preview: {result.response.content[:200]}...")
        else:
            print("❌ Message failed!")
            print(f"Error: {result.error_message}")

    except Exception as e:
        print(f"❌ Exception during message sending: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Multiple messages (if first one works)
    if result.success:
        print("\n" + "=" * 40)
        print("🧪 TEST 2: Multiple messages")
        print("=" * 40)

        messages = [
            "Test message 2 - please respond briefly",
            "Test message 3 - how are you doing?",
            "Test message 4 - final test message"
        ]

        for i, msg in enumerate(messages, 2):
            print(f"\n📤 Test {i}: {msg}")
            try:
                result = coordinator.send_message(msg)
                if result.success:
                    print(f"✅ Success - Response: {result.response.content[:100]}...")
                else:
                    print(f"❌ Failed - Error: {result.error_message}")
            except Exception as e:
                print(f"❌ Exception: {e}")

    print("\n" + "=" * 60)
    print("🎯 REAL-WORLD TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_real_thea_operations()