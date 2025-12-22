#!/usr/bin/env python3
"""
Debug script for main.py
Checks for common issues and validates functionality.
"""

import sys
import os
from pathlib import Path

def check_imports():
    """Check if all required imports work."""
    print("=" * 70)
    print("CHECKING IMPORTS")
    print("=" * 70)
    
    issues = []
    
    # Check standard library imports
    try:
        from dotenv import load_dotenv
        print("✅ dotenv")
    except ImportError as e:
        issues.append(f"❌ dotenv: {e}")
        print(f"❌ dotenv: {e}")
    
    try:
        import argparse
        print("✅ argparse")
    except ImportError as e:
        issues.append(f"❌ argparse: {e}")
        print(f"❌ argparse: {e}")
    
    try:
        import subprocess
        print("✅ subprocess")
    except ImportError as e:
        issues.append(f"❌ subprocess: {e}")
        print(f"❌ subprocess: {e}")
    
    try:
        import psutil
        print("✅ psutil")
    except ImportError as e:
        issues.append(f"❌ psutil: {e}")
        print(f"❌ psutil: {e}")
    
    # Check agent_mode_manager import
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / "src"))
    try:
        from src.core.agent_mode_manager import get_mode_manager
        print("✅ agent_mode_manager")
        
        # Test getting mode manager
        try:
            mm = get_mode_manager()
            print(f"   Current mode: {mm.get_current_mode()}")
            print(f"   Active agents: {mm.get_active_agents()}")
        except Exception as e:
            issues.append(f"⚠️  agent_mode_manager.get_mode_manager(): {e}")
            print(f"⚠️  agent_mode_manager.get_mode_manager(): {e}")
    except ImportError as e:
        issues.append(f"❌ agent_mode_manager: {e}")
        print(f"❌ agent_mode_manager: {e}")
    
    print()
    return issues

def check_files():
    """Check if required files exist."""
    print("=" * 70)
    print("CHECKING REQUIRED FILES")
    print("=" * 70)
    
    project_root = Path(__file__).parent.parent
    issues = []
    
    files_to_check = [
        ("main.py", project_root / "main.py"),
        ("Message Queue Processor", project_root / "tools" / "start_message_queue_processor.py"),
        ("Twitch Bot", project_root / "tools" / "START_CHAT_BOT_NOW.py"),
        ("Discord Bot", project_root / "tools" / "start_discord_system.py"),
        ("agent_mode_config.json", project_root / "agent_mode_config.json"),
    ]
    
    for name, path in files_to_check:
        if path.exists():
            print(f"✅ {name}: {path}")
        else:
            issues.append(f"❌ {name}: {path} (NOT FOUND)")
            print(f"❌ {name}: {path} (NOT FOUND)")
    
    # Check pids directory
    pids_dir = project_root / "pids"
    if pids_dir.exists():
        print(f"✅ pids directory: {pids_dir}")
    else:
        print(f"ℹ️  pids directory will be created: {pids_dir}")
    
    print()
    return issues

def check_environment():
    """Check environment variables."""
    print("=" * 70)
    print("CHECKING ENVIRONMENT VARIABLES")
    print("=" * 70)
    
    issues = []
    
    env_vars = {
        "TWITCH_CHANNEL": "Twitch channel name",
        "TWITCH_ACCESS_TOKEN": "Twitch access token",
        "DISCORD_BOT_TOKEN": "Discord bot token",
    }
    
    for var, description in env_vars.items():
        value = os.getenv(var, "").strip()
        if value:
            # Mask sensitive values
            if "TOKEN" in var:
                masked = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                print(f"✅ {var}: {masked} ({description})")
            else:
                print(f"✅ {var}: {value} ({description})")
        else:
            issues.append(f"⚠️  {var}: NOT SET ({description})")
            print(f"⚠️  {var}: NOT SET ({description})")
    
    print()
    return issues

def check_syntax():
    """Check Python syntax."""
    print("=" * 70)
    print("CHECKING SYNTAX")
    print("=" * 70)
    
    project_root = Path(__file__).parent.parent
    main_py = project_root / "main.py"
    
    try:
        compile(main_py.read_text(), str(main_py), 'exec')
        print("✅ main.py syntax is valid")
        print()
        return []
    except SyntaxError as e:
        print(f"❌ Syntax error in main.py:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   {e.msg}")
        print()
        return [f"Syntax error: {e}"]

def main():
    """Main debug function."""
    print("\n" + "=" * 70)
    print("DEBUG MAIN.PY")
    print("=" * 70)
    print()
    
    all_issues = []
    
    # Check syntax
    all_issues.extend(check_syntax())
    
    # Check imports
    all_issues.extend(check_imports())
    
    # Check files
    all_issues.extend(check_files())
    
    # Check environment
    all_issues.extend(check_environment())
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if all_issues:
        print(f"⚠️  Found {len(all_issues)} issue(s):")
        for issue in all_issues:
            print(f"   {issue}")
    else:
        print("✅ No issues found - main.py appears to be working correctly!")
    
    print()
    return 0 if not all_issues else 1

if __name__ == "__main__":
    sys.exit(main())

