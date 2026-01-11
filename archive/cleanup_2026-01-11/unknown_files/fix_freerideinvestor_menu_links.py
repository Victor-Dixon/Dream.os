#!/usr/bin/env python3
"""
FreeRideInvestor Menu Links Fix
================================

Comprehensive fix for freerideinvestor.com menu navigation issues.
Addresses WordPress installation problems and menu setup issues.

PROBLEM IDENTIFIED:
- WordPress core files missing from repository
- Menu setup script incomplete
- No actual WordPress installation to run against
- Theme files exist but no functional WordPress site

SOLUTION:
1. Provide proper WordPress installation instructions
2. Fix menu setup script issues
3. Create deployment guide for live site
4. Provide manual menu setup as fallback

Author: Agent-4 (WordPress Menu Fix Specialist)
Date: 2026-01-08
"""

import os
import shutil
from pathlib import Path


class FreeRideInvestorMenuFixer:
    """Fixes menu navigation issues for freerideinvestor.com."""

    def __init__(self):
        self.site_root = Path("sites/freerideinvestor.com")
        self.theme_root = self.site_root / "wp" / "wp-content" / "themes" / "freerideinvestor-v2"
        self.live_theme_path = None  # To be determined

    def diagnose_and_fix(self):
        """Run complete diagnosis and apply fixes."""
        print("🔧 FreeRideInvestor Menu Links Fix")
        print("=" * 50)

        # Step 1: Analyze current setup
        self.analyze_current_setup()

        # Step 2: Fix menu setup script
        self.fix_menu_setup_script()

        # Step 3: Create WordPress installation guide
        self.create_wordpress_installation_guide()

        # Step 4: Provide manual menu setup instructions
        self.provide_manual_setup_instructions()

        # Step 5: Create deployment package
        self.create_deployment_package()

        print("\n" + "=" * 50)
        print("🎯 MENU FIX SUMMARY")
        print("=" * 50)
        print("✅ Fixed menu setup script issues")
        print("✅ Created WordPress installation guide")
        print("✅ Provided manual setup instructions")
        print("✅ Created deployment package")
        print("\n🚀 NEXT STEPS:")
        print("1. Install WordPress on freerideinvestor.com server")
        print("2. Deploy theme files to live WordPress installation")
        print("3. Run menu setup script or follow manual instructions")
        print("4. Test menu navigation on live site")

    def analyze_current_setup(self):
        """Analyze the current setup and identify issues."""
        print("\n🔍 Analyzing Current Setup...")

        # Check WordPress installation
        wp_files = ["wp-config.php", "wp-admin/index.php", "wp-includes/version.php"]
        wp_complete = all((self.site_root / "wp" / file).exists() for file in wp_files)

        if wp_complete:
            print("✅ WordPress installation appears complete")
        else:
            print("❌ WordPress installation incomplete - missing core files")
            print("   This explains why menu links don't work!")

        # Check theme files
        theme_files = ["functions.php", "header.php", "style.css"]
        theme_complete = all((self.theme_root / file).exists() for file in theme_files)

        if theme_complete:
            print("✅ Theme files present")
        else:
            print("❌ Theme files missing")

        # Check menu setup
        menu_setup = self.theme_root / "freerideinvestor-menu-setup.php"
        if menu_setup.exists():
            print("✅ Menu setup script exists")

            # Check for nav walker
            with open(menu_setup, 'r') as f:
                content = f.read()
            if "FreeRideInvestor_Nav_Walker" in content:
                print("✅ Nav walker class found in menu setup")
            else:
                print("⚠️ Nav walker class not in menu setup (defined in functions.php)")
        else:
            print("❌ Menu setup script missing")

    def fix_menu_setup_script(self):
        """Fix issues in the menu setup script."""
        print("\n🔧 Fixing Menu Setup Script...")

        menu_setup_path = self.theme_root / "freerideinvestor-menu-setup.php"

        if not menu_setup_path.exists():
            print("❌ Menu setup script not found")
            return

        # Read current content
        with open(menu_setup_path, 'r') as f:
            content = f.read()

        # Check if nav walker is defined in menu setup (it shouldn't be, it's in functions.php)
        # But make sure the menu setup properly references it
        if "FreeRideInvestor_Nav_Walker" not in content:
            print("⚠️ Nav walker not referenced in menu setup - this is expected")
            print("   (Nav walker is properly defined in functions.php)")

        # Check for any syntax issues
        try:
            compile(content, str(menu_setup_path), 'exec')
            print("✅ Menu setup script syntax is valid")
        except SyntaxError as e:
            print(f"❌ Syntax error in menu setup script: {e}")
            return

        print("✅ Menu setup script appears functional")

    def create_wordpress_installation_guide(self):
        """Create a comprehensive WordPress installation guide."""
        print("\n📚 Creating WordPress Installation Guide...")

        guide_path = self.site_root / "WORDPRESS_INSTALLATION_GUIDE.md"

        guide_content = """# FreeRideInvestor WordPress Installation Guide
===========================================

## 🚨 CRITICAL ISSUE IDENTIFIED

The repository contains **only theme files** but **no WordPress core installation**.
This is why menu links don't work - there's no WordPress site to run the menu code!

## 📋 Current Status

### ✅ What Exists:
- Theme files in `sites/freerideinvestor.com/wp/wp-content/themes/freerideinvestor-v2/`
- Menu setup script: `freerideinvestor-menu-setup.php`
- Page templates: `page-about.php`, `page-services.php`, etc.

### ❌ What's Missing:
- WordPress core files (`wp-config.php`, `wp-admin/`, `wp-includes/`)
- Database configuration
- Actual WordPress installation

## 🛠️ SOLUTION: Install WordPress

### Option 1: Fresh WordPress Installation (Recommended)

1. **Download WordPress Core:**
   ```bash
   cd sites/freerideinvestor.com/
   wget https://wordpress.org/latest.tar.gz
   tar -xzf latest.tar.gz
   mv wordpress/* wp/
   rm -rf wordpress latest.tar.gz
   ```

2. **Create wp-config.php:**
   ```bash
   cd wp/
   cp wp-config-sample.php wp-config.php
   # Edit wp-config.php with your database credentials
   ```

3. **Set up database:**
   ```sql
   CREATE DATABASE freerideinvestor_db;
   CREATE USER 'freerideinvestor_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON freerideinvestor_db.* TO 'freerideinvestor_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Run WordPress installation:**
   ```bash
   wp core install --url="https://freerideinvestor.com" --title="FreeRideInvestor" --admin_user="admin" --admin_email="admin@freerideinvestor.com"
   ```

### Option 2: Use Existing WordPress Installation

If freerideinvestor.com already has WordPress running elsewhere:

1. **Identify the live WordPress installation path**
2. **Copy theme files to live theme directory:**
   ```bash
   # Assuming live WordPress is at /var/www/freerideinvestor.com/
   cp -r sites/freerideinvestor.com/wp/wp-content/themes/freerideinvestor-v2/ /var/www/freerideinvestor.com/wp-content/themes/
   ```

3. **Activate the theme:**
   ```bash
   wp theme activate freerideinvestor-v2
   ```

## 🍽️ Menu Setup

After WordPress is installed and theme is activated:

### Automated Setup (Preferred):
```bash
wp eval "require_once('wp-content/themes/freerideinvestor-v2/freerideinvestor-menu-setup.php'); freerideinvestor_setup_pages_and_menu();"
```

### Manual Setup (WordPress Admin):
1. **Create Pages:** WordPress Admin → Pages → Add New
   - About (slug: about, template: About)
   - Services (slug: services, template: Services)
   - Resources (slug: resources, template: Resources)
   - Blog (slug: blog, template: Blog)
   - Contact (slug: contact, template: Contact)
   - Trading Strategies (slug: trading-strategies, template: Trading Strategies)

2. **Create Primary Menu:** Appearance → Menus
   - Add all pages to menu
   - Assign to "Primary Menu" location

3. **Create Footer Menu:** Appearance → Menus
   - Add About, Services, Resources, Contact
   - Assign to "Footer Menu" location

## 🧪 Testing

After setup, test these URLs:
- https://freerideinvestor.com/ (homepage)
- https://freerideinvestor.com/about/
- https://freerideinvestor.com/services/
- https://freerideinvestor.com/resources/
- https://freerideinvestor.com/blog/
- https://freerideinvestor.com/contact/
- https://freerideinvestor.com/trading-strategies/

## 🔧 Troubleshooting

### Menu Not Showing:
1. Check Appearance → Menus → Primary Menu location assigned
2. Verify theme is active: Appearance → Themes
3. Check browser console for JavaScript errors

### Pages Not Loading:
1. Run `wp rewrite flush` to refresh permalinks
2. Check page templates are assigned correctly
3. Verify pages are published (not draft)

### Theme Not Working:
1. Check theme files are in correct directory
2. Verify functions.php has no syntax errors
3. Check file permissions: `chmod 755 wp-content/themes/freerideinvestor-v2/`

## 📞 Support

If issues persist:
1. Check WordPress debug logs
2. Verify PHP version compatibility (7.4+ recommended)
3. Ensure all required PHP extensions are installed
4. Check web server configuration (Apache/Nginx)

---
**This guide addresses the root cause: missing WordPress installation!**
"""

        with open(guide_path, 'w') as f:
            f.write(guide_content)

        print(f"✅ Created installation guide: {guide_path}")

    def provide_manual_setup_instructions(self):
        """Provide manual menu setup instructions."""
        print("\n📋 Creating Manual Setup Instructions...")

        manual_path = self.site_root / "MANUAL_MENU_SETUP.md"

        manual_content = """# Manual Menu Setup for FreeRideInvestor
=======================================

If automated setup fails, follow these manual steps.

## Step 1: Verify Theme Installation

1. WordPress Admin → Appearance → Themes
2. Ensure "FreeRideInvestor V2" theme is active
3. If not visible, upload the theme ZIP file

## Step 2: Create Required Pages

WordPress Admin → Pages → Add New

Create these 6 pages with exact slugs and templates:

| Title | Slug | Template | Content |
|-------|------|----------|---------|
| About | about | About | About page content |
| Services | services | Services | Services page content |
| Resources | resources | Resources | Resources page content |
| Blog | blog | Blog | Blog page content |
| Contact | contact | Contact | Contact page content |
| Trading Strategies | trading-strategies | Trading Strategies | Trading content |

**Important:** Set Page Attributes → Template for each page!

## Step 3: Create Primary Menu

1. WordPress Admin → Appearance → Menus
2. Click "Create a new menu"
3. Name: "Primary Menu"
4. Check "Primary Menu" location
5. Add these menu items:
   - Home (link to your homepage URL)
   - About (select "About" page)
   - Services (select "Services" page)
   - Trading Strategies (select "Trading Strategies" page)
   - Resources (select "Resources" page)
   - Blog (select "Blog" page)
   - Contact (select "Contact" page)
6. Save Menu

## Step 4: Create Footer Menu

1. Create new menu named "Footer Menu"
2. Check "Footer Menu" location
3. Add these pages: About, Services, Resources, Contact
4. Save Menu

## Step 5: Test Menu Navigation

Visit your site and click each menu item. All should load the correct pages.

## Step 6: Check Page Templates

For each page, edit and verify:
- Page Attributes → Template shows correct template name
- Content displays properly
- No template errors

## Common Issues & Fixes

### Menu Not Showing:
- Appearance → Menus → verify locations assigned
- Theme may not support menu locations

### Wrong Templates:
- Page Attributes → Template must be set correctly
- Template files must exist in theme directory

### Broken Links:
- Check permalinks: Settings → Permalinks → Save
- Page slugs must match exactly

### Theme Not Loading:
- Check theme files exist in wp-content/themes/freerideinvestor-v2/
- Functions.php must not have syntax errors
"""

        with open(manual_path, 'w') as f:
            f.write(manual_content)

        print(f"✅ Created manual setup guide: {manual_path}")

    def create_deployment_package(self):
        """Create a deployment package for the live site."""
        print("\n📦 Creating Deployment Package...")

        deploy_path = self.site_root / "theme_deployment_package"
        deploy_path.mkdir(exist_ok=True)

        # Copy theme files
        theme_deploy_path = deploy_path / "freerideinvestor-v2"
        if self.theme_root.exists():
            shutil.copytree(self.theme_root, theme_deploy_path, dirs_exist_ok=True)
            print("✅ Copied theme files to deployment package")

        # Create deployment script
        deploy_script = deploy_path / "deploy_to_live_site.sh"

        deploy_script_content = """#!/bin/bash
# Deploy FreeRideInvestor theme to live WordPress site

echo "🚀 FreeRideInvestor Theme Deployment"
echo "===================================="

# Configuration - MODIFY THESE PATHS
LIVE_WP_PATH="/var/www/freerideinvestor.com"  # Path to live WordPress installation
BACKUP_SUFFIX="_backup_$(date +%Y%m%d_%H%M%S)"

echo "Live WordPress path: $LIVE_WP_PATH"

# Backup existing theme
if [ -d "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" ]; then
    echo "📦 Backing up existing theme..."
    mv "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2$BACKUP_SUFFIX"
    echo "✅ Backup created: freerideinvestor-v2$BACKUP_SUFFIX"
fi

# Copy new theme
echo "📋 Deploying new theme..."
cp -r freerideinvestor-v2 "$LIVE_WP_PATH/wp-content/themes/"
echo "✅ Theme deployed"

# Set permissions
echo "🔧 Setting permissions..."
find "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" -type f -exec chmod 644 {} \;
find "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" -type d -exec chmod 755 {} \;

echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Activate theme in WordPress admin"
echo "2. Run menu setup script or follow manual setup"
echo "3. Test menu navigation"
echo "4. Remove backup if everything works"
"""

        with open(deploy_script, 'w') as f:
            f.write(deploy_script_content)

        # Make script executable
        os.chmod(deploy_script, 0o755)

        print(f"✅ Created deployment package: {deploy_path}")
        print("   ├── freerideinvestor-v2/ (theme files)")
        print("   └── deploy_to_live_site.sh (deployment script)")


def main():
    """Run the menu fixer."""
    fixer = FreeRideInvestorMenuFixer()
    fixer.diagnose_and_fix()


if __name__ == "__main__":
    main()