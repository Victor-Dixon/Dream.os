#!/usr/bin/env python3
"""
Setup Cursor MCP Configuration
Helps configure MCP servers for Cursor IDE

<!-- SSOT Domain: tools -->
"""

import json
import os
import platform
from pathlib import Path

def get_cursor_config_paths():
    """Get possible Cursor configuration file paths"""
    system = platform.system()
    paths = []
    
    if system == "Windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            paths.extend([
                Path(appdata) / "Cursor" / "User" / "settings.json",
                Path(appdata) / "Cursor" / "User" / "globalStorage" / "mcp.json",
            ])
    elif system == "Darwin":  # macOS
        home = Path.home()
        paths.extend([
            home / "Library" / "Application Support" / "Cursor" / "User" / "settings.json",
            home / ".cursor" / "mcp.json",
        ])
    else:  # Linux
        home = Path.home()
        paths.extend([
            home / ".config" / "Cursor" / "User" / "settings.json",
            home / ".cursor" / "mcp.json",
        ])
    
    return paths

def load_mcp_config():
    """Load MCP server configuration"""
    config_path = Path(__file__).parent.parent / "mcp_servers" / "all_mcp_servers.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def create_cursor_mcp_config():
    """Create Cursor MCP configuration"""
    mcp_config = load_mcp_config()
    
    if not mcp_config:
        print("❌ Could not load MCP server configuration")
        return None
    
    # Format for Cursor (may need adjustment based on Cursor's actual format)
    cursor_config = {
        "mcpServers": mcp_config.get("mcpServers", {})
    }
    
    return cursor_config

def main():
    print("🔧 Cursor MCP Server Setup")
    print("="*60)
    print()
    
    # Load MCP config
    mcp_config = load_mcp_config()
    if not mcp_config:
        print("❌ Could not load mcp_servers/all_mcp_servers.json")
        return
    
    servers = mcp_config.get("mcpServers", {})
    print(f"✅ Loaded {len(servers)} MCP server configurations")
    print()
    
    # Show configuration
    print("📋 MCP Server Configuration:")
    for name, config in servers.items():
        print(f"   {name}:")
        print(f"      Command: {config.get('command', 'N/A')}")
        print(f"      Args: {config.get('args', [])}")
        print()
    
    # Check Cursor config paths
    print("🔍 Checking Cursor Configuration Locations:")
    config_paths = get_cursor_config_paths()
    
    found_configs = []
    for path in config_paths:
        if path.exists():
            print(f"   ✅ Found: {path}")
            found_configs.append(path)
        else:
            print(f"   ⚠️  Not found: {path}")
    
    print()
    print("="*60)
    print("📝 SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("To enable MCP servers in Cursor:")
    print()
    print("1. Open Cursor Settings:")
    print("   - Press Ctrl+Shift+P (Cmd+Shift+P on Mac)")
    print("   - Type 'Preferences: Open User Settings (JSON)'")
    print("   - Press Enter")
    print()
    print("2. Add MCP Configuration:")
    print("   Add this to your settings.json:")
    print()
    print("   {")
    print('     "mcp.servers": {')
    
    for name, config in servers.items():
        args_str = json.dumps(config.get("args", []))
        print(f'       "{name}": {{')
        print(f'         "command": "{config.get("command", "python")}",')
        print(f'         "args": {args_str}')
        print('       },')
    
    print("     }")
    print("   }")
    print()
    print("3. Alternative: Create workspace .cursor/mcp.json")
    print("   (Note: May be blocked by .gitignore)")
    print()
    print("4. RESTART CURSOR COMPLETELY")
    print("   - Quit Cursor (not just close window)")
    print("   - Restart Cursor")
    print("   - MCP servers should auto-start")
    print()
    print("5. Verify Connection:")
    print("   - Run: python tools/test_mcp_server_connectivity.py")
    print("   - Check Cursor Developer Tools (Ctrl+Shift+I)")
    print("   - Look for MCP server startup messages")
    print()
    
    # Generate config file content
    cursor_config = create_cursor_mcp_config()
    if cursor_config:
        config_file = Path(__file__).parent.parent / "CURSOR_MCP_CONFIG.json"
        with open(config_file, 'w') as f:
            json.dump(cursor_config, f, indent=2)
        print(f"✅ Generated configuration file: {config_file}")
        print("   Copy this content to your Cursor settings.json")
        print()

if __name__ == '__main__':
    main()




