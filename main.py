#!/usr/bin/env python3
"""
Main Service Launcher - Agent Cellphone V2
==========================================

Unified entry point to start and manage all critical services:
- Message Queue Processor
- Twitch Bot
- Discord Bot

Features:
- Interactive agent mode selection (4-agent, 5-agent, 6-agent, 8-agent)
- Service status monitoring
- Individual service control

Usage:
    python main.py                    # Start all services (foreground)
    python main.py --background       # Start all services in background
    python main.py --status            # Check service status
    python main.py --stop             # Stop all background services
    python main.py --kill             # Force kill all services
    python main.py --select-mode       # Select agent mode (interactive)
    python main.py --message-queue    # Start only message queue
    python main.py --twitch           # Start only Twitch bot
    python main.py --discord          # Start only Discord bot
    python main.py --autonomous-reports # Display autonomous config reports
    python main.py --run-autonomous-config # Run autonomous config system
    python main.py --cleanup-logs     # Clean up old log files
    python main.py --help             # Show help

Background Mode:
    With --background, services run as detached processes and main.py exits.
    Services continue running after the terminal closes.
    
    To run main.py itself in background (Windows):
        start /B python main.py --background
    
    To run main.py itself in background (Unix/Mac):
        python main.py --background &
        nohup python main.py --background &

Author: Agent-2
V2 Compliant: <300 lines
"""

from dotenv import load_dotenv
import argparse
import os
import sys
import subprocess
import time
import psutil
import platform
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import Thread
from typing import Optional

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "systems"))  # Add systems directory for Wave C extracted components

load_dotenv()


def cleanup_old_logs(log_dir: Path, max_age_days: int = 30, max_size_mb: int = 50) -> int:
    """Clean up old and oversized log files to prevent disk space issues."""
    import time
    import os

    if not log_dir.exists():
        return 0

    cleaned_count = 0
    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60
    max_size_bytes = max_size_mb * 1024 * 1024

    for log_file in log_dir.glob("*.log"):
        try:
            # Check file age
            file_age = current_time - log_file.stat().st_mtime
            file_size = log_file.stat().st_size

            # Remove if too old or too large
            if file_age > max_age_seconds or file_size > max_size_bytes:
                log_file.unlink()
                cleaned_count += 1
                print(f"   🗑️ Removed old/oversized log: {log_file.name} ({file_size/1024/1024:.1f}MB, {file_age/86400:.1f} days old)")
        except Exception as e:
            print(f"   ⚠️ Failed to clean log {log_file.name}: {e}")

    return cleaned_count


