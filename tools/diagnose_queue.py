#!/usr/bin/env python3
"""
Queue Diagnostic Tool
=====================

Quick diagnostic to check queue status and test message delivery.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue import MessageQueue
from src.core.keyboard_control_lock import is_locked, get_current_holder

def main():
    print("🔍 Queue Diagnostic Tool\n")
    
    # Check keyboard lock
    print("📊 Keyboard Lock Status:")
    locked = is_locked()
    holder = get_current_holder()
    print(f"  Status: {'LOCKED' if locked else 'UNLOCKED'}")
    print(f"  Holder: {holder or 'None'}\n")
    
    # Check queue
    print("📋 Queue Status:")
    try:
        queue = MessageQueue()
        
        # Get statistics
        stats = queue.get_statistics()
        print(f"  Total entries: {stats.get('total_entries', 0)}")
        print(f"  PENDING: {stats.get('pending_count', 0)}")
        print(f"  PROCESSING: {stats.get('processing_count', 0)}")
        print(f"  DELIVERED: {stats.get('delivered_count', 0)}")
        print(f"  FAILED: {stats.get('failed_count', 0)}")
        
        # Get health status
        health = queue.get_health_status()
        print(f"\n  Health Status:")
        print(f"    Status: {health.get('status', 'unknown')}")
        print(f"    Issues: {len(health.get('issues', []))}")
        if health.get('issues'):
            for issue in health['issues'][:3]:
                print(f"      - {issue}")
        
        # Try to get pending messages
        pending = queue.dequeue(batch_size=1000)  # Get all
        pending_only = [e for e in pending if e.status == 'PENDING']
        if pending_only:
            print(f"\n  Sample PENDING messages ({len(pending_only)}):")
            for e in pending_only[:5]:
                msg = e.message if hasattr(e, 'message') else {}
                print(f"    - {e.queue_id}: {msg.get('recipient', 'unknown')} - {str(msg.get('content', ''))[:50]}...")
        
    except Exception as e:
        print(f"  ❌ Error checking queue: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Diagnostic complete")

if __name__ == "__main__":
    main()

