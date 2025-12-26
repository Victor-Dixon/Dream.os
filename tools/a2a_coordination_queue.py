#!/usr/bin/env python3
"""
A2A Coordination Queue Manager
==============================

Tool to manage A2A coordination messages when rate-limited.
Queues throttled messages for automatic retry and provides visibility.

Use Case: During this session, multiple A2A coordination messages were
throttled by the 30-minute rate limit. This tool queues them for retry
and provides status visibility.

V2 Compliance | Author: Agent-6 | Date: 2025-12-25
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

QUEUE_FILE = project_root / "runtime" / "coordination_queue.json"
THROTTLE_MINUTES = 30


def load_queue() -> dict:
    """Load the coordination queue from file."""
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    return {"pending": [], "sent": [], "failed": []}


def save_queue(queue: dict) -> None:
    """Save the coordination queue to file."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2, default=str)


def add_to_queue(sender: str, recipient: str, message: str, category: str = "a2a") -> None:
    """Add a message to the coordination queue."""
    queue = load_queue()
    
    entry = {
        "id": f"coord_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "sender": sender,
        "recipient": recipient,
        "message": message,
        "category": category,
        "queued_at": datetime.now().isoformat(),
        "retry_after": (datetime.now() + timedelta(minutes=THROTTLE_MINUTES)).isoformat(),
        "attempts": 0
    }
    
    queue["pending"].append(entry)
    save_queue(queue)
    
    print(f"✅ Message queued for {recipient}")
    print(f"   Retry after: {entry['retry_after']}")
    print(f"   Queue ID: {entry['id']}")


def check_ready() -> list:
    """Check which messages are ready to send."""
    queue = load_queue()
    now = datetime.now()
    ready = []
    
    for entry in queue["pending"]:
        retry_after = datetime.fromisoformat(entry["retry_after"])
        if now >= retry_after:
            ready.append(entry)
    
    return ready


def process_queue() -> None:
    """Process all ready messages in the queue."""
    queue = load_queue()
    now = datetime.now()
    
    ready = []
    still_pending = []
    
    for entry in queue["pending"]:
        retry_after = datetime.fromisoformat(entry["retry_after"])
        if now >= retry_after:
            ready.append(entry)
        else:
            still_pending.append(entry)
    
    if not ready:
        print("📭 No messages ready to send")
        print(f"   Pending: {len(still_pending)}")
        if still_pending:
            next_ready = min(datetime.fromisoformat(e["retry_after"]) for e in still_pending)
            print(f"   Next ready: {next_ready.strftime('%H:%M:%S')}")
        return
    
    print(f"📬 {len(ready)} message(s) ready to send")
    
    for entry in ready:
        print(f"\n🚀 Sending to {entry['recipient']}...")
        entry["attempts"] += 1
        
        # Try to send using messaging CLI
        try:
            import subprocess
            result = subprocess.run(
                [
                    sys.executable, "-m", "src.services.messaging_cli",
                    "--agent", entry["recipient"],
                    "--message", entry["message"],
                    "--category", entry["category"],
                    "--sender", entry["sender"]
                ],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(project_root)
            )
            
            if result.returncode == 0 and "Message sent" in result.stdout:
                print(f"   ✅ Sent successfully!")
                entry["sent_at"] = datetime.now().isoformat()
                queue["sent"].append(entry)
            else:
                if "throttled" in result.stdout.lower() or "rate limit" in result.stdout.lower():
                    print(f"   ⏳ Still throttled, requeueing...")
                    entry["retry_after"] = (datetime.now() + timedelta(minutes=THROTTLE_MINUTES)).isoformat()
                    still_pending.append(entry)
                else:
                    print(f"   ❌ Failed: {result.stderr or result.stdout}")
                    entry["error"] = result.stderr or result.stdout
                    queue["failed"].append(entry)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            entry["error"] = str(e)
            queue["failed"].append(entry)
    
    queue["pending"] = still_pending
    save_queue(queue)
    
    print(f"\n📊 Queue Status:")
    print(f"   Pending: {len(queue['pending'])}")
    print(f"   Sent: {len(queue['sent'])}")
    print(f"   Failed: {len(queue['failed'])}")


def show_status() -> None:
    """Show current queue status."""
    queue = load_queue()
    now = datetime.now()
    
    print("📊 A2A COORDINATION QUEUE STATUS")
    print("=" * 50)
    
    print(f"\n📬 Pending: {len(queue['pending'])}")
    for entry in queue["pending"]:
        retry_after = datetime.fromisoformat(entry["retry_after"])
        remaining = retry_after - now
        if remaining.total_seconds() > 0:
            mins = int(remaining.total_seconds() / 60)
            secs = int(remaining.total_seconds() % 60)
            status = f"ready in {mins}m {secs}s"
        else:
            status = "READY"
        print(f"   • {entry['sender']} → {entry['recipient']}: {status}")
    
    print(f"\n✅ Sent: {len(queue['sent'])}")
    for entry in queue["sent"][-5:]:  # Show last 5
        print(f"   • {entry['sender']} → {entry['recipient']} at {entry.get('sent_at', 'unknown')}")
    
    print(f"\n❌ Failed: {len(queue['failed'])}")
    for entry in queue["failed"][-5:]:  # Show last 5
        print(f"   • {entry['sender']} → {entry['recipient']}: {entry.get('error', 'unknown error')[:50]}")


def clear_queue(queue_type: str = "all") -> None:
    """Clear the queue."""
    queue = load_queue()
    
    if queue_type in ["all", "pending"]:
        queue["pending"] = []
    if queue_type in ["all", "sent"]:
        queue["sent"] = []
    if queue_type in ["all", "failed"]:
        queue["failed"] = []
    
    save_queue(queue)
    print(f"✅ Cleared {queue_type} queue")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="A2A Coordination Queue Manager - Handle rate-limited messages"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add message to queue")
    add_parser.add_argument("--sender", "-s", required=True, help="Sender agent ID")
    add_parser.add_argument("--recipient", "-r", required=True, help="Recipient agent ID")
    add_parser.add_argument("--message", "-m", required=True, help="Message content")
    add_parser.add_argument("--category", "-c", default="a2a", help="Message category")
    
    # Status command
    subparsers.add_parser("status", help="Show queue status")
    
    # Process command
    subparsers.add_parser("process", help="Process ready messages")
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear queue")
    clear_parser.add_argument("--type", "-t", choices=["all", "pending", "sent", "failed"], 
                              default="all", help="Queue type to clear")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_to_queue(args.sender, args.recipient, args.message, args.category)
    elif args.command == "status":
        show_status()
    elif args.command == "process":
        process_queue()
    elif args.command == "clear":
        clear_queue(args.type)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

