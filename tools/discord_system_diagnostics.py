#!/usr/bin/env python3
"""
Discord System Diagnostics
==========================

Comprehensive diagnostics for Discord bot and message delivery system.

Author: Agent-3 (Infrastructure & DevOps)
Date: 2025-01-27
Priority: CRITICAL
"""

import logging
import os
import sys
from pathlib import Path

# Load .env file FIRST
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_discord_bot_token():
    """Check if Discord bot token is set."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        return {
            "status": "❌ NOT SET",
            "issue": "DISCORD_BOT_TOKEN environment variable not set",
            "fix": "Set DISCORD_BOT_TOKEN in .env file or environment"
        }
    elif len(token) < 50:
        return {
            "status": "⚠️ INVALID",
            "issue": f"Token appears invalid (length: {len(token)}, expected >50)",
            "fix": "Verify token is correct in Discord Developer Portal"
        }
    else:
        return {
            "status": "✅ SET",
            "issue": None,
            "fix": None
        }


def check_discord_library():
    """Check if discord.py is installed."""
    try:
        import discord
        return {
            "status": "✅ INSTALLED",
            "version": discord.__version__,
            "issue": None
        }
    except ImportError:
        return {
            "status": "❌ NOT INSTALLED",
            "version": None,
            "issue": "discord.py library not found",
            "fix": "Install with: pip install discord.py"
        }


def check_queue_processor():
    """Check if queue processor is running."""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('queue_processor' in str(arg).lower() or 'start_message_queue' in str(arg).lower() for arg in cmdline):
                    return {
                        "status": "✅ RUNNING",
                        "pid": proc.info['pid'],
                        "issue": None
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return {
            "status": "❌ NOT RUNNING",
            "issue": "Queue processor not running - messages won't be delivered",
            "fix": "Start with: python tools/start_message_queue_processor.py"
        }
    except ImportError:
        # Fallback to process count check
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "Get-Process python | Measure-Object | Select-Object -ExpandProperty Count"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                count = int(result.stdout.strip())
                if count >= 2:  # At least bot + processor
                    return {
                        "status": "⚠️ POSSIBLY RUNNING",
                        "issue": "Cannot verify - install psutil for accurate detection",
                        "fix": "pip install psutil or manually verify"
                    }
        except:
            pass
        return {
            "status": "❌ NOT RUNNING",
            "issue": "Queue processor not running - messages won't be delivered",
            "fix": "Start with: python tools/start_message_queue_processor.py"
        }
    except Exception as e:
        return {
            "status": "⚠️ UNKNOWN",
            "issue": f"Could not check: {e}",
            "fix": "Manually verify queue processor is running"
        }


def check_message_queue():
    """Check message queue status."""
    queue_file = Path("message_queue/queue.json")
    if not queue_file.exists():
        return {
            "status": "⚠️ NO QUEUE FILE",
            "pending": 0,
            "total": 0,
            "issue": "Queue file doesn't exist (may be normal if no messages sent)"
        }
    
    try:
        import json
        data = json.loads(queue_file.read_text())
        
        # Handle both dict and list formats
        if isinstance(data, list):
            entries = data
        elif isinstance(data, dict):
            entries = data.get("entries", [])
        else:
            entries = []
        
        pending = [e for e in entries if isinstance(e, dict) and e.get("status") == "PENDING"]
        
        return {
            "status": "✅ EXISTS",
            "pending": len(pending),
            "total": len(entries),
            "issue": f"{len(pending)} messages pending delivery" if pending else None
        }
    except Exception as e:
        return {
            "status": "❌ ERROR",
            "pending": 0,
            "total": 0,
            "issue": f"Could not read queue: {e}"
        }


def check_discord_bot_process():
    """Check if Discord bot process is running."""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('discord' in str(arg).lower() or 'start_discord' in str(arg).lower() for arg in cmdline):
                    return {
                        "status": "✅ RUNNING",
                        "pid": proc.info['pid'],
                        "issue": None
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return {
            "status": "❌ NOT RUNNING",
            "issue": "Discord bot process not running",
            "fix": "Start with: python scripts/start_discord_bot.py"
        }
    except ImportError:
        # Fallback to process count check
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "Get-Process python | Measure-Object | Select-Object -ExpandProperty Count"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                count = int(result.stdout.strip())
                if count >= 1:
                    return {
                        "status": "⚠️ POSSIBLY RUNNING",
                        "issue": "Cannot verify - install psutil for accurate detection",
                        "fix": "pip install psutil or manually verify"
                    }
        except:
            pass
        return {
            "status": "❌ NOT RUNNING",
            "issue": "Discord bot process not running",
            "fix": "Start with: python scripts/start_discord_bot.py"
        }
    except Exception as e:
        return {
            "status": "⚠️ UNKNOWN",
            "issue": f"Could not check: {e}",
            "fix": "Manually verify Discord bot is running"
        }


def run_diagnostics():
    """Run all diagnostics."""
    print("\n" + "="*70)
    print("🔍 DISCORD SYSTEM DIAGNOSTICS")
    print("="*70 + "\n")
    
    # Check Discord bot token
    token_check = check_discord_bot_token()
    print(f"📋 Discord Bot Token: {token_check['status']}")
    if token_check.get('issue'):
        print(f"   Issue: {token_check['issue']}")
        if token_check.get('fix'):
            print(f"   Fix: {token_check['fix']}")
    print()
    
    # Check Discord library
    lib_check = check_discord_library()
    print(f"📚 Discord.py Library: {lib_check['status']}")
    if lib_check.get('version'):
        print(f"   Version: {lib_check['version']}")
    if lib_check.get('issue'):
        print(f"   Issue: {lib_check['issue']}")
        if lib_check.get('fix'):
            print(f"   Fix: {lib_check['fix']}")
    print()
    
    # Check Discord bot process
    bot_check = check_discord_bot_process()
    print(f"🤖 Discord Bot Process: {bot_check['status']}")
    if bot_check.get('issue'):
        print(f"   Issue: {bot_check['issue']}")
        if bot_check.get('fix'):
            print(f"   Fix: {bot_check['fix']}")
    print()
    
    # Check queue processor
    queue_proc_check = check_queue_processor()
    print(f"📬 Queue Processor: {queue_proc_check['status']}")
    if queue_proc_check.get('issue'):
        print(f"   Issue: {queue_proc_check['issue']}")
        if queue_proc_check.get('fix'):
            print(f"   Fix: {queue_proc_check['fix']}")
    print()
    
    # Check message queue
    queue_check = check_message_queue()
    print(f"📦 Message Queue: {queue_check['status']}")
    if queue_check.get('pending') is not None:
        print(f"   Pending: {queue_check['pending']}")
        print(f"   Total: {queue_check['total']}")
    if queue_check.get('issue'):
        print(f"   Issue: {queue_check['issue']}")
    print()
    
    # Summary
    print("="*70)
    issues = [
        token_check.get('issue'),
        lib_check.get('issue'),
        bot_check.get('issue'),
        queue_proc_check.get('issue'),
        queue_check.get('issue') if queue_check.get('pending', 0) > 0 else None
    ]
    issues = [i for i in issues if i]
    
    if not issues:
        print("✅ ALL SYSTEMS OPERATIONAL")
    else:
        print(f"⚠️  {len(issues)} ISSUE(S) FOUND")
        print("\n💡 RECOMMENDED ACTIONS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_diagnostics()

