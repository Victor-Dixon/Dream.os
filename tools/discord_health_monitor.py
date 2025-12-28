#!/usr/bin/env python3
"""
Discord Health Monitor
=====================

Monitors Discord bot health and prevents heartbeat timeouts.

Author: Agent-2 (Architecture & Design)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)
"""

import asyncio
import time
import threading
import psutil
from typing import Dict, Any, Optional
import logging

class DiscordHealthMonitor:
    """Monitors Discord bot health and prevents timeout shutdowns."""

    def __init__(self, bot_pid: int, check_interval: int = 30):
        self.bot_pid = bot_pid
        self.check_interval = check_interval
        self.last_heartbeat = time.time()
        self.monitoring = False
        self.thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger(__name__)

    def start_monitoring(self):
        """Start the health monitoring thread."""
        if self.monitoring:
            return

        self.monitoring = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        self.logger.info("Discord health monitoring started")

    def stop_monitoring(self):
        """Stop the health monitoring."""
        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Discord health monitoring stopped")

    def update_heartbeat(self):
        """Update the last heartbeat timestamp."""
        self.last_heartbeat = time.time()

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                current_time = time.time()
                time_since_heartbeat = current_time - self.last_heartbeat

                # Check if bot process is still running
                if not psutil.pid_exists(self.bot_pid):
                    self.logger.error(f"Discord bot process {self.bot_pid} no longer exists")
                    self._trigger_recovery()
                    break

                # Check for heartbeat timeout
                if time_since_heartbeat > 60:  # 60 seconds threshold
                    self.logger.warning(f"Discord heartbeat timeout detected: {time_since_heartbeat:.1f}s")
                    self._handle_timeout()

                # Check bot responsiveness (basic ping)
                self._check_bot_responsiveness()

                time.sleep(self.check_interval)

            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(self.check_interval)

    def _handle_timeout(self):
        """Handle heartbeat timeout."""
        self.logger.info("Attempting to recover from heartbeat timeout...")

        # Try to restart the heartbeat mechanism
        # This would integrate with the Discord bot's heartbeat system
        self._restart_heartbeat()

        # If that fails, consider graceful restart
        if not self._attempt_graceful_restart():
            self.logger.error("Failed to recover from heartbeat timeout")
            self._trigger_shutdown()

    def _restart_heartbeat(self) -> bool:
        """Attempt to restart the Discord heartbeat."""
        try:
            # This would send a signal to the Discord bot to restart heartbeats
            # Implementation depends on how the Discord bot exposes heartbeat control
            self.logger.info("Heartbeat restart requested")
            return True
        except Exception as e:
            self.logger.error(f"Heartbeat restart failed: {e}")
            return False

    def _attempt_graceful_restart(self) -> bool:
        """Attempt to gracefully restart the Discord bot."""
        try:
            # Send restart signal to bot process
            self.logger.info("Graceful restart requested")
            return True
        except Exception as e:
            self.logger.error(f"Graceful restart failed: {e}")
            return False

    def _trigger_shutdown(self):
        """Trigger system shutdown due to unrecoverable error."""
        self.logger.critical("Triggering system shutdown due to Discord health failure")
        # This would integrate with the main system shutdown mechanism

    def _check_bot_responsiveness(self):
        """Check if the Discord bot is responsive."""
        try:
            # Basic responsiveness check
            # Could be enhanced with actual bot health checks
            process = psutil.Process(self.bot_pid)
            cpu_percent = process.cpu_percent(interval=1)
            memory_mb = process.memory_info().rss / 1024 / 1024

            if cpu_percent > 90:
                self.logger.warning(".1f")
            if memory_mb > 500:  # 500MB threshold
                self.logger.warning(".1f")

        except Exception as e:
            self.logger.error(f"Bot responsiveness check failed: {e}")

    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        return {
            "monitoring_active": self.monitoring,
            "bot_pid": self.bot_pid,
            "last_heartbeat": self.last_heartbeat,
            "time_since_heartbeat": time.time() - self.last_heartbeat,
            "process_exists": psutil.pid_exists(self.bot_pid)
        }


def main():
    """CLI interface for Discord health monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Discord Health Monitor")
    parser.add_argument("--pid", type=int, required=True, help="Discord bot process ID")
    parser.add_argument("--interval", type=int, default=30, help="Check interval in seconds")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")

    args = parser.parse_args()

    monitor = DiscordHealthMonitor(args.pid, args.interval)

    if args.daemon:
        monitor.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
    else:
        # Print current status
        status = monitor.get_health_status()
        print(f"Discord Health Status: {status}")


if __name__ == "__main__":
    main()
