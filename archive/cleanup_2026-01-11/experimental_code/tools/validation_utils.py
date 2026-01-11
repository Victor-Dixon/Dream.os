#!/usr/bin/env python3
"""
Validation Utilities
Shared utilities for HTTP validation, response checking, and common validation patterns
"""

import requests
import logging
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin
import time

logger = logging.getLogger(__name__)

class HTTPValidator:
    """HTTP validation utilities"""

    def __init__(self, base_url: str = "", timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def check_url(self, url: str, expected_status: int = 200) -> Dict[str, Any]:
        """
        Check if URL returns expected status code

        Args:
            url: URL to check
            expected_status: Expected HTTP status code

        Returns:
            Dict with validation results
        """
        try:
            full_url = urljoin(self.base_url + '/', url.lstrip('/'))
            response = self.session.get(full_url, timeout=self.timeout)

            return {
                "url": full_url,
                "status_code": response.status_code,
                "success": response.status_code == expected_status,
                "content_length": len(response.text),
                "response_time": response.elapsed.total_seconds(),
                "error": None
            }
        except Exception as e:
            return {
                "url": url,
                "status_code": None,
                "success": False,
                "content_length": 0,
                "response_time": None,
                "error": str(e)
            }

    def validate_pages(self, pages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Validate multiple pages

        Args:
            pages: List of dicts with 'title' and 'slug' keys

        Returns:
            List of validation results
        """
        results = []
        for page in pages:
            result = self.check_url(page['slug'])
            result['title'] = page['title']
            results.append(result)
            logger.info(f"Validated {page['title']}: {'✅' if result['success'] else '❌'}")

        return results

class ContentValidator:
    """Content validation utilities"""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self.validator = HTTPValidator(base_url)

    def check_content_presence(self, url: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Check if keywords are present in page content

        Args:
            url: URL to check
            keywords: List of keywords to search for

        Returns:
            Dict with validation results
        """
        result = self.validator.check_url(url)
        if not result['success']:
            result['keyword_matches'] = {}
            return result

        try:
            response = requests.get(result['url'], timeout=10)
            content = response.text.lower()

            keyword_matches = {}
            for keyword in keywords:
                keyword_matches[keyword] = keyword.lower() in content

            result['keyword_matches'] = keyword_matches
            result['all_keywords_found'] = all(keyword_matches.values())

        except Exception as e:
            result['keyword_matches'] = {}
            result['all_keywords_found'] = False
            result['error'] = str(e)

        return result

class WordPressValidator:
    """WordPress-specific validation utilities"""

    def __init__(self, site_url: str = "https://tradingrobotplug.com"):
        self.site_url = site_url.rstrip('/')
        self.http_validator = HTTPValidator(site_url)

    def validate_theme_integrity(self) -> Dict[str, Any]:
        """Validate WordPress theme integrity"""
        # Check if main page loads
        result = self.http_validator.check_url('/')
        if not result['success']:
            return {"theme_integrity": False, "error": "Main page failed to load"}

        # Check for WordPress-specific elements
        try:
            response = requests.get(self.site_url, timeout=10)
            content = response.text

            checks = {
                "has_wp_head": "wp_head" in content,
                "has_wp_footer": "wp_footer" in content,
                "has_body_class": "body_class" in content,
                "has_theme_stylesheet": "style.css" in content
            }

            return {
                "theme_integrity": all(checks.values()),
                "checks": checks,
                "content_length": len(content)
            }
        except Exception as e:
            return {"theme_integrity": False, "error": str(e)}

    def validate_menu_structure(self, menu_items: List[str]) -> Dict[str, Any]:
        """Validate menu contains expected items"""
        result = self.http_validator.check_url('/')
        if not result['success']:
            return {"menu_valid": False, "error": "Page failed to load"}

        try:
            response = requests.get(result['url'], timeout=10)
            content = response.text.lower()

            found_items = []
            missing_items = []

            for item in menu_items:
                if item.lower() in content:
                    found_items.append(item)
                else:
                    missing_items.append(item)

            return {
                "menu_valid": len(missing_items) == 0,
                "found_items": found_items,
                "missing_items": missing_items,
                "total_items": len(menu_items)
            }
        except Exception as e:
            return {"menu_valid": False, "error": str(e)}

class FontValidator:
    """Font loading and rendering validation"""

    def __init__(self, base_url: str = "https://weareswarm.online"):
        self.base_url = base_url.rstrip('/')
        self.http_validator = HTTPValidator(base_url)

    def validate_font_loading(self) -> Dict[str, Any]:
        """Validate Google Fonts loading"""
        result = self.http_validator.check_url('/')
        if not result['success']:
            return {"fonts_loaded": False, "error": "Page failed to load"}

        try:
            response = requests.get(result['url'], timeout=10)
            content = response.text

            # Check for Google Fonts links
            google_fonts = 'fonts.googleapis.com' in content
            preconnect = 'fonts.gstatic.com' in content

            # Check for common font families
            font_families = ['Inter', 'Roboto', 'Open Sans', 'Lato']
            found_fonts = [font for font in font_families if font in content]

            return {
                "fonts_loaded": google_fonts,
                "preconnect_configured": preconnect,
                "font_families_found": found_fonts,
                "multiple_fonts": len(found_fonts) > 0
            }
        except Exception as e:
            return {"fonts_loaded": False, "error": str(e)}

    def validate_character_rendering(self, test_chars: str = "sS") -> Dict[str, Any]:
        """Validate character rendering"""
        result = self.http_validator.check_url('/')
        if not result['success']:
            return {"characters_render": False, "error": "Page failed to load"}

        try:
            response = requests.get(result['url'], timeout=10)
            content = response.text

            # Count test characters
            char_counts = {}
            for char in test_chars:
                char_counts[char] = content.count(char)

            total_chars = sum(char_counts.values())

            return {
                "characters_render": total_chars > 0,
                "character_counts": char_counts,
                "total_test_chars": total_chars,
                "content_length": len(content)
            }
        except Exception as e:
            return {"characters_render": False, "error": str(e)}

# Utility functions for common validation patterns
def validate_service_response(url: str, expected_status: int = 200, timeout: int = 10) -> bool:
    """Quick validation of service response"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == expected_status
    except:
        return False

def validate_content_keywords(url: str, keywords: List[str], timeout: int = 10) -> Dict[str, bool]:
    """Quick validation of content keywords"""
    try:
        response = requests.get(url, timeout=timeout)
        content = response.text.lower()

        results = {}
        for keyword in keywords:
            results[keyword] = keyword.lower() in content

        return results
    except:
        return {keyword: False for keyword in keywords}