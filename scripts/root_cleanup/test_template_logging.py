#!/usr/bin/env python3
"""
Test script to test template application directly to trigger logging.
This will help verify the duplicate message fix.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.messaging_infrastructure import _apply_template
from src.core.messaging_template_texts import MessageCategory
from src.core.messaging_core import UnifiedMessagePriority

def main():
    """Test template application directly."""
    
    # Test message - should appear only once in the template
    test_message = "Test message for duplicate detection - this should appear only once in the User Message section"
    
    print("=" * 60)
    print("Testing template application directly...")
    print(f"Message: {test_message}")
    print("=" * 60)
    
    # Apply D2A template directly
    result = _apply_template(
        category=MessageCategory.D2A,
        message=test_message,
        sender="Test User",
        recipient="Agent-7",
        priority=UnifiedMessagePriority.REGULAR,
        message_id="test_msg_001",
        extra={}  # No extra metadata - this should trigger the default actions
    )
    
    print("\n" + "=" * 60)
    print("TEMPLATE RESULT:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    
    # Check for duplicates
    message_count = result.count(test_message)
    print(f"\nMessage appears {message_count} time(s) in template")
    
    if message_count > 1:
        print("⚠️  DUPLICATE DETECTED - Message appears multiple times!")
    elif message_count == 1:
        print("✅ Message appears exactly once (correct)")
    else:
        print("❌ Message not found in template (unexpected)")
    
    print("\n" + "=" * 60)
    print("Check the log file at: d:\\Agent_Cellphone_V2_Repository\\.cursor\\debug.log")
    print("Look for:")
    print("  - 'format_success' entries showing message_appears_count")
    print("  - 'duplicate_detected' entries if duplication is found")
    print("=" * 60)
    
    return 0 if message_count == 1 else 1

if __name__ == "__main__":
    sys.exit(main())
