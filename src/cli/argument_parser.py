"""
CLI Argument Parser - Agent Cellphone V2
======================================

Handles command-line argument parsing for main.py with comprehensive
option support and validation.

Features:
- Service selection options
- Mode selection (agent modes)
- Background/foreground execution
- Status and control commands
- Validation and help options

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import argparse
import sys
from typing import Dict, Any, Optional

class MainArgumentParser:
    """
    Comprehensive argument parser for main.py with all service options.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Agent Cellphone V2 - Unified Service Launcher",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_epilog()
        )
        self._setup_arguments()

    def _get_epilog(self) -> str:
        """Get the help epilog with usage examples."""
        return """
Examples:
  python main.py                          # Start all services (foreground)
  python main.py --background             # Start all services in background
  python main.py --status                 # Check service status
  python main.py --stop                   # Stop all background services
  python main.py --kill                   # Force kill all services
  python main.py --message-queue          # Start only message queue
  python main.py --twitch                 # Start only Twitch bot
  python main.py --discord                # Start only Discord bot
  python main.py --fastapi                # Start only FastAPI service
  python main.py --validate               # Run comprehensive validation
  python main.py --select-mode            # Select agent mode (interactive)
  python main.py --autonomous-reports     # Display autonomous config reports
  python main.py --status-integration     # Start automated agent status integration
  python main.py --thea-capture-cookies   # Capture Thea cookies interactively
  python main.py --thea-test-cookies      # Test Thea cookies
  python main.py --thea-scan-project      # Scan project with Thea guidance
  python main.py --thea-status            # Show Thea integration status

Background Mode:
  Services run as detached processes. Use --stop to terminate them.
  Services continue running after terminal closes.

Windows background: start /B python main.py --background
Unix/Mac background: python main.py --background &
"""

    def _setup_arguments(self):
        """Setup all command-line arguments."""

        # Service selection (mutually exclusive)
        service_group = self.parser.add_mutually_exclusive_group()

        service_group.add_argument(
            '--message-queue', '-mq',
            action='store_true',
            help='Start only message queue processor'
        )

        service_group.add_argument(
            '--twitch', '-t',
            action='store_true',
            help='Start only Twitch bot'
        )

        service_group.add_argument(
            '--discord', '-d',
            action='store_true',
            help='Start only Discord bot'
        )

        service_group.add_argument(
            '--fastapi', '-f',
            action='store_true',
            help='Start only FastAPI service'
        )

        # Execution mode
        self.parser.add_argument(
            '--background', '-b',
            action='store_true',
            help='Run services in background (detached processes)'
        )

        # Control commands (mutually exclusive)
        control_group = self.parser.add_mutually_exclusive_group()

        control_group.add_argument(
            '--status', '-s',
            action='store_true',
            help='Check status of all services'
        )

        control_group.add_argument(
            '--stop',
            action='store_true',
            help='Stop all background services gracefully'
        )

        control_group.add_argument(
            '--kill', '-k',
            action='store_true',
            help='Force kill all services'
        )

        control_group.add_argument(
            '--status-integration',
            action='store_true',
            help='Start automated agent status integration service'
        )

        # Configuration and setup
        self.parser.add_argument(
            '--select-mode', '-m',
            action='store_true',
            help='Select agent mode (interactive)'
        )

        self.parser.add_argument(
            '--autonomous-reports',
            action='store_true',
            help='Display autonomous configuration reports'
        )

        self.parser.add_argument(
            '--run-autonomous-config',
            action='store_true',
            help='Run autonomous configuration system'
        )

        # Thea integration
        self.parser.add_argument(
            '--thea-capture-cookies',
            action='store_true',
            help='Capture new Thea cookies interactively'
        )

        self.parser.add_argument(
            '--thea-test-cookies',
            action='store_true',
            help='Test existing Thea cookies'
        )

        self.parser.add_argument(
            '--thea-scan-project',
            action='store_true',
            help='Scan project with Thea guidance'
        )

        self.parser.add_argument(
            '--thea-status',
            action='store_true',
            help='Show Thea integration status'
        )

        # Maintenance
        self.parser.add_argument(
            '--cleanup-logs',
            action='store_true',
            help='Clean up old log files (>7 days)'
        )

        # Validation
        self.parser.add_argument(
            '--validate', '-v',
            action='store_true',
            help='Run comprehensive validation checks'
        )

        # Utility
        self.parser.add_argument(
            '--version',
            action='version',
            version='Agent Cellphone V2 1.0.0'
        )

    def parse_args(self, args: Optional[list] = None) -> argparse.Namespace:
        """Parse command-line arguments."""
        if args is None:
            args = sys.argv[1:]
        return self.parser.parse_args(args)

    def get_command_info(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        Analyze parsed arguments and return command information.

        Returns:
            Dict containing command type, services to start, and options
        """
        command_info = {
            'command_type': 'start_services',
            'services': [],
            'background': args.background,
            'options': {}
        }

        # Determine command type
        if args.status:
            command_info['command_type'] = 'status'
        elif args.stop:
            command_info['command_type'] = 'stop'
        elif args.kill:
            command_info['command_type'] = 'kill'
        elif args.select_mode:
            command_info['command_type'] = 'select_mode'
        elif args.autonomous_reports:
            command_info['command_type'] = 'autonomous_reports'
        elif args.run_autonomous_config:
            command_info['command_type'] = 'run_autonomous_config'
        elif args.cleanup_logs:
            command_info['command_type'] = 'cleanup_logs'
        elif args.validate:
            command_info['command_type'] = 'validate'
        else:
            # Determine which services to start
            if args.message_queue:
                command_info['services'].append('message_queue')
            elif args.twitch:
                command_info['services'].append('twitch')
            elif args.discord:
                command_info['services'].append('discord')
            elif args.fastapi:
                command_info['services'].append('fastapi')
            else:
                # Start all services if no specific service selected
                command_info['services'] = ['message_queue', 'twitch', 'discord', 'fastapi']

        # Set options
        command_info['options'] = {
            'force_kill': args.kill if hasattr(args, 'kill') else False
        }

        return command_info

def get_argument_parser() -> MainArgumentParser:
    """Factory function for argument parser."""
    return MainArgumentParser()

def parse_main_args(args: Optional[list] = None) -> tuple[argparse.Namespace, Dict[str, Any]]:
    """
    Convenience function to parse arguments and get command info.

    Returns:
        Tuple of (parsed_args, command_info)
    """
    parser = get_argument_parser()
    parsed_args = parser.parse_args(args)
    command_info = parser.get_command_info(parsed_args)
    return parsed_args, command_info