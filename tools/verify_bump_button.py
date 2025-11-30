#!/usr/bin/env python3
"""
Verify Bump Button - Check if button is properly configured
==========================================================

Author: Agent-6
Created: 2025-11-30
"""

import sys
from pathlib import Path
import ast

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_button_code():
    """Verify bump button code is in the file."""
    file_path = Path("src/discord_commander/views/main_control_panel_view.py")
    
    if not file_path.exists():
        print("❌ Control panel file not found!")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    
    checks = {
        "bump_btn definition": "self.bump_btn = discord.ui.Button" in content,
        "bump_btn label": '"Bump Agents"' in content or "'Bump Agents'" in content,
        "bump_btn custom_id": '"control_bump"' in content or "'control_bump'" in content,
        "bump_btn row": "row=2" in content.split("control_bump")[1].split("\n")[0] if "control_bump" in content else False,
        "bump_btn callback": "self.bump_btn.callback = self.show_bump_selector" in content,
        "bump_btn added": "self.add_item(self.bump_btn)" in content,
        "show_bump_selector method": "async def show_bump_selector" in content,
        "BumpAgentView import": "from .bump_agent_view import BumpAgentView" in content,
    }
    
    print("=" * 60)
    print("VERIFYING BUMP BUTTON CODE")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    # Count buttons in row 2
    lines = content.split("\n")
    row_2_buttons = []
    in_row_2 = False
    for i, line in enumerate(lines):
        if "row=2" in line and "Button" in lines[max(0, i-5):i+1]:
            # Find the button label
            for j in range(max(0, i-10), i+1):
                if 'label=' in lines[j] or 'label =' in lines[j]:
                    label_line = lines[j]
                    if '"' in label_line:
                        label = label_line.split('"')[1]
                    elif "'" in label_line:
                        label = label_line.split("'")[1]
                    else:
                        label = "Unknown"
                    row_2_buttons.append(label)
                    break
    
    print(f"\n📊 Buttons in Row 2: {len(row_2_buttons)}")
    for btn in row_2_buttons:
        print(f"   - {btn}")
    
    if len(row_2_buttons) > 5:
        print(f"\n⚠️ WARNING: Row 2 has {len(row_2_buttons)} buttons (Discord limit: 5)")
        all_passed = False
    elif "Bump Agents" not in row_2_buttons:
        print("\n⚠️ WARNING: 'Bump Agents' not found in Row 2 buttons")
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CODE CHECKS PASSED")
        print("\n💡 IMPORTANT: To see the button in Discord:")
        print("   1. Restart the Discord bot (code changes require restart)")
        print("   2. The control panel message needs to be RE-SENT")
        print("      (Discord buttons are tied to the message - can't edit)")
        print("   3. Use !help command or restart bot to get new control panel")
    else:
        print("❌ SOME CHECKS FAILED")
        print("   Review the output above")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    verify_button_code()

