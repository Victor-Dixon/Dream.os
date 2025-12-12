#!/usr/bin/env python3
"""Check recent activation messages from today 15:36."""
import json
from pathlib import Path

queue_file = Path('message_queue/queue.json')
data = json.loads(queue_file.read_text())
entries = data if isinstance(data, list) else data.get('entries', [])

print("Recent Activation Messages (15:36 timeframe):")
print("=" * 70)

target_ids = [
    '2f82def8-2015-43d6-b899-27ed478d6d70',  # Agent-7
    '837bc0d5-01eb-4273-b4d4-6f6caa9eb331'   # Agent-8
]

found = []

for entry in entries:
    if not isinstance(entry, dict):
        continue
    
    msg_id = entry.get('id', '') or entry.get('queue_id', '')
    created = entry.get('created_at', '')
    
    # Check if created around 15:36 (our activation time)
    if '2025-12-11T15:3' in str(created) or '2025-12-11T15:4' in str(created):
        message = entry.get('message', {})
        content = str(message.get('content', '')) if isinstance(message, dict) else str(message)
        recipient = message.get('recipient', '') if isinstance(message, dict) else ''
        
        # Check if it's an activation message
        if 'JET FUEL ACTIVATION' in content or 'Check inbox' in content:
            found.append({
                'id': msg_id,
                'status': entry.get('status'),
                'created': created,
                'recipient': recipient,
                'content_preview': content[:80]
            })

# Also check for our specific IDs
for entry in entries:
    if not isinstance(entry, dict):
        continue
    msg_id = entry.get('id', '') or entry.get('queue_id', '')
    for target_id in target_ids:
        if target_id in msg_id:
            found.append({
                'id': msg_id,
                'status': entry.get('status'),
                'created': entry.get('created_at', ''),
                'recipient': (
                    entry.get('message', {}).get('recipient', 'unknown')
                    if isinstance(entry.get('message'), dict)
                    else 'unknown'
                ),
                'content_preview': 'ACTIVATION MESSAGE (matched by ID)'
            })

print(f"\nFound {len(found)} activation messages:\n")
for i, msg in enumerate(found, 1):
    if msg['status'] == 'DELIVERED':
        status_icon = "✅"
    elif msg['status'] == 'PROCESSING':
        status_icon = "⏳"
    else:
        status_icon = "❌"
    print(f"{status_icon} Message {i}:")
    print(f"   ID: {msg['id'][:32]}...")
    print(f"   Status: {msg['status']}")
    print(f"   Recipient: {msg['recipient']}")
    print(f"   Created: {msg['created'][:19]}")
    print(f"   Preview: {msg['content_preview']}")
    print()

