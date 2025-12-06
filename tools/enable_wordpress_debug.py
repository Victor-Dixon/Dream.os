#!/usr/bin/env python3
"""
Enable WordPress Debug Mode - Error Detection
==============================================

Enables WordPress debug mode to capture runtime errors.
Helps identify fatal errors preventing theme detection.

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
    print("⚠️  wordpress_manager not available")


def enable_debug_mode(site: str, enable: bool = True) -> bool:
    """
    Enable or disable WordPress debug mode.
    
    Args:
        site: Site key
        enable: True to enable, False to disable
        
    Returns:
        True if successful
    """
    action = "Enable" if enable else "Disable"
    print("=" * 60)
    print(f"🔧 {action} WordPress Debug Mode")
    print("=" * 60)
    print(f"Site: {site}")
    print()
    
    if not HAS_WORDPRESS_MANAGER:
        print("❌ wordpress_manager not available")
        print("💡 Manual method:")
        print("   1. Edit wp-config.php")
        print("   2. Add: define('WP_DEBUG', true);")
        print("   3. Add: define('WP_DEBUG_LOG', true);")
        print("   4. Add: define('WP_DEBUG_DISPLAY', false);")
        return False
    
    try:
        manager = WordPressManager(site)
        
        if not manager.connect():
            print("❌ Failed to connect to server")
            return False
        
        print("📡 Connected to server")
        print()
        
        # Path to wp-config.php
        wp_config_path = "/public_html/wp-config.php"
        
        # Read current wp-config.php
        print(f"📖 Reading wp-config.php...")
        try:
            sftp = manager.conn_manager.sftp
            with sftp.open(wp_config_path, 'r') as f:
                content = f.read().decode('utf-8')
        except Exception as e:
            print(f"❌ Error reading wp-config.php: {e}")
            manager.disconnect()
            return False
        
        # Check if debug is already set
        has_debug = "define('WP_DEBUG'" in content or 'define("WP_DEBUG"' in content
        
        if enable and has_debug:
            print("✅ Debug mode already enabled")
            manager.disconnect()
            return True
        
        if not enable and not has_debug:
            print("✅ Debug mode already disabled")
            manager.disconnect()
            return True
        
        # Add or modify debug constants
        debug_lines = [
            "define('WP_DEBUG', true);",
            "define('WP_DEBUG_LOG', true);",
            "define('WP_DEBUG_DISPLAY', false);",
            "@ini_set('display_errors', 0);"
        ]
        
        if enable:
            # Find insertion point (before "That's all, stop editing!")
            if "/* That's all, stop editing!" in content:
                insertion_point = content.find("/* That's all, stop editing!")
                new_content = content[:insertion_point]
                new_content += "\n// Enable WordPress debug mode\n"
                new_content += "\n".join(debug_lines) + "\n\n"
                new_content += content[insertion_point:]
            else:
                # Add at end of file
                new_content = content.rstrip() + "\n\n"
                new_content += "// Enable WordPress debug mode\n"
                new_content += "\n".join(debug_lines) + "\n"
        else:
            # Remove debug lines
            new_content = content
            for line in debug_lines:
                new_content = new_content.replace(line + "\n", "")
                new_content = new_content.replace(line, "")
        
        # Write back
        print(f"📝 Writing wp-config.php...")
        try:
            with sftp.open(wp_config_path, 'w') as f:
                f.write(new_content.encode('utf-8'))
            print("✅ wp-config.php updated")
        except Exception as e:
            print(f"❌ Error writing wp-config.php: {e}")
            manager.disconnect()
            return False
        
        manager.disconnect()
        
        print()
        if enable:
            print("✅ Debug mode enabled!")
            print("💡 Check wp-content/debug.log for errors")
        else:
            print("✅ Debug mode disabled!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enable/disable WordPress debug mode"
    )
    parser.add_argument(
        "--site",
        required=True,
        help="Site key (e.g., ariajet, freerideinvestor)"
    )
    parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable debug mode (default: enable)"
    )
    
    args = parser.parse_args()
    
    success = enable_debug_mode(args.site, enable=not args.disable)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())




