#!/usr/bin/env python3
"""
Debug dotenv loading in launcher context
"""

import os
import sys
from pathlib import Path

# Add project root to path (same as launcher)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file (same as launcher)
try:
    from dotenv import load_dotenv
    # Load from repo root (same as launcher)
    repo_root = Path(__file__).resolve().parent
    dotenv_path = repo_root / ".env"
    print(f"Loading .env from: {dotenv_path}")
    print(f".env exists: {dotenv_path.exists()}")

    result = load_dotenv(dotenv_path=dotenv_path)
    print(f"load_dotenv returned: {result}")
except ImportError:
    print("⚠️  python-dotenv not installed. Using existing environment variables.")

# Check environment variables
print("\nEnvironment check:")
token = os.getenv('DISCORD_BOT_TOKEN')
guild = os.getenv('DISCORD_GUILD_ID')
print(f"DISCORD_BOT_TOKEN: {'SET' if token else 'NOT SET'}")
print(f"DISCORD_GUILD_ID: {'SET' if guild else 'NOT SET'}")

if token:
    print(f"Token preview: {token[:20]}...")
if guild:
    print(f"Guild ID: {guild}")