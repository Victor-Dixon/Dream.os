#!/usr/bin/env python3
"""
Test Agent Activity Tracking
============================

Tests AgentActivityTracker integration.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.agent_activity_tracker import get_activity_tracker

def test_activity_tracking():
    """Test activity tracking."""
    print("=" * 60)
    print("Agent Activity Tracking Test")
    print("=" * 60)
    
    tracker = get_activity_tracker()
    
    # Test marking active
    print("\n1. Testing mark_active()...")
    tracker.mark_active("Agent-1", "testing")
    print("   ✅ Agent-1 marked as active")
    
    # Test checking activity
    print("\n2. Testing is_agent_active()...")
    is_active = tracker.is_agent_active("Agent-1")
    print(f"   ✅ Agent-1 active: {is_active}")
    
    # Test marking delivering
    print("\n3. Testing mark_delivering()...")
    tracker.mark_delivering("Agent-1", "test_queue_id")
    print("   ✅ Agent-1 marked as delivering")
    
    # Test marking inactive
    print("\n4. Testing mark_inactive()...")
    tracker.mark_inactive("Agent-1")
    print("   ✅ Agent-1 marked as inactive")
    
    # Test getting activity
    print("\n4. Testing get_agent_activity()...")
    activity = tracker.get_agent_activity("Agent-1")
    print(f"   ✅ Activity retrieved: {activity.get('is_active', False)}")
    
    print("\n" + "=" * 60)
    print("Activity Tracking Test Complete")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_activity_tracking()
    exit(0 if success else 1)

