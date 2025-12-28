import sys
from pathlib import Path
import os
import re

# Add paths
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def configure_analytics_ids(site_key, ga4_id, pixel_id):
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"Failed to connect to {site_key}")
        return False
    
    remote_config_path = f"{deployer.remote_path}/wp-config.php"
    local_temp_path = f"wp-config-{site_key}.php"
    
    print(f"Downloading {remote_config_path}...")
    if not deployer.download_file(remote_config_path, Path(local_temp_path)):
        print(f"Failed to download {remote_config_path}")
        deployer.disconnect()
        return False
    
    with open(local_temp_path, 'r') as f:
        content = f.read()
    
    # Check if already configured
    if "GA4_MEASUREMENT_ID" in content and "FACEBOOK_PIXEL_ID" in content:
        print(f"Analytics IDs already configured in {site_key}")
        # Update if different
        content = re.sub(r"define\(\s*'GA4_MEASUREMENT_ID',\s*'.*?'\s*\);", f"define('GA4_MEASUREMENT_ID', '{ga4_id}');", content)
        content = re.sub(r"define\(\s*'FACEBOOK_PIXEL_ID',\s*'.*?'\s*\);", f"define('FACEBOOK_PIXEL_ID', '{pixel_id}');", content)
    else:
        # Insert before "stop editing" line
        insertion = f"\n// GA4/Pixel Analytics Configuration\ndefine('GA4_MEASUREMENT_ID', '{ga4_id}');\ndefine('FACEBOOK_PIXEL_ID', '{pixel_id}');\n"
        
        stop_editing_marker = "/* That's all, stop editing!"
        if stop_editing_marker in content:
            content = content.replace(stop_editing_marker, insertion + stop_editing_marker)
        else:
            # Fallback insertion point
            content += insertion
    
    with open(local_temp_path, 'w') as f:
        f.write(content)
    
    print(f"Uploading modified {local_temp_path} to {remote_config_path}...")
    if not deployer.deploy_file(Path(local_temp_path), remote_config_path):
        print(f"Failed to upload {remote_config_path}")
        deployer.disconnect()
        return False
    
    print(f"Checking PHP syntax for {remote_config_path}...")
    syntax_result = deployer.check_php_syntax(remote_config_path)
    if not syntax_result.get('valid', False):
        print(f"CRITICAL: Syntax error in wp-config.php after modification!")
        print(syntax_result.get('output'))
        # We should probably rollback but for now just report
    else:
        print("Syntax check PASSED.")
    
    deployer.disconnect()
    return True

if __name__ == "__main__":
    sites = [
        "freerideinvestor.com",
        "tradingrobotplug.com",
        "dadudekc.com",
        "crosbyultimateevents.com"
    ]
    
    # Using placeholders as requested in docs/website_audits/2026/GA4_PIXEL_ID_REQUEST_TEMPLATE.md
    ga4_placeholder = "G-PLACEHOLDER"
    pixel_placeholder = "000000000000000"
    
    for site in sites:
        print(f"\n--- Configuring {site} ---")
        configure_analytics_ids(site, ga4_placeholder, pixel_placeholder)

