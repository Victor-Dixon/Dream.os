#!/usr/bin/env python3
"""
Deploy TradingRobotPlug Theme NOW
==================================

Actually deploys theme files to live server.
"""

import sys
from pathlib import Path

# Add deployment tools to path
sys.path.insert(0, str(Path("D:/websites/ops/deployment")))

try:
    from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
    DEPLOYER_AVAILABLE = True
except ImportError:
    print("❌ SimpleWordPressDeployer not available")
    DEPLOYER_AVAILABLE = False
    sys.exit(1)

# Theme path
theme_path = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")

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
    "inc/dashboard-api.php",  # Updated: Primary symbols (TSLA, QQQ, SPY, NVDA) + data collection
    "inc/charts-api.php",  # Updated: Primary symbols focus
    "inc/asset-enqueue.php",
    "inc/theme-setup.php",
    "assets/css/custom.css",
    "assets/js/main.js",
]

def main():
    """Deploy theme files."""
    print("🚀 Deploying TradingRobotPlug Theme")
    print("=" * 60)
    
    if not theme_path.exists():
        print(f"❌ Theme path not found: {theme_path}")
        return
    
    # Load site configs
    site_configs = load_site_configs()
    
    # Initialize deployer
    deployer = SimpleWordPressDeployer("tradingrobotplug.com", site_configs)
    
    # Connect to server
    print("🔌 Connecting to server...", end=" ")
    if not deployer.connect():
        print("❌")
        print("❌ Failed to connect to server. Check credentials and network.")
        return
    print("✅")
    print()
    
    # Get remote path
    remote_path = getattr(deployer, 'remote_path', '') or "domains/tradingrobotplug.com/public_html"
    theme_remote_path = f"{remote_path}/wp-content/themes/tradingrobotplug-theme"
    
    print(f"📁 Remote theme path: {theme_remote_path}")
    print()
    
    # Deploy files
    deployed = 0
    failed = 0
    
    for file_path in files_to_deploy:
        local_file = theme_path / file_path
        remote_file = f"{theme_remote_path}/{file_path}"
        
        if not local_file.exists():
            print(f"⚠️  Skipping (not found): {file_path}")
            continue
        
        print(f"📤 Deploying: {file_path}...", end=" ")
        
        try:
            if deployer.deploy_file(local_file, remote_file):
                print("✅")
                deployed += 1
            else:
                print("❌")
                failed += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"✅ Deployed: {deployed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(files_to_deploy)}")
    
    # Disconnect
    deployer.disconnect()
    
    if deployed > 0:
        print()
        print("🎉 Deployment complete!")
        print("   Next: Verify theme activation in WordPress Admin")
        print("   Next: Run verification tests")

if __name__ == "__main__":
    main()




