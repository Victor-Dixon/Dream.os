#!/usr/bin/env python3
"""
Simple test for refactored messaging_pyautogui functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

from messaging_formatting import MessageFormattingService
from messaging_models import UnifiedMessage, UnifiedMessageType

def test_message_formatting_service():
    """Test MessageFormattingService functionality."""
    service = MessageFormattingService()

    # Test normalize_message with dict
    msg_dict = {'content': 'Test message', 'sender': 'Test', 'recipient': 'Agent-1'}
    result = service.normalize_message(msg_dict)
    assert result is not None and hasattr(result, "content"), "normalize_message(dict) failed"
    print("✓ normalize_message(dict) works")

    # Test normalize_message with string
    result2 = service.normalize_message('Test string')
    assert result2 is not None and hasattr(result2, "content"), "normalize_message(string) failed"
    print("✓ normalize_message(string) works")

    # Test format_message_content
    msg = UnifiedMessage(content='Test', sender='Test', recipient='Agent-1', message_type=UnifiedMessageType.TEXT)
    result3 = service.format_message_content(msg, 'TestSender')
    assert isinstance(result3, str), "format_message_content failed"
    print("✓ format_message_content works")

    print("All MessageFormattingService tests passed!")

if __name__ == "__main__":
    test_message_formatting_service()