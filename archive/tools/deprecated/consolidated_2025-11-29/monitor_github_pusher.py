#!/usr/bin/env python3
"""
GitHub Pusher Monitor - Health Check & Monitoring Tool
======================================================

Monitors the GitHub Pusher Agent service and queue status.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.core.deferred_push_queue import get_deferred_push_queue

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_queue_health() -> Dict[str, Any]:
    """Check health of deferred push queue."""
    try:
        queue = get_deferred_push_queue()
        stats = queue.get_stats()
        
        # Calculate health score
        total = stats.get("total", 0)
        pending = stats.get("pending", 0)
        failed = stats.get("failed", 0)
        
        if total == 0:
            health_score = 100  # Empty queue = healthy
        else:
            # Health based on failure rate
            failure_rate = (failed / total) * 100 if total > 0 else 0
            health_score = max(0, 100 - failure_rate)
        
        health_status = "HEALTHY" if health_score >= 80 else "DEGRADED" if health_score >= 50 else "UNHEALTHY"
        
        return {
            "status": health_status,
            "score": health_score,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking queue health: {e}")
        return {
            "status": "ERROR",
            "score": 0,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def check_service_running() -> bool:
    """Check if GitHub Pusher service is running."""
    try:
        import psutil
        
        # Check for running python processes with github_pusher in command
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('github_pusher' in str(arg) for arg in cmdline):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False
    except ImportError:
        logger.warning("psutil not available - cannot check service status")
        return None
    except Exception as e:
        logger.error(f"Error checking service status: {e}")
        return None


def print_health_report(health: Dict[str, Any], service_running: bool = None):
    """Print formatted health report."""
    print("\n" + "=" * 70)
    print("📊 GITHUB PUSHER SERVICE - HEALTH REPORT")
    print("=" * 70)
    
    # Service status
    if service_running is True:
        print("✅ Service: RUNNING")
    elif service_running is False:
        print("❌ Service: NOT RUNNING")
    else:
        print("⚠️  Service: UNKNOWN (psutil not available)")
    
    # Queue health
    status = health.get("status", "UNKNOWN")
    score = health.get("score", 0)
    
    if status == "HEALTHY":
        print(f"✅ Queue Health: {status} (Score: {score:.1f}%)")
    elif status == "DEGRADED":
        print(f"⚠️  Queue Health: {status} (Score: {score:.1f}%)")
    else:
        print(f"❌ Queue Health: {status} (Score: {score:.1f}%)")
    
    # Queue statistics
    stats = health.get("stats", {})
    print(f"\n📦 Queue Statistics:")
    print(f"   Total: {stats.get('total', 0)}")
    print(f"   Pending: {stats.get('pending', 0)}")
    print(f"   Retrying: {stats.get('retrying', 0)}")
    print(f"   Failed: {stats.get('failed', 0)}")
    print(f"   Completed: {stats.get('completed', 0)}")
    
    # Timestamp
    timestamp = health.get("timestamp", "unknown")
    print(f"\n🕐 Last Check: {timestamp}")
    print("=" * 70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Monitor GitHub Pusher Agent service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check health once
  python tools/monitor_github_pusher.py

  # Continuous monitoring (every 30 seconds)
  python tools/monitor_github_pusher.py --watch --interval 30

  # JSON output
  python tools/monitor_github_pusher.py --json
        """
    )
    
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch mode: continuously monitor (default: check once)"
    )
    
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=30,
        help="Watch interval in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    if args.watch:
        # Continuous monitoring
        logger.info(f"👀 Watch mode: Checking every {args.interval}s (Ctrl+C to stop)")
        try:
            while True:
                health = check_queue_health()
                service_running = check_service_running()
                
                if args.json:
                    output = {
                        "health": health,
                        "service_running": service_running
                    }
                    print(json.dumps(output, indent=2))
                else:
                    print_health_report(health, service_running)
                
                time.sleep(args.interval)
        except KeyboardInterrupt:
            logger.info("\n🛑 Monitoring stopped")
    else:
        # Single check
        health = check_queue_health()
        service_running = check_service_running()
        
        if args.json:
            output = {
                "health": health,
                "service_running": service_running
            }
            print(json.dumps(output, indent=2))
        else:
            print_health_report(health, service_running)


if __name__ == "__main__":
    main()

