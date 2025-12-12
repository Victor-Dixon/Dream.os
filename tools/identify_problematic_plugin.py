#!/usr/bin/env python3
"""
Identify Problematic WordPress Plugin
=====================================

Re-enables plugins one by one to identify which plugin causes the error.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import sys
import time
import requests
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager


def identify_problematic_plugin(site: str, site_url: str) -> str:
    """
    Identify which plugin is causing the error.
    
    Args:
        site: Site key
        site_url: Site URL (e.g., https://freerideinvestor.com)
        
    Returns:
        Name of problematic plugin, or None if not found
    """
    print("=" * 60)
    print("🔍 Identify Problematic WordPress Plugin")
    print("=" * 60)
    print(f"Site: {site}")
    print(f"URL: {site_url}")
    print()
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return None
        
        print("📡 Connected to server")
        print()
        
        # Path to plugins directories
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                plugins_disabled_path = f"domains/{domain}/public_html/wp-content/plugins-disabled"
            else:
                plugins_disabled_path = "/public_html/wp-content/plugins-disabled"
        else:
            plugins_disabled_path = "/public_html/wp-content/plugins-disabled"
        
        sftp = manager.conn_manager.sftp
        
        # List plugins in disabled folder
        print("📋 Listing disabled plugins...")
        try:
            plugins = sftp.listdir(plugins_disabled_path)
            # Filter out . and .. and non-directory items
            plugin_dirs = []
            for plugin in plugins:
                try:
                    plugin_path = f"{plugins_disabled_path}/{plugin}"
                    attrs = sftp.stat(plugin_path)
                    # Check if it's a directory (basic check)
                    if attrs.st_mode & 0o040000:  # Directory bit
                        plugin_dirs.append(plugin)
                except:
                    pass
            
            print(f"   Found {len(plugin_dirs)} plugins")
            print()
            
            if not plugin_dirs:
                print("⚠️  No plugins found in disabled folder")
                manager.disconnect()
                return None
            
            # Re-enable plugins one by one
            print("🔄 Testing plugins one by one...")
            print()
            
            # First, ensure plugins folder exists
            plugins_path = plugins_disabled_path.replace("-disabled", "")
            try:
                sftp.stat(plugins_path)
            except FileNotFoundError:
                sftp.mkdir(plugins_path)
            
            problematic_plugin = None
            
            for i, plugin in enumerate(plugin_dirs, 1):
                print(f"[{i}/{len(plugin_dirs)}] Testing: {plugin}")
                
                # Move plugin from disabled to enabled
                disabled_plugin_path = f"{plugins_disabled_path}/{plugin}"
                enabled_plugin_path = f"{plugins_path}/{plugin}"
                
                try:
                    sftp.rename(disabled_plugin_path, enabled_plugin_path)
                    print(f"   ✅ Enabled {plugin}")
                    
                    # Wait a moment for WordPress to load
                    time.sleep(2)
                    
                    # Test site
                    try:
                        response = requests.get(site_url, timeout=10)
                        if response.status_code == 500:
                            print(f"   ❌ ERROR: {plugin} causes HTTP 500!")
                            problematic_plugin = plugin
                            
                            # Move it back to disabled
                            sftp.rename(enabled_plugin_path, disabled_plugin_path)
                            print(f"   🔄 Disabled {plugin} again")
                            break
                        else:
                            print(f"   ✅ Site works with {plugin}")
                    except Exception as e:
                        print(f"   ⚠️  Error testing site: {e}")
                        
                except Exception as e:
                    print(f"   ❌ Error enabling plugin: {e}")
            
            manager.disconnect()
            
            if problematic_plugin:
                print()
                print("=" * 60)
                print(f"🎯 PROBLEMATIC PLUGIN IDENTIFIED: {problematic_plugin}")
                print("=" * 60)
                return problematic_plugin
            else:
                print()
                print("=" * 60)
                print("✅ All plugins tested - none cause HTTP 500")
                print("💡 The issue may be a plugin combination or theme conflict")
                print("=" * 60)
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            manager.disconnect()
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Identify problematic WordPress plugin")
    parser.add_argument("--site", required=True, help="Site key")
    parser.add_argument("--url", required=True, help="Site URL")
    
    args = parser.parse_args()
    result = identify_problematic_plugin(args.site, args.url)
    sys.exit(0 if result else 1)

