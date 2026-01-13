#!/usr/bin/env python3
"""
Shared Pydantic Configuration - SSOT
====================================

Single source of truth for Pydantic model configurations.
Provides shared config classes for all Pydantic models in the codebase.

<!-- SSOT Domain: core -->

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

from typing import Any

try:
    from pydantic import ConfigDict
    PYDANTIC_V2_AVAILABLE = True
except ImportError:
    PYDANTIC_V2_AVAILABLE = False
    ConfigDict = None


# Pydantic v2 style (recommended for new code)
if PYDANTIC_V2_AVAILABLE:
    BasePydanticConfig = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",  # Prevent extra fields
    )
else:
    BasePydanticConfig = None


# Pydantic v1 style (for backward compatibility)
class PydanticConfigV1:
    """
    Pydantic v1 config class - SSOT for Pydantic v1 models.
    
    Use this for Pydantic v1 BaseModel classes:
    
    ```python
    from pydantic import BaseModel
    from src.core.pydantic_config import PydanticConfigV1
    
    class MyModel(BaseModel):
        class Config(PydanticConfigV1):
            pass
    ```
    """
    arbitrary_types_allowed = True
    validate_assignment = True
    use_enum_values = True
    extra = "forbid"  # Prevent extra fields


# Convenience alias
PydanticConfig = PydanticConfigV1


__all__ = [
    "BasePydanticConfig",
    "PydanticConfigV1",
    "PydanticConfig",
    "PYDANTIC_V2_AVAILABLE",
]

