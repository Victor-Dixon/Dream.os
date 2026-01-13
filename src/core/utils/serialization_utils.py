#!/usr/bin/env python3
"""
Serialization Utilities - SSOT for to_dict() Patterns
======================================================

Provides standardized object-to-dictionary conversion functionality.
Consolidates duplicate to_dict() implementations across models.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

from dataclasses import asdict, fields, is_dataclass
from datetime import datetime
from typing import Any, Dict


def to_dict(obj: Any, include_none: bool = False) -> Dict[str, Any]:
    """
    Convert object to dictionary.
    
    SSOT for to_dict() conversion - consolidates duplicate serialization
    code from coordinator_models, analytics_models, and other model files.
    
    Handles:
    - Dataclasses (uses asdict)
    - Datetime objects (converts to ISO format)
    - Nested objects (recursive)
    - Enum values (converts to value attribute)
    - Regular objects (uses __dict__)
    
    Args:
        obj: Object to convert to dictionary
        include_none: Whether to include None values in output
        
    Returns:
        Dictionary representation of object
    """
    if is_dataclass(obj):
        result = {}
        for field in fields(obj):
            value = getattr(obj, field.name)
            
            # Handle None values
            if value is None and not include_none:
                continue
                
            # Handle datetime
            if isinstance(value, datetime):
                result[field.name] = value.isoformat()
            # Handle Enum (has value attribute)
            elif hasattr(value, 'value') and not isinstance(value, type):
                result[field.name] = value.value
            # Handle nested dataclasses
            elif is_dataclass(value):
                result[field.name] = to_dict(value, include_none)
            # Handle lists/tuples
            elif isinstance(value, (list, tuple)):
                result[field.name] = [
                    to_dict(item, include_none) if is_dataclass(item) else item
                    for item in value
                ]
            # Handle dictionaries
            elif isinstance(value, dict):
                result[field.name] = {
                    k: to_dict(v, include_none) if is_dataclass(v) else v
                    for k, v in value.items()
                }
            else:
                result[field.name] = value
        return result
    
    # Fallback for non-dataclass objects with __dict__
    if hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if value is None and not include_none:
                continue
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif hasattr(value, 'value') and not isinstance(value, type):
                result[key] = value.value
            elif is_dataclass(value):
                result[key] = to_dict(value, include_none)
            else:
                result[key] = value
        return result
    
    # Primitive types
    return obj


class DictSerializable:
    """
    Mixin class for objects that need to_dict() method.
    
    Classes can inherit from this mixin to get standardized to_dict()
    functionality without implementing it manually.
    """
    
    def to_dict(self, include_none: bool = False) -> Dict[str, Any]:
        """
        Convert object to dictionary using SSOT utility.
        
        Args:
            include_none: Whether to include None values
            
        Returns:
            Dictionary representation
        """
        return to_dict(self, include_none)


__all__ = ["to_dict", "DictSerializable"]

