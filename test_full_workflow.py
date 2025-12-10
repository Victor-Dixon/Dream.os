#!/usr/bin/env python3
"""
Test Full Thea Automation Workflow
==================================

Tests the complete Thea prompt submission and response retrieval workflow.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.infrastructure.browser.thea_browser_service import TheaBrowserService
from src.infrastructure.browser.browser_models import BrowserConfig


def test_full_workflow():
    """Test the complete Thea automation workflow."""
    print('=== FULL THEA AUTOMATION WORKFLOW TEST ===')
    print()

    config = BrowserConfig(headless=False)
    service = TheaBrowserService(config)

    try:
        print('1. Initializing Thea service...')
        if not service.initialize():
            print('❌ Browser initialization failed')
            return False

        print('2. Testing send_prompt_and_get_response...')
        test_prompt = "Hello, this is a test message from Agent-3 infrastructure testing."

        print(f'   Sending prompt: "{test_prompt[:50]}..."')

        response = service.send_prompt_and_get_response_text(
            prompt=test_prompt,
            timeout=60,  # Shorter timeout for testing
            poll_interval=2
        )

        if response:
            print('✅ Response received!')
            print(f'   Response length: {len(response)} characters')
            print(f'   Response preview: {response[:100]}...')
            return True
        else:
            print('❌ No response received')
            return False

    except Exception as e:
        print(f'❌ Workflow test failed: {e}')
        return False

    finally:
        service.close()
        print('Browser closed')


if __name__ == '__main__':
    success = test_full_workflow()
    sys.exit(0 if success else 1)
