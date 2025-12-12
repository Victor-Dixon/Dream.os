#!/usr/bin/env python3
"""
Fix WordPress wp-admin Redirect Loop
=====================================

Fixes common causes of wp-admin redirect loops:
1. .htaccess redirect rules
2. WordPress site URL configuration
3. Plugin conflicts

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager


def fix_htaccess_redirects(site: str) -> bool:
    """Check and fix .htaccess redirect issues."""
    print("=" * 60)
    print("📄 Fixing .htaccess Redirect Issues")
    print("=" * 60)
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        
        # Get .htaccess path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                htaccess_path = f"domains/{domain}/public_html/.htaccess"
                backup_path = f"domains/{domain}/public_html/.htaccess.backup"
            else:
                htaccess_path = "/public_html/.htaccess"
                backup_path = "/public_html/.htaccess.backup"
        else:
            htaccess_path = "/public_html/.htaccess"
            backup_path = "/public_html/.htaccess.backup"
        
        try:
            sftp = manager.conn_manager.sftp
            
            # Check if .htaccess exists
            try:
                sftp.stat(htaccess_path)
                print("✅ .htaccess exists")
                
                # Read .htaccess
                with sftp.open(htaccess_path, 'r') as f:
                    content = f.read().decode('utf-8')
                
                # Backup original
                with sftp.open(backup_path, 'w') as f:
                    f.write(content)
                print(f"✅ Created backup: {backup_path}")
                
                # Check for problematic redirect rules
                lines = content.split('\n')
                new_lines = []
                removed_rules = []
                
                for i, line in enumerate(lines):
                    # Remove rules that might cause redirect loops
                    line_lower = line.lower().strip()
                    
                    # Skip rules that redirect wp-admin
                    if 'wp-admin' in line_lower and ('redirect' in line_lower or 'rewriterule' in line_lower):
                        removed_rules.append(line.strip())
                        print(f"⚠️  Removing potentially problematic rule: {line.strip()}")
                        continue
                    
                    # Skip duplicate redirect rules
                    if i > 0 and 'redirect' in line_lower and 'redirect' in lines[i-1].lower():
                        removed_rules.append(line.strip())
                        print(f"⚠️  Removing duplicate redirect: {line.strip()}")
                        continue
                    
                    new_lines.append(line)
                
                if removed_rules:
                    # Write fixed .htaccess
                    new_content = '\n'.join(new_lines)
                    with sftp.open(htaccess_path, 'w') as f:
                        f.write(new_content)
                    print(f"✅ Fixed .htaccess (removed {len(removed_rules)} problematic rules)")
                    print("💡 Test the site now. If issues persist, restore from backup:")
                    print(f"   mv {backup_path} {htaccess_path}")
                    return True
                else:
                    print("✅ No problematic redirect rules found in .htaccess")
                    return False
                    
            except FileNotFoundError:
                print("⚠️  .htaccess does not exist (this is normal)")
                return False
                
        except Exception as e:
            print(f"❌ Error fixing .htaccess: {e}")
            return False
        
        manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_wp_config_urls(site: str) -> bool:
    """Check WordPress site URL configuration."""
    print("\n" + "=" * 60)
    print("⚙️  Checking WordPress Configuration")
    print("=" * 60)
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        
        # Get wp-config.php path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                wp_config_path = f"domains/{domain}/public_html/wp-config.php"
            else:
                wp_config_path = "/public_html/wp-config.php"
        else:
            wp_config_path = "/public_html/wp-config.php"
        
        try:
            sftp = manager.conn_manager.sftp
            
            # Read wp-config.php
            with sftp.open(wp_config_path, 'r') as f:
                content = f.read().decode('utf-8')
            
            # Check for WP_HOME and WP_SITEURL
            has_wp_home = 'WP_HOME' in content
            has_wp_siteurl = 'WP_SITEURL' in content
            
            print(f"WP_HOME defined: {has_wp_home}")
            print(f"WP_SITEURL defined: {has_wp_siteurl}")
            
            if has_wp_home and has_wp_siteurl:
                # Extract URLs
                import re
                wp_home_match = re.search(r"define\s*\(\s*['\"]WP_HOME['\"]\s*,\s*['\"]([^'\"]+)['\"]", content)
                wp_siteurl_match = re.search(r"define\s*\(\s*['\"]WP_SITEURL['\"]\s*,\s*['\"]([^'\"]+)['\"]", content)
                
                if wp_home_match and wp_siteurl_match:
                    wp_home = wp_home_match.group(1)
                    wp_siteurl = wp_siteurl_match.group(1)
                    
                    print(f"WP_HOME: {wp_home}")
                    print(f"WP_SITEURL: {wp_siteurl}")
                    
                    # Check if they match
                    if wp_home != wp_siteurl:
                        print("⚠️  WP_HOME and WP_SITEURL don't match - this can cause redirect loops")
                        print("💡 They should both be: https://freerideinvestor.com")
                        return False
                    else:
                        print("✅ WP_HOME and WP_SITEURL match")
                        return True
                else:
                    print("⚠️  Could not parse WP_HOME/WP_SITEURL values")
                    return False
            else:
                print("⚠️  WP_HOME or WP_SITEURL not defined in wp-config.php")
                print("💡 WordPress will use database values - check database if redirect loop persists")
                return False
                
        except FileNotFoundError:
            print("❌ wp-config.php not found")
            return False
        except Exception as e:
            print(f"❌ Error checking wp-config.php: {e}")
            return False
        
        manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def disable_problematic_plugins(site: str) -> bool:
    """Temporarily disable plugins that might cause redirect loops."""
    print("\n" + "=" * 60)
    print("🔌 Checking for Problematic Plugins")
    print("=" * 60)
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        
        # Get plugins path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                plugins_path = f"domains/{domain}/public_html/wp-content/plugins"
            else:
                plugins_path = "/public_html/wp-content/plugins"
        else:
            plugins_path = "/public_html/wp-content/plugins"
        
        # Plugins known to cause redirect loops
        problematic_plugins = [
            'really-simple-ssl',
            'wordfence',
            'ithemes-security',
            'sucuri-scanner',
            'all-in-one-wp-security',
            'better-wp-security'
        ]
        
        try:
            sftp = manager.conn_manager.sftp
            active_plugins = sftp.listdir(plugins_path)
            
            found_problematic = []
            for plugin in active_plugins:
                if any(prob in plugin.lower() for prob in problematic_plugins):
                    found_problematic.append(plugin)
            
            if found_problematic:
                print(f"⚠️  Found potentially problematic plugins: {', '.join(found_problematic)}")
                print("💡 Consider temporarily disabling these plugins to test")
                return True
            else:
                print("✅ No known problematic plugins found")
                return False
                
        except Exception as e:
            print(f"❌ Error checking plugins: {e}")
            return False
        
        manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main fix function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix WordPress wp-admin redirect loop")
    parser.add_argument("--site", required=True, help="Site key (e.g., freerideinvestor)")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("🔧 WordPress Redirect Loop Fix Tool")
    print("=" * 60)
    print(f"Site: {args.site}")
    print()
    
    # Run fixes
    htaccess_fixed = fix_htaccess_redirects(args.site)
    config_ok = check_wp_config_urls(args.site)
    plugins_checked = disable_problematic_plugins(args.site)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Fix Summary")
    print("=" * 60)
    
    if htaccess_fixed:
        print("✅ .htaccess has been fixed")
        print("💡 Test wp-admin access now")
    
    if not config_ok:
        print("⚠️  WordPress URL configuration may need attention")
        print("💡 Check database wp_options table for siteurl and home values")
    
    if plugins_checked:
        print("⚠️  Some plugins may need to be disabled for testing")
    
    print("\n💡 Next Steps:")
    print("   1. Test wp-admin access")
    print("   2. If still redirecting, check database wp_options table")
    print("   3. Temporarily disable all plugins to test")
    print("   4. Check server error logs")
    print()


if __name__ == "__main__":
    main()

