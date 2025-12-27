#!/usr/bin/env python3
"""
Post The Long Vigil to Digital Dreamscape WordPress
===================================================

Posts the "The Long Vigil" blog post to digitaldreamscape.site WordPress.

V2 Compliance | Author: Agent-2 | Date: 2025-12-25
"""

import json
import sys
from pathlib import Path

# Add tools to path
websites_tools = Path("D:/websites/tools/blog")
sys.path.insert(0, str(websites_tools))

try:
    from unified_blogging_automation import WordPressBlogClient
    HAS_BLOGGING = True
except ImportError as e:
    HAS_BLOGGING = False
    print(f"❌ unified_blogging_automation not available: {e}")

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_wordpress_credentials() -> dict:
    """Load WordPress credentials for digitaldreamscape.site."""
    # Try environment variables first
    import os
    username = os.getenv("WORDPRESS_USERNAME")
    password = os.getenv("WORDPRESS_APPLICATION_PASSWORD")
    site_url = os.getenv("WORDPRESS_SITE_URL", "https://digitaldreamscape.site")
    
    if username and password:
        return {
            "username": username,
            "password": password,
            "site_url": site_url.rstrip("/")
        }
    
    # Try config file
    config_path = Path("D:/websites/configs/site_configs.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
            site_config = configs.get("digitaldreamscape.site", {})
            if site_config:
                rest_api = site_config.get("rest_api", {})
                return {
                    "username": rest_api.get("username"),
                    "password": rest_api.get("app_password"),
                    "site_url": site_config.get("site_url", "https://digitaldreamscape.site")
                }
    
    # Try .deploy_credentials
    deploy_creds_path = Path("D:/websites/.deploy_credentials/blogging_api.json")
    if deploy_creds_path.exists():
        with open(deploy_creds_path, 'r', encoding='utf-8') as f:
            creds = json.load(f)
            if "digitaldreamscape.site" in creds:
                site_creds = creds["digitaldreamscape.site"]
                return {
                    "username": site_creds.get("username"),
                    "password": site_creds.get("application_password"),
                    "site_url": site_creds.get("site_url", "https://digitaldreamscape.site")
                }
    
    return None


def read_blog_post() -> str:
    """Read the blog post markdown file."""
    blog_file = Path("D:/websites/websites/digitaldreamscape.site/blog/006-the-long-vigil.md")
    if not blog_file.exists():
        print(f"❌ Blog post not found: {blog_file}")
        return None
    
    return blog_file.read_text(encoding='utf-8')


def extract_frontmatter(content: str) -> tuple:
    """Extract frontmatter from markdown and return (metadata, body)."""
    if not content.startswith("---"):
        return {}, content
    
    lines = content.split('\n')
    frontmatter = {}
    body_start = 0
    
    # Find end of frontmatter
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            body_start = i + 1
            break
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    body = '\n'.join(lines[body_start:])
    return frontmatter, body


def post_to_wordpress():
    """Post The Long Vigil to WordPress."""
    print("📝 Posting 'The Long Vigil' to Digital Dreamscape WordPress...\n")
    
    if not HAS_BLOGGING:
        print("❌ Blogging automation tool not available")
        return False
    
    # Load credentials
    creds = load_wordpress_credentials()
    if not creds:
        print("❌ WordPress credentials not found.")
        print("\n📝 To fix this, set environment variables:")
        print("   - WORDPRESS_USERNAME")
        print("   - WORDPRESS_APPLICATION_PASSWORD")
        print("   - WORDPRESS_SITE_URL (optional, defaults to https://digitaldreamscape.site)")
        print("\n   OR create config file:")
        print("   D:/websites/configs/site_configs.json")
        return False
    
    # Read blog post
    content = read_blog_post()
    if not content:
        return False
    
    # Extract frontmatter
    frontmatter, body = extract_frontmatter(content)
    
    # Initialize WordPress client
    client = WordPressBlogClient(
        site_url=creds["site_url"],
        username=creds["username"],
        app_password=creds["password"]
    )
    
    # Check API availability
    print("🔍 Checking WordPress REST API...")
    if not client.check_api_availability():
        print("❌ WordPress REST API not available")
        return False
    print("✅ WordPress REST API available\n")
    
    # Get or create category
    category = frontmatter.get("Category", "World-Building")
    print(f"📁 Category: {category}")
    category_id = client.get_or_create_category(category)
    if not category_id:
        print("⚠️  Could not get/create category, continuing without category")
    else:
        print(f"✅ Category ID: {category_id}\n")
    
    # Get or create tags
    tags_str = frontmatter.get("Tags", "")
    tag_ids = []
    if tags_str:
        tags = [t.strip() for t in tags_str.split(',')]
        print(f"🏷️  Tags: {', '.join(tags)}")
        for tag in tags:
            tag_id = client.get_or_create_tag(tag)
            if tag_id:
                tag_ids.append(tag_id)
        print(f"✅ Created/found {len(tag_ids)} tags\n")
    
    # Convert markdown to HTML
    print("🔄 Converting markdown to HTML...")
    html_content = client.convert_markdown_to_html(body)
    print("✅ Content converted\n")
    
    # Create post
    title = frontmatter.get("title", "The Long Vigil")
    if not title or title == "The Long Vigil":
        title = "The Long Vigil"
    
    print(f"📝 Creating post: '{title}'...")
    
    # Prepare categories and tags as lists of names (client will resolve IDs)
    categories = [category] if category else []
    tags = [t.strip() for t in tags_str.split(',')] if tags_str else []
    
    result = client.create_post(
        title=title,
        content=body,  # Pass markdown, client will convert
        status="publish",  # Publish immediately
        categories=categories,
        tags=tags,
    )
    
    if result and result.get("success"):
        post_id = result.get("post_id")
        post_url = result.get("post_url", f"{creds['site_url']}/wp-admin/post.php?post={post_id}&action=edit")
        print(f"✅ Post created successfully!")
        print(f"   Post ID: {post_id}")
        print(f"   URL: {post_url}")
        print(f"\n🌐 View post: {creds['site_url']}/blog/")
        return True
    else:
        error = result.get("error", "Unknown error") if result else "No response"
        print(f"❌ Failed to create post: {error}")
        return False


if __name__ == "__main__":
    success = post_to_wordpress()
    sys.exit(0 if success else 1)

