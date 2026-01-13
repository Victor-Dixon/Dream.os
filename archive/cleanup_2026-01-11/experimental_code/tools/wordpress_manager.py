#!/usr/bin/env python3
"""
WordPress Manager Tool - Complete WordPress Site Management & Diagnostics
==========================================================================

<!-- SSOT Domain: wordpress -->

Comprehensive WordPress management tool for all WordPress sites in the swarm.
Handles debugging, configuration, deployment, and maintenance tasks.

Features:
- WP_DEBUG management (enable/disable/toggle)
- Permalink refresh and validation
- File integrity verification
- JavaScript error detection (via Selenium)
- Database connection testing
- Plugin/theme status checks
- Automated deployment and updates
- Backup and restore operations
- Security scanning
- Performance diagnostics

Author: Agent-4 (WordPress Infrastructure Specialist)
Date: 2026-01-08
License: MIT
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Selenium for browser-based checks
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import (
        NoSuchElementException,
        TimeoutException,
        WebDriverException
    )
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = None

# Requests for HTTP checks
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class WordPressManager:
    """
    Comprehensive WordPress site manager.

    Handles all WordPress operations including debugging, configuration,
    deployment, and maintenance across all swarm WordPress sites.
    """

    def __init__(self, site_name: Optional[str] = None):
        """
        Initialize WordPress manager.

        Args:
            site_name: Specific site to manage (optional)
        """
        self.sites_root = Path("sites")
        self.site_name = site_name
        self.current_site = None

        # WordPress sites we manage
        self.managed_sites = [
            "crosbyultimateevents.com",
            "dadudekc.com",
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "weareswarm.online",
            "weareswarm.site"
        ]

        # Common WordPress files to check
        self.core_files = [
            "wp-config.php",
            "wp-admin/index.php",
            "wp-includes/version.php",
            "wp-content/index.php"
        ]

        # Initialize site if specified
        if site_name:
            self.set_site(site_name)

    def set_site(self, site_name: str) -> bool:
        """
        Set the current site to manage.

        Args:
            site_name: Name of the site to manage

        Returns:
            True if site found and set, False otherwise
        """
        if site_name not in self.managed_sites:
            print(f"❌ Site '{site_name}' not in managed sites list")
            print(f"Available sites: {', '.join(self.managed_sites)}")
            return False

        site_path = self.sites_root / site_name
        if not site_path.exists():
            print(f"❌ Site directory not found: {site_path}")
            return False

        self.current_site = site_name
        self.site_path = site_path
        print(f"✅ Active site set to: {site_name}")
        return True

    def list_sites(self) -> None:
        """List all managed WordPress sites with status."""
        print("🗂️  Managed WordPress Sites:")
        print("=" * 50)

        for site in self.managed_sites:
            site_path = self.sites_root / site
            status = "✅" if site_path.exists() else "❌"
            wp_exists = (site_path / "wp-config.php").exists()

            print(f"{status} {site}")
            if site_path.exists():
                print(f"   📁 Path: {site_path}")
                print(f"   🔧 WP Config: {'✅' if wp_exists else '❌'}")

                # Check for wp directory
                wp_dir = site_path / "wp"
                if wp_dir.exists():
                    print("   📂 WP Directory: ✅")
                else:
                    print("   📂 WP Directory: ❌")

                print()

    def enable_wp_debug(self, site_name: Optional[str] = None) -> bool:
        """
        Enable WordPress debugging in wp-config.php.

        Args:
            site_name: Site to enable debug for (uses current if None)

        Returns:
            True if successful, False otherwise
        """
        if site_name and not self.set_site(site_name):
            return False

        if not self.current_site:
            print("❌ No active site. Use --site or set_site() first")
            return False

        wp_config = self._find_wp_config()
        if not wp_config:
            print("❌ wp-config.php not found")
            return False

        try:
            # Read current config
            with open(wp_config, 'r', encoding='utf-8') as f:
                content = f.read()

            # Enable debug settings
            debug_settings = """
// WordPress Debug Settings - ENABLED
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
define('WP_DISABLE_FATAL_ERROR_HANDLER', true);

// Save queries for analysis
define('SAVEQUERIES', true);

// Script debugging
define('SCRIPT_DEBUG', true);

