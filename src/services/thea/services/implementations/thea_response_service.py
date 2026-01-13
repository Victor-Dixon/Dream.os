#!/usr/bin/env python3
"""
Thea Response Service Implementation - Response Extraction Business Logic
=========================================================================

<!-- SSOT Domain: thea -->

Service implementation for Thea response extraction operations.
Implements multiple extraction strategies for reliable response capture.

V2 Compliance: Business logic service with dependency injection.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

import time
from typing import List, Optional

from ...domain.models import TheaResponse
from ...domain.enums import ResponseExtractionStrategy
from ...repositories.interfaces.i_browser_repository import IBrowserRepository
from ..interfaces.i_response_service import IResponseService


class TheaResponseService(IResponseService):
    """
    Thea response service implementation.

    Extracts responses from Thea using multiple strategies:
    - Assistant message extraction
    - Article content extraction
    - Markdown content extraction
    - Message ID based extraction
    - Manual fallback extraction
    """

    def __init__(self, browser_repository: IBrowserRepository):
        """
        Initialize Thea response service.

        Args:
            browser_repository: Repository for browser operations
        """
        self.browser_repo = browser_repository
        self.strategies = [
            AssistantMessageStrategy(),
            ArticleContentStrategy(),
            MarkdownContentStrategy(),
            MessageIdStrategy(),
            ManualFallbackStrategy()
        ]

    def extract_response(self, timeout_seconds: int = 120) -> Optional[TheaResponse]:
        """
        Extract a response from Thea using available strategies.

        Args:
            timeout_seconds: Maximum time to wait for response

        Returns:
            TheaResponse if extraction successful, None otherwise
        """
        print("🔍 Extracting response from Thea...")

        # First wait for response to appear
        if not self.wait_for_response_appearance(timeout_seconds):
            print("❌ No response appeared within timeout")
            return None

        # Try each extraction strategy
        for strategy in self.strategies:
            try:
                response = strategy.extract(self.browser_repo)
                if response and self.validate_response_content(response):
                    # Calculate confidence
                    response.confidence_score = self.calculate_response_confidence(response)
                    response.processing_time_seconds = time.time() - time.time()  # Placeholder

                    print(f"✅ Response extracted using {strategy.__class__.__name__}")
                    return response

            except Exception as e:
                print(f"⚠️ Strategy {strategy.__class__.__name__} failed: {e}")
                continue

        print("❌ All response extraction strategies failed")
        return None

    def wait_for_response_appearance(self, timeout_seconds: int = 120) -> bool:
        """
        Wait for a response to appear on the page.

        Args:
            timeout_seconds: Maximum time to wait

        Returns:
            True if response appears within timeout, False otherwise
        """
        print(f"⏳ Waiting up to {timeout_seconds}s for response...")

        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            # Check for response indicators
            if self._has_response_indicators():
                print("✅ Response indicators detected")
                return True

            time.sleep(2)  # Check every 2 seconds

        print("⏰ Response timeout - no response indicators found")
        return False

    def validate_response_content(self, response: TheaResponse) -> bool:
        """
        Validate that extracted response content is meaningful.

        Args:
            response: Response to validate

        Returns:
            True if response appears valid, False otherwise
        """
        if not response.content or not response.content.strip():
            return False

        content = response.content.strip()

        # Check minimum length
        if len(content) < 10:
            return False

        # Check for common invalid responses
        invalid_indicators = [
            "please wait",
            "loading",
            "connecting",
            "error",
            "sorry, something went wrong"
        ]

        content_lower = content.lower()
        if any(indicator in content_lower for indicator in invalid_indicators):
            return False

        return True

    def calculate_response_confidence(self, response: TheaResponse) -> float:
        """
        Calculate confidence score for response extraction.

        Args:
            response: Response to analyze

        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.5  # Base confidence

        content = response.content.strip()

        # Length factor
        if len(content) > 50:
            confidence += 0.2
        elif len(content) < 20:
            confidence -= 0.2

        # Structure factor (paragraphs, sentences)
        sentences = content.count('.') + content.count('!') + content.count('?')
        if sentences > 2:
            confidence += 0.2

        # Keyword factor (AI-like responses)
        ai_keywords = ['however', 'therefore', 'additionally', 'furthermore', 'based on']
        keyword_matches = sum(1 for keyword in ai_keywords if keyword in content.lower())
        confidence += min(keyword_matches * 0.1, 0.2)

        return min(max(confidence, 0.0), 1.0)

    def get_available_strategies(self) -> List[str]:
        """Get list of available response extraction strategies."""
        return [strategy.__class__.__name__ for strategy in self.strategies]

    def try_strategy(self, strategy_name: str, timeout_seconds: int = 30) -> Optional[TheaResponse]:
        """
        Try a specific extraction strategy.

        Args:
            strategy_name: Name of strategy to try
            timeout_seconds: Timeout for this strategy

        Returns:
            TheaResponse if strategy succeeds, None otherwise
        """
        strategy_map = {strategy.__class__.__name__: strategy for strategy in self.strategies}

        if strategy_name not in strategy_map:
            print(f"❌ Unknown strategy: {strategy_name}")
            return None

        strategy = strategy_map[strategy_name]

        try:
            response = strategy.extract(self.browser_repo)
            if response and self.validate_response_content(response):
                response.confidence_score = self.calculate_response_confidence(response)
                return response

        except Exception as e:
            print(f"❌ Strategy {strategy_name} failed: {e}")

        return None

    def get_response_metadata(self, response: TheaResponse) -> dict:
        """
        Extract additional metadata from a response.

        Args:
            response: Response to analyze

        Returns:
            Dictionary of metadata about the response
        """
        content = response.content

        return {
            "length": len(content),
            "sentences": content.count('.') + content.count('!') + content.count('?'),
            "words": len(content.split()),
            "has_code": '```' in content,
            "confidence": response.confidence_score,
            "extraction_timestamp": response.timestamp.isoformat()
        }

    def _has_response_indicators(self) -> bool:
        """Check for indicators that a response has appeared."""
        # Check for response containers
        response_selectors = [
            "[data-message-author-role='assistant']",
            "article",
            ".markdown",
            "[data-message-id]",
            ".agent-turn"
        ]

        for selector in response_selectors:
            elements = self.browser_repo.get_elements_text(selector)
            if elements and any(len(text.strip()) > 20 for text in elements):
                return True

        return False


