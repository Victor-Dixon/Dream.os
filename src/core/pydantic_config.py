"""
@file
@summary Expose shared Pydantic config classes with v1 and v2 compatibility.
@registry docs/recovery/recovery_registry.yaml#core-pydantic-config-shim
"""

try:
    from pydantic import ConfigDict

    PYDANTIC_V2_AVAILABLE = True
    BasePydanticConfig = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",
    )
except Exception:
    PYDANTIC_V2_AVAILABLE = False
    BasePydanticConfig = None


class PydanticConfigV1:
    arbitrary_types_allowed = True
    validate_assignment = True
    use_enum_values = True
    extra = "forbid"


PydanticConfig = PydanticConfigV1

__all__ = [
    "PydanticConfigV1",
    "PydanticConfig",
    "BasePydanticConfig",
    "PYDANTIC_V2_AVAILABLE",
]
