#!/usr/bin/env python3
import json
from pathlib import Path

# Check queue status
queue_file = Path('message_queue/queue.json')
if queue_file.exists():
    with open(queue_file, 'r') as f:
        queue_data = json.load(f)

    print(f'Queue has {len(queue_data)} messages')

    # Count statuses
    statuses = {}
    for msg in queue_data:
        status = msg.get('status', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1

    print('Status breakdown:')
    for status, count in statuses.items():
        print(f'  {status}: {count}')

    # Check for our test message
    test_found = False
    for msg in queue_data:
        content = msg.get('message', {}).get('content', '')
        if 'KeyError fix verification' in content:
            test_found = True
            print(f'Test message status: {msg.get("status")}')
            break

    if not test_found:
        print('Test message not found in queue (may have been processed)')

    # Check for delivered messages
    delivered = [msg for msg in queue_data if msg.get('status') == 'DELIVERED']
    if delivered:
        print(f'\\n✅ {len(delivered)} messages have been delivered!')
        for msg in delivered[:2]:  # Show first 2
            recipient = msg.get('message', {}).get('recipient', 'unknown')
            print(f'  ✓ Delivered to {recipient}')
    else:
        print('\\n⏳ No messages delivered yet')
else:
    print('Queue file not found')