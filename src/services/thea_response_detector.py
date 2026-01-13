#!/usr/bin/env python3
"""
Thea Response Detector - V2 Compliance
=====================================

Monitors ChatGPT responses and detects completion.

<!-- SSOT Domain: infrastructure -->

Author: Agent-6 (Quality Assurance & Reliability)
License: MIT
"""

import time
import logging
from enum import Enum
from typing import Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class ResponseWaitResult(Enum):
    """Response wait result enumeration."""
    COMPLETE = "complete"
    TIMEOUT = "timeout"
    ERROR = "error"
    INTERRUPTED = "interrupted"

@dataclass
class ResponseDetectionResult:
    """Result of response detection."""
    status: ResponseWaitResult
    text: Optional[str] = None
    duration: float = 0.0
    stable_checks: int = 0

class ResponseDetector:
    """
    Detects when ChatGPT responses are complete.

    Uses multiple heuristics:
    - DOM stability (no changes for N seconds)
    - Response indicators (buttons, cursors)
    - Content length stability
    """

    def __init__(self, driver, stability_secs: float = 3.0, max_checks: int = 10):
        """
        Initialize response detector.

        Args:
            driver: Selenium WebDriver instance
            stability_secs: Seconds of stability required
            max_checks: Maximum stability checks
        """
        self.driver = driver
        self.stability_secs = stability_secs
        self.max_checks = max_checks
        self._last_content = ""
        self._last_length = 0

    def wait_until_complete(self, timeout: float = 120.0, stable_secs: float = 3.0,
                          auto_continue: bool = True) -> ResponseWaitResult:
        """
        Wait for response to complete.

        Args:
            timeout: Maximum wait time in seconds
            stable_secs: Stability time required
            auto_continue: Auto-continue if conversation stops

        Returns:
            ResponseWaitResult indicating completion status
        """
        start_time = time.time()
        stable_count = 0
        last_stable_time = 0

        logger.info(f"⏳ Waiting for response completion (timeout: {timeout}s)")

        try:
            while time.time() - start_time < timeout:
                current_time = time.time()

                # Check if response is complete
                if self._is_response_complete():
                    logger.info("✅ Response complete (completion indicator)")
                    return ResponseWaitResult.COMPLETE

                # Check content stability
                current_content = self.extract_response_text() or ""
                current_length = len(current_content)

                if current_length > self._last_length:
                    # Content is still growing
                    stable_count = 0
                    last_stable_time = current_time
                    self._last_content = current_content
                    self._last_length = current_length
                elif current_length == self._last_length and current_length > 0:
                    # Content length stable
                    if current_time - last_stable_time >= stable_secs:
                        stable_count += 1
                        if stable_count >= self.max_checks:
                            logger.info(f"✅ Response complete (stable for {stable_secs}s)")
                            return ResponseWaitResult.COMPLETE
                    # Else continue waiting for more stability checks
                else:
                    # Content length decreased (unexpected)
                    stable_count = 0
                    last_stable_time = current_time

                # Check for auto-continue scenarios
                if auto_continue and self._should_continue():
                    logger.info("🔄 Auto-continuing conversation")
                    self._continue_conversation()

                time.sleep(0.5)  # Check every 0.5 seconds

            logger.warning(f"⏰ Response timeout after {timeout}s")
            return ResponseWaitResult.TIMEOUT

        except KeyboardInterrupt:
            logger.info("🛑 Response detection interrupted")
            return ResponseWaitResult.INTERRUPTED
        except Exception as e:
            logger.error(f"❌ Response detection error: {e}")
            return ResponseWaitResult.ERROR

    def _is_response_complete(self) -> bool:
        """Check if response is complete using DOM indicators."""
        if not self.driver:
            return False

        try:
            # Check for completion indicators
            script = """
            return !document.querySelector('.generating-indicator') &&
                   !document.querySelector('.cursor-blink') &&
                   !document.querySelector('[data-testid="stop-button"]') &&
                   !document.querySelector('.result-streaming');
            """
            return self.driver.execute_script(script)
        except:
            return False

    def _should_continue(self) -> bool:
        """Check if conversation should be continued."""
        if not self.driver:
            return False

        try:
            # Look for continue/regenerate buttons or truncated responses
            continue_selectors = [
                '[data-testid="continue-button"]',
                '.continue-button',
                '.regenerate-button',
                '.truncated-response'
            ]

            for selector in continue_selectors:
                try:
                    element = self.driver.find_element_by_css_selector(selector)
                    if element and element.is_displayed():
                        return True
                except:
                    continue

            return False
        except:
            return False

    def _continue_conversation(self):
        """Continue the conversation if possible."""
        if not self.driver:
            return

        try:
            # Try to click continue button
            continue_selectors = [
                '[data-testid="continue-button"]',
                '.continue-button'
            ]

            for selector in continue_selectors:
                try:
                    button = self.driver.find_element_by_css_selector(selector)
                    if button and button.is_displayed():
                        button.click()
                        logger.info("✅ Clicked continue button")
                        time.sleep(1)
                        return
                except:
                    continue

            logger.warning("⚠️ Could not find continue button")

        except Exception as e:
            logger.error(f"❌ Continue conversation failed: {e}")

    def extract_response_text(self) -> Optional[str]:
        """Extract current response text from page."""
        if not self.driver:
            return None

        try:
            # Primary selectors for ChatGPT responses (updated for current DOM)
            selectors = [
                # Most specific selectors first
                "[data-message-author-role='assistant']:last-child",  # Working selector from debug
                "[data-message-author-role='assistant']:last-of-type .markdown",
                "[data-testid='conversation-turn']:last-child .markdown",
                "[data-message-id]:last-of-type .markdown",
                ".agent-turn:last-child .markdown",
                "article:last-of-type .markdown",
                "article:last-of-type",
                # Additional selectors for current ChatGPT interface
                "[data-testid*='message']:last-child",
                ".markdown:last-of-type",
                "[data-message-id]:last-child",
                ".agent-turn:last-child"  # Another working selector
            ]

            logger.debug(f"🔍 Extracting response text with {len(selectors)} selectors...")
            for i, selector in enumerate(selectors):
                try:
                    # Use find_elements (plural) exactly like the working debug code
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    logger.debug(f"  Selector {i+1} ({selector}): found {len(elements)} elements")

                    if elements:
                        # Check the last elements first (like debug code does with [-2:])
                        for j, element in enumerate(reversed(elements[-2:])):  # Last 2 elements, in reverse order
                            actual_index = len(elements) - j - 1  # Convert back to actual index
                            try:
                                if element and element.is_displayed():
                                    text = element.text.strip() if element.text else ""
                                    logger.debug(f"    Element {actual_index} (from end): text length {len(text)}")
                                    if text and len(text) > 10:  # Minimum viable response
                                        logger.debug(f"  ✅ Using selector {i+1} ({selector}), element {actual_index} - returning response")
                                        return text
                                    else:
                                        logger.debug(f"    ⚠️ Element {actual_index}: text too short or empty ('{text[:50]}...')")
                                else:
                                    logger.debug(f"    ⚠️ Element {actual_index}: not displayed or None")
                            except Exception as e:
                                logger.debug(f"    ⚠️ Element {actual_index}: error checking - {e}")

                except Exception as e:
                    logger.debug(f"  ❌ Selector {i+1} ({selector}): exception - {e}")

            logger.warning("❌ No response text found with any selector")
            return None

        except Exception as e:
            logger.debug(f"Response extraction failed: {e}")
            return None

    def get_response_stats(self) -> dict:
        """Get statistics about current response state."""
        if not self.driver:
            return {"error": "No driver"}

        try:
            current_text = self.extract_response_text() or ""
            is_complete = self._is_response_complete()
            should_continue = self._should_continue()

            return {
                "text_length": len(current_text),
                "is_complete": is_complete,
                "should_continue": should_continue,
                "last_content_length": self._last_length,
                "has_content": len(current_text) > 0
            }

        except Exception as e:
            return {"error": str(e)}


# Convenience function
def wait_for_response(driver, timeout: float = 120.0, stable_secs: float = 3.0) -> Tuple[ResponseWaitResult, Optional[str]]:
    """
    Convenience function to wait for response.

    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum wait time
        stable_secs: Stability time required

    Returns:
        Tuple of (result, response_text)
    """
    detector = ResponseDetector(driver)
    result = detector.wait_until_complete(timeout=timeout, stable_secs=stable_secs)

    if result == ResponseWaitResult.COMPLETE:
        text = detector.extract_response_text()
        return result, text
    else:
        return result, None


__all__ = ["ResponseDetector", "ResponseWaitResult", "ResponseDetectionResult", "wait_for_response"]