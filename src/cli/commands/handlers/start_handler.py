#!/usr/bin/env python3
"""
@file
@summary Execute service start flows for foreground and background modes.
@registry docs/recovery/recovery_registry.yaml#cli-start-handler
"""


import time
from typing import Dict, Any, List
from src.services.service_manager import ServiceManager


class StartHandler:
    """Handles start-related CLI commands."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def execute(self, command_info: Dict[str, Any]) -> None:
        """Execute start command based on command_info."""
        self.handle_start_services_command(command_info)

    def handle_start_services_command(self, command_info: Dict[str, Any]) -> None:
        """Handle start services command with enhanced feedback and health checks."""
        services = command_info.get('services', [])
        background = command_info.get('background', False)

        if not services:
            self._print_no_services_error()
            return

        self._start_services(services, background)

    def _start_services(self, services: List[str], background: bool) -> None:
        """Start the specified services."""
        mode = "background" if background else "foreground"
        print("🐝 dream.os - Starting Services")
        print("=" * 40)
        print(f"🚀 Launching {len(services)} service(s) in {mode} mode...")
        print()

        success_count = 0
        failed_services = []

        # Start each service
        for service_name in services:
            print(f"   Starting {service_name}...", end=" ")
            if self.service_manager.start_service(service_name, background=background):
                success_count += 1
                print("✅")
            else:
                failed_services.append(service_name)
                print("❌")

        print()
        print(f"📊 Results: {success_count}/{len(services)} services started successfully")

        if background:
            self._handle_background_mode(success_count, failed_services)
        else:
            self._handle_foreground_mode()

    def _handle_background_mode(self, success_count: int, failed_services: List[str]) -> None:
        """Handle background mode startup."""
        if success_count > 0:
            self._print_background_success_info()

            # Quick health verification
            print("\n🔍 Performing quick health check...")
            try:
                time.sleep(3)  # Give services time to start
                all_status = self.service_manager.get_all_status()
                running_now = sum(1 for status in all_status.values() if status == "running")
                if running_now == success_count:
                    print("✅ All started services are healthy!")
                else:
                    print(f"⚠️ {running_now}/{success_count} services are responding")
            except Exception:
                print("⚠️ Health check inconclusive (services may still be starting)")

        if failed_services:
            self._print_failed_services_info(failed_services)

    def _handle_foreground_mode(self) -> None:
        """Handle foreground mode startup."""
        print("\n💡 Services running in foreground mode")
        print("   Press Ctrl+C to stop all services")
        print()

        self._monitor_foreground_services()

    def _monitor_foreground_services(self) -> None:
        """Monitor services running in foreground mode."""
        try:
            running_check_count = 0

            while True:
                time.sleep(5)  # Check every 5 seconds

                # Periodic health check
                all_status = self.service_manager.get_all_status()
                running_count = sum(1 for status in all_status.values() if status == "running")
                total_count = len(all_status)

                running_check_count += 1

                # Print status update every 6 checks (30 seconds)
                if running_check_count % 6 == 0:
                    print(f"📊 Status: {running_count}/{total_count} services running")
                    if running_count < total_count:
                        failing = [name for name, status in all_status.items() if status != "running"]
                        print(f"   Services not responding: {', '.join(failing)}")

        except KeyboardInterrupt:
            print("\n🛑 Received shutdown signal...")
            print("Stopping all services...")
            self.service_manager.stop_all_services()
            print("✅ All services stopped. Goodbye!")

    def _print_no_services_error(self) -> None:
        """Print error when no services are specified."""
        print("❌ No services specified")
        print("💡 Try: python main.py --background  # Start all services")

    def _print_background_success_info(self) -> None:
        """Print success information for background mode."""
        print("\n🎉 Services are running in the background!")
        print("\n🌐 Access Points:")
        print("   • Web Dashboard: http://localhost:8001")
        print("   • API Documentation: http://localhost:8001/docs")
        print("   • Discord Bot: Ready for !commands")

        print("\n🛠️ Management Commands:")
        print("   • Check status: python main.py --status")
        print("   • Stop services: python main.py --stop")
        print("   • View logs: tail -f logs/app.log")
        print("   • Health check: python scripts/health_check.py")

    def _print_failed_services_info(self, failed_services: List[str]) -> None:
        """Print information about failed services."""
        print(f"\n❌ Failed to start: {', '.join(failed_services)}")
        print("\n🔧 Troubleshooting:")
        print("   • Check logs: tail -f logs/app.log")
        print("   • Verify configuration: python setup_wizard.py --validate")
        print("   • Check port conflicts: netstat -tulpn | grep :5000")
        print("   • Restart failed services individually")


# Factory function for backward compatibility
def create_start_handler(service_manager: ServiceManager) -> StartHandler:
    """Create and return a StartHandler instance."""
    return StartHandler(service_manager)