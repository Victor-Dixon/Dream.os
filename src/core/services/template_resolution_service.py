#!/usr/bin/env python3
"""
Template Resolution Service - Service Layer Architecture
=====================================================

<!-- SSOT Domain: integration -->

Service for resolving and formatting message templates.

Author: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-16
Refactored from messaging_core.py for V2 compliance (file size limits)
"""

import logging
from pathlib import Path
from typing import List, Dict, Any

# Use relative imports for V2 compliance
from ..messaging_models import UnifiedMessage
from ..messaging_template_texts import MESSAGE_TEMPLATES

logger = logging.getLogger(__name__)


class TemplateResolutionService:
    """Service for resolving and formatting message templates."""

    def __init__(self):
        self.templates = MESSAGE_TEMPLATES

    def resolve_template(self, template_key: str, **kwargs) -> str:
        """Resolve template with provided variables."""
        if template_key not in self.templates:
            logger.warning(f"Template {template_key} not found")
            return kwargs.get('content', '')

        template = self.templates[template_key]

        try:
            # Handle different template formats
            if isinstance(template, str):
                return template.format(**kwargs)
            elif isinstance(template, dict):
                # Handle structured templates
                base_template = template.get('template', '')
                return base_template.format(**kwargs)
            else:
                return str(template)

        except KeyError as e:
            logger.error(f"Missing template variable: {e}")
            return f"Template error: missing {e}"

    def format_message_content(self, message: UnifiedMessage, **context) -> str:
        """Format message content with template resolution."""
        if not message.content:
            return ""

        # Check if content is a template key
        if message.content in self.templates:
            template_vars = {
                'sender': message.sender,
                'recipient': message.recipient,
                'timestamp': message.timestamp.isoformat(),
                **context
            }
            return self.resolve_template(message.content, **template_vars)

        # Return content as-is if not a template
        return message.content

    def resolve_file_template(self, template_filename: str, **kwargs) -> str:
        """Resolve file-based template with provided variables."""
        try:
            templates_dir = Path(__file__).parent.parent.parent / "templates"
            template_file = templates_dir / template_filename

            if not template_file.exists():
                # Try subdirectories
                for sub_dir in ["coordination", "messaging"]:
                    sub_template = templates_dir / sub_dir / template_filename
                    if sub_template.exists():
                        template_file = sub_template
                        break

            if not template_file.exists():
                logger.warning(f"File template {template_filename} not found")
                return ""

            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()

            # Apply variable substitution
            result = template_content
            for key, value in kwargs.items():
                result = result.replace(f"{{{key}}}", str(value))

            return result

        except Exception as e:
            logger.error(f"Error resolving file template {template_filename}: {e}")
            return ""

    def get_available_templates(self) -> List[str]:
        """Get list of available template keys."""
        template_keys = list(self.templates.keys())

        # Also include file-based templates from templates/ directory
        try:
            templates_dir = Path(__file__).parent.parent.parent / "templates"
            if templates_dir.exists():
                for template_file in templates_dir.rglob("*.txt"):
                    if template_file.is_file():
                        template_keys.append(f"file:{template_file.name}")
                for template_file in templates_dir.rglob("*.md"):
                    if template_file.is_file():
                        template_keys.append(f"file:{template_file.name}")
        except Exception as e:
            logger.debug(f"Could not scan templates directory: {e}")

        return template_keys