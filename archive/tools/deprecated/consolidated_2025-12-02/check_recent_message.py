#!/usr/bin/env python3
"""Check for recent REAL TEST message."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.message_queue_persistence import FileQueuePersistence

p = FileQueuePersistence(Path("message_queue/queue.json"))
entries = p.load_entries()

# Find REAL TEST message
real_test = [e for e in entries if 'REAL TEST' in str(getattr(e, 'message', {}).get('content', ''))]

print(f"REAL TEST messages found: {len(real_test)}")
for e in real_test:
    msg = getattr(e, 'message', {})
    print(f"  Queue ID: {getattr(e, 'queue_id', 'unknown')[:8]}")
    print(f"  Status: {getattr(e, 'status', 'unknown')}")
    print(f"  Content: {str(msg.get('content', ''))[:80]}")
    print(f"  Recipient: {msg.get('recipient', 'unknown')}")
    print()

# Show most recent 5 messages
print("\nMost recent 5 messages:")
recent = entries[-5:] if len(entries) > 5 else entries
for e in recent:
    msg = getattr(e, 'message', {})
    print(f"  {getattr(e, 'queue_id', 'unknown')[:8]}: {getattr(e, 'status', 'unknown')} -> {msg.get('recipient', 'unknown')} - {str(msg.get('content', ''))[:50]}")

