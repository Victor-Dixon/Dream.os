#!/usr/bin/env python3
"""
Type Utilities Module
====================

Standardized type system utilities for tools consolidation.
Provides unified type hints, validation, and conversion patterns.

Part of Phase 2A: Foundation Consolidation
Addresses typing.List, typing.Dict, typing.Any usage across tools.

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

import logging
from typing import Any, Dict, List, Optional, Union, Tuple, Set, Callable
from pathlib import Path

logger = logging.getLogger(__name__)

class TypeUtils:
    """Unified type system utilities for tools consolidation."""

    @staticmethod
    def safe_dict_get(data: Any, key: str, default: Any = None) -> Any:
        """Safely get value from dictionary-like object.

        Args:
            data: Dictionary or object to get value from
            key: Key to retrieve
            default: Default value if key not found or data invalid

        Returns:
            Retrieved value or default
        """
        try:
            if isinstance(data, dict):
                return data.get(key, default)
            elif hasattr(data, '__getitem__'):
                return data[key] if key in data else default
            elif hasattr(data, key):
                return getattr(data, key, default)
        except (KeyError, AttributeError, TypeError):
            pass

        return default

    @staticmethod
    def ensure_list(value: Any) -> List[Any]:
        """Ensure value is a list, converting if necessary.

        Args:
            value: Value to convert to list

        Returns:
            List representation of value
        """
        if value is None:
            return []
        elif isinstance(value, list):
            return value
        elif isinstance(value, (tuple, set)):
            return list(value)
        else:
            return [value]

    @staticmethod
    def ensure_dict(value: Any, default_key: str = "value") -> Dict[str, Any]:
        """Ensure value is a dictionary, converting if necessary.

        Args:
            value: Value to convert to dictionary
            default_key: Key to use for single values

        Returns:
            Dictionary representation of value
        """
        if isinstance(value, dict):
            return value
        elif value is None:
            return {}
        else:
            return {default_key: value}

    @staticmethod
    def validate_path_type(path: Any) -> Optional[Path]:
        """Validate and convert path-like objects to Path.

        Args:
            path: Path-like object to validate

        Returns:
            Path object or None if invalid
        """
        try:
            if path is None:
                return None
            return Path(path)
        except (TypeError, ValueError):
            logger.warning(f"Invalid path type: {type(path)} - {path}")
            return None

    @staticmethod
    def safe_cast(value: Any, target_type: type, default: Any = None) -> Any:
        """Safely cast value to target type.

        Args:
            value: Value to cast
            target_type: Type to cast to
            default: Default value on cast failure

        Returns:
            Cast value or default
        """
        try:
            if value is None:
                return default
            return target_type(value)
        except (ValueError, TypeError):
            logger.debug(f"Failed to cast {value} to {target_type.__name__}")
            return default

    @staticmethod
    def merge_dicts(*dicts: Dict[str, Any], deep: bool = False) -> Dict[str, Any]:
        """Merge multiple dictionaries.

        Args:
            *dicts: Dictionaries to merge
            deep: Whether to perform deep merge

        Returns:
            Merged dictionary
        """
        if not deep:
            result = {}
            for d in dicts:
                if isinstance(d, dict):
                    result.update(d)
            return result

        # Deep merge implementation
        result = {}
        for d in dicts:
            if not isinstance(d, dict):
                continue

            for key, value in d.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = TypeUtils.merge_dicts(result[key], value, deep=True)
                else:
                    result[key] = value

        return result

    @staticmethod
    def filter_dict(data: Dict[str, Any],
                   include_keys: Optional[List[str]] = None,
                   exclude_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """Filter dictionary keys.

        Args:
            data: Dictionary to filter
            include_keys: Keys to include (if specified, only these keys)
            exclude_keys: Keys to exclude

        Returns:
            Filtered dictionary
        """
        if not isinstance(data, dict):
            return {}

        result = data.copy()

        if include_keys:
            result = {k: v for k, v in result.items() if k in include_keys}

        if exclude_keys:
            for key in exclude_keys:
                result.pop(key, None)

        return result

    @staticmethod
    def validate_structure(data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate data structure against schema.

        Args:
            data: Data to validate
            schema: Schema definition

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        def validate_value(value: Any, schema_value: Any, path: str = "") -> None:
            if isinstance(schema_value, type):
                if not isinstance(value, schema_value):
                    errors.append(f"{path}: Expected {schema_value.__name__}, got {type(value).__name__}")
            elif isinstance(schema_value, dict):
                if not isinstance(value, dict):
                    errors.append(f"{path}: Expected dict, got {type(value).__name__}")
                else:
                    for key, expected_type in schema_value.items():
                        if key in value:
                            validate_value(value[key], expected_type, f"{path}.{key}")
                        else:
                            errors.append(f"{path}: Missing required key '{key}'")
            elif isinstance(schema_value, list) and len(schema_value) == 1:
                if not isinstance(value, list):
                    errors.append(f"{path}: Expected list, got {type(value).__name__}")
                else:
                    for i, item in enumerate(value):
                        validate_value(item, schema_value[0], f"{path}[{i}]")

        validate_value(data, schema)
        return len(errors) == 0, errors

# Convenience functions for backward compatibility
def safe_get(data: Any, key: str, default: Any = None) -> Any:
    """Legacy function for safe_dict_get."""
    return TypeUtils.safe_dict_get(data, key, default)

def to_list(value: Any) -> List[Any]:
    """Legacy function for ensure_list."""
    return TypeUtils.ensure_list(value)

def to_dict(value: Any, default_key: str = "value") -> Dict[str, Any]:
    """Legacy function for ensure_dict."""
    return TypeUtils.ensure_dict(value, default_key)