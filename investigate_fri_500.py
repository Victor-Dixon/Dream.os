import sys
from pathlib import Path
import os

# Add paths
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def investigate_500_error(site_key):
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"Failed to connect to {site_key}")
        return False
    
    remote_path = deployer.remote_path
    print(f"Connected to {site_key}. Remote path: {remote_path}")
    
    # Check for error_log at root
    error_log_path = f"{remote_path}/error_log"
    print(f"Checking {error_log_path}...")
    if deployer.file_exists(error_log_path):
        print("error_log found! Downloading last 50 lines...")
        # We don't have a tail_file method in SimpleWordPressDeployer, so we download and read
        local_log = f"error_log_{site_key}.txt"
        if deployer.download_file(error_log_path, Path(local_log)):
            with open(local_log, 'r') as f:
                lines = f.readlines()
                for line in lines[-50:]:
                    print(line.strip())
    else:
        print("error_log not found at root.")
        
    # Check for wp-content/debug.log
    debug_log_path = f"{remote_path}/wp-content/debug.log"
    print(f"Checking {debug_log_path}...")
    if deployer.file_exists(debug_log_path):
        print("debug.log found! Downloading last 50 lines...")
        local_debug = f"debug_log_{site_key}.txt"
        if deployer.download_file(debug_log_path, Path(local_debug)):
            with open(local_debug, 'r') as f:
                lines = f.readlines()
                for line in lines[-50:]:
                    print(line.strip())
    else:
        print("debug.log not found.")

    # Check wp-config.php for WP_DEBUG
    config_path = f"{remote_path}/wp-config.php"
    print(f"Downloading {config_path}...")
    local_config = f"wp-config-{site_key}-investigate.php"
    if deployer.download_file(config_path, Path(local_config)):
        with open(local_config, 'r') as f:
            content = f.read()
            if "define('WP_DEBUG', true)" in content or "define( 'WP_DEBUG', true )" in content:
                print("WP_DEBUG is ENABLED")
            else:
                print("WP_DEBUG is DISABLED")
                
    deployer.disconnect()

if __name__ == "__main__":
    investigate_500_error("freerideinvestor.com")

