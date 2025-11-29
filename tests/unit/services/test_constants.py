"""
Tests for constants.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services import constants


class TestConstants:
    """Test constants module values."""

    def test_default_contract_id_constant(self):
        """Test DEFAULT_CONTRACT_ID constant value."""
        assert constants.DEFAULT_CONTRACT_ID == "default_contract"
        assert isinstance(constants.DEFAULT_CONTRACT_ID, str)

    def test_results_key_constant(self):
        """Test RESULTS_KEY constant value."""
        assert constants.RESULTS_KEY == "results"
        assert isinstance(constants.RESULTS_KEY, str)

    def test_summary_failed_constant(self):
        """Test SUMMARY_FAILED constant value."""
        assert constants.SUMMARY_FAILED == "failed"
        assert isinstance(constants.SUMMARY_FAILED, str)

    def test_summary_key_constant(self):
        """Test SUMMARY_KEY constant value."""
        assert constants.SUMMARY_KEY == "summary"
        assert isinstance(constants.SUMMARY_KEY, str)

    def test_summary_passed_constant(self):
        """Test SUMMARY_PASSED constant value."""
        assert constants.SUMMARY_PASSED == "passed"
        assert isinstance(constants.SUMMARY_PASSED, str)

    def test_all_exports(self):
        """Test __all__ list contains all expected constants."""
        expected_constants = [
            "SUMMARY_PASSED",
            "SUMMARY_FAILED",
            "RESULTS_KEY",
            "SUMMARY_KEY",
            "DEFAULT_CONTRACT_ID",
        ]
        
        assert hasattr(constants, '__all__')
        assert isinstance(constants.__all__, list)
        assert len(constants.__all__) == len(expected_constants)
        
        for constant in expected_constants:
            assert constant in constants.__all__, f"{constant} missing from __all__"

    def test_all_constants_are_strings(self):
        """Test all constants are string values."""
        constants_to_check = [
            constants.DEFAULT_CONTRACT_ID,
            constants.RESULTS_KEY,
            constants.SUMMARY_FAILED,
            constants.SUMMARY_KEY,
            constants.SUMMARY_PASSED,
        ]
        
        for constant_value in constants_to_check:
            assert isinstance(constant_value, str), f"Expected string, got {type(constant_value)}"

    def test_constants_not_empty(self):
        """Test all constants have non-empty values."""
        constants_to_check = [
            constants.DEFAULT_CONTRACT_ID,
            constants.RESULTS_KEY,
            constants.SUMMARY_FAILED,
            constants.SUMMARY_KEY,
            constants.SUMMARY_PASSED,
        ]
        
        for constant_value in constants_to_check:
            assert len(constant_value) > 0, f"Constant {constant_value} is empty"

    def test_constants_importable(self):
        """Test constants can be imported directly."""
        from src.services.constants import (
            DEFAULT_CONTRACT_ID,
            RESULTS_KEY,
            SUMMARY_FAILED,
            SUMMARY_KEY,
            SUMMARY_PASSED,
        )
        
        assert DEFAULT_CONTRACT_ID == "default_contract"
        assert RESULTS_KEY == "results"
        assert SUMMARY_FAILED == "failed"
        assert SUMMARY_KEY == "summary"
        assert SUMMARY_PASSED == "passed"

    def test_constants_module_has_correct_attributes(self):
        """Test constants module has all expected attributes."""
        expected_attrs = [
            "DEFAULT_CONTRACT_ID",
            "RESULTS_KEY",
            "SUMMARY_FAILED",
            "SUMMARY_KEY",
            "SUMMARY_PASSED",
            "__all__",
        ]
        
        for attr in expected_attrs:
            assert hasattr(constants, attr), f"Missing attribute: {attr}"

