#!/usr/bin/env python3
"""
Check Business Plan Plugin Status
==================================

Checks if the plugin is installed and activated on WordPress.

Usage:
    python check_plugin_status.py --site crosbyultimateevents.com
"""

import sys
from pathlib import Path

# Add tools to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "tools"))

try:
    from wordpress_manager import WordPressManager
    HAS_WP_MANAGER = True
except ImportError:
    HAS_WP_MANAGER = False
    print("Warning: wordpress_manager not available")


def check_plugin_status(site_name: str = "crosbyultimateevents.com"):
    """Check if plugin is installed and activated."""
    
    if not HAS_WP_MANAGER:
        print("❌ WordPress manager not available")
        return False
    
    print(f"🔍 Checking plugin status for {site_name}...\n")
    
    try:
        manager = WordPressManager(site_name)
        
        # Check if plugin is installed
        print("1. Checking if plugin is installed...")
        stdout, stderr, code = manager.wp_cli("plugin list --format=json")
        
        if code == 0:
            import json
            try:
                plugins = json.loads(stdout)
                plugin_found = False
                for plugin in plugins:
                    if 'crosby-business-plan' in plugin.get('name', '').lower() or 'business-plan' in plugin.get('name', '').lower():
                        plugin_found = True
                        status = plugin.get('status', 'unknown')
                        version = plugin.get('version', 'N/A')
                        name = plugin.get('name', 'Unknown')
                        
                        print(f"   ✅ Plugin found: {name}")
                        print(f"      Status: {status}")
                        print(f"      Version: {version}")
                        
                        if status == 'active':
                            print("\n   ✅ Plugin is ACTIVATED")
                        else:
                            print(f"\n   ⚠️  Plugin is NOT activated (status: {status})")
                            print("   💡 Activate it with:")
                            print(f"      python tools/wordpress_manager.py --site {site_name} --wp-cli-path 'wp' --execute 'plugin activate crosby-business-plan'")
                            # Try to activate it
                            print("\n   🔄 Attempting to activate...")
                            activate_stdout, activate_stderr, activate_code = manager.wp_cli(f"plugin activate {name}")
                            if activate_code == 0:
                                print("   ✅ Plugin activated successfully!")
                            else:
                                print(f"   ❌ Activation failed: {activate_stderr or activate_stdout}")
                        
                        break
                
                if not plugin_found:
                    print("   ❌ Plugin not found in plugin list")
                    print("   💡 Make sure plugin files are deployed correctly")
                    print(f"      Expected location: /wp-content/plugins/crosby-business-plan/")
                    
            except json.JSONDecodeError:
                print(f"   ⚠️  Could not parse plugin list: {stdout}")
        else:
            print(f"   ❌ Failed to get plugin list: {stderr or stdout}")
        
        # Check plugin directory exists
        print("\n2. Checking plugin files on server...")
        check_stdout, check_stderr, check_code = manager.wp_cli("eval 'echo file_exists(ABSPATH . \"wp-content/plugins/crosby-business-plan/crosby-business-plan.php\") ? \"EXISTS\" : \"NOT_FOUND\";'")
        
        if 'EXISTS' in check_stdout:
            print("   ✅ Plugin main file exists on server")
        else:
            print("   ❌ Plugin main file NOT found on server")
            print("   💡 Plugin may need to be redeployed")
        
        # Check for PHP errors
        print("\n3. Checking for PHP errors...")
        error_stdout, error_stderr, error_code = manager.wp_cli("eval 'if (file_exists(ABSPATH . \"wp-content/plugins/crosby-business-plan/crosby-business-plan.php\")) { include_once(ABSPATH . \"wp-content/plugins/crosby-business-plan/crosby-business-plan.php\"); echo \"LOADED\"; } else { echo \"NOT_FOUND\"; }'")
        
        if 'LOADED' in error_stdout:
            print("   ✅ Plugin file loads without errors")
        else:
            print(f"   ⚠️  Plugin file check: {error_stdout}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking plugin status: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check Business Plan Plugin Status")
    parser.add_argument(
        "--site",
        default="crosbyultimateevents.com",
        help="WordPress site name"
    )
    
    args = parser.parse_args()
    check_plugin_status(args.site)

