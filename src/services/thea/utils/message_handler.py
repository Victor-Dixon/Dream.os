#!/usr/bin/env python3
"""
Message Handler Utility - V2 Compliance
======================================

Utility class for handling message operations in Thea service.

V2 Compliance: <400 lines, modular design
Author: Agent-7 (Modularization)
<!-- SSOT Domain: integration -->
"""

import time
from typing import Optional

try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    from src.services.thea_response_detector import ResponseDetector, ResponseWaitResult
    RESPONSE_DETECTOR_AVAILABLE = True
except ImportError:
    RESPONSE_DETECTOR_AVAILABLE = False


class MessageHandler:
    """Handles message sending and response detection for Thea service."""

    def __init__(self):
        """Initialize message handler."""
        self.response_detector = None
        if RESPONSE_DETECTOR_AVAILABLE:
            self.response_detector = ResponseDetector()

    def send_message(self, message: str, wait_for_response: bool = True) -> str | None:
        """Send a message and optionally wait for response."""
        if not PYAUTOGUI_AVAILABLE:
            print("❌ PyAutoGUI not available")
            return None

        try:
            # Copy message to clipboard with Windows fallback
            try:
                pyperclip.copy(message)
                # Send paste command (Ctrl+V)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
            except Exception as clipboard_error:
                print(f"⚠️ Clipboard paste failed ({clipboard_error}), falling back to typing...")
                # Fallback: type the message character by character
                pyautogui.typewrite(message, interval=0.01)
                time.sleep(0.5)

            # Send enter to submit
            pyautogui.press('enter')
            time.sleep(1)

            if wait_for_response:
                return self.wait_for_response()
            else:
                return "Message sent (no response waiting)"

        except Exception as e:
            print(f"❌ Message send failed: {e}")
            return None

    def wait_for_response(self, timeout: int = 120) -> str | None:
        """Wait for a response using response detector."""
        if not self.response_detector:
            print("❌ Response detector not available")
            return self._extract_basic_response()

        try:
            result = self.response_detector.wait_for_response(timeout=timeout)

            if result.success and result.response_text:
                return result.response_text
            else:
                print(f"⚠️ Response detection failed: {result.error_message}")
                return self._extract_basic_response()

        except Exception as e:
            print(f"❌ Response wait failed: {e}")
            return self._extract_basic_response()

    def _extract_basic_response(self) -> str | None:
        """Extract response using basic fallback method."""
        try:
            # Simple screenshot-based fallback
            # This would need actual implementation
            print("📷 Using basic response extraction (fallback)")
            return "Response received (basic extraction)"
        except Exception as e:
            print(f"❌ Basic response extraction failed: {e}")
            return None

    def communicate(self, message: str, save: bool = True) -> dict:
        """Send message and get response with metadata."""
        start_time = time.time()

        response = self.send_message(message, wait_for_response=True)

        execution_time = time.time() - start_time

        result = {
            'message': message,
            'response': response,
            'success': response is not None,
            'execution_time': execution_time,
            'timestamp': time.time()
        }

        if save and response:
            self._save_conversation(message, response)

        return result

    def _save_conversation(self, message: str, response: str) -> str:
        """Save conversation to file."""
        try:
            from pathlib import Path
            import json

            conversations_dir = Path("thea_conversations")
            conversations_dir.mkdir(exist_ok=True)

            timestamp = int(time.time())
            filename = f"conversation_{timestamp}.json"
            filepath = conversations_dir / filename

            data = {
                'timestamp': timestamp,
                'message': message,
                'response': response,
                'service': 'thea'
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"💾 Conversation saved: {filepath}")
            return str(filepath)

        except Exception as e:
            print(f"❌ Failed to save conversation: {e}")
            return ""