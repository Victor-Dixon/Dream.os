#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Diagnose AriaJet WordPress Path Issue
=====================================

Helps identify the correct WordPress installation path for ariajet.site.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-03
"""

import os
import sys
from pathlib import Path

try:
    from ftplib import FTP
    FTP_AVAILABLE = True
except ImportError:
    FTP_AVAILABLE = False
    print("❌ ftplib not available")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def list_ftp_directory(ftp, path="/"):
    """List directory contents via FTP."""
    try:
        ftp.cwd(path)
        items = []
        ftp.retrlines('LIST', items.append)
        return items
    except Exception as e:
        return [f"Error: {e}"]


def diagnose_wordpress_path():
    """Diagnose WordPress installation paths."""
    print("🔍 AriaJet WordPress Path Diagnostic")
    print("=" * 60)
    
    # Get FTP credentials
    host = os.getenv("HOSTINGER_HOST")
    username = os.getenv("HOSTINGER_USER")
    password = os.getenv("HOSTINGER_PASS")
    port = int(os.getenv("HOSTINGER_PORT", "21"))
    
    if not all([host, username, password]):
        print("❌ FTP credentials not found in .env")
        print("   Need: HOSTINGER_HOST, HOSTINGER_USER, HOSTINGER_PASS")
        return 1
    
    print(f"\n📡 Connecting to {host}:{port}...")
    
    try:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(username, password)
        print("✅ Connected to FTP server\n")
        
        # Check root directory
        print("📁 Root directory (/):")
        root_items = list_ftp_directory(ftp, "/")
        for item in root_items[:10]:
            print(f"   {item}")
        if len(root_items) > 10:
            print(f"   ... and {len(root_items) - 10} more items")
        
        # Check common WordPress paths
        print("\n🔍 Checking common WordPress paths:")
        paths_to_check = [
            "/public_html",
            "/public_html/wp-content/themes",
            "/domains/ariajet.site/public_html",
            "/domains/ariajet.site/public_html/wp-content/themes",
            "/ariajet",
            "/ariajet/wp-content/themes",
        ]
        
        for path in paths_to_check:
            print(f"\n   Checking: {path}")
            try:
                items = list_ftp_directory(ftp, path)
                if items and not items[0].startswith("Error"):
                    print(f"   ✅ EXISTS - Found {len(items)} items")
                    # Check if ariajet theme is there
                    if "ariajet" in str(items).lower():
                        print(f"   🎯 FOUND ARIAJET THEME!")
                else:
                    print(f"   ❌ Not found or error")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Check current deployment location
        print("\n📦 Current deployment location:")
        current_path = "/public_html/wp-content/themes/ariajet"
        try:
            items = list_ftp_directory(ftp, current_path)
            if items and not items[0].startswith("Error"):
                print(f"   ✅ {current_path} EXISTS")
                print(f"   Found {len(items)} files:")
                for item in items[:5]:
                    print(f"      {item}")
            else:
                print(f"   ❌ {current_path} NOT FOUND")
        except Exception as e:
            print(f"   ❌ Error checking {current_path}: {e}")
        
        ftp.quit()
        print("\n✅ Diagnostic complete")
        print("\n💡 Next steps:")
        print("   1. Identify which path contains WordPress")
        print("   2. Check if ariajet.site uses same WordPress as freerideinvestor.com")
        print("   3. Update deployment path in sites.json if needed")
        
        return 0
        
    except Exception as e:
        print(f"❌ FTP Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(diagnose_wordpress_path())


