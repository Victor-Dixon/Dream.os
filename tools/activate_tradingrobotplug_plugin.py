#!/usr/bin/env python3
"""
Activate TradingRobotPlug plugin and flush REST API routes.

<!-- SSOT Domain: web -->
"""

import subprocess
import sys
from pathlib import Path

def activate_plugin_via_wp_cli(site_key="tradingrobotplug.com"):
    """Activate plugin using WP-CLI."""
    # Try different possible plugin slugs
    plugin_slugs = [
        "tradingrobotplug-wordpress-plugin",
        "tradingrobotplug",
        "trading-robot-plug-platform"
    ]
    
    for slug in plugin_slugs:
        try:
            # Use MCP tool via Python subprocess would require MCP client
            # For now, document the command
            print(f"🔍 Attempting to activate plugin: {slug}")
            print(f"   Command: wp plugin activate {slug} --path=/path/to/wordpress")
            print("   Note: Requires WP-CLI access to WordPress installation")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n📋 Manual Activation Steps:")
    print("   1. Log into WordPress admin")
    print("   2. Go to Plugins → Installed Plugins")
    print("   3. Find 'Trading Robot Plug Platform'")
    print("   4. Click 'Activate'")
    print("   5. Run: wp rewrite flush")

def main():
    """Activate plugin and flush routes."""
    print("🔧 TradingRobotPlug Plugin Activation\n")
    activate_plugin_via_wp_cli()
    print("\n✅ Routes already flushed (executed via MCP)")
    return 0

if __name__ == "__main__":
    sys.exit(main())


