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
from pathlib import Path
from threading import Thread
from typing import Optional

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Always load repo-root .env (avoid accidentally loading a parent-directory .env)
load_dotenv(dotenv_path=project_root / ".env")


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
                    # Detach so bot survives when main.py/terminal closes
                    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
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
                        if process.name().lower() in ['python.exe', 'python3.exe', 'python']:
                            cmdline = process.cmdline()

                            # Define expected scripts/modules for each service
                            # Include both script names and module import patterns
                            expected_scripts = {
                                'message_queue': ['start_message_queue_processor.py', 'message_queue_processor'],
                                'twitch': ['START_CHAT_BOT_NOW.py', 'twitch_eventsub_server.py'],
                                # Be strict: only count the actual Discord bot runner, not unrelated discord tooling
                                'discord': ['bot_runner']
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
                    if proc.info['name'] and proc.info['name'].lower() in ['python.exe', 'python3.exe', 'python']:
                        if proc.info['cmdline']:
                            cmdline = ' '.join(proc.info['cmdline'])
                            
                            # Define expected scripts/modules for each service
                            expected_scripts = {
                                'message_queue': ['start_message_queue_processor.py', 'message_queue_processor'],
                                'twitch': ['START_CHAT_BOT_NOW.py', 'twitch_eventsub_server.py'],
                                # Be strict: only count the actual Discord bot runner, not unrelated discord tooling
                                'discord': ['bot_runner']
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
                # Be strict: only stop the actual Discord bot runner
                'discord': ['bot_runner']
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

        print()
        print("=" * 60)
        print(f"✅ Started {success_count}/3 services")
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
