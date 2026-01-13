#!/usr/bin/env python3
"""
Agent Cellphone V2 - Main Entry Point
====================================

Professional entry point for the Agent Cellphone V2 system.

Usage:
    python main.py                    # Start interactive mode
    python main.py --api-only         # Start API only
    python main.py --status           # Check system status
    python main.py --stop             # Stop running services
"""

<<<<<<< HEAD
import asyncio
import argparse
=======
from src.services.agent_status_integration import get_agent_status_integration
from src.cli.commands.start_handler import StartHandler
from src.cli.commands.autonomous_handler import AutonomousHandler
from src.cli.commands.mode_handler import ModeHandler
from src.cli.commands.cleanup_handler import CleanupHandler
from src.cli.commands.validation_handler import ValidationHandler
from src.cli.commands.stop_handler import StopHandler
from src.cli.commands.status_handler import StatusHandler
from src.cli.argument_parser import parse_main_args
from src.services.service_manager import ServiceManager
import os
import sys
>>>>>>> rescue/dreamos-down-
import logging
import signal
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from agent_cellphone_v2 import AgentCoordinator
from agent_cellphone_v2.config import Settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

<<<<<<< HEAD

class AgentCellphoneApp:
    """Main application class."""

    def __init__(self):
        self.coordinator: AgentCoordinator = None
        self.settings = Settings()
=======
# Import our modular components

# Import command handlers

# Import automated status integration

>>>>>>> rescue/dreamos-down-

    async def start(self, api_only: bool = False):
        """Start the application."""
        logger.info("Starting Agent Cellphone V2...")

        # Setup directories
        self.settings.setup_directories()

        # Validate configuration
        validation_messages = self.settings.validate_config()
        for message in validation_messages:
            if message.startswith("❌"):
                logger.error(message)
            else:
                logger.warning(message)

<<<<<<< HEAD
        # Initialize coordinator
        self.coordinator = AgentCoordinator()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
=======
    # Count running services
    running_count = sum(1 for status in all_status.values()
                        if status == "running")
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

        print(
            f"{status_icon} {service_name}: {status.upper()} {health_icon}{port_info}")
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
    handler = ValidationHandler()
    exit_code = handler.execute()
    return exit_code


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
    print(
        f"📊 Results: {success_count}/{len(services)} services started successfully")

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
                running_now = sum(
                    1 for status in all_status.values() if status == "running")
                if running_now == success_count:
                    print("✅ All started services are healthy!")
                else:
                    print(
                        f"⚠️ {running_now}/{success_count} services are responding")
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
>>>>>>> rescue/dreamos-down-

        try:
            await self.coordinator.start()
            logger.info("Agent Cellphone V2 started successfully")
            logger.info(f"API available at: http://{self.settings.api_host}:{self.settings.api_port}")
            logger.info("Press Ctrl+C to stop")

<<<<<<< HEAD
            # Keep running
            while self.coordinator.is_running():
                await asyncio.sleep(1)
=======
            while True:
                time.sleep(5)  # Check every 5 seconds

                # Periodic health check
                all_status = service_manager.get_all_status()
                running_count = sum(
                    1 for status in all_status.values() if status == "running")

                running_check_count += 1
                if running_check_count % 6 == 0:  # Every 30 seconds
                    print(
                        f"📊 Health check: {running_count}/{len(services)} services running")

                if running_count == 0:
                    print("⚠️ All services have stopped unexpectedly")
                    break
>>>>>>> rescue/dreamos-down-

        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Error during startup: {e}")
            raise
        finally:
            if self.coordinator:
                await self.coordinator.stop()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        if self.coordinator:
            asyncio.create_task(self.coordinator.stop())

    async def status(self):
        """Get system status."""
        if not self.coordinator:
            self.coordinator = AgentCoordinator()

        status = await self.coordinator.get_status()
        print("Agent Cellphone V2 Status:")
        print(f"  Running: {status['running']}")
        print(f"  Version: {status['version']}")
        print("  Services:")
        for service, running in status['services'].items():
            print(f"    {service}: {'✅' if running else '❌'}")

    async def stop(self):
        """Stop running services."""
        logger.info("Stopping Agent Cellphone V2...")
        if self.coordinator:
            await self.coordinator.stop()
        logger.info("Agent Cellphone V2 stopped")



