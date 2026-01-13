#!/usr/bin/env python3
"""
Command Router - CLI Command Routing System
===========================================

Routes CLI commands to appropriate handlers for modular command processing.

V2 Compliant: Yes (<200 lines)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-07
"""

from typing import Dict, Any, Optional
from src.services.service_manager import ServiceManager

# Import handlers
from .handlers.status_handler import create_status_handler
from .handlers.stop_handler import create_stop_handler
from .handlers.start_handler import create_start_handler
from .handlers.validation_handler import create_validation_handler
from .handlers.cleanup_handler import create_cleanup_handler


class CommandRouter:
    """Routes CLI commands to appropriate handler modules."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager
        self._initialize_handlers()

    def _initialize_handlers(self) -> None:
        """Initialize all command handlers."""
        self.status_handler = create_status_handler(self.service_manager)
        self.stop_handler = create_stop_handler(self.service_manager)
        self.start_handler = create_start_handler(self.service_manager)
        self.validation_handler = create_validation_handler()
        self.cleanup_handler = create_cleanup_handler(self.service_manager)

    def route_command(self, command: str, command_info: Dict[str, Any]) -> bool:
        """Route a command to the appropriate handler.

        Args:
            command: The command name (e.g., 'status', 'start', 'stop')
            command_info: Dictionary containing command parameters and options

        Returns:
            bool: True if command was handled successfully, False otherwise
        """
        try:
            # Route to appropriate handler based on command
            if command == 'status' or command == 'monitor':
                self.status_handler.handle_monitor_command(command_info)
            elif command == 'stop' or command == 'kill':
                self.stop_handler.handle_stop_command(command_info)
            elif command == 'start' or command == 'launch':
                self.start_handler.handle_start_services_command(command_info)
            elif command == 'validate' or command == 'check':
                self.validation_handler.handle_validate_command(command_info)
            elif command == 'cleanup' or command == 'clean':
                self.cleanup_handler.handle_cleanup_command(command_info)
            else:
                self._handle_unknown_command(command)
                return False

            return True

        except Exception as e:
            print(f"❌ Error executing command '{command}': {e}")
            return False

    def _handle_unknown_command(self, command: str) -> None:
        """Handle unknown commands."""
        print(f"❌ Unknown command: {command}")
        print("\n💡 Available commands:")
        print("   • status, monitor  - Check service status")
        print("   • start, launch    - Start services")
        print("   • stop, kill       - Stop services")
        print("   • validate, check  - Run validation")
        print("   • cleanup, clean   - Clean up resources")
        print("\n   Use 'python main.py --help' for more options")

    def get_available_commands(self) -> Dict[str, str]:
        """Get dictionary of available commands and their descriptions."""
        return {
            'status': 'Check service status and health',
            'monitor': 'Monitor service status (alias for status)',
            'start': 'Start services',
            'launch': 'Launch services (alias for start)',
            'stop': 'Stop services',
            'kill': 'Kill services forcefully (alias for stop)',
            'validate': 'Run validation checks',
            'check': 'Check system validation (alias for validate)',
            'cleanup': 'Clean up resources and logs',
            'clean': 'Clean resources (alias for cleanup)'
        }

    def validate_command_exists(self, command: str) -> bool:
        """Check if a command is supported."""
        available_commands = self.get_available_commands()
        return command in available_commands


# Factory function for backward compatibility
def create_command_router(service_manager: ServiceManager) -> CommandRouter:
    """Create and return a CommandRouter instance."""
    return CommandRouter(service_manager)