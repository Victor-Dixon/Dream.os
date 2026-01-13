"""
Tests for Pydantic Config SSOT

Tests for shared Pydantic configuration SSOT.
Ensures backward compatibility and proper configuration.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-05
"""

import pytest
from pydantic import BaseModel

from src.core.pydantic_config import (
    PydanticConfigV1,
    PydanticConfig,
    BasePydanticConfig,
    PYDANTIC_V2_AVAILABLE,
)


class TestPydanticConfigV1:
    """Tests for PydanticConfigV1 SSOT."""

    def test_pydantic_config_v1_attributes(self):
        """Test PydanticConfigV1 has required attributes."""
        assert hasattr(PydanticConfigV1, "arbitrary_types_allowed")
        assert hasattr(PydanticConfigV1, "validate_assignment")
        assert hasattr(PydanticConfigV1, "use_enum_values")
        assert hasattr(PydanticConfigV1, "extra")

    def test_pydantic_config_v1_values(self):
        """Test PydanticConfigV1 attribute values."""
        assert PydanticConfigV1.arbitrary_types_allowed is True
        assert PydanticConfigV1.validate_assignment is True
        assert PydanticConfigV1.use_enum_values is True
        assert PydanticConfigV1.extra == "forbid"

    def test_pydantic_config_v1_usage(self):
        """Test PydanticConfigV1 can be used in BaseModel."""
        class TestModel(BaseModel):
            class Config(PydanticConfigV1):
                pass
            
            value: str = "test"
        
        model = TestModel(value="test_value")
        assert model.value == "test_value"

    def test_pydantic_config_alias(self):
        """Test PydanticConfig is alias for PydanticConfigV1."""
        assert PydanticConfig is PydanticConfigV1


class TestBasePydanticConfig:
    """Tests for BasePydanticConfig (Pydantic v2)."""

    def test_base_pydantic_config_availability(self):
        """Test BasePydanticConfig availability based on Pydantic version."""
        if PYDANTIC_V2_AVAILABLE:
            assert BasePydanticConfig is not None
        else:
            assert BasePydanticConfig is None

    @pytest.mark.skipif(not PYDANTIC_V2_AVAILABLE, reason="Pydantic v2 not available")
    def test_base_pydantic_config_usage(self):
        """Test BasePydanticConfig can be used in Pydantic v2 models."""
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            model_config = BasePydanticConfig
            
            value: str = "test"
        
        model = TestModel(value="test_value")
        assert model.value == "test_value"


class TestPydanticConfigSSOT:
    """Tests for SSOT compliance."""

    def test_pydantic_config_ssot_import(self):
        """Test PydanticConfigV1 can be imported."""
        from src.core.pydantic_config import PydanticConfigV1
        assert PydanticConfigV1 is not None

    def test_pydantic_config_all_exports(self):
        """Test all expected exports are available."""
        from src.core.pydantic_config import (
            PydanticConfigV1,
            PydanticConfig,
            BasePydanticConfig,
            PYDANTIC_V2_AVAILABLE,
        )
        assert PydanticConfigV1 is not None
        assert PydanticConfig is not None
        assert PYDANTIC_V2_AVAILABLE is not None


