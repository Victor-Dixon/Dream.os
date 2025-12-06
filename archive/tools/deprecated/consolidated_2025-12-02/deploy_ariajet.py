#!/usr/bin/env python3
"""
Deploy ariajet.site - Static HTML Site Deployment
================================================

Deploys static HTML files to ariajet.site hosting.

Author: Agent-1 (Integration & Core Systems Specialist)
"""

import json
import sys
from pathlib import Path

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False
    print("❌ paramiko not installed. Install with: pip install paramiko")
    sys.exit(1)


def load_credentials():
    """Load deployment credentials."""
    creds_file = Path(
        "D:/Agent_Cellphone_V2_Repository/.deploy_credentials/sites.json")
    if not creds_file.exists():
        print("❌ Credentials file not found. Checking for ariajet config...")
        return None

    with open(creds_file) as f:
        return json.load(f)


def deploy_file_via_sftp(local_path: Path, remote_path: str, host: str,
                         username: str, password: str, port: int = 22):
    """Deploy file via SFTP."""
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Create remote directory if needed
        remote_dir = '/'.join(remote_path.split('/')[:-1])
        try:
            sftp.mkdir(remote_dir)
        except:
            pass  # Directory might already exist

        # Upload file
        sftp.put(str(local_path), remote_path)
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(f"❌ SFTP Error: {e}")
        return False


def deploy_ariajet():
    """Deploy ariajet.site files."""
    local_file = Path("D:/websites/ariajet.site/index.html")

    if not local_file.exists():
        print(f"❌ Local file not found: {local_file}")
        return False

    # Get credentials
    creds = load_credentials()
    if not creds:
        print("⚠️  No credentials file found. Creating template...")
        creds = {}

    # Get ariajet config
    aria_config = creds.get("ariajet") or creds.get("ariajet.site") or {}

    # Prompt for credentials if missing
    if not aria_config.get("host") or not aria_config.get("username") or not aria_config.get("password"):
        print("📋 SFTP credentials needed for ariajet.site deployment")
        print("   Please provide the following:")
        print()

        host = input("   Host (e.g., ftp.ariajet.site): ").strip()
        username = input("   Username: ").strip()
        password = input("   Password: ").strip()

        if not all([host, username, password]):
            print("❌ All credentials are required")
            return False

        # Save credentials for future use
        aria_config = {
            "host": host,
            "username": username,
            "password": password,
            "remote_path": "/public_html"
        }

        # Update and save credentials file
        creds["ariajet"] = aria_config
        creds["ariajet.site"] = aria_config

        creds_file = Path(
            "D:/Agent_Cellphone_V2_Repository/.deploy_credentials/sites.json")
        creds_file.parent.mkdir(parents=True, exist_ok=True)
        with open(creds_file, 'w') as f:
            json.dump(creds, f, indent=2)
        print("✅ Credentials saved for future deployments")
        print()

    host = aria_config.get("host")
    username = aria_config.get("username")
    password = aria_config.get("password")
    remote_base = aria_config.get("remote_path", "/public_html")

    print(f"🚀 Deploying ariajet.site...")
    print(f"   Host: {host}")
    print(f"   Remote: {remote_base}")
    print()

    # Deploy index.html
    remote_path = f"{remote_base}/index.html"
    print(f"📤 Deploying index.html...")

    if deploy_file_via_sftp(local_file, remote_path, host, username, password):
        print(f"   ✅ index.html deployed successfully")
        print()
        print(f"✅ Deployment complete! Check https://ariajet.site/")
        return True
    else:
        print(f"   ❌ Failed to deploy index.html")
        return False


if __name__ == '__main__':
    success = deploy_ariajet()
    sys.exit(0 if success else 1)
