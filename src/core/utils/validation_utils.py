#!/usr/bin/env python3
"""
Validation Utilities - SSOT for Validation Output Formatting
===========================================================

Provides standardized validation report printing functionality.
Consolidates duplicate validation error/warning printing code.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

from typing import List, Optional


def print_validation_report(
    errors: Optional[List[str]] = None,
    warnings: Optional[List[str]] = None,
    success_message: str = "✅ All validations passed!",
) -> None:
    """
    Print formatted validation report.
    
    SSOT for validation output formatting - consolidates duplicate code
    from tools/communication/*_validator.py files.
    
    Args:
        errors: List of error messages
        warnings: List of warning messages
        success_message: Message to display when no errors/warnings
    """
    if errors:
        print("❌ VALIDATION ERRORS:")
        for error in errors:
            print(f"  • {error}")
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
    if not errors and not warnings:
        print(success_message)


class ValidationReporter:
    """
    Mixin class for validators to use validation reporting.
    
    Validators can either:
    1. Inherit from this class and call self.print_report()
    2. Call the standalone function print_validation_report() directly
    
    The print_validation_report() function is available at module level.
    """
    
    def print_report(self) -> None:
        """
        Print validation report using errors and warnings attributes.
        
        Expects validator to have:
        - self.errors: Optional[List[str]]
        - self.warnings: Optional[List[str]]
        """
        print_validation_report(
            errors=getattr(self, 'errors', None),
            warnings=getattr(self, 'warnings', None),
        )


def validate_range(
    value: float,
    min_val: float,
    max_val: float,
    field_name: str,
) -> None:
    """
    Validate value is within specified range.
    
    SSOT for range validation - consolidates duplicate range checking code.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        field_name: Name of field for error message
        
    Raises:
        ValueError: If value is outside range
    """
    if not (min_val <= value <= max_val):
        raise ValueError(
            f"{field_name} must be between {min_val} and {max_val}"
        )


def validate_positive(
    value: float,
    field_name: str,
    min_val: float = 1,
) -> None:
    """
    Validate value is positive (>= min_val).
    
    SSOT for positive value validation - consolidates duplicate positive
    checking code.
    
    Args:
        value: Value to validate
        field_name: Name of field for error message
        min_val: Minimum allowed value (default: 1)
        
    Raises:
        ValueError: If value is less than min_val
    """
    if value < min_val:
        raise ValueError(f"{field_name} must be at least {min_val}")


def validate_config_list(
    config: object,
    validators: List[tuple[str, callable]],
) -> List[str]:
    """
    Validate configuration using list of field validators.
    
    SSOT for list-based configuration validation - consolidates duplicate
    validation error collection patterns.
    
    Args:
        config: Configuration object to validate
        validators: List of (field_name, validator_func) tuples
                   validator_func should return error message or None
        
    Returns:
        List of error messages (empty if all validations pass)
    """
    errors = []
    for field_name, validator in validators:
        try:
            value = getattr(config, field_name, None)
            error = validator(value, field_name)
            if error:
                errors.append(error)
        except ValueError as e:
            errors.append(str(e))
        except Exception as e:
            errors.append(f"{field_name}: {str(e)}")
    return errors


__all__ = [
    "print_validation_report",
    "ValidationReporter",
    "validate_range",
    "validate_positive",
    "validate_config_list",
]

