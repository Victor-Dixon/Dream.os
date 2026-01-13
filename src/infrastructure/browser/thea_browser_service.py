#!/usr/bin/env python3
"""
Thea Browser Service - V2 Compliance (Refactored)
==================================================

Unified browser service for Thea Manager automation.
Refactored to use extracted modules: core, operations, utils.

This service now acts as an orchestration layer that delegates to:
- TheaBrowserCore: Browser initialization and lifecycle
- TheaBrowserOperations: Navigation, authentication, prompt/response operations
- TheaBrowserUtils: Cookie management, selector caching utilities

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - V2 Refactoring Batch 1 Module 5
Date: 2025-12-14
License: MIT
"""

import logging
from pathlib import Path
from typing import Any

from .browser_models import BrowserConfig, TheaConfig
from .thea_browser_core import TheaBrowserCore
from .thea_browser_operations import TheaBrowserOperations
from .thea_browser_utils import TheaBrowserUtils

logger = logging.getLogger(__name__)


class TheaBrowserService:
    """Unified browser service for Thea Manager automation (V2 refactored)."""

    def __init__(self, config: BrowserConfig | None = None, thea_config: TheaConfig | None = None):
        """Initialize browser service with refactored modules."""
        self.config = config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()

        # Initialize core module
        self.core = TheaBrowserCore(
            config=self.config, thea_config=self.thea_config)

        # Initialize utilities
        self.browser_utils = TheaBrowserUtils(self.thea_config)

        # Operations will be initialized after core is ready
        self.operations: TheaBrowserOperations | None = None
        self._initialized = False

    def initialize(self, profile_name: str | None = None, user_data_dir: str | None = None) -> bool:
        """Initialize browser with optional profile."""
        if not self.core.initialize(profile_name, user_data_dir):
            return False

        # Initialize operations module with driver and element finders
        driver = self.core.get_driver()
        if not driver:
            return False

        self.operations = TheaBrowserOperations(
            driver=driver,
            thea_config=self.thea_config,
            browser_utils=self.browser_utils,
            find_textarea_func=self._find_prompt_textarea,
            find_send_button_func=self._find_send_button,
        )

        self._initialized = True
        return True

    # ========== Delegate to Core ==========

    def is_initialized(self) -> bool:
        """Check if browser is initialized."""
        return self._initialized and self.core.is_initialized()

    def close(self) -> None:
        """Close browser."""
        self.core.close()
        self.operations = None
        self._initialized = False

    def get_driver(self) -> Any | None:
        """Get browser driver instance."""
        return self.core.get_driver()

