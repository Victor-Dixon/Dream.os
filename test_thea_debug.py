#!/usr/bin/env python3
"""
Test Thea cookie loading fix
"""

from src.services.thea.thea_service import TheaService

def test_thea_communication():
    """Test complete Thea communication flow."""
    print('🧪 Testing complete Thea flow (cookie loading + message sending)...')

    thea = TheaService()
    try:
        # Test full communication cycle
        print('🔄 Testing full Thea communication...')
        result = thea.communicate('Hello Thea, this is a test message from the debug session. Please acknowledge.')

        success = result.get('success', False)
        response = result.get('response', '')

        print(f'Communication result: Success={success}')

        if success:
            print('✅ Message sent and response received!')
            print(f'Response length: {len(response)} characters')
            print(f'Response preview: {response[:200]}...')
            return True
        else:
            print('❌ Communication failed')
            print(f'Error response: {response}')

            # Debug: Check what response elements exist (if driver still available)
            if hasattr(thea, 'driver') and thea.driver:
                print('🔍 Debugging response elements...')
                try:
                    from selenium.webdriver.common.by import By
                    # Check for any response-like elements
                    response_selectors = [
                        "[data-message-author-role='assistant']",
                        "[data-testid*='message']",
                        "article",
                        ".markdown",
                        "[data-message-id]",
                        ".agent-turn"
                    ]

                    for selector in response_selectors:
                        try:
                            elements = thea.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                print(f"Found {len(elements)} elements with selector '{selector}'")
                                for i, elem in enumerate(elements[-2:]):  # Last 2
                                    text = elem.text[:100] if elem.text else "empty"
                                    print(f"  Element {i+1}: '{text}'...")
                        except Exception as e:
                            print(f"Selector '{selector}' failed: {e}")

                except Exception as e:
                    print(f"Debug failed: {e}")

            return False

    except Exception as e:
        print(f'❌ Test failed with exception: {e}')
        return False
    finally:
        thea.cleanup()
        print('✅ Full test completed')

if __name__ == '__main__':
    test_thea_communication()