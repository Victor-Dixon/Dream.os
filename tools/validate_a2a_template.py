#!/usr/bin/env python3
"""
Validate A2A template contains Directive Push Principle.

<!-- SSOT Domain: core -->
"""

import sys
from pathlib import Path

def validate_template():
    """Check A2A template includes directive push guidance."""
    template_path = Path("src/core/messaging_templates_data/template_a2a.py")
    
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return False
    
    content = template_path.read_text()
    
    required_phrases = [
        "Push directives forward",
        "acknowledge",
        "Messages are fuel for action",
        "confirmation loops"
    ]
    
    content_lower = content.lower()
    missing = [phrase for phrase in required_phrases if phrase.lower() not in content_lower]
    
    if missing:
        print(f"❌ Missing required phrases: {missing}")
        return False
    
    print("✅ A2A template contains Directive Push Principle")
    return True

if __name__ == "__main__":
    success = validate_template()
    sys.exit(0 if success else 1)

