#!/usr/bin/env python3
"""
⚠️ DEPRECATED - DO NOT USE

This file is deprecated as part of the SSOT consolidation effort.

REPLACEMENT: mcp_servers/wp_cli_manager_server.py
MIGRATION: Use WP-CLI based management functions instead of direct API calls
DEADLINE: 2026-02-01

For new code, use: mcp_servers/wp_cli_manager_server.py

Original docstring:
WordPress Manager - MCP Server Adapter
======================================

Provides the WordPressManager class expected by the website_manager_server.py MCP server.
This adapter bridges to the UnifiedWordPressManager in the websites repository.

SSOT Domain: web
Author: Agent-7 (Web Development Specialist)
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add websites tools to path
WEBSITES_PATH = Path("D:/websites")
sys.path.insert(0, str(WEBSITES_PATH / "tools"))
sys.path.insert(0, str(WEBSITES_PATH / "ops" / "deployment"))

try:
    from unified_wordpress_manager import UnifiedWordPressManager, DeploymentMethod
    HAS_UNIFIED_MANAGER = True
except ImportError:
    HAS_UNIFIED_MANAGER = False
    UnifiedWordPressManager = None
    DeploymentMethod = None

try:
    from simple_wordpress_deployer import SimpleWordPressDeployer
    HAS_DEPLOYER = True
except ImportError:
    HAS_DEPLOYER = False
    SimpleWordPressDeployer = None


class WordPressManager:
    """
    WordPress Manager adapter for MCP server.
    
    Provides the interface expected by website_manager_server.py:
    - connect() / disconnect() for connection management
    - execute_wp_cli() for WP-CLI command execution
    - create_page(), list_pages(), add_to_menu() for content management
    - deploy_theme(), deploy_plugin_file(), deploy_file() for deployment
    - purge_caches() for cache management
    """
    
    def __init__(self, site_key: str, dry_run: bool = False):
        """
        Initialize WordPress manager for a site.
        
        Args:
            site_key: Site identifier (domain or short key like 'freerideinvestor')
        """
        self.site_key = site_key
        self.dry_run = dry_run
        self.site_domain = self._resolve_site_domain(site_key)
        self._connected = False
        self._unified_manager = None
        self._deployer = None
        
        # Initialize the unified manager if available
        if HAS_UNIFIED_MANAGER:
            try:
                self._unified_manager = UnifiedWordPressManager(self.site_domain)
            except Exception as e:
                print(f"⚠️  UnifiedWordPressManager init warning: {e}")
        
        # Initialize deployer for SFTP operations
        if HAS_DEPLOYER:
            try:
                site_configs = self._load_site_configs()
                self._deployer = SimpleWordPressDeployer(self.site_domain, site_configs)
            except Exception as e:
                print(f"⚠️  SimpleWordPressDeployer init warning: {e}")
    
    def _resolve_site_domain(self, site_key: str) -> str:
        """Resolve short site key to full domain."""
        # Common site key mappings
        site_map = {
            "prismblossom": "prismblossom.com",
            "freerideinvestor": "freerideinvestor.com",
            "tradingrobotplug": "tradingrobotplug.com",
            "ariajet": "ariajet.site",
            "dadudekc": "dadudekc.com",
            "digitaldreamscape": "digitaldreamscapellc.com",
            "southwestsecret": "southwestsecret.com",
            "theformulaic": "theformulaic.com",
            "weareswarm": "weareswarm.online",
        }
        
        # Check if already a domain
        if "." in site_key:
            return site_key
        
        # Look up in map
        return site_map.get(site_key.lower(), site_key)
    
    def _load_site_configs(self) -> Dict:
        """Load site configurations."""
        config_path = WEBSITES_PATH / "configs" / "site_configs.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def connect(self) -> bool:
        """Establish connection to WordPress site."""
        if self._connected:
            return True
        
        if self._deployer:
            try:
                self._connected = self._deployer.connect()
                return self._connected
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                return False
        
        # If no deployer but unified manager exists, consider connected
        if self._unified_manager:
            self._connected = True
            return True
        
        return False
    
    def disconnect(self) -> None:
        """Close connection to WordPress site."""
        if self._deployer and self._connected:
            try:
                self._deployer.disconnect()
            except Exception:
                pass
        self._connected = False
    
    def execute_wp_cli(self, command: str) -> Dict[str, Any]:
        """
        Execute WP-CLI command on the WordPress site.
        
        Args:
            command: WP-CLI command (without 'wp' prefix)
            
        Returns:
            Dict with 'success' and 'output' keys
        """
        if not self._connected:
            return {"success": False, "output": "Not connected"}
        
        if self.dry_run:
            return {"success": True, "output": f"[DRY RUN] Would execute: wp {command}"}
        
        if self._deployer and hasattr(self._deployer, 'execute_command'):
            try:
                # Get remote path for WP-CLI execution
                remote_path = getattr(self._deployer, 'remote_path', '')
                if not remote_path:
                    remote_path = f"domains/{self.site_domain}/public_html"
                
                # Execute WP-CLI command via SSH
                full_command = f"cd {remote_path} && wp {command} --allow-root"
                output = self._deployer.execute_command(full_command)
                
                # Determine success based on output
                success = output and ("Error" not in output or "Success" in output)
                
                return {"success": success, "output": output or ""}
            except Exception as e:
                return {"success": False, "output": str(e)}
        
        return {"success": False, "output": "No deployer available for WP-CLI execution"}
    
    def create_page(
        self, 
        page_name: str, 
        page_slug: Optional[str] = None,
        template_name: Optional[str] = None
    ) -> bool:
        """Create a WordPress page."""
        if self.dry_run:
            print(f"[DRY RUN] Would create page: {page_name}")
            return True
        
        slug = page_slug or page_name.lower().replace(" ", "-")
        
        # Build WP-CLI command
        cmd = f'post create --post_type=page --post_title="{page_name}" --post_name="{slug}" --post_status=publish'
        
        if template_name:
            # Add template as post meta
            cmd += f' --meta_input=\'{{"_wp_page_template":"{template_name}"}}\''
        
        result = self.execute_wp_cli(cmd)
        return result.get("success", False)
    
    def list_pages(self) -> List[Dict[str, Any]]:
        """List all WordPress pages."""
        result = self.execute_wp_cli("post list --post_type=page --format=json")
        
        if result.get("success") and result.get("output"):
            try:
                pages = json.loads(result["output"])
                return [
                    {
                        "id": p.get("ID"),
                        "title": p.get("post_title", ""),
                        "slug": p.get("post_name", ""),
                        "status": p.get("post_status", "")
                    }
                    for p in pages
                ]
            except json.JSONDecodeError:
                pass
        
        return []
    
    def add_to_menu(self, page_slug: str, menu_text: Optional[str] = None) -> bool:
        """Add a page to the primary WordPress menu."""
        if self.dry_run:
            print(f"[DRY RUN] Would add to menu: {page_slug}")
            return True
        
        # Get primary menu name (usually 'primary' or 'main-menu')
        menu_result = self.execute_wp_cli("menu list --format=json")
        
        menu_name = "primary"  # Default
        if menu_result.get("success") and menu_result.get("output"):
            try:
                menus = json.loads(menu_result["output"])
                if menus:
                    menu_name = menus[0].get("slug", "primary")
            except json.JSONDecodeError:
                pass
        
        # Add page to menu
        text = menu_text or page_slug.replace("-", " ").title()
        cmd = f'menu item add-custom {menu_name} "{text}" "/{page_slug}/"'
        
        result = self.execute_wp_cli(cmd)
        return result.get("success", False)
    
    def deploy_theme(self, local_path: Path, remote_path: str = None) -> bool:
        """Deploy theme files to WordPress site."""
        return self.deploy_file(local_path, remote_path)
    
    def deploy_plugin_file(self, local_path: Path, remote_path: str = None) -> bool:
        """Deploy plugin files to WordPress site."""
        return self.deploy_file(local_path, remote_path)
    
    def deploy_file(self, local_path: Path, remote_path: str = None) -> bool:
        """Deploy a file to WordPress site via SFTP."""
        if self.dry_run:
            print(f"[DRY RUN] Would deploy: {local_path} -> {remote_path}")
            return True
        
        if not self._deployer:
            return False
        
        try:
            return self._deployer.deploy_file(local_path, remote_path)
        except Exception as e:
            print(f"❌ Deploy failed: {e}")
            return False
    
    def purge_caches(self, use_comprehensive_flush: bool = True) -> bool:
        """Purge WordPress caches."""
        if self.dry_run:
            print("[DRY RUN] Would purge caches")
            return True
        
        success = True
        
        # Flush object cache
        result = self.execute_wp_cli("cache flush")
        success = success and result.get("success", False)
        
        if use_comprehensive_flush:
            # Flush transients
            self.execute_wp_cli("transient delete --all")
            
            # Flush rewrite rules
            self.execute_wp_cli("rewrite flush")
        
        return success
    
    # ==================== THEME MANAGEMENT ====================
    
    def activate_theme(self, theme_name: str) -> bool:
        """Activate a WordPress theme."""
        if self._unified_manager:
            return self._unified_manager.activate_theme(theme_name)
        
        result = self.execute_wp_cli(f"theme activate {theme_name}")
        return result.get("success", False)
    
    def list_themes(self) -> List[Dict[str, Any]]:
        """List installed themes."""
        if self._unified_manager:
            return self._unified_manager.list_themes()
        
        result = self.execute_wp_cli("theme list --format=json")
        if result.get("success") and result.get("output"):
            try:
                return json.loads(result["output"])
            except json.JSONDecodeError:
                pass
        return []
    
    # ==================== PLUGIN MANAGEMENT ====================
    
    def activate_plugin(self, plugin_slug: str) -> bool:
        """Activate a WordPress plugin."""
        if self._unified_manager:
            return self._unified_manager.activate_plugin(plugin_slug)
        
        result = self.execute_wp_cli(f"plugin activate {plugin_slug}")
        return result.get("success", False)
    
    def deactivate_plugin(self, plugin_slug: str) -> bool:
        """Deactivate a WordPress plugin."""
        if self._unified_manager:
            return self._unified_manager.deactivate_plugin(plugin_slug)
        
        result = self.execute_wp_cli(f"plugin deactivate {plugin_slug}")
        return result.get("success", False)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List installed plugins."""
        if self._unified_manager:
            return self._unified_manager.list_plugins()
        
        result = self.execute_wp_cli("plugin list --format=json")
        if result.get("success") and result.get("output"):
            try:
                return json.loads(result["output"])
            except json.JSONDecodeError:
                pass
        return []


def main():
    """CLI test interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="WordPress Manager Test")
    parser.add_argument("--site", required=True, help="Site key or domain")
    parser.add_argument("--action", required=True, 
                       choices=["list-themes", "list-plugins", "list-pages", "test-connection"])
    
    args = parser.parse_args()
    
    manager = WordPressManager(site_key=args.site)
    
    if not manager.connect():
        print("❌ Failed to connect")
        return 1
    
    try:
        if args.action == "list-themes":
            themes = manager.list_themes()
            for t in themes:
                print(f"  {t.get('name', 'Unknown')} - {t.get('status', 'Unknown')}")
        
        elif args.action == "list-plugins":
            plugins = manager.list_plugins()
            for p in plugins:
                print(f"  {p.get('name', 'Unknown')} - {p.get('status', 'Unknown')}")
        
        elif args.action == "list-pages":
            pages = manager.list_pages()
            for p in pages:
                print(f"  {p.get('slug', 'Unknown')} - {p.get('title', 'Unknown')}")
        
        elif args.action == "test-connection":
            print(f"✅ Connected to {manager.site_domain}")
    
    finally:
        manager.disconnect()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

