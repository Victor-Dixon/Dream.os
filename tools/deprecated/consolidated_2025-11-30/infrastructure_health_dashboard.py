#!/usr/bin/env python3
"""
Infrastructure Health Dashboard
================================

Comprehensive infrastructure health monitoring dashboard.
Combines all monitoring tools into a single report.

Author: Agent-3 (Infrastructure & DevOps) - JET FUEL AUTONOMOUS MODE
Created: 2025-01-27
Priority: CRITICAL
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InfrastructureHealthDashboard:
    """Comprehensive infrastructure health dashboard."""

    def __init__(self):
        """Initialize dashboard."""
        self.reports = {}

    def check_all_systems(self) -> dict:
        """Check all infrastructure systems."""
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "systems": {},
            "overall_status": "unknown",
            "issues": [],
            "warnings": [],
        }
        
        # Message Compression Health
        try:
            result = subprocess.run(
                ["python", "tools/message_compression_health_check.py", "--json"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                dashboard["systems"]["compression"] = json.loads(result.stdout)
            else:
                dashboard["systems"]["compression"] = {"status": "error", "error": result.stderr}
        except Exception as e:
            dashboard["systems"]["compression"] = {"status": "error", "error": str(e)}
        
        # Infrastructure Monitoring
        try:
            result = subprocess.run(
                ["python", "tools/infrastructure_monitoring_enhancement.py", "--json"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                dashboard["systems"]["monitoring"] = json.loads(result.stdout)
            else:
                dashboard["systems"]["monitoring"] = {"status": "error", "error": result.stderr}
        except Exception as e:
            dashboard["systems"]["monitoring"] = {"status": "error", "error": str(e)}
        
        # Discord Bot Status
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            processes = result.stdout.lower()
            bot_running = "start_discord_bot" in processes or "unified_discord_bot" in processes
            dashboard["systems"]["discord_bot"] = {
                "status": "running" if bot_running else "stopped",
                "bot_running": bot_running,
            }
        except Exception as e:
            dashboard["systems"]["discord_bot"] = {"status": "error", "error": str(e)}
        
        # Determine overall status
        all_healthy = True
        for system_name, system_data in dashboard["systems"].items():
            status = system_data.get("status", "unknown")
            if status not in ["healthy", "running", "unknown"]:
                all_healthy = False
                if status == "error":
                    dashboard["issues"].append(f"{system_name}: {system_data.get('error', 'Unknown error')}")
                else:
                    dashboard["warnings"].append(f"{system_name}: {status}")
        
        dashboard["overall_status"] = "healthy" if all_healthy else "warning" if dashboard["warnings"] else "error"
        
        return dashboard

    def print_dashboard(self) -> None:
        """Print human-readable dashboard."""
        dashboard = self.check_all_systems()
        
        print("\n" + "="*70)
        print("🔍 INFRASTRUCTURE HEALTH DASHBOARD")
        print("="*70)
        print(f"Timestamp: {dashboard['timestamp']}")
        print(f"Overall Status: {dashboard['overall_status'].upper()}")
        print()
        
        # System Status
        for system_name, system_data in dashboard["systems"].items():
            status = system_data.get("status", "unknown")
            emoji = "🟢" if status in ["healthy", "running"] else "🟡" if status == "warning" else "🔴"
            print(f"{emoji} {system_name.upper()}: {status}")
            
            if "metrics" in system_data:
                metrics = system_data["metrics"]
                if system_name == "compression":
                    print(f"   Messages: {metrics.get('total_messages', 0)}")
                    print(f"   File Size: {metrics.get('file_size_mb', 0)} MB")
                elif system_name == "monitoring":
                    print(f"   Compression: {metrics.get('compression_health', {}).get('status', 'unknown')}")
                    print(f"   Discord Bot: {metrics.get('discord_bot_status', {}).get('status', 'unknown')}")
            elif system_name == "discord_bot":
                print(f"   Running: {system_data.get('bot_running', False)}")
            print()
        
        if dashboard["warnings"]:
            print("⚠️  WARNINGS:")
            for warning in dashboard["warnings"]:
                print(f"  • {warning}")
            print()
        
        if dashboard["issues"]:
            print("❌ ISSUES:")
            for issue in dashboard["issues"]:
                print(f"  • {issue}")
            print()
        
        print("="*70 + "\n")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Infrastructure Health Dashboard")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    dashboard = InfrastructureHealthDashboard()
    
    if args.json:
        report = dashboard.check_all_systems()
        print(json.dumps(report, indent=2))
    else:
        dashboard.print_dashboard()


if __name__ == "__main__":
    main()




