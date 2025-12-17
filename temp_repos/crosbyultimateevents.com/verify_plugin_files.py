#!/usr/bin/env python3
"""
Verify Business Plan Plugin Files on Server
===========================================

Checks if all required plugin files exist on the WordPress server.
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
    print("❌ WordPress manager not available")
    sys.exit(1)

# Required plugin files
REQUIRED_FILES = [
    "crosby-business-plan.php",
    "templates/business-plan-display.php",
    "assets/style.css"
]


def verify_plugin_files(site_name: str = "crosbyultimateevents.com"):
    """Verify all required plugin files exist on server."""

    print(f"🔍 Verifying plugin files on {site_name}...\n")

    try:
        manager = WordPressManager(site_name)

        # Connect to ensure SFTP is available
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False

        # Check each required file using SFTP
        missing_files = []
        existing_files = []

        for file_path in REQUIRED_FILES:
            # Construct remote path (same logic as deploy_plugin_file)
            domain = site_name.replace(".com", "").replace(
                ".online", "").replace(".site", "")
            remote_path = f"domains/{domain}.com/public_html/wp-content/plugins/crosby-business-plan/{file_path}"

            # Use SFTP to check if file exists
            try:
                manager.conn_manager.sftp.stat(remote_path)
                print(f"   ✅ {file_path}")
                existing_files.append(file_path)
            except FileNotFoundError:
                print(f"   ❌ {file_path} - MISSING")
                print(f"      Checked: {remote_path}")
                missing_files.append(file_path)
            except Exception as e:
                print(f"   ⚠️  {file_path} - Error checking: {e}")
                missing_files.append(file_path)

        print(f"\n📊 Summary:")
        print(f"   Found: {len(existing_files)}/{len(REQUIRED_FILES)} files")

        if missing_files:
            print(f"\n❌ Missing files ({len(missing_files)}):")
            for file in missing_files:
                print(f"   - {file}")
            print(f"\n💡 Solution: Redeploy the plugin:")
            print(
                f"   python temp_repos/crosbyultimateevents.com/deploy_business_plan_plugin.py --site {site_name}")
            return False
        else:
            print(f"\n✅ All required files are present!")
            print(f"\n💡 If the plugin still doesn't work, check:")
            print(f"   1. Plugin is activated in WordPress Admin → Plugins")
            print(f"   2. Shortcode syntax: [crosby_business_plan]")
            print(f"   3. Clear WordPress cache")
            return True

    except Exception as e:
        print(f"❌ Error verifying files: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify Business Plan Plugin Files")
    parser.add_argument(
        "--site",
        default="crosbyultimateevents.com",
        help="WordPress site name"
    )

    args = parser.parse_args()
    success = verify_plugin_files(args.site)
    sys.exit(0 if success else 1)
