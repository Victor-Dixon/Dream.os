#!/usr/bin/env python3
"""Check status of activation messages."""
import json
from pathlib import Path

queue_file = Path('message_queue/queue.json')
data = json.loads(queue_file.read_text())
entries = data if isinstance(data, list) else data.get('entries', [])

activation_ids = [
    '2f82def8-2015-43d6-b899-27ed478d6d70',  # Agent-7
    '837bc0d5-01eb-4273-b4d4-6f6caa9eb331'   # Agent-8
]

print("Activation Message Status:\n")
for entry in entries:
    if not isinstance(entry, dict):
        continue
    msg_id = entry.get('id', '') or entry.get('queue_id', '')
    if msg_id in activation_ids:
        status = entry.get('status', 'unknown')
        recipient = entry.get('recipient', 'unknown')
        created = entry.get('created_at', 'unknown')
        print(f"✅ {recipient}:")
        print(f"   ID: {msg_id[:16]}...")
        print(f"   Status: {status}")
        print(f"   Created: {created}")
        print()

# Also check last 5 entries
print("\nLast 5 queue entries:")
for entry in entries[-5:]:
    if isinstance(entry, dict):
        entry_id = entry.get('id', 'unknown')[:16]
        recipient = entry.get('recipient', 'unknown')
        status = entry.get('status', 'unknown')
        print(f"  - {entry_id}... ({recipient}): {status}")

