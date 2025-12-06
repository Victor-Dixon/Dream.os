#!/usr/bin/env python3
"""Quick script to verify FTP configuration."""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("🔍 FTP Configuration Check")
print("=" * 50)

host = os.getenv("HOSTINGER_HOST") or os.getenv("SSH_HOST")
port = os.getenv("HOSTINGER_PORT") or os.getenv("SSH_PORT", "21")
username = os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER")
password = os.getenv("HOSTINGER_PASS") or os.getenv("SSH_PASS")

print(f"Host: {host or '❌ NOT SET'}")
print(f"Port: {port or '❌ NOT SET'}")
print(f"Username: {username or '❌ NOT SET'}")
print(f"Password: {'✅ SET' if password else '❌ NOT SET (reset in Hostinger)'}")

print("\n✅ Expected Values:")
print("   Host: 157.173.214.121")
print("   Port: 21")
print("   Username: u996867598.freerideinvestor.com")
print("   Password: <set via Hostinger control panel>")

print("\n📋 Status:")
if host == "157.173.214.121":
    print("   ✅ Host is correct")
else:
    print(f"   ❌ Host is incorrect (got: {host})")

if port == "21":
    print("   ✅ Port is correct")
else:
    print(f"   ❌ Port is incorrect (got: {port}, expected: 21)")

if username == "u996867598.freerideinvestor.com":
    print("   ✅ Username is correct")
else:
    print(f"   ❌ Username is incorrect (got: {username})")

if password:
    print("   ✅ Password is set")
else:
    print("   ⚠️  Password not set - reset in Hostinger control panel")

