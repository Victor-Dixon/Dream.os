#!/usr/bin/env python3
"""Find Agent-8 activation message."""
import json
from pathlib import Path

queue_file = Path('message_queue/queue.json')
data = json.loads(queue_file.read_text())
entries = data if isinstance(data, list) else data.get('entries', [])

print("Searching for Agent-8 message...")
print("=" * 60)

# Search all entries
for i, entry in enumerate(entries):
    if not isinstance(entry, dict):
        continue
    
    msg_id = entry.get('id', '') or entry.get('queue_id', '')
    message = entry.get('message', {})
    
    # Check if message content mentions Agent-8 or Phase 2 SSOT
    content = ""
    recipient = ""
    if isinstance(message, dict):
        content = str(message.get('content', ''))
        recipient = message.get('recipient', '')
    elif isinstance(message, str):
        content = message
    
    # Check various conditions
    if 'Agent-8' in str(entry) or 'Agent-8' in content or recipient == 'Agent-8' or 'Phase 2' in content or '837bc0d5' in msg_id:
        print(f"\n✅ Found Agent-8 message at index {i}:")
        print(f"   Queue ID: {msg_id[:32]}...")
        print(f"   Status: {entry.get('status', 'unknown')}")
        print(f"   Created: {entry.get('created_at', 'unknown')[:19]}")
        print(f"   Recipient: {recipient}")
        if content:
            preview = content[:100].replace('\n', ' ')
            print(f"   Content preview: {preview}...")
        print()

# Also check last few entries more carefully
print("\nLast 10 entries (detailed):")
print("=" * 60)
for i, entry in enumerate(entries[-10:], start=len(entries)-10):
    if isinstance(entry, dict):
        msg_id = entry.get('id', '') or entry.get('queue_id', '')
        status = entry.get('status', 'unknown')
        message = entry.get('message', {})
        recipient = message.get('recipient', 'unknown') if isinstance(message, dict) else 'unknown'
        print(f"{i}: {msg_id[:16]}... | {status} | {recipient}")

