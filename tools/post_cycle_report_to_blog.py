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
import markdown
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

def convert_to_html_with_styling(markdown_content):
    """Convert Markdown to HTML and inject professional dark theme styling."""
    
    # Convert MD to HTML
    html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'codehilite'])
    
    # Define Professional Dark Theme Styles (Based on Victor's preference & dadudekc dark theme)
    # Using specific class names to avoid global conflicts, but injecting them into the content container
    
    css = """
    <style>
    .victor-report {
        font-family: 'SF Mono', 'Segoe UI Mono', 'Roboto Mono', Menlo, Courier, monospace;
        line-height: 1.6;
        color: #e8e8e8;
        background-color: #1a1a1a;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #333;
        max-width: 800px;
        margin: 0 auto;
    }
    .victor-report h1, .victor-report h2, .victor-report h3 {
        color: #fff;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    .victor-report h1 { font-size: 2.2rem; border-bottom: 1px solid #333; padding-bottom: 0.5rem; }
    .victor-report h2 { font-size: 1.5rem; color: #4a9eff; }
    .victor-report h3 { font-size: 1.2rem; color: #a0a0a0; }
    
    .victor-report p { margin-bottom: 1.2rem; font-size: 1rem; }
    
    .victor-report ul, .victor-report ol { margin-bottom: 1.2rem; padding-left: 1.5rem; }
    .victor-report li { margin-bottom: 0.5rem; color: #ccc; }
    
    .victor-report code {
        background-color: #2a2a2a;
        color: #ff79c6;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
    }
    
    .victor-report pre {
        background-color: #0f0f0f;
        padding: 1.5rem;
        border-radius: 6px;
        overflow-x: auto;
        border: 1px solid #333;
        margin-bottom: 1.5rem;
    }
    
    .victor-report pre code {
        background-color: transparent;
        color: #f8f8f2;
        padding: 0;
    }
    
    .victor-report .status-block {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    
    .victor-report .status-active { background-color: #28a745; color: white; }
    .victor-report .priority-high { background-color: #ffc107; color: black; }
    
    .victor-report hr {
        border: 0;
        border-top: 1px solid #333;
        margin: 2rem 0;
    }
    </style>
    """
    
    # Wrap content
    wrapped_html = f"""
    {css}
    <div class="victor-report">
        {html_content}
    </div>
    """
    
    return wrapped_html

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
    
    # Convert body (Markdown) to styled HTML
    html_body = convert_to_html_with_styling(body)
    
    result = post_to_wordpress(wp_url, wp_user, wp_password, title, html_body, excerpt, args.status)
    
    if result:
        print(f"✅ Posted successfully! ID: {result.get('id')}")
        print(f"   Link: {result.get('link')}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
