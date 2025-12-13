#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Restart Discord Bot - Direct Method
===================================

Stops any running Discord bot processes and restarts the bot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def find_bot_processes():
    """Find running Discord bot processes."""
    import psutil
    
    bot_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline:
                cmdline_str = ' '.join(cmdline)
                if 'unified_discord_bot' in cmdline_str or 'run_unified_discord_bot' in cmdline_str:
                    bot_processes.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return bot_processes

def stop_bot_processes():
    """Stop all Discord bot processes."""
    try:
        import psutil
        processes = find_bot_processes()
        
        if not processes:
            print("ℹ️  No Discord bot processes found")
            return True
        
        print(f"🛑 Stopping {len(processes)} bot process(es)...")
        for pid in processes:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                print(f"   Stopped PID {pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"   Could not stop PID {pid}: {e}")
        
        # Wait for processes to terminate
        time.sleep(2)
        
        # Force kill if still running
        for pid in processes:
            try:
                proc = psutil.Process(pid)
                if proc.is_running():
                    proc.kill()
                    print(f"   Force killed PID {pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return True
        
    except ImportError:
        print("⚠️  psutil not available - cannot find/stop processes")
        print("   Install with: pip install psutil")
        return False

def restart_bot():
    """Restart the Discord bot."""
    project_root = Path(__file__).parent.parent
    
    # Stop existing processes
    stop_bot_processes()
    
    # Wait a moment
    time.sleep(1)
    
    # Start bot
    bot_script = project_root / "tools" / "run_unified_discord_bot_with_restart.py"
    
    print(f"🚀 Starting Discord bot...")
    print(f"   Script: {bot_script}")
    
    # Start in background
    subprocess.Popen(
        [sys.executable, str(bot_script)],
        cwd=str(project_root),
        env=os.environ.copy()
    )
    
    print("✅ Bot restart initiated")
    print("   Check logs/discord_bot.log for status")

if __name__ == "__main__":
    restart_bot()