def setup_logging(log_dir: Path, log_level: int = logging.INFO) -> logging.Logger:
    """Setup logging with rotation for main service launcher."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "main_service_launcher.log"

    # Create logger
    logger = logging.getLogger('main_service_launcher')
    logger.setLevel(log_level)

    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create rotating file handler (max 10MB per file, keep 5 backup files)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class ServiceManager:
    """Manages all critical services."""

    def __init__(self, background_mode: bool = False):
        self.project_root = project_root
        self.processes = {}
        self.pid_dir = self.project_root / "pids"
        self.pid_dir.mkdir(exist_ok=True)
        self.log_dir = self.project_root / "runtime" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.agent_mode_manager: Optional[object] = None
        self.background_mode = background_mode
        self.auto_gas_system: Optional[object] = None

        # Setup logging for service manager
        self.logger = setup_logging(self.log_dir, logging.INFO)

        # Clean up old logs on startup
        cleaned_logs = cleanup_old_logs(self.log_dir)
        if cleaned_logs > 0:
            self.logger.info(f"Cleaned up {cleaned_logs} old/oversized log files on startup")

    def setup_agent_mode_manager(self):
        """Setup agent mode manager."""
        try:
            sys.path.insert(0, str(self.project_root / "src"))
            from src.core.agent_mode_manager import get_mode_manager
            self.agent_mode_manager = get_mode_manager()
            return True
        except ImportError as e:
            print(f"   ⚠️  Warning: Could not import agent mode manager: {e}")
            return False

    def select_agent_mode(self):
        """Interactive agent mode selection."""
        if not self.agent_mode_manager:
            if not self.setup_agent_mode_manager():
                print(
                    "   ⚠️  Agent mode manager not available, using default 4-agent mode")
                return

        print("\n🔧 AGENT MODE SELECTION")
        print("=" * 40)

        current_mode = self.agent_mode_manager.get_current_mode()
        available_modes = self.agent_mode_manager.get_available_modes()

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
            # Validate script exists and is executable
            if not script.exists():
                print(f"   ❌ Message Queue script not found: {script}")
                print(f"   📝 Expected location: scripts/start_queue_processor.py or tools/start_message_queue_processor.py")
                return False

            # Pass current environment to subprocess so it inherits .env variables
            env = os.environ.copy()

            # Configure output based on background mode
            stdout = None
            stderr = None
            creation_flags = 0

            try:
                if self.background_mode:
                    log_file = self.log_dir / "message_queue.log"
                    stdout = open(log_file, 'a')
                    stderr = subprocess.STDOUT
                    if platform.system() == 'Windows':
                        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
                else:
                    stdout = subprocess.PIPE
                    stderr = subprocess.STDOUT
            except (OSError, IOError) as file_error:
                print(f"   ❌ Failed to open log file: {file_error}")
                return False

            try:
                process = subprocess.Popen(
                    [sys.executable, str(script)],
                    cwd=str(self.project_root),
                    env=env,
                    stdout=stdout,
                    stderr=stderr,
                    creationflags=creation_flags if platform.system() == 'Windows' else 0
                )
            except (OSError, FileNotFoundError) as proc_error:
                print(f"   ❌ Failed to create subprocess: {proc_error}")
                print("   💡 Check if Python executable is available and script is valid")
                return False
            except subprocess.SubprocessError as sub_error:
                print(f"   ❌ Subprocess error: {sub_error}")
                return False

            # Verify process started successfully
            if process.poll() is not None:
                # Process exited immediately
                exit_code = process.returncode
                print(f"   ❌ Message Queue process exited immediately (exit code: {exit_code})")
                return False

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
            error_type = type(e).__name__
            print(f"   ❌ Failed to start Message Queue ({error_type}): {e}")
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

        # Validate and normalize channel format
        if channel.startswith("#"):
            channel = channel[1:]
            print(f"   ⚠️  Removed # prefix from channel: {channel}")

        if "twitch.tv/" in channel.lower():
            # Extract channel name from URL
            parts = channel.lower().split("twitch.tv/")
            if len(parts) > 1:
                channel = parts[-1].split("/")[0].split("?")[0].rstrip("/")
                print(f"   ⚠️  Extracted channel name from URL: {channel}")

        # Normalize channel (lowercase, no spaces)
        channel = channel.lower().strip()

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
            # Validate Discord module is available
            try:
                import src.discord_commander.bot_runner
            except ImportError as import_error:
                print(f"   ❌ Discord bot module not found: {import_error}")
                print("   💡 Run: pip install discord.py")
                return False

            # Pass current environment to subprocess so it inherits .env variables
            env = os.environ.copy()

            # Configure output based on background mode
            stdout = None
            stderr = None
            creation_flags = 0
            log_file = None

            try:
                if self.background_mode:
                    log_file = self.log_dir / "discord_bot.log"
                    stdout = open(log_file, 'a')
                    stderr = subprocess.STDOUT
                    if platform.system() == 'Windows':
                        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
                else:
                    stdout = subprocess.PIPE
                    stderr = subprocess.STDOUT
            except (OSError, IOError) as file_error:
                print(f"   ❌ Failed to open Discord log file: {file_error}")
                return False

            try:
                # Run bot_runner directly as a module for clean process management
                process = subprocess.Popen(
                    [sys.executable, "-m", "src.discord_commander.bot_runner"],
                    cwd=str(self.project_root),
                    env=env,
                    stdout=stdout,
                    stderr=stderr,
                    creationflags=creation_flags if platform.system() == 'Windows' else 0
                )
            except (OSError, FileNotFoundError) as proc_error:
                print(f"   ❌ Failed to create Discord subprocess: {proc_error}")
                print("   💡 Check if Python executable is available and discord module is properly installed")
                return False
            except subprocess.SubprocessError as sub_error:
                print(f"   ❌ Discord subprocess error: {sub_error}")
                return False

            # Verify process started successfully
            if process.poll() is not None:
                # Process exited immediately
                exit_code = process.returncode
                print(f"   ❌ Discord Bot process exited immediately (exit code: {exit_code})")
                return False

            self.processes['discord'] = process
            self._save_pid('discord', process)
            print("   ✅ Discord Bot started (PID: {})".format(process.pid))
            if self.background_mode and log_file:
                print(f"   📝 Logs: {log_file}")
            else:
                # Start thread to monitor output
                Thread(target=self._monitor_process_output, args=('discord', process), daemon=True).start()
            return True

        except Exception as e:
            error_type = type(e).__name__
            print(f"   ❌ Failed to start Discord Bot ({error_type}): {e}")
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


def show_autonomous_reports():
    """Display autonomous configuration reports."""
    print("🤖 AUTONOMOUS CONFIG SYSTEM - REPORTS")
    print("=" * 60)

    reports_dir = Path("autonomous_config_reports")

    if not reports_dir.exists():
        print("❌ Autonomous config reports directory not found")
        return

    # Display master report
    master_report = reports_dir / "autonomous_master_report.md"
    if master_report.exists():
        print("📋 MASTER REPORT:")
        print("-" * 30)
        try:
            with open(master_report, 'r', encoding='utf-8') as f:
                content = f.read()
                # Show first 2000 characters to avoid overwhelming output
                if len(content) > 2000:
                    print(content[:2000] + "\n... (truncated)")
                else:
                    print(content)
        except Exception as e:
            print(f"❌ Error reading master report: {e}")
    else:
        print("❌ Master report not found")

    # List available reports
    print("\n📁 AVAILABLE REPORTS:")
    print("-" * 30)
    for report_file in sorted(reports_dir.glob("*.md")):
        print(f"📄 {report_file.name}")

    print("\n💡 Use individual report files for detailed analysis")
    print("📂 Location: autonomous_config_reports/")


def run_autonomous_config_system():
    """Run the autonomous configuration system."""
    print("🤖 AUTONOMOUS CONFIG SYSTEM - EXECUTION")
    print("=" * 60)

    try:
        # Import the autonomous config orchestrator
        from src.utils.autonomous_config_orchestrator import AutonomousConfigOrchestrator

        # Run autonomous configuration (dry run by default)
        root_dir = Path("src")
        orchestrator = AutonomousConfigOrchestrator(root_dir=root_dir, auto_apply=False)

        print("🔍 Running autonomous configuration analysis...")
        results = orchestrator.run_autonomous_consolidation()

        print("✅ Autonomous configuration analysis complete!")
        print("\n📊 SUMMARY:")
        print(f"   Patterns Found: {results.get('patterns_found', 0)}")
        print(f"   Files Processed: {results.get('files_processed', 0)}")
        print(f"   Issues Detected: {results.get('issues_detected', 0)}")

        print("\n📋 REPORTS GENERATED:")
        print("   - autonomous_config_reports/autonomous_master_report.md")
        print("   - autonomous_config_reports/autonomous_consolidation_report.md")
        print("   - autonomous_config_reports/autonomous_migration_report.md")
        print("   - autonomous_config_reports/autonomous_remediation_report.md")

        print("\n💡 Run 'python main.py --autonomous-reports' to view results")
    except ImportError as e:
        print(f"❌ Autonomous config system not available: {e}")
        print("💡 The autonomous config orchestrator may need to be implemented")
    except Exception as e:
        print(f"❌ Error running autonomous config system: {e}")


def main():
    """Main entry point."""
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
    parser.add_argument(
        '--cleanup-logs',
        action='store_true',
        help='Clean up old and oversized log files'
    )

    args = parser.parse_args()

    manager = ServiceManager(background_mode=args.background)

    # Setup agent mode manager
    manager.setup_agent_mode_manager()

    # Agent mode selection mode
    if args.select_mode:
        manager.select_agent_mode()
        return

    # Status check mode
    if args.status:
        manager.check_status()
        return

    # Log cleanup mode
    if args.cleanup_logs:
        log_dir = project_root / "runtime" / "logs"
        cleaned_count = cleanup_old_logs(log_dir)
        print(f"✅ Log cleanup completed: {cleaned_count} files removed")
        return

    # Stop services mode
    if args.stop or args.kill:
        manager.stop_all_services(force=args.kill)
        return

    # Start specific services
    if args.message_queue:
        manager.start_message_queue()
        if args.background:
            print("\n✅ Service started in background")
            print("   To check status: python main.py --status")
            return
        print("\n💡 Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_all()
    elif args.twitch:
        manager.start_twitch_bot()
        if args.background:
            print("\n✅ Service started in background")
            print("   To check status: python main.py --status")
            return
        print("\n💡 Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_all()
    elif args.discord:
        manager.start_discord_bot()
        if args.background:
            print("\n✅ Service started in background")
            print("   To check status: python main.py --status")
            return
        print("\n💡 Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_all()
    elif args.autonomous_reports:
        # Display autonomous configuration reports
        show_autonomous_reports()
        return
    elif args.run_autonomous_config:
        # Run autonomous configuration system
        run_autonomous_config_system()
        return
    else:
        # Start all services
        print("🚀 AGENT CELLPHONE V2 - SERVICE LAUNCHER")
        print("=" * 60)

        # Show current agent mode
        if manager.agent_mode_manager:
            current_mode = manager.agent_mode_manager.get_current_mode()
            active_agents = manager.agent_mode_manager.get_active_agents()
            monitor_setup = manager.agent_mode_manager.get_monitor_setup()
            print(
                f"Agent Mode: {current_mode} ({len(active_agents)} agents, {monitor_setup} monitor)")
            print(f"Active Agents: {', '.join(active_agents)}")
        print()

        success_count = 0
        if manager.start_message_queue():
            success_count += 1
        time.sleep(1)

        if manager.start_twitch_bot():
            success_count += 1
        time.sleep(1)

        if manager.start_discord_bot():
            success_count += 1
        time.sleep(1)

        # Start Auto-Gas Pipeline if requested
        if args.auto_gas:
            jet_fuel_enabled = not args.no_jet_fuel
            if manager.start_auto_gas_pipeline(jet_fuel=jet_fuel_enabled):
                success_count += 1
                print("⛽ Auto-Gas Pipeline: ACTIVE")
            else:
                print("⛽ Auto-Gas Pipeline: FAILED")

        # Scan project if requested
        if args.scan_project:
            project_path = Path(args.scan_project).resolve()
            send_to_thea = not args.scan_no_thea

            if manager.scan_project(project_path, send_to_thea):
                print("🔍 Project Scan: COMPLETED")
                if send_to_thea:
                    print("🤖 Thea Guidance: REQUESTED")
                else:
                    print("🤖 Thea Guidance: SKIPPED")
            else:
                print("🔍 Project Scan: FAILED")

        print()
        print("=" * 60)
        base_services = 3
        total_services = base_services + (1 if args.auto_gas else 0)
        print(f"✅ Started {success_count}/{total_services} services")
        if args.auto_gas:
            print("   Including: Auto-Gas Pipeline (perpetual fuel delivery)")
        print()
        
        if args.background:
            print("✅ All services started in background")
            print("   To check status: python main.py --status")
            print("   To stop services: python main.py --stop")
            print("   To force kill: python main.py --kill")
            print("   To change agent mode: python main.py --select-mode")
            print("   PIDs saved to: pids/ directory")
            print("   Logs saved to: runtime/logs/ directory")
            return

        print("💡 All services running. Press Ctrl+C to stop all services.")
        print("   To check status: python main.py --status")
        print("   To change agent mode: python main.py --select-mode")
        print()

        try:
            while True:
                time.sleep(1)
                # Check if any process died
                for name, process in list(manager.processes.items()):
                    if process.poll() is not None:
                        print(
                            f"⚠️  {name} process exited (code: {process.returncode})")
                        del manager.processes[name]
        except KeyboardInterrupt:
            print("\n\n📦 Shutting down all services...")
            try:
                manager.stop_all()
            except (Exception, KeyboardInterrupt):
                # Force cleanup on second interrupt
                pass
            print("\n👋 All services stopped. Goodbye!")


if __name__ == "__main__":
    main()
