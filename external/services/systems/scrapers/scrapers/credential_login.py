"""
Credential Login Handler
Handles username/password login for ChatGPT.
"""

import os
import time
import logging
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .two_factor_auth import TwoFactorAuth

logger = logging.getLogger(__name__)

class CredentialLogin:
    """Handles username/password login for ChatGPT."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, 
                 totp_secret: Optional[str] = None, timeout: int = 30):
        """
        Initialize the credential login handler.
        
        Args:
            username: ChatGPT username/email
            password: ChatGPT password
            totp_secret: TOTP secret for 2FA
            timeout: Timeout for web operations
        """
        self.username = username or os.getenv('CHATGPT_USERNAME')
        self.password = password or os.getenv('CHATGPT_PASSWORD')
        self.timeout = int(os.getenv('CHATGPT_TIMEOUT', timeout))
        self.two_factor_auth = TwoFactorAuth(totp_secret, timeout)
        
        # Log credential status
        if self.username:
            masked_username = f"{self.username[:3]}***{self.username[-3:] if len(self.username) > 6 else ''}"
            logger.info(f"Username configured: {masked_username}")
        else:
            logger.info("No username configured - will require manual login")
        
        if self.password:
            logger.info("Password configured: [HIDDEN]")
        else:
            logger.info("No password configured - will require manual login")
    
    def login_with_credentials(self, driver) -> bool:
        """
        Attempt to login with stored credentials.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if login successful, False otherwise
        """
        if not driver:
            logger.error("No driver provided for login")
            return False
        
        if not self.username or not self.password:
            logger.warning("Username or password not configured")
            return False
        
        try:
            logger.info("Attempting automated login...")
            
            # Wait for login form to be present
            wait = WebDriverWait(driver, self.timeout)
            
            # Look for login button and click it (new UI sometimes wraps text in <div>)
            try:
                login_btn_xpath = (
                    "//button[.//div[contains(normalize-space(text()),'Log in')] or contains(normalize-space(text()),'Log in') or contains(normalize-space(text()),'Sign in')]"
                )
                login_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, login_btn_xpath))
                )
                login_button.click()
                logger.info("Clicked login button")
                time.sleep(2)
            except TimeoutException:
                logger.info("Login button not found, may already be on login page")
            
            # Find and fill username field
            username_field = self._find_username_field(driver, wait)
            if not username_field:
                return False
            
            username_field.clear()
            username_field.send_keys(self.username)
            logger.info("Entered username/email")
            
            # Find and fill password field
            password_field = self._find_password_field(driver, wait)
            if not password_field:
                return False
            
            password_field.clear()
            password_field.send_keys(self.password)
            logger.info("Entered password")
            
            # Click continue/submit button
            if not self._click_submit_button(driver, wait):
                return False
            
            # Handle 2FA if configured
            if self.two_factor_auth.totp_secret:
                return self.two_factor_auth.handle_2fa(driver)
            
            # Wait for successful login
            time.sleep(3)
            
            # Check if login was successful
            if self._is_login_successful(driver):
                logger.info("✅ Login successful")
                return True
            else:
                logger.error("❌ Login failed")
                return False
                
        except Exception as e:
            logger.error(f"Error during credential login: {e}")
            return False
    
    def _find_username_field(self, driver, wait):
        """Find the username/email input field."""
        username_selectors = [
            "//input[@id='username']",
            "//input[@id='email']",
            "//input[@name='username']",
            "//input[@name='email']",
            "//input[@type='email']",
            "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'email')]",
            "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'username')]",
            "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'user')]",
            "//input[@data-testid='email-input']",
            "//input[@data-testid='username-input']",
            "//input[contains(@class, 'email')]",
            "//input[contains(@class, 'username')]",
            "//input[contains(@class, 'user')]",
        ]
        
        username_field = None
        for sel in username_selectors:
            try:
                username_field = wait.until(
                    EC.presence_of_element_located((By.XPATH, sel))
                )
                if username_field and username_field.is_displayed() and username_field.is_enabled():
                    logger.info(f"Found username field with selector: {sel}")
                    break
            except TimeoutException:
                continue

        if not username_field:
            logger.error("Username/email field not found via any selector")
            # Try to find any input field that might be for email/username
            try:
                all_inputs = driver.find_elements("tag name", "input")
                for inp in all_inputs:
                    if inp.is_displayed() and inp.is_enabled():
                        inp_type = inp.get_attribute("type") or ""
                        inp_name = inp.get_attribute("name") or ""
                        inp_id = inp.get_attribute("id") or ""
                        inp_placeholder = inp.get_attribute("placeholder") or ""
                        
                        # Check if this looks like an email/username field
                        if (inp_type.lower() in ['email', 'text'] or 
                            'email' in inp_name.lower() or 'user' in inp_name.lower() or
                            'email' in inp_id.lower() or 'user' in inp_id.lower() or
                            'email' in inp_placeholder.lower() or 'user' in inp_placeholder.lower()):
                            username_field = inp
                            logger.info(f"Found username field by inspection: type={inp_type}, name={inp_name}, id={inp_id}, placeholder={inp_placeholder}")
                            break
            except Exception as e:
                logger.error(f"Error during fallback username field search: {e}")
            
            if not username_field:
                return None
        
        return username_field
    
    def _find_password_field(self, driver, wait):
        """Find the password input field."""
        password_selectors = [
            "//input[@id='password']",
            "//input[@name='password']",
            "//input[@type='password']",
            "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'password')]",
        ]
        
        password_field = None
        for sel in password_selectors:
            try:
                password_field = wait.until(
                    EC.presence_of_element_located((By.XPATH, sel))
                )
                if password_field:
                    break
            except TimeoutException:
                continue

        if not password_field:
            logger.error("Password field not found via any selector")
            return None
        
        return password_field
    
    def _click_submit_button(self, driver, wait):
        """Click the submit/continue button."""
        try:
            submit_xpath = (
                "//button[@type='submit' or contains(normalize-space(text()),'Continue') or contains(normalize-space(text()),'Verify') or contains(normalize-space(text()),'Next')]"
            )
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, submit_xpath))
            )
            submit_button.click()
            logger.info("Clicked submit/continue button")
            return True
        except TimeoutException:
            logger.error("Submit/Continue button not found")
            return False
    
    def _is_login_successful(self, driver) -> bool:
        """Check if login was successful."""
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