def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Agent Cellphone V2")
    parser.add_argument("--api-only", action="store_true", help="Start API service only")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--stop", action="store_true", help="Stop running services")
    parser.add_argument("--config", help="Path to config file")

    args = parser.parse_args()

    # Override config if specified
    if args.config:
        Settings.Config.env_file = args.config

    app = AgentCellphoneApp()

    if args.status:
        asyncio.run(app.status())
    elif args.stop:
        asyncio.run(app.stop())
    else:
        # Start the application
        asyncio.run(app.start(api_only=args.api_only))

<<<<<<< HEAD
=======
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
                print("\n💾 Configuration saved!")
                print("💡 Start services with: python main.py --start")
                print(
                    f"💡 Or use specific mode: python main.py --start --mode {result['mode']}")
        elif command_type == 'autonomous_reports':
            handler = AutonomousHandler()
            handler.handle_reports_command()
        elif command_type == 'run_autonomous_config':
            handler = AutonomousHandler()
            handler.handle_run_autonomous_config_command()
        elif command_type == 'status_integration':
            print("🤖 Starting Automated Agent Status Integration...")
            try:
                import asyncio
                asyncio.run(get_agent_status_integration().run())
            except KeyboardInterrupt:
                print("\n🛑 Status integration stopped")
            except Exception as e:
                print(f"❌ Status integration failed: {e}")
                sys.exit(1)
        elif command_type == 'thea_capture_cookies':
            print("🍪 Starting Thea Cookie Capture...")
            try:
                from tools.thea_manual_login import TheaManualLogin
                tool = TheaManualLogin()
                success = tool.capture_cookies_interactive()
                sys.exit(0 if success else 1)
            except Exception as e:
                print(f"❌ Thea cookie capture failed: {e}")
                sys.exit(1)
        elif command_type == 'thea_test_cookies':
            print("🧪 Testing Thea Cookies...")
            try:
                from tools.thea_manual_login import TheaManualLogin
                tool = TheaManualLogin()
                success = tool.test_cookies()
                sys.exit(0 if success else 1)
            except Exception as e:
                print(f"❌ Thea cookie test failed: {e}")
                sys.exit(1)
        elif command_type == 'thea_scan_project':
            print("🔍 Thea Project Scanner...")
            try:
                from tools.thea_manual_login import TheaManualLogin
                tool = TheaManualLogin()
                success = tool.scan_project_with_thea()
                sys.exit(0 if success else 1)
            except Exception as e:
                print(f"❌ Thea project scan failed: {e}")
                sys.exit(1)
        elif command_type == 'thea_status':
            try:
                from tools.thea_manual_login import TheaManualLogin
                tool = TheaManualLogin()
                tool.show_status()
            except Exception as e:
                print(f"❌ Thea status check failed: {e}")
                sys.exit(1)
        elif command_type == 'thea_login':
            print("🔐 Starting Thea Manual Login...")
            try:
                from tools.thea_manual_login import TheaManualLogin
                tool = TheaManualLogin()
                success = tool.start_manual_login()
                sys.exit(0 if success else 1)
            except Exception as e:
                print(f"❌ Thea manual login failed: {e}")
                sys.exit(1)
        elif command_type == 'show_help':
            # Show help when no arguments provided
            from src.cli.argument_parser import get_argument_parser
            parser = get_argument_parser()
            parser.parser.print_help()
            sys.exit(0)
        elif command_type == 'start_services':
            handler = StartHandler(service_manager)
            handler.execute(command_info)
        else:
            print("❌ Unknown command. Use --help for usage information.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Command execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
>>>>>>> rescue/dreamos-down-


if __name__ == "__main__":
    main()
