#!/usr/bin/env python3
"""
<<<<<<< HEAD
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

=======
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

# Import command handlers

# Import automated status integration


def _handle_monitor_command(service_manager: ServiceManager, command_info: dict):
    """Handle status command with enhanced health checks and troubleshooting."""
    print("🐝 dream.os - Service Status Report")
    print("=" * 50)

    all_status = service_manager.get_all_status()

<<<<<<< HEAD
        print(f"Current mode: {current_mode}")
        print(f"Available modes: {', '.join(available_modes)}")
        print()

        # Show mode details
        for mode_name in available_modes:
            mode_info = self.agent_mode_manager.get_mode_info(mode_name)
            agents = mode_info.get('active_agents', [])
            monitor = mode_info.get('monitor_setup', 'unknown')
            print(f"  {mode_name}: {len(agents)} agents ({monitor} monitor)")
            print(f"    Agents: {', '.join(agents)}")
            if mode_name == current_mode:
                print("    ⭐ CURRENT MODE")
            print()

        while True:
            try:
                choice = input(
                    "Select agent mode (or press Enter to keep current): ").strip()

                if not choice:  # Keep current
                    print(f"✅ Keeping current mode: {current_mode}")
                    return

                if choice in available_modes:
                    if self.agent_mode_manager.set_mode(choice):
                        new_mode = self.agent_mode_manager.get_current_mode()
                        active_agents = self.agent_mode_manager.get_active_agents()
                        print(f"✅ Agent mode set to: {new_mode}")
                        print(f"   Active agents: {', '.join(active_agents)}")
                        print(
                            f"   Monitor setup: {self.agent_mode_manager.get_monitor_setup()}")
                        return
                    else:
                        print(f"❌ Failed to set mode: {choice}")
                else:
                    print(
                        f"❌ Invalid mode. Available: {', '.join(available_modes)}")

            except KeyboardInterrupt:
                print("\n⚠️  Mode selection canceled, keeping current mode")
                return
            except Exception as e:
                print(f"❌ Error selecting mode: {e}")
                return

    def start_message_queue(self):
        """Start message queue processor directly using the main script."""
        print("📬 Starting Message Queue Processor...")
        
        # Use the actual script directly (not the wrapper)
        script = self.project_root / "scripts" / "start_queue_processor.py"
        
        if not script.exists():
            # Fallback to tools wrapper (for backward compatibility)
            script = self.project_root / "tools" / "start_message_queue_processor.py"
            if not script.exists():
                print("   ❌ Message Queue Processor script not found")
                print(f"      Checked: scripts/start_queue_processor.py")
                print(f"      Checked: tools/start_message_queue_processor.py")
                return False

        try:
            # Pass current environment to subprocess so it inherits .env variables
            env = os.environ.copy()
            
            # Configure output based on background mode
            if self.background_mode:
                log_file = self.log_dir / "message_queue.log"
                stdout = open(log_file, 'a')
                stderr = subprocess.STDOUT
                creation_flags = 0
                if platform.system() == 'Windows':
                    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                stdout = subprocess.PIPE
                stderr = subprocess.STDOUT
                creation_flags = 0
            
            process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(self.project_root),
                env=env,
                stdout=stdout,
                stderr=stderr,
                creationflags=creation_flags if platform.system() == 'Windows' else 0
            )
            self.processes['message_queue'] = process
            self._save_pid('message_queue', process)
            print("   ✅ Message Queue Processor started (PID: {})".format(process.pid))
            if self.background_mode:
                print(f"   📝 Logs: {log_file}")
            else:
                # Start thread to monitor output
                Thread(target=self._monitor_process_output, args=('message_queue', process), daemon=True).start()
            return True
        except Exception as e:
            print(f"   ❌ Failed to start Message Queue: {e}")
            import traceback
            traceback.print_exc()
            return False

    def start_twitch_bot(self):
        """Start Twitch bot."""
        print("📺 Starting Twitch Bot...")
        
        # Check configuration first
        channel = os.getenv("TWITCH_CHANNEL", "").strip()
        token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()

        if not channel or not token:
            print("   ⚠️  Warning: Twitch configuration incomplete")
            print(f"      Channel: {'SET' if channel else 'NOT SET'}")
            print(f"      Token: {'SET' if token else 'NOT SET'}")
            if not channel or not token:
                print("   ❌ Cannot start Twitch Bot without configuration")
                print("   💡 Run 'python tools/test_twitch_config.py' to validate your setup")
                return False
        
        # Validate token format
        token_clean = token.strip().strip('"').strip("'")
        if not token_clean.startswith("oauth:"):
            print("   ⚠️  Warning: Token should start with 'oauth:' prefix")
            print("   💡 Run 'python tools/test_twitch_config.py' to validate your configuration")

        # Try script first (for backward compatibility)
        script = self.project_root / "tools" / "START_CHAT_BOT_NOW.py"
        
        if script.exists():
            # Use script if it exists
            try:
                # Configure output based on background mode
                if self.background_mode:
                    log_file = self.log_dir / "twitch_bot.log"
                    stdout = open(log_file, 'a')
                    stderr = subprocess.STDOUT
                    creation_flags = 0
                    if platform.system() == 'Windows':
                        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
                else:
                    stdout = subprocess.PIPE
                    stderr = subprocess.PIPE
                    creation_flags = 0
                
                env = os.environ.copy()
                process = subprocess.Popen(
                    [sys.executable, str(script)],
                    cwd=str(self.project_root),
                    env=env,
                    stdout=stdout,
                    stderr=stderr,
                    creationflags=creation_flags if platform.system() == 'Windows' else 0
                )
                self.processes['twitch'] = process
                self._save_pid('twitch', process)
                print("   ✅ Twitch Bot started (PID: {})".format(process.pid))
                if self.background_mode:
                    print(f"   📝 Logs: {log_file}")
                return True
            except Exception as e:
                print(f"   ❌ Failed to start Twitch Bot: {e}")
                return False
        else:
            # Fallback: Try to start via EventSub server (if available)
            eventsub_script = self.project_root / "src" / "services" / "chat_presence" / "twitch_eventsub_server.py"
            if eventsub_script.exists():
                try:
                    # Configure output based on background mode
                    if self.background_mode:
                        log_file = self.log_dir / "twitch_bot.log"
                        stdout = open(log_file, 'a')
                        stderr = subprocess.STDOUT
                        creation_flags = 0
                        if platform.system() == 'Windows':
                            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
                    else:
                        stdout = subprocess.PIPE
                        stderr = subprocess.PIPE
                        creation_flags = 0
                    
                    env = os.environ.copy()
                    process = subprocess.Popen(
                        [sys.executable, str(eventsub_script)],
                        cwd=str(self.project_root),
                        env=env,
                        stdout=stdout,
                        stderr=stderr,
                        creationflags=creation_flags if platform.system() == 'Windows' else 0
                    )
                    self.processes['twitch'] = process
                    self._save_pid('twitch', process)
                    print("   ✅ Twitch Bot started via EventSub server (PID: {})".format(process.pid))
                    if self.background_mode:
                        print(f"   📝 Logs: {log_file}")
                    return True
                except Exception as e:
                    print(f"   ❌ Failed to start Twitch Bot via EventSub: {e}")
                    print(f"   ⚠️  Note: START_CHAT_BOT_NOW.py not found. Twitch bot may need manual setup.")
                    return False
            else:
                print(f"   ❌ Twitch bot script not found: {script}")
                print(f"   ⚠️  EventSub server also not found: {eventsub_script}")
                print(f"   ℹ️  Twitch bot may need to be started manually or script created")
                return False

    def start_discord_bot(self):
        """Start Discord bot directly using bot_runner module.

        This directly launches the Discord bot for reliable process management.
        """
        print("💬 Starting Discord Bot...")

        # Check configuration
        token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
        if not token:
            print("   ⚠️  Warning: Discord token not set in .env or environment")
            print("   ❌ Cannot start Discord Bot without DISCORD_BOT_TOKEN")
            return False

        try:
            # Pass current environment to subprocess so it inherits .env variables
            env = os.environ.copy()

            # Configure output based on background mode
            if self.background_mode:
                log_file = self.log_dir / "discord_bot.log"
                stdout = open(log_file, 'a')
                stderr = subprocess.STDOUT
                creation_flags = 0
                if platform.system() == 'Windows':
                    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                stdout = subprocess.PIPE
                stderr = subprocess.STDOUT
                creation_flags = 0

            # Run bot_runner directly as a module for clean process management
            process = subprocess.Popen(
                [sys.executable, "-m", "src.discord_commander.bot_runner"],
                cwd=str(self.project_root),
                env=env,
                stdout=stdout,
                stderr=stderr,
                creationflags=creation_flags if platform.system() == 'Windows' else 0
            )
            self.processes['discord'] = process
            self._save_pid('discord', process)
            print("   ✅ Discord Bot started (PID: {})".format(process.pid))
            if self.background_mode:
                print(f"   📝 Logs: {log_file}")
            else:
                # Start thread to monitor output
                Thread(target=self._monitor_process_output, args=('discord', process), daemon=True).start()
            return True
        except Exception as e:
            print(f"   ❌ Failed to start Discord Bot: {e}")
            import traceback
            traceback.print_exc()
            return False

    def scan_project(self, project_path: Path, send_to_thea: bool = True) -> bool:
        """Scan a project and optionally send results to Thea for guidance."""
        print(f"🔍 Scanning project: {project_path}")

        try:
            # Import project scanner integration
            from src.core.project_scanner_integration import ProjectScannerIntegration
            from src.core.error_handling import validate_project_syntax, get_error_handler, ErrorContext, ErrorSeverity, ErrorCategory

            # Perform syntax validation first
            print("   🔧 Running syntax validation...")
            syntax_results = validate_project_syntax(self.project_root)

            if syntax_results["invalid_files"] > 0:
                print(f"   ⚠️  Found {syntax_results['invalid_files']} syntax errors")
                for error in syntax_results["errors"][:5]:  # Show first 5 errors
                    print(f"      ❌ {error['file']}: {error['error']}")
                if len(syntax_results["errors"]) > 5:
                    print(f"      ... and {len(syntax_results['errors']) - 5} more errors")

                # Log syntax errors
                error_handler = get_error_handler("project_scan")
                for error in syntax_results["errors"]:
                    context = ErrorContext(
                        component="project_scan",
                        operation="syntax_validation",
                        metadata={"file": error["file"], "error": error["error"]}
                    )
                    error_handler.log_error(
                        Exception(error["error"]),
                        context,
                        ErrorSeverity.HIGH,
                        ErrorCategory.SYNTAX
                    )
            else:
                print("   ✅ All Python files have valid syntax")

            scanner = ProjectScannerIntegration(self.project_root)

            # Perform scan
            results = scanner.scan_project(
                project_path=project_path,
                send_to_thea=send_to_thea,
                force_rescan=False  # Use cache if available
            )

            if "error" in results:
                print(f"   ❌ Scan failed: {results['error']}")
                return False

            # Display summary
            metadata = results.get("scan_metadata", {})
            scan_data = results.get("scan_data", {})
            thea_guidance = results.get("thea_guidance", {})

            print("   ✅ Project scan completed")
            print(f"   📊 Files analyzed: {len(scan_data)}")
            print(f"   ⏰ Scan duration: {metadata.get('scan_duration', 'Unknown')}s")

            if send_to_thea and "error" not in thea_guidance:
                priority_tasks = thea_guidance.get("priority_tasks", [])
                print(f"   🎯 Thea suggests {len(priority_tasks)} priority tasks")

                # Display top 3 priority tasks
                for i, task in enumerate(priority_tasks[:3], 1):
                    print(f"      {i}. {task}")

            return True

        except ImportError as e:
            print(f"   ⚠️  Project scanner not available: {e}")
            print("   💡 Install project scanner from temp_repos/Auto_Blogger/")
            return False
        except Exception as e:
            print(f"   ❌ Project scan failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def start_auto_gas_pipeline(self, jet_fuel: bool = True, monitoring_interval: int = 60):
        """Start the Auto-Gas Pipeline system for automated agent fuel delivery."""
        print("⛽ Starting Auto-Gas Pipeline System...")

        try:
            # Import and initialize the auto-gas system
            from src.core.auto_gas_pipeline_system import AutoGasPipelineSystem

            self.auto_gas_system = AutoGasPipelineSystem(
                workspace_root=self.project_root,
                monitoring_interval=monitoring_interval
            )

            # Start the system
            success = self.auto_gas_system.start(jet_fuel=jet_fuel)

            if success:
                print("   ✅ Auto-Gas Pipeline started")
                print(f"   🚀 Jet Fuel: {'ENABLED' if jet_fuel else 'DISABLED'}")
                print(f"   ⏱️  Monitoring Interval: {monitoring_interval}s")
                print("   🎯 Thresholds: 75%, 90%, 100% completion")
                return True
            else:
                print("   ❌ Failed to start Auto-Gas Pipeline")
                return False

        except ImportError as e:
            print(f"   ⚠️  Auto-Gas Pipeline not available: {e}")
            print("   💡 System requires src.core.auto_gas_pipeline_system")
            return False
        except Exception as e:
            print(f"   ❌ Failed to start Auto-Gas Pipeline: {e}")
            import traceback
            traceback.print_exc()
            return False

    def check_status(self):
        """Check status of all services."""
        print("\n🔍 SERVICE STATUS CHECK")
        print("=" * 60)

        # Check Message Queue
        print("\n📬 Message Queue Processor:")
        mq_running = self._check_process("message_queue")
        if mq_running:
            print("   ✅ RUNNING")
        else:
            print("   ❌ NOT RUNNING")
            print("   To start: python main.py --message-queue")

        # Check Twitch Bot
        print("\n📺 Twitch Bot:")
        channel = os.getenv("TWITCH_CHANNEL", "").strip()
        token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()
        print(f"   Channel: {channel if channel else 'NOT SET'}")
        print(f"   Token: {'SET' if token else 'NOT SET'}")
        twitch_running = self._check_process("twitch")
        if twitch_running:
            print("   ✅ RUNNING")
        else:
            print("   ❌ NOT RUNNING")
            print("   To start: python main.py --twitch")

        # Check Discord Bot
        print("\n💬 Discord Bot:")
        discord_token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
        print(f"   Token: {'SET' if discord_token else 'NOT SET'}")
        discord_running = self._check_process("discord")
        if discord_running:
            print("   ✅ RUNNING")
        else:
            print("   ❌ NOT RUNNING")
            print("   To start: python main.py --discord")

        # Check Auto-Gas Pipeline
        print("\n⛽ Auto-Gas Pipeline:")
        if hasattr(self, 'auto_gas_system') and self.auto_gas_system:
            status = self.auto_gas_system.get_status()
            if status.get("running"):
                print("   ✅ RUNNING")
                print(f"   Jet Fuel: {'ENABLED' if status.get('jet_fuel_enabled') else 'DISABLED'}")
                print(f"   Interval: {status.get('monitoring_interval')}s")
                print(f"   Deliveries Today: {status.get('gas_deliveries_today')}")
            else:
                print("   ❌ NOT RUNNING")
        else:
            print("   ❌ NOT RUNNING")
            print("   To start: python main.py --auto-gas")

        print("\n" + "=" * 60)

    def _check_process(self, service_name):
        """Check if a service process is running."""
        # First check local processes (for services started in this session)
        if service_name in self.processes:
            process = self.processes[service_name]
            if process.poll() is None:
                return True

        # Check PID file for services started in other sessions
        pid_file = self.pid_dir / f"{service_name}.pid"
        if pid_file.exists():
            try:
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())

                # Check if process is actually running
                if psutil.pid_exists(pid):
                    try:
                        process = psutil.Process(pid)
                        # Check if it's a Python process and cmdline contains the expected service script
                        if process.name().lower() in ['python.exe', 'python3.exe', 'python', 'python3']:
                            cmdline = process.cmdline()

                            # Define expected scripts/modules for each service
                            # Include both script names and module import patterns
                            expected_scripts = {
                                'message_queue': ['start_queue_processor.py', 'start_message_queue_processor.py', 'message_queue_processor'],
                                'twitch': ['START_CHAT_BOT_NOW.py', 'twitch_eventsub_server.py'],
                                'discord': ['bot_runner', 'unified_discord_bot.py', 'discord_commander']
                            }

                            expected = expected_scripts.get(service_name, [])
                            if isinstance(expected, str):
                                expected = [expected]

                            if any(script in ' '.join(cmdline) for script in expected):
                                # Additional check: verify process is responsive (not zombie/hanging)
                                if process.status() in ['running', 'sleeping']:
                                    return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                # PID file exists but process is dead, clean up
                pid_file.unlink()

            except (ValueError, FileNotFoundError):
                # Invalid PID file, remove it
                try:
                    pid_file.unlink()
                except:
                    pass

        # Also check for processes without PID files (orphaned processes)
        # This handles cases where processes were started outside of main.py
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() in ['python.exe', 'python3.exe', 'python', 'python3']:
                        if proc.info['cmdline']:
                            cmdline = ' '.join(proc.info['cmdline'])
                            
                            # Define expected scripts/modules for each service
                            expected_scripts = {
                                'message_queue': ['start_queue_processor.py', 'start_message_queue_processor.py', 'message_queue_processor'],
                                'twitch': ['START_CHAT_BOT_NOW.py', 'twitch_eventsub_server.py'],
                                'discord': ['bot_runner', 'unified_discord_bot.py', 'discord_commander']
                            }
                            
                            expected = expected_scripts.get(service_name, [])
                            if isinstance(expected, str):
                                expected = [expected]
                            
                            # Only match if it's the exact module/script we expect
                            if any(script in cmdline for script in expected):
                                # Verify it's a running process, not zombie/hanging
                                if proc.info['status'] in ['running', 'sleeping']:
                                    return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

        return False

    def _save_pid(self, service_name, process):
        """Save process PID to file for cross-session tracking."""
        pid_file = self.pid_dir / f"{service_name}.pid"
        try:
            with open(pid_file, 'w') as f:
                f.write(str(process.pid))
        except Exception as e:
            print(f"   ⚠️  Failed to save PID file: {e}")

    def _cleanup_pid(self, service_name):
        """Remove PID file for service."""
        pid_file = self.pid_dir / f"{service_name}.pid"
        try:
            if pid_file.exists():
                pid_file.unlink()
        except (Exception, KeyboardInterrupt) as e:
            # Silently handle - PID cleanup is best-effort
            pass

    def _monitor_process_output(self, service_name, process):
        """Monitor process output and display errors."""
        try:
            for line in iter(process.stdout.readline, b''):
                if line:
                    decoded = line.decode('utf-8', errors='replace').strip()
                    if decoded:
                        # Only show errors/warnings to avoid spam
                        if any(keyword in decoded.lower() for keyword in ['error', 'exception', 'failed', 'traceback', 'warning']):
                            print(f"   [{service_name}] {decoded}")
        except Exception:
            pass  # Process may have terminated

    def stop_all(self):
        """Stop all running services."""
        print("\n🛑 Stopping all services...")
        try:
            for name, process in list(self.processes.items()):
                try:
                    if process.poll() is None:
                        print(f"   Stopping {name}...")
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                        print(f"   ✅ {name} stopped")
                    self._cleanup_pid(name)
                except (Exception, KeyboardInterrupt):
                    # Best-effort cleanup - don't let one failure stop others
                    pass

            # Stop Auto-Gas Pipeline if running
            if hasattr(self, 'auto_gas_system') and self.auto_gas_system:
                print("   Stopping auto_gas_pipeline...")
                success = self.auto_gas_system.stop()
                if success:
                    print("   ✅ auto_gas_pipeline stopped")
                else:
                    print("   ⚠️  auto_gas_pipeline stop may have failed")

            # Also clean up PID files for services started in other sessions
            for service_name in ['message_queue', 'twitch', 'discord']:
                self._cleanup_pid(service_name)

            self.processes.clear()
        except (Exception, KeyboardInterrupt):
            # Ensure we always clear the processes dict
            self.processes.clear()

    def stop_service(self, service_name: str, force: bool = False):
        """Stop a specific service by reading its PID file."""
        pid_file = self.pid_dir / f"{service_name}.pid"
        
        if not pid_file.exists():
            print(f"   ⚠️  No PID file found for {service_name} (may not be running)")
            return False
        
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            if not psutil.pid_exists(pid):
                print(f"   ⚠️  Process {pid} for {service_name} not found (already stopped)")
                self._cleanup_pid(service_name)
                return False
            
            process = psutil.Process(pid)
            
            # Verify it's the right process
            cmdline = ' '.join(process.cmdline())
            expected_scripts = {
                'message_queue': ['start_queue_processor.py', 'start_message_queue_processor.py', 'message_queue_processor'],
                'twitch': ['START_CHAT_BOT_NOW.py', 'twitch_eventsub_server.py'],
                'discord': ['bot_runner', 'unified_discord_bot.py', 'discord_commander']
            }
            
            expected = expected_scripts.get(service_name, [])
            if not any(script in cmdline for script in expected):
                print(f"   ⚠️  PID {pid} doesn't match expected {service_name} process")
                return False
            
            print(f"   Stopping {service_name} (PID: {pid})...")
            
            if force:
                process.kill()
                print(f"   ✅ {service_name} force killed")
            else:
                process.terminate()
                try:
                    process.wait(timeout=5)
                    print(f"   ✅ {service_name} stopped gracefully")
                except psutil.TimeoutExpired:
                    process.kill()
                    print(f"   ✅ {service_name} force killed (didn't respond to terminate)")
            
            self._cleanup_pid(service_name)
            return True
            
        except (ValueError, FileNotFoundError, psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"   ❌ Error stopping {service_name}: {e}")
            # Clean up invalid PID file
            try:
                if pid_file.exists():
                    pid_file.unlink()
            except:
                pass
            return False

    def stop_all_services(self, force: bool = False):
        """Stop all services by reading PID files (for background services)."""
        print("\n🛑 Stopping all services...")
        print("=" * 60)
        
        # First stop services from current session
        if self.processes:
            print("\n🛑 Stopping services from current session...")
            for name, process in list(self.processes.items()):
                if process.poll() is None:
                    print(f"   Stopping {name}...")
                    if force:
                        process.kill()
                    else:
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                    print(f"   ✅ {name} stopped")
                    self._cleanup_pid(name)
            self.processes.clear()
        
        # Then stop services from PID files (background services)
        services = ['message_queue', 'twitch', 'discord']
        stopped_count = 0
        
        for service_name in services:
            if self.stop_service(service_name, force=force):
                stopped_count += 1
        
        print()
        print("=" * 60)
        if stopped_count > 0:
            print(f"✅ Stopped {stopped_count} background service(s)")
        else:
            print("ℹ️  No background services found running")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console


def show_autonomous_reports():
    """Display autonomous configuration reports."""
    print("🤖 AUTONOMOUS CONFIG SYSTEM - REPORTS")
    print("=" * 60)

    reports_dir = Path("autonomous_config_reports")

    if not reports_dir.exists():
        print("❌ Autonomous config reports directory not found")
=======
    if not all_status:
        print("❌ No services configured or found.")
        print("\n💡 Quick Fix:")
        print("   1. Run setup: python setup.py")
        print("   2. Check config: python setup_wizard.py --validate")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        return

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

        try:
            import time
            running_check_count = 0

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
<<<<<<< HEAD
    """Main entry point."""
<<<<<<< HEAD
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
=======
    parser = argparse.ArgumentParser(
        description="Agent Cellphone V2 - Unified Service Launcher"
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Check status of all services'
    )
    parser.add_argument(
        '--message-queue',
        action='store_true',
        help='Start only Message Queue Processor'
    )
    parser.add_argument(
        '--twitch',
        action='store_true',
        help='Start only Twitch Bot'
    )
    parser.add_argument(
        '--discord',
        action='store_true',
        help='Start only Discord Bot'
    )
    parser.add_argument(
        '--select-mode',
        action='store_true',
        help='Select agent mode (interactive)'
    )
    parser.add_argument(
        '--background',
        action='store_true',
        help='Run services in background and exit immediately'
    )
    parser.add_argument(
        '--stop',
        action='store_true',
        help='Stop all running services (reads from PID files)'
    )
    parser.add_argument(
        '--kill',
        action='store_true',
        help='Force kill all running services (use if --stop fails)'
    )
    parser.add_argument(
        '--auto-gas',
        action='store_true',
        help='Start Auto-Gas Pipeline system for automated agent fuel delivery'
    )
    parser.add_argument(
        '--no-jet-fuel',
        action='store_true',
        help='Disable jet fuel optimization in auto-gas pipeline'
    )
    parser.add_argument(
        '--scan-project',
        nargs='?',
        const='.',
        help='Scan project on startup and send to Thea (default: current directory)'
    )
    parser.add_argument(
        '--scan-no-thea',
        action='store_true',
        help='Scan project but skip sending to Thea'
    )
    parser.add_argument(
        '--autonomous-reports',
        action='store_true',
        help='Display autonomous configuration reports'
    )
    parser.add_argument(
        '--run-autonomous-config',
        action='store_true',
        help='Run autonomous configuration system (dry run by default)'
    )
=======
    """Main entry point - simplified launcher using modular components."""
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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
<<<<<<< HEAD
                manager.stop_all()
            except (Exception, KeyboardInterrupt):
                # Force cleanup on second interrupt
                pass
            print("\n👋 All services stopped. Goodbye!")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
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
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1


if __name__ == "__main__":
    main()
