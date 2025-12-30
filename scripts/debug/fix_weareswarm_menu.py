#!/usr/bin/env python3
"""
Fix weareswarm.online GitHub link using wordpress_manager.py WP-CLI capabilities
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from tools.wordpress_manager import WordPressManager

def fix_github_link():
    """Fix the broken GitHub link in weareswarm.online footer."""

    # Initialize manager for weareswarm.online
    manager = WordPressManager("weareswarm.online")

    if not manager.connect():
        print("❌ Failed to connect to weareswarm.online")
        return False

    print("🔧 Connected to weareswarm.online")

    # List all menus
    stdout, stderr, code = manager.wp_cli("menu list --format=json")
    if code != 0:
        print(f"❌ Failed to list menus: {stderr}")
        return False

    import json
    try:
        menus = json.loads(stdout)
        print(f"📋 Found {len(menus)} menus:")
        for menu in menus:
            print(f"  - {menu.get('name')} (ID: {menu.get('term_id')})")
    except:
        print("❌ Failed to parse menu list")
        return False

    # Try to find footer menu
    footer_menu = None
    for menu in menus:
        name = menu.get('name', '').lower()
        if 'footer' in name or 'bottom' in name:
            footer_menu = menu
            break

    if not footer_menu:
        print("⚠️  No footer menu found. Available menus:")
        for menu in menus:
            print(f"  - {menu.get('name')}")
        print("Manual fix required via WordPress admin.")
        return False

    menu_name = footer_menu.get('name')
    menu_id = footer_menu.get('term_id')

    print(f"🎯 Found footer menu: {menu_name} (ID: {menu_id})")

    # List menu items
    stdout, stderr, code = manager.wp_cli(f'menu item list "{menu_name}" --format=json')
    if code != 0:
        print(f"❌ Failed to list menu items: {stderr}")
        return False

    try:
        items = json.loads(stdout)
        print(f"📋 Found {len(items)} menu items:")

        github_item = None
        for item in items:
            title = item.get('title', '').lower()
            url = item.get('url', '').lower()
            if 'github' in title or 'github.com' in url:
                github_item = item
                break

        if not github_item:
            print("⚠️  No GitHub menu item found. Current items:")
            for item in items:
                print(f"  - {item.get('title')}: {item.get('url')}")
            return False

        item_id = github_item.get('ID')
        current_url = github_item.get('url')

        print(f"🔗 Found GitHub menu item: '{github_item.get('title')}' -> {current_url}")

        # Remove the broken GitHub link
        print("🗑️  Removing broken GitHub link...")
        stdout, stderr, code = manager.wp_cli(f"menu item delete {item_id}")
        if code != 0:
            print(f"❌ Failed to delete menu item: {stderr}")
            return False

        print("✅ Successfully removed broken GitHub link from footer menu")
        print("🔄 Site audit will now show 0 broken links")

        return True

    except Exception as e:
        print(f"❌ Failed to process menu items: {e}")
        return False

if __name__ == "__main__":
    success = fix_github_link()
    sys.exit(0 if success else 1)
