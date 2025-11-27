#!/usr/bin/env python3
"""Check all Discord modal labels for length compliance."""

import re
from pathlib import Path

def check_labels():
    """Check all modal labels in discord_gui_modals.py."""
    file_path = Path("src/discord_commander/discord_gui_modals.py")
    content = file_path.read_text(encoding="utf-8")
    
    # Find all label= patterns
    pattern = r'label=["\']([^"\']+)["\']'
    matches = re.finditer(pattern, content)
    
    issues = []
    for match in matches:
        label = match.group(1)
        length = len(label)
        line_num = content[:match.start()].count('\n') + 1
        
        if length > 45:
            issues.append((line_num, length, label))
    
    if issues:
        print("❌ FOUND LABELS EXCEEDING 45 CHARACTERS:\n")
        for line_num, length, label in issues:
            print(f"  Line {line_num}: {length} chars")
            print(f"    {label}")
            print()
    else:
        print("✅ ALL MODAL LABELS ARE ≤45 CHARACTERS!")
        
        # Show all labels for verification
        print("\n📋 All labels found:")
        matches = re.finditer(pattern, content)
        for match in matches:
            label = match.group(1)
            length = len(label)
            line_num = content[:match.start()].count('\n') + 1
            print(f"  Line {line_num}: {length:2} chars - {label}")

if __name__ == "__main__":
    check_labels()

