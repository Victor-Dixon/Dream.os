#!/usr/bin/env python3
"""
Basic Mobile Components Test for Thea Restoration
===============================================

Tests if the restored mobile application components can initialize properly.
This validates Phase 1 mobile component extraction.
"""

import sys
import os
from pathlib import Path

# Add the project root to path so we can import thea modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_mobile_imports():
    """Test if all mobile modules can be imported."""
    try:
        print("🧪 Testing mobile module imports...")

        # Test mobile app module
        from systems.thea.mobile.mobile_app import MobileApp
        print("✅ MobileApp import successful")

        # Test mobile features module
        from systems.thea.mobile.mobile_features import MobileFeatureManager, VoiceTask, LocationReminder, QuestProgress
        print("✅ Mobile features import successful")

        print("🎉 All mobile modules imported successfully!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_mobile_initialization():
    """Test if MobileApp can be instantiated."""
    try:
        print("🧪 Testing basic MobileApp instantiation...")

        from systems.thea.mobile.mobile_app import MobileApp

        # Test basic instantiation
        app = MobileApp()
        assert app is not None
        print("✅ MobileApp instance created")

        # Test manager initialization
        assert hasattr(app, 'manager')
        assert app.manager is not None
        print("✅ MobileFeatureManager initialized")

        # Test storage path
        assert hasattr(app, 'storage_path')
        print("✅ Storage path configured")

        print("🎉 Basic MobileApp structure validated!")
        return True

    except Exception as e:
        print(f"❌ MobileApp validation failed: {e}")
        return False

def test_mobile_features():
    """Test mobile feature classes."""
    try:
        print("🧪 Testing mobile feature classes...")

        from systems.thea.mobile.mobile_features import VoiceTask, LocationReminder, QuestProgress

        # Test VoiceTask
        task = VoiceTask(text="Test voice task")
        assert task.text == "Test voice task"
        assert not task.completed
        print("✅ VoiceTask class functional")

        # Test LocationReminder
        reminder = LocationReminder(
            location=(40.0, -74.0),
            radius_meters=100.0,
            message="Test reminder"
        )
        assert reminder.location == (40.0, -74.0)
        assert reminder.radius_meters == 100.0
        assert reminder.message == "Test reminder"
        print("✅ LocationReminder class functional")

        # Test QuestProgress
        progress = QuestProgress(name="Test quest", progress=5, target=10)
        assert progress.name == "Test quest"
        assert progress.progress == 5
        assert progress.target == 10
        print("✅ QuestProgress class functional")

        print("🎉 All mobile feature classes validated!")
        return True

    except Exception as e:
        print(f"❌ Mobile features validation failed: {e}")
        return False

def main():
    """Run all mobile restoration tests."""
    print("🚀 Thea Mobile Components - Basic Functionality Test")
    print("=" * 50)

    success_count = 0
    total_tests = 3

    # Test 1: Import validation
    if test_mobile_imports():
        success_count += 1

    print()

    # Test 2: Basic initialization validation
    if test_basic_mobile_initialization():
        success_count += 1

    print()

    # Test 3: Mobile features validation
    if test_mobile_features():
        success_count += 1

    print()
    print("=" * 50)
    print(f"📊 Test Results: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 PHASE 1 MOBILE COMPONENTS: VALIDATION SUCCESSFUL!")
        print("✅ Mobile application structure is sound and ready for integration")
        return True
    else:
        print("⚠️  Some tests failed - check import paths and dependencies")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)