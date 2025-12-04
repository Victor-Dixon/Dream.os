#!/usr/bin/env python3
"""
Discord Bot Infrastructure Check - Agent-3
==========================================

<!-- SSOT Domain: infrastructure -->

Comprehensive infrastructure check for Discord bot restart support.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class DiscordBotInfrastructureChecker:
    """Comprehensive Discord bot infrastructure checker."""

    def __init__(self):
        """Initialize checker."""
        self.issues = []
        self.warnings = []
        self.info = []

    def check_python_processes(self) -> Dict[str, any]:
        """Check for running Python processes that might be Discord bot."""
        result = {
            "python_processes": [],
            "discord_processes": [],
            "total_python": 0,
        }

        if not HAS_PSUTIL:
            self.warnings.append("psutil not available - cannot check processes")
            return result

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        result["total_python"] += 1
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        
                        process_info = {
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cmdline": cmdline,
                            "start_time": time.ctime(proc.info['create_time']),
                        }

                        result["python_processes"].append(process_info)

                        # Check if it's Discord bot related
                        if any(keyword in cmdline.lower() for keyword in [
                            'discord', 'unified_discord_bot', 'start_discord', 'bot'
                        ]):
                            result["discord_processes"].append(process_info)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except Exception as e:
            self.warnings.append(f"Error checking processes: {e}")

        return result

    def check_queue_file(self) -> Dict[str, any]:
        """Check queue.json file status."""
        result = {
            "exists": False,
            "readable": False,
            "writable": False,
            "size": 0,
            "last_modified": None,
            "locked": False,
            "valid_json": False,
        }

        queue_file = Path("message_queue/queue.json")
        
        if not queue_file.exists():
            self.warnings.append("queue.json does not exist")
            return result

        result["exists"] = True
        result["size"] = queue_file.stat().st_size
        result["last_modified"] = time.ctime(queue_file.stat().st_mtime)

        # Check readability
        try:
            with open(queue_file, 'r', encoding='utf-8') as f:
                content = f.read()
                result["readable"] = True
                
                # Check if valid JSON
                try:
                    json.loads(content)
                    result["valid_json"] = True
                except json.JSONDecodeError:
                    self.issues.append("queue.json is not valid JSON")
        except PermissionError:
            self.issues.append("queue.json is not readable (permission denied)")
        except Exception as e:
            self.issues.append(f"Error reading queue.json: {e}")

        # Check writability
        try:
            with open(queue_file, 'a', encoding='utf-8') as f:
                result["writable"] = True
        except PermissionError:
            self.issues.append("queue.json is not writable (permission denied)")
        except Exception as e:
            self.warnings.append(f"queue.json may be locked: {e}")

        return result

    def check_lock_files(self) -> Dict[str, any]:
        """Check for Discord bot lock files."""
        result = {
            "lock_files": [],
            "stale_locks": [],
        }

        lock_paths = [
            Path("data/discord_system.lock"),
            Path("discord_system.lock"),
            Path(".discord_bot.lock"),
        ]

        for lock_path in lock_paths:
            if lock_path.exists():
                try:
                    lock_content = lock_path.read_text(encoding='utf-8').strip()
                    lock_info = {
                        "path": str(lock_path),
                        "content": lock_content,
                        "exists": True,
                    }

                    # Check if lock is stale (older than 5 minutes)
                    lock_age = time.time() - lock_path.stat().st_mtime
                    if lock_age > 300:  # 5 minutes
                        lock_info["stale"] = True
                        lock_info["age_seconds"] = lock_age
                        result["stale_locks"].append(lock_info)
                    else:
                        lock_info["stale"] = False
                        lock_info["age_seconds"] = lock_age

                    result["lock_files"].append(lock_info)

                except Exception as e:
                    self.warnings.append(f"Error reading lock file {lock_path}: {e}")

        return result

    def check_python_environment(self) -> Dict[str, any]:
        """Check Python environment and dependencies."""
        result = {
            "python_version": sys.version,
            "discord_available": False,
            "discord_version": None,
            "dotenv_available": False,
            "psutil_available": HAS_PSUTIL,
        }

        # Check discord.py
        try:
            import discord
            result["discord_available"] = True
            result["discord_version"] = getattr(discord, '__version__', 'unknown')
        except ImportError:
            self.issues.append("discord.py not installed - bot cannot run")

        # Check dotenv
        try:
            import dotenv
            result["dotenv_available"] = True
        except ImportError:
            self.warnings.append("python-dotenv not installed - .env loading may fail")

        return result

    def check_environment_variables(self) -> Dict[str, any]:
        """Check required environment variables."""
        result = {
            "discord_bot_token": bool(os.getenv("DISCORD_BOT_TOKEN")),
            "discord_channel_id": bool(os.getenv("DISCORD_CHANNEL_ID")),
            "missing_vars": [],
        }

        if not result["discord_bot_token"]:
            result["missing_vars"].append("DISCORD_BOT_TOKEN")
            self.issues.append("DISCORD_BOT_TOKEN not set in environment")

        return result

    def check_system_resources(self) -> Dict[str, any]:
        """Check system resources."""
        result = {
            "cpu_percent": None,
            "memory_percent": None,
            "disk_space": None,
        }

        if HAS_PSUTIL:
            try:
                result["cpu_percent"] = psutil.cpu_percent(interval=1)
                result["memory_percent"] = psutil.virtual_memory().percent
                
                # Check disk space
                disk = psutil.disk_usage('.')
                result["disk_space"] = {
                    "total_gb": disk.total / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "free_gb": disk.free / (1024**3),
                    "percent_used": (disk.used / disk.total) * 100,
                }

                # Warn if resources are high
                if result["cpu_percent"] > 80:
                    self.warnings.append(f"High CPU usage: {result['cpu_percent']:.1f}%")
                if result["memory_percent"] > 80:
                    self.warnings.append(f"High memory usage: {result['memory_percent']:.1f}%")
                if result["disk_space"]["percent_used"] > 90:
                    self.warnings.append(f"Low disk space: {result['disk_space']['percent_used']:.1f}% used")

            except Exception as e:
                self.warnings.append(f"Error checking system resources: {e}")

        return result

    def run_full_check(self) -> Dict[str, any]:
        """Run complete infrastructure check."""
        print("🔍 Running Discord Bot Infrastructure Check...")
        print()

        results = {
            "python_processes": self.check_python_processes(),
            "queue_file": self.check_queue_file(),
            "lock_files": self.check_lock_files(),
            "python_environment": self.check_python_environment(),
            "environment_variables": self.check_environment_variables(),
            "system_resources": self.check_system_resources(),
            "issues": self.issues,
            "warnings": self.warnings,
            "info": self.info,
        }

        return results

    def generate_report(self, results: Dict[str, any]) -> str:
        """Generate human-readable report."""
        report = []
        report.append("=" * 70)
        report.append("🔍 Discord Bot Infrastructure Check Report")
        report.append("=" * 70)
        report.append("")

        # Python Processes
        report.append("📊 Python Processes:")
        report.append("-" * 70)
        proc_info = results["python_processes"]
        report.append(f"Total Python processes: {proc_info['total_python']}")
        report.append(f"Discord-related processes: {len(proc_info['discord_processes'])}")
        
        if proc_info['discord_processes']:
            report.append("")
            report.append("Discord bot processes found:")
            for proc in proc_info['discord_processes']:
                report.append(f"  - PID {proc['pid']}: {proc['cmdline'][:80]}...")
        report.append("")

        # Queue File
        report.append("📁 Queue File Status:")
        report.append("-" * 70)
        queue = results["queue_file"]
        report.append(f"Exists: {queue['exists']}")
        if queue['exists']:
            report.append(f"Size: {queue['size']:,} bytes")
            report.append(f"Last Modified: {queue['last_modified']}")
            report.append(f"Readable: {queue['readable']}")
            report.append(f"Writable: {queue['writable']}")
            report.append(f"Valid JSON: {queue['valid_json']}")
        report.append("")

        # Lock Files
        report.append("🔒 Lock Files:")
        report.append("-" * 70)
        locks = results["lock_files"]
        if locks['lock_files']:
            for lock in locks['lock_files']:
                status = "⚠️ STALE" if lock.get('stale') else "✅ ACTIVE"
                report.append(f"{status} {lock['path']} (age: {lock.get('age_seconds', 0):.1f}s)")
        else:
            report.append("No lock files found")
        report.append("")

        # Python Environment
        report.append("🐍 Python Environment:")
        report.append("-" * 70)
        env = results["python_environment"]
        report.append(f"Python: {env['python_version'].split()[0]}")
        report.append(f"discord.py: {'✅' if env['discord_available'] else '❌'} {env['discord_version'] or 'NOT INSTALLED'}")
        report.append(f"psutil: {'✅' if env['psutil_available'] else '❌'}")
        report.append(f"dotenv: {'✅' if env['dotenv_available'] else '❌'}")
        report.append("")

        # Environment Variables
        report.append("🔐 Environment Variables:")
        report.append("-" * 70)
        env_vars = results["environment_variables"]
        report.append(f"DISCORD_BOT_TOKEN: {'✅ SET' if env_vars['discord_bot_token'] else '❌ NOT SET'}")
        report.append(f"DISCORD_CHANNEL_ID: {'✅ SET' if env_vars['discord_channel_id'] else '⚠️ OPTIONAL'}")
        report.append("")

        # System Resources
        report.append("💻 System Resources:")
        report.append("-" * 70)
        resources = results["system_resources"]
        if resources.get("cpu_percent") is not None:
            report.append(f"CPU Usage: {resources['cpu_percent']:.1f}%")
        if resources.get("memory_percent") is not None:
            report.append(f"Memory Usage: {resources['memory_percent']:.1f}%")
        if resources.get("disk_space"):
            disk = resources["disk_space"]
            report.append(f"Disk: {disk['used_gb']:.1f}GB / {disk['total_gb']:.1f}GB ({disk['percent_used']:.1f}% used)")
        report.append("")

        # Issues
        if results["issues"]:
            report.append("❌ ISSUES:")
            report.append("-" * 70)
            for issue in results["issues"]:
                report.append(f"  - {issue}")
            report.append("")

        # Warnings
        if results["warnings"]:
            report.append("⚠️ WARNINGS:")
            report.append("-" * 70)
            for warning in results["warnings"]:
                report.append(f"  - {warning}")
            report.append("")

        # Summary
        report.append("📋 SUMMARY:")
        report.append("-" * 70)
        if results["issues"]:
            report.append("❌ Issues found - bot may not start properly")
        elif results["warnings"]:
            report.append("⚠️ Warnings found - bot should work but check warnings")
        else:
            report.append("✅ Infrastructure looks good - ready for bot restart")
        report.append("")

        return "\n".join(report)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Discord Bot Infrastructure Check")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--save-report", action="store_true", help="Save report to file")

    args = parser.parse_args()

    checker = DiscordBotInfrastructureChecker()
    results = checker.run_full_check()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        report = checker.generate_report(results)
        print(report)

        if args.save_report:
            report_file = Path("agent_workspaces/Agent-3/discord_bot_infrastructure_check.txt")
            report_file.parent.mkdir(parents=True, exist_ok=True)
            report_file.write_text(report)
            print(f"✅ Report saved: {report_file}")

    # Return exit code based on issues
    return 1 if results["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())

