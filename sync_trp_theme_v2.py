import sys
from pathlib import Path
import os

# Add paths
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def deploy_full_theme(site_key, local_theme_path, remote_theme_path):
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
    
    print(f"Starting full theme deployment for {site_key}...")
    
    # Pre-create all directories using SSH mkdir -p
    print("Pre-creating remote directories...")
    all_dirs = set()
    for root, dirs, files in os.walk(local_path):
        for d in dirs:
            dir_path = Path(root) / d
            rel_dir = dir_path.relative_to(local_path)
            all_dirs.add(f"{remote_theme_path}/{rel_dir}".replace('\\', '/'))
    
    for d in sorted(list(all_dirs)):
        # print(f"Creating {d}...")
        deployer.execute_command(f"mkdir -p {d}")
    
    files_count = 0
    errors_count = 0
    
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if file.endswith('.pyc') or file == '__pycache__':
                continue
                
            local_file_path = Path(root) / file
            relative_path = local_file_path.relative_to(local_path)
            remote_file_path = f"{remote_theme_path}/{relative_path}".replace('\\', '/')
            
            if deployer.deploy_file(local_file_path, remote_file_path):
                files_count += 1
            else:
                print(f"Failed to deploy {relative_path}")
                errors_count += 1
    
    print(f"Deployment complete. Files deployed: {files_count}, Errors: {errors_count}")
    
    deployer.disconnect()
    return errors_count == 0

if __name__ == "__main__":
    local_trp = "D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme"
    remote_trp = "domains/tradingrobotplug.com/public_html/wp-content/themes/tradingrobotplug-theme"
    
    deploy_full_theme("tradingrobotplug.com", local_trp, remote_trp)

