#!/usr/bin/env python3
"""
Stop all running Discord bot processes
"""

import psutil
import os
import signal
import subprocess

print('🔍 CHECKING FOR RUNNING DISCORD BOT PROCESSES')
print('=' * 60)

# Find all Python processes that might be Discord bots
discord_processes = []
for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
    try:
        if proc.info['name'] and 'python' in proc.info['name'].lower():
            cmdline = proc.info['cmdline']
            if cmdline and any('discord' in str(arg).lower() or 'bot' in str(arg).lower() for arg in cmdline):
                discord_processes.append(proc)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        continue

if discord_processes:
    print(f'✅ Found {len(discord_processes)} Discord-related process(es):')
    for proc in discord_processes:
        try:
            cmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else 'Unknown'
            print(f'  🐍 PID {proc.pid}: {cmd}')
            print(f'     Status: {proc.info["status"]}')

            # Try to terminate gracefully first
            if proc.info['status'] != 'zombie':
                print('     💡 Attempting to stop process...')
                try:
                    proc.terminate()
                    # Wait a bit for graceful shutdown
                    proc.wait(timeout=3)
                    print('     ✅ Process stopped gracefully')
                except psutil.TimeoutExpired:
                    print('     ⚠️ Process didn\'t respond to terminate, force killing...')
                    proc.kill()
                    print('     ✅ Process force-killed')
                except Exception as e:
                    print(f'     ❌ Failed to stop process: {e}')
        except Exception as e:
            print(f'  ❌ Error with process {proc.pid}: {e}')
else:
    print('❌ No Discord bot processes currently running')

print()
print('🧹 CLEANUP COMPLETE - ALL DISCORD BOTS STOPPED')
print('=' * 60)