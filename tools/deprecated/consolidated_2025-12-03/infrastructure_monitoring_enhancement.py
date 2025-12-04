#!/usr/bin/env python3
"""
Infrastructure Monitoring Enhancement
=====================================

Enhanced monitoring for message compression, Discord bot, and system health.
Integrates compression health checks with infrastructure monitoring.

Author: Agent-3 (Infrastructure & DevOps) - JET FUEL AUTONOMOUS MODE
Created: 2025-01-27
Priority: CRITICAL
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InfrastructureMonitoringEnhancement:
    """Enhanced infrastructure monitoring system."""

    def __init__(self):
        """Initialize monitoring enhancement."""
        self.monitoring_data = {}

    def check_message_compression_health(self) -> dict[str, Any]:
        """Check message compression system health."""
        try:
            result = subprocess.run(
                ["python", "tools/message_compression_health_check.py", "--json"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"status": "error", "error": result.stderr}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_discord_bot_status(self) -> dict[str, Any]:
        """Check Discord bot process status."""
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            processes = result.stdout.lower()
            bot_running = "start_discord_bot" in processes or "unified_discord_bot" in processes
            
            return {
                "status": "running" if bot_running else "stopped",
                "bot_running": bot_running,
                "checked_at": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_message_history_size(self) -> dict[str, Any]:
        """Check message history file size and growth."""
        history_file = Path("data/message_history.json")
        archive_dir = Path("data/message_history_archive")
        
        if not history_file.exists():
            return {"status": "error", "error": "History file not found"}
        
        file_size = history_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        archive_files = list(archive_dir.glob("*.json")) if archive_dir.exists() else []
        archive_size = sum(f.stat().st_size for f in archive_files)
        archive_size_mb = archive_size / (1024 * 1024)
        
        return {
            "history_file_size_mb": round(file_size_mb, 2),
            "archive_files_count": len(archive_files),
            "archive_size_mb": round(archive_size_mb, 2),
            "total_size_mb": round(file_size_mb + archive_size_mb, 2),
            "status": "healthy" if file_size_mb < 10 else "warning",
        }

    def comprehensive_monitoring_report(self) -> dict[str, Any]:
        """Generate comprehensive infrastructure monitoring report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "compression_health": self.check_message_compression_health(),
            "discord_bot_status": self.check_discord_bot_status(),
            "message_history": self.check_message_history_size(),
        }
        
        # Overall status
        issues = []
        if report["compression_health"].get("status") not in ["healthy", "unknown"]:
            issues.append("Compression health issue")
        if report["discord_bot_status"].get("status") != "running":
            issues.append("Discord bot not running")
        if report["message_history"].get("status") == "warning":
            issues.append("Message history size warning")
        
        report["overall_status"] = "healthy" if not issues else "warning"
        report["issues"] = issues
        
        return report

    def print_monitoring_report(self) -> None:
        """Print human-readable monitoring report."""
        report = self.comprehensive_monitoring_report()
        
        print("\n" + "="*70)
        print("🔍 INFRASTRUCTURE MONITORING REPORT")
        print("="*70)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Overall Status: {report['overall_status'].upper()}")
        print()
        
        # Compression Health
        comp = report["compression_health"]
        print("📦 MESSAGE COMPRESSION:")
        print(f"  Status: {comp.get('status', 'unknown')}")
        if "metrics" in comp:
            m = comp["metrics"]
            print(f"  Total Messages: {m.get('total_messages', 0)}")
            print(f"  File Size: {m.get('file_size_mb', 0)} MB")
            print(f"  Archive Files: {m.get('archive_files', 0)}")
        print()
        
        # Discord Bot
        bot = report["discord_bot_status"]
        print("🤖 DISCORD BOT:")
        print(f"  Status: {bot.get('status', 'unknown')}")
        print(f"  Running: {bot.get('bot_running', False)}")
        print()
        
        # Message History
        hist = report["message_history"]
        print("📊 MESSAGE HISTORY:")
        print(f"  History Size: {hist.get('history_file_size_mb', 0)} MB")
        print(f"  Archive Size: {hist.get('archive_size_mb', 0)} MB")
        print(f"  Total Size: {hist.get('total_size_mb', 0)} MB")
        print()
        
        if report["issues"]:
            print("⚠️  ISSUES:")
            for issue in report["issues"]:
                print(f"  • {issue}")
            print()
        
        print("="*70 + "\n")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Infrastructure Monitoring Enhancement")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    monitor = InfrastructureMonitoringEnhancement()
    
    if args.json:
        report = monitor.comprehensive_monitoring_report()
        print(json.dumps(report, indent=2))
    else:
        monitor.print_monitoring_report()


if __name__ == "__main__":
    main()




