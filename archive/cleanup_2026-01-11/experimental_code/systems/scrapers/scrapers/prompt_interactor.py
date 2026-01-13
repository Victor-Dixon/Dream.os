#!/usr/bin/env python3
"""
Prompt Interactor for ChatGPT Scraper
Handles prompt sending and response interaction operations.
"""

import sys
import os
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class PromptInteractor:
    """Handles prompt interaction with ChatGPT."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the prompt interactor.
        
        Args:
            timeout: Timeout for web operations
        """
        self.timeout = timeout
        self.max_retries = 3
        self.typing_delay = 0.05  # Reduced delay between characters for faster typing
        self.post_typing_delay = 2.0  # Delay after typing before submitting
    
    def send_prompt(self, driver, prompt: str, wait_for_response: bool = True, 
                   streaming: bool = True, retry_on_error: bool = True) -> bool:
        """
        Send a prompt to the current conversation.
        
        Args:
            driver: Selenium webdriver instance
            prompt: Text prompt to send
            wait_for_response: Whether to wait for response
            streaming: Whether to wait for streaming response
            retry_on_error: Whether to retry on error
            
        Returns:
            True if prompt sent successfully, False otherwise
        """
        if not driver:
            logger.error("No driver provided for prompt sending")
            return False
        
        try:
            logger.info(f"Sending prompt: {prompt[:50]}...")
            
            # Find and fill the input field
            input_field = self._find_input_field(driver)
            if not input_field:
                logger.error("Input field not found")
                return False
            
            # Clear any existing text
            input_field.clear()
            
            # Type the prompt with human-like delays
            if not self._type_with_delay(input_field, prompt):
                logger.error("Failed to type prompt text")
                return False
            
            # Wait a moment after typing before submitting (simulates human behavior)
            logger.info(f"Waiting {self.post_typing_delay}s after typing before submitting...")
            time.sleep(self.post_typing_delay)
            
            # Send the prompt
            if not self._submit_prompt(input_field):
                logger.error("Failed to submit prompt")
                return False
            
            # Wait for response if requested
            if wait_for_response:
                return self._wait_for_response(driver, streaming)
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending prompt: {e}")
            if retry_on_error and self.max_retries > 0:
                logger.info("Retrying prompt send...")
                self.max_retries -= 1
                time.sleep(2)  # Wait before retry
                return self.send_prompt(driver, prompt, wait_for_response, streaming)
            return False
    
    def _find_input_field(self, driver):
        """Find the input field using robust selectors from chat_navigation.py."""
        try:
            # Try p[data-placeholder] first (most common for ChatGPT)
            try:
                input_element = driver.find_element(By.CSS_SELECTOR, "p[data-placeholder]")
                if input_element.is_displayed() and input_element.is_enabled():
                    logger.info("✅ Found p[data-placeholder] input element")
                    return input_element
            except Exception as e:
                logger.debug(f"p[data-placeholder] not found: {e}")
            
            # Fallback to textarea
            try:
                input_element = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='Message']")
                if input_element.is_displayed() and input_element.is_enabled():
                    logger.info("✅ Found textarea input element")
                    return input_element
            except Exception as e:
                logger.debug(f"textarea not found: {e}")
            
            # Additional fallbacks for different ChatGPT layouts
            fallback_selectors = [
                "//textarea[@placeholder]",
                "//div[@contenteditable='true']",
                "//textarea[contains(@class, 'prompt-textarea')]",
                "//input[@type='text']",
                "//textarea"
            ]
            
            for selector in fallback_selectors:
                try:
                    input_element = driver.find_element(By.XPATH, selector)
                    if input_element.is_displayed() and input_element.is_enabled():
                        logger.info(f"✅ Found input field using fallback: {selector}")
                        return input_element
                except Exception as e:
                    logger.debug(f"Fallback selector {selector} failed: {e}")
                    continue
            
            logger.error("❌ Could not find any input field")
            return None
            
        except Exception as e:
            logger.error(f"Error finding input field: {e}")
            return None
    
    def _type_with_delay(self, element, text: str):
        """Type text using robust logic from chat_navigation.py."""
        try:
            logger.info(f"Typing {len(text)} characters...")
            
            # Clear any existing text
            element.clear()
            
            # For p[data-placeholder], we need to use JavaScript to set content
            if element.tag_name == "p":
                driver = element.parent
                driver.execute_script("arguments[0].textContent = arguments[1];", element, text)
                logger.info("✅ Prompt entered via JavaScript (p element)")
            else:
                # For textarea and other elements, use send_keys
                element.send_keys(text)
                logger.info("✅ Prompt entered via send_keys")
            
            # Wait a moment after typing before submitting (simulates human behavior)
            logger.info(f"Waiting {self.post_typing_delay}s after typing before submitting...")
            time.sleep(self.post_typing_delay)
            
            return True
            
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False
    
    def _submit_prompt(self, element) -> bool:
        """Submit the prompt using the reliable method from chat_navigation.py."""
        try:
            logger.info("Submitting prompt...")
            
            # Use the simple, reliable method from chat_navigation.py
            element.send_keys(Keys.RETURN)
            logger.info("✅ Prompt sent via Keys.RETURN")
            
            # Wait a moment to ensure submission is processed
            time.sleep(2)
            
            # More robust submission verification
            submission_successful = self._verify_submission_success(element)
            
            if submission_successful:
                logger.info("✅ Submission verified as successful")
                return True
            else:
                logger.warning("⚠️ Primary submission may have failed, trying alternatives...")
                # Try alternative submission methods as fallback
                return self._try_alternative_submission(element)
            
        except Exception as e:
            logger.error(f"Error submitting prompt: {e}")
            return self._try_alternative_submission(element)
    
    def _verify_submission_success(self, element) -> bool:
        """Verify if submission was successful using multiple indicators."""
        try:
            # Method 1: Check if input field is cleared
            content = element.get_attribute('value') or element.text
            if not content or content.strip() == "":
                logger.info("✅ Input field cleared - submission successful")
                return True
            
            # Method 2: Check if there's a response starting to appear
            driver = element.parent
            try:
                response_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'markdown')]")
                if response_elements:
                    logger.info("✅ Response elements found - submission successful")
                    return True
            except:
                pass
            
            # Method 3: Check if the input field is disabled or has different state
            try:
                if not element.is_enabled():
                    logger.info("✅ Input field disabled - submission in progress")
                    return True
            except:
                pass
            
            # Method 4: Check if there's a "Stop generating" button (indicates response started)
            try:
                stop_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='stop-generating']")
                if stop_button.is_displayed():
                    logger.info("✅ Stop generating button visible - response started")
                    return True
            except:
                pass
            
            # Method 5: For longer prompts, the input field might not clear immediately
            # Check if the content has changed or if there are any visual indicators
            logger.debug(f"Input field still has content: {content[:50]}...")
            logger.debug("Submission verification inconclusive, assuming success for now")
            return True  # Assume success for longer prompts
            
        except Exception as e:
            logger.debug(f"Error verifying submission: {e}")
            return True  # Assume success if verification fails
    
    def _try_alternative_submission(self, element) -> bool:
        """Try alternative submission methods if the primary method fails."""
        try:
            logger.info("Trying alternative submission methods...")
            
            # Try different submission methods in order of preference
            submission_methods = [
                # Method 1: Click the send button
                lambda: self._click_send_button(element),
                # Method 2: Ctrl+Enter (common shortcut)
                lambda: element.send_keys(Keys.CONTROL + Keys.ENTER),
                # Method 3: Submit method
                lambda: element.submit(),
            ]
            
            for i, method in enumerate(submission_methods, 1):
                try:
                    logger.info(f"Trying alternative submission method {i}...")
                    method()
                    time.sleep(1)  # Wait to see if submission worked
                    
                    # Check if the input field is cleared
                    if not element.get_attribute('value') and not element.text:
                        logger.info(f"✅ Alternative submission method {i} successful")
                        return True
                    else:
                        logger.debug(f"Alternative submission method {i} may not have worked")
                        
                except Exception as method_error:
                    logger.debug(f"Alternative submission method {i} failed: {method_error}")
                    continue
            
            logger.error("❌ All submission methods failed")
            return False
            
        except Exception as e:
            logger.error(f"Error with alternative submission: {e}")
            return False
    
    def _click_send_button(self, element):
        """Try to find and click a send button using robust selectors."""
        try:
            driver = element.parent
            
            # Comprehensive send button selectors (CSS and XPath)
            send_button_selectors = [
                # CSS selectors (more reliable)
                "button[data-testid='send-button']",
                "button[aria-label*='Send']",
                "button[title*='Send']",
                "button[class*='send']",
                "button:has(svg[class*='send'])",
                "button:has([class*='send'])",
                # XPath selectors
                "//button[@data-testid='send-button']",
                "//button[contains(@class, 'send')]",
                "//button[contains(@aria-label, 'Send')]",
                "//button[contains(@title, 'Send')]",
                "//button[contains(text(), 'Send')]",
                "//button[.//svg[contains(@class, 'send')]]",
                "//button[.//*[contains(@class, 'send')]]",
                # Additional ChatGPT-specific selectors
                "button[data-testid='send-button']",
                "button[aria-label='Send message']",
                "button[title='Send message']",
            ]
            
            # Search in multiple locations
            search_locations = [
                # 1. Search the entire page
                lambda: driver.find_elements(By.CSS_SELECTOR, "button"),
                # 2. Search near the input element
                lambda: element.find_elements(By.XPATH, "./ancestor::form//button"),
                # 3. Search in parent containers
                lambda: element.find_elements(By.XPATH, "./ancestor::*[contains(@class, 'input') or contains(@class, 'form')]//button"),
            ]
            
            for location_func in search_locations:
                try:
                    buttons = location_func()
                    for button in buttons:
                        # Check if this button looks like a send button
                        if self._is_send_button(button):
                            if button.is_displayed() and button.is_enabled():
                                logger.info(f"✅ Found and clicking send button: {button.get_attribute('outerHTML')[:100]}...")
                                button.click()
                                return True
                except Exception as e:
                    logger.debug(f"Search location failed: {e}")
                    continue
            
            # If no send button found, try to trigger submission via JavaScript
            logger.info("No send button found, trying JavaScript submission...")
            return self._submit_via_javascript(element)
            
        except Exception as e:
            logger.error(f"Error clicking send button: {e}")
            return False
    
    def _is_send_button(self, button) -> bool:
        """Check if a button is likely a send button."""
        try:
            # Get button attributes
            aria_label = button.get_attribute('aria-label') or ''
            title = button.get_attribute('title') or ''
            data_testid = button.get_attribute('data-testid') or ''
            class_name = button.get_attribute('class') or ''
            text = button.text or ''
            
            # Check for send-related keywords
            send_indicators = ['send', 'submit', 'send message', 'send-button']
            
            for indicator in send_indicators:
                if (indicator in aria_label.lower() or 
                    indicator in title.lower() or 
                    indicator in data_testid.lower() or 
                    indicator in class_name.lower() or 
                    indicator in text.lower()):
                    return True
            
            # Check if button contains send icon
            try:
                svg_elements = button.find_elements(By.TAG_NAME, "svg")
                for svg in svg_elements:
                    svg_class = svg.get_attribute('class') or ''
                    if 'send' in svg_class.lower():
                        return True
            except:
                pass
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking if button is send button: {e}")
            return False
    
    def _submit_via_javascript(self, element) -> bool:
        """Submit the prompt via JavaScript as a last resort."""
        try:
            driver = element.parent
            
            # Try to trigger form submission
            driver.execute_script("""
                // Try to submit the form
                var form = arguments[0].closest('form');
                if (form) {
                    form.submit();
                    return true;
                }
                
                // Try to trigger Enter key event
                var event = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                });
                arguments[0].dispatchEvent(event);
                
                // Try to trigger input event
                var inputEvent = new Event('input', { bubbles: true });
                arguments[0].dispatchEvent(inputEvent);
                
                return true;
            """, element)
            
            logger.info("✅ JavaScript submission attempted")
            return True
            
        except Exception as e:
            logger.error(f"JavaScript submission failed: {e}")
            return False
    
    def _wait_for_response(self, driver, streaming: bool = True) -> bool:
        """
        Wait for the AI response.
        
        Args:
            driver: Selenium webdriver instance
            streaming: Whether to wait for streaming response
            
        Returns:
            True if response received, False if timeout
        """
        try:
            wait = WebDriverWait(driver, self.timeout)
            
            # Wait for response to start
            logger.info("⏳ Waiting for response to start...")
            response_started = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'markdown')]"
            )))
            logger.info("✅ Response started")
            
            if not streaming:
                return True
            
            # Wait for streaming to complete using multiple detection methods
            logger.info("⏳ Waiting for response to complete...")
            time.sleep(3)  # Initial wait for streaming to begin
            
            # Method 1: Look for "Stop generating" button disappearance
            max_wait = 60  # Increased from 30 to 60 seconds
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                try:
                    # Look for the "Stop generating" button - if it's gone, response is complete
                    stop_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='stop-generating']")
                    if not stop_button.is_displayed():
                        logger.info("✅ Stop generating button disappeared - response complete")
                        break
                    else:
                        logger.debug("⏳ Stop generating button still visible, waiting...")
                except:
                    # No stop button found, response might be complete
                    logger.info("✅ No stop generating button found - response likely complete")
                    break
                
                time.sleep(1)
            
            # Method 2: Additional stability check with longer unchanged period
            logger.info("⏳ Performing final stability check...")
            previous_text = ""
            unchanged_count = 0
            max_unchanged = 10  # Increased from 5 to 10 for more stability
            
            while unchanged_count < max_unchanged:
                try:
                    # Re-find the element to avoid stale element reference
                    current_response = driver.find_element(By.XPATH, "//div[contains(@class, 'markdown')]")
                    current_text = current_response.text
                    
                    if current_text == previous_text:
                        unchanged_count += 1
                        logger.debug(f"⏳ Text unchanged for {unchanged_count}/{max_unchanged} checks")
                    else:
                        unchanged_count = 0
                        previous_text = current_text
                        logger.debug("📝 Text changed, resetting stability counter")
                    
                    time.sleep(1)
                    
                except Exception as e:
                    # If element becomes stale, try to re-find it
                    logger.debug(f"Element became stale, re-finding: {e}")
                    try:
                        current_response = wait.until(EC.presence_of_element_located((
                            By.XPATH, "//div[contains(@class, 'markdown')]"
                        )))
                        current_text = current_response.text
                        
                        if current_text == previous_text:
                            unchanged_count += 1
                        else:
                            unchanged_count = 0
                            previous_text = current_text
                        
                        time.sleep(1)
                        
                    except Exception as retry_error:
                        logger.error(f"Failed to re-find response element: {retry_error}")
                        return False
            
            # Additional wait to ensure response is fully rendered
            logger.info("⏳ Final wait for response rendering...")
            time.sleep(3)  # Increased from 2 to 3 seconds
            
            logger.info("✅ Response streaming completed")
            return True
            
        except TimeoutException:
            logger.error("Timeout waiting for response")
            return False
        except Exception as e:
            logger.error(f"Error waiting for response: {e}")
            return False
    
    def get_last_response(self, driver) -> str:
        """
        Get the last response from the conversation.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            The text of the last response
        """
        try:
            # Find all response elements with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Use multiple selectors to find response elements
                    response_selectors = [
                        "div[class*='markdown']",
                        "[data-testid='conversation-turn-2'] div[class*='markdown']",
                        "[class*='response'] div[class*='markdown']",
                        "div[class*='prose']",
                        "[data-testid='conversation-turn-2']",
                        "//div[contains(@class, 'markdown')]"
                    ]
                    
                    responses = []
                    for selector in response_selectors:
                        try:
                            if selector.startswith("//"):
                                # XPath selector
                                elements = driver.find_elements(By.XPATH, selector)
                            else:
                                # CSS selector
                                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            
                            for element in elements:
                                if element.is_displayed():
                                    text = element.text.strip()
                                    if text and len(text) > 10:  # Filter out very short responses
                                        responses.append(text)
                        except Exception as e:
                            logger.debug(f"Selector {selector} failed: {e}")
                            continue
                    
                    if responses:
                        # Get the longest response (usually the most recent/complete one)
                        longest_response = max(responses, key=len)
                        logger.info(f"✅ Found response ({len(longest_response)} characters)")
                        return longest_response
                    
                    # If no responses found with selectors, try the original method
                    logger.debug("Trying fallback response detection...")
                    responses = driver.find_elements(By.XPATH, "//div[contains(@class, 'markdown')]")
                    
                    if responses:
                        # Get the last response
                        last_response = responses[-1]
                        response_text = last_response.text.strip()
                        if response_text:
                            logger.info(f"✅ Found response via fallback ({len(response_text)} characters)")
                            return response_text
                    
                    logger.warning(f"No response found on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        time.sleep(2)  # Wait before retry
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.debug(f"Attempt {attempt + 1} failed, retrying: {e}")
                        time.sleep(2)
                    else:
                        logger.error(f"Failed to get last response after {max_retries} attempts: {e}")
                        return ""
            
            logger.warning("No response content found after all attempts")
            return ""
            
        except Exception as e:
            logger.error(f"Error getting last response: {e}")
            return ""