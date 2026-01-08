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

V2 Compliant: Yes (<400 lines)
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

# Import command handlers
from src.cli.commands.status_handler import StatusHandler
from src.cli.commands.stop_handler import StopHandler
from src.cli.commands.validation_handler import ValidationHandler
from src.cli.commands.cleanup_handler import CleanupHandler
from src.cli.commands.mode_handler import ModeHandler
from src.cli.commands.autonomous_handler import AutonomousHandler
from src.cli.commands.start_handler import StartHandler

def _handle_monitor_command(service_manager: ServiceManager, command_info: dict):
    """Handle status command with enhanced health checks and troubleshooting."""
    print("🐝 dream.os - Service Status Report")
    print("=" * 50)

    all_status = service_manager.get_all_status()

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
        info = service_manager.get_service_info(service_name)
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
        print("🎉 All systems operational!")
        print("\n🚀 Ready to use:")
        print("   • Web Dashboard: http://localhost:5000")
        print("   • API Docs: http://localhost:8001/docs")
        print("   • Discord Bot: Ready for commands")
    elif running_count > 0:
        print("⚠️ Partial system operational")
        print("   Some services are running, but not all.")
    else:
        print("❌ System offline")
        print("   No services are currently running.")

    # Troubleshooting section
    if running_count < total_count:
        print("\n🔧 Troubleshooting:")
        if running_count == 0:
            print("   • Start services: python main.py --background")
            print("   • Check setup: python setup.py --validate")
        else:
            print("   • Check logs: tail -f logs/app.log")
            print("   • Restart failed services individually")
            print("   • Run health check: python scripts/health_check.py")

    print("\n💡 Commands:")
    print("   • Start all: python main.py --background")
    print("   • Stop all: python main.py --stop")
    print("   • Health check: python scripts/health_check.py")
    print("   • View logs: tail -f logs/app.log")

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
    """Handle start services command with enhanced feedback and health checks."""
    services = command_info['services']
    background = command_info['background']

    if not services:
        print("❌ No services specified")
        print("💡 Try: python main.py --background  # Start all services")
        return

    mode = "background" if background else "foreground"
    print(f"🐝 dream.os - Starting Services")
    print("=" * 40)
    print(f"🚀 Launching {len(services)} service(s) in {mode} mode...")
    print()

    success_count = 0
    failed_services = []

    for service_name in services:
        print(f"   Starting {service_name}...", end=" ")
        if service_manager.start_service(service_name, background=background):
            success_count += 1
            print("✅")
        else:
            failed_services.append(service_name)
            print("❌")

    print()
    print(f"📊 Results: {success_count}/{len(services)} services started successfully")

    if background:
        if success_count > 0:
            print("\n🎉 Services are running in the background!")
            print("\n🌐 Access Points:")
            print("   • Web Dashboard: http://localhost:5000")
            print("   • API Documentation: http://localhost:8001/docs")
            print("   • Discord Bot: Ready for !commands")

            print("\n🛠️ Management Commands:")
            print("   • Check status: python main.py --status")
            print("   • Stop services: python main.py --stop")
            print("   • View logs: tail -f logs/app.log")
            print("   • Health check: python scripts/health_check.py")

            # Quick health verification
            print("\n🔍 Performing quick health check...")
            try:
                import time
                time.sleep(3)  # Give services time to start
                all_status = service_manager.get_all_status()
                running_now = sum(1 for status in all_status.values() if status == "running")
                if running_now == success_count:
                    print("✅ All started services are healthy!")
                else:
                    print(f"⚠️ {running_now}/{success_count} services are responding")
            except Exception:
                print("⚠️ Health check inconclusive (services may still be starting)")

        if failed_services:
            print(f"\n❌ Failed to start: {', '.join(failed_services)}")
            print("\n🔧 Troubleshooting:")
            print("   • Check logs: tail -f logs/app.log")
            print("   • Verify configuration: python setup_wizard.py --validate")
            print("   • Check port conflicts: netstat -tulpn | grep :5000")
            print("   • Restart failed services individually")

    else:
        # Foreground mode
        print("\n💡 Services running in foreground mode")
        print("   Press Ctrl+C to stop all services")
        print()

        try:
            import time
            running_check_count = 0

            while True:
                time.sleep(5)  # Check every 5 seconds

                # Periodic health check
                all_status = service_manager.get_all_status()
                running_count = sum(1 for status in all_status.values() if status == "running")

                running_check_count += 1
                if running_check_count % 6 == 0:  # Every 30 seconds
                    print(f"📊 Health check: {running_count}/{len(services)} services running")

                if running_count == 0:
                    print("⚠️ All services have stopped unexpectedly")
                    break

        except KeyboardInterrupt:
            print("\n🛑 Received shutdown signal...")
            print("👋 Stopping all services gracefully...")

        # Always attempt clean shutdown
        shutdown_success = service_manager.stop_all_services(force=False)
        if shutdown_success:
            print("✅ All services stopped successfully. Goodbye! 👋")
        else:
            print("⚠️ Some services may not have stopped cleanly.")
            print("   Force kill if needed: python main.py --kill")

def main():
    """Main entry point - simplified launcher using modular components."""

    # Parse command line arguments
    parsed_args, command_info = parse_main_args()

    # Initialize service manager
    service_manager = ServiceManager()

    # Execute command based on type
    command_type = command_info['command_type']

    try:
        if command_type == 'status':
            handler = StatusHandler(service_manager)
            handler.execute()
        elif command_type in ['stop', 'kill']:
            force = (command_type == 'kill')
            handler = StopHandler(service_manager)
            handler.execute(force=force)
        elif command_type == 'validate':
            handler = ValidationHandler()
            exit_code = handler.execute()
            sys.exit(exit_code)
        elif command_type == 'cleanup_logs':
            handler = CleanupHandler(service_manager)
            handler.execute()
        elif command_type == 'select_mode':
            handler = ModeHandler()
            result = handler.execute()
            if result:
                print("
💾 Configuration saved!"                print("💡 Start services with: python main.py --start")
                print(f"💡 Or use specific mode: python main.py --start --mode {result['mode']}")
        elif command_type == 'autonomous_reports':
            handler = AutonomousHandler()
            handler.handle_reports_command()
        elif command_type == 'run_autonomous_config':
            handler = AutonomousHandler()
            handler.handle_run_autonomous_config_command()
        elif command_type == 'start_services':
            handler = StartHandler(service_manager)
            handler.execute(command_info)
        else:
            print("❌ Unknown command. Use --help for usage information.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Command execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()