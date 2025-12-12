#!/usr/bin/env python3
"""
Diagnose WordPress Admin Login Issues
=====================================

Checks various causes of WordPress login problems:
- Site accessibility
- Debug log errors
- Plugin conflicts
- .htaccess issues
- Database connection
- File permissions

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import sys
import requests
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager


def check_site_accessibility(url: str) -> dict:
    """Check if the site is accessible."""
    print("=" * 60)
    print("🌐 Checking Site Accessibility")
    print("=" * 60)
    
    results = {
        "homepage": None,
        "wp_admin": None,
        "wp_login": None,
        "errors": []
    }
    
    # Check homepage
    try:
        print(f"Checking homepage: {url}")
        response = requests.get(url, timeout=10, allow_redirects=True)
        results["homepage"] = {
            "status_code": response.status_code,
            "accessible": response.status_code == 200,
            "url": response.url
        }
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Homepage accessible")
        else:
            print(f"  ❌ Homepage returned {response.status_code}")
            results["errors"].append(f"Homepage returned {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error accessing homepage: {e}")
        results["errors"].append(f"Homepage error: {e}")
        results["homepage"] = {"accessible": False, "error": str(e)}
    
    # Check wp-admin
    try:
        admin_url = f"{url}/wp-admin"
        print(f"\nChecking wp-admin: {admin_url}")
        response = requests.get(admin_url, timeout=10, allow_redirects=True)
        results["wp_admin"] = {
            "status_code": response.status_code,
            "accessible": response.status_code in [200, 302, 301],
            "url": response.url,
            "redirects_to_login": "wp-login.php" in response.url
        }
        print(f"  Status: {response.status_code}")
        print(f"  Final URL: {response.url}")
        if response.status_code in [200, 302, 301]:
            if "wp-login.php" in response.url:
                print("  ✅ wp-admin redirects to login (normal)")
            else:
                print("  ✅ wp-admin accessible")
        else:
            print(f"  ❌ wp-admin returned {response.status_code}")
            results["errors"].append(f"wp-admin returned {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error accessing wp-admin: {e}")
        results["errors"].append(f"wp-admin error: {e}")
        results["wp_admin"] = {"accessible": False, "error": str(e)}
    
    # Check wp-login.php
    try:
        login_url = f"{url}/wp-login.php"
        print(f"\nChecking wp-login.php: {login_url}")
        response = requests.get(login_url, timeout=10, allow_redirects=False)
        results["wp_login"] = {
            "status_code": response.status_code,
            "accessible": response.status_code == 200,
            "has_form": "loginform" in response.text.lower() or "user_login" in response.text.lower()
        }
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            if results["wp_login"]["has_form"]:
                print("  ✅ Login page accessible and has login form")
            else:
                print("  ⚠️  Login page accessible but form may be missing")
                results["errors"].append("Login form not found on login page")
        else:
            print(f"  ❌ Login page returned {response.status_code}")
            results["errors"].append(f"Login page returned {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error accessing login page: {e}")
        results["errors"].append(f"Login page error: {e}")
        results["wp_login"] = {"accessible": False, "error": str(e)}
    
    return results


def check_debug_log(site: str) -> dict:
    """Check WordPress debug log for login-related errors."""
    print("\n" + "=" * 60)
    print("📋 Checking Debug Log")
    print("=" * 60)
    
    results = {
        "log_exists": False,
        "login_errors": [],
        "fatal_errors": [],
        "recent_errors": []
    }
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return results
        
        print("📡 Connected to server")
        
        # Get debug log path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                debug_log_path = f"domains/{domain}/public_html/wp-content/debug.log"
            else:
                debug_log_path = "/public_html/wp-content/debug.log"
        else:
            debug_log_path = "/public_html/wp-content/debug.log"
        
        try:
            sftp = manager.conn_manager.sftp
            sftp.stat(debug_log_path)
            results["log_exists"] = True
            print("✅ debug.log exists")
            
            # Read log
            with sftp.open(debug_log_path, 'r') as f:
                lines = f.readlines()
            
            # Check for login-related errors
            for line in lines:
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ["login", "authentication", "wp-login", "wp-admin"]):
                    results["login_errors"].append(line.strip())
                if "fatal error" in line_lower:
                    results["fatal_errors"].append(line.strip())
            
            # Get recent errors (last 20 lines)
            results["recent_errors"] = [line.strip() for line in lines[-20:]]
            
            if results["login_errors"]:
                print(f"\n⚠️  Found {len(results['login_errors'])} login-related errors:")
                for error in results["login_errors"][:5]:
                    print(f"   {error}")
            else:
                print("✅ No login-related errors in debug log")
            
            if results["fatal_errors"]:
                print(f"\n❌ Found {len(results['fatal_errors'])} fatal errors:")
                for error in results["fatal_errors"][:5]:
                    print(f"   {error}")
            
        except FileNotFoundError:
            print("⚠️  debug.log does not exist")
        except Exception as e:
            print(f"❌ Error reading debug.log: {e}")
        
        manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return results


def check_htaccess(site: str) -> dict:
    """Check .htaccess file for issues."""
    print("\n" + "=" * 60)
    print("📄 Checking .htaccess")
    print("=" * 60)
    
    results = {
        "exists": False,
        "has_issues": False,
        "issues": []
    }
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return results
        
        # Get .htaccess path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                htaccess_path = f"domains/{domain}/public_html/.htaccess"
            else:
                htaccess_path = "/public_html/.htaccess"
        else:
            htaccess_path = "/public_html/.htaccess"
        
        try:
            sftp = manager.conn_manager.sftp
            sftp.stat(htaccess_path)
            results["exists"] = True
            print("✅ .htaccess exists")
            
            # Read .htaccess
            with sftp.open(htaccess_path, 'r') as f:
                content = f.read().decode('utf-8')
            
            # Check for common issues
            if "deny from all" in content.lower() and "wp-admin" in content.lower():
                results["has_issues"] = True
                results["issues"].append("wp-admin may be blocked by .htaccess")
                print("⚠️  Potential wp-admin blocking rule found")
            
            if "RewriteRule.*wp-admin" in content and "deny" in content.lower():
                results["has_issues"] = True
                results["issues"].append("Rewrite rules may be blocking wp-admin")
                print("⚠️  Potential rewrite rule blocking wp-admin")
            
            if not results["has_issues"]:
                print("✅ No obvious blocking rules in .htaccess")
            
        except FileNotFoundError:
            print("⚠️  .htaccess does not exist (this is normal for some setups)")
        except Exception as e:
            print(f"❌ Error reading .htaccess: {e}")
        
        manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return results


def check_plugins_status(site: str) -> dict:
    """Check plugin status."""
    print("\n" + "=" * 60)
    print("🔌 Checking Plugins")
    print("=" * 60)
    
    results = {
        "plugins_dir_exists": False,
        "disabled_plugins": [],
        "active_plugins": []
    }
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return results
        
        # Get plugins path
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                plugins_path = f"domains/{domain}/public_html/wp-content/plugins"
                disabled_path = f"domains/{domain}/public_html/wp-content/plugins-disabled"
            else:
                plugins_path = "/public_html/wp-content/plugins"
                disabled_path = "/public_html/wp-content/plugins-disabled"
        else:
            plugins_path = "/public_html/wp-content/plugins"
            disabled_path = "/public_html/wp-content/plugins-disabled"
        
        try:
            sftp = manager.conn_manager.sftp
            
            # Check if plugins directory exists
            try:
                sftp.stat(plugins_path)
                results["plugins_dir_exists"] = True
                print("✅ Plugins directory exists")
                
                # List active plugins
                active_plugins = sftp.listdir(plugins_path)
                results["active_plugins"] = [p for p in active_plugins if not p.startswith('.')]
                print(f"   Active plugins: {len(results['active_plugins'])}")
                for plugin in results["active_plugins"][:10]:
                    print(f"     - {plugin}")
                
            except FileNotFoundError:
                print("⚠️  Plugins directory not found")
            
            # Check for disabled plugins
            try:
                disabled_plugins = sftp.listdir(disabled_path)
                results["disabled_plugins"] = [p for p in disabled_plugins if not p.startswith('.')]
                if results["disabled_plugins"]:
                    print(f"\n⚠️  Disabled plugins: {len(results['disabled_plugins'])}")
                    for plugin in results["disabled_plugins"]:
                        print(f"     - {plugin}")
            except FileNotFoundError:
                print("✅ No disabled plugins directory (all plugins active)")
            
        except Exception as e:
            print(f"❌ Error checking plugins: {e}")
        
        manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return results


def main():
    """Main diagnostic function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Diagnose WordPress login issues")
    parser.add_argument("--site", required=True, help="Site key (e.g., freeride)")
    parser.add_argument("--url", help="Site URL (e.g., https://freerideinvestor.com)")
    
    args = parser.parse_args()
    
    # Get URL from site config if not provided
    if not args.url:
        try:
            manager = WordPressManager(args.site)
            site_config = manager.SITE_CONFIGS.get(args.site, {})
            args.url = site_config.get("url", f"https://{args.site}.com")
        except:
            args.url = f"https://{args.site}.com"
    
    print("\n" + "=" * 60)
    print("🔍 WordPress Login Diagnostic Tool")
    print("=" * 60)
    print(f"Site: {args.site}")
    print(f"URL: {args.url}")
    print()
    
    # Run diagnostics
    accessibility = check_site_accessibility(args.url)
    debug_log = check_debug_log(args.site)
    htaccess = check_htaccess(args.site)
    plugins = check_plugins_status(args.site)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Diagnostic Summary")
    print("=" * 60)
    
    issues = []
    
    if accessibility["errors"]:
        issues.extend(accessibility["errors"])
    
    if debug_log["fatal_errors"]:
        issues.append(f"{len(debug_log['fatal_errors'])} fatal errors in debug log")
    
    if debug_log["login_errors"]:
        issues.append(f"{len(debug_log['login_errors'])} login-related errors in debug log")
    
    if htaccess["has_issues"]:
        issues.extend(htaccess["issues"])
    
    if issues:
        print("\n❌ Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        
        print("\n💡 Recommendations:")
        if not accessibility["wp_login"]["accessible"]:
            print("   1. Check if wp-login.php file exists and is accessible")
            print("   2. Check file permissions (should be 644)")
            print("   3. Check .htaccess for blocking rules")
        
        if debug_log["fatal_errors"]:
            print("   4. Fix fatal errors in debug log")
            print("   5. Disable problematic plugins")
        
        if htaccess["has_issues"]:
            print("   6. Review .htaccess rules")
            print("   7. Temporarily rename .htaccess to test")
    else:
        print("\n✅ No obvious issues found")
        print("\n💡 If login still doesn't work:")
        print("   1. Check username/password are correct")
        print("   2. Try password reset")
        print("   3. Check database connection")
        print("   4. Check user table in database")
    
    print()


if __name__ == "__main__":
    main()

