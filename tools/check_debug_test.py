#!/usr/bin/env python3
"""Check for DEBUG TEST message in queue."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.message_queue_persistence import FileQueuePersistence

p = FileQueuePersistence(Path("message_queue/queue.json"))
entries = p.load_entries()

# Find DEBUG TEST message
debug_test = [e for e in entries if 'DEBUG TEST' in str(getattr(e, 'message', {}).get('content', ''))]

print(f"DEBUG TEST messages found: {len(debug_test)}")
for e in debug_test:
    msg = getattr(e, 'message', {})
    print(f"  Queue ID: {getattr(e, 'queue_id', 'unknown')[:8]}")
    print(f"  Status: {getattr(e, 'status', 'unknown')}")
    print(f"  Content: {str(msg.get('content', ''))[:80]}")
    print(f"  Recipient: {msg.get('recipient', 'unknown')}")
    print(f"  Sender: {msg.get('sender', 'unknown')}")
    print()

# Show ALL recent messages
print("\nAll recent messages (last 10):")
recent = entries[-10:] if len(entries) > 10 else entries
for e in recent:
    msg = getattr(e, 'message', {})
    content = str(msg.get('content', ''))[:50]
    print(f"  {getattr(e, 'queue_id', 'unknown')[:8]}: {getattr(e, 'status', 'unknown')} -> {msg.get('recipient', 'unknown')} - {content}")

