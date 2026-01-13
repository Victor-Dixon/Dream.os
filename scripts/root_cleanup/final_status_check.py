#!/usr/bin/env python3
"""Final status check of activation messages."""
import json
from pathlib import Path

queue_file = Path('message_queue/queue.json')
data = json.loads(queue_file.read_text())
entries = data if isinstance(data, list) else data.get('entries', [])

activation_ids = {
    '2f82def8-2015-43d6-b899-27ed478d6d70': 'Agent-7',
    '837bc0d5-01eb-4273-b4d4-6f6caa9eb331': 'Agent-8'
}

print("=" * 60)
print("ACTIVATION MESSAGE DELIVERY STATUS")
print("=" * 60)
print()

found_messages = {}

for entry in entries:
    if not isinstance(entry, dict):
        continue
    msg_id = entry.get('id', '') or entry.get('queue_id', '')
    for activation_id, agent_name in activation_ids.items():
        if activation_id in msg_id:
            found_messages[agent_name] = {
                'id': msg_id[:16] + '...',
                'status': entry.get('status', 'unknown'),
                'created': entry.get('created_at', 'unknown')[:19] if entry.get('created_at') else 'unknown',
                'recipient': entry.get('message', {}).get('recipient', agent_name) if isinstance(entry.get('message'), dict) else agent_name
            }

for agent, info in activation_ids.items():
    agent_name = info
    if agent_name in found_messages:
        msg = found_messages[agent_name]
        status_icon = "✅" if msg['status'] == 'DELIVERED' else "⏳" if msg['status'] == 'PROCESSING' else "❌"
        print(f"{status_icon} {agent_name}:")
        print(f"   Status: {msg['status']}")
        print(f"   Created: {msg['created']}")
        print(f"   ID: {msg['id']}")
        print()
    else:
        print(f"❓ {agent_name}: Message not found in queue")
        print()

print("=" * 60)
print(f"Queue Summary: {len(entries)} total entries")
pending = len([e for e in entries if isinstance(e, dict) and e.get('status') == 'PENDING'])
processing = len([e for e in entries if isinstance(e, dict) and e.get('status') == 'PROCESSING'])
delivered = len([e for e in entries if isinstance(e, dict) and e.get('status') == 'DELIVERED'])
print(f"  - PENDING: {pending}")
print(f"  - PROCESSING: {processing}")
print(f"  - DELIVERED: {delivered}")
print("=" * 60)

