#!/usr/bin/env python3
"""Debug status check to see why Discord shows as running when it's not."""

import psutil
from pathlib import Path

# Check PID file
pid_dir = Path("runtime/pids")
discord_pid_file = pid_dir / "discord.pid"

print("=== Discord Status Debug ===\n")

print("1. PID File Check:")
print(f"   PID dir exists: {pid_dir.exists()}")
print(f"   Discord PID file exists: {discord_pid_file.exists()}")

if discord_pid_file.exists():
    try:
        with open(discord_pid_file, 'r') as f:
            pid = int(f.read().strip())
        print(f"   PID from file: {pid}")
        print(f"   Process exists: {psutil.pid_exists(pid)}")
    except Exception as e:
        print(f"   Error reading PID file: {e}")
else:
    print("   No PID file found")

print("\n2. Python Processes with 'discord' in cmdline:")
discord_keywords = ['bot_runner', 'unified_discord_bot.py', 'discord_commander']
found = False

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if proc.info['name'] and 'python' in proc.info['name'].lower():
            if proc.info['cmdline']:
                cmdline_str = ' '.join(proc.info['cmdline'])
                for keyword in discord_keywords:
                    if keyword in cmdline_str:
                        found = True
                        print(f"   PID {proc.info['pid']}: {cmdline_str[:100]}")
                        break
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

if not found:
    print("   No matching processes found")

print("\n3. All Python processes (first 10):")
count = 0
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if proc.info['name'] and 'python' in proc.info['name'].lower():
            if proc.info['cmdline']:
                cmdline_str = ' '.join(proc.info['cmdline'])
                print(f"   PID {proc.info['pid']}: {cmdline_str[:80]}")
                count += 1
                if count >= 10:
                    break
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

