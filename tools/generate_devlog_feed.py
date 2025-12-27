#!/usr/bin/env python3
"""
Public Build Feed Generator
============================

Generates a JSON Feed from devlogs for weareswarm.online public build updates.

This tool scans agent workspace devlogs and generates a public-facing feed
that showcases the swarm's build-in-public progress.

Usage:
    python tools/generate_devlog_feed.py [--output feed.json] [--limit 50] [--public-only]

Output:
    Generates JSON Feed format (https://jsonfeed.org/) compatible with web consumption.
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


@dataclass
class DevlogEntry:
    """Structured devlog entry for feed."""
    title: str
    content: str
    date: str
    agent_id: str
    file_path: str
    public_build_signal: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class DevlogParser:
    """Parser for extracting structured data from devlog markdown files."""
    
    def __init__(self, public_only: bool = True):
        """
        Initialize parser.
        
        Args:
            public_only: If True, only include devlogs with "Public Build Signal" section
        """
        self.public_only = public_only
    
    def parse_devlog(self, file_path: Path) -> Optional[DevlogEntry]:
        """
        Parse a devlog markdown file into structured data.
        
        Args:
            file_path: Path to devlog markdown file
            
        Returns:
            DevlogEntry if parseable, None otherwise
        """
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"⚠️  Failed to read {file_path}: {e}")
            return None
        
        # Extract metadata
        agent_id = self._extract_agent_id(file_path, content)
        date = self._extract_date(file_path, content)
        title = self._extract_title(content, file_path)
        public_build_signal = self._extract_public_build_signal(content)
        tags = self._extract_tags(content)
        
        # Filter if public_only and no public build signal
        if self.public_only and not public_build_signal:
            return None
        
        return DevlogEntry(
            title=title,
            content=content,
            date=date,
            agent_id=agent_id,
            file_path=str(file_path.relative_to(project_root)),
            public_build_signal=public_build_signal,
            tags=tags
        )
    
    def _extract_agent_id(self, file_path: Path, content: str) -> str:
        """Extract agent ID from filename or content."""
        # Try filename pattern: YYYY-MM-DD_agent-X_*.md
        filename_match = re.search(r'agent[_-]?(\d+)', file_path.name, re.IGNORECASE)
        if filename_match:
            return f"Agent-{filename_match.group(1)}"
        
        # Try content: **Agent:** Agent-X
        content_match = re.search(r'\*\*Agent:\*\*\s*(Agent[_-]?\d+)', content, re.IGNORECASE)
        if content_match:
            return content_match.group(1).replace('_', '-')
        
        # Try content: [AGENT-X]
        bracket_match = re.search(r'\[AGENT[_-]?(\d+)\]', content, re.IGNORECASE)
        if bracket_match:
            return f"Agent-{bracket_match.group(1)}"
        
        return "Unknown"
    
    def _extract_date(self, file_path: Path, content: str) -> str:
        """Extract date from filename or content."""
        # Try filename pattern: YYYY-MM-DD_*.md
        filename_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.name)
        if filename_match:
            return filename_match.group(1)
        
        # Try content: **Date:** YYYY-MM-DD
        content_match = re.search(r'\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
        if content_match:
            return content_match.group(1)
        
        # Fallback to file modification time
        try:
            mtime = file_path.stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_title(self, content: str, file_path: Path) -> str:
        """Extract title from content or filename."""
        # Try first # heading
        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            title = heading_match.group(1).strip()
            # Remove [AGENT-X] prefix if present
            title = re.sub(r'^\[AGENT[_-]?\d+\]\s*', '', title, flags=re.IGNORECASE)
            return title
        
        # Fallback to filename without extension
        return file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    def _extract_public_build_signal(self, content: str) -> Optional[str]:
        """Extract Public Build Signal section if present."""
        # Look for "Public Build Signal" section
        pattern = r'(?:Public Build Signal|PUBLIC BUILD SIGNAL)[:\-]?\s*\n\s*[-*]?\s*(.+?)(?:\n\n|\n##|\Z)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            signal = match.group(1).strip()
            # Clean up markdown formatting
            signal = re.sub(r'^\s*[-*]\s*', '', signal, flags=re.MULTILINE)
            signal = re.sub(r'\*\*', '', signal)
            return signal.strip()
        return None
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content (hashtags or explicit tags)."""
        tags = []
        
        # Extract hashtags
        hashtags = re.findall(r'#([\w-]+)', content)
        tags.extend(hashtags)
        
        # Extract explicit tags section
        tags_match = re.search(r'(?:Tags|TAGS)[:\-]?\s*\n\s*(.+?)(?:\n\n|\n##|\Z)', content, re.IGNORECASE)
        if tags_match:
            tag_text = tags_match.group(1)
            explicit_tags = re.findall(r'[\w-]+', tag_text)
            tags.extend(explicit_tags)
        
        # Remove duplicates and normalize
        return sorted(list(set(t.lower() for t in tags if t)))


