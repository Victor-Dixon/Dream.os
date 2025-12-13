#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Quick status check for Discord system.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import psutil
from pathlib import Path

lock_file = Path("logs/discord_system.lock")

if lock_file.exists():
    pid = int(lock_file.read_text().strip())
    try:
        proc = psutil.Process(pid)
        print(f"✅ Main process running (PID: {pid})")
        print(f"   Status: {proc.status()}")
        print(f"   Command: {' '.join(proc.cmdline()[:3])}...")
    except psutil.NoSuchProcess:
        print(f"❌ Lock file exists but process {pid} not found")
else:
    print("❌ Lock file not found - Discord system not running")

# Check for Discord bot and queue processor
discord_procs = []
queue_procs = []

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmdline_list = proc.info.get('cmdline') or []
        cmdline = ' '.join(cmdline_list).lower()
        if 'run_unified_discord_bot' in cmdline:
            discord_procs.append(proc.info['pid'])
        elif 'start_message_queue' in cmdline:
            queue_procs.append(proc.info['pid'])
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

print(f"\n📊 Process Status:")
print(f"   Discord Bot processes: {len(discord_procs)} {discord_procs}")
print(f"   Queue Processor processes: {len(queue_procs)} {queue_procs}")

