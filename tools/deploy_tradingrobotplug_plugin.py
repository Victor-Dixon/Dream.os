#!/usr/bin/env python3
"""
Deploy TradingRobotPlug plugin to production WordPress site.

<!-- SSOT Domain: web -->
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Add websites repo to path
websites_root = Path("D:/websites")
sys.path.insert(0, str(websites_root))

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def deploy_plugin():
    """Deploy TradingRobotPlug plugin to production."""
    site_key = "tradingrobotplug.com"
    
    # Load site configs
    site_configs = load_site_configs()
    if not site_configs:
        print("❌ No site configurations found")
        return False
    
    # Initialize deployer
    deployer = SimpleWordPressDeployer(site_key, site_configs)
    
    # Connect to SFTP
    if not deployer.connect():
        print("❌ Failed to connect to SFTP server")
        return False
    
    # Plugin source directory
    plugin_source = Path("D:/websites/sites/tradingrobotplug.com/wp/plugins/tradingrobotplug-wordpress-plugin")
    if not plugin_source.exists():
        print(f"❌ Plugin source not found: {plugin_source}")
        return False
    
    # Remote plugin directory
    remote_plugin_dir = "wp-content/plugins/tradingrobotplug-wordpress-plugin"
    
    print(f"🚀 Deploying TradingRobotPlug plugin to {site_key}\n")
    print(f"   Source: {plugin_source}")
    print(f"   Target: {remote_plugin_dir}\n")
    
    # Deploy all plugin files
    deployed_count = 0
    failed_count = 0
    
    # Get all files in plugin directory
    for file_path in plugin_source.rglob("*"):
        if file_path.is_file():
            # Calculate relative path
            rel_path = file_path.relative_to(plugin_source)
            remote_path = f"{remote_plugin_dir}/{rel_path.as_posix()}"
            
            try:
                deployer.deploy_file(file_path, remote_path)
                deployed_count += 1
                if deployed_count % 10 == 0:
                    print(f"   ✅ Deployed {deployed_count} files...")
            except Exception as e:
                print(f"   ❌ Failed to deploy {rel_path}: {e}")
                failed_count += 1
    
    print(f"\n📊 Deployment Summary:")
    print(f"   ✅ Deployed: {deployed_count} files")
    if failed_count > 0:
        print(f"   ❌ Failed: {failed_count} files")
    
    if failed_count == 0:
        print("\n✅ Plugin deployment complete!")
        print("   Next: Activate plugin via WP-CLI")
        return True
    else:
        print(f"\n⚠️  Deployment completed with {failed_count} failures")
        return False

def main():
    """Deploy plugin."""
    success = deploy_plugin()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

