#!/usr/bin/env python3
"""
Fix Theme Typo Script
Fixes 'Capabilitie' → 'Capabilities' in theme files
"""

import json
import paramiko
from pathlib import Path

def fix_theme_typo():
    """Fix the typo in theme files"""

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

    # Files to fix
    files_to_fix = [
        "wp-content/themes/swarm-theme/front-page.php",
        "wp-content/themes/tradingrobotplug-theme/quality_fixes.php"
    ]

    for file_path in files_to_fix:
        print(f"🔧 Fixing typo in {file_path}...")

        # Use sed to replace the typo
        command = f"cd {wp_path} && sed -i 's/Capabilitie/Capabilities/g' {file_path}"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            print(f"❌ Error fixing {file_path}: {error}")
        else:
            print(f"✅ Fixed typo in {file_path}")

    ssh.close()
    print("✅ Theme typo fix completed")
    return True

if __name__ == "__main__":
    fix_theme_typo()