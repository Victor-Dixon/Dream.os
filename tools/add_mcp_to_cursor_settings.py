#!/usr/bin/env python3
"""
Add MCP Server Configuration to Cursor Settings
Automatically adds MCP servers to Cursor User Settings
"""

import json
import platform
import os
from pathlib import Path

def get_cursor_settings_path():
    """Get Cursor settings.json path"""
    system = platform.system()
    
    if system == "Windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            return Path(appdata) / "Cursor" / "User" / "settings.json"
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
    else:  # Linux
        return Path.home() / ".config" / "Cursor" / "User" / "settings.json"
    
    return None

def load_mcp_config():
    """Load MCP server configuration"""
    config_path = Path(__file__).parent.parent / "mcp_servers" / "all_mcp_servers.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return None

def add_mcp_to_settings(dry_run=False, force_yes=False):
    """Add MCP configuration to Cursor settings.json"""
    settings_path = get_cursor_settings_path()
    
    if not settings_path:
        print("❌ Could not determine Cursor settings.json path")
        return False
    
    if not settings_path.exists():
        print(f"⚠️  Cursor settings.json not found at: {settings_path}")
        print("   Creating new settings file...")
        settings = {}
    else:
        print(f"✅ Found Cursor settings at: {settings_path}")
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error reading settings.json: {e}")
            return False
    
    # Load MCP config
    mcp_config = load_mcp_config()
    if not mcp_config:
        print("❌ Could not load MCP server configuration")
        return False
    
    # Check if MCP servers already configured
    if "mcp.servers" in settings:
        print("⚠️  MCP servers already configured in settings.json")
        print("   Current configuration:")
        for name in settings["mcp.servers"].keys():
            print(f"      - {name}")
        
        if not force_yes:
            response = input("\n   Overwrite existing configuration? (y/N): ")
            if response.lower() != 'y':
                print("   Skipping update")
                return False
        else:
            print("\n   --yes flag provided, overwriting configuration")
    
    # Prepare MCP servers config (remove description field for Cursor)
    mcp_servers = {}
    for name, config in mcp_config.get("mcpServers", {}).items():
        mcp_servers[name] = {
            "command": config.get("command", "python"),
            "args": config.get("args", [])
        }
    
    # Add to settings
    settings["mcp.servers"] = mcp_servers
    
    if dry_run:
        print("\n📋 DRY RUN - Would add to settings.json:")
        print(json.dumps({"mcp.servers": mcp_servers}, indent=2))
        return True
    
    # Backup original settings
    backup_path = settings_path.with_suffix('.json.backup')
    try:
        import shutil
        shutil.copy2(settings_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
    
    # Write updated settings
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated Cursor settings.json")
        print(f"   Added {len(mcp_servers)} MCP servers")
        return True
    except Exception as e:
        print(f"❌ Error writing settings.json: {e}")
        return False

def main():
    print("🔧 Add MCP Servers to Cursor Settings")
    print("="*60)
    print()
    
    # Check for dry run and yes flags
    dry_run = "--dry-run" in os.sys.argv or "-n" in os.sys.argv
    force_yes = "--yes" in os.sys.argv or "-y" in os.sys.argv
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
    
    success = add_mcp_to_settings(dry_run=dry_run, force_yes=force_yes)
    
    print()
    print("="*60)
    if success:
        if not dry_run:
            print("✅ Configuration added successfully!")
            print()
            print("📋 NEXT STEPS:")
            print("   1. RESTART CURSOR COMPLETELY")
            print("      - Quit Cursor (File → Exit)")
            print("      - Restart Cursor")
            print("   2. Verify MCP servers started:")
            print("      - Check Cursor Developer Tools (Ctrl+Shift+I)")
            print("      - Run: python tools/test_mcp_server_connectivity.py")
        else:
            print("✅ Dry run completed - no changes made")
    else:
        print("❌ Configuration update failed")
        print()
        print("💡 Manual Setup:")
        print("   1. Open Cursor Settings: Ctrl+Shift+P → 'Preferences: Open User Settings (JSON)'")
        print("   2. Add the content from CURSOR_MCP_CONFIG.json")
        print("   3. Restart Cursor")

if __name__ == '__main__':
    main()


