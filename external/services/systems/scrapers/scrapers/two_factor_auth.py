"""
Two-Factor Authentication Handler
Handles TOTP generation and 2FA verification for ChatGPT login.
"""

import os
import time
import logging
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class TwoFactorAuth:
    """Handles two-factor authentication for ChatGPT login."""
    
    def __init__(self, totp_secret: Optional[str] = None, timeout: int = 30):
        """
        Initialize the 2FA handler.
        
        Args:
            totp_secret: TOTP secret for 2FA
            timeout: Timeout for web operations
        """
        self.totp_secret = totp_secret or os.getenv('CHATGPT_TOTP_SECRET')
        self.timeout = timeout
        
        if self.totp_secret:
            logger.info("TOTP secret configured: [HIDDEN]")
        else:
            logger.info("No TOTP secret configured - will require manual 2FA")
    
    def handle_2fa(self, driver) -> bool:
        """
        Handle 2FA verification if TOTP secret is configured.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if 2FA successful, False otherwise
        """
        if not self.totp_secret:
            logger.info("No TOTP secret configured - skipping 2FA")
            return True
        
        try:
            logger.info("Handling 2FA verification...")
            wait = WebDriverWait(driver, self.timeout)
            
            # Look for 2FA input field
            totp_selectors = [
                "//input[@id='totp']",
                "//input[@name='totp']",
                "//input[@type='text'][@placeholder*='code']",
                "//input[@data-testid='totp-input']",
                "//input[contains(@placeholder, 'code')]",
                "//input[contains(@placeholder, 'Code')]",
                "//input[contains(@placeholder, 'verification')]",
                "//input[contains(@placeholder, 'Verification')]",
            ]
            
            totp_field = None
            for sel in totp_selectors:
                try:
                    totp_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, sel))
                    )
                    if totp_field and totp_field.is_displayed() and totp_field.is_enabled():
                        logger.info(f"Found 2FA field with selector: {sel}")
                        break
                except TimeoutException:
                    continue
            
            if not totp_field:
                logger.warning("2FA field not found - may not be required")
                return True
            
            # Generate TOTP code
            totp_code = self._generate_totp_code()
            if not totp_code:
                logger.error("Failed to generate TOTP code")
                return False
            
            # Enter TOTP code
            totp_field.clear()
            totp_field.send_keys(totp_code)
            logger.info("Entered TOTP code")
            
            # Click verify/submit button
            try:
                verify_xpath = (
                    "//button[@type='submit' or contains(normalize-space(text()),'Verify') or contains(normalize-space(text()),'Continue') or contains(normalize-space(text()),'Submit')]"
                )
                verify_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, verify_xpath))
                )
                verify_button.click()
                logger.info("Clicked verify button")
            except TimeoutException:
                logger.error("Verify button not found")
                return False
            
            # Wait for verification to complete
            time.sleep(3)
            
            # Check if login was successful
            if self._is_login_successful(driver):
                logger.info("✅ 2FA verification successful")
                return True
            else:
                logger.error("❌ 2FA verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Error during 2FA: {e}")
            return False
    
    def _generate_totp_code(self) -> Optional[str]:
        """
        Generate TOTP code using the configured secret.
        
        Returns:
            TOTP code as string or None if generation failed
        """
        if not self.totp_secret:
            return None
        
        try:
            # Try to use pyotp if available
            try:
                import pyotp
                totp = pyotp.TOTP(self.totp_secret)
                code = totp.now()
                logger.info("Generated TOTP code using pyotp")
                return code
            except ImportError:
                logger.warning("pyotp not available - cannot generate TOTP code")
                return None
                
        except Exception as e:
            logger.error(f"Failed to generate TOTP code: {e}")
            return None
    
    def _is_login_successful(self, driver) -> bool:
        """
        Check if login was successful after 2FA.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if login appears successful, False otherwise
        """
        try:
            # Look for indicators of successful login
            success_indicators = [
                "//div[contains(text(), 'Welcome')]",
                "//div[contains(text(), 'Chat')]",
                "//div[contains(@class, 'chat')]",
                "//div[@data-testid='chat']",
                "//div[contains(@class, 'conversation')]",
            ]
            
            for indicator in success_indicators:
                try:
                    element = driver.find_element(By.XPATH, indicator)
                    if element.is_displayed():
                        return True
                except:
                    continue
            
            # Check if we're redirected to the main chat page
            current_url = driver.current_url
            if "chat.openai.com" in current_url and "login" not in current_url.lower():
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking login success: {e}")
            return False 