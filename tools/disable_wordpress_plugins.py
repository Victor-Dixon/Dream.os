#!/usr/bin/env python3
"""
Disable WordPress Plugins - Isolate Plugin Conflicts
====================================================

Disables WordPress plugins by renaming the plugins folder.
Helps identify if a plugin is causing the critical error.

Author: Agent-3 (Infrastructure & DevOps Specialist)

<!-- SSOT Domain: infrastructure -->
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager


def disable_plugins(site: str, disable: bool = True) -> bool:
    """
    Disable or enable WordPress plugins.
    
    Args:
        site: Site key
        disable: True to disable, False to enable
        
    Returns:
        True if successful
    """
    action = "Disable" if disable else "Enable"
    print("=" * 60)
    print(f"🔧 {action} WordPress Plugins")
    print("=" * 60)
    print(f"Site: {site}")
    print()
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        print()
        
        # Path to plugins directory
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                plugins_path = f"domains/{domain}/public_html/wp-content/plugins"
                plugins_disabled_path = f"domains/{domain}/public_html/wp-content/plugins-disabled"
            else:
                plugins_path = "/public_html/wp-content/plugins"
                plugins_disabled_path = "/public_html/wp-content/plugins-disabled"
        else:
            plugins_path = "/public_html/wp-content/plugins"
            plugins_disabled_path = "/public_html/wp-content/plugins-disabled"
        
        sftp = manager.conn_manager.sftp
        
        try:
            if disable:
                # Check if plugins directory exists
                try:
                    sftp.stat(plugins_path)
                    print(f"📁 Found plugins directory")
                except FileNotFoundError:
                    print(f"⚠️  Plugins directory not found: {plugins_path}")
                    manager.disconnect()
                    return False
                
                # Check if already disabled
                try:
                    sftp.stat(plugins_disabled_path)
                    print("✅ Plugins already disabled")
                    manager.disconnect()
                    return True
                except FileNotFoundError:
                    pass
                
                # Rename plugins to plugins-disabled
                print(f"🔄 Renaming plugins → plugins-disabled...")
                sftp.rename(plugins_path, plugins_disabled_path)
                print("✅ Plugins disabled!")
                print("💡 Test the site now. If it works, a plugin is causing the error.")
                
            else:
                # Enable plugins
                try:
                    sftp.stat(plugins_disabled_path)
                    print(f"📁 Found plugins-disabled directory")
                except FileNotFoundError:
                    print(f"⚠️  plugins-disabled directory not found")
                    manager.disconnect()
                    return False
                
                # Check if already enabled
                try:
                    sftp.stat(plugins_path)
                    print("✅ Plugins already enabled")
                    manager.disconnect()
                    return True
                except FileNotFoundError:
                    pass
                
                # Rename plugins-disabled back to plugins
                print(f"🔄 Renaming plugins-disabled → plugins...")
                sftp.rename(plugins_disabled_path, plugins_path)
                print("✅ Plugins enabled!")
            
            manager.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            manager.disconnect()
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Disable/enable WordPress plugins")
    parser.add_argument("--site", required=True, help="Site key")
    parser.add_argument("--enable", action="store_true", help="Enable plugins (default: disable)")
    
    args = parser.parse_args()
    success = disable_plugins(args.site, disable=not args.enable)
    sys.exit(0 if success else 1)

