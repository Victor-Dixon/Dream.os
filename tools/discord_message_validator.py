#!/usr/bin/env python3
"""
Discord Message Validator
=========================

Validates Discord messages, embeds, and fields against Discord's limits.
Prevents truncation and API errors by checking content before sending.

Discord Limits:
- Regular messages: 2000 characters
- Embed descriptions: 4096 characters
- Embed field values: 1024 characters
- Embed field names: 256 characters
- Total embed: 6000 characters
- Modal input labels: 45 characters

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-01-27
Status: ✅ V2 COMPLIANT (<400 lines)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Discord limits
MAX_MESSAGE_LENGTH = 2000
MAX_EMBED_DESCRIPTION = 4096
MAX_FIELD_VALUE = 1024
MAX_FIELD_NAME = 256
MAX_EMBED_TOTAL = 6000
MAX_MODAL_LABEL = 45
MAX_FIELDS_PER_EMBED = 25


class DiscordMessageValidator:
    """Validates Discord message content against limits."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_message(self, content: str) -> bool:
        """Validate regular message content."""
        if len(content) > MAX_MESSAGE_LENGTH:
            self.errors.append(
                f"Message exceeds limit: {len(content)}/{MAX_MESSAGE_LENGTH} chars"
            )
            return False
        return True

    def validate_embed(self, embed_data: Dict[str, Any]) -> bool:
        """Validate embed structure and content."""
        valid = True
        total_length = 0

        # Check description
        description = embed_data.get("description", "")
        if description:
            desc_len = len(description)
            total_length += desc_len
            if desc_len > MAX_EMBED_DESCRIPTION:
                self.errors.append(
                    f"Embed description exceeds limit: {desc_len}/{MAX_EMBED_DESCRIPTION} chars"
                )
                valid = False

        # Check fields
        fields = embed_data.get("fields", [])
        if len(fields) > MAX_FIELDS_PER_EMBED:
            self.errors.append(
                f"Too many fields: {len(fields)}/{MAX_FIELDS_PER_EMBED}"
            )
            valid = False

        for i, field in enumerate(fields):
            field_valid = self.validate_field(field, i)
            if not field_valid:
                valid = False
            # Add to total length
            field_name = field.get("name", "")
            field_value = field.get("value", "")
            total_length += len(field_name) + len(field_value)

        # Check total embed length
        if total_length > MAX_EMBED_TOTAL:
            self.warnings.append(
                f"Embed total length high: {total_length}/{MAX_EMBED_TOTAL} chars"
            )

        return valid

    def validate_field(self, field: Dict[str, Any], index: int) -> bool:
        """Validate embed field."""
        valid = True

        # Check field name
        name = field.get("name", "")
        if len(name) > MAX_FIELD_NAME:
            self.errors.append(
                f"Field {index} name exceeds limit: {len(name)}/{MAX_FIELD_NAME} chars"
            )
            valid = False

        # Check field value
        value = field.get("value", "")
        if len(value) > MAX_FIELD_VALUE:
            self.errors.append(
                f"Field {index} value exceeds limit: {len(value)}/{MAX_FIELD_VALUE} chars"
            )
            valid = False

        return valid

    def validate_modal_label(self, label: str) -> bool:
        """Validate modal input label."""
        if len(label) > MAX_MODAL_LABEL:
            self.errors.append(
                f"Modal label exceeds limit: {len(label)}/{MAX_MODAL_LABEL} chars"
            )
            return False
        return True

    def validate_file(self, file_path: Path) -> bool:
        """Validate Discord message/embed from JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            valid = True

            # Check for message content
            if "content" in data:
                if not self.validate_message(data["content"]):
                    valid = False

            # Check for embed
            if "embed" in data:
                if not self.validate_embed(data["embed"]):
                    valid = False

            # Check for modal labels
            if "modal_labels" in data:
                for i, label in enumerate(data["modal_labels"]):
                    if not self.validate_modal_label(label):
                        valid = False

            return valid

        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False

    def print_report(self) -> None:
        """Print validation report."""
        if self.errors:
            print("❌ VALIDATION ERRORS:")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")

        if not self.errors and not self.warnings:
            print("✅ All validations passed!")

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Discord messages against Discord limits"
    )
    parser.add_argument(
        "content",
        nargs="?",
        help="Message content to validate (or use --file)",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="JSON file with message/embed data",
    )
    parser.add_argument(
        "--embed-description",
        help="Embed description to validate",
    )
    parser.add_argument(
        "--field-value",
        help="Field value to validate",
    )
    parser.add_argument(
        "--modal-label",
        help="Modal label to validate",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    validator = DiscordMessageValidator()

    # Validate based on provided arguments
    if args.file:
        valid = validator.validate_file(args.file)
    elif args.embed_description:
        valid = validator.validate_embed({"description": args.embed_description})
    elif args.field_value:
        valid = validator.validate_field({"value": args.field_value}, 0)
    elif args.modal_label:
        valid = validator.validate_modal_label(args.modal_label)
    elif args.content:
        valid = validator.validate_message(args.content)
    else:
        parser.print_help()
        return 1

    if args.json:
        summary = validator.get_summary()
        print(json.dumps(summary, indent=2))
        return 0 if summary["valid"] else 1
    else:
        validator.print_report()
        return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())

