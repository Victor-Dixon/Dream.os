#!/usr/bin/env python3
"""
Discord Bot Debug Tool
======================

Diagnoses and fixes common Discord bot startup issues.

Author: Agent-7 (Web Development Specialist)
"""

import sys
import os
from pathlib import Path

def check_imports():
    """Check if all required modules can be imported."""
    print("=" * 60)
    print("🔍 Checking Imports")
    print("=" * 60)
    print()
    
    issues = []
    
    # Check Python path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"✅ Added project root to path: {project_root}")
    else:
        print(f"✅ Project root in path: {project_root}")
    print()
    
    # Check discord.py
    try:
        import discord
        from discord.ext import commands
        print(f"✅ discord.py: {discord.__version__}")
    except ImportError as e:
        print(f"❌ discord.py not installed: {e}")
        issues.append("Install discord.py: pip install discord.py")
    print()
    
    # Check dotenv
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv installed")
    except ImportError:
        print("⚠️  python-dotenv not installed (optional)")
        print("   Install with: pip install python-dotenv")
    print()
    
    # Check src imports
    try:
        from src.services.messaging_infrastructure import ConsolidatedMessagingService
        print("✅ ConsolidatedMessagingService imports successfully")
    except ImportError as e:
        print(f"❌ ConsolidatedMessagingService import failed: {e}")
        issues.append(f"Import error: {e}")
    print()
    
    try:
        from src.discord_commander.discord_gui_controller import DiscordGUIController
        print("✅ DiscordGUIController imports successfully")
    except ImportError as e:
        print(f"❌ DiscordGUIController import failed: {e}")
        issues.append(f"Import error: {e}")
    print()
    
    return issues

def check_environment():
    """Check environment variables."""
    print("=" * 60)
    print("🔍 Checking Environment Variables")
    print("=" * 60)
    print()
    
    issues = []
    
    # Load .env if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loaded")
    except:
        print("⚠️  Could not load .env file")
    print()
    
    # Check DISCORD_BOT_TOKEN
    token = os.getenv("DISCORD_BOT_TOKEN")
    if token:
        print(f"✅ DISCORD_BOT_TOKEN: {'*' * min(len(token), 20)}... (set)")
    else:
        print("❌ DISCORD_BOT_TOKEN not set")
        issues.append("Set DISCORD_BOT_TOKEN in .env file or environment")
    print()
    
    # Check DISCORD_CHANNEL_ID (optional)
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    if channel_id:
        print(f"✅ DISCORD_CHANNEL_ID: {channel_id}")
    else:
        print("ℹ️  DISCORD_CHANNEL_ID not set (optional)")
    print()
    
    return issues

def check_bot_file():
    """Check bot file syntax and structure."""
    print("=" * 60)
    print("🔍 Checking Bot File")
    print("=" * 60)
    print()
    
    issues = []
    bot_file = Path(__file__).parent.parent / "src" / "discord_commander" / "unified_discord_bot.py"
    
    if not bot_file.exists():
        print(f"❌ Bot file not found: {bot_file}")
        issues.append(f"Bot file missing: {bot_file}")
        return issues
    
    print(f"✅ Bot file exists: {bot_file}")
    
    # Check syntax
    try:
        with open(bot_file) as f:
            compile(f.read(), str(bot_file), 'exec')
        print("✅ Bot file syntax is valid")
    except SyntaxError as e:
        print(f"❌ Syntax error in bot file: {e}")
        issues.append(f"Syntax error: {e}")
    except Exception as e:
        print(f"⚠️  Error checking syntax: {e}")
    print()
    
    # Check import order
    content = bot_file.read_text()
    if "from src.services" in content and "sys.path.insert" in content:
        # Check if path is set before imports
        path_line = None
        import_line = None
        for i, line in enumerate(content.split('\n'), 1):
            if "sys.path.insert" in line and path_line is None:
                path_line = i
            if "from src.services" in line and import_line is None:
                import_line = i
        
        if path_line and import_line:
            if import_line < path_line:
                print("⚠️  Import order issue: src imports before path setup")
                print(f"   Imports at line {import_line}, path setup at line {path_line}")
                issues.append("Fix import order: Set sys.path before src imports")
            else:
                print("✅ Import order is correct (path set before imports)")
    print()
    
    return issues

def main():
    """Main debug function."""
    print("=" * 60)
    print("🐛 Discord Bot Debug Tool")
    print("=" * 60)
    print()
    
    all_issues = []
    
    # Run checks
    all_issues.extend(check_imports())
    all_issues.extend(check_environment())
    all_issues.extend(check_bot_file())
    
    # Summary
    print("=" * 60)
    print("📊 Debug Summary")
    print("=" * 60)
    print()
    
    if not all_issues:
        print("✅ All checks passed! Bot should start successfully.")
        print()
        print("🚀 Try starting the bot:")
        print("   python tools/run_unified_discord_bot_with_restart.py")
        return 0
    else:
        print(f"⚠️  Found {len(all_issues)} issue(s):")
        print()
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
        print()
        print("💡 Fix the issues above and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


