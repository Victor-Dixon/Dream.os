#!/usr/bin/env python3
"""
Unit Tests for Secure Cookie Repository
======================================

<!-- SSOT Domain: thea -->

Unit tests for the secure cookie repository implementation.
Demonstrates how the modular architecture enables proper testing.

V2 Compliance: Isolated unit tests with mocked dependencies.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.services.thea.domain.models import CookieData
from src.services.thea.repositories.implementations.secure_cookie_repository import SecureCookieRepository


class TestSecureCookieRepository:
    """Unit tests for secure cookie repository."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cookie_file = Path(self.temp_dir) / "test_cookies.enc"
        self.key_file = Path(self.temp_dir) / "test_key.bin"

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp files
        for file in [self.cookie_file, self.key_file]:
            if file.exists():
                file.unlink()
        Path(self.temp_dir).rmdir()

    def test_initialization_creates_key_file(self):
        """Test that initialization creates encryption key file."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        assert self.key_file.exists()
        assert self.key_file.stat().st_size > 0

    def test_save_and_load_cookies(self):
        """Test saving and loading cookies."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        # Create test cookie data
        cookies = {"session": "abc123", "user": "test"}
        cookie_data = CookieData(
            cookies=cookies,
            domain="chatgpt.com"
        )

        # Save cookies
        result = repo.save_cookies(cookie_data)
        assert result is True
        assert self.cookie_file.exists()

        # Load cookies
        loaded_data = repo.load_cookies()
        assert loaded_data is not None
        assert loaded_data.cookies == cookies
        assert loaded_data.domain == "chatgpt.com"
        assert loaded_data.is_encrypted is True

    def test_has_valid_cookies_with_valid_data(self):
        """Test has_valid_cookies returns True for valid cookies."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        cookies = {"session": "valid"}
        cookie_data = CookieData(cookies=cookies, domain="chatgpt.com")

        repo.save_cookies(cookie_data)
        assert repo.has_valid_cookies() is True

    def test_has_valid_cookies_with_no_file(self):
        """Test has_valid_cookies returns False when no cookie file exists."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        assert repo.has_valid_cookies() is False

    def test_delete_cookies(self):
        """Test deleting cookies."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        # Save cookies first
        cookies = {"session": "test"}
        cookie_data = CookieData(cookies=cookies, domain="chatgpt.com")
        repo.save_cookies(cookie_data)

        # Verify file exists
        assert self.cookie_file.exists()

        # Delete cookies
        result = repo.delete_cookies()
        assert result is True
        assert not self.cookie_file.exists()

    def test_load_invalid_encrypted_data(self):
        """Test loading invalid encrypted data."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        # Write invalid data to cookie file
        with open(self.cookie_file, 'wb') as f:
            f.write(b"invalid encrypted data")

        loaded_data = repo.load_cookies()
        assert loaded_data is None

    def test_get_storage_type(self):
        """Test getting storage type identifier."""
        repo = SecureCookieRepository(
            cookie_file=str(self.cookie_file),
            key_file=str(self.key_file)
        )

        assert repo.get_storage_type() == "secure_encrypted"


class TestPlainJsonCookieRepository:
    """Unit tests for plain JSON cookie repository."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cookie_file = Path(self.temp_dir) / "test_cookies.json"

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.cookie_file.exists():
            self.cookie_file.unlink()
        Path(self.temp_dir).rmdir()

    def test_save_and_load_plain_cookies(self):
        """Test saving and loading plain JSON cookies."""
        from ..repositories.implementations.secure_cookie_repository import PlainJsonCookieRepository

        repo = PlainJsonCookieRepository(
            cookie_file=str(self.cookie_file)
        )

        # Create test cookie data
        cookies = {"session": "plain123", "user": "test"}
        cookie_data = CookieData(
            cookies=cookies,
            domain="chatgpt.com"
        )

        # Save cookies
        result = repo.save_cookies(cookie_data)
        assert result is True
        assert self.cookie_file.exists()

        # Load cookies
        loaded_data = repo.load_cookies()
        assert loaded_data is not None
        assert loaded_data.cookies == cookies
        assert loaded_data.is_encrypted is False

    def test_get_storage_type_plain(self):
        """Test getting storage type for plain JSON."""
        from ..repositories.implementations.secure_cookie_repository import PlainJsonCookieRepository

        repo = PlainJsonCookieRepository(
            cookie_file=str(self.cookie_file)
        )

        assert repo.get_storage_type() == "plain_json"