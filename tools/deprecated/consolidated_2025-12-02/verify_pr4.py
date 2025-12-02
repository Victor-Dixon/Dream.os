#!/usr/bin/env python3
"""Verify PR #4 exists"""
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
    r = requests.get("https://api.github.com/repos/Dadudekc/DreamVault/pulls/4", headers=headers, timeout=30)
    if r.status_code == 200:
        print(f"✅ PR #4 exists: {r.json().get('html_url')}")
    else:
        print(f"❌ PR #4 not found: {r.status_code}")
else:
    print("❌ GITHUB_TOKEN not found")

