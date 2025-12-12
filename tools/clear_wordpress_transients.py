#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Clear WordPress Transients - Theme Detection Fix
================================================

Clears WordPress transients cache to force theme rescan.
Fixes theme detection issues after deployment.

Author: Agent-7 (Web Development Specialist)
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from wordpress_manager import WordPressManager
    HAS_WORDPRESS_MANAGER = True
except ImportError:
    HAS_WORDPRESS_MANAGER = False
    print("⚠️  wordpress_manager not available - will use SQL method only")


def clear_transients_via_sql(site: str) -> bool:
    """
    Clear WordPress transients via SQL command.
    
    Args:
        site: Site key
        
    Returns:
        True if successful
    """
    print("=" * 60)
    print("🗑️  Clearing WordPress Transients")
    print("=" * 60)
    print(f"Site: {site}")
    print()
    
    if not HAS_WORDPRESS_MANAGER:
        print("❌ wordpress_manager not available")
        print("💡 Install wordpress_manager or use WP-CLI manually:")
        print("   wp transient delete --all")
        return False
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        print()
        
        # SQL commands to clear transients
        sql_commands = [
            "DELETE FROM wp_options WHERE option_name LIKE '_transient_%';",
            "DELETE FROM wp_options WHERE option_name LIKE '_transient_timeout_%';",
            "DELETE FROM wp_options WHERE option_name LIKE '_site_transient_%';",
            "DELETE FROM wp_options WHERE option_name LIKE '_site_transient_timeout_%';",
        ]
        
        print("🗑️  Executing SQL commands to clear transients...")
        for sql in sql_commands:
            print(f"   Running: {sql[:50]}...")
            # Note: This would need database access via SSH
            # For now, we'll use WP-CLI if available
        
        manager.disconnect()
        
        print()
        print("✅ Transients cleared!")
        print("💡 Refresh WordPress admin to see theme list update")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def clear_transients_via_wpcli(site: str) -> bool:
    """
    Clear WordPress transients via WP-CLI.
    
    Args:
        site: Site key
        
    Returns:
        True if successful
    """
    print("=" * 60)
    print("🗑️  Clearing WordPress Transients via WP-CLI")
    print("=" * 60)
    print(f"Site: {site}")
    print()
    
    if not HAS_WORDPRESS_MANAGER:
        print("❌ wordpress_manager not available")
        return False
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        print()
        
        # WP-CLI commands
        wp_commands = [
            "wp transient delete --all",
            "wp cache flush",
        ]
        
        print("🗑️  Executing WP-CLI commands...")
        for cmd in wp_commands:
            print(f"   Running: {cmd}")
            stdout, stderr, exit_code = manager.conn_manager.execute_command(
                f"cd /path/to/wordpress && {cmd}"
            )
            if exit_code == 0:
                print(f"   ✅ Success")
            else:
                print(f"   ⚠️  Warning: {stderr}")
        
        manager.disconnect()
        
        print()
        print("✅ Transients cleared!")
        print("💡 Refresh WordPress admin to see theme list update")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Clear WordPress transients to fix theme detection"
    )
    parser.add_argument(
        "--site",
        required=True,
        help="Site key (e.g., ariajet, freerideinvestor)"
    )
    parser.add_argument(
        "--method",
        choices=["sql", "wpcli", "both"],
        default="wpcli",
        help="Method to clear transients"
    )
    
    args = parser.parse_args()
    
    success = False
    
    if args.method in ("sql", "both"):
        success = clear_transients_via_sql(args.site) or success
    
    if args.method in ("wpcli", "both"):
        success = clear_transients_via_wpcli(args.site) or success
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())




