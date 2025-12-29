import sys
from pathlib import Path
import os

# Add project root to path
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def deploy_trp_templates():
    site_key = "tradingrobotplug.com"
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"❌ Failed to connect to {site_key}")
        return False
    
    # Local paths (fromwebsites repo)
    local_base = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")
    
    templates = [
        "page-waitlist.php",
        "page-thank-you.php",
        "page-pricing.php",
        "page-features.php",
        "page-ai-swarm.php",
        "page-blog.php"
    ]
    
    # Remote paths
    # From site_configs.json: "remote_path": "domains/tradingrobotplug.com/public_html"
    remote_theme_base = f"{deployer.remote_path}/wp-content/themes/tradingrobotplug-theme"
    
    print(f"🚀 Deploying 6 templates to {site_key}...")
    
    success_count = 0
    for template in templates:
        local_path = local_base / template
        remote_path = f"{remote_theme_base}/{template}"
        
        if not local_path.exists():
            print(f"⚠️  Local file not found: {local_path}")
            continue
            
        print(f"📤 Uploading {template} -> {remote_path}...", end=" ")
        if deployer.deploy_file(local_path, remote_path):
            print("✅")
            # Verify syntax
            syntax_check = deployer.check_php_syntax(remote_path)
            if syntax_check["valid"]:
                print(f"   ✅ Syntax OK")
                success_count += 1
            else:
                print(f"   ❌ Syntax Error: {syntax_check['error_message']} on line {syntax_check['line_number']}")
        else:
            print("❌")

    deployer.disconnect()
    
    print(f"\n📊 Summary: {success_count}/{len(templates)} templates deployed and verified.")
    return success_count == len(templates)

if __name__ == "__main__":
    deploy_trp_templates()

