#!/usr/bin/env python3
"""
Quick Test Script for Main Application
=====================================

This script provides a quick way to test the main application functionality
without launching the full GUI. Useful for debugging and validation.
"""

import sys
import os
import time
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_environment():
    """Test basic environment setup."""
    print("🔍 Testing Environment...")
    
    # Check Python version
    print(f"  Python Version: {sys.version}")
    
    # Check working directory
    print(f"  Working Directory: {os.getcwd()}")
    
    # Check if we're in the right place
    if not Path("main.py").exists():
        print("  ❌ main.py not found in current directory")
        return False
    
    print("  ✅ Environment check passed")
    return True

def test_imports():
    """Test all critical imports."""
    print("\n📦 Testing Imports...")
    
    imports_to_test = [
        ("dreamscape.gui.main_window", "TheaMainWindow"),
        ("dreamscape.core.expanded_analytics_system", "ExpandedAnalyticsSystem"),
        ("dreamscape.core.community_template_system", "CommunityTemplateSystem"),
        ("dreamscape.core.voice_modeling_system", "VoiceModelingSystem"),
        ("dreamscape.gui.panels.community_templates_panel", "CommunityTemplatesPanel"),
        ("dreamscape.gui.panels.voice_modeling_panel", "VoiceModelingPanel"),
        ("PyQt6.QtWidgets", "QApplication"),
        ("sqlite3", None),
        ("numpy", None),
        ("pandas", None),
    ]
    
    failed_imports = []
    
    for module, class_name in imports_to_test:
        try:
            if class_name:
                exec(f"from {module} import {class_name}")
                print(f"  ✅ {module}.{class_name}")
            else:
                exec(f"import {module}")
                print(f"  ✅ {module}")
        except Exception as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append((module, str(e)))
    
    if failed_imports:
        print(f"\n  ⚠️ {len(failed_imports)} import(s) failed")
        return False
    
    print("  ✅ All imports successful")
    return True

def test_main_function():
    """Test main function import and basic functionality."""
    print("\n🚀 Testing Main Function...")
    
    try:
        # Add parent directory to path to import main
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from main import main
        print("  ✅ Main function imported successfully")
        
        # Test that main function exists and is callable
        if callable(main):
            print("  ✅ Main function is callable")
            return True
        else:
            print("  ❌ Main function is not callable")
            return False
            
    except Exception as e:
        print(f"  ❌ Main function test failed: {e}")
        return False

def test_component_functions():
    """Test individual component functions."""
    print("\n🧪 Testing Component Functions...")
    
    # Add parent directory to path to import main
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    components = [
        ("test_template_engine", "Template Engine"),
        ("test_scraper", "Scraper"),
        ("test_enhanced_skill_system", "Enhanced Skill System"),
        ("test_enhanced_ingestion", "Enhanced Ingestion"),
    ]
    
    failed_components = []
    
    for func_name, display_name in components:
        try:
            # Import the function
            exec(f"from main import {func_name}")
            print(f"  ✅ {display_name} function imported")
        except Exception as e:
            print(f"  ❌ {display_name} function import failed: {e}")
            failed_components.append((display_name, str(e)))
    
    if failed_components:
        print(f"\n  ⚠️ {len(failed_components)} component(s) failed to import")
        return False
    
    print("  ✅ All component functions imported successfully")
    return True

def test_agent4_systems():
    """Test Agent 4 systems initialization."""
    print("\n🤖 Testing Agent 4 Systems...")
    
    systems = [
        ("ExpandedAnalyticsSystem", "Analytics"),
        ("CommunityTemplateSystem", "Community Templates"),
        ("VoiceModelingSystem", "Voice Modeling"),
    ]
    
    failed_systems = []
    
    for class_name, display_name in systems:
        try:
            # Import the class with correct module names
            if class_name == "ExpandedAnalyticsSystem":
                from dreamscape.core.expanded_analytics_system import ExpandedAnalyticsSystem
                system = ExpandedAnalyticsSystem(f"test_{display_name.lower()}.db")
                system.init_databases()
            elif class_name == "CommunityTemplateSystem":
                from dreamscape.core.community_template_system import CommunityTemplateSystem
                system = CommunityTemplateSystem(f"test_{display_name.lower()}.db")
                system.init_database()
            elif class_name == "VoiceModelingSystem":
                from dreamscape.core.voice_modeling_system import VoiceModelingSystem
                system = VoiceModelingSystem(f"test_{display_name.lower()}.db")
                system.init_database()
            
            print(f"  ✅ {display_name} system initialized")
            
            # Cleanup test database
            test_db = f"test_{display_name.lower()}.db"
            if os.path.exists(test_db):
                os.remove(test_db)
                
        except Exception as e:
            print(f"  ❌ {display_name} system failed: {e}")
            failed_systems.append((display_name, str(e)))
    
    if failed_systems:
        print(f"\n  ⚠️ {len(failed_systems)} system(s) failed")
        return False
    
    print("  ✅ All Agent 4 systems initialized successfully")
    return True

def test_gui_components():
    """Test GUI components without launching full application."""
    print("\n🖥️ Testing GUI Components...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        
        # Create QApplication instance
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test panel instantiation
        from dreamscape.gui.panels.community_templates_panel import CommunityTemplatesPanel
        from dreamscape.gui.panels.voice_modeling_panel import VoiceModelingPanel
        
        community_panel = CommunityTemplatesPanel()
        voice_panel = VoiceModelingPanel()
        
        print("  ✅ Community Templates Panel created")
        print("  ✅ Voice Modeling Panel created")
        
        # Test main window import (don't instantiate to avoid GUI)
        from dreamscape.gui.main_window import TheaMainWindow
        print("  ✅ Main Window class imported")
        
        return True
        
    except Exception as e:
        print(f"  ❌ GUI component test failed: {e}")
        return False

def test_database_operations():
    """Test basic database operations."""
    print("\n🗄️ Testing Database Operations...")
    
    try:
        import sqlite3
        
        # Test basic SQLite operations
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # Create test table
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO test (name) VALUES (?)", ("test",))
        cursor.execute("SELECT * FROM test")
        result = cursor.fetchone()
        
        conn.close()
        
        if result and result[1] == "test":
            print("  ✅ Database operations successful")
            return True
        else:
            print("  ❌ Database operations failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def run_quick_tests():
    """Run all quick tests."""
    print("🚀 Starting Quick Application Tests")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Main Function", test_main_function),
        ("Component Functions", test_component_functions),
        ("Agent 4 Systems", test_agent4_systems),
        ("GUI Components", test_gui_components),
        ("Database Operations", test_database_operations),
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    end_time = time.time()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if passed == total:
        print("\n🎉 All tests passed! Application is ready to run.")
        print("You can now run: python main.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the issues above.")
        return False

def main():
    """Main function."""
    try:
        success = run_quick_tests()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Test script crashed: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 