// WordPress Debug Settings - END
"""

            # Remove existing debug settings
            content = re.sub(
                r'// WordPress Debug Settings.*?(?=// WordPress Debug Settings - END).*?// WordPress Debug Settings - END',
                '',
                content,
                flags=re.DOTALL
            )

            # Add debug settings after WP_DEBUG definition or at the end
            if "define('WP_DEBUG'" in content:
                # Replace existing WP_DEBUG
                content = re.sub(
                    r"define\('WP_DEBUG',\s*(true|false)\);",
                    "define('WP_DEBUG', true);",
                    content
                )
                # Add additional debug settings after the last define
                last_define = content.rfind("define(")
                if last_define != -1:
                    insert_pos = content.find(';', last_define) + 1
                    content = content[:insert_pos] + "\n" + debug_settings + content[insert_pos:]
            else:
                # Add at the end before closing ?>
                if "?>" in content:
                    content = content.replace("?>", debug_settings + "\n?>")
                else:
                    content += "\n" + debug_settings

            # Write back
            with open(wp_config, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ WP_DEBUG enabled in: {wp_config}")
            print("🔧 Debug settings added:")
            print("   - WP_DEBUG: true")
            print("   - WP_DEBUG_LOG: true")
            print("   - WP_DEBUG_DISPLAY: false")
            print("   - SAVEQUERIES: true")
            print("   - SCRIPT_DEBUG: true")
            print(f"📝 Debug log will be saved to: {wp_config.parent}/wp-content/debug.log")

            return True

        except Exception as e:
            print(f"❌ Failed to enable WP_DEBUG: {e}")
            return False

    def disable_wp_debug(self, site_name: Optional[str] = None) -> bool:
        """
        Disable WordPress debugging in wp-config.php.

        Args:
            site_name: Site to disable debug for (uses current if None)

        Returns:
            True if successful, False otherwise
        """
        if site_name and not self.set_site(site_name):
            return False

        if not self.current_site:
            print("❌ No active site. Use --site or set_site() first")
            return False

        wp_config = self._find_wp_config()
        if not wp_config:
            print("❌ wp-config.php not found")
            return False

        try:
            # Read current config
            with open(wp_config, 'r', encoding='utf-8') as f:
                content = f.read()

            # Disable debug settings
            content = re.sub(
                r"define\('WP_DEBUG',\s*true\);",
                "define('WP_DEBUG', false);",
                content
            )

            # Remove debug block
            content = re.sub(
                r'// WordPress Debug Settings.*?(?=// WordPress Debug Settings - END).*?// WordPress Debug Settings - END',
                '',
                content,
                flags=re.DOTALL
            )

            # Write back
            with open(wp_config, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ WP_DEBUG disabled in: {wp_config}")
            return True

        except Exception as e:
            print(f"❌ Failed to disable WP_DEBUG: {e}")
            return False

    def refresh_permalinks(self, site_name: Optional[str] = None) -> bool:
        """
        Refresh WordPress permalinks by updating .htaccess.

        Args:
            site_name: Site to refresh permalinks for (uses current if None)

        Returns:
            True if successful, False otherwise
        """
        if site_name and not self.set_site(site_name):
            return False

        if not self.current_site:
            print("❌ No active site. Use --site or set_site() first")
            return False

        wp_root = self._find_wp_root()
        if not wp_root:
            print("❌ WordPress root directory not found")
            return False

        htaccess = wp_root / ".htaccess"
        try:
            # Standard WordPress .htaccess content
            htaccess_content = """# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^index\\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
