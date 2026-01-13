#!/usr/bin/env python3
"""
Remote Analytics Deployment Tool
Deploys GA4/Pixel analytics configuration to WordPress sites

Usage:
python tools/deploy_analytics_remote.py --site freerideinvestor.com
python tools/deploy_analytics_remote.py --site tradingrobotplug.com
python tools/deploy_analytics_remote.py --all
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Optional

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    print("❌ paramiko not available. Install with: pip install paramiko")
    sys.exit(1)

# Repository root
REPO_ROOT = Path(__file__).resolve().parents[1]

def load_credentials() -> Dict[str, Dict]:
    """Load deployment credentials from various sources."""
    credentials = {}

    # Try to load from environment variables (Hostinger)
    host = os.getenv("HOSTINGER_HOST")
    username = os.getenv("HOSTINGER_USER")
    password = os.getenv("HOSTINGER_PASS")
    port = int(os.getenv("HOSTINGER_PORT", "65002"))

    if all([host, username, password]):
        credentials["default"] = {
            "host": host,
            "username": username,
            "password": password,
            "port": port
        }
        print("✅ Loaded credentials from environment variables")
    else:
        print("⚠️  No credentials found in environment variables")
        return {}

    return credentials

def deploy_analytics_config(site_key: str, credentials: Dict) -> bool:
    """
    Deploy analytics configuration to remote WordPress site.

    Args:
        site_key: Site domain (e.g., 'freerideinvestor.com')
        credentials: SFTP credentials dictionary

    Returns:
        bool: Success status
    """
    print(f"\n🚀 Deploying analytics config to {site_key}")

    # Check if local config file exists
    local_config_path = REPO_ROOT / "sites" / site_key / f"wp-config-analytics.php"
    if not local_config_path.exists():
        print(f"❌ Local config file not found: {local_config_path}")
        return False

    # Get credentials for this site
    site_creds = credentials.get(site_key) or credentials.get("default")
    if not site_creds:
        print(f"❌ No credentials available for {site_key}")
        return False

    try:
        # Establish SFTP connection
        print(f"📡 Connecting to {site_creds['host']}:{site_creds['port']} as {site_creds['username']}")

        transport = paramiko.Transport((site_creds['host'], site_creds['port']))
        transport.connect(
            username=site_creds['username'],
            password=site_creds['password']
        )

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload the analytics config file
        remote_path = f"/home/{site_key}/public_html/wp-config-analytics.php"

        print(f"📤 Uploading {local_config_path} to {remote_path}")
        sftp.put(str(local_config_path), remote_path)

        # Verify the upload
        try:
            remote_stat = sftp.stat(remote_path)
            print(f"✅ Upload successful - {remote_stat.st_size} bytes")
        except Exception as e:
            print(f"⚠️  Upload completed but verification failed: {e}")

        sftp.close()
        transport.close()

        print(f"✅ Successfully deployed analytics config to {site_key}")
        return True

    except Exception as e:
        print(f"❌ Deployment failed for {site_key}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Deploy analytics configuration to WordPress sites")
    parser.add_argument("--site", help="Specific site to deploy to")
    parser.add_argument("--all", action="store_true", help="Deploy to all configured sites")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deployed without actually deploying")

    args = parser.parse_args()

    # Load credentials
    credentials = load_credentials()
    if not credentials:
        print("❌ No deployment credentials available")
        return 1

    # Determine target sites
    target_sites = []
    if args.site:
        target_sites = [args.site]
    elif args.all:
        # Deploy to sites that have local analytics configs
        sites_dir = REPO_ROOT / "sites"
        if sites_dir.exists():
            for site_dir in sites_dir.iterdir():
                if site_dir.is_dir():
                    config_file = site_dir / "wp-config-analytics.php"
                    if config_file.exists():
                        target_sites.append(site_dir.name)
    else:
        print("❌ Specify --site <domain> or --all")
        return 1

    if not target_sites:
        print("❌ No target sites found")
        return 1

    print(f"🎯 Target sites: {', '.join(target_sites)}")

    if args.dry_run:
        print("🔍 DRY RUN - Would deploy to:")
        for site in target_sites:
            config_path = REPO_ROOT / "sites" / site / "wp-config-analytics.php"
            if config_path.exists():
                print(f"  - {site}: {config_path}")
        return 0

    # Execute deployments
    success_count = 0
    for site in target_sites:
        if deploy_analytics_config(site, credentials):
            success_count += 1

    print(f"\n📊 Deployment Summary: {success_count}/{len(target_sites)} sites successful")

    if success_count == len(target_sites):
        print("✅ All deployments completed successfully")
        return 0
    else:
        print("⚠️  Some deployments failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())