#!/usr/bin/env python3
"""Check queue errors for diagnostics."""

import json
from pathlib import Path

q = Path('message_queue/queue.json')
if not q.exists():
    print("Queue file not found")
    exit(1)

data = json.loads(q.read_text())
failed = [e for e in data if e.get('status') == 'FAILED']

print(f"Total failed messages: {len(failed)}\n")
print("Recent failed messages (last 5):")
for e in failed[-5:]:
    print(f"\nQueue ID: {e.get('queue_id', 'Unknown')[:40]}")
    error = e.get('error') or e.get('metadata', {}).get('last_error', 'No error message')
    print(f"Error: {error}")
    print(f"Recipient: {e.get('message', {}).get('recipient', 'Unknown')}")
    print(f"Created: {e.get('created_at', 'Unknown')}")
    print(f"Updated: {e.get('updated_at', 'Unknown')}")

