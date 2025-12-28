import sys
from pathlib import Path
import os

# Add paths
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def check_posts_remotely(site_key):
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"Failed to connect to {site_key}")
        return False
    
    print(f"Connected to {site_key}. Checking posts...")
    
    # Create a temporary PHP script to check posts
    php_code = """<?php
define('WP_USE_THEMES', false);
require('./wp-load.php');

$post_types = ['icp_definition', 'offer_ladder'];
foreach ($post_types as $pt) {
    echo "--- $pt ---\\n";
    $exists = post_type_exists($pt);
    echo "Post type exists: " . ($exists ? 'YES' : 'NO') . "\\n";
    if ($exists) {
        $posts = get_posts(['post_type' => $pt, 'post_status' => 'any', 'posts_per_page' => -1]);
        foreach ($posts as $p) {
            $site = get_post_meta($p->ID, 'site_assignment', true);
            echo "ID: $p->ID, Title: $p->post_title, Status: $p->post_status, Site: $site\\n";
        }
    }
}
?>"""
    
    with open('check_posts.php', 'w') as f:
        f.write(php_code)
        
    remote_script = f"{deployer.remote_path}/check_posts_temp.php"
    deployer.deploy_file(Path('check_posts.php'), remote_script)
    
    # Execute the script
    output = deployer.execute_command(f"php {remote_script}")
    print(output)
    
    # Cleanup
    deployer.execute_command(f"rm {remote_script}")
    deployer.disconnect()
    os.remove('check_posts.php')

if __name__ == "__main__":
    check_posts_remotely("dadudekc.com")
    # check_posts_remotely("freerideinvestor.com")

