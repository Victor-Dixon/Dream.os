#!/usr/bin/env python3
"""
Deploy FreeRideInvestor functions.php via SFTP
==============================================

Quick deployment script for freerideinvestor.com functions.php file.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.wordpress_manager import WordPressManager

def main():
    """Deploy functions.php to freerideinvestor.com."""
    print("=" * 60)
    print("🚀 FreeRideInvestor functions.php Deployment")
    print("=" * 60)
    print()
    
    # Initialize manager
    try:
        manager = WordPressManager("freerideinvestor")
        print("✅ Manager initialized")
    except Exception as e:
        print(f"❌ Failed to initialize manager: {e}")
        return 1
    
    # Connect to server
    print("🔌 Connecting to server...")
    if not manager.connect():
        print("❌ Connection failed")
        print()
        print("💡 Troubleshooting:")
        print("  1. Check SFTP credentials in .env file")
        print("  2. Verify HOSTINGER_HOST, HOSTINGER_USER, HOSTINGER_PASS are set")
        print("  3. Run: python tools/sftp_credential_troubleshooter.py")
        return 1
    
    print("✅ Connected to server")
    print()
    
    # Deploy functions.php
    functions_file = Path("D:/websites/FreeRideInvestor/functions.php")
    if not functions_file.exists():
        print(f"❌ File not found: {functions_file}")
        return 1
    
    print(f"📤 Deploying: {functions_file}")
    print(f"   Size: {functions_file.stat().st_size:,} bytes")
    print()
    
    if manager.deploy_file(functions_file):
        print("✅ File deployed successfully!")
        print()
        print("Next steps:")
        print("  1. Clear WordPress cache")
        print("  2. Check live site: https://freerideinvestor.com")
        print("  3. Verify menu filter changes are live")
        return 0
    else:
        print("❌ Deployment failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
