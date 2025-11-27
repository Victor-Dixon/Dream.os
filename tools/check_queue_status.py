#!/usr/bin/env python3
"""Quick queue status check."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.message_queue_persistence import FileQueuePersistence

p = FileQueuePersistence(Path("message_queue/queue.json"))
entries = p.load_entries()

status_counts = {}
for entry in entries:
    status = getattr(entry, 'status', 'UNKNOWN')
    status_counts[status] = status_counts.get(status, 0) + 1

print(f"Queue Status:")
print(f"  PENDING: {status_counts.get('PENDING', 0)}")
print(f"  PROCESSING: {status_counts.get('PROCESSING', 0)}")
print(f"  DELIVERED: {status_counts.get('DELIVERED', 0)}")
print(f"  FAILED: {status_counts.get('FAILED', 0)}")

# Show recent messages
recent = entries[-5:] if len(entries) > 5 else entries
print(f"\nRecent messages:")
for e in recent:
    msg = getattr(e, 'message', {})
    print(f"  {getattr(e, 'queue_id', 'unknown')[:8]}: {getattr(e, 'status', 'unknown')} -> {msg.get('recipient', 'unknown')} - {str(msg.get('content', ''))[:40]}")

