#!/usr/bin/env python3
"""
TradingRobotPlug.com Urgent Theme Deployment
===========================================

Deploys TradingRobotPlug theme files to production using Hostinger SFTP.
URGENT: Theme not deployed, site non-functional (~5/100 score).

Author: Agent-3 (Infrastructure & DevOps)
Date: 2025-12-26
"""

import sys
from pathlib import Path

# Add websites deployment tools to path
sys.path.insert(0, str(Path("D:/websites/ops/deployment").resolve()))

from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

# Theme files to deploy
THEME_FILES = [
    # Core theme files
    "functions.php",
    "front-page.php",  # CRITICAL - Hero section, waitlist form
    "style.css",
    "header.php",
    "footer.php",
    "index.php",
    # Template helpers
    "inc/template-helpers.php",
    "inc/forms.php",
    "inc/analytics.php",
    "inc/rest-api.php",  # CRITICAL - REST API endpoints
    "inc/dashboard-api.php",
    "inc/asset-enqueue.php",
    "inc/theme-setup.php",
    # Assets
    "assets/css/custom.css",
    "assets/js/main.js",
]

# Local theme directory (check both possible locations)
LOCAL_THEME_DIR = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")
if not LOCAL_THEME_DIR.exists():
    LOCAL_THEME_DIR = Path("D:/websites/sites/tradingrobotplug.com/wp/theme/tradingrobotplug-theme")

# Remote theme path
REMOTE_THEME_PATH = "domains/tradingrobotplug.com/public_html/wp-content/themes/tradingrobotplug-theme"


def deploy_tradingrobotplug_theme(dry_run: bool = False):
    """Deploy TradingRobotPlug theme files to production."""
    print("🚀 TradingRobotPlug.com Urgent Theme Deployment")
    print("=" * 60)
    
    # Load site configurations
    site_configs = load_site_configs()
    if not site_configs:
        print("❌ No site configurations found")
        print("   💡 Ensure HOSTINGER_* environment variables are set in .env")
        return False
    
    # Initialize deployer
    try:
        deployer = SimpleWordPressDeployer("tradingrobotplug.com", site_configs)
    except ValueError as e:
        print(f"❌ {e}")
        return False
    
    # Connect to server
    print(f"\n🔌 Connecting to server...")
    if not deployer.connect():
        print("❌ Failed to connect to server")
        return False
    
    print(f"✅ Connected successfully\n")
    
    # Deploy files
    success_count = 0
    failed_files = []
    
    for file_path in THEME_FILES:
        local_file = LOCAL_THEME_DIR / file_path
        
        if not local_file.exists():
            print(f"⚠️  File not found: {local_file}")
            failed_files.append(file_path)
            continue
        
        # Build remote path
        remote_file = f"{REMOTE_THEME_PATH}/{file_path}"
        
        if dry_run:
            print(f"📋 [DRY RUN] Would deploy: {file_path}")
            print(f"   Local: {local_file}")
            print(f"   Remote: {remote_file}\n")
            success_count += 1
        else:
            print(f"📤 Deploying: {file_path}...")
            if deployer.deploy_file(local_file, remote_file):
                print(f"✅ Deployed: {file_path}\n")
                success_count += 1
            else:
                print(f"❌ Failed: {file_path}\n")
                failed_files.append(file_path)
    
    # Disconnect
    deployer.disconnect()
    
    # Summary
    print("=" * 60)
    print(f"📊 Deployment Summary:")
    print(f"   ✅ Success: {success_count}/{len(THEME_FILES)} files")
    if failed_files:
        print(f"   ❌ Failed: {len(failed_files)} files")
        print(f"   Failed files: {', '.join(failed_files)}")
    
    if success_count == len(THEME_FILES):
        print(f"\n✅ All files deployed successfully!")
        if not dry_run:
            print(f"   🎯 Next steps:")
            print(f"   1. Verify theme activation in WordPress Admin")
            print(f"   2. Clear all caches (WordPress, browser, CDN)")
            print(f"   3. Verify hero section and waitlist form visible on live site")
            print(f"   4. Re-run Agent-1 integration tests")
        return True
    else:
        print(f"\n⚠️  Partial deployment - {len(failed_files)} files failed")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy TradingRobotPlug theme")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (no actual deployment)")
    args = parser.parse_args()
    
    success = deploy_tradingrobotplug_theme(dry_run=args.dry_run)
    sys.exit(0 if success else 1)

