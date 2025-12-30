#!/usr/bin/env python3
"""
System Health Dashboard
======================

Comprehensive dashboard for monitoring Agent Cellphone V2 system health.

Author: Agent-2 (Architecture & Design)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)

<!-- SSOT Domain: tools -->
"""

import json
import time
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

class SystemHealthDashboard:
    """Comprehensive system health monitoring dashboard."""

    def __init__(self):
        self.services = {
            "message_queue": {"pid": None, "status": "unknown", "last_check": None},
            "discord_bot": {"pid": None, "status": "unknown", "last_check": None},
            "twitch_bot": {"pid": None, "status": "unknown", "last_check": None}
        }
        self.alerts = []
        self.monitoring = False
        self.check_interval = 30  # seconds
        self.logger = logging.getLogger(__name__)

    def start_monitoring(self):
        """Start the health monitoring."""
        if self.monitoring:
            return

        self.monitoring = True
        self.logger.info("System health monitoring started")

        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()

    def stop_monitoring(self):
        """Stop the health monitoring."""
        self.monitoring = False
        self.logger.info("System health monitoring stopped")

    def update_service_pid(self, service_name: str, pid: int):
        """Update the PID for a service."""
        if service_name in self.services:
            self.services[service_name]["pid"] = pid
            self.services[service_name]["last_check"] = datetime.now()
            self.logger.info(f"Updated {service_name} PID: {pid}")

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._check_all_services()
                self._check_system_resources()
                self._check_agent_coordinates()
                self._cleanup_old_alerts()

                time.sleep(self.check_interval)

            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(self.check_interval)

    def _check_all_services(self):
        """Check the health of all services."""
        for service_name, service_info in self.services.items():
            pid = service_info["pid"]

            if pid is None:
                self._add_alert(f"{service_name}: No PID assigned", "warning")
                continue

            if psutil.pid_exists(pid):
                # Check if process is actually running (not zombie)
                try:
                    process = psutil.Process(pid)
                    if process.status() == psutil.STATUS_ZOMBIE:
                        self._add_alert(f"{service_name}: Zombie process (PID: {pid})", "critical")
                        service_info["status"] = "zombie"
                    else:
                        service_info["status"] = "running"
                        cpu_percent = process.cpu_percent(interval=0.1)
                        memory_mb = process.memory_info().rss / 1024 / 1024

                        # Check for high resource usage
                        if cpu_percent > 80:
                            self._add_alert(".1f")
                        if memory_mb > 400:
                            self._add_alert(".1f")

                except psutil.NoSuchProcess:
                    self._add_alert(f"{service_name}: Process not found (PID: {pid})", "critical")
                    service_info["status"] = "not_found"
                except Exception as e:
                    self._add_alert(f"{service_name}: Error checking process: {e}", "error")
            else:
                self._add_alert(f"{service_name}: Process not running (PID: {pid})", "critical")
                service_info["status"] = "stopped"

            service_info["last_check"] = datetime.now()

    def _check_system_resources(self):
        """Check overall system resources."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            if cpu_percent > 90:
                self._add_alert(".1f")
            if memory.percent > 90:
                self._add_alert(".1f")
            if disk.percent > 95:
                self._add_alert(".1f")

        except Exception as e:
            self._add_alert(f"System resource check failed: {e}", "error")

    def _check_agent_coordinates(self):
        """Check if agent coordinates are still valid."""
        try:
            # This would integrate with the coordinate calibration tool
            # For now, just check if PyAutoGUI is available
            import pyautogui
            screen_size = pyautogui.size()

            # Basic coordinate bounds check (simplified)
            agent_coords = {
                "Agent-1": (-1269, 481),
                "Agent-2": (-308, 480),
                "Agent-3": (-1269, 1001),
                "Agent-4": (-308, 1000),
                "Agent-5": (652, 421),
                "Agent-6": (1612, 419),
                "Agent-7": (653, 940),
                "Agent-8": (1611, 941),
            }

            out_of_bounds = []
            for agent, (x, y) in agent_coords.items():
                if not (0 <= x < screen_size.width and 0 <= y < screen_size.height):
                    out_of_bounds.append(agent)

            if out_of_bounds:
                self._add_alert(f"Agents out of screen bounds: {', '.join(out_of_bounds)}", "warning")

        except ImportError:
            self._add_alert("PyAutoGUI not available for coordinate checks", "warning")
        except Exception as e:
            self._add_alert(f"Coordinate check failed: {e}", "error")

    def _add_alert(self, message: str, level: str):
        """Add an alert to the dashboard."""
        alert = {
            "timestamp": datetime.now(),
            "message": message,
            "level": level,  # critical, warning, error, info
            "acknowledged": False
        }

        self.alerts.append(alert)
        self.logger.log(getattr(logging, level.upper(), logging.INFO), message)

    def _cleanup_old_alerts(self):
        """Clean up old alerts (older than 1 hour)."""
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.alerts = [alert for alert in self.alerts if alert["timestamp"] > cutoff_time]

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data."""
        return {
            "timestamp": datetime.now(),
            "services": self.services,
            "alerts": self.alerts[-20:],  # Last 20 alerts
            "system_info": self._get_system_info(),
            "summary": self._get_summary()
        }

    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform
            }
        except Exception:
            return {"error": "System info unavailable"}

    def _get_summary(self) -> Dict[str, Any]:
        """Get dashboard summary."""
        critical_alerts = len([a for a in self.alerts if a["level"] == "critical"])
        warning_alerts = len([a for a in self.alerts if a["level"] == "warning"])

        running_services = len([s for s in self.services.values() if s["status"] == "running"])
        total_services = len(self.services)

        return {
            "services_running": f"{running_services}/{total_services}",
            "active_alerts": len(self.alerts),
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "overall_status": "healthy" if critical_alerts == 0 else "critical" if critical_alerts > 2 else "warning"
        }

    def print_dashboard(self):
        """Print the current dashboard to console."""
        data = self.get_dashboard_data()

        print("\n" + "="*70)
        print("🩺 AGENT CELLPHONE V2 - SYSTEM HEALTH DASHBOARD")
        print("="*70)
        print(f"📅 Time: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

        # Summary
        summary = data["summary"]
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "critical": "❌"
        }.get(summary["overall_status"], "❓")

        print(f"🏥 Overall Status: {status_emoji} {summary['overall_status'].title()}")
        print(f"🔧 Services Running: {summary['services_running']}")
        print(f"🚨 Active Alerts: {summary['active_alerts']} (Critical: {summary['critical_alerts']}, Warnings: {summary['warning_alerts']})")

        # Services
        print(f"\n🔧 SERVICE STATUS:")
        for service_name, service_info in data["services"].items():
            status = service_info["status"]
            pid = service_info["pid"] or "N/A"
            last_check = service_info["last_check"]

            status_emoji = {
                "running": "✅",
                "stopped": "❌",
                "zombie": "👻",
                "not_found": "❓",
                "unknown": "❓"
            }.get(status, "❓")

            check_time = last_check.strftime("%H:%M:%S") if last_check else "Never"
            print(f"  {status_emoji} {service_name}: {status.title()} (PID: {pid}, Last Check: {check_time})")

        # Recent Alerts
        if data["alerts"]:
            print(f"\n🚨 RECENT ALERTS (Last {len(data['alerts'])}):")
            for alert in data["alerts"][-10:]:  # Show last 10
                level_emoji = {
                    "critical": "🚨",
                    "warning": "⚠️",
                    "error": "❌",
                    "info": "ℹ️"
                }.get(alert["level"], "❓")

                timestamp = alert["timestamp"].strftime("%H:%M:%S")
                print(f"  {level_emoji} [{timestamp}] {alert['message']}")

        # System Info
        if "error" not in data["system_info"]:
            sys_info = data["system_info"]
            print(f"\n💻 SYSTEM INFO:")
            print(f"  CPU: {sys_info['cpu_percent']:.1f}%")
            print(f"  Memory: {sys_info['memory_percent']:.1f}%")
            print(f"  Disk: {sys_info['disk_percent']:.1f}%")
            print(f"  Python: {sys_info['python_version']}")
            print(f"  Platform: {sys_info['platform']}")

        print("="*70)


def main():
    """CLI interface for system health dashboard."""
    import argparse

    parser = argparse.ArgumentParser(description="System Health Dashboard")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring mode")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--update-pid", nargs=2, metavar=("SERVICE", "PID"), help="Update service PID")

    args = parser.parse_args()

    dashboard = SystemHealthDashboard()

    if args.update_pid:
        service, pid = args.update_pid
        try:
            dashboard.update_service_pid(service, int(pid))
            print(f"✅ Updated {service} PID to {pid}")
        except ValueError:
            print("❌ Invalid PID format")

    if args.monitor:
        print("🔍 Starting system health monitoring...")
        dashboard.start_monitoring()
        try:
            while True:
                dashboard.print_dashboard()
                time.sleep(10)
        except KeyboardInterrupt:
            dashboard.stop_monitoring()
            print("\n🛑 Monitoring stopped")

    elif args.status:
        dashboard.print_dashboard()

    else:
        print("Use --status to show current status or --monitor to start monitoring")
        print("Example: python tools/system_health_dashboard.py --status")


if __name__ == "__main__":
    main()


