#!/usr/bin/env python3
"""
Thea Browser Service - V2 Compliance
====================================

Unified browser service for Thea Manager automation.
Consolidates: browser_adapter, chrome_undetected, thea_login_handler, thea_manager_profile

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - Browser Consolidation
License: MIT
"""

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import undetected_chromedriver as uc

    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False

from .browser_models import BrowserConfig, TheaConfig

logger = logging.getLogger(__name__)


class TheaBrowserService:
    """Unified browser service for Thea Manager automation."""

    def __init__(self, config: BrowserConfig | None = None, thea_config: TheaConfig | None = None):
        """Initialize browser service."""
        self.config = config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()
        self.driver = None
        self.profile = None
        self._initialized = False

    def initialize(self, profile_name: str | None = None, user_data_dir: str | None = None) -> bool:
        """Initialize browser with optional profile."""
        if os.getenv("DISABLE_BROWSER") == "1":
            logger.warning("Browser disabled via DISABLE_BROWSER=1")
            return False

        if not UC_AVAILABLE:
            logger.error("undetected_chromedriver not available - install with `pip install undetected-chromedriver`")
            return False

        try:
            self.profile = {"profile_name": profile_name, "user_data_dir": user_data_dir}

            # Setup Chrome options (undetected only)
            options = uc.ChromeOptions()

            if self.config.headless:
                options.add_argument("--headless=new")

            if user_data_dir or (self.profile and self.profile.get("user_data_dir")):
                data_dir = user_data_dir or self.profile.get("user_data_dir")
                options.add_argument(f"--user-data-dir={data_dir}")

            if profile_name or (self.profile and self.profile.get("profile_name")):
                prof_name = profile_name or self.profile.get("profile_name")
                options.add_argument(f"--profile-directory={prof_name}")

            # Anti-detection options (minimal for uc compatibility)
            options.add_argument("--disable-blink-features=AutomationControlled")
            w, h = self.config.window_size
            options.add_argument(f"--window-size={w}x{h}")

            # Initialize driver
            self.driver = uc.Chrome(options=options, headless=self.config.headless)

            self.driver.implicitly_wait(self.config.implicit_wait)
            try:
                self.driver.set_page_load_timeout(self.config.page_load_timeout)
            except Exception:
                pass
            self._initialized = True

            logger.info("✅ Browser initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Browser initialization failed: {e}")
            return False

    def navigate_to(self, url: str, wait_seconds: float = 2.0) -> bool:
        """Navigate to URL with optional wait."""
        if not self._initialized or not self.driver:
            logger.error("Browser not initialized")
            return False

        try:
            self.driver.get(url)
            time.sleep(wait_seconds)
            logger.info(f"✅ Navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False

    def ensure_thea_authenticated(self, thea_url: str | None = None, allow_manual: bool = True) -> bool:
        """Ensure authenticated to Thea Manager."""
        if not self._initialized:
            logger.debug("🔍 DEBUG: Browser not initialized")
            return False

        try:
            target_url = thea_url or self.thea_config.conversation_url
            logger.debug(f"🔍 DEBUG: Target URL: {target_url}")

            # Navigate to Thea with longer wait for page load
            logger.debug("🔍 DEBUG: Navigating to Thea page...")
            if not self.navigate_to(target_url, wait_seconds=5.0):
                logger.debug("🔍 DEBUG: Navigation failed")
                return False
            logger.debug("🔍 DEBUG: Navigation successful")

            # Wait for page to stabilize
            logger.debug("🔍 DEBUG: Waiting 3 seconds for page stabilization...")
            time.sleep(3)
            logger.debug("🔍 DEBUG: Page stabilization wait complete")

            # Try loading cookies if available
            logger.debug("🔍 DEBUG: Loading cookies...")
            self._load_cookies(target_url)
            logger.debug("🔍 DEBUG: Refreshing page after cookie load...")
            self.driver.refresh()

            # Wait longer for page to reload after cookie loading
            logger.debug("🔍 DEBUG: Waiting 5 seconds for page reload...")
            time.sleep(5)
            logger.debug("🔍 DEBUG: Page reload wait complete")

            # Additional wait for dynamic content to load
            logger.debug("🔍 DEBUG: Waiting for page to be ready...")
            self._wait_for_page_ready()
            logger.debug("🔍 DEBUG: Page ready check complete")

            # Check if already authenticated
            logger.debug("🔍 DEBUG: Checking authentication status...")
            if self._is_thea_authenticated():
                logger.info("✅ Already authenticated to Thea (via cookies)")
                self._save_cookies()
                return True

            # Manual authentication if allowed
            if allow_manual:
                logger.info("⚠️  Manual authentication required")
                logger.info("Please log in to Thea Manager in the browser window...")
                logger.info("Waiting 45 seconds for manual login...")
                time.sleep(45)  # Allow more time for manual login

                # Check authentication again after manual login
                logger.debug("🔍 DEBUG: Checking authentication after manual login...")
                if self._is_thea_authenticated():
                    logger.info("✅ Authentication successful")
                    self._save_cookies()
                    return True

            logger.error("❌ Authentication failed")
            return False

        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False

    def _wait_for_page_ready(self, timeout: float = 10.0) -> bool:
        """Wait for page to be ready by checking for common elements."""
        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            # Wait for at least one of these elements to be present
            ready_selectors = [
                "textarea",
                "div[contenteditable='true']",
                "[data-testid]",
                ".composer",
                "form",
                "[role='textbox']",
                "button",
                "input"
            ]

            for selector in ready_selectors:
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(("css selector", selector))
                    )
                    logger.debug(f"Page ready indicator found: {selector}")
                    return True
                except:
                    continue

            # If no specific elements found, wait for document ready state
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.debug("Page ready state: complete")
            return True

        except Exception as e:
            logger.debug(f"Page ready wait failed: {e}")
            return False

    def _is_thea_authenticated(self) -> bool:
        """Check if authenticated to Thea Manager."""
        try:
            # Check for authenticated page elements
            current_url = self.driver.current_url
            return (
                ("chat.openai.com" in current_url or "chatgpt.com" in current_url)
                and "auth" not in current_url
            )
        except:
            return False

    # ========== Prompt & response helpers ==========
    def _find_prompt_textarea(self) -> Any | None:
        """Locate Thea/ChatGPT prompt textarea with auto-healing fallbacks."""
        if not self.driver:
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
                el = self.driver.find_element("css selector", selector)
                if el and self._is_textarea_ready(el):
                    logger.debug(f"🔍 DEBUG: Selector {selector} worked!")
                    self._record_successful_selector(selector)
                    return el
                else:
                    logger.debug(f"🔍 DEBUG: Selector {selector} found element but not ready")
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
                elements = self.driver.find_elements("css selector", selector)
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
            "div[contenteditable='true'][id='prompt-textarea']",  # Primary: visible contenteditable div
            "#prompt-textarea",  # ID selector for the input area
            "div[contenteditable='true'].ProseMirror",  # ProseMirror contenteditable
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

        # Try to load successful selectors from cache
        try:
            cache_file = Path(self.thea_config.cache_dir) / "selector_success.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    success_data = json.load(f)
                    # Sort by success rate
                    sorted_selectors = sorted(
                        success_data.items(),
                        key=lambda x: x[1].get('success_rate', 0),
                        reverse=True
                    )
                    prioritized = [sel for sel, _ in sorted_selectors]
                    # Combine with base selectors, putting successful ones first
                    return prioritized + [s for s in base_selectors if s not in prioritized]
        except Exception:
            logger.debug("Could not load selector cache")

        return base_selectors

    def _record_successful_selector(self, selector: str) -> None:
        """Record a successful selector for future prioritization."""
        try:
            cache_file = Path(self.thea_config.cache_dir) / "selector_success.json"
            cache_file.parent.mkdir(parents=True, exist_ok=True)

            success_data = {}
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    success_data = json.load(f)

            # Update success metrics
            if selector not in success_data:
                success_data[selector] = {'attempts': 0, 'successes': 0}

            success_data[selector]['attempts'] += 1
            success_data[selector]['successes'] += 1
            success_data[selector]['success_rate'] = (
                success_data[selector]['successes'] / success_data[selector]['attempts']
            )
            success_data[selector]['last_success'] = datetime.now().isoformat()

            with open(cache_file, 'w') as f:
                json.dump(success_data, f, indent=2)

        except Exception as e:
            logger.debug(f"Could not record selector success: {e}")

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
                element_class = element.get_attribute('class')
                if element_id == 'prompt-textarea' or 'ProseMirror' in element_class:
                    return True

            # For other elements, assume they're ready if they pass basic checks
            return True

        except Exception:
            return False

    def _discover_textarea_dynamically(self) -> Any | None:
        """Dynamically discover textarea-like elements by analyzing page structure."""
        try:
            # Strategy 1: Look for forms with text inputs
            forms = self.driver.find_elements("css selector", "form")
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
                    elements = self.driver.find_elements("css selector", pattern)
                    for el in elements:
                        if self._is_textarea_ready(el):
                            return el
                except Exception:
                    continue

            # Strategy 3: Find all textareas and divs, filter by heuristics
            all_candidates = []
            all_candidates.extend(self.driver.find_elements("css selector", "textarea"))
            all_candidates.extend(self.driver.find_elements("css selector",
                "div[contenteditable='true']"))
            all_candidates.extend(self.driver.find_elements("css selector",
                "input[type='text']"))

            # Strategy 3b: Find placeholder nodes and climb to contenteditable parent
            try:
                placeholders = self.driver.find_elements("css selector", "p[data-placeholder], div[data-placeholder]")
                for node in placeholders:
                    try:
                        parent = node.find_element("xpath", "ancestor-or-self::*[@contenteditable='true'][1]")
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
                logger.info(f"Dynamic discovery found candidate with score {scored_candidates[0][0]}")
                return best_candidate

        except Exception as e:
            logger.debug(f"Dynamic discovery failed: {e}")

        return None

    def _find_send_button(self) -> Any | None:
        """Locate send button with auto-healing fallbacks."""
        if not self.driver:
            logger.debug("🔍 DEBUG: Driver not available for send button search")
            return None

        logger.debug("🔍 DEBUG: Starting send button discovery...")

        # Phase 1: Try known working selectors
        logger.debug("🔍 DEBUG: Phase 1 - Trying known send button selectors...")
        known_selectors = self._get_prioritized_send_selectors()
        logger.debug(f"🔍 DEBUG: Trying {len(known_selectors)} send button selectors")
        for i, selector in enumerate(known_selectors):
            try:
                logger.debug(f"🔍 DEBUG: Trying send selector {i+1}: {selector}")
                el = self.driver.find_element("css selector", selector)
                if el and self._is_send_button_ready(el):
                    logger.debug(f"🔍 DEBUG: Send selector {selector} worked!")
                    self._record_successful_selector(f"send:{selector}")
                    return el
                else:
                    logger.debug(f"🔍 DEBUG: Send selector {selector} found element but not ready")
            except Exception as e:
                logger.debug(f"🔍 DEBUG: Send selector {selector} failed: {e}")
                continue

        # Phase 2: Dynamic discovery around textarea
        textarea = self._find_prompt_textarea()
        if textarea:
            discovered_button = self._discover_send_button_near_textarea(textarea)
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
                elements = self.driver.find_elements("css selector", selector)
                for el in elements:
                    if self._is_send_button_ready(el):
                        logger.info(f"Fallback send button selector worked: {selector}")
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

        # Try to load successful selectors from cache
        try:
            cache_file = Path(self.thea_config.cache_dir) / "selector_success.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    success_data = json.load(f)
                    # Filter for send button selectors and sort by success rate
                    send_selectors = {k: v for k, v in success_data.items() if k.startswith('send:')}
                    sorted_selectors = sorted(
                        send_selectors.items(),
                        key=lambda x: x[1].get('success_rate', 0),
                        reverse=True
                    )
                    prioritized = [sel.replace('send:', '') for sel, _ in sorted_selectors]
                    # Combine with base selectors
                    return prioritized + [s for s in base_selectors if s not in prioritized]
        except Exception:
            logger.debug("Could not load send button selector cache")

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
            attrs_to_check = ['aria-label', 'data-testid', 'class', 'title', 'type', 'name']
            text_content = ""
            for attr in attrs_to_check:
                value = element.get_attribute(attr) or ""
                text_content += value + " "

            # Look for send-related keywords
            send_keywords = ['send', 'submit', 'enter', 'go', 'arrow', 'prompt']
            if any(keyword in text_content.lower() for keyword in send_keywords):
                return True

            # Check if element has click-like behavior (common for SVG icons)
            if tag_name in ['svg', 'path']:
                try:
                    parent = element.find_element("xpath", "..")
                    if parent:
                        parent_attrs = ['aria-label', 'data-testid', 'class', 'title']
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
            candidates = self.driver.find_elements("css selector",
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

    def _set_textarea_value(self, textarea: Any, prompt: str) -> bool:
        """Inject prompt text via JS to avoid flaky send_keys."""
        try:
            self.driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
                textarea,
                prompt,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set prompt value: {e}")
            return False

    def _get_latest_assistant_message_text(self) -> str | None:
        """Return latest assistant message text."""
        try:
            script = """
                const nodes = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
                if (!nodes.length) return null;
                const last = nodes[nodes.length - 1];
                return last.innerText || last.textContent || null;
            """
            return self.driver.execute_script(script)
        except Exception:
            return None

    def send_prompt_and_get_response_text(
        self, prompt: str, timeout: float = 90.0, poll_interval: float = 2.0
    ) -> str | None:
        """Send a prompt and return the assistant reply text (headless-safe)."""
        if not self._initialized or not self.driver:
            logger.error("Browser not initialized")
            return None

        logger.debug("🔍 DEBUG: Starting prompt sending process")
        logger.debug(f"🔍 DEBUG: Prompt length: {len(prompt)} characters")

        # Ensure on conversation page
        logger.debug("🔍 DEBUG: Ensuring on conversation page...")
        self.navigate_to(self.thea_config.conversation_url, wait_seconds=5.0)

        # Wait for page to be fully ready before looking for elements
        logger.debug("🔍 DEBUG: Waiting for page to be fully ready...")
        if not self._wait_for_page_ready(timeout=15.0):
            logger.error("Page failed to load properly")
            return None
        logger.debug("🔍 DEBUG: Page is ready")

        # Additional wait for dynamic content
        logger.debug("🔍 DEBUG: Waiting 3 seconds for dynamic content...")
        time.sleep(3)
        logger.debug("🔍 DEBUG: Dynamic content wait complete")

        logger.debug("🔍 DEBUG: Looking for prompt textarea...")
        textarea = self._find_prompt_textarea()
        if not textarea:
            logger.error("Could not find textarea for prompt input")
            return None
        logger.debug("🔍 DEBUG: Textarea found")

        logger.debug("🔍 DEBUG: Setting textarea value...")
        if not self._set_textarea_value(textarea, prompt):
            logger.debug("🔍 DEBUG: Failed to set textarea value")
            return None
        logger.debug("🔍 DEBUG: Textarea value set successfully")

        # Send via button if present; fallback to ENTER or other methods
        logger.debug("🔍 DEBUG: Looking for send button...")
        send_btn = self._find_send_button()
        try:
            if send_btn:
                logger.info("Found send button, clicking it")
                send_btn.click()
                logger.debug("🔍 DEBUG: Send button clicked")
            else:
                logger.info("No send button found, trying ENTER key")
                from selenium.webdriver.common.keys import Keys

                # For contenteditable divs, try different approaches
                tag_name = textarea.tag_name.lower()
                logger.debug(f"🔍 DEBUG: Textarea tag name: {tag_name}")

                if tag_name == 'div':
                    logger.debug("🔍 DEBUG: Trying Ctrl+Enter for contenteditable div...")
                    # Try Ctrl+Enter for some interfaces
                    textarea.send_keys(Keys.CONTROL, Keys.ENTER)
                    time.sleep(0.5)
                    logger.debug("🔍 DEBUG: Trying plain Enter as fallback...")
                    # If that didn't work, try just ENTER
                    textarea.send_keys(Keys.ENTER)
                else:
                    logger.debug("🔍 DEBUG: Sending Enter key to textarea...")
                    # For textareas, just ENTER
                    textarea.send_keys(Keys.ENTER)

                # Also try clicking any nearby submit elements as backup
                logger.debug("🔍 DEBUG: Trying backup submit elements...")
                try:
                    submit_elements = self.driver.find_elements("css selector",
                        "button[type='submit'], input[type='submit'], [role='button']")
                    logger.debug(f"🔍 DEBUG: Found {len(submit_elements)} potential submit elements")
                    for elem in submit_elements:
                        if elem.is_displayed() and elem.is_enabled():
                            logger.debug("🔍 DEBUG: Clicking backup submit element")
                            elem.click()
                            break
                except Exception as e:
                    logger.debug(f"🔍 DEBUG: Backup submit elements failed: {e}")

            logger.debug("🔍 DEBUG: Prompt submission attempt complete")

        except Exception as e:
            logger.error(f"Failed to submit prompt: {e}")
            return None

        # Wait for response
        start = time.time()
        baseline = self._get_latest_assistant_message_text()
        while time.time() - start < timeout:
            time.sleep(poll_interval)
            latest = self._get_latest_assistant_message_text()
            if latest and latest != baseline:
                logger.info("✅ Received assistant response")
                return latest.strip()

        logger.error("❌ Timed out waiting for assistant response")
        return None

    def execute_script(self, script: str) -> Any:
        """Execute JavaScript in browser."""
        if not self._initialized:
            return None
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            logger.error(f"Script execution error: {e}")
            return None

    def find_element(self, by: str, value: str, timeout: float = 10.0) -> Any | None:
        """Find element with timeout."""
        if not self._initialized:
            return None

        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception:
            logger.debug(f"Element not found: {by}={value}")
            return None

    def find_elements(self, by: str, value: str) -> list:
        """Find multiple elements."""
        if not self._initialized:
            return []
        try:
            return self.driver.find_elements(by, value)
        except Exception:
            logger.debug(f"Elements not found: {by}={value}")
            return []

    def take_screenshot(self, filepath: str) -> bool:
        """Take screenshot and save to file."""
        if not self._initialized:
            return False
        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"✅ Screenshot saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Screenshot failed: {e}")
            return False

    def get_page_source(self) -> str | None:
        """Get current page HTML source."""
        if not self._initialized:
            return None
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Error getting page source: {e}")
            return None

    def refresh(self) -> bool:
        """Refresh current page."""
        if not self._initialized:
            return False
        try:
            self.driver.refresh()
            return True
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            return False

    def back(self) -> bool:
        """Navigate back."""
        if not self._initialized:
            return False
        try:
            self.driver.back()
            return True
        except Exception as e:
            logger.error(f"Back navigation failed: {e}")
            return False

    def forward(self) -> bool:
        """Navigate forward."""
        if not self._initialized:
            return False
        try:
            self.driver.forward()
            return True
        except Exception as e:
            logger.error(f"Forward navigation failed: {e}")
            return False

    def get_current_url(self) -> str | None:
        """Get current URL."""
        if not self._initialized:
            return None
        try:
            return self.driver.current_url
        except:
            return None

    def get_title(self) -> str | None:
        """Get page title."""
        if not self._initialized:
            return None
        try:
            return self.driver.title
        except:
            return None

    def close(self) -> None:
        """Close browser."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None
                self._initialized = False

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # ========== Cookie helpers ==========
    def _cookie_file(self) -> Path:
        return Path(self.thea_config.cookie_file)

    def _load_cookies(self, base_url: str) -> None:
        try:
            cookie_path = self._cookie_file()
            if not cookie_path.exists():
                return
            with open(cookie_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            self.driver.get(base_url)
            for cookie in cookies:
                # Selenium/uc requires domain stripped when adding after navigation
                cookie.pop("domain", None)
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    continue
            logger.info("✅ Cookies loaded")
        except Exception as e:
            logger.debug(f"Cookie load skipped: {e}")

    def _save_cookies(self) -> None:
        try:
            cookies = self.driver.get_cookies()
            cookie_path = self._cookie_file()
            cookie_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)
            logger.info("✅ Cookies saved")
        except Exception as e:
            logger.debug(f"Cookie save skipped: {e}")


# Factory function
def create_thea_browser_service(config: BrowserConfig | None = None) -> TheaBrowserService:
    """Create Thea browser service instance."""
    return TheaBrowserService(config)


__all__ = ["TheaBrowserService", "create_thea_browser_service"]