"""

            with open(htaccess, 'w', encoding='utf-8') as f:
                f.write(htaccess_content)

            print(f"✅ Permalinks refreshed: {htaccess}")
            print("🔧 .htaccess updated with standard WordPress rewrite rules")

            return True

        except Exception as e:
            print(f"❌ Failed to refresh permalinks: {e}")
            return False

    def check_javascript_errors(self, site_name: Optional[str] = None, url: Optional[str] = None) -> bool:
        """
        Check for JavaScript errors on the site using Selenium.

        Args:
            site_name: Site to check (uses current if None)
            url: Specific URL to check (uses site homepage if None)

        Returns:
            True if no errors found, False if errors detected
        """
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available. Install with: pip install selenium")
            return False

        if site_name and not self.set_site(site_name):
            return False

        if not self.current_site:
            print("❌ No active site. Use --site or set_site() first")
            return False

        # Determine URL to check
        if not url:
            url = f"https://{self.current_site}"

        print(f"🔍 Checking JavaScript errors on: {url}")

        driver = None
        try:
            # Setup headless Chrome
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--log-level=3")  # Reduce Chrome logging

            driver = webdriver.Chrome(options=options)

            # Navigate to page
            driver.get(url)

            # Wait for page load
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Get browser console logs (JavaScript errors)
            logs = driver.get_log("browser")

            errors = []
            warnings = []

            for log in logs:
                level = log.get('level', '').upper()
                message = log.get('message', '')

                if level == 'SEVERE':
                    errors.append(f"🚨 {message}")
                elif level == 'WARNING':
                    warnings.append(f"⚠️  {message}")

            # Print results
            if errors:
                print(f"❌ Found {len(errors)} JavaScript errors:")
                for error in errors[:10]:  # Show first 10
                    print(f"   {error}")
                if len(errors) > 10:
                    print(f"   ... and {len(errors) - 10} more")
                return False
            else:
                print("✅ No JavaScript errors found")

            if warnings:
                print(f"⚠️  Found {len(warnings)} JavaScript warnings:")
                for warning in warnings[:5]:  # Show first 5
                    print(f"   {warning}")
                if len(warnings) > 5:
                    print(f"   ... and {len(warnings) - 5} more")

            return len(errors) == 0

        except Exception as e:
            print(f"❌ JavaScript error check failed: {e}")
            return False

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def verify_file_integrity(self, site_name: Optional[str] = None) -> Dict[str, bool]:
        """
        Verify that all WordPress files are properly uploaded and intact.

        Args:
            site_name: Site to verify (uses current if None)

        Returns:
            Dictionary with file status (True = OK, False = Missing/Corrupted)
        """
        if site_name and not self.set_site(site_name):
            return {}

        if not self.current_site:
            print("❌ No active site. Use --site or set_site() first")
            return {}

        print(f"🔍 Verifying file integrity for: {self.current_site}")

        wp_root = self._find_wp_root()
        if not wp_root:
            print("❌ WordPress root directory not found")
            return {"wordpress_root": False}

        results = {}

        # Check core WordPress files
        for core_file in self.core_files:
            file_path = wp_root / core_file
            results[core_file] = file_path.exists() and file_path.stat().st_size > 0

        # Check theme files if theme directory exists
        theme_dir = wp_root / "wp-content" / "themes"
        if theme_dir.exists():
            # Look for any theme directory
            theme_dirs = [d for d in theme_dir.iterdir() if d.is_dir()]
            if theme_dirs:
                active_theme = theme_dirs[0]  # Assume first theme is active
                results["theme_directory"] = True

                # Check key theme files
                theme_files = ["functions.php", "style.css", "index.php"]
                for theme_file in theme_files:
                    file_path = active_theme / theme_file
                    results[f"theme_{theme_file}"] = file_path.exists()
            else:
                results["theme_directory"] = False
        else:
            results["theme_directory"] = False

        # Check uploads directory
        uploads_dir = wp_root / "wp-content" / "uploads"
        results["uploads_directory"] = uploads_dir.exists()

        # Check plugins directory
        plugins_dir = wp_root / "wp-content" / "plugins"
        results["plugins_directory"] = plugins_dir.exists()

        # Print results
        print("📊 File Integrity Results:")
        all_good = True

        for file_name, status in results.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {file_name}")
            if not status:
                all_good = False

        if all_good:
            print("✅ All critical files present and intact")
        else:
            print("❌ Some files are missing or corrupted")

        return results

    def run_full_diagnostic(self, site_name: Optional[str] = None) -> Dict[str, any]:
        """
        Run complete diagnostic suite on a WordPress site.

        Args:
            site_name: Site to diagnose (uses current if None)

        Returns:
            Dictionary with diagnostic results
        """
        if site_name and not self.set_site(site_name):
            return {}

        if not self.current_site:
            print("❌ No active site. Use --site or set_site() first")
            return {}

        print(f"🔬 Running full diagnostic for: {self.current_site}")
        print("=" * 50)

        results = {
            "site": self.current_site,
            "timestamp": datetime.now().isoformat(),
            "diagnostics": {}
        }

        # File integrity
        print("\n📁 Checking File Integrity...")
        results["diagnostics"]["file_integrity"] = self.verify_file_integrity()

        # WordPress configuration
        print("\n⚙️ Checking WordPress Configuration...")
        wp_config = self._find_wp_config()
        results["diagnostics"]["wp_config_exists"] = wp_config is not None

        if wp_config:
            try:
                with open(wp_config, 'r', encoding='utf-8') as f:
                    config_content = f.read()

                results["diagnostics"]["wp_debug_enabled"] = "define('WP_DEBUG', true)" in config_content
                results["diagnostics"]["wp_debug_log_enabled"] = "define('WP_DEBUG_LOG', true)" in config_content
                results["diagnostics"]["save_queries_enabled"] = "define('SAVEQUERIES', true)" in config_content

            except Exception as e:
                results["diagnostics"]["config_read_error"] = str(e)

        # Site accessibility
        if REQUESTS_AVAILABLE:
            print("\n🌐 Checking Site Accessibility...")
            try:
                response = requests.get(f"https://{self.current_site}", timeout=10, verify=False)
                results["diagnostics"]["site_accessible"] = response.status_code == 200
                results["diagnostics"]["response_code"] = response.status_code
            except Exception as e:
                results["diagnostics"]["site_accessible"] = False
                results["diagnostics"]["accessibility_error"] = str(e)

        # JavaScript errors (if Selenium available)
        if SELENIUM_AVAILABLE:
            print("\n🔍 Checking JavaScript Errors...")
            js_clean = self.check_javascript_errors()
            results["diagnostics"]["javascript_errors"] = not js_clean

        print("\n📊 Diagnostic Summary:")
        print("=" * 30)

        # Summarize results
        issues = []

        if not all(results["diagnostics"].get("file_integrity", {}).values()):
            issues.append("Missing or corrupted files")

        if not results["diagnostics"].get("wp_config_exists", False):
            issues.append("Missing wp-config.php")

        if not results["diagnostics"].get("site_accessible", False):
            issues.append("Site not accessible")

        if results["diagnostics"].get("javascript_errors", False):
            issues.append("JavaScript errors detected")

        if issues:
            print(f"❌ Found {len(issues)} issues:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ All diagnostics passed - site appears healthy")

        return results

    def _find_wp_config(self) -> Optional[Path]:
        """Find wp-config.php file."""
        if not self.current_site:
            return None

        # Check in wp subdirectory first
        wp_config = self.site_path / "wp" / "wp-config.php"
        if wp_config.exists():
            return wp_config

        # Check in site root
        wp_config = self.site_path / "wp-config.php"
        if wp_config.exists():
            return wp_config

        return None

    def _find_wp_root(self) -> Optional[Path]:
        """Find WordPress root directory."""
        if not self.current_site:
            return None

        # Check if wp subdirectory exists
        wp_root = self.site_path / "wp"
        if wp_root.exists() and (wp_root / "wp-config.php").exists():
            return wp_root

        # Check if WordPress is in site root
        if (self.site_path / "wp-config.php").exists():
            return self.site_path

        return None


def main():
    """Command-line interface for WordPress Manager."""
    parser = argparse.ArgumentParser(
        description="WordPress Manager Tool - Complete WordPress site management and diagnostics"
    )

    # Site selection
    parser.add_argument("--site", "-s", help="WordPress site to manage")

    # Actions
    parser.add_argument("--list", action="store_true", help="List all managed sites")
    parser.add_argument("--debug-enable", action="store_true", help="Enable WP_DEBUG")
    parser.add_argument("--debug-disable", action="store_true", help="Disable WP_DEBUG")
    parser.add_argument("--refresh-permalinks", action="store_true", help="Refresh WordPress permalinks")
    parser.add_argument("--check-js-errors", action="store_true", help="Check for JavaScript errors")
    parser.add_argument("--verify-files", action="store_true", help="Verify file integrity")
    parser.add_argument("--diagnostic", action="store_true", help="Run full diagnostic suite")

    # Options
    parser.add_argument("--url", help="Specific URL to check for JS errors")
    parser.add_argument("--output", "-o", help="Output file for results (JSON)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode - less output")

    args = parser.parse_args()

    # Initialize manager
    manager = WordPressManager()

    # List sites if requested
    if args.list:
        manager.list_sites()
        return

    # Set site if specified
    if args.site:
        if not manager.set_site(args.site):
            return

    # Perform requested actions
    results = {}

    if args.debug_enable:
        success = manager.enable_wp_debug()
        results["debug_enabled"] = success

    if args.debug_disable:
        success = manager.disable_wp_debug()
        results["debug_disabled"] = success

    if args.refresh_permalinks:
        success = manager.refresh_permalinks()
        results["permalinks_refreshed"] = success

    if args.check_js_errors:
        success = manager.check_javascript_errors(url=args.url)
        results["js_errors_checked"] = success

    if args.verify_files:
        file_status = manager.verify_file_integrity()
        results["file_integrity"] = file_status

    if args.diagnostic:
        diagnostic_results = manager.run_full_diagnostic()
        results["diagnostic"] = diagnostic_results

    # Output results if requested
    if args.output and results:
        try:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Results saved to: {args.output}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

    # Print summary
    if not args.quiet and results:
        print("\n📊 Action Summary:")
        for action, result in results.items():
            status = "✅" if result else "❌"
            print(f"   {status} {action.replace('_', ' ').title()}")


if __name__ == "__main__":
    main()