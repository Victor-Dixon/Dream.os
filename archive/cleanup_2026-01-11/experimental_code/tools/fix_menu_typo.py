#!/usr/bin/env python3
"""
Fix Menu Typo Script
Searches for and fixes the 'Capabilitie' → 'Capabilities' typo in WordPress
"""

import json
import paramiko
from pathlib import Path

def fix_menu_typo():
    """Fix the menu typo in WordPress"""

    # Load credentials
    repo_root = Path(__file__).resolve().parents[1]
    creds_file = repo_root / ".deploy_credentials" / "sites.json"
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    config = creds_data["tradingrobotplug.com"]

    # Connect via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=config["host"],
        username=config["username"],
        password=config["password"],
        port=config["port"]
    )

    wp_path = config["remote_path"]

    print("🔍 Searching for 'Capabilitie' typo...")

    # Search for the typo in database first
    command = f'cd {wp_path} && wp search-replace "Capabilitie" "Capabilities" --all-tables'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("Database search-replace results:")
    print(output)
    if error:
        print("Error:", error)

    # Also search in theme files
    command = f'cd {wp_path} && find wp-content/themes -name "*.php" -exec grep -l "Capabilitie" {{}} \\;'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("\nFiles containing 'Capabilitie':")
    print(output)

    # If files found, we might need manual editing
    if output.strip():
        print("⚠️ Found files with typo - may need manual editing")
        files = output.strip().split('\n')
        for file_path in files:
            if file_path:
                print(f"Found in: {file_path}")

    ssh.close()

    print("\n✅ Menu typo fix attempted")
    return True

if __name__ == "__main__":
    fix_menu_typo()