#!/usr/bin/env python3
"""
Deploy Business Plan Plugin to WordPress
=========================================

Deploys the Crosby Business Plan plugin to the WordPress site.
Uses WordPress Manager with plugin deployment support.

Usage:
    python deploy_business_plan_plugin.py
    python deploy_business_plan_plugin.py --site crosbyultimateevents.com
    python deploy_business_plan_plugin.py --dry-run
"""

import sys
from pathlib import Path

# Add tools to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "tools"))

try:
    from wordpress_manager import WordPressManager
    HAS_WP_MANAGER = True
except ImportError:
    HAS_WP_MANAGER = False
    print("Warning: wordpress_manager not available")

# Plugin configuration
PLUGIN_NAME = "crosby-business-plan"
PLUGIN_DIR = Path(__file__).parent / "wordpress-plugins" / PLUGIN_NAME
PLUGIN_FILES = [
    "crosby-business-plan.php",
    "assets/style.css",
    "templates/business-plan-display.php",
    "README.md",
    "INSTALLATION.md"
]


def deploy_plugin(site_name: str = "crosbyultimateevents.com", dry_run: bool = False):
    """Deploy the business plan plugin to WordPress."""
    
    if not HAS_WP_MANAGER:
        print("❌ WordPress manager not available")
        print("💡 Manual deployment instructions:")
        print(f"   1. Upload {PLUGIN_DIR} to /wp-content/plugins/")
        print("   2. Activate plugin in WordPress Admin")
        return False
    
    # Check if plugin directory exists
    if not PLUGIN_DIR.exists():
        print(f"❌ Plugin directory not found: {PLUGIN_DIR}")
        return False
    
    print(f"🚀 Deploying Business Plan Plugin to {site_name}...")
    print(f"📁 Plugin directory: {PLUGIN_DIR}")
    print(f"📦 Plugin name: {PLUGIN_NAME}")
    
    if dry_run:
        print("🔍 DRY-RUN MODE: No changes will be made")
    
    try:
        manager = WordPressManager(site_name, dry_run=dry_run)
        files_deployed = manager.deploy_plugin(PLUGIN_NAME, auto_flush_cache=True)
        
        if files_deployed > 0:
            print(f"\n✅ Successfully deployed {files_deployed} plugin files!")
            print("\n📋 Next steps:")
            print("   1. Go to WordPress Admin → Plugins")
            print(f"   2. Find 'Crosby Ultimate Events - Business Plan'")
            print("   3. Click 'Activate'")
            print("   4. Add shortcode [crosby_business_plan] to any page")
            return True
        else:
            print("❌ No files were deployed. Check plugin directory and credentials.")
            return False
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"💡 Make sure plugin exists at: {PLUGIN_DIR}")
        return False
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        print("\n💡 Alternative: Use WordPress Manager directly:")
        print(f"   python tools/wordpress_manager.py --site {site_name} --deploy-plugin {PLUGIN_NAME}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy Business Plan Plugin")
    parser.add_argument(
        "--site",
        default="crosbyultimateevents.com",
        help="WordPress site name"
    )
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="List plugin files to deploy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry-run mode: simulate deployment without making changes"
    )
    
    args = parser.parse_args()
    
    if args.list_files:
        print("📦 Plugin Files:")
        for file in PLUGIN_FILES:
            file_path = PLUGIN_DIR / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"   ✅ {file} ({size:,} bytes)")
            else:
                print(f"   ❌ {file} (missing)")
        
        # Count total files
        total_files = sum(1 for _ in PLUGIN_DIR.rglob("*") if _.is_file())
        print(f"\n📊 Total files in plugin: {total_files}")
    else:
        deploy_plugin(args.site, dry_run=args.dry_run)

