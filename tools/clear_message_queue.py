#!/usr/bin/env python3
"""
Clear Message Queue
===================

Utility script to clear the message queue for testing/debugging purposes.

Usage:
    python tools/clear_message_queue.py
    python tools/clear_message_queue.py --backup  # Create backup before clearing
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import shutil

def clear_queue(backup: bool = False) -> bool:
    """Clear the message queue.
    
    Args:
        backup: If True, create a backup before clearing
        
    Returns:
        True if successful, False otherwise
    """
    queue_file = Path("message_queue/queue.json")
    
    if not queue_file.exists():
        print("⚠️  Queue file not found - nothing to clear")
        return False
    
    # Read current queue
    try:
        with open(queue_file, "r", encoding="utf-8") as f:
            current_data = json.load(f)
        entry_count = len(current_data.get("entries", []))
    except Exception as e:
        print(f"❌ Error reading queue: {e}")
        return False
    
    # Create backup if requested
    if backup and entry_count > 0:
        backup_file = queue_file.parent / f"queue_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            shutil.copy2(queue_file, backup_file)
            print(f"✅ Backup created: {backup_file}")
        except Exception as e:
            print(f"⚠️  Failed to create backup: {e}")
    
    # Clear queue
    empty_queue = {
        "entries": [],
        "metadata": {
            "last_updated": datetime.now().isoformat(),
            "version": "1.0",
            "cleared_at": datetime.now().isoformat(),
            "previous_entry_count": entry_count
        }
    }
    
    try:
        with open(queue_file, "w", encoding="utf-8") as f:
            json.dump(empty_queue, f, indent=2)
        print(f"✅ Queue cleared successfully")
        print(f"   Previous entries: {entry_count}")
        print(f"   Current entries: 0")
        return True
    except Exception as e:
        print(f"❌ Error clearing queue: {e}")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Clear message queue")
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backup before clearing"
    )
    args = parser.parse_args()
    
    print("=" * 70)
    print("CLEAR MESSAGE QUEUE")
    print("=" * 70)
    print()
    
    success = clear_queue(backup=args.backup)
    
    print()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

