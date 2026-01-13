#!/usr/bin/env python3
"""
Check Cursor MCP Configuration
=============================

Diagnoses MCP server connectivity issues by comparing Cursor's MCP config
with the project's expected configuration.
"""

import json
import os
import sys

def check_cursor_mcp_config():
    """Check if Cursor MCP configuration matches project expectations."""

    print("🔍 Cursor MCP Configuration Diagnostic")
    print("=" * 50)

    # Check Cursor config
    cursor_config_path = os.path.expanduser('~/.cursor/mcp.json')
    print(f"Checking Cursor config at: {cursor_config_path}")

    if not os.path.exists(cursor_config_path):
        print("❌ CURSOR MCP CONFIG MISSING")
        print("This is the root cause of 'No server info found' errors!")
        print("\n💡 SOLUTION:")
        print("1. Open Cursor Settings")
        print("2. Go to MCP Servers section")
        print("3. Copy configuration from CURSOR_MCP_CONFIG.json")
        print("4. Paste into Cursor MCP settings")
        print("5. Restart Cursor completely")
        return False

    # Read Cursor config
    try:
        with open(cursor_config_path, 'r') as f:
            cursor_config = json.load(f)
    except Exception as e:
        print(f"❌ Error reading Cursor config: {e}")
        return False

    cursor_servers = set(cursor_config.get('mcpServers', {}).keys())
    print(f"✅ Found {len(cursor_servers)} servers in Cursor config")

    # Read our expected config
    our_config_path = 'CURSOR_MCP_CONFIG.json'
    if not os.path.exists(our_config_path):
        print(f"❌ Project config missing: {our_config_path}")
        return False

    try:
        with open(our_config_path, 'r') as f:
            our_config = json.load(f)
    except Exception as e:
        print(f"❌ Error reading project config: {e}")
        return False

    our_servers = set(our_config.get('mcpServers', {}).keys())
    print(f"✅ Found {len(our_servers)} servers in project config")

    # Compare configs
    if our_servers == cursor_servers:
        print("✅ CONFIGURATION MATCH - Servers should be available")
        print("\nIf still getting 'No server info found' errors:")
        print("1. Restart Cursor completely")
        print("2. Check Cursor logs for MCP connection errors")
        print("3. Verify Python is available in PATH")
        return True
    else:
        print("⚠️ CONFIGURATION MISMATCH")
        missing = our_servers - cursor_servers
        extra = cursor_servers - our_servers

        if missing:
            print(f"❌ Missing in Cursor: {sorted(list(missing))}")
        if extra:
            print(f"⚠️ Extra in Cursor: {sorted(list(extra))}")

        print("\n💡 SOLUTION:")
        print("1. Update Cursor MCP settings to match CURSOR_MCP_CONFIG.json")
        print("2. Restart Cursor completely")
        return False

if __name__ == '__main__':
    success = check_cursor_mcp_config()
    sys.exit(0 if success else 1)

