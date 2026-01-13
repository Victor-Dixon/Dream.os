#!/usr/bin/env python3
"""
Secure Cookie Repository Implementation - Encrypted Cookie Storage
=================================================================

<!-- SSOT Domain: thea -->

Repository implementation for secure, encrypted cookie storage.
Uses cryptography library for encryption/decryption.

V2 Compliance: Repository pattern implementation.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from ...domain.models import CookieData
from ..interfaces.i_cookie_repository import ICookieRepository


class SecureCookieRepository(ICookieRepository):
    """
    Secure cookie repository with encryption.

    Uses Fernet encryption for cookie data storage.
    Keys are derived from a master key file.
    """

    def __init__(self,
                 cookie_file: str = "thea_cookies.enc",
                 key_file: str = "thea_key.bin",
                 domain: str = "chatgpt.com"):
        """
        Initialize secure cookie repository.

        Args:
            cookie_file: Path to encrypted cookie file
            key_file: Path to encryption key file
            domain: Cookie domain for validation
        """
        self.cookie_file = Path(cookie_file)
        self.key_file = Path(key_file)
        self.domain = domain
        self._cipher = None
        self._ensure_key_exists()

    def _ensure_key_exists(self) -> None:
        """Ensure encryption key exists, generate if needed."""
        if not self.key_file.exists():
            # Generate a new encryption key
            key = Fernet.generate_key()
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            print(f"🔐 Generated new encryption key: {self.key_file}")

        # Load the key and create cipher
        with open(self.key_file, 'rb') as f:
            key = f.read()
        self._cipher = Fernet(key)

    def save_cookies(self, cookies: CookieData) -> bool:
        """
        Save cookie data with encryption.

        Args:
            cookies: Cookie data to encrypt and save

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Prepare data for encryption
            data = {
                "cookies": cookies.cookies,
                "domain": cookies.domain,
                "created_at": cookies.created_at.isoformat(),
                "expires_at": cookies.expires_at.isoformat() if cookies.expires_at else None,
                "is_encrypted": True
            }

            # Convert to JSON and encrypt
            json_data = json.dumps(data, ensure_ascii=False)
            encrypted_data = self._cipher.encrypt(json_data.encode('utf-8'))

            # Save to file
            self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cookie_file, 'wb') as f:
                f.write(encrypted_data)

            print(f"💾 Saved encrypted cookies to: {self.cookie_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to save cookies: {e}")
            return False

    def load_cookies(self) -> Optional[CookieData]:
        """
        Load and decrypt cookie data.

        Returns:
            CookieData if found and valid, None otherwise
        """
        try:
            if not self.cookie_file.exists():
                print(f"🍪 No cookie file found: {self.cookie_file}")
                return None

            # Load and decrypt data
            with open(self.cookie_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = self._cipher.decrypt(encrypted_data)
            data = json.loads(decrypted_data.decode('utf-8'))

            # Validate data structure
            if not data.get("is_encrypted", False):
                print("❌ Cookie file is not encrypted")
                return None

            # Reconstruct CookieData object
            cookies = CookieData(
                cookies=data["cookies"],
                domain=data["domain"],
                created_at=datetime.fromisoformat(data["created_at"]),
                expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
                is_encrypted=True
            )

            # Validate cookies
            if not cookies.is_valid():
                print("❌ Loaded cookies are invalid or expired")
                return None

            print(f"🔓 Loaded valid encrypted cookies from: {self.cookie_file}")
            return cookies

        except (InvalidToken, json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"❌ Failed to load/decrypt cookies: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error loading cookies: {e}")
            return None

    def delete_cookies(self) -> bool:
        """
        Delete stored cookie data.

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if self.cookie_file.exists():
                self.cookie_file.unlink()
                print(f"🗑️ Deleted cookie file: {self.cookie_file}")
            else:
                print(f"🍪 No cookie file to delete: {self.cookie_file}")

            return True

        except Exception as e:
            print(f"❌ Failed to delete cookies: {e}")
            return False

    def has_valid_cookies(self) -> bool:
        """
        Check if valid, non-expired cookies exist.

        Returns:
            True if valid cookies exist, False otherwise
        """
        cookies = self.load_cookies()
        return cookies is not None and cookies.is_valid()

    def get_storage_type(self) -> str:
        """
        Get the type of storage mechanism used.

        Returns:
            String identifier for storage type
        """
        return "secure_encrypted"


class PlainJsonCookieRepository(ICookieRepository):
    """
    Plain JSON cookie repository (for development/testing).

    WARNING: This stores cookies in plain text - NOT SECURE for production!
    """

    def __init__(self,
                 cookie_file: str = "thea_cookies.json",
                 domain: str = "chatgpt.com"):
        """
        Initialize plain JSON cookie repository.

        Args:
            cookie_file: Path to plain JSON cookie file
            domain: Cookie domain for validation
        """
        self.cookie_file = Path(cookie_file)
        self.domain = domain

    def save_cookies(self, cookies: CookieData) -> bool:
        """Save cookies as plain JSON (INSECURE)."""
        try:
            data = {
                "cookies": cookies.cookies,
                "domain": cookies.domain,
                "created_at": cookies.created_at.isoformat(),
                "expires_at": cookies.expires_at.isoformat() if cookies.expires_at else None,
                "is_encrypted": False
            }

            self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"💾 Saved plain JSON cookies to: {self.cookie_file} (INSECURE)")
            return True

        except Exception as e:
            print(f"❌ Failed to save plain cookies: {e}")
            return False

    def load_cookies(self) -> Optional[CookieData]:
        """Load cookies from plain JSON."""
        try:
            if not self.cookie_file.exists():
                return None

            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data.get("is_encrypted", False):
                print("❌ Expected plain JSON but file is encrypted")
                return None

            cookies = CookieData(
                cookies=data["cookies"],
                domain=data["domain"],
                created_at=datetime.fromisoformat(data["created_at"]),
                expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
                is_encrypted=False
            )

            return cookies if cookies.is_valid() else None

        except Exception as e:
            print(f"❌ Failed to load plain cookies: {e}")
            return None

    def delete_cookies(self) -> bool:
        """Delete plain cookie file."""
        try:
            if self.cookie_file.exists():
                self.cookie_file.unlink()
                print(f"🗑️ Deleted plain cookie file: {self.cookie_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete plain cookies: {e}")
            return False

    def has_valid_cookies(self) -> bool:
        """Check if valid cookies exist."""
        cookies = self.load_cookies()
        return cookies is not None and cookies.is_valid()

    def get_storage_type(self) -> str:
        """Get storage type identifier."""
        return "plain_json"