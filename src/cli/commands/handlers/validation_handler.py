#!/usr/bin/env python3
"""
Validation Handler - CLI Command Handler
=======================================

Handles validation and testing commands for the main CLI.

V2 Compliant: Yes (<100 lines)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2026-01-07
"""

from typing import Dict, Any
from src.cli.validation_runner import ValidationRunner


class ValidationHandler:
    """Handles validation-related CLI commands."""

    def __init__(self):
        self.validation_runner = ValidationRunner()

    def handle_validate_command(self, command_info: Dict[str, Any]) -> None:
        """Handle validation command."""
        output_file = command_info.get('output_file', 'main_validation.json')
        results = self.validation_runner.run_comprehensive_validation(output_file)

        self._print_validation_results(results)

    def handle_quick_validate_command(self) -> bool:
        """Handle quick validation check."""
        try:
            results = self.validation_runner.run_quick_validation()
            return results.get('overall_status') == 'PASS'
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return False

    def _print_validation_results(self, results: Dict[str, Any]) -> None:
        """Print comprehensive validation results."""
        print("📊 Comprehensive Validation Results")
        print("=" * 40)
        print(f"🏥 Overall Status: {results['overall_status']}")

        validations = results.get('validations', {})
        for validation_name, result in validations.items():
            status = result.get('status', 'UNKNOWN')
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {validation_name.replace('_', ' ').title()}: {status}")

        # Print summary
        passed = sum(1 for r in validations.values() if r.get('status') == 'PASS')
        total = len(validations)
        print(f"\n📈 Summary: {passed}/{total} validations passed")

        if passed < total:
            print("\n🔧 Failed validations require attention:")
            for name, result in validations.items():
                if result.get('status') != 'PASS':
                    error = result.get('error', 'Unknown error')
                    print(f"   • {name}: {error}")


# Factory function for backward compatibility
def create_validation_handler() -> ValidationHandler:
    """Create and return a ValidationHandler instance."""
    return ValidationHandler()