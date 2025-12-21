#!/usr/bin/env python3
"""
Check PHP Error Logs for freerideinvestor.com
==============================================

Checks for PHP error logs in common locations via SFTP.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import sys
import json
import paramiko
from pathlib import Path
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def check_php_error_logs(site_key: str = "freerideinvestor") -> List[str]:
    """Check for PHP error logs in common locations."""
    # Load site config
    config_file = project_root / ".deploy_credentials" / "sites.json"
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return []

    with open(config_file) as f:
        sites = json.load(f)
        config = sites.get(site_key, {})

    if not config:
        print(f"❌ Site '{site_key}' not found in config")
        return []

    host = config.get("host")
    port = config.get("port", 65002)
    username = config.get("username")
    password = config.get("password")
    remote_path = config.get("remote_path", "")

    if not all([host, username, password]):
        print(f"❌ Missing SFTP credentials for {site_key}")
        return []

    # Connect to SFTP
    try:
        transport = paramiko.Transport((host, port))
        transport.banner_timeout = 10
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print(f"✅ Connected to SFTP: {host}:{port}")
    except Exception as e:
        print(f"❌ SFTP connection failed: {e}")
        return []

    errors_found = []

    # Common PHP error log locations
    error_log_paths = [
        f"{remote_path}/error_log".lstrip('/'),
        f"{remote_path}/php_error_log".lstrip('/'),
        "error_log",
        "php_error_log",
        "public_html/error_log",
        f"domains/{site_key}.com/public_html/error_log",
        f"domains/{site_key}.com/public_html/php_error_log",
        f"domains/{site_key}.com/error_log",
        f"{remote_path}/wp-content/debug.log".lstrip('/'),
        "wp-content/debug.log",
        "public_html/wp-content/debug.log",
        f"domains/{site_key}.com/public_html/wp-content/debug.log",
    ]

    print("\n🔍 Checking for error logs...")
    for log_path in error_log_paths:
        try:
            file_attr = sftp.stat(log_path)
            print(f"✅ Found: {log_path} ({file_attr.st_size} bytes)")
            
            # Read last 50 lines
            try:
                with sftp.open(log_path, 'r') as f:
                    lines = f.readlines()
                    recent_lines = [line.decode('utf-8', errors='ignore').strip() 
                                  for line in lines[-50:]]
                    errors_found.extend(recent_lines)
                    print(f"   Read {len(recent_lines)} recent lines")
            except Exception as e:
                print(f"   ⚠️  Could not read file: {e}")
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"   ⚠️  Error checking {log_path}: {e}")

    sftp.close()
    transport.close()

    if errors_found:
        print(f"\n✅ Found {len(errors_found)} error log entries")
        print("\n📋 Recent errors:")
        for error in errors_found[-20:]:  # Show last 20
            if error.strip():
                print(f"   {error[:200]}...")  # Truncate long lines
    else:
        print("\n⚠️  No error logs found in common locations")

    return errors_found


def main():
    """Main execution."""
    print("🔍 Checking PHP Error Logs for freerideinvestor.com")
    print("=" * 60)
    
    errors = check_php_error_logs("freerideinvestor")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

