#!/usr/bin/env python3
"""
Sync Devlog Feed to weareswarm.online

Generates JSON Feed format from devlogs and deploys to WordPress site.

Usage:
    python tools/sync_feed_to_weareswarm.py [--limit N] [--dry-run]

SSOT Domain: web
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add websites tools to path
WEBSITES_PATH = Path("D:/websites")
sys.path.insert(0, str(WEBSITES_PATH / "tools"))
sys.path.insert(0, str(WEBSITES_PATH / "ops" / "deployment"))

try:
    from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
    HAS_DEPLOYER = True
except ImportError:
    HAS_DEPLOYER = False
    print("⚠️  SimpleWordPressDeployer not available - deployment will be skipped")


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEVLOGS_DIR = PROJECT_ROOT / "devlogs"
FEED_OUTPUT = PROJECT_ROOT / "public_build_feed.json"
SITE_KEY = "weareswarm.online"
# Use wp-content/uploads for easier access (directory always exists)
REMOTE_FEED_PATH = "wp-content/uploads/public_build_feed.json"


def parse_devlog_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Parse a devlog markdown file and extract structured data."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"⚠️  Failed to read {file_path.name}: {e}")
        return None
    
    # Extract filename metadata
    filename = file_path.stem
    parts = filename.split('_', 2)
    
    if len(parts) < 2:
        return None
    
    date_str = parts[0]
    agent_id = parts[1] if len(parts) > 1 else "Unknown"
    topic = parts[2] if len(parts) > 2 else "Update"
    
    # Parse date
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_published = date_obj.isoformat() + "Z"
    except ValueError:
        date_published = datetime.now().isoformat() + "Z"
    
    # Extract title (first # heading or filename)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = topic.replace('_', ' ').title()
    
    # Extract summary (first paragraph after title or first 200 chars)
    lines = content.split('\n')
    summary = ""
    in_summary = False
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('##'):
            break
        if line:
            summary = line[:200]
            break
    
    if not summary:
        summary = content[:200].strip()
    
    # Extract tags (agent ID, date-based tags)
    tags = [agent_id.lower(), f"devlog-{date_str}"]
    
    # Generate URL (GitHub devlogs path)
    url = f"https://github.com/Victor-Dixon/Dream.os/tree/main/devlogs/{file_path.name}"
    
    return {
        "id": f"devlog-{filename}",
        "title": title,
        "url": url,
        "date_published": date_published,
        "date_modified": date_published,
        "authors": [{"name": agent_id}],
        "summary": summary,
        "content_html": content.replace('\n', '<br>\n'),
        "tags": tags,
    }


def generate_feed(limit: int = 50) -> Dict[str, Any]:
    """Generate JSON Feed from devlog files."""
    if not DEVLOGS_DIR.exists():
        print(f"❌ Devlogs directory not found: {DEVLOGS_DIR}")
        return {}
    
    # Find all devlog files
    devlog_files = sorted(
        DEVLOGS_DIR.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if not devlog_files:
        print("⚠️  No devlog files found")
        return {}
    
    # Parse devlogs
    items = []
    for file_path in devlog_files[:limit]:
        item = parse_devlog_file(file_path)
        if item:
            items.append(item)
    
    # Build feed structure (JSON Feed 1.1 format)
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Swarm Build Feed",
        "description": "Real-time updates from the Swarm. No polish. Just progress.",
        "home_page_url": "https://weareswarm.online",
        "feed_url": f"https://weareswarm.online/wp-content/uploads/public_build_feed.json",
        "items": items,
    }
    
    return feed


def deploy_feed(feed_data: Dict[str, Any], dry_run: bool = False) -> bool:
    """Deploy feed JSON to WordPress site."""
    if not HAS_DEPLOYER:
        print("⚠️  Deployer not available - skipping deployment")
        return False
    
    if dry_run:
        print("🔍 DRY RUN: Would deploy feed to WordPress")
        return True
    
    # Save feed locally first
    FEED_OUTPUT.write_text(json.dumps(feed_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Feed saved locally: {FEED_OUTPUT}")
    
    # Deploy to WordPress
    try:
        configs = load_site_configs()
        deployer = SimpleWordPressDeployer(SITE_KEY, configs)
        
        if not deployer.connect():
            print(f"❌ Failed to connect to {SITE_KEY}")
            return False
        
        # Ensure remote directory exists (create runtime/feeds if needed)
        remote_dir = "wp-content/themes/runtime/feeds"
        
        # Deploy the feed file
        if deployer.deploy_file(FEED_OUTPUT, REMOTE_FEED_PATH):
            print(f"✅ Feed deployed to {SITE_KEY}: {REMOTE_FEED_PATH}")
            deployer.disconnect()
            return True
        else:
            print(f"❌ Failed to deploy feed")
            deployer.disconnect()
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sync devlog feed to weareswarm.online"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of feed items (default: 50)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate feed without deploying"
    )
    
    args = parser.parse_args()
    
    print("🔄 Generating feed from devlogs...")
    feed = generate_feed(limit=args.limit)
    
    if not feed or not feed.get("items"):
        print("❌ No feed items generated")
        return 1
    
    print(f"✅ Generated feed with {len(feed['items'])} items")
    
    if not args.dry_run:
        if deploy_feed(feed, dry_run=False):
            print("✅ Feed sync complete!")
            return 0
        else:
            print("❌ Feed sync failed")
            return 1
    else:
        print("🔍 DRY RUN: Feed generated but not deployed")
        print(f"   Feed preview: {len(feed['items'])} items")
        return 0


if __name__ == "__main__":
    sys.exit(main())

