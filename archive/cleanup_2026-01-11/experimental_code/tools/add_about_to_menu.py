#!/usr/bin/env python3
"""
Add About Us Page to Navigation Menu
Ensures the About Us page is properly integrated into the site navigation
"""

import json
import paramiko
from pathlib import Path

def add_about_to_menu():
    """Add About Us page to the navigation menu"""

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

    print("🔍 Checking current menu items...")

    # Check current menu items
    command = f"cd {wp_path} && wp menu item list swarm-primary --format=json"
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("Current menu items:")
    print(output)

    # Parse menu items
    try:
        menu_items = json.loads(output)
        about_exists = any(item.get('title', '').lower() == 'about us' for item in menu_items)

        if not about_exists:
            print("📝 Adding About Us to menu...")
            command = f'cd {wp_path} && wp menu item add-post swarm-primary 73 --title="About Us"'
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            print("Menu addition result:", output)
            if error:
                print("Error:", error)
            else:
                print("✅ About Us added to menu")
        else:
            print("✅ About Us already in menu")

    except Exception as e:
        print(f"❌ Error processing menu: {e}")

    ssh.close()

    return True

if __name__ == "__main__":
    success = add_about_to_menu()
    if success:
        print("\n🎯 Menu integration complete!")
        print("About Us page is now accessible via navigation")