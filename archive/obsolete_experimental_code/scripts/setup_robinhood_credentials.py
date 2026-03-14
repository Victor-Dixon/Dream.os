#!/usr/bin/env python3
"""
Robinhood Credentials Setup Script
==================================

Interactive setup for Robinhood API credentials.
This script helps you configure your Robinhood credentials safely.

Usage:
    python setup_robinhood_credentials.py

This will:
1. Guide you through setting up your Robinhood credentials
2. Help you obtain your TOTP secret from your authenticator app
3. Test the authentication (optional)
4. Save credentials to .env file

Security Note:
- Credentials are stored locally in .env file
- Never commit .env files to version control
- Credentials are only used for read-only API access
"""

import os
import getpass
from pathlib import Path


def get_env_file_path():
    """Find the .env file in the project root"""
    project_root = Path(__file__).parent
    env_file = project_root / '.env'
    return env_file


def read_existing_env():
    """Read existing .env file if it exists"""
    env_file = get_env_file_path()
    if env_file.exists():
        with open(env_file, 'r') as f:
            return f.read()
    return ""


def write_env_file(content):
    """Write content to .env file"""
    env_file = get_env_file_path()
    with open(env_file, 'w') as f:
        f.write(content)
    print(f"✅ Credentials saved to {env_file}")


def setup_credentials():
    """Interactive credential setup"""
    print("🚀 Robinhood Credentials Setup")
    print("=" * 40)

    # Check existing credentials
    existing_env = read_existing_env()
    has_existing = any(line.startswith(('ROBINHOOD_USERNAME=', 'ROBINHOOD_PASSWORD=', 'ROBINHOOD_TOTP_SECRET=')) for line in existing_env.split('\n'))

    if has_existing:
        print("⚠️  Existing Robinhood credentials found!")
        overwrite = input("Overwrite existing credentials? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return

    # Get credentials
    print("\n📧 Step 1: Robinhood Account")
    username = input("Enter your Robinhood email/username: ").strip()
    if not username:
        print("❌ Username is required")
        return

    password = getpass.getpass("Enter your Robinhood password: ")
    if not password:
        print("❌ Password is required")
        return

    print("\n🔐 Step 2: Two-Factor Authentication (2FA)")
    print("Robinhood requires 2FA. You have two options:")
    print()
    print("Option A: Automatic 2FA (Recommended)")
    print("  - Export your TOTP secret from your authenticator app")
    print("  - Google Authenticator: Settings → Export accounts")
    print("  - Authy: Account → Settings → Show 2FA QR Code")
    print()
    print("Option B: Manual 2FA (Fallback)")
    print("  - Leave TOTP secret empty")
    print("  - Approve login requests in Robinhood app/browser")
    print()

    totp_secret = getpass.getpass("Enter TOTP secret (or press Enter for manual 2FA): ").strip()

    # Create .env content
    env_lines = []

    # Preserve existing content
    for line in existing_env.split('\n'):
        if line.strip() and not line.startswith(('ROBINHOOD_USERNAME=', 'ROBINHOOD_PASSWORD=', 'ROBINHOOD_TOTP_SECRET=')):
            env_lines.append(line)

    # Add Robinhood credentials
    env_lines.extend([
        "",
        "# Robinhood API Credentials",
        f"ROBINHOOD_USERNAME={username}",
        f"ROBINHOOD_PASSWORD={password}",
    ])

    if totp_secret:
        env_lines.append(f"ROBINHOOD_TOTP_SECRET={totp_secret}")
        print("✅ Automatic 2FA configured")
    else:
        print("⚠️  Manual 2FA selected - you'll need to approve logins manually")

    # Write to file
    write_env_file('\n'.join(env_lines))

    print("\n🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Test your credentials: python -m src.services.messaging_cli --robinhood-stats")
    print("2. If using manual 2FA, be ready to approve login requests")
    print("3. View your 2026 options statistics and account balance")

    # Optional test
    test_now = input("\nTest credentials now? (y/N): ").lower().strip()
    if test_now == 'y':
        print("\n🧪 Testing authentication...")
        os.system("python -m src.services.messaging_cli --robinhood-stats")


if __name__ == "__main__":
    try:
        setup_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")