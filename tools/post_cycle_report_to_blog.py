#!/usr/bin/env python3
"""
Post Cycle Report to Blog
=========================

Reads a cycle accomplishment report (Markdown with frontmatter) and posts it to a WordPress site.
Uses standard WordPress REST API.

Usage:
    python tools/post_cycle_report_to_blog.py --file docs/blog/cycle_accomplishments_2025-12-28.md --site dadudekc.com
"""

import os
import sys
import argparse
import re
import json
import base64
import requests
from pathlib import Path
from datetime import datetime

def parse_frontmatter(content):
    """Parse Jekyll-style frontmatter from markdown content."""
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_block = parts[1]
            body = parts[2].strip()
            
            for line in yaml_block.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle arrays
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip() for v in value[1:-1].split(',')]
                    
                    frontmatter[key] = value
                    
    return frontmatter, body

def post_to_wordpress(site_url, username, password, title, content, excerpt="", status="draft", tags=None, categories=None):
    """Post content to WordPress via REST API."""
    
    # Ensure URL ends with slash
    if not site_url.endswith('/'):
        site_url += '/'
        
    api_url = f"{site_url}wp-json/wp/v2/posts"
    
    # Create auth header
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }
    
    # Prepare payload
    payload = {
        'title': title,
        'content': content,
        'status': status,
        'excerpt': excerpt
    }
    
    # Add tags/categories logic here if needed (requires resolving IDs first usually)
    # For now, we'll skip tag mapping to keep it simple, or implement it if critical.
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to WordPress: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Post cycle report to blog")
    parser.add_argument("--file", required=True, help="Path to markdown file with frontmatter")
    parser.add_argument("--site", help="Site domain (e.g. dadudekc.com)")
    parser.add_argument("--url", help="WordPress URL (if not using predefined sites)")
    parser.add_argument("--user", help="WordPress Username")
    parser.add_argument("--password", help="WordPress Application Password")
    parser.add_argument("--status", default="draft", help="Post status (draft/publish)")
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
        
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    frontmatter, body = parse_frontmatter(content)
    
    title = frontmatter.get('title', f"Cycle Report - {datetime.now().strftime('%Y-%m-%d')}")
    excerpt = frontmatter.get('excerpt', "")
    
    # Determine credentials
    wp_url = args.url
    wp_user = args.user
    wp_password = args.password
    
    # Try loading from env or credentials file if not provided
    if not wp_url or not wp_user or not wp_password:
        # Check env vars
        wp_url = wp_url or os.getenv("WORDPRESS_URL")
        wp_user = wp_user or os.getenv("WORDPRESS_USER")
        wp_password = wp_password or os.getenv("WORDPRESS_APP_PASSWORD")
        
        # If still missing, try .deploy_credentials/blogging_api.json (mocking the missing unified tool logic)
        cred_file = Path(".deploy_credentials/blogging_api.json")
        if (not wp_url or not wp_user or not wp_password) and cred_file.exists():
            try:
                with open(cred_file, 'r') as f:
                    creds = json.load(f)
                    
                site_key = args.site or "dadudekc.com" # Default
                
                if site_key in creds:
                    site_creds = creds[site_key]
                    wp_url = wp_url or site_creds.get("url")
                    wp_user = wp_user or site_creds.get("username")
                    wp_password = wp_password or site_creds.get("password")
            except Exception as e:
                print(f"⚠️ Error reading credentials file: {e}")

    if not wp_url or not wp_user or not wp_password:
        print("❌ Missing WordPress credentials. Provide via args, env vars, or .deploy_credentials/blogging_api.json")
        sys.exit(1)
        
    print(f"🚀 Posting '{title}' to {wp_url}...")
    result = post_to_wordpress(wp_url, wp_user, wp_password, title, body, excerpt, args.status)
    
    if result:
        print(f"✅ Posted successfully! ID: {result.get('id')}")
        print(f"   Link: {result.get('link')}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