<<<<<<< HEAD
    # ========== Delegate to Utils ==========

    def save_cookies(self) -> bool:
        """Save cookies from current browser session."""
        driver = self.core.get_driver()
        if not driver:
            logger.error("No browser driver available")
            return False

        try:
            self.browser_utils.save_cookies(driver)
            return True
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            return False

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    # ========== Delegate to Operations ==========

    def navigate_to(self, url: str, wait_seconds: float = 2.0) -> bool:
        """Navigate to URL with optional wait."""
        if not self.operations:
            logger.error("Browser not initialized")
            return False
        return self.operations.navigate_to(url, wait_seconds)

    def ensure_thea_authenticated(self, thea_url: str | None = None, allow_manual: bool = True) -> bool:
        """Ensure authenticated to Thea Manager."""
        if not self.operations:
            logger.error("Browser not initialized")
            return False
        return self.operations.ensure_thea_authenticated(thea_url, allow_manual)

    def send_prompt_and_get_response_text(
        self, prompt: str, timeout: float = 90.0, poll_interval: float = 2.0
    ) -> str | None:
        """Send a prompt and return the assistant reply text."""
        if not self.operations:
            logger.error("Browser not initialized")
            return None
        return self.operations.send_prompt_and_get_response_text(prompt, timeout, poll_interval)

    def refresh(self) -> bool:
        """Refresh current page."""
        if not self.operations:
            return False
        return self.operations.refresh()

    def back(self) -> bool:
        """Navigate back."""
        if not self.operations:
            return False
        return self.operations.back()

    def forward(self) -> bool:
        """Navigate forward."""
        if not self.operations:
            return False
        return self.operations.forward()

    def get_current_url(self) -> str | None:
        """Get current URL."""
        if not self.operations:
            return None
        return self.operations.get_current_url()

    def get_title(self) -> str | None:
        """Get page title."""
        if not self.operations:
            return None
        return self.operations.get_title()

    def execute_script(self, script: str) -> Any:
        """Execute JavaScript in browser."""
        if not self.operations:
            return None
        return self.operations.execute_script(script)

    def find_element(self, by: str, value: str, timeout: float = 10.0) -> Any | None:
        """Find element with timeout."""
        if not self.operations:
            return None
        return self.operations.find_element(by, value, timeout)

    def find_elements(self, by: str, value: str) -> list:
        """Find multiple elements."""
        if not self.operations:
            return []
        return self.operations.find_elements(by, value)

    def take_screenshot(self, filepath: str) -> bool:
        """Take screenshot and save to file."""
        if not self.operations:
            return False
        return self.operations.take_screenshot(filepath)

    def get_page_source(self) -> str | None:
        """Get current page HTML source."""
        if not self.operations:
            return None
        return self.operations.get_page_source()

    # ========== Element Finding Methods (Still in service for now) ==========
    # These will be moved to separate modules in future refactoring

    def _find_prompt_textarea(self) -> Any | None:
        """Locate Thea/ChatGPT prompt textarea with auto-healing fallbacks."""
        driver = self.get_driver()
        if not driver:
            logger.debug("🔍 DEBUG: Driver not available")
            return None

        logger.debug("🔍 DEBUG: Starting textarea discovery...")

        # Phase 1: Try known working selectors (prioritized by success rate)
        logger.debug("🔍 DEBUG: Phase 1 - Trying known selectors...")
        known_selectors = self._get_prioritized_selectors()
        logger.debug(f"🔍 DEBUG: Trying {len(known_selectors)} known selectors")
        for i, selector in enumerate(known_selectors):
            try:
                logger.debug(f"🔍 DEBUG: Trying selector {i+1}: {selector}")
                el = driver.find_element("css selector", selector)
                if el and self._is_textarea_ready(el):
                    logger.debug(f"🔍 DEBUG: Selector {selector} worked!")
                    self._record_successful_selector(selector)
                    return el
                else:
                    logger.debug(
                        f"🔍 DEBUG: Selector {selector} found element but not ready")
            except Exception as e:
                logger.debug(f"🔍 DEBUG: Selector {selector} failed: {e}")
                continue

        # Phase 2: Dynamic discovery - analyze page for input-like elements
        logger.debug("🔍 DEBUG: Phase 1 failed, trying dynamic discovery...")
        discovered_element = self._discover_textarea_dynamically()
        if discovered_element:
            logger.debug("🔍 DEBUG: Dynamic discovery successful")
            return discovered_element
        else:
            logger.debug("🔍 DEBUG: Dynamic discovery also failed")

        # Phase 3: Broad fallback patterns
        fallback_selectors = [
            "textarea",
            "div[contenteditable='true']",
            "div[role='textbox']",
            "#prompt-textarea",
            "div[contenteditable='true'][aria-label*='message']",
            "div[contenteditable='true'][aria-label*='Send']",
            "div[contenteditable='true'][placeholder*='message']",
            "input[type='text']",
            "[data-testid*='input']",
            "[aria-label*='message']",
            "[placeholder*='message']",
            "[data-placeholder*='message']",
            "p[data-placeholder]",
        ]

        for selector in fallback_selectors:
            try:
                elements = driver.find_elements("css selector", selector)
                for el in elements:
                    if self._is_textarea_ready(el):
                        logger.info(f"Fallback selector worked: {selector}")
                        return el
            except Exception:
                continue

        logger.error("All textarea discovery methods failed")
        return None

    def _get_prioritized_selectors(self) -> list[str]:
        """Get selectors prioritized by historical success rate."""
        base_selectors = [
            # Updated selectors based on current ChatGPT UI analysis
            # Primary: visible contenteditable div
            "div[contenteditable='true'][id='prompt-textarea']",
            "#prompt-textarea",  # ID selector for the input area
            # ProseMirror contenteditable
            "div[contenteditable='true'].ProseMirror",
            "div.ProseMirror[contenteditable='true']",
            "textarea[data-testid='prompt-textarea']",
            "div[data-testid='prompt-textarea']",
            "div[contenteditable='true'][data-testid='prompt-textarea']",
            # Fallback patterns
            "textarea[aria-label*='Send a message']",
            "textarea[placeholder*='Send a message']",
            "textarea[aria-label*='Message']",
            "textarea[placeholder*='Message']",
            "textarea[aria-label*='Ask anything']",
            "textarea[placeholder*='Ask anything']",
            "[data-placeholder*='Ask anything']",
            "[data-placeholder*='Message']",
            "div[contenteditable='true'][role='textbox']",
            "div[contenteditable='true'][aria-label*='Send a message']",
            "div[contenteditable='true'][aria-label*='Message']",
            "form textarea",
            ".composer textarea",
            "#composer textarea",
        ]

        # Load from cache using utils
        cache_data = self.browser_utils.load_selector_cache()
        if cache_data:
            sorted_selectors = sorted(
                cache_data.items(),
                key=lambda x: x[1].get('success_rate', 0),
                reverse=True
            )
            prioritized = [sel for sel, _ in sorted_selectors]
            # Combine with base selectors, putting successful ones first
            return prioritized + [s for s in base_selectors if s not in prioritized]

        return base_selectors

    def _record_successful_selector(self, selector: str) -> None:
        """Record a successful selector for future prioritization."""
        self.browser_utils.record_successful_selector(selector)

    def _is_textarea_ready(self, element: Any) -> bool:
        """Check if an element is a ready-to-use textarea/input."""
        try:
            # Check if element is visible and enabled
            if not element.is_displayed() or not element.is_enabled():
                return False

            # Check if it's actually an input element
            tag_name = element.tag_name.lower()
            if tag_name not in ['textarea', 'input', 'div']:
                return False

            # For div elements, check if they're contenteditable
            if tag_name == 'div':
                contenteditable = element.get_attribute('contenteditable')
                if contenteditable != 'true':
                    return False

            # Check if element can accept input (not readonly)
            readonly = element.get_attribute('readonly')
            if readonly:
                return False

            # For contenteditable divs, do a simpler check based on attributes
            if tag_name == 'div':
                # Check if it has the right attributes for a ChatGPT input
                element_id = element.get_attribute('id')
                element_class = element.get_attribute('class') or ""
                if element_id == 'prompt-textarea' or 'ProseMirror' in element_class:
                    return True

            # For other elements, assume they're ready if they pass basic checks
            return True

        except Exception:
            return False

    def _discover_textarea_dynamically(self) -> Any | None:
        """Dynamically discover textarea-like elements by analyzing page structure."""
        driver = self.get_driver()
        if not driver:
            return None

        try:
            # Strategy 1: Look for forms with text inputs
            forms = driver.find_elements("css selector", "form")
            for form in forms:
                text_inputs = form.find_elements("css selector",
                                                 "textarea, input[type='text'], input:not([type]), div[contenteditable='true']")
                for input_el in text_inputs:
                    if self._is_textarea_ready(input_el):
                        return input_el

            # Strategy 2: Look for common chat interface patterns
            chat_patterns = [
                ".chat-input textarea",
                ".composer textarea",
                ".message-input textarea",
                "[data-testid*='composer'] textarea",
                "[data-testid*='input'] textarea",
                "[data-testid*='composer'] div[contenteditable='true']",
                "[data-testid='prompt-textarea']",
                "div[contenteditable='true'][data-testid='prompt-textarea']",
                ".conversation textarea",
                ".chat-form textarea"
            ]

            for pattern in chat_patterns:
                try:
                    elements = driver.find_elements("css selector", pattern)
                    for el in elements:
                        if self._is_textarea_ready(el):
                            return el
                except Exception:
                    continue

            # Strategy 3: Find all textareas and divs, filter by heuristics
            all_candidates = []
            all_candidates.extend(
                driver.find_elements("css selector", "textarea"))
            all_candidates.extend(driver.find_elements("css selector",
                                                       "div[contenteditable='true']"))
            all_candidates.extend(driver.find_elements("css selector",
                                                       "input[type='text']"))

            # Strategy 3b: Find placeholder nodes and climb to contenteditable parent
            try:
                placeholders = driver.find_elements(
                    "css selector", "p[data-placeholder], div[data-placeholder]")
                for node in placeholders:
                    try:
                        parent = node.find_element(
                            "xpath", "ancestor-or-self::*[@contenteditable='true'][1]")
                        if parent and self._is_textarea_ready(parent):
                            return parent
                    except Exception:
                        continue
            except Exception:
                pass

            # Score candidates by relevance
            scored_candidates = []
            for el in all_candidates:
                if not self._is_textarea_ready(el):
                    continue

                score = 0
                # Prefer elements near bottom of page (chat inputs are usually at bottom)
                location = el.location
                size = el.size
                if location['y'] > 500:  # Below fold
                    score += 10

                # Prefer larger elements (chat inputs are usually substantial)
                if size['height'] > 20:
                    score += 5

                # Prefer elements with chat-related attributes
                attrs = ['placeholder', 'aria-label', 'data-testid']
                for attr in attrs:
                    value = el.get_attribute(attr) or ""
                    if any(keyword in value.lower() for keyword in
                           ['message', 'chat', 'send', 'ask', 'prompt', 'input']):
                        score += 15
                        break

                scored_candidates.append((score, el))

            # Return highest scoring candidate
            if scored_candidates:
                scored_candidates.sort(key=lambda x: x[0], reverse=True)
                best_candidate = scored_candidates[0][1]
                logger.info(
                    f"Dynamic discovery found candidate with score {scored_candidates[0][0]}")
                return best_candidate

        except Exception as e:
            logger.debug(f"Dynamic discovery failed: {e}")

        return None

    def _find_send_button(self) -> Any | None:
        """Locate send button with auto-healing fallbacks."""
        driver = self.get_driver()
        if not driver:
            logger.debug(
                "🔍 DEBUG: Driver not available for send button search")
            return None

        logger.debug("🔍 DEBUG: Starting send button discovery...")

        # Phase 1: Try known working selectors
        logger.debug(
            "🔍 DEBUG: Phase 1 - Trying known send button selectors...")
        known_selectors = self._get_prioritized_send_selectors()
        logger.debug(
            f"🔍 DEBUG: Trying {len(known_selectors)} send button selectors")
        for i, selector in enumerate(known_selectors):
            try:
                logger.debug(
                    f"🔍 DEBUG: Trying send selector {i+1}: {selector}")
                el = driver.find_element("css selector", selector)
                if el and self._is_send_button_ready(el):
                    logger.debug(f"🔍 DEBUG: Send selector {selector} worked!")
                    self._record_successful_selector(f"send:{selector}")
                    return el
                else:
                    logger.debug(
                        f"🔍 DEBUG: Send selector {selector} found element but not ready")
            except Exception as e:
                logger.debug(f"🔍 DEBUG: Send selector {selector} failed: {e}")
                continue

        # Phase 2: Dynamic discovery around textarea
        textarea = self._find_prompt_textarea()
        if textarea:
            discovered_button = self._discover_send_button_near_textarea(
                textarea)
            if discovered_button:
                logger.info("Dynamic send button discovery successful")
                return discovered_button

        # Phase 3: Broad fallback patterns
        fallback_selectors = [
            "button[type='submit']",
            "button[data-testid*='send']",
            "button[aria-label*='send']",
            "input[type='submit']",
            "button[class*='send']",
            "svg[aria-label*='send']",
            "[role='button'][aria-label*='send']",
        ]

        for selector in fallback_selectors:
            try:
                elements = driver.find_elements("css selector", selector)
                for el in elements:
                    if self._is_send_button_ready(el):
                        logger.info(
                            f"Fallback send button selector worked: {selector}")
                        return el
            except Exception:
                continue

        logger.debug("Send button not found; will use ENTER fallback")
        return None

    def _get_prioritized_send_selectors(self) -> list[str]:
        """Get send button selectors prioritized by historical success."""
        base_selectors = [
            # Updated selectors based on current ChatGPT UI analysis
            "button[data-testid*='send-button']",
            "button[aria-label*='Send message']",
            "button[aria-label*='Send']",
            "button[data-testid*='composer-send-button']",
            "button[data-testid*='send']",
            ".composer-send-button",
            "[data-testid='send-button']",
            "button[type='submit'][aria-label*='Send']",
            "button svg",  # Look for buttons containing SVG icons
            "svg[aria-label*='Send']",
            "[role='button'][aria-label*='Send']",
            # Fallback to common patterns
            "#composer-submit-button",
            "button[data-testid*='submit']",
            "button[type='submit']",
            "form button[type='submit']",
            ".composer button:last-child",  # Last button in composer area
            "button[class*='send']",
            "button[aria-label*='Submit']",
            "button[aria-label*='Send prompt']",
            ".send-button",
            "[role='button'][data-testid*='send']",
        ]

        # Load from cache using utils
        cache_data = self.browser_utils.load_selector_cache()
        if cache_data:
            send_selectors = {k: v for k,
                              v in cache_data.items() if k.startswith('send:')}
            sorted_selectors = sorted(
                send_selectors.items(),
                key=lambda x: x[1].get('success_rate', 0),
                reverse=True
            )
            prioritized = [sel.replace('send:', '')
                           for sel, _ in sorted_selectors]
            # Combine with base selectors
            return prioritized + [s for s in base_selectors if s not in prioritized]

        return base_selectors

    def _is_send_button_ready(self, element: Any) -> bool:
        """Check if an element is a ready-to-use send button."""
        try:
            # Check if element is visible and enabled
            if not element.is_displayed() or not element.is_enabled():
                return False

            # Check tag name
            tag_name = element.tag_name.lower()
            if tag_name not in ['button', 'input', 'a', 'div', 'span', 'svg']:
                return False

            # Check for send-related attributes
            attrs_to_check = ['aria-label', 'data-testid',
                              'class', 'title', 'type', 'name']
            text_content = ""
            for attr in attrs_to_check:
                value = element.get_attribute(attr) or ""
                text_content += value + " "

            # Look for send-related keywords
            send_keywords = ['send', 'submit',
                             'enter', 'go', 'arrow', 'prompt']
            if any(keyword in text_content.lower() for keyword in send_keywords):
                return True

            # Check if element has click-like behavior (common for SVG icons)
            if tag_name in ['svg', 'path']:
                try:
                    parent = element.find_element("xpath", "..")
                    if parent:
                        parent_attrs = ['aria-label',
                                        'data-testid', 'class', 'title']
                        for attr in parent_attrs:
                            value = parent.get_attribute(attr) or ""
                            if any(keyword in value.lower() for keyword in send_keywords):
                                return True
                except Exception:
                    pass

            # Check for icon-based send buttons (common in modern UIs)
            try:
                # Look for SVG paths that might represent send arrows
                if tag_name == 'svg':
                    # Check if it contains path elements that look like arrows
                    paths = element.find_elements("tag name", "path")
                    if paths:
                        # Simple heuristic: if SVG has paths, it might be an icon
                        return True
            except Exception:
                pass

            # Position-based heuristic: send buttons are often near input areas
            try:
                location = element.location
                if location.get('x', 0) > 500:  # Far right side of screen
                    return True
            except Exception:
                pass

            return False

        except Exception:
            return False

    def _discover_send_button_near_textarea(self, textarea: Any) -> Any | None:
        """Find send button near the textarea element."""
        driver = self.get_driver()
        if not driver:
            return None

        try:
            # Look in the same form or parent container
            textarea_location = textarea.location
            textarea_size = textarea.size

            # Search within reasonable distance (right side, below, etc.)
            search_area = {
                'x': textarea_location['x'] - 50,
                'y': textarea_location['y'] - 20,
                'width': textarea_size['width'] + 200,
                'height': textarea_size['height'] + 100
            }

            # Find all clickable elements in the area
            candidates = driver.find_elements("css selector",
                                              "button, input[type='submit'], [role='button'], svg")

            for candidate in candidates:
                try:
                    loc = candidate.location
                    size = candidate.size

                    # Check if candidate is within search area
                    if (loc['x'] >= search_area['x'] and
                        loc['y'] >= search_area['y'] and
                        loc['x'] + size['width'] <= search_area['x'] + search_area['width'] and
                            loc['y'] + size['height'] <= search_area['y'] + search_area['height']):

                        if self._is_send_button_ready(candidate):
                            return candidate

                except Exception:
                    continue

        except Exception as e:
            logger.debug(f"Send button discovery near textarea failed: {e}")

        return None

    # ========== Context Manager Support ==========

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Factory function
def create_thea_browser_service(
    config: BrowserConfig | None = None,
    thea_config: TheaConfig | None = None
) -> TheaBrowserService:
    """Create Thea browser service instance."""
    return TheaBrowserService(config, thea_config)


__all__ = ["TheaBrowserService", "create_thea_browser_service"]
