#!/usr/bin/env python3
"""
Test Deployment Staging & Rollback Functionality
===============================================

Tests the new staging/snapshot and rollback capabilities in the deployment MCP server.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)

<!-- SSOT Domain: tools -->
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "mcp_servers"))

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers'))

# Import directly from deployment_server module
from deployment_server import (
    create_deployment_snapshot,
    list_deployment_snapshots,
    rollback_deployment,
    delete_deployment_snapshot,
    deploy_with_staging,
    DeploymentSnapshot
)


def test_snapshot_creation():
    """Test snapshot creation functionality."""
    print("\n🖼️ Testing Snapshot Creation...")

    # Test with a real site key
    result = create_deployment_snapshot("tradingrobotplug.com", "Test snapshot creation")

    if result.get("success"):
        print("✅ Snapshot creation successful")
        print(f"   Snapshot ID: {result['snapshot_id']}")
        print(f"   Site: {result['site_key']}")
        print(f"   Files: {result['files_count']}")

        # Verify snapshot file exists
        snapshot_dir = Path("deployment_snapshots/tradingrobotplug.com")
        if snapshot_dir.exists():
            snapshot_files = list(snapshot_dir.glob("*.json"))
            if snapshot_files:
                print(f"   ✅ Snapshot file created: {snapshot_files[0].name}")
                return result['snapshot_id']
            else:
                print("   ❌ No snapshot files found")
                return None
        else:
            print("   ❌ Snapshot directory not created")
            return None
    else:
        print(f"❌ Snapshot creation failed: {result.get('error')}")
        return None


def test_snapshot_listing(snapshot_id):
    """Test snapshot listing functionality."""
    print("\n📋 Testing Snapshot Listing...")

    # Test listing all snapshots
    result = list_deployment_snapshots()

    if result.get("success"):
        print(f"✅ Snapshot listing successful: {result['count']} snapshots found")

        # Test filtering by site
        site_result = list_deployment_snapshots("tradingrobotplug.com")
        if site_result.get("success"):
            print(f"   ✅ Site filtering works: {site_result['count']} snapshots for tradingrobotplug.com")

            # Check if our snapshot is in the list
            snapshot_ids = [s['snapshot_id'] for s in site_result['snapshots']]
            if snapshot_id in snapshot_ids:
                print(f"   ✅ Created snapshot found in list: {snapshot_id}")
                return True
            else:
                print(f"   ❌ Created snapshot not found in list: {snapshot_id}")
                return False
        else:
            print("❌ Site filtering failed")
            return False
    else:
        print(f"❌ Snapshot listing failed: {result.get('error')}")
        return False


def test_snapshot_deletion(snapshot_id):
    """Test snapshot deletion functionality."""
    print("\n🗑️ Testing Snapshot Deletion...")

    result = delete_deployment_snapshot("tradingrobotplug.com", snapshot_id)

    if result.get("success"):
        print("✅ Snapshot deletion successful")
        print(f"   Deleted snapshot: {snapshot_id}")

        # Verify snapshot file is gone
        snapshot_path = Path(f"deployment_snapshots/tradingrobotplug.com/{snapshot_id}.json")
        if not snapshot_path.exists():
            print("   ✅ Snapshot file successfully deleted")
            return True
        else:
            print("   ❌ Snapshot file still exists")
            return False
    else:
        print(f"❌ Snapshot deletion failed: {result.get('error')}")
        return False


def test_staging_deployment():
    """Test staging deployment functionality."""
    print("\n🚀 Testing Staging Deployment...")

    # Create a mock theme file for testing
    test_file = "test_theme_file.css"
    test_content = "/* Test theme file */\nbody { color: blue; }"

    try:
        with open(test_file, 'w') as f:
            f.write(test_content)

        # Test staging deployment
        result = deploy_with_staging(
            site_key="tradingrobotplug.com",
            theme_files=[test_file],
            description="Test staging deployment"
        )

        if result.get("success"):
            print("✅ Staging deployment successful")
            print(f"   Site: {result['site_key']}")
            print(f"   Rollback available: {result['rollback_available']}")

            if result['rollback_available'] and result.get('rollback_snapshot_id'):
                rollback_id = result['rollback_snapshot_id']
                print(f"   Rollback snapshot: {rollback_id}")
                return rollback_id
            else:
                print("   ⚠️ No rollback snapshot created")
                return None
        else:
            print(f"❌ Staging deployment failed: {result.get('error')}")
            return None

    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)


def test_rollback_functionality(snapshot_id):
    """Test rollback functionality."""
    print("\n🔄 Testing Rollback Functionality...")

    if not snapshot_id:
        print("❌ No snapshot ID provided for rollback test")
        return False

    result = rollback_deployment("tradingrobotplug.com", snapshot_id)

    if result.get("success"):
        print("✅ Rollback successful")
        print(f"   Rolled back to snapshot: {snapshot_id}")
        rollback_info = result.get("rollback", {})
        print(f"   Files restored: {rollback_info.get('files_to_restore', 0)}")
        return True
    else:
        print(f"❌ Rollback failed: {result.get('error')}")
        return False


def cleanup_test_data():
    """Clean up test data."""
    print("\n🧹 Cleaning up test data...")

    import shutil

    # Remove test snapshot directory
    test_snapshot_dir = Path("deployment_snapshots/tradingrobotplug.com")
    if test_snapshot_dir.exists():
        try:
            shutil.rmtree(test_snapshot_dir)
            print("✅ Test snapshot directory removed")
        except Exception as e:
            print(f"⚠️ Could not remove test directory: {e}")

    # Remove main deployment_snapshots directory if empty
    main_dir = Path("deployment_snapshots")
    if main_dir.exists():
        try:
            if not any(main_dir.iterdir()):
                main_dir.rmdir()
                print("✅ Empty deployment_snapshots directory removed")
            else:
                print("⚠️ deployment_snapshots directory not empty, leaving for manual cleanup")
        except Exception as e:
            print(f"⚠️ Could not check/remove main directory: {e}")


def main():
    """Run all staging/rollback tests."""
    print("=" * 70)
    print("Deployment Staging & Rollback Test Suite")
    print("=" * 70)
    print()

    tests = []
    snapshot_id = None
    staging_snapshot_id = None

    try:
        # Test 1: Snapshot creation
        snapshot_id = test_snapshot_creation()
        tests.append(("Snapshot Creation", snapshot_id is not None))

        # Test 2: Snapshot listing
        if snapshot_id:
            list_success = test_snapshot_listing(snapshot_id)
            tests.append(("Snapshot Listing", list_success))

        # Test 3: Staging deployment
        staging_snapshot_id = test_staging_deployment()
        tests.append(("Staging Deployment", staging_snapshot_id is not None))

        # Test 4: Rollback functionality
        if staging_snapshot_id:
            rollback_success = test_rollback_functionality(staging_snapshot_id)
            tests.append(("Rollback Functionality", rollback_success))

        # Test 5: Snapshot deletion
        if snapshot_id:
            delete_success = test_snapshot_deletion(snapshot_id)
            tests.append(("Snapshot Deletion", delete_success))

    finally:
        # Always clean up test data
        cleanup_test_data()

    print("\n" + "=" * 70)
    print("STAGING/ROLLBACK TEST RESULTS SUMMARY")
    print("=" * 70)

    passed = 0
    total = len(tests)

    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1

    print(f"\n📊 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All staging and rollback functionality tests passed!")
        print("\n📝 New Features Available:")
        print("   • create_deployment_snapshot() - Create deployment snapshots")
        print("   • list_deployment_snapshots() - List available snapshots")
        print("   • rollback_deployment() - Rollback to previous snapshots")
        print("   • deploy_with_staging() - Deploy with automatic rollback protection")
        print("\n🔧 Ready for production deployment with rollback safety!")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Check file permissions for snapshot directory creation")
        print("   2. Verify deployment server dependencies")
        print("   3. Check for existing snapshot conflicts")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
