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
    python main.py                    # Start all services
    python main.py --status            # Check service status
    python main.py --select-mode       # Select agent mode (interactive)
    python main.py --message-queue    # Start only message queue
    python main.py --twitch           # Start only Twitch bot
    python main.py --discord          # Start only Discord bot
    python main.py --help             # Show help

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
from pathlib import Path
from threading import Thread
from typing import Optional

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

load_dotenv()


class ServiceManager:
    """Manages all critical services."""

    def __init__(self):
        self.project_root = project_root
        self.processes = {}
        self.pid_dir = self.project_root / "pids"
        self.pid_dir.mkdir(exist_ok=True)
        self.agent_mode_manager: Optional[object] = None

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
                print("   ⚠️  Agent mode manager not available, using default 4-agent mode")
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
                choice = input("Select agent mode (or press Enter to keep current): ").strip()

                if not choice:  # Keep current
                    print(f"✅ Keeping current mode: {current_mode}")
                    return

                if choice in available_modes:
                    if self.agent_mode_manager.set_mode(choice):
                        new_mode = self.agent_mode_manager.get_current_mode()
                        active_agents = self.agent_mode_manager.get_active_agents()
                        print(f"✅ Agent mode set to: {new_mode}")
                        print(f"   Active agents: {', '.join(active_agents)}")
                        print(f"   Monitor setup: {self.agent_mode_manager.get_monitor_setup()}")
                        return
                    else:
                        print(f"❌ Failed to set mode: {choice}")
                else:
                    print(f"❌ Invalid mode. Available: {', '.join(available_modes)}")

            except KeyboardInterrupt:
                print("\n⚠️  Mode selection canceled, keeping current mode")
                return
            except Exception as e:
                print(f"❌ Error selecting mode: {e}")
                return

    def start_message_queue(self):
        """Start message queue processor."""
        print("📬 Starting Message Queue Processor...")
        script = self.project_root / "tools" / "start_message_queue_processor.py"
        if not script.exists():
            print(f"   ❌ Script not found: {script}")
            return False

        try:
            process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['message_queue'] = process
            self._save_pid('message_queue', process)
            print("   ✅ Message Queue Processor started (PID: {})".format(process.pid))
            return True
        except Exception as e:
            print(f"   ❌ Failed to start Message Queue: {e}")
            return False

    def start_twitch_bot(self):
        """Start Twitch bot."""
        print("📺 Starting Twitch Bot...")
        script = self.project_root / "tools" / "START_CHAT_BOT_NOW.py"
        if not script.exists():
            print(f"   ❌ Script not found: {script}")
            return False

        # Check configuration
        channel = os.getenv("TWITCH_CHANNEL", "").strip()
        token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()

        if not channel or not token:
            print("   ⚠️  Warning: Twitch configuration incomplete")
            print(f"      Channel: {'SET' if channel else 'NOT SET'}")
            print(f"      Token: {'SET' if token else 'NOT SET'}")

        try:
            process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['twitch'] = process
            self._save_pid('twitch', process)
            print("   ✅ Twitch Bot started (PID: {})".format(process.pid))
            return True
        except Exception as e:
            print(f"   ❌ Failed to start Twitch Bot: {e}")
            return False

    def start_discord_bot(self):
        """Start Discord bot."""
        print("💬 Starting Discord Bot...")
        script = self.project_root / "tools" / "run_unified_discord_bot_with_restart.py"
        if not script.exists():
            # Try alternative location
            script = self.project_root / "src" / \
                "discord_commander" / "unified_discord_bot.py"
            if not script.exists():
                print(f"   ❌ Script not found: {script}")
                return False

        # Check configuration
        token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
        if not token:
            print("   ⚠️  Warning: Discord token not set")

        try:
            # Pass current environment to subprocess so it inherits .env variables
            env = os.environ.copy()
            process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(self.project_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['discord'] = process
            self._save_pid('discord', process)
            print("   ✅ Discord Bot started (PID: {})".format(process.pid))
            return True
        except Exception as e:
            print(f"   ❌ Failed to start Discord Bot: {e}")
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

                            # Define expected scripts for each service
                            expected_scripts = {
                                'message_queue': 'start_message_queue_processor.py',
                                'twitch': 'START_CHAT_BOT_NOW.py',
                                'discord': ['run_unified_discord_bot_with_restart.py', 'unified_discord_bot.py']
                            }

                            expected = expected_scripts.get(service_name, [])
                            if isinstance(expected, str):
                                expected = [expected]

                            if any(script in ' '.join(cmdline) for script in expected):
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
        except Exception as e:
            print(f"   ⚠️  Failed to cleanup PID file: {e}")

    def stop_all(self):
        """Stop all running services."""
        print("\n🛑 Stopping all services...")
        for name, process in self.processes.items():
            if process.poll() is None:
                print(f"   Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print(f"   ✅ {name} stopped")
                self._cleanup_pid(name)

        # Also clean up PID files for services started in other sessions
        for service_name in ['message_queue', 'twitch', 'discord']:
            self._cleanup_pid(service_name)

        self.processes.clear()


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

    args = parser.parse_args()

    manager = ServiceManager()

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

    # Start specific services
    if args.message_queue:
        manager.start_message_queue()
        print("\n💡 Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_all()
    elif args.twitch:
        manager.start_twitch_bot()
        print("\n💡 Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_all()
    elif args.discord:
        manager.start_discord_bot()
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
            print(f"Agent Mode: {current_mode} ({len(active_agents)} agents, {monitor_setup} monitor)")
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
            print("\n\n🛑 Shutting down all services...")
            manager.stop_all()
            print("\n👋 All services stopped. Goodbye!")


if __name__ == "__main__":
    main()




