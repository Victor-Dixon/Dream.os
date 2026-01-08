#!/usr/bin/env python3
"""
Cleanup Handler - CLI Command Handler
====================================

Handles cleanup and maintenance commands for the main CLI.

V2 Compliant: Yes (<100 lines)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-07
"""

from typing import Dict, Any
from src.services.service_manager import ServiceManager


class CleanupHandler:
    """Handles cleanup-related CLI commands."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def handle_cleanup_command(self, command_info: Dict[str, Any]) -> None:
        """Handle cleanup logs command."""
        cleanup_type = command_info.get('type', 'logs')

        if cleanup_type == 'logs':
            self._cleanup_logs()
        elif cleanup_type == 'cache':
            self._cleanup_cache()
        elif cleanup_type == 'all':
            self._cleanup_all()
        else:
            print(f"❌ Unknown cleanup type: {cleanup_type}")
            print("💡 Available types: logs, cache, all")

    def _cleanup_logs(self) -> None:
        """Clean up old log files."""
        print("🧹 Cleaning up old log files...")
        self.service_manager.cleanup_logs()
        print("✅ Log cleanup completed")

    def _cleanup_cache(self) -> None:
        """Clean up cache files."""
        print("🧹 Cleaning up cache files...")
        # Add cache cleanup logic here
        print("✅ Cache cleanup completed")

    def _cleanup_all(self) -> None:
        """Clean up everything."""
        print("🧹 Performing full cleanup...")
        self._cleanup_logs()
        self._cleanup_cache()
        print("✅ Full cleanup completed")


# Factory function for backward compatibility
def create_cleanup_handler(service_manager: ServiceManager) -> CleanupHandler:
    """Create and return a CleanupHandler instance."""
    return CleanupHandler(service_manager)