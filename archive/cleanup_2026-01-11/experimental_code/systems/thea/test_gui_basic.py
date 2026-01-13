#!/usr/bin/env python3
"""
Basic GUI Test for Thea Restoration
===================================

Tests if the restored GUI system can initialize properly.
This is a basic smoke test for Phase 1 GUI restoration.
"""

import sys
import os
from pathlib import Path

# Add the project root to path so we can import thea modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_gui_imports():
    """Test if all GUI modules can be imported."""
    try:
        print("🧪 Testing GUI module imports...")

        # Test main GUI module
        from systems.thea.gui import TheaMainWindow
        print("✅ TheaMainWindow import successful")

        # Test controllers
        from systems.thea.gui.controllers.main_controller import MainController
        from systems.thea.gui.controllers.panel_controller import PanelController
        print("✅ GUI controllers import successful")

        # Test components
        from systems.thea.gui.components.shared_components import SharedComponents
        print("✅ GUI components import successful")

        # Test panels
        from systems.thea.gui.panels.analytics_panel import AnalyticsPanel
        from systems.thea.gui.panels.dashboard_panel import DashboardPanel
        print("✅ GUI panels import successful")

        # Test viewmodels
        from systems.thea.gui.viewmodels.main_viewmodel import MainViewModel
        print("✅ GUI viewmodels import successful")

        print("🎉 All GUI modules imported successfully!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_initialization():
    """Test if TheaMainWindow can be instantiated (without PyQt6)."""
    try:
        print("🧪 Testing basic TheaMainWindow instantiation...")

        # This will fail if PyQt6 is not available, but that's expected
        # We just want to test if our code structure is correct
        from systems.thea.gui.main_window import TheaMainWindow

        # We can't actually instantiate without PyQt6, but we can check the class exists
        assert TheaMainWindow is not None
        print("✅ TheaMainWindow class available")

        # Check if required attributes exist
        assert hasattr(TheaMainWindow, 'initialization_completed')
        assert hasattr(TheaMainWindow, 'initialization_failed')
        print("✅ TheaMainWindow signals available")

        print("🎉 Basic TheaMainWindow structure validated!")
        return True

    except Exception as e:
        print(f"❌ TheaMainWindow validation failed: {e}")
        return False

def main():
    """Run all GUI restoration tests."""
    print("🚀 Thea GUI Restoration - Basic Functionality Test")
    print("=" * 50)

    success_count = 0
    total_tests = 2

    # Test 1: Import validation
    if test_gui_imports():
        success_count += 1

    print()

    # Test 2: Basic initialization validation
    if test_basic_initialization():
        success_count += 1

    print()
    print("=" * 50)
    print(f"📊 Test Results: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 PHASE 1 GUI FOUNDATION: VALIDATION SUCCESSFUL!")
        print("✅ GUI system structure is sound and ready for PyQt6 integration")
        return True
    else:
        print("⚠️  Some tests failed - check import paths and dependencies")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)