#!/usr/bin/env python3
"""
Message Deduplication Manager - CLI Tool
========================================

Command-line utility for managing the message deduplication service.
Provides statistics, cleanup operations, and maintenance tools.

Usage:
    python tools/message_deduplication_manager.py stats
    python tools/message_deduplication_manager.py cleanup
    python tools/message_deduplication_manager.py check <message_id>

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2026-01-11
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging.message_deduplication_service import get_message_deduplication_service


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Message Deduplication Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/message_deduplication_manager.py stats
  python tools/message_deduplication_manager.py cleanup
  python tools/message_deduplication_manager.py check 12345678-1234-1234-1234-123456789abc
        """
    )

    parser.add_argument(
        "command",
        choices=["stats", "cleanup", "check"],
        help="Command to execute"
    )

    parser.add_argument(
        "message_id",
        nargs="?",
        help="Message ID to check (for 'check' command)"
    )

    args = parser.parse_args()

    try:
        service = get_message_deduplication_service()

        if args.command == "stats":
            stats = service.get_stats()
            print("📊 Message Deduplication Statistics:")
            print(f"   Total seen messages: {stats['total_seen']}")
            print(f"   Max entries: {stats['max_entries']}")
            print(f"   Retention: {stats['retention_hours']} hours")

        elif args.command == "cleanup":
            cleaned = service.force_cleanup()
            print(f"🧹 Cleaned up {cleaned} expired message entries")

        elif args.command == "check":
            if not args.message_id:
                print("❌ ERROR: message_id required for 'check' command")
                return 1

            is_duplicate = service.is_duplicate(args.message_id)
            status = "🚫 DUPLICATE" if is_duplicate else "✅ NEW MESSAGE"
            print(f"{status}: {args.message_id}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())