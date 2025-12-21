#!/usr/bin/env python3
"""
Clear Message Queue - Remove all pending messages
=================================================

<!-- SSOT Domain: tools -->

Clears the message queue by backing up current queue and creating empty queue.

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-12-21
License: MIT
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

QUEUE_FILE = Path("message_queue/queue.json")
QUEUE_DIR = Path("message_queue")


def backup_queue():
    """Create backup of current queue."""
    if not QUEUE_FILE.exists():
        print("⚠️  Queue file not found - nothing to backup")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = QUEUE_DIR / f"queue_backup_clear_{timestamp}.json"
    
    shutil.copy2(QUEUE_FILE, backup_path)
    print(f"✅ Queue backed up to: {backup_path}")
    return backup_path


def check_queue_status():
    """Check current queue status."""
    if not QUEUE_FILE.exists():
        print("ℹ️  Queue file does not exist")
        return {"total": 0, "pending": 0, "delivered": 0, "failed": 0}
    
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
        
        stats = {
            "total": len(messages),
            "pending": len([m for m in messages if isinstance(m, dict) and m.get("status") == "PENDING"]),
            "delivered": len([m for m in messages if isinstance(m, dict) and m.get("status") == "DELIVERED"]),
            "failed": len([m for m in messages if isinstance(m, dict) and m.get("status") == "FAILED"]),
        }
        
        print(f"📊 Queue Status:")
        print(f"  Total messages: {stats['total']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Delivered: {stats['delivered']}")
        print(f"  Failed: {stats['failed']}")
        
        return stats
    except Exception as e:
        print(f"❌ Error reading queue: {e}")
        return None


def clear_queue():
    """Clear the message queue."""
    # Backup first
    backup_path = backup_queue()
    
    # Create empty queue (format: list, not dict)
    empty_queue = []
    
    # Ensure directory exists
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write empty queue
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(empty_queue, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Queue cleared - empty queue created")
    print(f"   Backup saved to: {backup_path}")


def main():
    """Main execution."""
    print("🧹 Message Queue Cleanup")
    print("=" * 60)
    
    # Check current status
    stats = check_queue_status()
    
    if stats and stats["total"] > 0:
        print(f"\n⚠️  Queue contains {stats['total']} messages")
        print(f"   Pending: {stats['pending']}, Delivered: {stats['delivered']}, Failed: {stats['failed']}")
        
        response = input("\nClear queue? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            clear_queue()
            print("\n✅ Queue cleared successfully!")
        else:
            print("\n❌ Queue clear cancelled")
    else:
        print("\n✅ Queue is already empty - nothing to clear")


if __name__ == "__main__":
    import sys
    
    if "--force" in sys.argv:
        # Force clear without prompt
        backup_queue()
        clear_queue()
        print("✅ Queue force-cleared")
    else:
        main()

