#!/usr/bin/env python3
"""
Message Formatting Service
===========================

<!-- SSOT Domain: communication -->

Service for message formatting and template detection for PyAutoGUI message delivery.
Extracted from messaging_pyautogui.py as part of Phase 2A Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~150 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Import formatting functions from messaging_pyautogui.py
# These will be moved here once refactoring is complete
from .messaging_pyautogui import get_message_tag, format_c2a_message


class MessageFormattingService:
    """
    Service for message formatting and template detection.
    
    Handles:
    - Message content formatting
    - Template detection
    - Content extraction from templates
    """
    
    def __init__(self):
        """Initialize message formatting service."""
        logger.debug("MessageFormattingService initialized")
    
    def format_message_content(
        self,
        message,
        sender: str
    ) -> str:
        """
        Format message content for delivery.
        
        Detects if message already has a template header and uses it,
        otherwise formats with appropriate prefix.
        
        Args:
            message: UnifiedMessage object
            sender: Message sender identifier
            
        Returns:
            Formatted message content string
        """
        metadata = message.metadata if isinstance(message.metadata, dict) else {}
        message_category = metadata.get("message_category") or getattr(message, "category", None)
        
        # Log for debugging
        logger.info(
            f"🔍 Template detection for {message.recipient}: "
            f"content_length={len(message.content)}, category={message_category}, "
            f"content_preview={message.content[:100]}"
        )
        
        # Check if content has template header
        content_has_template_header = self._detect_template_header(message.content)
        
        # Check if metadata indicates templated message
        category_value = self._extract_category_value(message_category)
        
        is_templated_message = (
            category_value in ["d2a", "c2a", "a2a", "s2a"] or
            content_has_template_header
        )
        
        logger.info(
            f"🔍 Template check result: has_header={content_has_template_header}, "
            f"category={category_value}, is_templated={is_templated_message}"
        )
        
        if is_templated_message:
            # Message already has template applied - use content as-is
            content_to_use = message.content
            
            # If content has both prefix AND template header, extract template part
            if "[HEADER]" in content_to_use and not content_to_use.startswith("[HEADER]"):
                header_index = content_to_use.find("[HEADER]")
                if header_index > 0:
                    original_length = len(content_to_use)
                    content_to_use = content_to_use[header_index:]
                    logger.info(
                        f"🔧 Extracted template content: removed {header_index} chars prefix, "
                        f"template length: {len(content_to_use)} (was {original_length})"
                    )
            
            # Don't add any prefix - template is complete as-is
            msg_content = content_to_use
            logger.info(
                f"✅ Using pre-rendered template content "
                f"(category: {category_value}, has_header: {content_has_template_header}, "
                f"final_length: {len(msg_content)})"
            )
        else:
            # No template header - format with prefix
            logger.info(
                f"📝 No template detected - formatting with prefix "
                f"(category: {category_value}, has_header: {content_has_template_header})"
            )
            msg_content = format_c2a_message(
                recipient=message.recipient,
                content=message.content,
                priority=message.priority.value,
                sender=sender  # Pass sender for correct tagging
            )
        
        return msg_content
    
    def _detect_template_header(self, content: str) -> bool:
        """
        Detect if content has a template header.
        
        Args:
            content: Message content string
            
        Returns:
            True if template header detected
        """
        return (
            content.startswith("[HEADER]") or
            "[HEADER]" in content or
            "[HEADER] D2A" in content or
            "[HEADER] S2A" in content or
            "[HEADER] C2A" in content or
            "[HEADER] A2A" in content
        )
    
    def _extract_category_value(self, message_category) -> Optional[str]:
        """
        Extract category value from message category (handles enums and strings).
        
        Args:
            message_category: Category value (enum, string, or None)
            
        Returns:
            Lowercase category string or None
        """
        if not message_category:
            return None
        
        if isinstance(message_category, str):
            return message_category.lower()
        elif hasattr(message_category, 'value'):
            return message_category.value.lower()
        elif hasattr(message_category, 'name'):
            return message_category.name.lower()
        
        return None

