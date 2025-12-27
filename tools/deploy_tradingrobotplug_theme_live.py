#!/usr/bin/env python3
"""
Deploy TradingRobotPlug Theme - LIVE DEPLOYMENT
==============================================

Actually deploys theme files to live server.
"""

import sys
from pathlib import Path

# Add deployment tools to path
sys.path.insert(0, str(Path("D:/websites/ops/deployment")))

from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

# Theme path
theme_path = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme").resolve()

# Files to deploy
files_to_deploy = [
    "functions.php",
    "front-page.php",
    "style.css",
    "header.php",
    "footer.php",
    "index.php",
    "inc/template-helpers.php",
    "inc/forms.php",
    "inc/analytics.php",
    "inc/rest-api.php",
    "inc/dashboard-api.php",
    "inc/asset-enqueue.php",
    "inc/theme-setup.php",
    "assets/css/custom.css",
    "assets/js/main.js",
]

def main():
    """Deploy theme files."""
    print("🚀 Deploying TradingRobotPlug Theme - LIVE")
    print("=" * 60)
    
    if not theme_path.exists():
        print(f"❌ Theme path not found: {theme_path}")
        return 1
    
    # Load site configs
    site_configs = load_site_configs()
    
    # Initialize deployer
    deployer = SimpleWordPressDeployer("tradingrobotplug.com", site_configs)
    
    # Connect
    print("📡 Connecting to server...")
    if not deployer.connect():
        print("❌ Failed to connect")
        return 1
    
    print("✅ Connected!")
    
    # Get remote path
    remote_path = getattr(deployer, 'remote_path', '') or "domains/tradingrobotplug.com/public_html"
    theme_remote_path = f"{remote_path}/wp-content/themes/tradingrobotplug-theme"
    
    # Get username for full path
    username = deployer.site_config.get('username') if 'username' in deployer.site_config else deployer.site_config.get('sftp', {}).get('username', 'u996867598')
    full_remote_base = f"/home/{username}/{theme_remote_path}"
    
    print(f"📁 Remote theme path: {full_remote_base}")
    print()
    
    # Create remote directories first
    print("📁 Creating remote directories...")
    dirs_to_create = [
        full_remote_base,
        f"{full_remote_base}/inc",
        f"{full_remote_base}/assets",
        f"{full_remote_base}/assets/css",
        f"{full_remote_base}/assets/js",
    ]
    
    for dir_path in dirs_to_create:
        try:
            deployer.sftp.stat(dir_path)
            print(f"   ✅ {dir_path} exists")
        except FileNotFoundError:
            try:
                # Create directory recursively
                parts = dir_path.strip('/').split('/')
                current = ''
                for part in parts:
                    if part:
                        current = f"{current}/{part}" if current else f"/{part}"
                        try:
                            deployer.sftp.stat(current)
                        except FileNotFoundError:
                            deployer.sftp.mkdir(current)
                            print(f"   ✅ Created: {current}")
            except Exception as e:
                print(f"   ⚠️  Could not create {dir_path}: {e}")
    
    print()
    
    # Deploy files
    print("📤 Deploying files...")
    deployed = 0
    failed = 0
    
    for file_path in files_to_deploy:
        local_file = theme_path / file_path
        remote_file = f"{full_remote_base}/{file_path}"
        
        if not local_file.exists():
            print(f"⚠️  Skipping (not found): {file_path}")
            continue
        
        print(f"   📤 {file_path}...", end=" ")
        
        try:
            deployer.sftp.put(str(local_file), remote_file)
            print("✅")
            deployed += 1
        except Exception as e:
            print(f"❌ {e}")
            failed += 1
    
    # Close connection
    deployer.disconnect()
    
    print()
    print("=" * 60)
    print(f"✅ Deployed: {deployed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(files_to_deploy)}")
    
    if deployed > 0:
        print()
        print("🎉 Deployment complete!")
        print("   Next: Verify theme activation in WordPress Admin")
        print("   Next: Run verification tests")
        return 0
    else:
        print()
        print("❌ Deployment failed - no files deployed")
        return 1

if __name__ == "__main__":
    sys.exit(main())




