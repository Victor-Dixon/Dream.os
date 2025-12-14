#!/usr/bin/env python3
"""
Fix The Swarm Post - White on White Text Sections
==================================================

Directly fixes the specific sections in "Introducing The Swarm" post that have white-on-white text.

Author: Agent-4 (Captain)
Date: 2025-12-14
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import requests
from requests.auth import HTTPBasicAuth


def load_config() -> Dict[str, Any]:
    """Load WordPress configuration."""
    config_path = project_root / ".deploy_credentials" / "blogging_api.json"
    
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Try different config structures
    sites = config.get("sites", {})
    if not sites:
        site_config = config.get("dadudekc.com", {})
    else:
        site_config = sites.get("dadudekc.com", {})
    
    return {
        "url": site_config.get("url") or site_config.get("site_url") or "https://dadudekc.com",
        "username": site_config.get("username") or site_config.get("wp_user"),
        "app_password": site_config.get("app_password") or site_config.get("wp_app_password")
    }


def fix_swarm_post_content(content: str) -> str:
    """Fix specific white-on-white sections in The Swarm post."""
    
    # Fix 1: The Core Philosophy paragraph
    # Find: <p style="font-size: 1.1em; margin-bottom: 0;"> without color
    content = re.sub(
        r'(<p style="font-size:\s*1\.1em[^"]*?margin-bottom:\s*0[^"]*?)"',
        r'\1; color: #2d3748"',
        content
    )
    
    # Fix 2: Plain <p> tags in white background cards (#fff or #ffffff)
    # These are the Activity Detection, Unified Messaging, Test-Driven Development sections
    # Pattern: <div...background: #fff...><p> (plain p tag, no style)
    def fix_card_paragraphs(html):
        # Find all plain <p> tags that come after card divs
        # Match pattern: card div opening, then any content, then plain <p>
        pattern = r'(<div[^>]*background:\s*#fff[^>]*>.*?)(<p)(?!\s+style=")'
        
        def replace_func(match):
            before = match.group(1)
            p_tag = match.group(2)
            # Check if there's already content between div and p
            # We want to add style="color: #2d3748" to the <p> tag
            return f'{before}{p_tag} style="color: #2d3748"'
        
        # Use DOTALL to match across newlines
        fixed = re.sub(pattern, replace_func, html, flags=re.DOTALL)
        return fixed
    
    content = fix_card_paragraphs(content)
    
    # Fix 3: Why The Swarm Matters section (plain <p> with font-size but no color)
    content = re.sub(
        r'(<p style="font-size:\s*1\.15em[^"]*?line-height:\s*1\.8[^"]*?margin:\s*0[^"]*?)"',
        r'\1; color: #2d3748"',
        content
    )
    
    # Fix 4: Any other plain <p> tags in sections with background: #f7fafc or #f8f9fa
    # These are highlighted/conclusion sections
    def fix_highlighted_plain_p(html):
        # Match highlighted divs, then plain <p> tags
        pattern = r'(<div[^>]*(?:background:\s*#f[78]f[89]fa[fc]|border-left:\s*5px)[^>]*>.*?)(<p)(?!\s+style="[^"]*color)'
        
        def replace_func(match):
            before = match.group(1)
            p_tag = match.group(2)
            # Check if p tag already has style with color
            # If not, add it
            return f'{before}{p_tag} style="color: #2d3748"'
        
        return re.sub(pattern, replace_func, html, flags=re.DOTALL | re.IGNORECASE)
    
    content = fix_highlighted_plain_p(content)
    
    return content


def main():
    """Fix The Swarm post white-on-white sections."""
    print("=" * 60)
    print("FIXING THE SWARM POST - WHITE ON WHITE SECTIONS")
    print("=" * 60)
    print()
    
    config = load_config()
    if not config.get("username") or not config.get("app_password"):
        print("❌ Missing WordPress credentials")
        return 1
    
    site_url = config["url"]
    auth = HTTPBasicAuth(config["username"], config["app_password"])
    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    
    try:
        # Get all posts to find "Introducing The Swarm"
        response = requests.get(
            api_url,
            auth=auth,
            params={"per_page": 10, "status": "publish", "search": "Introducing The Swarm"},
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch posts: {response.status_code}")
            return 1
        
        posts = response.json()
        swarm_post = None
        
        for post in posts:
            title = post.get("title", {}).get("rendered", "")
            if "Introducing The Swarm" in title:
                swarm_post = post
                break
        
        if not swarm_post:
            print("❌ Could not find 'Introducing The Swarm' post")
            return 1
        
        post_id = swarm_post["id"]
        title = swarm_post.get("title", {}).get("rendered", "")
        content = swarm_post.get("content", {}).get("rendered", "")
        
        print(f"📋 Found post #{post_id}: {title[:60]}...")
        print()
        
        # Fix the content
        fixed_content = fix_swarm_post_content(content)
        
        # Check if changes were made
        if fixed_content == content:
            print("ℹ️  No changes needed - content already has color fixes")
            return 0
        
        print("🔧 Applying fixes...")
        
        # Update the post
        update_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
        update_response = requests.post(
            update_url,
            auth=auth,
            json={"content": fixed_content},
            timeout=30
        )
        
        if update_response.status_code == 200:
            result = update_response.json()
            print(f"✅ Successfully updated!")
            print(f"   Post ID: {post_id}")
            print(f"   URL: {result.get('link', 'N/A')}")
            return 0
        else:
            print(f"❌ Failed to update: {update_response.status_code}")
            print(f"   Error: {update_response.text[:200]}")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

