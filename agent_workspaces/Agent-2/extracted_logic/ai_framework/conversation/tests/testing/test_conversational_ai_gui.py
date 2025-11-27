#!/usr/bin/env python3
"""
Test Conversational AI GUI Integration
======================================

This script tests the integration of the conversational AI panel into the main GUI.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from dreamscape.gui.main_window import TheaMainWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def test_conversational_ai_integration():
    """Test the conversational AI panel integration."""
    print("🤖 Testing Conversational AI GUI Integration")
    print("=" * 50)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create main window
        print("📱 Creating main window...")
        main_window = TheaMainWindow()
        
        # Test panel switching
        print("🔄 Testing panel navigation...")
        main_window.switch_panel("conversational_ai")
        
        # Show the window
        print("👁️ Showing main window...")
        main_window.show()
        
        print("✅ Conversational AI panel successfully integrated!")
        print("📋 Available panels:")
        for key in main_window.panel_indices.keys():
            print(f"   - {key}")
        
        print("\n🎉 Integration test completed successfully!")
        print("💡 The conversational AI panel is now available in the GUI")
        print("   Navigate to '🤖 Conversational AI' in the sidebar to access it")
        
        # Run the application
        print("\n🚀 Starting GUI application...")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conversational_ai_integration() 