#!/usr/bin/env python3
"""
Test Discord Prefix Mapping
===========================

Tests the Discord bot's developer prefix mapping functionality.

Usage:
    python tools/test_discord_prefix_mapping.py

Author: Agent-7 (Web Development Specialist)
Date: 2025-01-27
"""

import json
import sys
from pathlib import Path

def test_prefix_mapping():
    """Test Discord prefix mapping functionality."""
    print("🧪 Testing Discord Prefix Mapping")
    print("=" * 60)
    
    # Test 1: Check config file exists
    print("\n1️⃣ Checking config file...")
    config_file = Path("config/discord_user_map.json")
    example_file = Path("config/discord_user_map.json.example")
    
    if config_file.exists():
        print(f"   ✅ Config file exists: {config_file}")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"   ✅ Config file is valid JSON")
            print(f"   📊 Mappings found: {len([k for k in config.keys() if not k.startswith('_')])}")
        except Exception as e:
            print(f"   ❌ Config file invalid: {e}")
    else:
        print(f"   ⚠️  Config file not found: {config_file}")
        if example_file.exists():
            print(f"   💡 Copy {example_file} to {config_file} and add your Discord user IDs")
        else:
            print(f"   ❌ Example file not found: {example_file}")
    
    # Test 2: Check agent profiles
    print("\n2️⃣ Checking agent profiles...")
    workspace_dir = Path("agent_workspaces")
    if not workspace_dir.exists():
        print(f"   ❌ Workspace directory not found: {workspace_dir}")
    else:
        profiles_with_discord = []
        for agent_dir in workspace_dir.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                profile_file = agent_dir / "profile.json"
                if profile_file.exists():
                    try:
                        with open(profile_file, 'r', encoding='utf-8') as f:
                            profile = json.load(f)
                        if profile.get("discord_user_id"):
                            profiles_with_discord.append({
                                "agent": agent_dir.name,
                                "user_id": profile.get("discord_user_id"),
                                "username": profile.get("discord_username", "N/A")
                            })
                    except Exception as e:
                        print(f"   ⚠️  Failed to read {profile_file}: {e}")
        
        print(f"   📊 Profiles with Discord mapping: {len(profiles_with_discord)}")
        for profile in profiles_with_discord:
            print(f"      ✅ {profile['agent']}: {profile['user_id']} → {profile['username']}")
    
    # Test 3: Check bot code
    print("\n3️⃣ Checking bot implementation...")
    bot_file = Path("src/discord_commander/unified_discord_bot.py")
    if bot_file.exists():
        content = bot_file.read_text(encoding='utf-8')
        if "_get_developer_prefix" in content:
            print(f"   ✅ Prefix mapping method found")
        else:
            print(f"   ❌ Prefix mapping method not found")
        
        if "_load_discord_user_map" in content:
            print(f"   ✅ User map loader found")
        else:
            print(f"   ❌ User map loader not found")
        
        valid_prefixes = ['CHRIS', 'ARIA', 'VICTOR', 'CARYMN', 'CHARLES']
        for prefix in valid_prefixes:
            if f"[{prefix}]" in content:
                print(f"   ✅ {prefix} prefix supported")
    else:
        print(f"   ❌ Bot file not found: {bot_file}")
    
    # Test 4: Message format validation
    print("\n4️⃣ Testing message format validation...")
    test_formats = [
        ("[VICTOR] Agent-1\n\nTest", True, "Explicit prefix"),
        ("Agent-1\n\nTest", True, "Simple format"),
        ("[D2A] Agent-1\n\nTest", True, "Default prefix"),
        ("[INVALID] Agent-1\n\nTest", False, "Invalid prefix"),
        ("No agent", False, "Missing agent"),
    ]
    
    for msg, should_pass, desc in test_formats:
        lines = msg.split('\n', 1)
        has_valid_format = (
            len(lines) >= 2 and
            (lines[0].strip().startswith('Agent-') or 
             any(lines[0].strip().startswith(f"[{p}]") for p in ['D2A', 'CHRIS', 'ARIA', 'VICTOR', 'CARYMN', 'CHARLES']))
        )
        status = "✅" if (has_valid_format == should_pass) else "❌"
        print(f"   {status} {desc}: {msg[:30]}...")
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")
    print("\n💡 Next steps:")
    print("   1. Add your Discord user ID to config/discord_user_map.json")
    print("   2. Restart Discord bot: python tools/start_discord_system.py")
    print("   3. Send a test message in Discord")
    print("   4. Check agent inbox for delivered message")


if __name__ == "__main__":
    try:
        test_prefix_mapping()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

