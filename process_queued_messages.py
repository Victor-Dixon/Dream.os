#!/usr/bin/env python3
"""
Process Queued Messages - Simulate Discord Bot Message Delivery
================================================================

This script processes messages from the unified messaging queue,
simulating what a Discord bot would do to deliver messages to agents.

Since we don't have Discord credentials in this environment, this script
will "deliver" messages by updating agent inboxes and logging deliveries.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List

def process_broadcast_messages():
    """Process broadcast messages from the queue."""
    queue_file = Path("ops/messaging/message_queue/queue.json")
    processed_dir = Path("ops/messaging/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    if not queue_file.exists():
        print("❌ Queue file not found")
        return 0

    try:
        with open(queue_file, 'r') as f:
            queue_data = json.load(f)

        if not isinstance(queue_data, list):
            print("❌ Invalid queue format")
            return 0

        processed_count = 0

        # Process each message in the queue
        for message in queue_data[:]:  # Copy to avoid modification issues
            message_id = message.get('id', f"msg_{datetime.now().timestamp()}")

            # Check if this is a broadcast message
            if message.get('type') == 'broadcast' or 'broadcast' in message.get('tags', []):
                recipient = message.get('recipient', 'unknown')
                content = message.get('content', '')

                print(f"📤 [BROADCAST DELIVERY] -> {recipient}")
                print(f"   Message: {content[:100]}{'...' if len(content) > 100 else ''}")

                # "Deliver" to agent inbox
                deliver_to_agent_inbox(message)

                # Move to processed
                processed_file = processed_dir / f"{message_id}.json"
                with open(processed_file, 'w') as f:
                    json.dump({
                        **message,
                        'processed_at': datetime.now().isoformat(),
                        'delivery_status': 'simulated_success'
                    }, f, indent=2)

                # Remove from queue
                queue_data.remove(message)
                processed_count += 1

        # Save updated queue
        with open(queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)

        return processed_count

    except Exception as e:
        print(f"❌ Error processing queue: {e}")
        return 0

def deliver_to_agent_inbox(message: Dict):
    """Deliver message to agent's inbox (simulate Discord delivery)."""
    recipient = message.get('recipient', 'unknown')
    content = message.get('content', '')
    sender = message.get('sender', 'system')

    # Map recipient to agent inbox
    agent_inbox_map = {
        'Agent-1': 'agent_workspaces/Agent-1/inbox/',
        'Agent-2': 'agent_workspaces/Agent-2/inbox/',
        'Agent-3': 'agent_workspaces/Agent-3/inbox/',
        'Agent-4': 'agent_workspaces/Agent-4/inbox/',
        'Agent-5': 'agent_workspaces/Agent-5/inbox/',
        'Agent-6': 'agent_workspaces/Agent-6/inbox/',
        'Agent-7': 'agent_workspaces/Agent-7/inbox/',
        'Agent-8': 'agent_workspaces/Agent-8/inbox/',
    }

    inbox_path = agent_inbox_map.get(recipient)
    if not inbox_path:
        print(f"⚠️  No inbox mapping for recipient: {recipient}")
        return

    inbox_dir = Path(inbox_path)
    inbox_dir.mkdir(parents=True, exist_ok=True)

    # Create message file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    message_file = inbox_dir / f"CAPTAIN_MESSAGE_{timestamp}_{message.get('id', 'broadcast')}.md"

    # Format as inbox message
    inbox_content = f"""# 🚨 CAPTAIN MESSAGE - BROADCAST

**From**: {sender}
**To**: {recipient}
**Priority**: {message.get('priority', 'normal')}
**Message ID**: {message.get('id', 'broadcast')}
**Timestamp**: {datetime.now().isoformat()}

---

{content}

---
*Message delivered via Unified Messaging Service (Simulated)*
"""

    with open(message_file, 'w', encoding='utf-8') as f:
        f.write(inbox_content)

    print(f"✅ Message delivered to: {message_file}")

def main():
    """Main processing function."""
    print("🤖 Processing Queued Messages (Discord Bot Simulation)")
    print("=" * 60)

    processed = process_broadcast_messages()

    print(f"\n📊 Processing Complete:")
    print(f"   Messages processed: {processed}")

    if processed > 0:
        print("✅ Messages successfully delivered to agent inboxes!")
        print("📬 Check agent_workspaces/*/inbox/ for delivered messages")
    else:
        print("ℹ️  No broadcast messages found in queue")

if __name__ == "__main__":
    main()