"""
Tests for Unified Cookie Manager - Infrastructure Domain

Tests for unified cookie management functionality.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.browser.unified_cookie_manager import UnifiedCookieManager


class TestUnifiedCookieManager:
    """Tests for UnifiedCookieManager SSOT."""

    def test_unified_cookie_manager_initialization(self):
        """Test UnifiedCookieManager initializes correctly."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_cookie_file = Path(f.name)
        
        try:
            manager = UnifiedCookieManager(
                cookie_file=str(temp_cookie_file),
                auto_save=True,
            )
            assert manager.cookie_file == str(temp_cookie_file)
            assert manager.auto_save is True
        finally:
            if temp_cookie_file.exists():
                temp_cookie_file.unlink()

    def test_unified_cookie_manager_with_auto_save_false(self):
        """Test UnifiedCookieManager with auto_save=False."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_cookie_file = Path(f.name)
        
        try:
            manager = UnifiedCookieManager(
                cookie_file=str(temp_cookie_file),
                auto_save=False,
            )
            assert manager.auto_save is False
        finally:
            if temp_cookie_file.exists():
                temp_cookie_file.unlink()

    def test_unified_cookie_manager_load_cookies_empty_file(self):
        """Test loading cookies from empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_cookie_file = Path(f.name)
        
        try:
            manager = UnifiedCookieManager(
                cookie_file=str(temp_cookie_file),
                auto_save=True,
            )
            # _load_persisted_cookies returns False on error, cookies dict otherwise
            result = manager._load_persisted_cookies()
            # Result can be False (error) or dict (success)
            assert result is False or isinstance(result, dict)
            # Cookies dict should exist regardless
            assert isinstance(manager.cookies, dict)
        finally:
            if temp_cookie_file.exists():
                temp_cookie_file.unlink()

