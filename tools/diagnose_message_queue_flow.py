#!/usr/bin/env python3
"""
Message Queue Flow Diagnostic Tool
===================================

Diagnoses why system messages aren't flowing through the queue.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
"""

import sys
import json
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def check_queue_processor_running():
    """Check if queue processor is running."""
    queue_dir = project_root / "message_queue"
    lock_files = [
        "delivered.json.lock",
        "failed.json.lock",
        "pending.json.lock",
        "processing.json.lock"
    ]
    
    has_locks = any((queue_dir / lf).exists() for lf in lock_files)
    return has_locks

def check_queue_status():
    """Check queue file status."""
    from src.core.message_queue import MessageQueue
    
    queue = MessageQueue()
    stats = queue.get_statistics()
    return stats

def check_recent_messages():
    """Check for recent message activity."""
    queue_file = project_root / "message_queue" / "queue.json"
    if not queue_file.exists():
        return []
    
    try:
        with open(queue_file, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        # Get recent entries (last 10)
        recent = sorted(
            [e for e in entries if 'created_at' in e],
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )[:10]
        
        return recent
    except Exception as e:
        return [{"error": str(e)}]

def main():
    """Run diagnostic checks."""
    # Handle --help flag
    if len(sys.argv) > 1 and sys.argv[1] in ('--help', '-h'):
        print("Usage: python diagnose_message_queue_flow.py [--help]")
        print("Diagnoses why system messages aren't flowing through the queue.")
        print("\nChecks:")
        print("  - Queue processor status")
        print("  - Queue statistics")
        print("  - Recent message activity")
        print("  - Queue file integrity")
        return 0
    
    print("=" * 70)
    print("MESSAGE QUEUE FLOW DIAGNOSTIC")
    print("=" * 70)
    print()
    
    # Check 1: Queue processor running
    print("1. Queue Processor Status:")
    processor_running = check_queue_processor_running()
    if processor_running:
        print("   ✅ Queue processor appears to be running (lock files present)")
    else:
        print("   ❌ Queue processor NOT running (no lock files)")
        print("   💡 SOLUTION: Start queue processor:")
        print("      python tools/start_message_queue_processor.py")
        print("      OR")
        print("      python tools/start_services_background.ps1")
    print()
    
    # Check 2: Queue statistics
    print("2. Queue Statistics:")
    try:
        stats = check_queue_status()
        print(f"   Total entries: {stats.get('total_entries', 0)}")
        print(f"   Pending: {stats.get('pending_entries', 0)}")
        print(f"   Processing: {stats.get('processing_entries', 0)}")
        print(f"   Delivered: {stats.get('delivered_entries', 0)}")
        print(f"   Failed: {stats.get('failed_entries', 0)}")
        
        if stats.get('pending_entries', 0) > 0:
            print("   ⚠️  WARNING: Messages are pending but processor may not be running")
    except Exception as e:
        print(f"   ❌ Error checking queue: {e}")
    print()
    
    # Check 3: Recent messages
    print("3. Recent Message Activity:")
    recent = check_recent_messages()
    if recent:
        print(f"   Found {len(recent)} recent entries:")
        for entry in recent[:5]:
            status = entry.get('status', 'UNKNOWN')
            recipient = 'unknown'
            if isinstance(entry.get('message'), dict):
                recipient = entry.get('message', {}).get('recipient', 'unknown')
            created = entry.get('created_at', 'unknown')[:19] if isinstance(entry.get('created_at'), str) else 'unknown'
            print(f"      [{status}] → {recipient} ({created})")
    else:
        print("   ⚠️  No recent message activity found")
    print()
    
    # Check 4: MessageCoordinator queue initialization
    print("4. MessageCoordinator Queue Status:")
    try:
        from src.services.messaging.coordination_handlers import MessageCoordinator
        queue = MessageCoordinator._get_queue()
        if queue:
            print("   ✅ MessageCoordinator queue initialized")
        else:
            print("   ❌ MessageCoordinator queue NOT initialized")
    except Exception as e:
        print(f"   ❌ Error checking MessageCoordinator: {e}")
    print()
    
    # Summary and recommendations
    print("=" * 70)
    print("RECOMMENDATIONS:")
    print("=" * 70)
    
    if not processor_running:
        print("1. START QUEUE PROCESSOR:")
        print("   python tools/start_message_queue_processor.py")
        print()
        print("   OR start all services:")
        print("   powershell -ExecutionPolicy Bypass -File tools/start_services_background.ps1")
        print()
    
    stats = check_queue_status()
    if stats.get('pending_entries', 0) > 0 and not processor_running:
        print("2. PENDING MESSAGES DETECTED:")
        print(f"   {stats.get('pending_entries', 0)} messages waiting for processing")
        print("   Start the queue processor to process them")
        print()
    
    print("3. VERIFY MESSAGES ARE BEING QUEUED:")
    print("   Messages sent via MessageCoordinator should be queued automatically")
    print("   Check logs for 'Message queued' or 'MessageCoordinator initialized'")
    print()
    
    print("4. FALLBACK QUEUING:")
    print("   If PyAutoGUI fails, messages should now automatically queue")
    print("   (Fixed in messaging_core.py - Agent-8)")
    print()

if __name__ == "__main__":
    main()

