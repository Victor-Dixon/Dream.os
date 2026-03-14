#!/usr/bin/env python3
"""
FreeRideInvestor Menu Diagnostic Script
========================================

Diagnoses menu link issues on freerideinvestor.com
Checks WordPress installation, menu setup, and navigation problems.

Author: Agent-4 (Infrastructure Diagnostic Specialist)
Date: 2026-01-08
"""

import os
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


class FreeRideInvestorMenuDiagnostic:
    """Diagnoses menu and navigation issues."""

    def __init__(self):
        self.site_root = Path("sites/freerideinvestor.com")
        self.wp_root = self.site_root / "wp"
        self.theme_root = self.wp_root / "wp-content" / "themes" / "freerideinvestor-v2"
        self.site_url = "https://freerideinvestor.com"
        self.issues = []

    def run_full_diagnostic(self):
        """Run complete diagnostic suite."""
        print("🔍 FreeRideInvestor Menu Diagnostic")
        print("=" * 50)

        # Check WordPress installation
        self.check_wordpress_installation()

        # Check theme files
        self.check_theme_files()

        # Check menu setup
        self.check_menu_setup()

        # Check pages
        self.check_pages()

        # Check site accessibility
        self.check_site_accessibility()

        # Check menu in theme
        self.check_menu_in_theme()

        # Report findings
        self.report_findings()

    def check_wordpress_installation(self):
        """Check if WordPress is properly installed."""
        print("\n📁 Checking WordPress Installation...")

        required_wp_files = [
            "wp-config.php",
            "wp-admin/index.php",
            "wp-includes/version.php",
            "wp-content/index.php"
        ]

        wp_complete = True
        for wp_file in required_wp_files:
            file_path = self.wp_root / wp_file
            if not file_path.exists():
                self.issues.append(f"❌ Missing WordPress core file: {wp_file}")
                wp_complete = False
            else:
                print(f"✅ Found: {wp_file}")

        if not wp_complete:
            self.issues.append("🚨 WordPress installation appears incomplete - no core files found")
            return False

        # Check if wp-config.php exists in parent directory
        wp_config = self.site_root / "wp-config.php"
        if wp_config.exists():
            print("✅ Found wp-config.php in site root")
        else:
            self.issues.append("⚠️ wp-config.php not found - WordPress may not be configured")

        return True

    def check_theme_files(self):
        """Check theme files and structure."""
        print("\n🎨 Checking Theme Files...")

        required_theme_files = [
            "functions.php",
            "header.php",
            "footer.php",
            "index.php",
            "style.css",
            "js/theme.js"
        ]

        theme_complete = True
        for theme_file in required_theme_files:
            file_path = self.theme_root / theme_file
            if not file_path.exists():
                self.issues.append(f"❌ Missing theme file: {theme_file}")
                theme_complete = False
            else:
                print(f"✅ Found: {theme_file}")

        # Check page templates
        page_templates = [
            "page-about.php",
            "page-services.php",
            "page-resources.php",
            "page-blog.php",
            "page-contact.php",
            "page-trading-strategies.php"
        ]

        for template in page_templates:
            file_path = self.theme_root / template
            if file_path.exists():
                print(f"✅ Page template: {template}")
            else:
                self.issues.append(f"❌ Missing page template: {template}")
                theme_complete = False

        return theme_complete

    def check_menu_setup(self):
        """Check menu setup script and configuration."""
        print("\n🍽️ Checking Menu Setup...")

        menu_setup_script = self.theme_root / "freerideinvestor-menu-setup.php"
        if menu_setup_script.exists():
            print("✅ Menu setup script exists")

            # Check if script has required functions
            with open(menu_setup_script, 'r') as f:
                content = f.read()

            required_functions = [
                "freerideinvestor_setup_pages_and_menu",
                "FreeRideInvestor_Nav_Walker"
            ]

            for func in required_functions:
                if func in content:
                    print(f"✅ Menu function found: {func}")
                else:
                    self.issues.append(f"❌ Missing menu function: {func}")
        else:
            self.issues.append("❌ Menu setup script not found")

    def check_pages(self):
        """Check if pages exist and are properly configured."""
        print("\n📄 Checking Pages...")

        # For now, just check if templates exist (can't check WP database without WP-CLI)
        expected_pages = [
            "about",
            "services",
            "resources",
            "blog",
            "contact",
            "trading-strategies"
        ]

        print("Note: Cannot check actual WordPress pages without WP-CLI access")
        print("Expected pages:", ", ".join(expected_pages))

    def check_site_accessibility(self):
        """Check if the site is accessible."""
        print("\n🌐 Checking Site Accessibility...")

        try:
            # Try to access the site
            response = urlopen(self.site_url, timeout=10)
            if response.status == 200:
                print(f"✅ Site accessible: {self.site_url} (Status: {response.status})")

                # Try to access homepage
                homepage_url = f"{self.site_url}/"
                homepage_response = urlopen(homepage_url, timeout=10)
                if homepage_response.status == 200:
                    print("✅ Homepage loads successfully")
                else:
                    self.issues.append(f"❌ Homepage error: Status {homepage_response.status}")

            else:
                self.issues.append(f"❌ Site not accessible: Status {response.status}")

        except URLError as e:
            self.issues.append(f"❌ Site not accessible: {e}")
        except Exception as e:
            self.issues.append(f"❌ Unexpected error accessing site: {e}")

    def check_menu_in_theme(self):
        """Check menu implementation in theme files."""
        print("\n🎭 Checking Menu in Theme...")

        # Check header.php for menu implementation
        header_file = self.theme_root / "header.php"
        if header_file.exists():
            with open(header_file, 'r') as f:
                header_content = f.read()

            if 'wp_nav_menu' in header_content:
                print("✅ Header contains wp_nav_menu call")

                if 'FreeRideInvestor_Nav_Walker' in header_content:
                    print("✅ Header uses custom nav walker")
                else:
                    self.issues.append("⚠️ Header does not use custom nav walker")

                if "theme_location' => 'primary'" in header_content:
                    print("✅ Header references primary menu location")
                else:
                    self.issues.append("❌ Header does not reference primary menu location")

            else:
                self.issues.append("❌ Header does not contain wp_nav_menu call")
        else:
            self.issues.append("❌ Header file not found")

        # Check functions.php for menu registration
        functions_file = self.theme_root / "functions.php"
        if functions_file.exists():
            with open(functions_file, 'r') as f:
                functions_content = f.read()

            if 'register_nav_menus' in functions_content:
                print("✅ Functions.php registers nav menus")

                if "'primary'" in functions_content:
                    print("✅ Primary menu location registered")
                else:
                    self.issues.append("❌ Primary menu location not registered")

            else:
                self.issues.append("❌ Functions.php does not register nav menus")

            # Check for duplicate menu removal
            if 'freerideinvestor_remove_duplicate_menu_items' in functions_content:
                print("✅ Duplicate menu removal function exists")
            else:
                self.issues.append("⚠️ Duplicate menu removal function not found")

        else:
            self.issues.append("❌ Functions.php not found")

    def report_findings(self):
        """Report diagnostic findings."""
        print("\n" + "=" * 50)
        print("📊 DIAGNOSTIC REPORT")
        print("=" * 50)

        if not self.issues:
            print("✅ No issues found - menu should be working!")
            print("\n💡 If menu links still don't work:")
            print("   1. Check WordPress admin: Appearance → Menus")
            print("   2. Ensure menu is assigned to 'Primary Menu' location")
            print("   3. Verify pages exist and are published")
            print("   4. Check browser console for JavaScript errors")
        else:
            print(f"❌ Found {len(self.issues)} issues:")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")

            print("\n🔧 Recommended fixes:")

            if any("WordPress" in issue and "incomplete" in issue for issue in self.issues):
                print("   🚨 CRITICAL: WordPress installation incomplete")
                print("      - Need full WordPress core installation")
                print("      - Run: wp core download && wp core config")
                print("      - Import database and configure wp-config.php")

            if any("wp-config.php" in issue for issue in self.issues):
                print("   ⚙️ WordPress configuration missing")
                print("      - Create wp-config.php with database credentials")
                print("      - Run: wp core install")

            if any("menu location" in issue.lower() for issue in self.issues):
                print("   🍽️ Menu location issue")
                print("      - In WordPress admin: Appearance → Menus")
                print("      - Assign menu to 'Primary Menu' location")

            if any("pages" in issue.lower() and "exist" in issue.lower() for issue in self.issues):
                print("   📄 Pages missing")
                print("      - Run menu setup script or create pages manually")
                print("      - Check: WordPress Admin → Pages")

        print("\n" + "=" * 50)


def main():
    """Run the diagnostic."""
    diagnostic = FreeRideInvestorMenuDiagnostic()
    diagnostic.run_full_diagnostic()


if __name__ == "__main__":
    main()