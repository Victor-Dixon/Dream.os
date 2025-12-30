#!/usr/bin/env python3
"""
Deploy TradingRobotPlug.com theme files immediately.
No coordination required - any agent can deploy.

<!-- SSOT Domain: tools -->
"""
import sys
from pathlib import Path

# Add repos to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "websites"))

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def main():
    site_key = "tradingrobotplug.com"
    configs = load_site_configs()
    
    if site_key not in configs:
        print(f"❌ Site '{site_key}' not found in configs")
        return 1
    
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"❌ Failed to connect to {site_key}")
        return 1
    
    print(f"✅ Connected to {site_key}")
    
    # Files to deploy
    theme_dir = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")
    files_to_deploy = [
        "front-page.php",  # Optimized homepage (4 sections)
        "footer.php",  # Updated footer with legal section
        "page-privacy.php",
        "page-terms-of-service.php",
        "page-product-terms.php",
        "page-waitlist.php",
        "page-thank-you.php",
        "page-pricing.php",
        "page-features.php",
        "page-ai-swarm.php",
        "page-blog.php",
        "inc/template-helpers.php",
    ]
    
    remote_base = "wp-content/themes/tradingrobotplug-theme"
    deployed = 0
    failed = 0
    
    for file_name in files_to_deploy:
        local_path = theme_dir / file_name
        if not local_path.exists():
            print(f"⚠️  File not found: {local_path}")
            failed += 1
            continue
        
        remote_path = f"{remote_base}/{file_name}"
        if deployer.deploy_file(local_path, remote_path):
            print(f"✅ Deployed: {file_name}")
            deployed += 1
        else:
            print(f"❌ Failed: {file_name}")
            failed += 1
    
    deployer.disconnect()
    
    print(f"\n📊 Deployment Summary:")
    print(f"   ✅ Deployed: {deployed}")
    print(f"   ❌ Failed: {failed}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

