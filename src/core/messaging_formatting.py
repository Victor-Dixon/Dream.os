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

def get_message_tag(sender: str, recipient: str) -> str:
    """
    Determine correct message tag based on sender and recipient.
    
    Args:
        sender: Message sender (GENERAL, DISCORD, CAPTAIN, Agent-X, SYSTEM)
        recipient: Message recipient (Agent-X, ALL, CAPTAIN)
    
    Returns:
        Correct message tag ([D2A], [G2A], [C2A], [A2A], [A2C], [S2A])
    """
    sender_upper = sender.upper()
    recipient_upper = recipient.upper() if recipient else ""
    
    # General broadcasts (STRATEGIC - highest priority!)
    if 'GENERAL' in sender_upper:
        return '[G2A]'  # General-to-Agent
    
    # Discord/Commander broadcasts
    if sender_upper in ['DISCORD', 'COMMANDER', 'DISCORD-CONTROLLER']:
        return '[D2A]'  # Discord-to-Agent
    
    # System automated messages
    if sender_upper == 'SYSTEM':
        return '[S2A]'  # System-to-Agent
    
    # Captain to Agent
    if sender_upper in ['CAPTAIN', 'AGENT-4']:
        if 'ALL' in recipient_upper or 'BROADCAST' in recipient_upper:
            return '[C2A-ALL]'  # Captain broadcast
        return '[C2A]'  # Captain-to-Agent
    
    # Agent to Captain
    if recipient_upper in ['CAPTAIN', 'AGENT-4']:
        return '[A2C]'  # Agent-to-Captain
    
    # Agent to Agent
    if sender.startswith('Agent-') and recipient.startswith('Agent-'):
        return '[A2A]'  # Agent-to-Agent
    
    # Fallback to C2A for safety
    return '[C2A]'


def format_c2a_message(recipient: str, content: str, priority: str | None = None, sender: str = "CAPTAIN") -> str:
    """
    Format message with correct tag based on sender.

    Per STANDARDS.md: Compact messaging with essential fields only.
    NOW SUPPORTS: [D2A], [G2A], [S2A], [C2A], [A2A], [A2C]

    Args:
        recipient: Target agent ID
        content: Message content
        priority: Optional priority level (defaults to 'normal')
        sender: Message sender (determines tag)

    Returns:
        Formatted message with correct tag
    """
    priority = priority or "normal"
    
    # Get correct message tag based on sender
    tag = get_message_tag(sender, recipient)

    # Add "URGENT MESSAGE" prefix for urgent priority
    urgent_prefix = ""
    if priority == "urgent":
        urgent_prefix = "🚨 URGENT MESSAGE 🚨\n\n"

    # Lean format: [Tag] Recipient (no priority in header for urgent)
    header = f"{tag} {recipient}"

    return f"{urgent_prefix}{header}\n\n{content}"


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
    
    def normalize_message(self, message) -> any:
        """
        Normalize message format to UnifiedMessage object.
        
        Handles both dictionary and UnifiedMessage object formats.
        
        Args:
            message: Message in dict or UnifiedMessage format
            
        Returns:
            Normalized UnifiedMessage object
        """
        if not isinstance(message, dict):
            return message
            
        from .messaging_models_core import (
            UnifiedMessage, 
            UnifiedMessageType, 
            UnifiedMessagePriority, 
            UnifiedMessageTag,
            MessageCategory
        )
        
        # Extract recipient from dict (CRITICAL for routing)
        recipient = message.get('recipient') or message.get('to')
        if not recipient:
            logger.error(f"❌ Message dict missing recipient: {message.keys()}")
            return None
        
        # Convert message_type string to enum if needed
        message_type_str = message.get('message_type', 'text')
        if isinstance(message_type_str, str):
            try:
                message_type = UnifiedMessageType(message_type_str)
            except (ValueError, AttributeError):
                message_type = UnifiedMessageType.TEXT
        else:
            message_type = message_type_str
        
        # Convert priority string to enum if needed
        priority_str = message.get('priority', 'regular')
        if isinstance(priority_str, str):
            try:
                priority = UnifiedMessagePriority(priority_str)
            except (ValueError, AttributeError):
                priority = UnifiedMessagePriority.REGULAR
        else:
            priority = priority_str
        
        # Convert tags list to enums if needed
        tags_list = message.get('tags', [])
        tags = []
        for tag in tags_list:
            if isinstance(tag, str):
                try:
                    tags.append(UnifiedMessageTag(tag))
                except (ValueError, AttributeError):
                    pass
            else:
                tags.append(tag)
        
        # Extract category from metadata if present
        category = None
        metadata_dict = message.get('metadata', {})
        if isinstance(metadata_dict, dict):
            category_str = metadata_dict.get('message_category')
            if category_str:
                try:
                    category = MessageCategory(category_str.lower())
                except (ValueError, AttributeError):
                    pass
        
        # Create UnifiedMessage object from dict
        return UnifiedMessage(
            content=message.get('content', ''),
            sender=message.get('sender', 'CAPTAIN'),
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags if tags else [UnifiedMessageTag.SYSTEM],
            metadata=metadata_dict,
            category=category if category else MessageCategory.S2A
        )

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

