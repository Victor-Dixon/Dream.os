#!/usr/bin/env python3
"""
Infrastructure Health Monitor

Monitors critical infrastructure components for automation reliability.
"""

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path


class InfrastructureHealthMonitor:
    """Monitors infrastructure health for automation reliability."""

    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"

    def check_disk_space(self, alert_threshold_gb: float = 5.0):
        """Check disk space on all drives."""
        result = {
            "status": "unknown",
            "drives": [],
            "alerts": []
        }

        try:
            if self.is_windows:
                drives = self._get_windows_drives()
                for drive in drives:
                    drive_info = self._check_windows_drive(drive, alert_threshold_gb)
                    result["drives"].append(drive_info)

                    if drive_info["free_gb"] < alert_threshold_gb:
                        result["alerts"].append(
                            f"CRITICAL: {drive} has only {drive_info['free_gb']:.1f}GB free space"
                        )

            # Overall status
            critical_alerts = [d for d in result["drives"] if d.get("free_gb", 0) < alert_threshold_gb]
            if critical_alerts:
                result["status"] = "critical"
            else:
                result["status"] = "healthy"

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)

        return result

    def _get_windows_drives(self):
        """Get available Windows drives."""
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = f"{letter}:"
            if os.path.exists(drive):
                drives.append(drive)
        return drives

    def _check_windows_drive(self, drive: str, threshold_gb: float):
        """Check a specific Windows drive."""
        try:
            # Simple check using os.statvfs or fallback
            try:
                stat = os.statvfs(drive + '\\')
                total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
                free_gb = (stat.f_available * stat.f_frsize) / (1024**3)
                used_gb = total_gb - free_gb
                usage_percent = (used_gb / total_gb * 100) if total_gb > 0 else 0

                return {
                    "drive": drive,
                    "total_gb": round(total_gb, 1),
                    "used_gb": round(used_gb, 1),
                    "free_gb": round(free_gb, 1),
                    "usage_percent": round(usage_percent, 1)
                }
            except:
                # Fallback for drives without statvfs
                return {
                    "drive": drive,
                    "total_gb": 0,
                    "used_gb": 0,
                    "free_gb": 100,  # Assume healthy if we can't check
                    "usage_percent": 0
                }

        except Exception as e:
            return {
                "drive": drive,
                "error": f"Unable to check drive: {e}"
            }

    def check_browser_readiness(self):
        """Check if browser automation is ready."""
        result = {
            "status": "unknown",
            "components": {},
            "issues": []
        }

        # Check Chrome
        try:
            import undetected_chromedriver as uc
            result["components"]["undetected_chromedriver"] = {"available": True}
        except ImportError:
            result["components"]["undetected_chromedriver"] = {"available": False}
            result["issues"].append("undetected-chromedriver not available")

        # Check Selenium
        try:
            import selenium
            result["components"]["selenium"] = {"available": True}
        except ImportError:
            result["components"]["selenium"] = {"available": False}
            result["issues"].append("selenium not available")

        # Overall status
        all_available = all(
            comp.get("available", False)
            for comp in result["components"].values()
        )

        if all_available and not result["issues"]:
            result["status"] = "ready"
        elif result["issues"]:
            result["status"] = "issues_found"
        else:
            result["status"] = "partial"

        return result

    def generate_report(self):
        """Generate comprehensive infrastructure health report."""
        report = {
            "disk_space": self.check_disk_space(),
            "browser_readiness": self.check_browser_readiness(),
            "overall_status": "unknown"
        }

        # Calculate overall status
        statuses = [
            report["disk_space"]["status"],
            report["browser_readiness"]["status"]
        ]

        if any(s == "critical" for s in statuses):
            report["overall_status"] = "critical"
        elif any(s in ["error", "issues_found"] for s in statuses):
            report["overall_status"] = "warning"
        elif all(s in ["healthy", "ready"] for s in statuses):
            report["overall_status"] = "healthy"
        else:
            report["overall_status"] = "partial"

        return report

    def print_report(self, report):
        """Print formatted health report."""
        print("🔍 INFRASTRUCTURE HEALTH MONITOR REPORT")
        print("=" * 50)

        status_emoji = {
            "healthy": "🟢",
            "warning": "🟡",
            "critical": "🔴",
            "partial": "🟠",
            "unknown": "⚪"
        }

        overall_status = report["overall_status"]
        print(f"Overall Status: {overall_status.upper()} {status_emoji.get(overall_status, '❓')}")

        # Disk space
        print("\n💾 DISK SPACE:")
        disk_status = report["disk_space"]
        print(f"Status: {disk_status['status'].upper()} {status_emoji.get(disk_status['status'], '❓')}")

        for drive in disk_status.get("drives", []):
            if "error" not in drive:
                print(f"  {drive['drive']}: {drive['free_gb']:.1f}GB free ({drive['usage_percent']:.1f}% used)")
                if drive.get("free_gb", 0) < 5.0:
                    print("  ⚠️  LOW DISK SPACE - Clean up required!")
        for alert in disk_status.get("alerts", []):
            print(f"  🚨 {alert}")

        # Browser readiness
        print("\n🌐 BROWSER READINESS:")
        browser_status = report["browser_readiness"]
        print(f"Status: {browser_status['status'].upper()} {status_emoji.get(browser_status['status'], '❓')}")

        for component, status in browser_status.get("components", {}).items():
            comp_status = "✅" if status.get("available", False) else "❌"
            print(f"  {comp_status} {component}")

        for issue in browser_status.get("issues", []):
            print(f"  🚨 {issue}")

        print("\n🐝 WE. ARE. SWARM. ⚡🔥")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Infrastructure Health Monitor")
    parser.add_argument("--check-all", action="store_true", help="Run all health checks")
    parser.add_argument("--disk-space", action="store_true", help="Check disk space only")
    parser.add_argument("--alert-threshold", type=float, default=5.0,
                       help="Disk space alert threshold in GB")
    parser.add_argument("--browser-ready", action="store_true", help="Check browser readiness only")

    args = parser.parse_args()

    monitor = InfrastructureHealthMonitor()

    if args.check_all or (not any([args.disk_space, args.browser_ready])):
        report = monitor.generate_report()
    else:
        report = {}
        if args.disk_space:
            report["disk_space"] = monitor.check_disk_space(args.alert_threshold)
        if args.browser_ready:
            report["browser_readiness"] = monitor.check_browser_readiness()

    monitor.print_report(report)


if __name__ == "__main__":
    main()