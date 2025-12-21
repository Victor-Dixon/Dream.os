#!/usr/bin/env python3
"""
Check Message Queue Status
===========================

<!-- SSOT Domain: tools -->

Quick status check for message queue.

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-12-21
License: MIT
"""

import json
from pathlib import Path

QUEUE_FILE = Path("message_queue/queue.json")

def main():
    """Check queue status."""
    if not QUEUE_FILE.exists():
        print("ℹ️  Queue file does not exist")
        return
    
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Queue format is a list, not a dict
        if isinstance(data, list):
            messages = data
        elif isinstance(data, dict):
            messages = data.get("messages", [])
        else:
            messages = []
        
        print("📊 Message Queue Status")
        print("=" * 60)
        print(f"Total messages: {len(messages)}")
        
        if messages:
            status_counts = {}
            for msg in messages:
                if isinstance(msg, dict):
                    status = msg.get("status", "UNKNOWN")
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            print("\nStatus breakdown:")
            for status, count in sorted(status_counts.items()):
                print(f"  {status}: {count}")
        else:
            print("\n✅ Queue is empty - ready for new messages")
        
    except Exception as e:
        print(f"❌ Error reading queue: {e}")

if __name__ == "__main__":
    main()
