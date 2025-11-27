#!/usr/bin/env python3
"""
Reset Stuck Messages in Queue
=============================

Resets messages stuck in PROCESSING status back to PENDING
so they can be reprocessed.

Author: Agent-3 (Infrastructure & DevOps)
Date: 2025-11-23
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def reset_stuck_messages():
    """Reset messages stuck in PROCESSING back to PENDING."""
    queue_file = Path("message_queue/queue.json")
    
    if not queue_file.exists():
        print("❌ Queue file not found")
        return 1
    
    # Load queue
    with open(queue_file, 'r') as f:
        data = json.load(f)
    
    entries = data.get('entries', []) if isinstance(data, dict) else data
    
    # Count stuck messages
    stuck = [e for e in entries if isinstance(e, dict) and e.get('status') == 'PROCESSING']
    print(f"Found {len(stuck)} messages stuck in PROCESSING")
    
    if not stuck:
        print("✅ No stuck messages found")
        return 0
    
    # Reset to PENDING
    reset_count = 0
    for entry in entries:
        if isinstance(entry, dict) and entry.get('status') == 'PROCESSING':
            entry['status'] = 'PENDING'
            entry['updated_at'] = datetime.now().isoformat()
            if 'error' in entry:
                del entry['error']
            reset_count += 1
    
    # Save queue
    if isinstance(data, dict):
        data['entries'] = entries
    else:
        data = entries
    
    with open(queue_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Reset {reset_count} messages from PROCESSING to PENDING")
    return 0

if __name__ == "__main__":
    sys.exit(reset_stuck_messages())

