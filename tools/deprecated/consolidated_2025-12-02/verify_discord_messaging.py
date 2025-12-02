#!/usr/bin/env python3
"""
Verify Discord Messaging System
================================

Quick verification script to check if Discord messaging is working.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def check_queue_processor():
    """Check if queue processor is running."""
    try:
        from src.core.message_queue import MessageQueue
        q = MessageQueue()
        entries = q.dequeue(batch_size=1000)
        pending = [e for e in entries if e.status == 'PENDING']
        processing = [e for e in entries if e.status == 'PROCESSING']
        delivered = [e for e in entries if e.status == 'DELIVERED']
        
        print("📬 Queue Status:")
        print(f"  Pending: {len(pending)}")
        print(f"  Processing: {len(processing)}")
        print(f"  Delivered: {len(delivered)}")
        return len(pending) == 0 and len(processing) == 0
    except Exception as e:
        print(f"❌ Queue check failed: {e}")
        return False

def check_messaging_service():
    """Check if messaging service can queue messages."""
    try:
        from src.services.messaging_infrastructure import ConsolidatedMessagingService
        service = ConsolidatedMessagingService()
        has_queue = service.queue is not None
        print(f"✅ Messaging Service: Queue {'initialized' if has_queue else 'NOT initialized'}")
        return has_queue
    except Exception as e:
        print(f"❌ Messaging service check failed: {e}")
        return False

def main():
    print("🔍 Verifying Discord Messaging System...\n")
    
    service_ok = check_messaging_service()
    queue_ok = check_queue_processor()
    
    print("\n" + "="*50)
    if service_ok and queue_ok:
        print("✅ System Ready for Testing!")
        print("\nTest in Discord:")
        print("  !gui - Open messaging interface")
        print("  !message Agent-1 Test - Send test message")
        print("  !broadcast Test - Broadcast to all")
    else:
        print("⚠️  Issues detected - check above")
    print("="*50)

if __name__ == "__main__":
    main()

