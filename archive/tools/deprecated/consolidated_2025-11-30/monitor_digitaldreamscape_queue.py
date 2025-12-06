#!/usr/bin/env python3
"""
DigitalDreamscape Queue Monitor - Continuous Monitoring Tool
============================================================

Monitors deferred push queue for DigitalDreamscape merge specifically.
Checks GitHub sandbox mode status and processes queue when access restored.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.core.deferred_push_queue import get_deferred_push_queue
from src.core.synthetic_github import GitHubSandboxMode

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_digitaldreamscape_entries(queue) -> List[Dict[str, Any]]:
    """Find all DigitalDreamscape-related entries in queue."""
    entries = []
    for entry in queue.pending_pushes:
        repo_name = entry.get('repo', '').lower()
        branch_name = entry.get('branch', '').lower()
        metadata_str = str(entry.get('metadata', {})).lower()
        
        # Check repo name, branch name, and metadata
        if any(term in repo_name or term in branch_name or term in metadata_str 
               for term in ['digitaldreamscape', 'digital', 'dreamscape', 'dreamvault']):
            entries.append(entry)
    return entries


def check_sandbox_mode() -> Dict[str, Any]:
    """Check GitHub sandbox mode status."""
    try:
        sandbox = GitHubSandboxMode()
        is_enabled = sandbox.is_enabled()
        
        return {
            "sandbox_mode_enabled": is_enabled,
            "github_available": not is_enabled,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking sandbox mode: {e}")
        return {
            "sandbox_mode_enabled": None,
            "github_available": None,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def get_queue_status() -> Dict[str, Any]:
    """Get comprehensive queue status."""
    try:
        queue = get_deferred_push_queue()
        stats = queue.get_stats()
        
        # Find DigitalDreamscape entries
        dd_entries = find_digitaldreamscape_entries(queue)
        
        return {
            "queue_stats": stats,
            "digitaldreamscape_entries": len(dd_entries),
            "digitaldreamscape_details": [
                {
                    "id": e.get("id", "unknown"),
                    "repo": e.get("repo", "unknown"),
                    "status": e.get("status", "unknown"),
                    "reason": e.get("reason", "unknown"),
                    "timestamp": e.get("timestamp", "unknown"),
                    "retry_count": e.get("retry_count", 0)
                }
                for e in dd_entries
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting queue status: {e}")
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def check_github_access() -> bool:
    """Check if GitHub API is accessible."""
    try:
        import requests
        response = requests.get("https://api.github.com/zen", timeout=5)
        return response.status_code == 200
    except Exception as e:
        logger.debug(f"GitHub API check failed: {e}")
        return False


def generate_status_report() -> str:
    """Generate human-readable status report."""
    queue_status = get_queue_status()
    sandbox_status = check_sandbox_mode()
    github_available = check_github_access()
    
    report = []
    report.append("=" * 70)
    report.append("📊 DIGITALDREAMSCAPE QUEUE MONITOR - STATUS REPORT")
    report.append("=" * 70)
    report.append("")
    
    # Queue Status
    report.append("📦 QUEUE STATUS:")
    stats = queue_status.get("queue_stats", {})
    report.append(f"  Total Pending: {stats.get('pending', 0)}")
    report.append(f"  Retrying: {stats.get('retrying', 0)}")
    report.append(f"  Failed: {stats.get('failed', 0)}")
    report.append(f"  DigitalDreamscape Entries: {queue_status.get('digitaldreamscape_entries', 0)}")
    report.append("")
    
    # DigitalDreamscape Details
    dd_details = queue_status.get("digitaldreamscape_details", [])
    if dd_details:
        report.append("🎯 DIGITALDREAMSCAPE ENTRIES:")
        for entry in dd_details:
            report.append(f"  - ID: {entry['id']}")
            report.append(f"    Repo: {entry['repo']}")
            report.append(f"    Status: {entry['status']}")
            report.append(f"    Reason: {entry['reason']}")
            report.append(f"    Retry Count: {entry['retry_count']}")
            report.append("")
    else:
        report.append("ℹ️  No DigitalDreamscape entries found in queue")
        report.append("")
    
    # Sandbox Mode Status
    report.append("🔒 SANDBOX MODE STATUS:")
    if sandbox_status.get("sandbox_mode_enabled"):
        report.append("  Status: 🔒 ENABLED (GitHub operations blocked)")
        report.append("  Action: Queue processing deferred")
    else:
        report.append("  Status: ✅ DISABLED (GitHub operations allowed)")
        report.append("  Action: Ready to process queue")
    report.append("")
    
    # GitHub Access
    report.append("🌐 GITHUB API ACCESS:")
    if github_available:
        report.append("  Status: ✅ AVAILABLE")
        report.append("  Action: Queue can be processed")
    else:
        report.append("  Status: ❌ UNAVAILABLE")
        report.append("  Action: Queue processing deferred")
    report.append("")
    
    # Recommendation
    report.append("💡 RECOMMENDATION:")
    if sandbox_status.get("sandbox_mode_enabled") or not github_available:
        report.append("  ⏳ WAIT: GitHub access not available yet")
        report.append("  🔄 Continue monitoring...")
    elif queue_status.get("digitaldreamscape_entries", 0) > 0:
        report.append("  ✅ PROCESS: GitHub available, entries in queue")
        report.append("  🚀 Ready to execute: python tools/github_pusher_agent.py")
    else:
        report.append("  ℹ️  NO ACTION: No DigitalDreamscape entries in queue")
    report.append("")
    
    report.append(f"📅 Report Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    return "\n".join(report)


def main():
    """Main monitoring loop."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Monitor DigitalDreamscape queue and GitHub sandbox mode",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--watch",
        "-w",
        action="store_true",
        help="Watch mode - continuously monitor (default: single check)"
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=60,
        help="Interval between checks in watch mode (seconds, default: 60)"
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output as JSON"
    )
    args = parser.parse_args()
    
    if args.watch:
        logger.info(f"🔄 Starting watch mode (checking every {args.interval}s)...")
        logger.info("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                if args.json:
                    status = get_queue_status()
                    status.update(check_sandbox_mode())
                    status["github_available"] = check_github_access()
                    print(json.dumps(status, indent=2))
                else:
                    report = generate_status_report()
                    print(report)
                    print()
                
                time.sleep(args.interval)
        except KeyboardInterrupt:
            logger.info("\n🛑 Monitoring stopped by user")
    else:
        # Single check
        if args.json:
            status = get_queue_status()
            status.update(check_sandbox_mode())
            status["github_available"] = check_github_access()
            print(json.dumps(status, indent=2))
        else:
            report = generate_status_report()
            print(report)


if __name__ == "__main__":
    main()

