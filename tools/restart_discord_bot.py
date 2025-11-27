#!/usr/bin/env python3
"""
Restart Discord Bot and Message Queue
=====================================

Stops Discord bot, checks message queue, then restarts both.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def find_discord_bot_processes():
    """Find processes running Discord bot."""
    import psutil
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline:
                cmdline_str = ' '.join(cmdline)
                if 'run_unified_discord_bot_with_restart.py' in cmdline_str or \
                   'unified_discord_bot.py' in cmdline_str or \
                   'start_discord_system.py' in cmdline_str:
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def stop_discord_bot():
    """Stop Discord bot processes."""
    print("🛑 Stopping Discord bot...")
    try:
        import psutil
        processes = find_discord_bot_processes()
        if not processes:
            print("   ℹ️  No Discord bot processes found")
            return True
        
        for proc in processes:
            try:
                print(f"   Stopping process {proc.pid}...")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    print(f"   ✅ Process {proc.pid} stopped")
                except psutil.TimeoutExpired:
                    print(f"   ⚠️  Process {proc.pid} didn't stop, forcing kill...")
                    proc.kill()
                    proc.wait()
                    print(f"   ✅ Process {proc.pid} killed")
            except Exception as e:
                print(f"   ❌ Error stopping process {proc.pid}: {e}")
        
        # Wait a moment for cleanup
        time.sleep(2)
        return True
    except ImportError:
        print("   ⚠️  psutil not available, trying alternative method...")
        # Try using taskkill on Windows
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/FI', 'WINDOWTITLE eq *discord*'], 
                         capture_output=True, timeout=10)
            return True
        except:
            print("   ❌ Could not stop processes automatically")
            print("   💡 Please stop Discord bot manually")
            return False

def check_message_queue():
    """Check message queue status."""
    print("\n📬 Checking message queue...")
    try:
        from src.core.message_queue import MessageQueue
        from src.core.message_queue_persistence import FileQueuePersistence
        
        queue_dir = Path("message_queue")
        if not queue_dir.exists():
            print("   ℹ️  Message queue directory does not exist")
            return
        
        queue_file = queue_dir / "queue.json"
        if not queue_file.exists():
            print("   ℹ️  No queue file found (queue is empty)")
            return
        
        # Load queue
        persistence = FileQueuePersistence(queue_file)
        entries = persistence.load_entries()
        
        if not entries:
            print("   ✅ Queue is empty")
        else:
            print(f"   ⚠️  Queue has {len(entries)} pending messages")
            for i, entry in enumerate(entries[:5], 1):
                status = entry.status
                queue_id = entry.queue_id[:8] if hasattr(entry, 'queue_id') else 'unknown'
                print(f"      {i}. Status: {status}, ID: {queue_id}")
            if len(entries) > 5:
                print(f"      ... and {len(entries) - 5} more")
    except Exception as e:
        print(f"   ⚠️  Error checking queue: {e}")

def restart_discord_bot():
    """Restart Discord bot."""
    print("\n🚀 Restarting Discord bot...")
    try:
        # Use start_discord_system.py to restart
        script_path = project_root / "tools" / "start_discord_system.py"
        if not script_path.exists():
            print("   ❌ start_discord_system.py not found")
            return False
        
        print("   Starting Discord system...")
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment
        time.sleep(3)
        
        if process.poll() is None:
            print("   ✅ Discord bot restart initiated")
            print(f"   PID: {process.pid}")
            return True
        else:
            print(f"   ❌ Discord bot exited immediately (code: {process.returncode})")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"   Error: {stderr[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Error restarting: {e}")
        return False

def main():
    """Main function."""
    print("="*70)
    print("🔄 DISCORD BOT RESTART")
    print("="*70)
    
    # Step 1: Stop bot
    if not stop_discord_bot():
        print("\n⚠️  Could not stop bot automatically")
        return 1
    
    # Step 2: Check queue
    check_message_queue()
    
    # Step 3: Restart bot
    if not restart_discord_bot():
        print("\n❌ Failed to restart Discord bot")
        return 1
    
    print("\n" + "="*70)
    print("✅ RESTART COMPLETE")
    print("="*70)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

