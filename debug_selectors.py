#!/usr/bin/env python3
"""
Debug Thea Selectors - Find why textarea discovery is failing
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.infrastructure.browser.thea_browser_service import TheaBrowserService
from src.infrastructure.browser.browser_models import BrowserConfig


def debug_selectors():
    """Debug selector discovery issues."""
    print('=== DEBUGGING SELECTOR DISCOVERY ===')

    config = BrowserConfig(headless=False)
    service = TheaBrowserService(config)

    if service.initialize():
        if service.navigate_to(service.thea_config.conversation_url, wait_seconds=5):
            if service.ensure_thea_authenticated(allow_manual=False):
                if service._wait_for_page_ready(timeout=15):

                    # Check what elements exist
                    textareas = service.driver.find_elements('tag name', 'textarea')
                    contenteditables = service.driver.find_elements('css selector', 'div[contenteditable="true"]')

                    print(f'Found {len(textareas)} textareas:')
                    for i, ta in enumerate(textareas):
                        visible = ta.is_displayed()
                        enabled = ta.is_enabled()
                        ta_id = ta.get_attribute('id')
                        ta_class = ta.get_attribute('class')
                        print(f'  {i}: visible={visible}, enabled={enabled}, id={ta_id}, class={ta_class}')

                    print(f'\nFound {len(contenteditables)} contenteditable divs:')
                    for i, div in enumerate(contenteditables):
                        visible = div.is_displayed()
                        enabled = div.is_enabled()
                        div_id = div.get_attribute('id')
                        div_class = div.get_attribute('class')
                        print(f'  {i}: visible={visible}, enabled={enabled}, id={div_id}, class={div_class}')

                    # Test selector prioritization
                    selectors = service._get_prioritized_selectors()
                    print(f'\nTop 3 prioritized selectors:')
                    for i, sel in enumerate(selectors[:3]):
                        print(f'  {i+1}: {sel}')

                    # Try each selector manually
                    print('\nTesting selectors manually:')
                    for i, sel in enumerate(selectors[:3]):
                        try:
                            elements = service.driver.find_elements('css selector', sel)
                            if elements:
                                el = elements[0]
                                visible = el.is_displayed()
                                enabled = el.is_enabled()
                                print(f'  {sel}: found {len(elements)} elements, first is visible={visible}, enabled={enabled}')
                            else:
                                print(f'  {sel}: no elements found')
                        except Exception as e:
                            print(f'  {sel}: error - {e}')

        service.close()
    else:
        print('Browser init failed')


if __name__ == '__main__':
    debug_selectors()
