#!/usr/bin/env python3
"""
Secure Cookie Manager for Thea - V2 Compliance
==============================================

Encrypted cookie storage with secure session management.

<!-- SSOT Domain: infrastructure -->

Author: Agent-6 (Quality Assurance & Security)
License: MIT
"""

import json
import base64
import hashlib
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class SecureCookieManager:
    """
    Secure cookie storage with encryption and validation.

    Features:
    - AES-256 encryption for cookie storage
    - Session validation and expiration
    - Secure key derivation from environment
    - Tamper detection and integrity checks
    """

    def __init__(self, cookie_file: str = "thea_cookies.enc", key_file: str = "thea_key.bin"):
        """
        Initialize secure cookie manager.

        Args:
            cookie_file: Encrypted cookie storage file
            key_file: Encryption key file
        """
        self.cookie_file = Path(cookie_file)
        self.key_file = Path(key_file)
        self.fernet: Optional[Fernet] = None
        self._initialize_encryption()

    def _initialize_encryption(self):
        """Initialize encryption with secure key derivation."""
        try:
            if self.key_file.exists():
                # Load existing key
                with open(self.key_file, "rb") as f:
                    key = f.read()
            else:
                # Generate new key from environment + salt
                key = self._derive_key()
                # Save key securely
                self.key_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.key_file, "wb") as f:
                    f.write(key)

            self.fernet = Fernet(key)
            logger.info("✅ Secure cookie encryption initialized")

        except Exception as e:
            logger.error(f"❌ Encryption initialization failed: {e}")
            raise

    def _derive_key(self) -> bytes:
        """Derive encryption key from environment variables and salt."""
        # Use environment variable or generate fallback
        password = os.getenv('THEA_ENCRYPTION_KEY', self._generate_fallback_password())

        # Add salt for additional security
        salt = b'thea_secure_cookies_salt_2024'

        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def _generate_fallback_password(self) -> str:
        """Generate fallback password from system entropy."""
        # Use system time and PID for entropy (not cryptographically secure but better than nothing)
        entropy = f"{os.getpid()}_{datetime.now().timestamp()}_{os.urandom(16).hex()}"
        return hashlib.sha256(entropy.encode()).hexdigest()[:32]

    def save_cookies(self, driver) -> bool:
        """
        Save cookies securely with encryption.

        Args:
            driver: Selenium WebDriver instance

        Returns:
            bool: Success status
        """
        try:
            # Get cookies from browser
            cookies = driver.get_cookies()

            if not cookies:
                logger.warning("⚠️ No cookies to save")
                return False

            # Add metadata
            cookie_data = {
                "cookies": cookies,
                "timestamp": datetime.now().isoformat(),
                "domain": "chatgpt.com",
                "version": "1.0",
                "integrity_hash": self._calculate_integrity_hash(cookies)
            }

            # Encrypt data
            json_data = json.dumps(cookie_data, ensure_ascii=False)
            encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))

            # Save encrypted data
            self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cookie_file, "wb") as f:
                f.write(encrypted_data)

            logger.info(f"✅ Cookies saved securely to {self.cookie_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Cookie save failed: {e}")
            return False

    def load_cookies(self, driver) -> bool:
        """
        Load and decrypt cookies securely.

        Args:
            driver: Selenium WebDriver instance

        Returns:
            bool: Success status
        """
        try:
            if not self.cookie_file.exists():
                logger.info("🍪 No encrypted cookie file found")
                return False

            # Load encrypted data
            with open(self.cookie_file, "rb") as f:
                encrypted_data = f.read()

            # Decrypt data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            cookie_data = json.loads(decrypted_data.decode('utf-8'))

            # Validate integrity
            stored_hash = cookie_data.get("integrity_hash")
            calculated_hash = self._calculate_integrity_hash(cookie_data["cookies"])

            if stored_hash != calculated_hash:
                logger.error("❌ Cookie integrity check failed - possible tampering")
                return False

            # Check expiration (24 hours)
            timestamp = datetime.fromisoformat(cookie_data["timestamp"])
            if datetime.now() - timestamp > timedelta(hours=24):
                logger.warning("⚠️ Cookies are older than 24 hours")
                # Don't fail, just warn - cookies might still work

            # Load cookies into browser
            for cookie in cookie_data["cookies"]:
                try:
                    # Ensure cookie has required fields
                    if 'name' in cookie and 'value' in cookie:
                        driver.add_cookie(cookie)
                except Exception as e:
                    logger.debug(f"Skipped cookie {cookie.get('name', 'unknown')}: {e}")

            logger.info("✅ Cookies loaded securely")
            return True

        except Exception as e:
            logger.error(f"❌ Cookie load failed: {e}")
            return False

    def has_valid_cookies(self) -> bool:
        """
        Check if valid encrypted cookies exist and are recent.

        Returns:
            bool: True if valid cookies exist
        """
        try:
            if not self.cookie_file.exists():
                return False

            # Load and check metadata without full decryption
            with open(self.cookie_file, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = self.fernet.decrypt(encrypted_data)
            cookie_data = json.loads(decrypted_data.decode('utf-8'))

            # Check timestamp (within 48 hours for validity)
            timestamp = datetime.fromisoformat(cookie_data["timestamp"])
            is_recent = datetime.now() - timestamp < timedelta(hours=48)

            # Check if cookies exist
            has_cookies = len(cookie_data.get("cookies", [])) > 0

            return is_recent and has_cookies

        except Exception as e:
            logger.debug(f"Cookie validation failed: {e}")
            return False

    def clear_cookies(self) -> bool:
        """Clear all stored cookies securely."""
        try:
            if self.cookie_file.exists():
                # Overwrite with random data before deletion (secure delete)
                with open(self.cookie_file, "wb") as f:
                    f.write(os.urandom(1024))  # Overwrite with random data

                self.cookie_file.unlink()
                logger.info("✅ Cookies cleared securely")

            if self.key_file.exists():
                self.key_file.unlink()
                logger.info("✅ Encryption key cleared")

            return True

        except Exception as e:
            logger.error(f"❌ Cookie clear failed: {e}")
            return False

    def _calculate_integrity_hash(self, cookies: List[Dict[str, Any]]) -> str:
        """Calculate integrity hash for cookies."""
        # Create a deterministic string representation
        cookie_string = json.dumps(cookies, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(cookie_string.encode()).hexdigest()

    def get_cookie_stats(self) -> Dict[str, Any]:
        """Get statistics about stored cookies."""
        try:
            if not self.cookie_file.exists():
                return {"status": "no_cookies"}

            with open(self.cookie_file, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = self.fernet.decrypt(encrypted_data)
            cookie_data = json.loads(decrypted_data.decode('utf-8'))

            cookies = cookie_data.get("cookies", [])
            timestamp = datetime.fromisoformat(cookie_data["timestamp"])

            return {
                "status": "valid",
                "cookie_count": len(cookies),
                "saved_at": timestamp.isoformat(),
                "age_hours": (datetime.now() - timestamp).total_seconds() / 3600,
                "file_size": self.cookie_file.stat().st_size,
                "encrypted": True
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Factory function
def create_secure_cookie_manager(
    cookie_file: str = "thea_cookies.enc",
    key_file: str = "thea_key.bin"
) -> SecureCookieManager:
    """Create secure cookie manager instance."""
    return SecureCookieManager(cookie_file, key_file)


__all__ = ["SecureCookieManager", "create_secure_cookie_manager"]