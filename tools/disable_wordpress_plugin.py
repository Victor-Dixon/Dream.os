#!/usr/bin/env python3
"""
Disable a specific WordPress plugin by renaming its directory
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager


def disable_plugin(site: str, plugin_name: str) -> bool:
    """Disable a WordPress plugin by renaming its directory."""
    print("=" * 60)
    print(f"🔌 Disabling Plugin: {plugin_name}")
    print("=" * 60)
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        
        # Get plugins path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                plugins_path = f"domains/{domain}/public_html/wp-content/plugins"
            else:
                plugins_path = "/public_html/wp-content/plugins"
        else:
            plugins_path = "/public_html/wp-content/plugins"
        
        try:
            sftp = manager.conn_manager.sftp
            
            # Find plugin directory
            active_plugins = sftp.listdir(plugins_path)
            plugin_dir = None
            
            for plugin in active_plugins:
                if plugin_name.lower() in plugin.lower():
                    plugin_dir = plugin
                    break
            
            if not plugin_dir:
                print(f"❌ Plugin '{plugin_name}' not found")
                print(f"Available plugins: {', '.join(active_plugins)}")
                manager.disconnect()
                return False
            
            plugin_path = f"{plugins_path}/{plugin_dir}"
            disabled_path = f"{plugins_path}/{plugin_dir}.disabled"
            
            # Check if already disabled
            try:
                sftp.stat(disabled_path)
                print(f"⚠️  Plugin already disabled: {plugin_dir}.disabled")
                manager.disconnect()
                return True
            except FileNotFoundError:
                pass
            
            # Rename plugin directory
            sftp.rename(plugin_path, disabled_path)
            print(f"✅ Plugin disabled: {plugin_dir} → {plugin_dir}.disabled")
            print("💡 Test the site now. To re-enable, rename back:")
            print(f"   {plugin_dir}.disabled → {plugin_dir}")
            
            manager.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Error disabling plugin: {e}")
            manager.disconnect()
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Disable a WordPress plugin")
    parser.add_argument("--site", required=True, help="Site key")
    parser.add_argument("--plugin", required=True, help="Plugin name (partial match)")
    
    args = parser.parse_args()
    disable_plugin(args.site, args.plugin)

