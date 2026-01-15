#!/usr/bin/env python3
"""
Status Handler - CLI Command Handler
====================================

Handles status monitoring and health check commands for the main CLI.

V2 Compliant: Yes (<300 lines)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-07
"""

from typing import Dict, Any
from src.services.service_manager import ServiceManager


class StatusHandler:
    """Handles status-related CLI commands with enhanced health checks."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def handle_monitor_command(self, command_info: Dict[str, Any]) -> None:
        """Handle status command with enhanced health checks and troubleshooting."""
        print("🐝 dream.os - Service Status Report")
        print("=" * 50)

        all_status = self.service_manager.get_all_status()

        if not all_status:
            print("❌ No services configured or found.")
            print("\n💡 Quick Fix:")
            print("   1. Run setup: python setup.py")
            print("   2. Check config: python setup_wizard.py --validate")
            return

        # Count running services
        running_count = sum(1 for status in all_status.values() if status == "running")
        total_count = len(all_status)

        print(f"📊 Services: {running_count}/{total_count} running")
        print()

        # Display each service with enhanced info
        for service_name, status in all_status.items():
            status_icon = "🟢" if status == "running" else "🔴"
            info = self.service_manager.get_service_info(service_name)
            pid = info.get('pid', 'N/A')
            port = info.get('port', 'N/A')
            health = info.get('health', 'unknown')

            # Enhanced status display
            health_icon = "💚" if health == "healthy" else "💔" if health == "unhealthy" else "🤔"
            port_info = f" (Port: {port})" if port != 'N/A' else ""

            print(f"{status_icon} {service_name}: {status.upper()} {health_icon}{port_info}")
            if pid != 'N/A':
                print(f"   └─ PID: {pid}")

        print()

        # Overall health assessment
        if running_count == total_count:
            self._print_full_system_status()
        elif running_count > 0:
            self._print_partial_system_status()
        else:
            self._print_offline_system_status()

        # Troubleshooting section
        if running_count < total_count:
            self._print_troubleshooting_info(running_count)

        self._print_command_help()

    def _print_full_system_status(self) -> None:
        """Print status when all systems are operational."""
        print("🎉 All systems operational!")
        print("\n🚀 Ready to use:")
        print("   • Web Dashboard: http://localhost:8001")
        print("   • API Docs: http://localhost:8001/docs")
        print("   • Discord Bot: Ready for commands")

    def _print_partial_system_status(self) -> None:
        """Print status when some systems are operational."""
        print("⚠️ Partial system operational")
        print("   Some services are running, but not all.")

    def _print_offline_system_status(self) -> None:
        """Print status when no systems are operational."""
        print("❌ System offline")
        print("   No services are currently running.")

    def _print_troubleshooting_info(self, running_count: int) -> None:
        """Print troubleshooting information based on system state."""
        print("\n🔧 Troubleshooting:")
        if running_count == 0:
            print("   • Start services: python main.py --background")
            print("   • Check setup: python setup.py --validate")
        else:
            print("   • Check logs: tail -f logs/app.log")
            print("   • Restart failed services individually")
            print("   • Run health check: python scripts/health_check.py")

    def _print_command_help(self) -> None:
        """Print available commands for user reference."""
        print("\n💡 Commands:")
        print("   • Start all: python main.py --background")
        print("   • Stop all: python main.py --stop")
        print("   • Health check: python scripts/health_check.py")
        print("   • View logs: tail -f logs/app.log")


# Factory function for backward compatibility
def create_status_handler(service_manager: ServiceManager) -> StatusHandler:
    """Create and return a StatusHandler instance."""
    return StatusHandler(service_manager)