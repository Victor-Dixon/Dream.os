<<<<<<< HEAD
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
=======
#!/usr/bin/env python3
"""
Start Discord System (Bot + optional queue processor)
=====================================================

Purpose: Start the Discord bot reliably (detached) so it doesn't die when a terminal closes.
Description: Validates DISCORD_BOT_TOKEN (from env or repo-root `.env`), starts the bot runner,
             writes `pids/discord.pid`, and tails log locations.

Usage:
  - python tools/start_discord_system.py
  - python tools/start_discord_system.py --restart
  - python tools/start_discord_system.py --status
  - python tools/start_discord_system.py --with-queue

Author: Agent-8 (stability patch)
Date: 2025-12-28
Tags: discord, bot, supervisor, ssot, tooling

<!-- SSOT Domain: tools -->
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_env(repo_root: Path) -> None:
    # Best-effort: load repo-root .env if python-dotenv is installed
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    load_dotenv(dotenv_path=repo_root / ".env")


def _taskkill(pid: int) -> None:
    # Use taskkill for Windows; no-op if it fails
    try:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def _read_pid(pid_file: Path) -> int | None:
    try:
        raw = pid_file.read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except Exception:
        return None


def _write_pid(pid_file: Path, pid: int) -> None:
    pid_file.parent.mkdir(parents=True, exist_ok=True)
    pid_file.write_text(f"{pid}\n", encoding="utf-8")


def _start_detached(cmd: list[str], cwd: Path, stdout_path: Path) -> int:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    # Append mode to keep history across restarts
    stdout_f = open(stdout_path, "a", encoding="utf-8")
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS  # type: ignore[attr-defined]
    p = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=stdout_f,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
    )
    return int(p.pid)


def _iter_pids_by_cmd_substrings(substrings: Iterable[str]) -> list[int]:
    """
    Best-effort: find Windows process ids whose CommandLine contains any of the provided substrings.
    Returns [] on failure or on non-Windows platforms.
    """
    if os.name != "nt":
        return []
    try:
        import subprocess as _sp

        # Use PowerShell to query Win32_Process (works without extra deps)
        joined = ",".join([f"'{s}'" for s in substrings])
        ps = (
            "$subs=@(" + joined + ");"
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.CommandLine -and ($subs | ForEach-Object { $_ }) -ne $null } | "
            "Where-Object { $cl=$_.CommandLine; ($subs | Where-Object { $cl -like ('*'+$_+'*') }).Count -gt 0 } | "
            "Select-Object -ExpandProperty ProcessId"
        )
        out = _sp.check_output(["powershell", "-NoProfile", "-Command", ps], text=True, stderr=_sp.DEVNULL)
        pids: list[int] = []
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                pids.append(int(line))
            except ValueError:
                continue
        return sorted(set(pids))
    except Exception:
        return []


def _kill_by_cmd_substrings(substrings: Iterable[str]) -> None:
    for pid in _iter_pids_by_cmd_substrings(substrings):
        _taskkill(pid)


def main() -> int:
    repo_root = _repo_root()
    _load_env(repo_root)

    parser = argparse.ArgumentParser(description="Start the Discord system reliably.")
    parser.add_argument("--restart", action="store_true", help="Stop existing bot pid (if any) before starting")
    parser.add_argument("--status", action="store_true", help="Print current pid + exit")
    parser.add_argument("--with-queue", action="store_true", help="Also start scripts/start_queue_processor.py")
    args = parser.parse_args()

    pid_dir = repo_root / "pids"
    discord_pid_file = pid_dir / "discord.pid"
    # Align naming with main.py (ServiceManager uses message_queue.pid)
    message_queue_pid_file = pid_dir / "message_queue.pid"

    existing_pid = _read_pid(discord_pid_file)
    if args.status:
        print(f"repo_root={repo_root}")
        print(f"discord.pid={existing_pid}")
        return 0

    if args.restart and existing_pid:
        print(f"Stopping existing Discord bot pid={existing_pid} ...")
        _taskkill(existing_pid)
    if args.restart:
        # Also clean up orphaned bot runners even if pid file is missing/stale
        _kill_by_cmd_substrings(["src.discord_commander.bot_runner", "discord_commander.bot_runner"])

    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN is not set.")
        print("Fix:")
        print("  1) Copy `env.example` -> `.env` and set DISCORD_BOT_TOKEN=... (repo root)")
        print("  2) OR set it for this shell:")
        print("     $env:DISCORD_BOT_TOKEN = '...token...'")
        return 2

    logs_dir = repo_root / "runtime" / "logs"
    bot_stdout = logs_dir / "discord_bot_runner_stdout.log"

    print("🤖 Starting Discord bot runner (detached)...")
    bot_pid = _start_detached(
        [sys.executable, "-m", "src.discord_commander.bot_runner"],
        cwd=repo_root,
        stdout_path=bot_stdout,
    )
    _write_pid(discord_pid_file, bot_pid)
    print(f"✅ Discord bot started (PID: {bot_pid})")
    print(f"   stdout/stderr -> {bot_stdout}")
    print(f"   logs (bot_runner) -> {repo_root / 'runtime' / 'logs' / ('discord_bot_' )}YYYYMMDD.log")

    if args.with_queue:
        queue_stdout = logs_dir / "message_queue_processor_stdout.log"
        print("📬 Starting message queue processor (detached)...")
        if args.restart:
            # Kill orphaned/duplicate queue processors (common failure mode: multiple instances)
            _kill_by_cmd_substrings(["scripts/start_queue_processor.py", "start_queue_processor.py", "message_queue_processor"])
        queue_pid = _start_detached(
            [sys.executable, str(repo_root / "scripts" / "start_queue_processor.py")],
            cwd=repo_root,
            stdout_path=queue_stdout,
        )
        _write_pid(message_queue_pid_file, queue_pid)
        print(f"✅ Queue processor started (PID: {queue_pid})")
        print(f"   stdout/stderr -> {queue_stdout}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
