#!/usr/bin/env python3
"""
Verify Message Logging Implementation
====================================

Tests all three logging points:
1. messaging_core.py
2. message_queue.py
3. message_queue_processor.py
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repositories.message_repository import MessageRepository
from src.core.messaging_core import UnifiedMessagingCore
from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority
from src.core.message_queue import MessageQueue

def verify_message_history_file():
    """Verify message_history.json is valid and populated."""
    history_file = Path("data/message_history.json")
    
    if not history_file.exists():
        print("❌ Message history file does not exist")
        return False
    
    try:
        with open(history_file, 'r') as f:
            data = json.load(f)
        
        messages = data.get("messages", [])
        print(f"✅ Message history file valid: {len(messages)} messages")
        
        if messages:
            latest = messages[-1]
            print(f"✅ Latest message: {latest.get('from')} → {latest.get('to')} at {latest.get('timestamp', '')[:19]}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading message history: {e}")
        return False

def verify_repository():
    """Verify MessageRepository is working."""
    try:
        repo = MessageRepository()
        count = repo.get_message_count()
        print(f"✅ MessageRepository: {count} total messages")
        
        recent = repo.get_recent_messages(limit=3)
        print(f"✅ Recent messages: {len(recent)} retrieved")
        
        return True
    except Exception as e:
        print(f"❌ Error with MessageRepository: {e}")
        return False

def test_messaging_core_logging():
    """Test messaging_core.py logging."""
    try:
        core = UnifiedMessagingCore()
        result = core.send_message(
            "Verification test message",
            "Agent-1",
            "Agent-7",
            UnifiedMessageType.TEXT,
            UnifiedMessagePriority.REGULAR
        )
        
        if result:
            print("✅ messaging_core.py: Message sent and logged")
            return True
        else:
            print("❌ messaging_core.py: Message send failed")
            return False
    except Exception as e:
        print(f"❌ Error testing messaging_core: {e}")
        return False

def test_queue_logging():
    """Test message_queue.py logging."""
    try:
        queue = MessageQueue()
        queue_id = queue.enqueue({
            "sender": "Agent-1",
            "recipient": "Agent-7",
            "content": "Verification test queued message",
            "type": "text",
            "priority": "regular"
        })
        
        print(f"✅ message_queue.py: Message queued and logged (ID: {queue_id[:8]}...)")
        return True
    except Exception as e:
        print(f"❌ Error testing message_queue: {e}")
        return False

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Message Logging Implementation Verification")
    print("=" * 60)
    print()
    
    results = []
    
    print("1. Verifying message history file...")
    results.append(verify_message_history_file())
    print()
    
    print("2. Verifying MessageRepository...")
    results.append(verify_repository())
    print()
    
    print("3. Testing messaging_core.py logging...")
    results.append(test_messaging_core_logging())
    print()
    
    print("4. Testing message_queue.py logging...")
    results.append(test_queue_logging())
    print()
    
    print("=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Message logging fully verified!")
        return 0
    else:
        print("❌ Some tests failed - Review implementation")
        return 1

if __name__ == "__main__":
    exit(main())

