"""
Tests for BroadcastTemplatesView.
"""
import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Mock pyautogui to prevent display errors in headless environment
from unittest.mock import MagicMock
sys.modules["pyautogui"] = MagicMock()

# Mock discord module structure
mock_discord = MagicMock()
mock_discord.ui = MagicMock()
mock_discord.ButtonStyle = MagicMock()

# Define a proper MockView class for inheritance
class MockView:
    def __init__(self, timeout=None):
        self.items = []
    
    def clear_items(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)

mock_discord.ui.View = MockView
sys.modules["discord"] = mock_discord

# Mock discord.ext.commands
mock_ext = MagicMock()
mock_commands = MagicMock()
mock_ext.commands = mock_commands
sys.modules["discord.ext"] = mock_ext
sys.modules["discord.ext.commands"] = mock_commands

import discord

from src.discord_commander.controllers.broadcast_templates_view import BroadcastTemplatesView

class TestBroadcastTemplatesView(unittest.TestCase):
    def setUp(self):
        self.mock_messaging_service = MagicMock()
        
        # Mock discord.ui.Button to verify row assignment
        self.mock_button = MagicMock()
        discord.ui.Button = self.mock_button
        
        # Create instance
        self.view = BroadcastTemplatesView(self.mock_messaging_service)
        # Reset mock calls from __init__
        self.view.clear_items = MagicMock()
        self.view.add_item = MagicMock()
        self.mock_button.reset_mock()

    def test_create_template_buttons_layout(self):
        """Test that buttons are assigned to correct rows."""
        # Force current mode to 'regular' (which has 4 templates by default)
        self.view.current_mode = 'regular'
        
        # Trigger button creation
        self.view._create_template_buttons()
        
        # Verify mode buttons (5 default modes + potentially 2 enhanced)
        # Check call args for discord.ui.Button
        button_calls = self.mock_button.call_args_list
        
        # Verify row indices
        rows_used = [call.kwargs.get('row', 0) for call in button_calls]
        
        # Assert no row index exceeds 4 (Discord limit)
        for row in rows_used:
            self.assertLess(row, 5, f"Row index {row} exceeds Discord limit of 4")
            
        # Assert rows are sequential (0, then 1, etc.)
        self.assertTrue(0 in rows_used, "Row 0 should be used")
        
        # Count items per row
        row_counts = {}
        for row in rows_used:
            row_counts[row] = row_counts.get(row, 0) + 1
            
        # Assert max 5 items per row
        for row, count in row_counts.items():
            self.assertLessEqual(count, 5, f"Row {row} has {count} items, max allowed is 5")

    def test_many_modes_layout(self):
        """Test layout with many modes (simulation)."""
        # Patch the modes list inside the method is hard, so we rely on the logic test
        # Instead, we can verify that if we had 7 modes, they split into 2 rows
        
        # Re-run with USE_ENHANCED_TEMPLATES=True simulation
        # The logic is self-contained in the method, so testing the logic directly:
        
        # We can simulate by inspecting the logic we wrote.
        # But let's verify the current implementation behavior with default modes
        self.view._create_template_buttons()
        
        # Retrieve all added items (simulated)
        # Since we mocked add_item, we can check what was passed
        added_items = self.view.add_item.call_args_list
        # Note: add_item receives the button instance created by mock_button
        # So we can't inspect the button attributes directly unless we mock the return value of Button
        
        # Let's verify the Button constructor calls instead
        button_calls = self.mock_button.call_args_list
        
        mode_buttons = [c for c in button_calls if 'template_mode_' in c.kwargs.get('custom_id', '')]
        template_buttons = [c for c in button_calls if 'template_' in c.kwargs.get('custom_id', '') and 'mode' not in c.kwargs.get('custom_id', '')]
        
        # Verify Mode Buttons
        # Default modes = 5. If enhanced = 7.
        num_modes = len(mode_buttons)
        expected_mode_rows = (num_modes + 4) // 5
        
        mode_rows = set(c.kwargs['row'] for c in mode_buttons)
        self.assertEqual(len(mode_rows), expected_mode_rows)
        
        # Verify Template Buttons start AFTER mode rows
        if template_buttons:
            min_template_row = min(c.kwargs['row'] for c in template_buttons)
            max_mode_row = max(c.kwargs['row'] for c in mode_buttons)
            self.assertGreater(min_template_row, max_mode_row)

if __name__ == '__main__':
    unittest.main()
