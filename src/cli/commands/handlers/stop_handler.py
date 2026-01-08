#!/usr/bin/env python3
"""
Stop Handler - CLI Command Handler
==================================

Handles service stop and kill commands for the main CLI.

V2 Compliant: Yes (<100 lines)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-07
"""

from typing import Dict, Any
from src.services.service_manager import ServiceManager


class StopHandler:
    """Handles stop-related CLI commands."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def handle_stop_command(self, command_info: Dict[str, Any]) -> None:
        """Handle stop/kill commands."""
        force = command_info.get('force', False)
        action = "force killing" if force else "stopping"
        print(f"🛑 {action.title()} all services...")

        success = self.service_manager.stop_all_services(force=force)
        if success:
            print("✅ All services stopped successfully")
        else:
            print("❌ Some services failed to stop")

    def handle_individual_stop_command(self, service_name: str, force: bool = False) -> bool:
        """Handle stopping an individual service."""
        action = "force killing" if force else "stopping"
        print(f"🛑 {action.title()} {service_name}...")

        success = self.service_manager.stop_service(service_name, force=force)
        if success:
            print(f"✅ {service_name} stopped successfully")
        else:
            print(f"❌ Failed to stop {service_name}")

        return success


# Factory function for backward compatibility
def create_stop_handler(service_manager: ServiceManager) -> StopHandler:
    """Create and return a StopHandler instance."""
    return StopHandler(service_manager)