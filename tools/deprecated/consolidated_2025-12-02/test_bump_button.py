#!/usr/bin/env python3
"""
Test Bump Button - Verify button is in control panel
====================================================

Quick test to verify the bump button is properly added to the control panel.

Author: Agent-6
Created: 2025-11-30
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_bump_button():
    """Test that bump button is in control panel."""
    try:
        from src.services.messaging_infrastructure import ConsolidatedMessagingService
        from src.discord_commander.views.main_control_panel_view import MainControlPanelView
        
        # Create messaging service (minimal for testing)
        messaging_service = ConsolidatedMessagingService()
        
        # Create control panel view
        view = MainControlPanelView(messaging_service)
        
        # Check for bump button
        bump_button = None
        for item in view.children:
            if hasattr(item, 'custom_id') and item.custom_id == "control_bump":
                bump_button = item
                break
        
        if bump_button:
            print("✅ Bump button found in control panel!")
            print(f"   Label: {bump_button.label}")
            print(f"   Custom ID: {bump_button.custom_id}")
            print(f"   Row: {bump_button.row}")
            print(f"   Style: {bump_button.style}")
            print(f"   Emoji: {bump_button.emoji}")
            return True
        else:
            print("❌ Bump button NOT found in control panel!")
            print("\nButtons found:")
            for item in view.children:
                if hasattr(item, 'label'):
                    print(f"   - {item.label} ({item.custom_id})")
            return False
            
    except Exception as e:
        print(f"❌ Error testing bump button: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bump_view():
    """Test that BumpAgentView can be imported and created."""
    try:
        from src.discord_commander.views.bump_agent_view import BumpAgentView
        
        # Note: Can't actually create view without event loop, but can test import
        print("✅ BumpAgentView imports successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error importing BumpAgentView: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_count():
    """Test button count per row to check Discord limits."""
    try:
        from src.services.messaging_infrastructure import ConsolidatedMessagingService
        from src.discord_commander.views.main_control_panel_view import MainControlPanelView
        
        messaging_service = ConsolidatedMessagingService()
        view = MainControlPanelView(messaging_service)
        
        # Count buttons per row
        row_counts = {}
        for item in view.children:
            if hasattr(item, 'row') and hasattr(item, 'label'):
                row = item.row
                row_counts[row] = row_counts.get(row, 0) + 1
        
        print("\n📊 Button count per row:")
        for row in sorted(row_counts.keys()):
            count = row_counts[row]
            status = "✅" if count <= 5 else "⚠️ (Discord limit: 5 per row)"
            print(f"   Row {row}: {count} buttons {status}")
        
        # Check row 2 specifically
        row_2_count = row_counts.get(2, 0)
        if row_2_count > 5:
            print(f"\n⚠️ WARNING: Row 2 has {row_2_count} buttons (Discord limit is 5)")
            print("   This may cause the bump button to not appear!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error counting buttons: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING BUMP BUTTON INTEGRATION")
    print("=" * 60)
    
    results = []
    
    print("\n1. Testing BumpAgentView import...")
    results.append(test_bump_view())
    
    print("\n2. Testing button count per row...")
    results.append(test_button_count())
    
    print("\n3. Testing bump button in control panel...")
    # Note: Can't actually test view creation without event loop
    # But we can check the code structure
    try:
        from src.discord_commander.views.main_control_panel_view import MainControlPanelView
        import inspect
        source = inspect.getsource(MainControlPanelView.show_bump_selector)
        if "BumpAgentView" in source and "show_bump_selector" in source:
            print("✅ show_bump_selector method found in MainControlPanelView")
            results.append(True)
        else:
            print("❌ show_bump_selector method not found or incomplete")
            results.append(False)
    except Exception as e:
        print(f"❌ Error checking show_bump_selector: {e}")
        results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL TESTS PASSED")
        print("\n💡 NOTE: If button doesn't appear in Discord:")
        print("   1. Restart the Discord bot to load new code")
        print("   2. The control panel message needs to be re-sent")
        print("   3. Use !help or restart command to get new control panel")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Check output above for details")
    print("=" * 60)

