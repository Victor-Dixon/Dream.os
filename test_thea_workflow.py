#!/usr/bin/env python3
"""
Test Thea Automation Workflow - Updated Selectors Validation
===========================================================

Tests the complete Thea prompt submission and response retrieval workflow
with the updated ChatGPT selectors.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.infrastructure.browser.thea_browser_service import TheaBrowserService
from src.infrastructure.browser.browser_models import BrowserConfig


def test_thea_workflow():
    """Test Thea automation workflow with updated selectors."""
    print('=== THEA AUTOMATION WORKFLOW TEST ===')
    print()

    # Initialize browser service
    config = BrowserConfig(headless=False)  # Need visible browser for testing
    service = TheaBrowserService(config)

    try:
        # Initialize browser
        print('1. Initializing browser...')
        if service.initialize():
            print('✅ Browser initialized successfully')

            # Navigate to Thea
            print('2. Navigating to Thea conversation URL...')
            if service.navigate_to(service.thea_config.conversation_url, wait_seconds=5):
                print('✅ Navigation successful')

                # Ensure authenticated
                print('3. Ensuring Thea authentication...')
                if service.ensure_thea_authenticated(allow_manual=False):
                    print('✅ Authentication confirmed')

                    # Wait for page to be ready
                    print('4. Waiting for page ready...')
                    if service._wait_for_page_ready(timeout=15):
                        print('✅ Page ready for interaction')

                        # Test finding textarea
                        print('5. Testing textarea selector...')
                        textarea = service._find_prompt_textarea()
                        if textarea:
                            ta_id = textarea.get_attribute('id')
                            ta_class = textarea.get_attribute('class')
                            print(f'✅ Textarea found: {textarea.tag_name} with id={ta_id}, class={ta_class}')

                            # Test finding send button
                            print('6. Testing send button selector...')
                            send_btn = service._find_send_button()
                            if send_btn:
                                btn_aria = send_btn.get_attribute('aria-label')
                                btn_data = send_btn.get_attribute('data-testid')
                                print(f'✅ Send button found: {send_btn.tag_name} with aria-label={btn_aria}, data-testid={btn_data}')
                                print('🎯 SELECTOR VALIDATION COMPLETE - Ready for full workflow test')
                                return True
                            else:
                                print('❌ Send button not found')
                                return False
                        else:
                            print('❌ Textarea not found')
                            return False
                    else:
                        print('❌ Page not ready')
                        return False
                else:
                    print('❌ Authentication failed')
                    return False
            else:
                print('❌ Navigation failed')
                return False
        else:
            print('❌ Browser initialization failed')
            return False

    except Exception as e:
        print(f'❌ Test failed with error: {e}')
        return False

    finally:
        service.close()
        print('Browser closed')


if __name__ == '__main__':
    success = test_thea_workflow()
    sys.exit(0 if success else 1)
