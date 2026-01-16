#!/usr/bin/env python3
"""
Deploy Animated Hero Section to TradingRobotPlug
===============================================

Automated deployment script for the revolutionary animated hero section.
Uses existing WordPress deployment tools to safely update the homepage.

Features:
- Backup current front-page.php
- Deploy animated hero section
- Update WordPress theme functions
- Test deployment
- Rollback capability
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

class AnimatedHeroDeployer:
    def __init__(self):
        self.site_root = Path(__file__).parent
        self.theme_dir = self.site_root / "wp" / "wp-content" / "themes" / "tradingrobotplug-theme"
        self.backup_dir = self.site_root / "backups" / "hero_deployments"

        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self):
        """Create backup of current front-page.php"""
        front_page = self.theme_dir / "front-page.php"
        backup_name = f"front-page-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}.php"
        backup_path = self.backup_dir / backup_name

        if front_page.exists():
            shutil.copy2(front_page, backup_path)
            print(f"✅ Backup created: {backup_path}")
            return backup_path
        else:
            print("⚠️  No existing front-page.php found")
            return None

    def deploy_animated_hero(self):
        """Deploy the animated hero section"""
        source_file = self.theme_dir / "front-page-animated.php"
        target_file = self.theme_dir / "front-page.php"

        if not source_file.exists():
            print("❌ Animated hero template not found!")
            return False

        # Deploy the file
        shutil.copy2(source_file, target_file)
        print("✅ Animated hero section deployed successfully!")
        return True

    def update_functions_php(self):
        """Ensure functions.php has Three.js and Tailwind enqueuing"""
        functions_file = self.theme_dir / "functions.php"

        if not functions_file.exists():
            print("⚠️  functions.php not found")
            return False

        # Read current content
        with open(functions_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if Three.js enqueuing is already there
        if 'three-js' in content and 'tailwind-css' in content:
            print("✅ functions.php already has required enqueuing")
            return True

        # Add the enqueuing code before the closing of the function
        enqueue_code = '''
    // Three.js and Tailwind for animated hero section
    if (is_front_page() && get_page_template_slug() === 'front-page-animated.php') {
        wp_enqueue_script('three-js', 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', array(), 'r128', true);
        wp_enqueue_script('tailwind-css', 'https://cdn.tailwindcss.com', array(), '3.4.0', false);
        wp_add_inline_script('tailwind-css', "
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            'brand-cyan': '#00d4ff',
                            'brand-purple': '#9d4edd',
                            'brand-pink': '#ff0080',
                            'brand-green': '#00ff88'
                        }
                    }
                }
            }
        ");
    }
'''

        # Insert before the closing brace of my_custom_theme_scripts function
        insert_position = content.find('add_action(\'wp_enqueue_scripts\', \'my_custom_theme_scripts\');')
        if insert_position > 0:
            # Find the function closing brace
            func_end = content.rfind('}', 0, insert_position)
            if func_end > 0:
                content = content[:func_end] + enqueue_code + content[func_end:]

                with open(functions_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("✅ functions.php updated with Three.js and Tailwind enqueuing")
                return True

        print("⚠️  Could not update functions.php automatically")
        print("   Please manually add Three.js and Tailwind enqueuing to my_custom_theme_scripts()")
        return False

    def create_wordpress_page_template(self):
        """Create WordPress page template for the animated hero"""
        template_file = self.theme_dir / "page-animated-hero.php"

        template_content = '''<?php
/*
Template Name: Animated Hero
Description: Revolutionary animated hero section with Three.js and live TSLA data
*/

get_header();

// Include the animated hero content
include(get_template_directory() . '/front-page-animated.php');

get_footer();
'''

        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)

        print("✅ WordPress page template created: page-animated-hero.php")

    def test_deployment(self):
        """Basic test of the deployment"""
        front_page = self.theme_dir / "front-page.php"

        if not front_page.exists():
            print("❌ Deployment failed - front-page.php not found")
            return False

        # Check if Three.js is referenced
        with open(front_page, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ('Three.js library', 'three.js' in content),
            ('Tailwind CSS', 'tailwindcss' in content),
            ('Particle system', 'ParticleSystem' in content),
            ('Live TSLA data', 'LiveTSLAData' in content),
            ('Canvas element', 'hero-canvas' in content)
        ]

        passed = 0
        for check_name, result in checks:
            if result:
                print(f"✅ {check_name} - OK")
                passed += 1
            else:
                print(f"❌ {check_name} - MISSING")

        if passed == len(checks):
            print("🎉 Deployment test PASSED!")
            return True
        else:
            print(f"⚠️  Deployment test: {passed}/{len(checks)} checks passed")
            return False

    def rollback(self):
        """Rollback to previous version"""
        backups = list(self.backup_dir.glob("front-page-backup-*.php"))
        if not backups:
            print("❌ No backups found for rollback")
            return False

        # Use the most recent backup
        latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
        target_file = self.theme_dir / "front-page.php"

        shutil.copy2(latest_backup, target_file)
        print(f"✅ Rolled back to: {latest_backup.name}")
        return True

    def deploy(self):
        """Full deployment process"""
        print("🚀 Starting Animated Hero Section Deployment")
        print("=" * 50)

        # Step 1: Backup
        print("\n📦 Step 1: Creating backup...")
        backup_path = self.create_backup()

        # Step 2: Deploy
        print("\n⚙️  Step 2: Deploying animated hero...")
        if not self.deploy_animated_hero():
            print("❌ Deployment failed!")
            return False

        # Step 3: Update functions
        print("\n🔧 Step 3: Updating theme functions...")
        self.update_functions_php()

        # Step 4: Create template
        print("\n📝 Step 4: Creating WordPress template...")
        self.create_wordpress_page_template()

        # Step 5: Test
        print("\n🧪 Step 5: Testing deployment...")
        if not self.test_deployment():
            print("⚠️  Tests failed, but deployment completed")
            print("   You may need to check the WordPress admin for issues")

        # Success message
        print("\n" + "=" * 50)
        print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\n📋 Next Steps:")
        print("1. Go to WordPress Admin → Pages")
        print("2. Edit your homepage")
        print("3. In 'Page Attributes' → 'Template', select 'Animated Hero'")
        print("4. Save and view your homepage")
        print("\n🌐 Your site will now have:")
        print("   • 200 interactive 3D particles")
        print("   • Live TSLA intelligence display")
        print("   • Holographic gradient backgrounds")
        print("   • AI swarm analysis with confidence %")
        print("   • Real-time market correlations")

        if backup_path:
            print(f"\n🔄 Backup saved: {backup_path.name}")
            print("   To rollback: Run this script with --rollback")

        print("\n🚀 Enjoy your revolutionary trading website!")
        return True


def main():
    deployer = AnimatedHeroDeployer()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--rollback':
            deployer.rollback()
            return
        elif sys.argv[1] == '--test':
            deployer.test_deployment()
            return
        elif sys.argv[1] == '--backup':
            deployer.create_backup()
            return

    # Full deployment
    deployer.deploy()


if __name__ == "__main__":
    main()