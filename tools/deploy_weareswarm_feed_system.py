#!/usr/bin/env python3
"""Deploy weareswarm.online dynamic feed system."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "websites"))

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def main():
    site_key = "weareswarm.online"
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"❌ Failed to connect to {site_key}")
        return 1
    
    print(f"✅ Connected to {site_key}")
    
    # Deploy updated front-page.php
    theme_dir = Path("D:/websites/sites/weareswarm.online/wp/theme/swarm")
    front_page = theme_dir / "front-page.php"
    
    if not front_page.exists():
        print(f"⚠️  File not found: {front_page}")
        return 1
    
    remote_path = "wp-content/themes/swarm/front-page.php"
    if deployer.deploy_file(front_page, remote_path):
        print(f"✅ Deployed: front-page.php")
    else:
        print(f"❌ Failed: front-page.php")
        deployer.disconnect()
        return 1
    
    # Deploy updated plugin
    plugin_file = Path("D:/websites/Swarm_website/swarm-build-feed.php")
    if plugin_file.exists():
        remote_plugin_path = "wp-content/plugins/swarm-build-feed/swarm-build-feed.php"
        if deployer.deploy_file(plugin_file, remote_plugin_path):
            print(f"✅ Deployed: swarm-build-feed.php")
        else:
            print(f"⚠️  Plugin deployment failed (may need manual activation)")
    
    deployer.disconnect()
    print(f"✅ Feed system deployment complete for {site_key}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

