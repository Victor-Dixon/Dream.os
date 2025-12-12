#!/usr/bin/env python3
"""Check WordPress wp-admin login page status."""

import requests
import sys

def check_wpadmin(url):
    """Check wp-admin page status."""
    print("=" * 60)
    print("Checking wp-admin Login Page")
    print("=" * 60)
    print(f"URL: {url}/wp-admin/")
    print()
    
    # Check without redirects
    print("1. Checking wp-admin (no redirects)...")
    try:
        r = requests.get(f"{url}/wp-admin/", timeout=10, allow_redirects=False)
        print(f"   Status Code: {r.status_code}")
        if r.status_code in [301, 302, 307, 308]:
            print(f"   Redirect Location: {r.headers.get('Location', 'N/A')}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    # Check with redirects
    print("2. Checking wp-admin (with redirects)...")
    try:
        r = requests.get(f"{url}/wp-admin/", timeout=10, allow_redirects=True)
        print(f"   Status Code: {r.status_code}")
        print(f"   Final URL: {r.url}")
        print(f"   Content Length: {len(r.text)} bytes")
        print()
        
        # Check for login form
        has_login_form = "user_login" in r.text or "wp-submit" in r.text or "loginform" in r.text.lower()
        print(f"   Has Login Form: {'✅ Yes' if has_login_form else '❌ No'}")
        
        # Check for errors
        has_error = "error" in r.text.lower() or "critical" in r.text.lower() or "fatal" in r.text.lower()
        print(f"   Has Error: {'⚠️  Yes' if has_error else '✅ No'}")
        
        # Check for redirect loop indicators
        has_redirect_issue = r.url != f"{url}/wp-admin/" and "wp-login" not in r.url
        if has_redirect_issue:
            print(f"   ⚠️  Redirected to: {r.url}")
        
        # Check for specific error messages
        if "critical error" in r.text.lower():
            print("   ❌ CRITICAL ERROR detected in page!")
        if "fatal error" in r.text.lower():
            print("   ❌ FATAL ERROR detected in page!")
        if "database error" in r.text.lower():
            print("   ❌ DATABASE ERROR detected in page!")
        
        print()
        
        # Save response for inspection
        output_file = "runtime/wpadmin_response.html"
        from pathlib import Path
        Path("runtime").mkdir(exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f"   ✅ Response saved to: {output_file}")
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    # Check wp-login.php directly
    print("3. Checking wp-login.php directly...")
    try:
        r = requests.get(f"{url}/wp-login.php", timeout=10)
        print(f"   Status Code: {r.status_code}")
        print(f"   Has Login Form: {'✅ Yes' if ('user_login' in r.text or 'wp-submit' in r.text) else '❌ No'}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print("If login form is missing or errors are present, there may be:")
    print("  - Plugin conflict (even with plugins disabled)")
    print("  - Theme issue affecting wp-admin")
    print("  - .htaccess redirect issue")
    print("  - WordPress core file corruption")
    print()

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://freerideinvestor.com"
    check_wpadmin(url)

