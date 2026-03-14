#!/usr/bin/env python3
"""
Deploy the complete FreeRideInvestor V2 theme to live server
"""

import paramiko
import json
import os
from pathlib import Path

def upload_directory(sftp, local_path, remote_path):
    """Recursively upload a directory"""
    for root, dirs, files in os.walk(local_path):
        # Calculate relative path
        relative_path = os.path.relpath(root, local_path)
        if relative_path == '.':
            current_remote = remote_path
        else:
            current_remote = os.path.join(remote_path, relative_path).replace('\\', '/')

        # Create remote directory
        try:
            sftp.mkdir(current_remote)
        except:
            pass  # Directory might already exist

        # Upload files
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = os.path.join(current_remote, file).replace('\\', '/')
            print(f"  📤 {local_file} -> {remote_file}")
            sftp.put(local_file, remote_file)

def deploy_full_theme():
    # Load credentials
    with open('.deploy_credentials/sites.json', 'r') as f:
        sites = json.load(f)

    site_config = sites['freerideinvestor.com']

    # SFTP connection
    transport = paramiko.Transport((site_config['host'], site_config['port']))
    transport.connect(
        username=site_config['username'],
        password=site_config['password']
    )

    sftp = paramiko.SFTPClient.from_transport(transport)

    # Theme paths
    local_theme = 'sites/freerideinvestor.com/wp/wp-content/themes/freerideinvestor-v2'
    remote_theme_base = f"{site_config['remote_path']}/wp-content/themes"

    # Backup existing theme if it exists
    try:
        sftp.stat(f"{remote_theme_base}/freerideinvestor-v2")
        print("📦 Backing up existing theme...")
        sftp.rename(
            f"{remote_theme_base}/freerideinvestor-v2",
            f"{remote_theme_base}/freerideinvestor-v2.backup"
        )
        print("✅ Backup created")
    except:
        print("ℹ️  No existing theme to backup")

    # Upload the theme
    print("📋 Deploying freerideinvestor-v2 theme...")
    upload_directory(sftp, local_theme, f"{remote_theme_base}/freerideinvestor-v2")
    print("✅ Theme deployment complete!")

    sftp.close()
    transport.close()

    print("\n🎉 Full theme deployment successful!")
    print("\nNext steps:")
    print("1. Activate the 'FreeRideInvestor V2' theme in WordPress admin")
    print("2. The homeUrl JavaScript error should be resolved")
    print("3. Test menu navigation on https://freerideinvestor.com")

if __name__ == "__main__":
    deploy_full_theme()