"""
Start Services Handler - V2 Compliant (<400 lines)
Handles service startup with dependency management and health verification.
"""

import time
from typing import Dict, Any, List
from src.services.service_manager import ServiceManager


class StartHandler:
    """Handles start services command with proper dependency management."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def execute(self, command_info: Dict[str, Any]) -> None:
        """Execute start services command."""
        print("🚀 dream.os - Starting Services")
        print("=" * 35)

        # Extract background mode
        background = command_info.get('background', False)

        # Determine which services to start
        if command_info.get('start_all'):
            services_to_start = self._get_all_services()
            print("Starting ALL services...")
        elif command_info.get('services'):
            services_to_start = command_info['services']
            print(f"Starting specified services: {', '.join(services_to_start)}")
        else:
            services_to_start = self._get_all_services()
            print("Starting all services...")

        if not services_to_start:
            print("❌ No services to start.")
            print("💡 Check service configuration.")
            return

        # Check current status
        current_status = self.service_manager.get_all_status()
        already_running = [
            name for name, status in current_status.items()
            if status == 'running'
        ]

        if already_running:
            print(f"⚠️  Services already running: {', '.join(already_running)}")
            try:
                choice = input("Continue starting remaining services? (Y/n): ").strip().lower()
                if choice in ['n', 'no']:
                    print("❌ Operation cancelled.")
                    return
            except (EOFError, KeyboardInterrupt):
                print("ℹ️  Non-interactive environment detected - continuing with service startup...")
                # Continue automatically in non-interactive mode

        # Filter out already running services
        services_to_start = [s for s in services_to_start if s not in already_running]

        if not services_to_start:
            print("ℹ️  All requested services are already running.")
            return

        print(f"\n🚀 Starting {len(services_to_start)} service(s)...")

        # Start services in dependency order
        start_order = self._get_start_order(services_to_start)

        success_count = 0
        failed_services = []

        for service_name in start_order:
            print(f"   Starting {service_name}...", end=' ')
            try:


                if result:  # start_service returns True/False
                    print("✅")

                    # Verify service is actually running
                    if self._verify_service_started(service_name):
                        success_count += 1
                    else:
                        print(" (⚠️  Started but health check failed)")
                        failed_services.append((service_name, "Health check failed after start"))

                else:
                    print("❌")
                    failed_services.append((service_name, "Service start failed"))

            except Exception as e:
                print("❌")
                failed_services.append((service_name, str(e)))

        # Wait a moment for services to fully initialize
        if success_count > 0:
            print("\n⏳ Waiting for services to initialize...")
            time.sleep(3)

        # Final health check
        self._perform_final_health_check(start_order)

        # Report results
        print(f"\n📊 START RESULTS: {success_count}/{len(services_to_start)} services started successfully")

        if failed_services:
            print("\n❌ FAILED SERVICES:")
            for service_name, error in failed_services:
                print(f"   🔴 {service_name}: {error}")

            print("\n💡 Troubleshooting:")
            print("   • Check service logs for detailed error information")
            print("   • Verify all dependencies are installed")
            print("   • Check .env file for required configuration")
            print("   • Try starting services individually")
        else:
            print("✅ All services started successfully!")
            print("\n🌐 Access Points:")
            print("   • Web Dashboard: http://localhost:8001")
            print("   • API Docs: http://localhost:8001/docs")

    def _get_all_services(self) -> List[str]:
        """Get list of all configured services."""
        # This would typically come from service manager
        return ['message_queue', 'twitch_bot', 'discord_bot', 'fastapi_service']

    def _get_start_order(self, services: List[str]) -> List[str]:
        """
        Get services in proper start order based on dependencies.
        Critical infrastructure services should start first.
        """
        # Define service priority (lower number = start first)
        priority_map = {
            'message_queue': 1,   # Start first - others depend on it
            'fastapi_service': 2,
            'discord_bot': 3,
            'twitch_bot': 4
        }

        # Sort by priority (ascending) - lowest priority started first
        return sorted(
            services,
            key=lambda s: priority_map.get(s, 99)
        )

    def _verify_service_started(self, service_name: str, timeout: int = 10) -> bool:
        """Verify that a service actually started and is healthy."""


        try:
            for attempt in range(timeout):
                status = self.service_manager.get_service_status(service_name)
                if status == 'running':
                    # Additional health checks could go here
                    return True
                time.sleep(1)

            return False

        except KeyboardInterrupt:
            # Handle KeyboardInterrupt gracefully - user wants to abort
            print(f"\n⚠️  Service verification interrupted for {service_name}")
            return False

    def _perform_final_health_check(self, services: List[str]) -> None:
        """Perform a final health check on all started services."""
        print("🔍 Performing final health checks...")

        unhealthy_services = []

        for service_name in services:
            status = self.service_manager.get_service_status(service_name)
            if not status or status != 'running':
                unhealthy_services.append(service_name)

        if unhealthy_services:
            print(f"⚠️  Health check warnings for: {', '.join(unhealthy_services)}")
            print("   Services may still be initializing...")
        else:
            print("✅ All services passed health checks!")