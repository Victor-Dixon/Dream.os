#!/usr/bin/env python3
"""
Check Queue Processor Status
============================

Checks if queue processor is running and processing messages.

Usage:
    python tools/check_queue_processor.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue import MessageQueue, QueueConfig
from src.core.message_queue_persistence import FileQueuePersistence

def check_queue_status():
    """Check queue processor status and message counts."""
    print("🔍 Checking queue processor status...\n")
    
    try:
        # Load queue
        queue_file = Path("message_queue/queue.json")
        if not queue_file.exists():
            print("❌ Queue file not found!")
            print("   Location: message_queue/queue.json")
            return 1
        
        persistence = FileQueuePersistence(queue_file)
        entries = persistence.load_entries()
        
        print(f"📊 Queue Status:")
        print(f"   Total entries: {len(entries)}")
        
        # Count by status
        status_counts = {}
        for entry in entries:
            status = getattr(entry, 'status', 'UNKNOWN')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\n   Status Breakdown:")
        for status in ['PENDING', 'PROCESSING', 'DELIVERED', 'FAILED']:
            count = status_counts.get(status, 0)
            emoji = "✅" if status == "DELIVERED" else "⚠️" if status in ["PROCESSING", "FAILED"] else "📋"
            print(f"   {emoji} {status}: {count}")
        
        # Check for stuck messages
        stuck = status_counts.get('PROCESSING', 0)
        if stuck > 0:
            print(f"\n⚠️  WARNING: {stuck} messages stuck in PROCESSING status")
            print("   Run: python tools/reset_stuck_messages.py")
        
        # Check recent messages
        print(f"\n📋 Recent Messages (last 5):")
        recent = sorted(entries, key=lambda e: getattr(e, 'created_at', ''), reverse=True)[:5]
        for entry in recent:
            queue_id = getattr(entry, 'queue_id', 'unknown')[:8]
            status = getattr(entry, 'status', 'UNKNOWN')
            msg = getattr(entry, 'message', {})
            sender = msg.get('sender', 'UNKNOWN')
            recipient = msg.get('recipient', 'UNKNOWN')
            created = getattr(entry, 'created_at', 'unknown')
            print(f"   {queue_id}... | {status:10} | {sender} → {recipient} | {created}")
        
        # Check if queue processor should be running
        pending = status_counts.get('PENDING', 0)
        if pending > 0:
            print(f"\n💡 INFO: {pending} messages waiting in queue")
            print("   Queue processor should be running to deliver these")
            print("   Start: python -m src.core.message_queue_processor")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error checking queue: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(check_queue_status())

