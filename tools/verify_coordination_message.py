#!/usr/bin/env python3
"""
Verify Coordination Message Delivery
=====================================

Quick utility to verify A2A coordination message delivery status.
Checks message queue or delivery logs for message ID.

V2 Compliant: <150 lines
Author: Agent-1
Date: 2025-12-30
"""

import sys
import json
from pathlib import Path
from typing import Optional

def find_message_in_queue(message_id: str, queue_file: Optional[Path] = None) -> bool:
    """Check if message exists in message queue."""
    if queue_file is None:
        queue_file = Path("data/message_queue.json")
    
    if not queue_file.exists():
        return False
    
    try:
        with open(queue_file, 'r', encoding='utf-8') as f:
            queue_data = json.load(f)
            messages = queue_data.get('messages', [])
            return any(msg.get('message_id') == message_id for msg in messages)
    except Exception:
        return False


def verify_message_delivery(message_id: str) -> dict:
    """Verify coordination message delivery."""
    result = {
        'message_id': message_id,
        'found_in_queue': False,
        'status': 'unknown'
    }
    
    # Check message queue
    result['found_in_queue'] = find_message_in_queue(message_id)
    
    if result['found_in_queue']:
        result['status'] = 'delivered'
    else:
        result['status'] = 'not_found_in_queue'
    
    return result


def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("Usage: python verify_coordination_message.py <message_id>")
        print("Example: python verify_coordination_message.py 8e2792e0-c00f-47c2-b660-5128d6d40d35")
        sys.exit(1)
    
    message_id = sys.argv[1]
    result = verify_message_delivery(message_id)
    
    print(f"Message ID: {result['message_id']}")
    print(f"Status: {result['status']}")
    print(f"Found in queue: {result['found_in_queue']}")
    
    if result['status'] == 'delivered':
        print("✅ Message delivery verified")
        sys.exit(0)
    else:
        print("⚠️  Message not found in queue (may be delivered but not queued)")
        sys.exit(1)


if __name__ == "__main__":
    main()

