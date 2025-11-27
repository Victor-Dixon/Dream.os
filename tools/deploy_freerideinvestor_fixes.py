#!/usr/bin/env python3
"""
Deploy freerideinvestor developer tools fixes
Documenting process for prismblossom.online deployment
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wordpress_manager import WordPressManager

def main():
    """Deploy freerideinvestor fixes and document process."""
    print("=" * 70)
    print("🚀 DEPLOYING freerideinvestor Developer Tools Fixes")
    print("=" * 70)
    print()
    print("📝 NOTE: Documenting this process for prismblossom.online deployment")
    print()
    
    # Initialize manager
    manager = WordPressManager("freerideinvestor")
    
    # Check credentials
    print("🔑 Credential Check:")
    print(f"   Credentials loaded: {'✅ YES' if manager.credentials else '❌ NO'}")
    if manager.credentials:
        print(f"   Host: {manager.credentials.get('host', 'EMPTY')}")
        print(f"   Port: {manager.credentials.get('port', 'EMPTY')}")
        print(f"   Username: {manager.credentials.get('username', 'EMPTY')[:15]}..." if len(manager.credentials.get('username', '')) > 15 else f"   Username: {manager.credentials.get('username', 'EMPTY')}")
        print(f"   Password: {'✅ SET' if manager.credentials.get('password') else '❌ EMPTY'}")
    print()
    
    if not manager.credentials:
        print("❌ ERROR: No credentials found")
        print("   freerideinvestor uses shared Hostinger environment variables")
        print("   Check .env file for:")
        print("     - HOSTINGER_HOST or SSH_HOST")
        print("     - HOSTINGER_USER or SSH_USER")
        print("     - HOSTINGER_PASS or SSH_PASS")
        print("     - HOSTINGER_PORT or SSH_PORT (default: 65002)")
        print()
        print("   NOTE: These are shared credentials for all Hostinger sites")
        return 1
    
    # Files to deploy
    files_to_deploy = [
        Path("D:/websites/FreeRideInvestor/functions.php"),
        Path("D:/websites/FreeRideInvestor/inc/developer-tool.php"),
        Path("D:/websites/FreeRideInvestor/inc/unified-developer-tools.php")
    ]
    
    print("📋 Files to Deploy (3):")
    for f in files_to_deploy:
        print(f"   - {f.name}")
    print()
    
    # Connect
    print("🔌 Connecting to server...")
    if not manager.connect():
        print("❌ Connection failed!")
        print("   Check credentials and server availability")
        return 1
    print("✅ Connected!")
    print()
    
    # Deploy files
    print("📤 Deploying files...")
    success_count = 0
    fail_count = 0
    
    for file_path in files_to_deploy:
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            fail_count += 1
            continue
        
        print(f"   Deploying {file_path.name}...", end=" ")
        if manager.deploy_file(file_path):
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1
    
    # Disconnect
    manager.disconnect()
    
    # Summary
    print()
    print("=" * 70)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 70)
    print(f"✅ Succeeded: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📁 Total: {len(files_to_deploy)}")
    print()
    
    if fail_count == 0:
        print("✅ All files deployed successfully!")
        print()
        print("📝 DEPLOYMENT PROCESS DOCUMENTED:")
        print("   - Credentials loaded from .env or sites.json")
        print("   - Connected via SSH on port 65002")
        print("   - Files deployed to remote theme directory")
        print("   - Same process will work for prismblossom.online")
        return 0
    else:
        print("⚠️  Some files failed to deploy")
        return 1

if __name__ == "__main__":
    sys.exit(main())

