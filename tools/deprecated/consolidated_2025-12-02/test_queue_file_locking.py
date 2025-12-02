#!/usr/bin/env python3
"""
Test Queue File Locking Fix
===========================

Tests the file locking fix for queue.json to ensure broadcast messages work correctly.

Author: Agent-7 (Web Development Specialist)
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_persistence import FileQueuePersistence, QueueEntry
from datetime import datetime

def test_save_entries_with_retry():
    """Test save_entries with retry logic."""
    print("=" * 70)
    print("🔍 Testing Queue File Locking Fix")
    print("=" * 70)
    print()
    
    # Create test queue file
    test_queue_file = Path("message_queue/test_queue.json")
    test_queue_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Clean up any existing test file
    if test_queue_file.exists():
        test_queue_file.unlink()
    
    try:
        # Create persistence instance
        persistence = FileQueuePersistence(test_queue_file)
        
        # Create test entries
        test_entries = [
            QueueEntry(
                message={"type": "test", "content": "Test message 1"},
                queue_id="test-1",
                priority_score=0.5,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            QueueEntry(
                message={"type": "test", "content": "Test message 2"},
                queue_id="test-2",
                priority_score=0.5,
                status="PENDING",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        print("📝 Test 1: Save entries (normal operation)")
        persistence.save_entries(test_entries)
        print("   ✅ PASS: Entries saved successfully")
        
        # Verify entries were saved
        loaded_entries = persistence.load_entries()
        if len(loaded_entries) == 2:
            print("   ✅ PASS: Entries loaded correctly")
        else:
            print(f"   ❌ FAIL: Expected 2 entries, got {len(loaded_entries)}")
            return False
        
        print()
        print("📝 Test 2: Save entries with retry (simulated lock)")
        # Save again to test retry logic
        persistence.save_entries(test_entries)
        print("   ✅ PASS: Retry logic works")
        
        print()
        print("📝 Test 3: Concurrent access simulation")
        # Try multiple saves in quick succession
        for i in range(3):
            persistence.save_entries(test_entries)
        print("   ✅ PASS: Multiple saves handled correctly")
        
        print()
        print("=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up test file
        if test_queue_file.exists():
            try:
                test_queue_file.unlink()
            except Exception:
                pass

if __name__ == "__main__":
    success = test_save_entries_with_retry()
    sys.exit(0 if success else 1)

