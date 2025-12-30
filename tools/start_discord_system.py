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


