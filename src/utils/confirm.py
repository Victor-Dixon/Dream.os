#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Minimal confirmation utility for handlers.
Provides basic confirm functionality to support onboarding/utility handlers.
"""

import sys


def confirm(message: str, default: bool = True) -> bool:
    """
    Get user confirmation.

    Args:
        message: Confirmation message to display
        default: Default value if no input provided

    Returns:
        True if confirmed, False otherwise
    """
    try:
        response = input(f"{message} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
        if not response:
            return default
        return response in ('y', 'yes', 'true', '1')
    except (EOFError, KeyboardInterrupt):
        # Handle non-interactive environments
        return default


if __name__ == "__main__":
    # Simple test
    if confirm("Test confirmation"):
        print("Confirmed")
    else:
        print("Not confirmed")

