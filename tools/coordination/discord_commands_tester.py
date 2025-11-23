#!/usr/bin/env python3
"""
Discord Commands Tester
=======================

Tests all Discord bot commands and verifies error handling.
Creates comprehensive test report for debugging.

Usage:
    python tools/coordination/discord_commands_tester.py
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Try to import discord (may not be available)
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("⚠️  discord.py not available - running in analysis mode")

def find_discord_command_files() -> List[Path]:
    """Find all Discord command files."""
    command_files = []
    discord_dir = Path("src/discord_commander")
    
    if not discord_dir.exists():
        return command_files
    
    # Common command file patterns
    patterns = [
        "*_commands.py",
        "*_command.py",
        "unified_*.py",
        "discord_commander_bot.py"
    ]
    
    for pattern in patterns:
        command_files.extend(discord_dir.glob(pattern))
    
    return sorted(set(command_files))

def analyze_command_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a Discord command file for commands and error handling."""
    result = {
        "file": str(file_path),
        "commands": [],
        "error_handling": {},
        "has_error_handler": False,
        "total_commands": 0,
        "commands_with_handling": 0
    }
    
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Find all @commands.command decorators
        import re
        command_pattern = r'@commands\.command\([^)]*name=["\']([^"\']+)["\']'
        commands_found = re.findall(command_pattern, content)
        result["commands"] = commands_found
        result["total_commands"] = len(commands_found)
        
        # Check for error handling patterns
        for cmd in commands_found:
            # Look for try/except blocks in command functions
            cmd_func_pattern = rf'async def {cmd}\(.*?\):(.*?)(?=async def |@commands\.command|$)'
            cmd_match = re.search(cmd_func_pattern, content, re.DOTALL)
            
            if cmd_match:
                func_body = cmd_match.group(1)
                has_try_except = "try:" in func_body and "except" in func_body
                has_error_response = "await ctx.send" in func_body and ("error" in func_body.lower() or "❌" in func_body)
                
                result["error_handling"][cmd] = {
                    "has_try_except": has_try_except,
                    "has_error_response": has_error_response,
                    "complete": has_try_except and has_error_response
                }
                
                if has_try_except and has_error_response:
                    result["commands_with_handling"] += 1
        
        # Check for global error handler
        result["has_error_handler"] = "on_command_error" in content or "CommandError" in content
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def generate_test_report(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comprehensive test report."""
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total_files": len(analyses),
            "total_commands": sum(a.get("total_commands", 0) for a in analyses),
            "commands_with_handling": sum(a.get("commands_with_handling", 0) for a in analyses),
            "files_with_error_handler": sum(1 for a in analyses if a.get("has_error_handler", False))
        },
        "files": analyses,
        "recommendations": []
    }
    
    # Calculate coverage
    total_commands = report["summary"]["total_commands"]
    commands_with_handling = report["summary"]["commands_with_handling"]
    
    if total_commands > 0:
        coverage = (commands_with_handling / total_commands) * 100
        report["summary"]["error_handling_coverage"] = f"{coverage:.1f}%"
    else:
        report["summary"]["error_handling_coverage"] = "0%"
    
    # Generate recommendations
    if coverage < 100:
        report["recommendations"].append(
            f"⚠️  {total_commands - commands_with_handling} commands need error handling"
        )
    
    if report["summary"]["files_with_error_handler"] < len(analyses):
        report["recommendations"].append(
            "⚠️  Some files missing global error handlers"
        )
    
    # Find commands without error handling
    commands_needing_handling = []
    for analysis in analyses:
        for cmd, handling in analysis.get("error_handling", {}).items():
            if not handling.get("complete", False):
                commands_needing_handling.append({
                    "command": cmd,
                    "file": analysis["file"],
                    "issues": [
                        k for k, v in handling.items() 
                        if k != "complete" and not v
                    ]
                })
    
    if commands_needing_handling:
        report["commands_needing_handling"] = commands_needing_handling
    
    return report

def print_report(report: Dict[str, Any]):
    """Print formatted test report."""
    print("=" * 70)
    print("📊 DISCORD COMMANDS TEST REPORT")
    print("=" * 70)
    print()
    
    summary = report["summary"]
    print(f"📁 Files Analyzed: {summary['total_files']}")
    print(f"🔧 Total Commands: {summary['total_commands']}")
    print(f"✅ Commands with Error Handling: {summary['commands_with_handling']}")
    print(f"📈 Coverage: {summary['error_handling_coverage']}")
    print(f"🛡️  Files with Global Error Handler: {summary['files_with_error_handler']}")
    print()
    
    if report.get("commands_needing_handling"):
        print("⚠️  COMMANDS NEEDING ERROR HANDLING:")
        print("-" * 70)
        for cmd_info in report["commands_needing_handling"]:
            print(f"  • {cmd_info['command']}")
            print(f"    File: {cmd_info['file']}")
            print(f"    Issues: {', '.join(cmd_info['issues'])}")
            print()
    
    if report.get("recommendations"):
        print("💡 RECOMMENDATIONS:")
        print("-" * 70)
        for rec in report["recommendations"]:
            print(f"  {rec}")
        print()
    
    print("=" * 70)

def main():
    """Main test execution."""
    print("🔍 Analyzing Discord Command Files...")
    print()
    
    command_files = find_discord_command_files()
    
    if not command_files:
        print("❌ No Discord command files found!")
        print("   Expected location: src/discord_commander/")
        return 1
    
    print(f"📁 Found {len(command_files)} command file(s):")
    for f in command_files:
        print(f"   • {f}")
    print()
    
    # Analyze each file
    analyses = []
    for file_path in command_files:
        print(f"🔍 Analyzing {file_path.name}...")
        analysis = analyze_command_file(file_path)
        analyses.append(analysis)
    
    # Generate report
    report = generate_test_report(analyses)
    
    # Print report
    print()
    print_report(report)
    
    # Save report
    report_file = Path("data/discord_commands_test_report.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"💾 Report saved to: {report_file}")
    print()
    
    # Return exit code based on coverage
    coverage = float(report["summary"]["error_handling_coverage"].rstrip("%"))
    if coverage < 100:
        print("⚠️  Some commands need error handling!")
        return 1
    else:
        print("✅ All commands have error handling!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

