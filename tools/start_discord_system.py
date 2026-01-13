#!/usr/bin/env python3
"""
Start Complete Discord System
==============================

Starts both Discord bot and message queue processor.
Ensures .env file is loaded properly.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps)
Date: 2025-01-27
Priority: CRITICAL
"""

import logging
import os
import subprocess
import sys
import time
import atexit
from pathlib import Path

# Load .env file FIRST
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import psutil (optional but recommended)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("⚠️  psutil not installed - single-instance check will be limited")
    logger.warning("   Install with: pip install psutil (recommended)")

# Lock file for single instance
LOCK_FILE = Path("logs/discord_system.lock")


def cleanup_lock():
    """Remove lock file on exit."""
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def check_existing_instance():
    """Check if another instance is already running."""
    if not LOCK_FILE.exists():
        return None

    try:
        pid = int(LOCK_FILE.read_text().strip())

        if PSUTIL_AVAILABLE:
            if psutil.pid_exists(pid):
                # Double-check it's actually our process
                try:
                    proc = psutil.Process(pid)
                    cmdline = ' '.join(proc.cmdline())
                    if 'start_discord_system.py' in cmdline:
                        logger.warning(f"⚠️  Found existing instance (PID {pid})")
                        return pid
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        # If we get here, either psutil not available or process not found
        logger.warning(f"⚠️  Found stale lock file (PID {pid} not running)")
        LOCK_FILE.unlink()
        return None

    except (ValueError, FileNotFoundError):
        # Invalid lock file or doesn't exist
        try:
            LOCK_FILE.unlink()
        except Exception:
            pass
        return None


def create_lock():
    """Create lock file with current PID."""
    try:
        # Ensure logs directory exists
        LOCK_FILE.parent.mkdir(exist_ok=True)

        # Write current PID
        LOCK_FILE.write_text(str(os.getpid()))

        # Register cleanup on exit
        atexit.register(cleanup_lock)

        logger.info(f"✅ Lock file created (PID: {os.getpid()})")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create lock file: {e}")
        return False


def check_token():
    """Check if Discord token is set."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN not set!")
        logger.error("   Set it in .env file or environment variable")
        return False
    if len(token) < 50:
        logger.warning(f"⚠️  Token appears invalid (length: {len(token)})")
        return False
    logger.info("✅ Discord bot token found")
    return True


def start_discord_bot():
    """Start Discord bot in background."""
    logger.info("🤖 Starting Discord bot...")
    try:
        # Create log directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Use the working unified discord bot
        process = subprocess.Popen(
            [sys.executable, "src/discord_commander/unified_discord_bot.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(Path.cwd())
        )

        # Give it a moment to start
        time.sleep(2)

        # Check if it started successfully
        if process.poll() is not None:
            logger.error(f"❌ Discord bot exited immediately (exit code: {process.returncode})")
            return None

        logger.info(f"✅ Discord bot started (PID: {process.pid})")
        return process

    except Exception as e:
        logger.error(f"❌ Failed to start Discord bot: {e}", exc_info=True)
        return None


def start_queue_processor():
    """Start message queue processor in background."""
    logger.info("📨 Starting message queue processor...")
    try:
        # Create log directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Redirect output to log files
        stdout_file = log_dir / "message_queue.log"
        stderr_file = log_dir / "message_queue_errors.log"

        with open(stdout_file, "w", encoding="utf-8") as stdout, \
                open(stderr_file, "w", encoding="utf-8") as stderr:
            process = subprocess.Popen(
                [sys.executable, "tools/utilities/start_message_queue.py"],
                stdout=stdout,
                stderr=stderr,
                text=True,
                cwd=str(Path.cwd())
            )

        # Give it a moment to start
        time.sleep(2)

        # Check if it started successfully
        if process.poll() is not None:
            logger.error(f"❌ Queue processor exited immediately (exit code: {process.returncode})")
            logger.error(f"   Check logs: {stdout_file} and {stderr_file}")
            # Read error output
            try:
                with open(stderr_file, "r", encoding="utf-8") as f:
                    error_output = f.read(1000)
                    if error_output:
                        logger.error(f"   Error output: {error_output[:500]}")
            except:
                pass
            return None

        logger.info(f"✅ Queue processor started (PID: {process.pid})")
        logger.info(f"   Logs: {stdout_file}")
        return process

    except Exception as e:
        logger.error(f"❌ Failed to start queue processor: {e}", exc_info=True)
        return None


def main():
    """Start complete Discord system."""
    print("\n" + "="*70)
    print("🚀 STARTING COMPLETE DISCORD SYSTEM")
    print("="*70 + "\n")

    # Check for existing instance
    existing_pid = check_existing_instance()
    if existing_pid:
        logger.error(f"❌ Discord system is already running (PID: {existing_pid})")
        logger.error("   Only one instance can run at a time.")
        logger.error("   To stop the existing instance:")
        logger.error("   - Press Ctrl+C in the terminal running it, or")
        logger.error(f"   - Kill the process: taskkill /F /PID {existing_pid}")
        return 1

    # Create lock file
    if not create_lock():
        logger.error("❌ Failed to create lock file - cannot ensure single instance")
        return 1

    # Check token
    if not check_token():
        cleanup_lock()
        print("\n💡 To fix:")
        print("   1. Create .env file in project root")
        print("   2. Add: DISCORD_BOT_TOKEN=your_bot_token_here")
        print("   3. Run this script again\n")
        return 1

    # Start Discord bot
    bot_process = start_discord_bot()
    if not bot_process:
        cleanup_lock()
        return 1

    # Wait a bit for bot to initialize
    time.sleep(3)

    # Start queue processor
    queue_process = start_queue_processor()
    if not queue_process:
        logger.warning("⚠️  Queue processor failed to start - messages won't be delivered")

    print("\n" + "="*70)
    print("✅ DISCORD SYSTEM STARTED")
    print("="*70)
    print(f"Discord Bot PID: {bot_process.pid if bot_process else 'FAILED'}")
    print(f"Queue Processor PID: {queue_process.pid if queue_process else 'FAILED'}")
    print("\n💡 To stop:")
    print("   Press Ctrl+C or kill the processes")
    print("="*70 + "\n")

    # Keep processes running and monitor them
    try:
        while True:
            time.sleep(5)  # Check every 5 seconds

            # Check if bot is still running
            if bot_process and bot_process.poll() is not None:
                logger.error(f"❌ Discord bot crashed (exit code: {bot_process.returncode})")
                logger.error("   Check logs in logs/ directory")
                break

            # Check if queue processor is still running
            if queue_process and queue_process.poll() is not None:
                logger.error(f"❌ Queue processor crashed (exit code: {queue_process.returncode})")
                logger.error("   Check logs: logs/message_queue_errors.log")
                # Don't break here - queue processor can restart

    except KeyboardInterrupt:
        logger.info("🛑 Shutdown requested by user")

    # Cleanup
    logger.info("🧹 Cleaning up processes...")
    if bot_process and bot_process.poll() is None:
        bot_process.terminate()
        try:
            bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot_process.kill()

    if queue_process and queue_process.poll() is None:
        queue_process.terminate()
        try:
            queue_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            queue_process.kill()

    cleanup_lock()
    logger.info("✅ Discord system stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())