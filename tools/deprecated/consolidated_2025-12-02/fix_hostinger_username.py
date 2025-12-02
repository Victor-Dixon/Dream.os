#!/usr/bin/env python3
"""
Fix Hostinger Username Format
==============================

Hostinger SFTP often requires just the username (not email).
This tool extracts the username from email format and updates .env.

Author: Agent-7 (Web Development Specialist)
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv, set_key, find_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False
    print("❌ python-dotenv not installed. Install with: pip install python-dotenv")

def extract_username_from_email(email: str) -> str:
    """Extract username from email address."""
    if "@" in email:
        return email.split("@")[0]
    return email

def fix_username_in_env():
    """Fix username format in .env file."""
    if not HAS_DOTENV:
        return False
    
    # Find .env file
    env_path = find_dotenv()
    if not env_path:
        # Try common locations
        env_paths = [
            Path(".env"),
            Path("D:/Agent_Cellphone_V2_Repository/.env"),
            Path("D:/websites/.env"),
        ]
        for path in env_paths:
            if path.exists():
                env_path = str(path)
                break
        else:
            print("❌ .env file not found")
            return False
    
    print(f"📁 Found .env file: {env_path}")
    
    # Load current .env
    load_dotenv(env_path)
    
    # Get current username
    current_user = os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER")
    
    if not current_user:
        print("❌ HOSTINGER_USER not found in .env")
        return False
    
    print(f"📧 Current username: {current_user}")
    
    # Check if it's an email
    if "@" in current_user:
        new_username = extract_username_from_email(current_user)
        print(f"✂️  Extracting username from email...")
        print(f"✅ New username: {new_username}")
        
        # Update .env
        set_key(env_path, "HOSTINGER_USER", new_username)
        print(f"✅ Updated HOSTINGER_USER in {env_path}")
        
        # Also update SSH_USER if it exists
        if os.getenv("SSH_USER"):
            set_key(env_path, "SSH_USER", new_username)
            print(f"✅ Updated SSH_USER in {env_path}")
        
        return True
    else:
        print("✅ Username is already in correct format (not an email)")
        return True

def main():
    """Main function."""
    print("=" * 60)
    print("🔧 Fix Hostinger Username Format")
    print("=" * 60)
    print()
    
    if fix_username_in_env():
        print()
        print("=" * 60)
        print("✅ Username format fixed!")
        print("=" * 60)
        print()
        print("💡 Next steps:")
        print("  1. Verify the username is correct")
        print("  2. Try deployment again:")
        print("     python tools/deploy_freeride_menu_fix.py")
        print()
        return 0
    else:
        print()
        print("❌ Failed to fix username")
        return 1

if __name__ == "__main__":
    sys.exit(main())

