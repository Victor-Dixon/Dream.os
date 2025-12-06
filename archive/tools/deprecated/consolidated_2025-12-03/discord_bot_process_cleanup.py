#!/usr/bin/env python3
"""
Discord Bot Process Cleanup - Agent-3
=====================================

Safely kills stuck Discord bot processes for clean restart.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines
"""

import sys
import time
from pathlib import Path
from typing import List, Dict

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("❌ psutil not installed. Install with: pip install psutil")
    sys.exit(1)


def find_discord_processes() -> List[Dict]:
    """Find all Discord bot related processes."""
    discord_processes = []
    
    keywords = [
        'discord', 'unified_discord_bot', 'start_discord', 
        'run_unified_discord', 'discord_bot'
    ]
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            
            # Check if it's Discord bot related
            if any(keyword in cmdline.lower() for keyword in keywords):
                discord_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': cmdline,
                    'start_time': time.ctime(proc.info['create_time']),
                    'process': proc,
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return discord_processes


def kill_process(proc_info: Dict, force: bool = False) -> bool:
    """Kill a process safely."""
    try:
        proc = proc_info['process']
        pid = proc_info['pid']
        
        if force:
            proc.kill()
            print(f"  ✅ Force killed PID {pid}")
        else:
            proc.terminate()
            print(f"  ✅ Terminated PID {pid}")
            
            # Wait for graceful shutdown
            try:
                proc.wait(timeout=5)
                print(f"  ✅ Process {pid} exited gracefully")
            except psutil.TimeoutExpired:
                print(f"  ⚠️  Process {pid} didn't exit, force killing...")
                proc.kill()
                print(f"  ✅ Force killed PID {pid}")
        
        return True
    except psutil.NoSuchProcess:
        print(f"  ⚠️  Process {pid} already exited")
        return True
    except psutil.AccessDenied:
        print(f"  ❌ Access denied - cannot kill PID {pid}")
        return False
    except Exception as e:
        print(f"  ❌ Error killing PID {pid}: {e}")
        return False


def cleanup_lock_files():
    """Remove stale lock files."""
    lock_paths = [
        Path("data/discord_system.lock"),
        Path("logs/discord_system.lock"),
        Path("discord_system.lock"),
        Path(".discord_bot.lock"),
    ]
    
    cleaned = []
    for lock_path in lock_paths:
        if lock_path.exists():
            try:
                lock_path.unlink()
                cleaned.append(str(lock_path))
                print(f"  ✅ Removed lock file: {lock_path}")
            except Exception as e:
                print(f"  ⚠️  Could not remove {lock_path}: {e}")
    
    return cleaned


def main():
    """Main cleanup function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discord Bot Process Cleanup")
    parser.add_argument("--force", action="store_true", help="Force kill (no graceful shutdown)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be killed without killing")
    parser.add_argument("--cleanup-locks", action="store_true", help="Also cleanup lock files")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🧹 Discord Bot Process Cleanup")
    print("=" * 70)
    print()
    
    # Find Discord processes
    print("🔍 Searching for Discord bot processes...")
    processes = find_discord_processes()
    
    if not processes:
        print("✅ No Discord bot processes found")
        if args.cleanup_locks:
            print()
            print("🧹 Cleaning up lock files...")
            cleanup_lock_files()
        return 0
    
    print(f"Found {len(processes)} Discord bot process(es):")
    print()
    for proc in processes:
        print(f"  PID {proc['pid']}: {proc['cmdline'][:80]}...")
        print(f"    Started: {proc['start_time']}")
    print()
    
    if args.dry_run:
        print("🔍 DRY-RUN: Would kill these processes")
        print("   Run without --dry-run to actually kill them")
        return 0
    
    # Confirm
    response = input(f"Kill {len(processes)} process(es)? (y/N): ").strip().lower()
    if response != 'y':
        print("Aborted")
        return 1
    
    # Kill processes
    print()
    print("🛑 Killing processes...")
    killed = 0
    failed = 0
    
    for proc in processes:
        if kill_process(proc, force=args.force):
            killed += 1
        else:
            failed += 1
        time.sleep(0.5)  # Small delay between kills
    
    print()
    print(f"✅ Killed: {killed}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    
    # Cleanup lock files
    if args.cleanup_locks:
        print()
        print("🧹 Cleaning up lock files...")
        cleanup_lock_files()
    
    print()
    print("✅ Cleanup complete - ready for bot restart")
    return 0


if __name__ == "__main__":
    sys.exit(main())

