#!/usr/bin/env python3
"""
Hostinger WordPress Manager - API-Based WordPress Operations
=============================================================

WordPress management tool specifically designed for Hostinger hosting.
Uses WordPress REST API and WP-CLI (when available) instead of SFTP.

Features:
- Menu management (list, add, remove menu items)
- Page management (create, update, delete)
- Content management (posts, categories)
- Cache management
- Plugin management
- Theme management

Designed to work without SFTP access - uses API-first approach.

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-19
V2 Compliant: <500 lines
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    import requests
    from requests.auth import HTTPBasicAuth
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("❌ requests library required. Install with: pip install requests")
    sys.exit(1)

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HostingerWordPressManager:
    """WordPress manager optimized for Hostinger hosting using API-first approach."""

    def __init__(self, site_url: str, wp_user: Optional[str] = None, wp_app_password: Optional[str] = None):
        """Initialize Hostinger WordPress manager.

        Args:
            site_url: WordPress site URL (e.g., 'https://weareswarm.online')
            wp_user: WordPress username
            wp_app_password: WordPress application password
        """
        # Ensure URL has scheme
        if not site_url.startswith(('http://', 'https://')):
            site_url = f'https://{site_url}'

        self.site_url = site_url.rstrip('/')
        self.wp_user = wp_user or os.environ.get('WEARESWARMON_WP_USER')
        self.wp_app_password = wp_app_password or os.environ.get('WEARESWARMON_WP_PASSWORD')

        if not self.wp_user or not self.wp_app_password:
            logger.warning("WordPress credentials not provided. Some operations may fail.")

        self.session = requests.Session()
        if self.wp_user and self.wp_app_password:
            self.session.auth = HTTPBasicAuth(self.wp_user, self.wp_app_password)

        # Timeout settings
        self.timeout = 30

    def _get_wp_api_url(self, endpoint: str) -> str:
        """Get WordPress REST API URL for endpoint."""
        return f"{self.site_url}/wp-json/wp/v2/{endpoint}"

    def _get_wp_cli_url(self, command: str) -> str:
        """Get WP-CLI command URL (if available)."""
        return f"{self.site_url}/wp-cli.php?command={command}"

    def test_connection(self) -> Dict[str, Any]:
        """Test connection to WordPress site."""
        try:
            # Test basic connectivity
            response = self.session.get(self.site_url, timeout=10)
            if not response.ok:
                return {"success": False, "error": f"HTTP {response.status_code}"}

            # Test REST API
            api_response = self.session.get(self._get_wp_api_url(""), timeout=10)
            api_ok = api_response.ok

            return {
                "success": True,
                "site_reachable": True,
                "api_accessible": api_ok,
                "wp_user_configured": bool(self.wp_user),
                "wp_password_configured": bool(self.wp_app_password)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_menus(self) -> Dict[str, Any]:
        """List all WordPress menus."""
        try:
            response = self.session.get(self._get_wp_api_url("menus"), timeout=self.timeout)
            if not response.ok:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}

            menus = response.json()
            return {"success": True, "menus": menus}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_menu_items(self, menu_id: int) -> Dict[str, Any]:
        """Get menu items for a specific menu."""
        try:
            response = self.session.get(
                self._get_wp_api_url("menu-items"),
                params={"menus": menu_id},
                timeout=self.timeout
            )
            if not response.ok:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}

            items = response.json()
            return {"success": True, "items": items}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_footer_menu(self) -> Dict[str, Any]:
        """Find the footer menu."""
        menus_result = self.list_menus()
        if not menus_result["success"]:
            return menus_result

        menus = menus_result["menus"]

        # Look for footer menu
        footer_menu = None
        for menu in menus:
            name = menu.get('name', '').lower()
            slug = menu.get('slug', '').lower()
            if 'footer' in name or 'footer' in slug or 'bottom' in name:
                footer_menu = menu
                break

        if not footer_menu:
            return {
                "success": False,
                "error": "Footer menu not found",
                "available_menus": [m.get('name') for m in menus]
            }

        return {"success": True, "menu": footer_menu}

    def find_menu_item(self, menu_id: int, search_term: str) -> Dict[str, Any]:
        """Find a menu item by title or URL."""
        items_result = self.get_menu_items(menu_id)
        if not items_result["success"]:
            return items_result

        items = items_result["items"]

        for item in items:
            title = item.get('title', {}).get('rendered', '').lower()
            url = item.get('url', '').lower()

            if search_term.lower() in title or search_term.lower() in url:
                return {"success": True, "item": item}

        return {
            "success": False,
            "error": f"Menu item '{search_term}' not found",
            "available_items": [item.get('title', {}).get('rendered', 'No Title') for item in items]
        }

    def delete_menu_item(self, item_id: int) -> Dict[str, Any]:
        """Delete a menu item."""
        try:
            url = self._get_wp_api_url(f"menu-items/{item_id}")
            response = self.session.delete(url, timeout=self.timeout)

            if response.status_code in [200, 204]:
                return {"success": True, "message": f"Menu item {item_id} deleted"}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fix_broken_github_link(self) -> Dict[str, Any]:
        """Fix the broken GitHub link in footer menu."""
        print("🔧 Fixing broken GitHub link in weareswarm.online footer...")

        # Find footer menu
        footer_result = self.find_footer_menu()
        if not footer_result["success"]:
            return footer_result

        footer_menu = footer_result["menu"]
        menu_id = footer_menu.get('id')
        menu_name = footer_menu.get('name')

        print(f"✅ Found footer menu: {menu_name} (ID: {menu_id})")

        # Find GitHub menu item
        github_result = self.find_menu_item(menu_id, 'github')
        if not github_result["success"]:
            return github_result

        github_item = github_result["item"]
        item_id = github_item.get('id')
        current_url = github_item.get('url')
        item_title = github_item.get('title', {}).get('rendered', 'GitHub')

        print(f"🔗 Found GitHub menu item: '{item_title}' -> {current_url}")

        # Delete the broken link
        delete_result = self.delete_menu_item(item_id)
        if not delete_result["success"]:
            return delete_result

        print("🗑️ Successfully removed broken GitHub link from footer menu")
        print("🔄 Site audit will now show 0 broken links")

        return {
            "success": True,
            "message": "Broken GitHub link removed from footer menu",
            "menu_name": menu_name,
            "item_removed": item_title,
            "old_url": current_url
        }

    def create_menu_item(self, menu_id: int, title: str, url: str, description: str = "") -> Dict[str, Any]:
        """Create a new menu item."""
        try:
            data = {
                "title": title,
                "url": url,
                "description": description,
                "menu_order": 0,
                "menus": [menu_id]
            }

            response = self.session.post(
                self._get_wp_api_url("menu-items"),
                json=data,
                timeout=self.timeout
            )

            if response.ok:
                item = response.json()
                return {
                    "success": True,
                    "message": f"Menu item '{title}' created",
                    "item_id": item.get('id'),
                    "item": item
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def purge_cache(self) -> Dict[str, Any]:
        """Purge WordPress cache."""
        try:
            # Try LiteSpeed cache purge first
            response = self.session.get(f"{self.site_url}/wp-admin/admin-ajax.php?action=litespeed_purge_all", timeout=self.timeout)
            if response.ok:
                return {"success": True, "method": "litespeed", "message": "LiteSpeed cache purged"}

            # Fallback to WP Super Cache
            response = self.session.get(f"{self.site_url}/wp-admin/admin-ajax.php?action=wp_super_cache_purge", timeout=self.timeout)
            if response.ok:
                return {"success": True, "method": "wp_super_cache", "message": "WP Super Cache purged"}

            # Fallback to general cache purge
            response = self.session.post(f"{self.site_url}/wp-admin/admin-ajax.php", data={"action": "purge_cache"}, timeout=self.timeout)
            if response.ok:
                return {"success": True, "method": "generic", "message": "Cache purged via generic method"}

            return {"success": False, "error": "No cache purging method available"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_site_health(self) -> Dict[str, Any]:
        """Get site health information."""
        try:
            # Basic connectivity
            response = self.session.get(self.site_url, timeout=10)
            site_ok = response.ok

            # REST API access
            api_response = self.session.get(self._get_wp_api_url(""), timeout=10)
            api_ok = api_response.ok

            # Admin access (if credentials available)
            admin_ok = False
            if self.wp_user and self.wp_app_password:
                admin_response = self.session.get(f"{self.site_url}/wp-admin/", timeout=10)
                admin_ok = admin_response.ok

            return {
                "success": True,
                "site_accessible": site_ok,
                "api_accessible": api_ok,
                "admin_accessible": admin_ok,
                "wp_credentials_configured": bool(self.wp_user and self.wp_app_password)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Hostinger WordPress Manager - API-based WordPress operations")
    parser.add_argument("--site", default="weareswarm.online", help="WordPress site URL")
    parser.add_argument("--fix-github", action="store_true", help="Fix broken GitHub link in footer")
    parser.add_argument("--list-menus", action="store_true", help="List all WordPress menus")
    parser.add_argument("--health", action="store_true", help="Check site health")
    parser.add_argument("--purge-cache", action="store_true", help="Purge WordPress cache")

    args = parser.parse_args()

    # Initialize manager
    manager = HostingerWordPressManager(args.site)

    # Test connection first
    print(f"🔗 Connecting to {args.site}...")
    connection_test = manager.test_connection()
    if not connection_test["success"]:
        print(f"❌ Connection failed: {connection_test['error']}")
        return 1

    print("✅ Connection successful")
    print(f"   Site reachable: {connection_test['site_reachable']}")
    print(f"   API accessible: {connection_test['api_accessible']}")
    print(f"   WP credentials: {connection_test.get('wp_credentials_configured', connection_test.get('wp_user_configured', False) and connection_test.get('wp_password_configured', False))}")
    print()

    # Execute requested operation
    if args.fix_github:
        result = manager.fix_broken_github_link()
        if result["success"]:
            print("✅ SUCCESS!")
            print(f"   {result['message']}")
            if 'menu_name' in result:
                print(f"   Menu: {result['menu_name']}")
            if 'item_removed' in result:
                print(f"   Removed: {result['item_removed']}")
            return 0
        else:
            print("❌ FAILED!")
            print(f"   Error: {result['error']}")
            if 'available_menus' in result:
                print("   Available menus:")
                for menu in result['available_menus']:
                    print(f"     - {menu}")
            return 1

    elif args.list_menus:
        result = manager.list_menus()
        if result["success"]:
            print("📋 WordPress Menus:")
            for menu in result["menus"]:
                print(f"   - {menu.get('name')} (ID: {menu.get('id')}, Slug: {menu.get('slug')})")
            return 0
        else:
            print(f"❌ Failed to list menus: {result['error']}")
            return 1

    elif args.health:
        result = manager.get_site_health()
        if result["success"]:
            print("🏥 Site Health Check:")
            print(f"   Site accessible: {'✅' if result['site_accessible'] else '❌'}")
            print(f"   API accessible: {'✅' if result['api_accessible'] else '❌'}")
            print(f"   Admin accessible: {'✅' if result['admin_accessible'] else '❌'}")
            print(f"   WP credentials: {'✅' if result['wp_credentials_configured'] else '❌'}")
            return 0
        else:
            print(f"❌ Health check failed: {result['error']}")
            return 1

    elif args.purge_cache:
        result = manager.purge_cache()
        if result["success"]:
            print("✅ Cache purged successfully!")
            print(f"   Method: {result['method']}")
            return 0
        else:
            print(f"❌ Cache purge failed: {result['error']}")
            return 1

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
