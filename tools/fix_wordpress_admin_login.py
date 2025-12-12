#!/usr/bin/env python3
"""
WordPress Admin Login Troubleshooter
=====================================

Helps diagnose and fix WordPress admin login issues.

Usage:
    python tools/fix_wordpress_admin_login.py --site freerideinvestor.com
    python tools/fix_wordpress_admin_login.py --site freerideinvestor.com --reset-password
"""

import argparse
import requests
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_site_status(site_url: str) -> dict:
    """Check if WordPress site is accessible."""
    results = {
        "site_reachable": False,
        "wp_admin_reachable": False,
        "wp_login_reachable": False,
        "status_code": None,
        "error": None
    }
    
    try:
        # Check main site
        response = requests.get(f"https://{site_url}", timeout=10)
        results["site_reachable"] = True
        results["status_code"] = response.status_code
        
        # Check wp-admin
        admin_response = requests.get(f"https://{site_url}/wp-admin", timeout=10)
        results["wp_admin_reachable"] = True
        results["wp_admin_status"] = admin_response.status_code
        
        # Check wp-login.php
        login_response = requests.get(f"https://{site_url}/wp-login.php", timeout=10)
        results["wp_login_reachable"] = True
        results["wp_login_status"] = login_response.status_code
        
    except requests.exceptions.RequestException as e:
        results["error"] = str(e)
    
    return results


def check_credentials_file() -> dict:
    """Check if credentials file exists and has site info."""
    creds_file = project_root / ".deploy_credentials" / "blogging_api.json"
    results = {
        "file_exists": False,
        "has_credentials": False,
        "username": None
    }
    
    if creds_file.exists():
        results["file_exists"] = True
        try:
            import json
            with open(creds_file) as f:
                creds = json.load(f)
                # Check for various site name formats
                for key in ["freerideinvestor.com", "freerideinvestor"]:
                    if key in creds:
                        results["has_credentials"] = True
                        results["username"] = creds[key].get("username")
                        break
        except Exception:
            pass
    
    return results


def print_diagnostics(site: str):
    """Print comprehensive diagnostics."""
    print("=" * 70)
    print(f"WordPress Admin Login Diagnostics - {site}")
    print("=" * 70)
    print()
    
    # Check site status
    print("1. Checking site accessibility...")
    status = check_site_status(site)
    
    if status["site_reachable"]:
        print(f"   ✅ Site is reachable (Status: {status['status_code']})")
        if status["status_code"] == 500:
            print("   ⚠️  HTTP 500 error detected - site has internal errors")
    else:
        print(f"   ❌ Site not reachable: {status.get('error', 'Unknown error')}")
    
    if status.get("wp_admin_reachable"):
        print(f"   ✅ /wp-admin accessible (Status: {status.get('wp_admin_status')})")
    else:
        print("   ❌ /wp-admin not accessible")
    
    if status.get("wp_login_reachable"):
        print(f"   ✅ /wp-login.php accessible (Status: {status.get('wp_login_status')})")
    else:
        print("   ❌ /wp-login.php not accessible")
    
    print()
    
    # Check credentials
    print("2. Checking credentials file...")
    creds = check_credentials_file()
    
    if creds["file_exists"]:
        print("   ✅ Credentials file exists")
        if creds["has_credentials"]:
            print(f"   ✅ Username found: {creds['username']}")
        else:
            print("   ⚠️  No credentials for this site in file")
    else:
        print("   ❌ Credentials file not found")
    
    print()
    
    # Recommendations
    print("=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    print()
    
    if status["status_code"] == 500:
        print("❌ Site has HTTP 500 error - needs to be fixed first!")
        print()
        print("Fixes:")
        print("1. Check WordPress error logs (via FTP/SFTP)")
        print("2. Check .htaccess file for issues")
        print("3. Disable recently activated plugins")
        print("4. Check database connectivity")
        print("5. Increase PHP memory limit")
        print()
        print("Use WordPress manager tool:")
        print("  python tools/wordpress_manager.py --site freerideinvestor.com --check-health")
    
    print("\nLogin Options:")
    print(f"1. Try password reset: https://{site}/wp-login.php?action=lostpassword")
    print(f"2. Direct login: https://{site}/wp-admin")
    print(f"3. wp-login.php: https://{site}/wp-login.php")
    print()
    print("If you need to reset password via database:")
    print("  python tools/wordpress_manager.py --site freerideinvestor.com --reset-admin-password")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Diagnose WordPress admin login issues"
    )
    parser.add_argument(
        "--site",
        default="freerideinvestor.com",
        help="WordPress site domain (default: freerideinvestor.com)"
    )
    parser.add_argument(
        "--reset-password",
        action="store_true",
        help="Show instructions for password reset"
    )
    
    args = parser.parse_args()
    
    print_diagnostics(args.site)
    
    if args.reset_password:
        print("\n" + "=" * 70)
        print("PASSWORD RESET INSTRUCTIONS")
        print("=" * 70)
        print()
        print("Method 1: WordPress Password Reset (Easiest)")
        print(f"  1. Go to: https://{args.site}/wp-login.php?action=lostpassword")
        print("  2. Enter your username or email")
        print("  3. Check email for reset link")
        print()
        print("Method 2: Database Reset (Advanced)")
        print("  1. Access database via Hostinger control panel")
        print("  2. Find wp_users table")
        print("  3. Update user_pass field with MD5 hash of new password")
        print("  4. Or use WordPress manager tool (if configured)")
        print()
        print("Method 3: FTP/SSH Reset")
        print("  1. Access site via SFTP")
        print("  2. Use wp-cli: wp user update admin --user_pass=newpassword")
        print()


if __name__ == "__main__":
    main()

