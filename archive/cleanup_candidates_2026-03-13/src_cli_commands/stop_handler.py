"""
Stop Command Handler - V2 Compliant (<400 lines)
Handles service stopping with safety checks and cleanup.
"""

from typing import Dict, Any
from src.services.service_manager import ServiceManager


class StopHandler:
    """Handles stop command with safety checks and graceful shutdown."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def execute(self, force: bool = False) -> None:
        """Execute stop command."""
        print("🛑 Stopping dream.os Services")
        print("=" * 40)

        all_status = self.service_manager.get_all_status()

        if not all_status:
            print("ℹ️  No services configured or found.")
            return

        # Check for running services
        running_services = [
            name for name, status in all_status.items()
            if status == 'running'
        ]

        if not running_services:
            print("ℹ️  No services currently running.")
            return

        print(f"Found {len(running_services)} running service(s):")
        for service in running_services:
            print(f"   • {service}")

        if not force:
            print("\n⚠️  This will stop all running services.")
            try:
                confirm = input("Continue? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("❌ Operation cancelled.")
                    return
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled.")
                return

        print("\n🛑 Stopping services...")

        success_count = 0
        failed_services = []

        # Stop services in reverse dependency order
        stop_order = self._get_stop_order(running_services)

        for service_name in stop_order:
            print(f"   Stopping {service_name}...", end=' ')
            try:
                result = self.service_manager.stop_service(service_name)
                if result:
                    print("✅")
                    success_count += 1
                else:
                    print("❌")
                    failed_services.append((service_name, 'Stop failed'))
            except Exception as e:
                print("❌")
                failed_services.append((service_name, str(e)))

        # Report results
        print(f"\n📊 STOP RESULTS: {success_count}/{len(running_services)} services stopped successfully")

        if failed_services:
            print("\n❌ FAILED SERVICES:")
            for service_name, error in failed_services:
                print(f"   🔴 {service_name}: {error}")

            print("\n💡 Troubleshooting:")
            print("   • Check service logs for detailed error information")
            print("   • Try force stop: python main.py --stop --force")
            print("   • Restart services individually if needed")
        else:
            print("\n✅ All services stopped successfully!")
            print("💡 Start services with: python main.py --start")

    def _get_stop_order(self, running_services: list) -> list:
        """
        Get services in proper stop order (reverse of start order).
        Critical services should be stopped last.
        """
        # Define service priority (lower number = stop later)
        priority_map = {
            'message_queue': 1,  # Stop last - other services depend on it
            'fastapi_service': 2,
            'discord_bot': 3,
            'twitch_bot': 4
        }

        # Sort by priority (ascending) - highest priority stopped last
        return sorted(
            running_services,
            key=lambda s: priority_map.get(s, 99)
        )