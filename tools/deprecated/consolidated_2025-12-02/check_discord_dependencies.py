#!/usr/bin/env python3
"""
Check Discord Dependencies
===========================

Quick check to see if discord.py is installed and if tests need it.

Author: Agent-8
Date: 2025-01-27
"""

import sys

def check_discord():
    """Check if discord.py is available."""
    print("🔍 Checking Discord dependencies...\n")
    
    # Check if discord.py is installed
    try:
        import discord
        print(f"✅ discord.py installed: {discord.__version__}")
        print(f"   Location: {discord.__file__}")
        return True
    except ImportError:
        print("❌ discord.py NOT installed")
        return False

def check_test_requirements():
    """Check what the test file actually needs."""
    print("\n📋 Analyzing test_discord_commands.py requirements...\n")
    
    test_file = "tools/test_discord_commands.py"
    try:
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Check for discord imports
        if "import discord" in content or "from discord" in content:
            print("⚠️  Test file imports discord.py")
            print("   Tests WILL fail without discord.py")
            return True
        else:
            print("✅ Test file does NOT import discord.py")
            print("   Tests should work without discord.py")
            
            # Check what it does import
            imports = []
            for line in content.split('\n'):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    imports.append(line.strip())
            
            print(f"\n   Imports found: {len(imports)}")
            for imp in imports[:10]:
                print(f"   - {imp}")
            
            return False
    except Exception as e:
        print(f"❌ Error reading test file: {e}")
        return None

def main():
    """Main entry point."""
    has_discord = check_discord()
    needs_discord = check_test_requirements()
    
    print("\n" + "="*60)
    print("RECOMMENDATION")
    print("="*60)
    
    if needs_discord and not has_discord:
        print("\n⚠️  Tests require discord.py but it's not installed")
        print("   Options:")
        print("   1. Install discord.py: pip install discord.py")
        print("   2. Modify tests to skip discord-dependent tests")
        print("   3. Delete tests if not needed")
    elif not needs_discord:
        print("\n✅ Tests don't require discord.py")
        print("   Tests should work fine as-is")
    else:
        print("\n✅ discord.py is installed and tests need it")
        print("   Everything should work!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


