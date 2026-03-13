"""
Status Command Handler - V2 Compliant (<400 lines)
Handles service status reporting and health checks.
"""

from typing import Dict, Any
from src.services.service_manager import ServiceManager


class StatusHandler:
    """Handles status command with enhanced health checks and troubleshooting."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def execute(self) -> None:
        """Execute status command."""
        print("🐝 dream.os - Service Status Report")
        print("=" * 50)

        all_status = self.service_manager.get_all_status()

        if not all_status:
            print("❌ No services configured or found.")
            print("\n💡 Quick Fix:")
            print("   1. Run: python main.py --validate")
            print("   2. Check .env file exists with required variables")
            print("   3. Ensure all dependencies are installed: pip install -r requirements.txt")
            return

        # Group services by status
        healthy = []
        unhealthy = []
        stopped = []

        for service_name, status in all_status.items():
            if status == 'running':
                healthy.append((service_name, status))
            elif status == 'error':
                unhealthy.append((service_name, status))
            else:
                stopped.append((service_name, status))

        # Report healthy services
        if healthy:
            print(f"\n✅ HEALTHY SERVICES ({len(healthy)}):")
            for service_name, status in healthy:
                print(f"   🟢 {service_name}: Running")

        # Report unhealthy services with troubleshooting
        if unhealthy:
            print(f"\n❌ UNHEALTHY SERVICES ({len(unhealthy)}):")
            for service_name, status in unhealthy:
                print(f"   🔴 {service_name}: Error")
                self._print_troubleshooting(service_name)

        # Report stopped services
        if stopped:
            print(f"\n⏹️  STOPPED SERVICES ({len(stopped)}):")
            for service_name, status in stopped:
                print(f"   ⭕ {service_name}: Stopped")

        # Overall system health
        total_services = len(all_status)
        healthy_count = len(healthy)

        print(f"\n📊 OVERALL HEALTH: {healthy_count}/{total_services} services healthy")

        if healthy_count == total_services:
            print("🎉 All systems operational!")
        elif healthy_count >= total_services * 0.8:
            print("⚠️  Most systems operational - minor issues detected")
        else:
            print("🚨 Critical issues detected - immediate attention required")

        print("\n💡 Management Commands:")
        print("   Start all:    python main.py --start")
        print("   Stop all:     python main.py --stop")
        print("   Restart all:  python main.py --restart")
        print("   Health check: python main.py --validate")

    def _print_troubleshooting(self, service_name: str) -> None:
        """Print service-specific troubleshooting information."""
        troubleshooting = {
            'message_queue': [
                "Check Redis connection: redis-cli ping",
                "Verify REDIS_URL in .env file",
                "Check Redis service status"
            ],
            'twitch_bot': [
                "Verify TWITCH_TOKEN in .env file",
                "Check Twitch API connectivity",
                "Validate bot permissions in Twitch channel"
            ],
            'discord_bot': [
                "Verify DISCORD_TOKEN in .env file",
                "Check Discord API connectivity",
                "Validate bot permissions in server"
            ],
            'fastapi_service': [
                "Check port availability (default: 8000)",
                "Verify FastAPI dependencies installed",
                "Check API endpoint health: curl http://localhost:8000/health"
            ]
        }

        if service_name in troubleshooting:
            print("      💡 Troubleshooting:")
            for step in troubleshooting[service_name]:
                print(f"         • {step}")