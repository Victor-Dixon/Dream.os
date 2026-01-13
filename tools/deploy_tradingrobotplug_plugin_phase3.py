#!/usr/bin/env python3
"""
⚠️ DEPRECATED - DO NOT USE

This file is deprecated as part of the SSOT consolidation effort.

REPLACEMENT: mcp_servers/deployment_server.py
MIGRATION: Use deploy_wordpress_theme() function instead
DEADLINE: 2026-02-01

For new code, use: mcp_servers/deployment_server.py::deploy_wordpress_theme()

Original docstring:
Deploy TradingRobotPlug Phase 3 Plugin to Production

Deploys entire plugin directory to production WordPress site.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ops" / "deployment"))
from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def deploy_plugin():
    """Deploy TradingRobotPlug plugin to production."""
    print("🚀 TradingRobotPlug Phase 3 Plugin Deployment\n")
    
    site_key = "tradingrobotplug.com"
    project_root = Path(__file__).parent.parent
    
    # Try multiple possible local paths
    local_plugin_paths = [
        Path("D:/websites/sites/tradingrobotplug.com/wp/plugins/tradingrobotplug-wordpress-plugin"),
        project_root / "websites" / "sites" / "tradingrobotplug.com" / "wp" / "plugins" / "tradingrobotplug-wordpress-plugin",
        Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/plugins/tradingrobotplug-wordpress-plugin"),
    ]
    
    local_plugin_dir = None
    for path in local_plugin_paths:
        if path.exists():
            local_plugin_dir = path
            break
    
    if not local_plugin_dir:
        print(f"❌ ERROR: Local plugin directory not found in any expected location")
        return False
    
    remote_plugin_dir = "wp-content/plugins/tradingrobotplug-wordpress-plugin"
    
    print(f"✅ Local plugin found: {local_plugin_dir}")
    print(f"📦 Deploying to: {remote_plugin_dir}\n")
    
    # Initialize deployer
    try:
        site_configs = load_site_configs()
        deployer = SimpleWordPressDeployer(site_key, site_configs)
        
        if not deployer.connect():
            print("❌ Failed to connect to SFTP server")
            return False
        
        print(f"✅ Connected to {site_key}\n")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize deployer: {e}")
        return False
    
    # Deploy all plugin files
    deployed_count = 0
    failed_count = 0
    
    for local_file in local_plugin_dir.rglob("*"):
        if local_file.is_file():
            relative_path = local_file.relative_to(local_plugin_dir)
            remote_relative = f"{remote_plugin_dir}/{relative_path.as_posix()}"
            
            # Build full remote path
            remote_base = deployer.remote_path or f"/home/u996867598/domains/{site_key}/public_html"
            full_remote_path = f"{remote_base}/{remote_relative}".replace('\\', '/')
            
            # Ensure remote directory exists
            remote_dir = '/'.join(full_remote_path.split('/')[:-1])
            mkdir_cmd = f"mkdir -p {remote_dir}"
            deployer.execute_command(mkdir_cmd)
            
            try:
                success = deployer.deploy_file(local_file, full_remote_path)
                if success:
                    deployed_count += 1
                    if deployed_count % 10 == 0:
                        print(f"✅ Deployed {deployed_count} files...")
                else:
                    failed_count += 1
                    print(f"❌ Failed: {relative_path}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Error deploying {relative_path}: {e}")
    
    deployer.disconnect()
    
    print(f"\n📊 Deployment Summary:")
    print(f"   ✅ Deployed: {deployed_count} files")
    print(f"   ❌ Failed: {failed_count} files")
    
    if failed_count == 0:
        print("\n✅ Plugin deployment complete!")
        print("\n📋 Next Steps:")
        print("   1. Agent-7: Activate plugin via WP-CLI")
        print("   2. Agent-7: Verify REST API endpoints")
        return True
    else:
        print(f"\n⚠️  Deployment completed with {failed_count} failures")
        return False

if __name__ == "__main__":
    success = deploy_plugin()
    sys.exit(0 if success else 1)

