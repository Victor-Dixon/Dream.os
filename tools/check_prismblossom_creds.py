#!/usr/bin/env python3
"""Check prismblossom.online deployment credentials."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path("D:/Agent_Cellphone_V2_Repository/.env")
if env_path.exists():
    load_dotenv(env_path)

# Check credentials
host = os.getenv("HOSTINGER_HOST") or os.getenv("SSH_HOST")
user = os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER")
password = os.getenv("HOSTINGER_PASS") or os.getenv("SSH_PASS")
port = os.getenv("HOSTINGER_PORT") or os.getenv("SSH_PORT")

print("=" * 60)
print("prismblossom.online Credential Check")
print("=" * 60)
print()
print(f"Host:     {'✅ SET' if host else '❌ MISSING'}")
print(f"User:     {'✅ SET' if user else '❌ MISSING'}")
print(f"Password: {'✅ SET' if password else '❌ MISSING'}")
print(f"Port:     {port or '❌ MISSING (needs 65002)'}")
print()

if host and user and password:
    print("✅ All credentials set! Ready to deploy.")
    print()
    print("To deploy, run:")
    print("  python tools/deploy_prismblossom.py")
else:
    print("❌ Missing credentials!")
    print()
    print("Add to .env file:")
    print("  HOSTINGER_HOST=your_host_ip")
    print("  HOSTINGER_USER=your_username")
    print("  HOSTINGER_PASS=your_password")
    print("  HOSTINGER_PORT=65002")
    print()
    print("Get credentials from: Hostinger hPanel → FTP Accounts")

