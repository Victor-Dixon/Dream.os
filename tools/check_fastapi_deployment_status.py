#!/usr/bin/env python3
"""
FastAPI Deployment Status Checker
==================================

Quick utility to check FastAPI deployment status on production server.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ops" / "deployment"))
from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

SITE_KEY = "tradingrobotplug.com"
BACKEND_DIR = "backend"


def check_deployment_status():
    """Check FastAPI deployment status on server."""
    print("🔍 FastAPI Deployment Status Check\n")
    
    site_configs = load_site_configs()
    try:
        deployer = SimpleWordPressDeployer(SITE_KEY, site_configs)
    except Exception as e:
        print(f"❌ Failed to initialize deployer: {e}")
        return False
    
    if not deployer.connect():
        print("❌ Failed to connect to server")
        return False
    
    print(f"✅ Connected to {SITE_KEY}\n")
    
    # Check key files
    key_files = [
        "backend/api/fastapi_app.py",
        "backend/requirements.txt",
        "backend/.env.example",
        "/tmp/tradingrobotplug-fastapi.service"
    ]
    
    found_count = 0
    for file_path in key_files:
        try:
            # Try to stat the file
            deployer.sftp.stat(file_path)
            print(f"✅ Found: {file_path}")
            found_count += 1
        except Exception:
            print(f"❌ Missing: {file_path}")
    
    print(f"\n📊 Status: {found_count}/{len(key_files)} key files found")
    
    if found_count == len(key_files):
        print("✅ Deployment appears complete")
        return True
    else:
        print("⚠️  Some files missing - deployment may be incomplete")
        return False


if __name__ == "__main__":
    success = check_deployment_status()
    sys.exit(0 if success else 1)

