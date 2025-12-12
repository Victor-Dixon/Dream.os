#!/usr/bin/env python3
"""
Check WordPress Debug Log - Read Error Logs
===========================================

Reads WordPress debug.log to identify actual errors.

Author: Agent-3 (Infrastructure & DevOps Specialist)

<!-- SSOT Domain: infrastructure -->
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager


def check_debug_log(site: str, lines: int = 50) -> bool:
    """
    Check WordPress debug.log for errors.
    
    Args:
        site: Site key
        lines: Number of recent lines to read
        
    Returns:
        True if log exists and has content
    """
    print("=" * 60)
    print("📋 Check WordPress Debug Log")
    print("=" * 60)
    print(f"Site: {site}")
    print()
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        print()
        
        # Path to debug.log
        site_config = manager.SITE_CONFIGS.get(site, {})
        remote_base = site_config.get("remote_base", "")
        if remote_base:
            parts = remote_base.split("/")
            if len(parts) >= 3 and parts[0] == "domains":
                domain = parts[1]
                debug_log_path = f"domains/{domain}/public_html/wp-content/debug.log"
            else:
                debug_log_path = "/public_html/wp-content/debug.log"
        else:
            debug_log_path = "/public_html/wp-content/debug.log"
        
        # Check if debug.log exists
        print(f"📖 Reading debug.log...")
        try:
            sftp = manager.conn_manager.sftp
            try:
                sftp.stat(debug_log_path)
                print("✅ debug.log exists")
            except FileNotFoundError:
                print("⚠️  debug.log does not exist yet")
                print("💡 The error may not have occurred since debug mode was enabled")
                print("💡 Try accessing the site to trigger the error")
                manager.disconnect()
                return False
            
            # Read debug.log
            with sftp.open(debug_log_path, 'r') as f:
                all_lines = f.readlines()
                
            if not all_lines:
                print("⚠️  debug.log is empty")
                print("💡 No errors logged yet")
                manager.disconnect()
                return False
            
            # Show recent lines
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            print(f"\n📋 Recent errors (last {len(recent_lines)} lines):")
            print("=" * 60)
            for line in recent_lines:
                print(line.rstrip())
            print("=" * 60)
            
            # Count error types
            fatal_count = sum(1 for line in all_lines if "Fatal error" in line or "fatal error" in line)
            warning_count = sum(1 for line in all_lines if "Warning" in line or "warning" in line)
            notice_count = sum(1 for line in all_lines if "Notice" in line or "notice" in line)
            
            print(f"\n📊 Error Summary:")
            print(f"   Fatal errors: {fatal_count}")
            print(f"   Warnings: {warning_count}")
            print(f"   Notices: {notice_count}")
            
            manager.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Error reading debug.log: {e}")
            manager.disconnect()
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check WordPress debug log")
    parser.add_argument("--site", required=True, help="Site key")
    parser.add_argument("--lines", type=int, default=50, help="Number of lines to show")
    
    args = parser.parse_args()
    success = check_debug_log(args.site, args.lines)
    sys.exit(0 if success else 1)

