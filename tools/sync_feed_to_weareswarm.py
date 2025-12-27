#!/usr/bin/env python3
"""
Sync Devlog Feed to WeAreSwarm.Online
=====================================

Uploads generated feed JSON to weareswarm.online WordPress site.

Usage:
    python tools/sync_feed_to_weareswarm.py [--feed feed.json] [--dry-run]
"""

import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

load_dotenv(project_root / ".env")

try:
    from src.control_plane.adapters.hostinger.weareswarm_adapter import (
        WeAreSwarmHostingerAdapter,
        get_weareswarm_adapter,
    )
    ADAPTER_AVAILABLE = True
except ImportError:
    ADAPTER_AVAILABLE = False
    print("⚠️  WordPress adapter not available")


def sync_feed(feed_path: Path, dry_run: bool = False) -> bool:
    """
    Sync feed file to weareswarm.online.
    
    Args:
        feed_path: Path to feed JSON file
        dry_run: If True, don't actually upload
        
    Returns:
        True if successful
    """
    if not feed_path.exists():
        print(f"❌ Feed file not found: {feed_path}")
        return False
    
    if not ADAPTER_AVAILABLE:
        print("❌ WordPress adapter not available")
        return False
    
    if dry_run:
        print(f"🧪 DRY RUN: Would upload {feed_path} to weareswarm.online")
        print(f"   Feed size: {feed_path.stat().st_size} bytes")
        return True
    
    # For now, we'll use FTP or direct file upload
    # The adapter doesn't have file upload capability yet
    # This is a placeholder for future implementation
    
    print("⚠️  Direct file upload not yet implemented in adapter")
    print(f"   Feed file: {feed_path}")
    print(f"   File size: {feed_path.stat().st_size} bytes")
    print("\n   To manually upload:")
    print(f"   1. Upload {feed_path} to: /wp-content/themes/runtime/feeds/public_build_feed.json")
    print(f"   2. Or use FTP/SFTP to upload to weareswarm.online")
    print(f"   3. Or configure WordPress REST API with file upload capability")
    
    return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sync devlog feed to weareswarm.online",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync feed (dry run)
  python tools/sync_feed_to_weareswarm.py --dry-run
  
  # Sync specific feed file
  python tools/sync_feed_to_weareswarm.py --feed runtime/feeds/public_build_feed.json
        """
    )
    
    parser.add_argument(
        "--feed",
        type=Path,
        default=Path("runtime/feeds/public_build_feed.json"),
        help="Path to feed JSON file (default: runtime/feeds/public_build_feed.json)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually upload, just show what would be done"
    )
    
    args = parser.parse_args()
    
    # Generate feed if it doesn't exist
    if not args.feed.exists():
        print(f"⚠️  Feed file not found: {args.feed}")
        print("   Generating feed first...")
        from tools.generate_devlog_feed import main as generate_main
        import sys as sys_module
        sys_module.argv = ["generate_devlog_feed.py", "--output", str(args.feed)]
        generate_main()
    
    # Sync feed
    success = sync_feed(args.feed, dry_run=args.dry_run)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

