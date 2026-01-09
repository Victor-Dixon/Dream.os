"""Simple scroll manager utility."""

import time
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from .scroll_strategies import ScrollStrategy

logger = logging.getLogger(__name__)

class ScrollManager:
    """Manage scrolling behavior based on strategy."""

    def __init__(self, strategy: ScrollStrategy = ScrollStrategy.TARGETED, delay: float = 1.0):
        self.strategy = strategy
        self.delay = delay

    def scroll(self, driver: WebDriver, container) -> None:
        """Perform a basic scroll action."""
        if not driver or not container:
            logger.warning("No driver or container provided for scrolling")
            return
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
        time.sleep(self.delay)
