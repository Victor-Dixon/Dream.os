#!/usr/bin/env python3
"""
Fix DaduDeKC.com Dark Theme for Home and About Pages
====================================================

Adds dark theme CSS to home and about pages to match other pages.

V2 Compliance | Author: Agent-2 | Date: 2025-12-24
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("❌ requests library required. Install with: pip install requests")


# Dark theme CSS to add to pages
DARK_THEME_CSS = """
<style>
/* Dark Theme Styles for Home and About Pages */
body {
    background-color: #1a1a1a !important;
    color: #e8e8e8 !important;
}

.page-content,
.entry-content,
.site-content,
main,
article {
    background-color: #1a1a1a !important;
    color: #e8e8e8 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

p, li, span, div {
    color: #e8e8e8 !important;
}

a {
    color: #4a9eff !important;
}

a:hover {
    color: #6bb3ff !important;
}

/* Ensure containers have dark background */
.container,
.wrapper,
.content-area,
.site-main {
    background-color: #1a1a1a !important;
}

/* Button styles */
button,
.btn,
input[type="submit"],
.wp-block-button__link {
    background-color: #4a9eff !important;
    color: #ffffff !important;
    border-color: #4a9eff !important;
}

button:hover,
.btn:hover,
input[type="submit"]:hover {
    background-color: #6bb3ff !important;
    border-color: #6bb3ff !important;
}

/* Form elements */
input[type="text"],
input[type="email"],
input[type="tel"],
textarea,
select {
    background-color: #2a2a2a !important;
    color: #e8e8e8 !important;
    border-color: #3a3a3a !important;
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="tel"]:focus,
textarea:focus,
select:focus {
    background-color: #2a2a2a !important;
    border-color: #4a9eff !important;
    color: #e8e8e8 !important;
}
</style>
"""


def load_wordpress_credentials() -> Optional[Dict]:
    """Load WordPress credentials from environment or config file."""
    # Try environment variables first
    username = os.getenv("WORDPRESS_USERNAME")
    password = os.getenv("WORDPRESS_APPLICATION_PASSWORD")
    site_url = os.getenv("WORDPRESS_SITE_URL", "https://dadudekc.com")
    
    if username and password:
        return {
            "username": username,
            "password": password,
            "site_url": site_url.rstrip("/")
        }
    
    # Try config file
    config_path = Path("D:/websites/configs/wordpress_credentials.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
            dadudekc_config = configs.get("dadudekc.com", {})
            if dadudekc_config:
                return {
                    "username": dadudekc_config.get("username"),
                    "password": dadudekc_config.get("application_password"),
                    "site_url": dadudekc_config.get("site_url", "https://dadudekc.com")
                }
    
    # Try .deploy_credentials directory
    deploy_creds_path = Path("D:/websites/.deploy_credentials/blogging_api.json")
    if deploy_creds_path.exists():
        with open(deploy_creds_path, 'r', encoding='utf-8') as f:
            creds = json.load(f)
            if "dadudekc.com" in creds:
                site_creds = creds["dadudekc.com"]
                return {
                    "username": site_creds.get("username"),
                    "password": site_creds.get("application_password"),
                    "site_url": site_creds.get("site_url", "https://dadudekc.com")
                }
    
    return None


def get_page_by_slug(site_url: str, slug: str, auth: tuple) -> Optional[Dict]:
    """Get WordPress page by slug."""
    url = f"{site_url}/wp-json/wp/v2/pages"
    params = {"slug": slug, "_embed": True}
    
    try:
        response = requests.get(url, params=params, auth=auth, timeout=30)
        response.raise_for_status()
        pages = response.json()
        
        if pages:
            return pages[0]
        return None
    except Exception as e:
        print(f"❌ Error fetching page '{slug}': {e}")
        return None


def update_page_content(page_id: int, current_content: str, site_url: str, auth: tuple) -> bool:
    """Update WordPress page content with dark theme CSS."""
    # Check if dark theme CSS is already present
    if "Dark Theme Styles" in current_content or "background-color: #1a1a1a" in current_content:
        print("   ℹ️  Dark theme CSS already present, skipping...")
        return True
    
    # Add dark theme CSS at the beginning of content
    updated_content = DARK_THEME_CSS + "\n\n" + current_content
    
    url = f"{site_url}/wp-json/wp/v2/pages/{page_id}"
    data = {
        "content": updated_content
    }
    
    try:
        response = requests.post(url, json=data, auth=auth, timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"   ❌ Error updating page: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return False


def fix_dark_theme_for_pages():
    """Fix dark theme for home and about pages."""
    print("🎨 Fixing Dark Theme for DaduDeKC.com Home and About Pages\n")
    
    if not REQUESTS_AVAILABLE:
        print("❌ requests library not available")
        return False
    
    # Load credentials
    creds = load_wordpress_credentials()
    if not creds:
        print("❌ WordPress credentials not found.")
        print("\n📝 To fix this, you can:")
        print("   1. Set environment variables:")
        print("      - WORDPRESS_USERNAME")
        print("      - WORDPRESS_APPLICATION_PASSWORD")
        print("      - WORDPRESS_SITE_URL (optional)")
        print("\n   2. Create config file:")
        print("      D:/websites/configs/wordpress_credentials.json")
        print("      {\"dadudekc.com\": {\"username\": \"...\", \"application_password\": \"...\", \"site_url\": \"...\"}}")
        print("\n   3. Create credentials file:")
        print("      D:/websites/.deploy_credentials/blogging_api.json")
        print("\n📋 Alternative: Manual Application")
        print("   The dark theme CSS has been generated. You can manually add it to:")
        print("   - WordPress Admin → Appearance → Customize → Additional CSS")
        print("   - OR edit the Home and About pages directly")
        print("\n   CSS saved to: tools/dadudekc_dark_theme_css.txt")
        
        # Save CSS to file for manual application
        css_file = Path(__file__).parent / "dadudekc_dark_theme_css.txt"
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(DARK_THEME_CSS.strip())
        print(f"   ✅ CSS saved to {css_file}")
        
        return False
    
    site_url = creds["site_url"]
    auth = (creds["username"], creds["password"])
    
    # Pages to fix
    pages_to_fix = [
        {"slug": "home", "name": "Home"},
        {"slug": "about", "name": "About"},
    ]
    
    success_count = 0
    total_count = len(pages_to_fix)
    
    for page_info in pages_to_fix:
        slug = page_info["slug"]
        name = page_info["name"]
        
        print(f"📄 Processing {name} page (slug: {slug})...")
        
        # Get page
        page = get_page_by_slug(site_url, slug, auth)
        if not page:
            print(f"   ⚠️  Page '{slug}' not found, trying alternative...")
            # Try with different slug variations
            alt_slugs = [f"{slug}-page", f"page-{slug}", slug.replace("-", "_")]
            for alt_slug in alt_slugs:
                page = get_page_by_slug(site_url, alt_slug, auth)
                if page:
                    break
            
            if not page:
                print(f"   ❌ Page '{slug}' not found")
                continue
        
        page_id = page.get("id")
        current_content = page.get("content", {}).get("rendered", "")
        
        if not current_content:
            # Try raw content
            current_content = page.get("content", {}).get("raw", "")
        
        print(f"   ✅ Found page (ID: {page_id})")
        
        # Update page
        if update_page_content(page_id, current_content, site_url, auth):
            print(f"   ✅ {name} page updated with dark theme CSS")
            success_count += 1
        else:
            print(f"   ❌ Failed to update {name} page")
    
    print(f"\n📊 Summary: {success_count}/{total_count} pages updated")
    
    if success_count == total_count:
        print("✅ All pages updated successfully!")
        return True
    else:
        print("⚠️  Some pages could not be updated")
        return False


if __name__ == "__main__":
    success = fix_dark_theme_for_pages()
    sys.exit(0 if success else 1)

