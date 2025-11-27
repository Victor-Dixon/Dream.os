#!/usr/bin/env python3
"""
Deploy prismblossom.online files using automated agent method
Same method as dadudekc and other sites - SSH on port 65002
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from wordpress_manager import WordPressManager

def main():
    """Deploy prismblossom.online files."""
    print("=" * 70)
    print("🚀 DEPLOYING prismblossom.online - Automated Agent Method")
    print("=" * 70)
    print()
    
    # Initialize manager
    manager = WordPressManager("prismblossom")
    
    # Check credentials
    if not manager.credentials:
        print("❌ ERROR: No credentials found for prismblossom")
        print("   Need to set credentials in .deploy_credentials/sites.json")
        print("   Or set environment variables:")
        print("   - HOSTINGER_HOST (157.173.214.121)")
        print("   - HOSTINGER_USER (SSH username)")
        print("   - HOSTINGER_PASS (SSH password)")
        print("   - HOSTINGER_PORT (65002)")
        return 1
    
    host = manager.credentials.get("host")
    port = manager.credentials.get("port", 22)
    
    if not host:
        print("❌ ERROR: Host not set in credentials")
        print("   Expected: 157.173.214.121 (Hostinger server)")
        print("   Port should be: 65002 (not 22)")
        return 1
    
    print(f"📡 Connection Details:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Username: {manager.credentials.get('username', 'NOT SET')}")
    print(f"   Password: {'SET' if manager.credentials.get('password') else 'NOT SET'}")
    print()
    
    # Files to deploy
    theme_path = Path("D:/websites/prismblossom.online/wordpress-theme/prismblossom")
    files_to_deploy = [
        "page-invitation.php",
        "page-guestbook.php",
        "page-birthday-fun.php",
        "page-birthday-blog.php"
    ]
    
    print(f"📋 Files to deploy ({len(files_to_deploy)}):")
    for f in files_to_deploy:
        print(f"   - {f}")
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
    
    for filename in files_to_deploy:
        local_path = theme_path / filename
        if not local_path.exists():
            print(f"⚠️  File not found: {local_path}")
            fail_count += 1
            continue
        
        print(f"   Deploying {filename}...", end=" ")
        if manager.deploy_file(local_path):
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
        return 0
    else:
        print("⚠️  Some files failed to deploy")
        return 1

if __name__ == "__main__":
    sys.exit(main())

