#!/usr/bin/env python3
"""
Main Service Launcher - Agent Cellphone V2
==========================================

Unified entry point to start and manage all critical services:
- Message Queue Processor
- Twitch Bot
- Discord Bot
- FastAPI Service

Features:
- Service status monitoring and control
- Background/foreground execution modes
- Comprehensive validation system
- Interactive agent mode selection

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import sys
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)

# Import our modular components
from src.services.service_manager import ServiceManager
from src.cli.argument_parser import parse_main_args
from src.cli.validation_runner import ValidationRunner

def _handle_status_command(service_manager: ServiceManager):
    """Handle status command."""
    print("📊 Service Status Report")
    print("=" * 40)

    all_status = service_manager.get_all_status()
    for service_name, status in all_status.items():
        status_icon = "🟢" if status == "running" else "🔴"
        info = service_manager.get_service_info(service_name)
        pid = info.get('pid', 'N/A')
        print(f"{status_icon} {service_name}: {status.upper()} (PID: {pid})")

def _handle_stop_command(service_manager: ServiceManager, force: bool = False):
    """Handle stop/kill commands."""
    action = "force killing" if force else "stopping"
    print(f"🛑 {action.title()} all services...")

    success = service_manager.stop_all_services(force=force)
    if success:
        print("✅ All services stopped successfully")
    else:
        print("❌ Some services failed to stop")

def _handle_validate_command():
    """Handle validation command."""
    runner = ValidationRunner()
    results = runner.run_comprehensive_validation('main_validation.json')

    print("📊 Comprehensive Validation Results")
    print("=" * 40)
    print(f"🏥 Overall Status: {results['overall_status']}")

    for validation_name, result in results.get('validations', {}).items():
        status = result.get('status', 'UNKNOWN')
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {validation_name.replace('_', ' ').title()}: {status}")

def _handle_cleanup_command(service_manager: ServiceManager):
    """Handle cleanup logs command."""
    print("🧹 Cleaning up old log files...")
    service_manager.cleanup_logs()
    print("✅ Log cleanup completed")

def _handle_select_mode_command():
    """Handle select mode command."""
    print("🎯 Agent Mode Selection")
    print("This feature requires additional setup. Please use the setup wizard:")
    print("   python setup_wizard.py")

def _handle_autonomous_reports_command():
    """Handle autonomous reports command."""
    print("📋 Autonomous Configuration Reports")
    print("This feature requires additional setup. Please use the setup wizard:")
    print("   python setup_wizard.py")

def _handle_run_autonomous_config_command():
    """Handle run autonomous config command."""
    print("⚙️ Autonomous Configuration System")
    print("This feature requires additional setup. Please use the setup wizard:")
    print("   python setup_wizard.py")

def _handle_start_services_command(service_manager: ServiceManager, command_info: dict):
    """Handle start services command."""
    services = command_info['services']
    background = command_info['background']

    if not services:
        print("❌ No services specified")
        return

    mode = "background" if background else "foreground"
    print(f"🚀 Starting {len(services)} service(s) in {mode} mode...")

    success_count = 0
    for service_name in services:
        if service_manager.start_service(service_name, background=background):
            success_count += 1
            status_icon = "✅"
        else:
            status_icon = "❌"
        print(f"   {status_icon} {service_name}")

    print(f"📊 Started {success_count}/{len(services)} services successfully")

    if background:
        print("\n✅ Services started in background mode")
        print("   Check status: python main.py --status")
        print("   Stop services: python main.py --stop")
        print("   Force kill: python main.py --kill")
    else:
        print("\n💡 Services running in foreground. Press Ctrl+C to stop.")
        try:
            import time
            while True:
                time.sleep(1)
                # Basic health monitoring
                all_status = service_manager.get_all_status()
                if not any(status == "running" for status in all_status.values()):
                    print("⚠️ All services have stopped")
                    break
        except KeyboardInterrupt:
            print("\n🛑 Stopping all services...")
            service_manager.stop_all_services(force=True)
            print("👋 All services stopped. Goodbye!")

def main():
    """Main entry point - simplified launcher using modular components."""

    # Parse command line arguments
    parsed_args, command_info = parse_main_args()

    # Initialize service manager
    service_manager = ServiceManager()

    # Execute command based on type
    command_type = command_info['command_type']

    if command_type == 'status':
        _handle_status_command(service_manager)
    elif command_type == 'stop':
        _handle_stop_command(service_manager, force=False)
    elif command_type == 'kill':
        _handle_stop_command(service_manager, force=True)
    elif command_type == 'validate':
        _handle_validate_command()
    elif command_type == 'cleanup_logs':
        _handle_cleanup_command(service_manager)
    elif command_type == 'select_mode':
        _handle_select_mode_command()
    elif command_type == 'autonomous_reports':
        _handle_autonomous_reports_command()
    elif command_type == 'run_autonomous_config':
        _handle_run_autonomous_config_command()
    elif command_type == 'start_services':
        _handle_start_services_command(service_manager, command_info)
    else:
        print("❌ Unknown command. Use --help for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main()