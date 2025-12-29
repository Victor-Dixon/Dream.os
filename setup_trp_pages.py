import sys
from pathlib import Path
import os
import json

# Add project root to path
sys.path.insert(0, "D:/Agent_Cellphone_V2_Repository")
sys.path.insert(0, "D:/websites")

from ops.deployment.simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

def execute_wp_cli(deployer, command):
    remote_path = deployer.remote_path
    full_command = f"cd {remote_path} && wp {command} --allow-root"
    return deployer.execute_command(full_command)

def setup_trp_pages():
    site_key = "tradingrobotplug.com"
    configs = load_site_configs()
    deployer = SimpleWordPressDeployer(site_key, configs)
    
    if not deployer.connect():
        print(f"❌ Failed to connect to {site_key}")
        return False
    
    pages = [
        {"name": "Waitlist", "slug": "waitlist", "template": "page-waitlist.php"},
        {"name": "Thank You", "slug": "thank-you", "template": "page-thank-you.php"},
        {"name": "Pricing", "slug": "pricing", "template": "page-pricing.php"},
        {"name": "Features", "slug": "features", "template": "page-features.php"},
        {"name": "AI Swarm", "slug": "ai-swarm", "template": "page-ai-swarm.php"},
        {"name": "Blog", "slug": "blog", "template": "page-blog.php"},
    ]
    
    print(f"🚀 Creating 6 pages for {site_key}...")
    
    for page in pages:
        print(f"📄 Creating page: {page['name']} ({page['slug']})...", end=" ")
        # Check if page exists
        check_cmd = f"post list --post_type=page --name='{page['slug']}' --format=ids"
        post_id = execute_wp_cli(deployer, check_cmd).strip()
        
        if post_id:
            print(f"EXISTS (ID: {post_id})")
        else:
            create_cmd = f"post create --post_type=page --post_title='{page['name']}' --post_name='{page['slug']}' --post_status=publish --porcelain"
            post_id = execute_wp_cli(deployer, create_cmd).strip()
            if post_id and post_id.isdigit():
                print(f"✅ CREATED (ID: {post_id})")
            else:
                print(f"❌ FAILED: {post_id}")
                continue
        
        # Set template meta
        print(f"   🛠️  Setting template {page['template']}...", end=" ")
        meta_cmd = f"post meta update {post_id} _wp_page_template {page['template']}"
        meta_res = execute_wp_cli(deployer, meta_cmd)
        print("✅")

    # Configure Menu
    print(f"\n🍴 Configuring Menu...")
    # Get primary menu
    menu_list_cmd = "menu list --format=json"
    menus_json = execute_wp_cli(deployer, menu_list_cmd)
    try:
        menus = json.loads(menus_json)
        if not menus:
            print("⚠️  No menus found. Creating 'Primary' menu...")
            execute_wp_cli(deployer, "menu create 'Primary'")
            menu_slug = "primary"
        else:
            menu_slug = menus[0]['slug']
            for m in menus:
                if 'primary' in m['slug'] or 'main' in m['slug']:
                    menu_slug = m['slug']
                    break
            print(f"✅ Found menu: {menu_slug}")
    except:
        print("⚠️  Failed to parse menus. Assuming 'primary'...")
        menu_slug = "primary"

    for page in pages:
        print(f"   🔗 Adding {page['name']} to menu...", end=" ")
        # Get page ID again to be sure
        get_id_cmd = f"post list --post_type=page --name='{page['slug']}' --field=ID"
        pid = execute_wp_cli(deployer, get_id_cmd).strip()
        
        if pid:
            add_menu_cmd = f"menu item add-post {menu_slug} {pid}"
            add_res = execute_wp_cli(deployer, add_menu_cmd)
            if "Success" in add_res:
                print("✅")
            else:
                print(f"❌ {add_res.strip()}")
        else:
            print("❌ (ID not found)")

    deployer.disconnect()
    print("\n✅ Task completed!")

if __name__ == "__main__":
    setup_trp_pages()

