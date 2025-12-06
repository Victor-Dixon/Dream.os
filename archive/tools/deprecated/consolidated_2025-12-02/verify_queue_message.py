#!/usr/bin/env python3
"""Verify message in queue."""
import json
from pathlib import Path

queue_file = Path("message_queue/queue.json")
if queue_file.exists():
    data = json.loads(queue_file.read_text())
    if data:
        last_msg = data[-1]
        print("✅ Last message in queue:")
        print(f"  Recipient: {last_msg['message']['recipient']}")
        print(f"  Sender: {last_msg['message']['sender']}")
        print(f"  Status: {last_msg.get('status', 'N/A')}")
        print(f"  Content preview: {last_msg['message']['content'][:100]}...")
    else:
        print("❌ Queue is empty")
else:
    print("❌ Queue file not found")