# Response Extraction Strategies

class AssistantMessageStrategy:
    """Extract response from assistant message containers."""

    def extract(self, browser_repo: IBrowserRepository) -> Optional[TheaResponse]:
        """Extract using assistant message selector."""
        elements = browser_repo.get_elements_text("[data-message-author-role='assistant']")
        if elements:
            # Return the last (most recent) response
            content = elements[-1].strip()
            if content:
                return TheaResponse(content=content, message_id="unknown")


class ArticleContentStrategy:
    """Extract response from article elements."""

    def extract(self, browser_repo: IBrowserRepository) -> Optional[TheaResponse]:
        """Extract using article selector."""
        elements = browser_repo.get_elements_text("article")
        if elements:
            content = elements[-1].strip()
            if content:
                return TheaResponse(content=content, message_id="unknown")


class MarkdownContentStrategy:
    """Extract response from markdown containers."""

    def extract(self, browser_repo: IBrowserRepository) -> Optional[TheaResponse]:
        """Extract using markdown selector."""
        elements = browser_repo.get_elements_text(".markdown")
        if elements:
            content = elements[-1].strip()
            if content:
                return TheaResponse(content=content, message_id="unknown")


class MessageIdStrategy:
    """Extract response from message ID containers."""

    def extract(self, browser_repo: IBrowserRepository) -> Optional[TheaResponse]:
        """Extract using message ID selector."""
        elements = browser_repo.get_elements_text("[data-message-id]")
        if elements:
            # Filter for substantial content
            substantial_elements = [elem for elem in elements if len(elem.strip()) > 50]
            if substantial_elements:
                content = substantial_elements[-1].strip()
                return TheaResponse(content=content, message_id="unknown")


class ManualFallbackStrategy:
    """Manual fallback extraction using multiple heuristics."""

    def extract(self, browser_repo: IBrowserRepository) -> Optional[TheaResponse]:
        """Extract using manual fallback approach."""
        # Try various selectors and heuristics
        fallback_selectors = [
            ".agent-turn",
            "[role='article']",
            "[data-testid*='conversation']",
            "[class*='response']",
            "[class*='message']"
        ]

        for selector in fallback_selectors:
            elements = browser_repo.get_elements_text(selector)
            if elements:
                # Look for the most substantial content
                substantial_elements = [elem for elem in elements if len(elem.strip()) > 30]
                if substantial_elements:
                    content = substantial_elements[-1].strip()
                    return TheaResponse(content=content, message_id="unknown")

        return None