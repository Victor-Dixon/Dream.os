#!/usr/bin/env python3
"""
Fix Stuck Message in Queue
===========================

Resets the single stuck PROCESSING message to PENDING for retry.

Author: Agent-7
Date: 2025-01-27
"""

import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
queue_file = project_root / "message_queue" / "queue.json"

if not queue_file.exists():
    print("❌ Queue file not found")
    sys.exit(1)

with open(queue_file, 'r', encoding='utf-8') as f:
    entries = json.load(f)

# Find and reset PROCESSING messages
reset_count = 0
for entry in entries:
    if entry.get('status') == 'PROCESSING':
        entry['status'] = 'PENDING'
        reset_count += 1
        print(f"✅ Reset message {entry.get('queue_id', 'N/A')[:20]}... to PENDING")

if reset_count == 0:
    print("✅ No stuck messages found")
else:
    # Backup
    backup = queue_file.with_suffix('.json.backup2')
    import shutil
    shutil.copy2(queue_file, backup)
    
    # Save
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reset {reset_count} message(s). Backup: {backup}")

