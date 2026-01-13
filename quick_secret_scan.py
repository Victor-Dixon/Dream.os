#!/usr/bin/env python3
"""
Quick Secret Scanner - Find exposed secrets in repository
"""

import os
from pathlib import Path

def scan_for_secrets():
    """Scan for known secrets"""
    print("🔍 Scanning for exposed secrets...")

    known_secrets = [
        "<REDACTED_DISCORD_BOT_TOKEN>",  # Discord token
        "<REDACTED_ROBINHOOD_CLIENT_ID>",  # Robinhood key
        "<REDACTED_GITHUB_TOKEN>",  # GitHub token
    ]

    found_secrets = []

    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.json', '.yaml', '.yml', '.env', '.bat', '.ps1')):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text()
                    for secret in known_secrets:
                        if secret in content:
                            found_secrets.append(f"{file_path}: {secret[:20]}...")
                            break
                except:
                    continue

    if found_secrets:
        print("❌ FOUND SECRETS:")
        for secret in found_secrets:
            print(f"  {secret}")
        return False
    else:
        print("✅ No known secrets found in current files")
        return True

def replace_secrets():
    """Replace known secrets with placeholders"""
    print("🔄 Replacing secrets with placeholders...")

    replacements = {
        "<REDACTED_DISCORD_BOT_TOKEN>": "<REDACTED_DISCORD_BOT_TOKEN>",
        "<REDACTED_ROBINHOOD_CLIENT_ID>": "<REDACTED_ROBINHOOD_CLIENT_ID>",
        "<REDACTED_GITHUB_TOKEN>": "<REDACTED_GITHUB_TOKEN>",
    }

    replaced_files = []

    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.json', '.yaml', '.yml', '.env', '.bat', '.ps1')):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text()
                    original_content = content

                    for secret, placeholder in replacements.items():
                        if secret in content:
                            content = content.replace(secret, placeholder)
                            print(f"  📝 Replaced secret in {file_path}")

                    if content != original_content:
                        file_path.write_text(content)
                        replaced_files.append(str(file_path))

                except:
                    continue

    if replaced_files:
        print(f"✅ Replaced secrets in {len(replaced_files)} files")
        print("📝 Ready to commit: git add . && git commit -m 'security: replace exposed secrets with placeholders'")
        return True
    else:
        print("ℹ️ No secrets found to replace")
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python quick_secret_scan.py scan    # Scan for secrets")
        print("  python quick_secret_scan.py replace # Replace secrets")
        sys.exit(1)

    command = sys.argv[1]

    if command == "scan":
        success = scan_for_secrets()
        sys.exit(0 if success else 1)
    elif command == "replace":
        success = replace_secrets()
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)