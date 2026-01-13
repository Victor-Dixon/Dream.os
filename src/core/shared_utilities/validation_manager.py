"""
<!-- SSOT Domain: core -->

Validation Manager - Validation Operations
==========================================

Manages validation operations.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

from datetime import datetime
from typing import Any, Dict

from .base_utility import BaseUtility


class ValidationManager(BaseUtility):
    """Manages validation operations."""

    def __init__(self):
        super().__init__()
        self.validation_rules = {}
        self.validation_results = []

    def initialize(self) -> bool:
        """Initialize validation manager."""
        self.logger.info("ValidationManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up validation resources."""
        self.validation_rules.clear()
        self.validation_results.clear()
        return True

    def add_validation_rule(self, name: str, rule: callable) -> None:
        """Add a validation rule."""
        self.validation_rules[name] = rule

    def validate(self, data: Any) -> Dict[str, Any]:
        """Validate data against all rules."""
        results = {}

        for name, rule in self.validation_rules.items():
            try:
                result = rule(data)
                results[name] = result
            except Exception as e:
                results[name] = f"Validation error: {e}"

        self.validation_results.append({
            'timestamp': datetime.now(),
            'data': str(data),
            'results': results
        })

        return results

    def get_validation_results(self) -> list:
        """Get validation results history."""
        return self.validation_results.copy()


