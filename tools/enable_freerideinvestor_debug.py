#!/usr/bin/env python3
"""
Enable WordPress Debug Mode for freerideinvestor.com
=====================================================

Enables WordPress debug logging to diagnose HTTP 500 errors.
Adds WP_DEBUG, WP_DEBUG_LOG, and WP_DEBUG_DISPLAY to wp-config.php.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import sys
import json
import paramiko
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def enable_debug_mode(site_key: str = "freerideinvestor") -> bool:
    """Enable WordPress debug mode via SFTP."""
    # Load site config
    config_file = project_root / ".deploy_credentials" / "sites.json"
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return False

    with open(config_file) as f:
        sites = json.load(f)
        config = sites.get(site_key, {})

    if not config:
        print(f"❌ Site '{site_key}' not found in config")
        return False

    host = config.get("host")
    port = config.get("port", 65002)
    username = config.get("username")
    password = config.get("password")
    remote_path = config.get("remote_path", "")

    if not all([host, username, password]):
        print(f"❌ Missing SFTP credentials for {site_key}")
        return False

    # Connect to SFTP
    try:
        transport = paramiko.Transport((host, port))
        transport.banner_timeout = 10
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print(f"✅ Connected to SFTP: {host}:{port}")
    except Exception as e:
        print(f"❌ SFTP connection failed: {e}")
        return False

    # Find wp-config.php
    wp_config_paths = [
        f"{remote_path}/wp-config.php".lstrip('/'),
        "wp-config.php",
        "public_html/wp-config.php",
        f"domains/{site_key}.com/public_html/wp-config.php"
    ]

    wp_config_path = None
    for path in wp_config_paths:
        try:
            sftp.stat(path)
            wp_config_path = path
            print(f"✅ Found wp-config.php: {path}")
            break
        except FileNotFoundError:
            continue

    if not wp_config_path:
        print("❌ wp-config.php not found")
        sftp.close()
        transport.close()
        return False

    # Read wp-config.php
    try:
        with sftp.open(wp_config_path, 'r') as f:
            content = f.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error reading wp-config.php: {e}")
        sftp.close()
        transport.close()
        return False

    # Check if debug mode already enabled
    if "WP_DEBUG" in content and "WP_DEBUG', true" in content.lower():
        print("✅ Debug mode already enabled")
        sftp.close()
        transport.close()
        return True

    # Find insertion point (before "That's all, stop editing!")
    insertion_point = content.find("That's all, stop editing!")
    if insertion_point == -1:
        insertion_point = content.rfind("?>")
        if insertion_point == -1:
            insertion_point = len(content)

    # Prepare debug constants
    debug_constants = """
/* Enable WordPress Debug Mode - Added by Agent-7 */
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
define('WP_MEMORY_LIMIT', '256M');
@ini_set('display_errors', 0);
"""

    # Insert debug constants
    new_content = (
        content[:insertion_point].rstrip() + 
        debug_constants + 
        "\n" + 
        content[insertion_point:]
    )

    # Write back wp-config.php
    try:
        # Create backup first
        backup_path = f"{wp_config_path}.backup"
        try:
            sftp.remove(backup_path)  # Remove old backup if exists
        except:
            pass
        
        with sftp.open(backup_path, 'w') as f:
            f.write(content.encode('utf-8'))
        print(f"✅ Backup created: {backup_path}")

        # Write new content
        with sftp.open(wp_config_path, 'w') as f:
            f.write(new_content.encode('utf-8'))
        print(f"✅ Debug mode enabled in wp-config.php")
        
    except Exception as e:
        print(f"❌ Error writing wp-config.php: {e}")
        sftp.close()
        transport.close()
        return False

    sftp.close()
    transport.close()

    print()
    print("✅ WordPress debug mode enabled successfully!")
    print("💡 Next steps:")
    print("   1. Try accessing the site to generate error logs")
    print("   2. Check wp-content/debug.log for errors")
    print("   3. Run investigation tool again to see errors")

    return True


def main():
    """Main execution."""
    print("🔧 Enabling WordPress Debug Mode for freerideinvestor.com")
    print("=" * 60)
    print()
    
    success = enable_debug_mode("freerideinvestor")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

