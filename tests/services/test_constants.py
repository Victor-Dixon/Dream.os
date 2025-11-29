"""
Tests for constants.py

Comprehensive tests for validation service constants.
Target: ≥85% coverage
"""

import pytest
from src.services.constants import (
    DEFAULT_CONTRACT_ID,
    RESULTS_KEY,
    SUMMARY_FAILED,
    SUMMARY_KEY,
    SUMMARY_PASSED,
)


class TestConstants:
    """Tests for constants."""

    def test_default_contract_id(self):
        """Test DEFAULT_CONTRACT_ID constant."""
        assert DEFAULT_CONTRACT_ID == "default_contract"
        assert isinstance(DEFAULT_CONTRACT_ID, str)

    def test_results_key(self):
        """Test RESULTS_KEY constant."""
        assert RESULTS_KEY == "results"
        assert isinstance(RESULTS_KEY, str)

    def test_summary_failed(self):
        """Test SUMMARY_FAILED constant."""
        assert SUMMARY_FAILED == "failed"
        assert isinstance(SUMMARY_FAILED, str)

    def test_summary_key(self):
        """Test SUMMARY_KEY constant."""
        assert SUMMARY_KEY == "summary"
        assert isinstance(SUMMARY_KEY, str)

    def test_summary_passed(self):
        """Test SUMMARY_PASSED constant."""
        assert SUMMARY_PASSED == "passed"
        assert isinstance(SUMMARY_PASSED, str)

    def test_all_constants_exported(self):
        """Test that all constants are in __all__."""
        from src.services.constants import __all__
        
        assert "DEFAULT_CONTRACT_ID" in __all__
        assert "RESULTS_KEY" in __all__
        assert "SUMMARY_FAILED" in __all__
        assert "SUMMARY_KEY" in __all__
        assert "SUMMARY_PASSED" in __all__

    def test_constants_usage_in_dict(self):
        """Test constants can be used as dictionary keys."""
        test_dict = {
            RESULTS_KEY: [],
            SUMMARY_KEY: {
                SUMMARY_PASSED: 0,
                SUMMARY_FAILED: 0,
            }
        }
        
        assert RESULTS_KEY in test_dict
        assert SUMMARY_KEY in test_dict
        assert SUMMARY_PASSED in test_dict[SUMMARY_KEY]
        assert SUMMARY_FAILED in test_dict[SUMMARY_KEY]

