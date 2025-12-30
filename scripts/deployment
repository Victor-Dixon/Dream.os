import sys
from pathlib import Path
import os

# Add paths
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def deploy_tier2_foundation(site_key, local_theme_path, remote_theme_path):
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"Failed to connect to {site_key}")
        return False
    
    local_path = Path(local_theme_path)
    if not local_path.exists():
        print(f"Local path does not exist: {local_theme_path}")
        deployer.disconnect()
        return False
    
    print(f"Starting Tier 2 Foundation deployment for {site_key}...")
    
    # Pre-create remote directories
    remote_dirs = [
        remote_theme_path,
        f"{remote_theme_path}/template-parts",
        f"{remote_theme_path}/template-parts/components",
        f"{remote_theme_path}/inc",
        f"{remote_theme_path}/inc/post-types",
        f"{remote_theme_path}/inc/meta-boxes",
        f"{remote_theme_path}/inc/cli-commands"
    ]
    for rd in remote_dirs:
        deployer.execute_command(f"mkdir -p {rd}")
    
    # Specific files to deploy
    files_to_sync = [
        "front-page.php",
        "index.php",
        "functions.php",
        "style.css",
        "template-parts/components/icp-definition.php",
        "template-parts/components/offer-ladder.php",
        "inc/post-types/icp-definition.php",
        "inc/post-types/offer-ladder.php"
    ]
    
    # For freerideinvestor.com, also include positioning-statement and different inc paths
    if "freerideinvestor" in site_key:
        files_to_sync.append("template-parts/components/positioning-statement.php")
        files_to_sync.append("inc/post-types/icp-definition.php")
        files_to_sync.append("inc/theme-setup.php")
        files_to_sync.append("inc/meta-boxes/brand-core-meta-boxes.php")
        files_to_sync.append("inc/cli-commands/create-brand-core-content.php")
    
    success_count = 0
    fail_count = 0
    
    for rel_path in files_to_sync:
        local_file = local_path / rel_path
        if local_file.exists():
            remote_file = f"{remote_theme_path}/{rel_path}".replace("\\", "/")
            print(f"Deploying {rel_path}...")
            if deployer.deploy_file(local_file, remote_file):
                success_count += 1
            else:
                fail_count += 1
        else:
            # Skip if file doesn't exist locally (e.g. index.php vs front-page.php)
            continue
            
    print(f"Deployment complete for {site_key}. Success: {success_count}, Failed: {fail_count}")
    deployer.disconnect()
    return fail_count == 0

if __name__ == "__main__":
    # Site 1: crosbyultimateevents.com
    deploy_tier2_foundation(
        "crosbyultimateevents.com",
        "D:/websites/sites/crosbyultimateevents.com/wp/theme/crosbyultimateevents",
        "domains/crosbyultimateevents.com/public_html/wp-content/themes/crosbyultimateevents"
    )
    
    # Site 2: dadudekc.com
    deploy_tier2_foundation(
        "dadudekc.com",
        "D:/websites/sites/dadudekc.com/wp/theme/dadudekc",
        "domains/dadudekc.com/public_html/wp-content/themes/dadudekc"
    )
    
    # Site 3: freerideinvestor.com
    deploy_tier2_foundation(
        "freerideinvestor.com",
        "D:/websites/websites/freerideinvestor.com/wp/wp-content/themes/freerideinvestor-modern",
        "domains/freerideinvestor.com/public_html/wp-content/themes/freerideinvestor-modern"
    )

