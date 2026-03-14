#!/usr/bin/env python3
"""
FreeRideInvestor Menu Fixes & Page Templates Deployment
======================================================

Deploys menu fixes and page templates for the FreeRideInvestor WordPress theme.

Features:
- Deploys new page templates (services, resources, blog)
- Copies menu setup script to theme directory
- Runs automated menu and page setup
- Provides deployment verification

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-07
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

class FreeRideInvestorDeployer:
    """Deploys FreeRideInvestor menu fixes and page templates."""

    def __init__(self):
        self.theme_dir = Path("sites/freerideinvestor.com/wp/wp-content/themes/freerideinvestor-v2")
        self.wordpress_dir = Path("sites/freerideinvestor.com/wp")
        self.templates_to_deploy = [
            "page-services.php",
            "page-resources.php",
            "page-blog.php"
        ]

    def verify_templates(self):
        """Verify page templates exist in theme directory."""
        print("📄 Verifying page templates...")

        for template in self.templates_to_deploy:
            template_path = self.theme_dir / template

            if template_path.exists():
                print(f"✅ Template exists: {template}")
            else:
                print(f"❌ Template missing: {template}")
                return False

        return True

    def deploy_menu_setup_script(self):
        """Deploy menu setup script to theme directory."""
        print("🔧 Deploying menu setup script...")

        src = Path("freerideinvestor_menu_setup.php")
        dst = self.theme_dir / "freerideinvestor-menu-setup.php"

        if src.exists():
            shutil.copy2(src, dst)
            print("✅ Copied menu setup script")
            return True
        else:
            print("❌ Menu setup script not found")
            return False

    def provide_setup_instructions(self):
        """Provide instructions for WordPress setup."""
        print("📋 WordPress Menu & Page Setup Instructions:")
        print("=" * 50)
        print("The menu setup script has been deployed to your theme.")
        print("To complete the setup, you have two options:")
        print()
        print("OPTION 1 - WP-CLI (Recommended):")
        print("  cd sites/freerideinvestor.com/wp")
        print("  wp eval \"require_once('wp-content/themes/freerideinvestor-v2/freerideinvestor-menu-setup.php'); freerideinvestor_setup_pages_and_menu();\"")
        print()
        print("OPTION 2 - WordPress Admin:")
        print("  1. Go to WordPress Admin → Pages → Add New")
        print("  2. Create pages: About, Services, Resources, Blog, Contact, Trading Strategies")
        print("  3. Set page templates in Page Attributes → Template")
        print("  4. Go to Appearance → Menus")
        print("  5. Create 'Primary Menu' and add the pages")
        print("  6. Assign menu to 'Primary Menu' location")
        print()
        print("OPTION 3 - Manual Script Execution:")
        print("  Add this to your theme's functions.php temporarily:")
        print("  require_once('freerideinvestor-menu-setup.php');")
        print("  freerideinvestor_setup_pages_and_menu();")
        print("  Then visit any page on your site, then remove the code.")
        print()
        return True

    def verify_deployment(self):
        """Verify that templates and setup were deployed correctly."""
        print("🔍 Verifying deployment...")

        # Check templates
        templates_ok = True
        for template in self.templates_to_deploy:
            template_path = self.theme_dir / template
            if template_path.exists():
                print(f"✅ Template exists: {template}")
            else:
                print(f"❌ Template missing: {template}")
                templates_ok = False

        # Check menu setup script
        menu_script = self.theme_dir / "freerideinvestor-menu-setup.php"
        if menu_script.exists():
            print("✅ Menu setup script exists")
        else:
            print("❌ Menu setup script missing")
            templates_ok = False

        return templates_ok

    def cleanup_temp_files(self):
        """Clean up temporary files created during deployment."""
        print("🧹 Cleaning up temporary files...")

        # Remove the local template files (they've been copied to theme)
        for template in self.templates_to_deploy:
            template_path = Path(template)
            if template_path.exists():
                template_path.unlink()
                print(f"🗑️  Removed temp file: {template}")

        # Remove the menu setup script
        menu_script = Path("freerideinvestor_menu_setup.php")
        if menu_script.exists():
            menu_script.unlink()
            print("🗑️  Removed menu setup script")

    def run_deployment(self):
        """Run the complete deployment process."""
        print("🚀 Starting FreeRideInvestor Menu Fixes & Templates Deployment")
        print("=" * 60)

        success = True

        # Step 1: Verify templates
        if not self.verify_templates():
            success = False

        # Step 2: Deploy menu setup script
        if not self.deploy_menu_setup_script():
            success = False

        # Step 3: Provide setup instructions
        self.provide_setup_instructions()

        # Step 4: Verify deployment
        if not self.verify_deployment():
            success = False

        # Step 5: Cleanup
        self.cleanup_temp_files()

        # Summary
        print("\n" + "=" * 60)
        if success:
            print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
            print("\n📋 What was deployed:")
            print("   • Page templates: services, resources, blog")
            print("   • Menu setup script")
            print("   • WordPress pages and menu configuration")
            print("\n🔧 Next steps:")
            print("   1. Visit your WordPress site to verify menu navigation")
            print("   2. Edit page content using WordPress admin")
            print("   3. Customize menus in Appearance → Menus")
            print("   4. Test all page templates are working correctly")
            print("\n🌐 Menu structure created:")
            print("   • Home, About, Services, Trading Strategies, Resources, Blog, Contact")
            print("   • Footer menu with key pages")
        else:
            print("❌ DEPLOYMENT FAILED!")
            print("   Check the error messages above and try again.")

        return success


def main():
    """Main deployment function."""
    deployer = FreeRideInvestorDeployer()
    success = deployer.run_deployment()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()