class DevlogFeedGenerator:
    """Generator for JSON Feed format from devlogs."""
    
    def __init__(self, feed_title: str = "Swarm Build Updates", feed_url: str = "https://weareswarm.online/feed.json"):
        """
        Initialize feed generator.
        
        Args:
            feed_title: Title of the feed
            feed_url: URL where feed will be hosted
        """
        self.feed_title = feed_title
        self.feed_url = feed_url
        self.feed_home_page_url = feed_url.replace('/feed.json', '')
    
    def generate_feed(self, entries: List[DevlogEntry], limit: int = 50) -> Dict[str, Any]:
        """
        Generate JSON Feed format from devlog entries.
        
        Args:
            entries: List of devlog entries (should be sorted by date desc)
            limit: Maximum number of entries to include
            
        Returns:
            JSON Feed dictionary
        """
        # Sort by date (most recent first) and limit
        sorted_entries = sorted(entries, key=lambda e: e.date, reverse=True)[:limit]
        
        # Generate feed items
        items = []
        for entry in sorted_entries:
            item = {
                "id": f"{entry.date}-{entry.agent_id}-{Path(entry.file_path).stem}",
                "title": entry.title,
                "content_html": self._markdown_to_html(entry.content),
                "content_text": self._markdown_to_text(entry.content),
                "date_published": f"{entry.date}T00:00:00Z",
                "authors": [{"name": entry.agent_id}],
                "tags": entry.tags,
                "url": f"{self.feed_home_page_url}/devlogs/{Path(entry.file_path).stem}",
            }
            
            # Add public build signal as summary if present
            if entry.public_build_signal:
                item["summary"] = entry.public_build_signal
            
            items.append(item)
        
        # Build feed
        feed = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": self.feed_title,
            "home_page_url": self.feed_home_page_url,
            "feed_url": self.feed_url,
            "description": "Public build updates from the Swarm agent collective",
            "icon": f"{self.feed_home_page_url}/icon.png",
            "favicon": f"{self.feed_home_page_url}/favicon.ico",
            "authors": [
                {
                    "name": "Swarm Collective",
                    "url": self.feed_home_page_url
                }
            ],
            "language": "en-US",
            "items": items
        }
        
        return feed
    
    def _markdown_to_html(self, markdown: str) -> str:
        """Convert markdown to HTML (basic conversion)."""
        # Basic markdown conversion (could use markdown library for full support)
        html = markdown
        
        # Headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Italic
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        
        # Code blocks
        html = re.sub(r'```([\w]+)?\n(.+?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        
        # Line breaks
        html = html.replace('\n\n', '</p><p>')
        html = f'<p>{html}</p>'
        
        # Lists (basic)
        html = re.sub(r'^[-*]\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        return html
    
    def _markdown_to_text(self, markdown: str) -> str:
        """Convert markdown to plain text."""
        text = markdown
        
        # Remove markdown formatting
        text = re.sub(r'#+\s+', '', text)  # Headers
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links
        text = re.sub(r'`(.+?)`', r'\1', text)  # Code
        text = re.sub(r'```[\w]*\n(.+?)```', r'\1', text, flags=re.DOTALL)  # Code blocks
        
        return text.strip()


def scan_devlogs(devlogs_dir: Path, public_only: bool = True) -> List[DevlogEntry]:
    """
    Scan devlogs directory and parse all devlogs.
    
    Args:
        devlogs_dir: Root directory containing agent workspaces
        public_only: Only include devlogs with public build signals
        
    Returns:
        List of parsed devlog entries
    """
    parser = DevlogParser(public_only=public_only)
    entries = []
    
    # Scan agent_workspaces/*/devlogs/
    workspaces_dir = devlogs_dir / "agent_workspaces"
    if not workspaces_dir.exists():
        print(f"⚠️  Workspaces directory not found: {workspaces_dir}")
        return entries
    
    devlog_dirs = list(workspaces_dir.glob("Agent-*/devlogs"))
    if not devlog_dirs:
        print(f"⚠️  No devlog directories found in {workspaces_dir}")
        return entries
    
    print(f"📁 Scanning {len(devlog_dirs)} devlog directories...")
    
    for devlog_dir in devlog_dirs:
        devlog_files = list(devlog_dir.glob("*.md"))
        print(f"  Found {len(devlog_files)} devlogs in {devlog_dir.name}")
        
        for devlog_file in devlog_files:
            entry = parser.parse_devlog(devlog_file)
            if entry:
                entries.append(entry)
                if len(entries) % 10 == 0:
                    print(f"  ✅ Parsed {len(entries)} devlogs...")
    
    print(f"✅ Total devlogs parsed: {len(entries)}")
    return entries


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate public build feed from devlogs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate feed.json with all public devlogs
  python tools/generate_devlog_feed.py --output feed.json
  
  # Generate feed with last 100 entries (include non-public)
  python tools/generate_devlog_feed.py --output feed.json --limit 100 --all
  
  # Generate feed for weareswarm.online
  python tools/generate_devlog_feed.py --output runtime/feeds/weareswarm_feed.json
        """
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runtime/feeds/public_build_feed.json"),
        help="Output path for feed JSON file (default: runtime/feeds/public_build_feed.json)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of entries to include (default: 50)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all devlogs (not just those with public build signals)"
    )
    
    parser.add_argument(
        "--feed-url",
        default="https://weareswarm.online/feed.json",
        help="URL where feed will be hosted (default: https://weareswarm.online/feed.json)"
    )
    
    parser.add_argument(
        "--root-dir",
        type=Path,
        default=project_root,
        help="Root directory containing agent_workspaces (default: project root)"
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Scan devlogs
    entries = scan_devlogs(args.root_dir, public_only=not args.all)
    
    if not entries:
        print("❌ No devlogs found matching criteria")
        sys.exit(1)
    
    # Generate feed
    generator = DevlogFeedGenerator(feed_url=args.feed_url)
    feed = generator.generate_feed(entries, limit=args.limit)
    
    # Write feed
    args.output.write_text(json.dumps(feed, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"✅ Feed generated: {args.output}")
    print(f"   Entries: {len(feed['items'])}")
    print(f"   Feed URL: {args.feed_url}")
    print(f"   Home URL: {feed['home_page_url']}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()

