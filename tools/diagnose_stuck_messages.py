#!/usr/bin/env python3
"""
Diagnose and Fix Stuck Messages in Queue
========================================

Identifies messages stuck in PROCESSING status and provides options to:
1. Reset them to PENDING for retry
2. Mark them as FAILED with timeout error
3. Show detailed diagnostics

Author: Agent-7 (Web Development Specialist)
Date: 2025-01-27
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def diagnose_stuck_messages():
    """Diagnose messages stuck in PROCESSING status."""
    print("🔍 Diagnosing stuck messages in queue...\n")
    
    # Load queue
    queue_file = project_root / "message_queue" / "queue.json"
    if not queue_file.exists():
        print("❌ Queue file not found:", queue_file)
        return 1
    
    with open(queue_file, 'r', encoding='utf-8') as f:
        queue_data = json.load(f)
    
    entries = queue_data.get('entries', [])
    
    # Find stuck messages
    processing = [e for e in entries if e.get('status') == 'PROCESSING']
    pending = [e for e in entries if e.get('status') == 'PENDING']
    delivered = [e for e in entries if e.get('status') == 'DELIVERED']
    failed = [e for e in entries if e.get('status') == 'FAILED']
    
    print(f"📊 Queue Status:")
    print(f"   PENDING: {len(pending)}")
    print(f"   PROCESSING: {len(processing)} ⚠️")
    print(f"   DELIVERED: {len(delivered)}")
    print(f"   FAILED: {len(failed)}")
    print(f"   TOTAL: {len(entries)}\n")
    
    if not processing:
        print("✅ No stuck messages found!")
        return 0
    
    print(f"⚠️ Found {len(processing)} stuck messages:\n")
    
    # Analyze stuck messages
    now = datetime.now()
    stuck_old = []
    stuck_recent = []
    
    for entry in processing:
        created_str = entry.get('created_at', '')
        try:
            if created_str:
                created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                age = now - created.replace(tzinfo=None) if created.tzinfo else now - created
                
                if age > timedelta(minutes=5):
                    stuck_old.append((entry, age))
                else:
                    stuck_recent.append((entry, age))
        except Exception:
            stuck_old.append((entry, None))
    
    if stuck_old:
        print(f"🔴 OLD stuck messages (>5 minutes): {len(stuck_old)}")
        for entry, age in stuck_old[:5]:
            queue_id = entry.get('queue_id', 'N/A')[:20]
            recipient = entry.get('recipient', 'N/A')
            sender = entry.get('sender', 'N/A')
            age_str = str(age).split('.')[0] if age else 'unknown'
            print(f"   ID: {queue_id}... | {sender} → {recipient} | Age: {age_str}")
        print()
    
    if stuck_recent:
        print(f"🟡 RECENT stuck messages (<5 minutes): {len(stuck_recent)}")
        for entry, age in stuck_recent[:3]:
            queue_id = entry.get('queue_id', 'N/A')[:20]
            recipient = entry.get('recipient', 'N/A')
            age_str = str(age).split('.')[0] if age else 'unknown'
            print(f"   ID: {queue_id}... | → {recipient} | Age: {age_str}")
        print()
    
    # Check for common issues
    print("🔍 Common Issues:")
    
    # Check for keyboard lock timeouts in logs
    log_file = project_root / "logs" / "queue_processor.log"
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            timeout_count = log_content.count('TIMEOUT: Could not acquire keyboard lock')
            if timeout_count > 0:
                print(f"   ⚠️ Keyboard lock timeouts in logs: {timeout_count}")
    
    # Check for test messages
    test_messages = [e for e in processing if e.get('recipient') == 'Test' or e.get('sender') == 'Test']
    if test_messages:
        print(f"   ⚠️ Test messages stuck: {len(test_messages)}")
    
    print()
    
    # Provide recommendations
    print("💡 Recommendations:")
    if stuck_old:
        print("   1. Reset old stuck messages (>5 min) to PENDING for retry")
        print("   2. Or mark them as FAILED with timeout error")
    if stuck_recent:
        print("   3. Recent messages may still be processing - wait a bit longer")
    print("   4. Check if queue processor is running and not blocked")
    print("   5. Check keyboard lock status - may need to clear lock file")
    
    return 0

if __name__ == "__main__":
    sys.exit(diagnose_stuck_messages())

