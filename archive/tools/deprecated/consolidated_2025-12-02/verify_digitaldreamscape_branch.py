#!/usr/bin/env python3
"""Verify DigitalDreamscape merge branch exists"""
import os
import requests
from pathlib import Path

token = os.getenv("GITHUB_TOKEN")
if not token:
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

if token:
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get("https://api.github.com/repos/Dadudekc/DreamVault/branches/merge-DigitalDreamscape-20251124", headers=headers, timeout=30)
    if r.status_code == 200:
        sha = r.json().get('commit', {}).get('sha', 'N/A')
        print(f"✅ Branch exists: {sha[:8]}...")
    else:
        print(f"❌ Branch not found: {r.status_code}")
else:
    print("❌ GITHUB_TOKEN not found")

