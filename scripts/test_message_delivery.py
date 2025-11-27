#!/usr/bin/env python3
"""
Test Message Delivery
====================

Tests if message delivery is working by sending a test message.
"""
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.messaging_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
)
from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
from src.core.coordinate_loader import get_coordinate_loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_delivery():
    """Test message delivery to Agent-1."""
    print("=" * 60)
    print("Testing Message Delivery")
    print("=" * 60)
    
    # Check coordinates
    coord_loader = get_coordinate_loader()
    coords = coord_loader.get_chat_coordinates("Agent-1")
    print(f"\n📍 Agent-1 coordinates: {coords}")
    
    if not coords:
        print("❌ No coordinates found for Agent-1")
        return False
    
    # Create test message
    msg = UnifiedMessage(
        sender="TEST",
        recipient="Agent-1",
        content="Test message from delivery test script",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.REGULAR,
    )
    
    # Test delivery
    print("\n📤 Attempting delivery...")
    try:
        delivery = PyAutoGUIMessagingDelivery()
        result = delivery.send_message(msg)
        
        if result:
            print("✅ Delivery successful!")
            return True
        else:
            print("❌ Delivery returned False")
            return False
    except Exception as e:
        print(f"❌ Delivery exception: {e}")
        logger.exception("Delivery failed")
        return False

if __name__ == "__main__":
    success = test_delivery()
    sys.exit(0 if success else 1)

