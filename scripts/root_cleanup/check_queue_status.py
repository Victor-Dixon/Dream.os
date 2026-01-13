#!/usr/bin/env python3
"""Check message queue status for activation messages."""
import json
from pathlib import Path

queue_file = Path('message_queue/queue.json')
if not queue_file.exists():
    print("Queue file not found")
    exit(1)

data = json.loads(queue_file.read_text())
entries = data if isinstance(data, list) else data.get('entries', [])

# Find our activation messages
activation_ids = [
    '2f82def8-2015-43d6-b899-27ed478d6d70',  # Agent-7
    '837bc0d5-01eb-4273-b4d4-6f6caa9eb331'   # Agent-8
]

print(f"Total queue entries: {len(entries)}")
print("\nActivation messages:")
for entry in entries:
    msg_id = entry.get('id', '') if isinstance(entry, dict) else ''
    if msg_id in activation_ids:
        status = entry.get('status', 'unknown') if isinstance(entry, dict) else 'unknown'
        recipient = entry.get('recipient', 'unknown') if isinstance(entry, dict) else 'unknown'
        print(f"  - {msg_id[:8]}... ({recipient}): {status}")

# Count by status
pending = [e for e in entries if isinstance(e, dict) and e.get('status') == 'PENDING']
processing = [e for e in entries if isinstance(e, dict) and e.get('status') == 'PROCESSING']
delivered = [e for e in entries if isinstance(e, dict) and e.get('status') == 'DELIVERED']

print("\nQueue status:")
print(f"  - PENDING: {len(pending)}")
print(f"  - PROCESSING: {len(processing)}")
print(f"  - DELIVERED: {len(delivered)}")

