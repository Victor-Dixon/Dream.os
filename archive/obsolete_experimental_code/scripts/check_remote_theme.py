#!/usr/bin/env python3
"""
Check what theme directories exist on the live freerideinvestor.com server
"""

import paramiko
import json

def check_remote_theme():
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

    remote_path = site_config['remote_path']
    themes_path = f"{remote_path}/wp-content/themes"

    try:
        print(f"🔍 Checking themes directory: {themes_path}")
        themes = sftp.listdir(themes_path)
        print("📁 Available themes:")
        for theme in themes:
            print(f"   - {theme}")

        # Check if freerideinvestor-v2 exists
        if 'freerideinvestor-v2' in themes:
            print("✅ freerideinvestor-v2 theme exists on server")
            # Check if functions.php exists
            try:
                sftp.stat(f"{themes_path}/freerideinvestor-v2/functions.php")
                print("✅ functions.php exists")
            except:
                print("❌ functions.php missing")

            try:
                sftp.stat(f"{themes_path}/freerideinvestor-v2/js/theme.js")
                print("✅ theme.js exists")
            except:
                print("❌ theme.js missing")
        else:
            print("❌ freerideinvestor-v2 theme NOT found on server")
            print("💡 Need to deploy the full theme first")

    except Exception as e:
        print(f"❌ Error accessing themes directory: {e}")

    sftp.close()
    transport.close()

if __name__ == "__main__":
    check_remote_theme()