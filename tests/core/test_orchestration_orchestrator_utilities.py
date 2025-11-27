"""
Unit tests for orchestration/orchestrator_utilities.py - MEDIUM PRIORITY

Tests OrchestratorUtilities class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using importlib to bypass __init__.py chain
import importlib.util
utilities_path = project_root / "src" / "core" / "orchestration" / "orchestrator_utilities.py"
spec = importlib.util.spec_from_file_location("orchestrator_utilities", utilities_path)
orchestrator_utilities = importlib.util.module_from_spec(spec)
orchestrator_utilities.__package__ = 'src.core.orchestration'
spec.loader.exec_module(orchestrator_utilities)

OrchestratorUtilities = orchestrator_utilities.OrchestratorUtilities


class TestOrchestratorUtilities:
    """Test suite for OrchestratorUtilities class."""

    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger."""
        return Mock()

    @pytest.fixture
    def mock_emit(self):
        """Create a mock emit function."""
        events = []
        def emit(event_type, data):
            events.append((event_type, data))
        emit.events = events
        return emit

    def test_safe_execute_success(self, mock_logger, mock_emit):
        """Test safe_execute with successful operation."""
        def operation(x, y):
            return x + y
        
        result = OrchestratorUtilities.safe_execute(
            operation=operation,
            operation_name="test_operation",
            default_return=0,
            logger_instance=mock_logger,
            emit_func=mock_emit,
            x=5,
            y=3
        )
        
        assert result == 8
        mock_logger.debug.assert_called_once()
        assert len(mock_emit.events) == 1
        assert mock_emit.events[0][0] == "test_operation_success"

    def test_safe_execute_failure(self, mock_logger, mock_emit):
        """Test safe_execute with failed operation."""
        def operation():
            raise ValueError("Test error")
        
        result = OrchestratorUtilities.safe_execute(
            operation=operation,
            operation_name="test_operation",
            default_return="default",
            logger_instance=mock_logger,
            emit_func=mock_emit
        )
        
        assert result == "default"
        mock_logger.error.assert_called_once()
        assert len(mock_emit.events) == 1
        assert mock_emit.events[0][0] == "test_operation_error"
        assert "error" in mock_emit.events[0][1]

    def test_safe_execute_with_kwargs(self, mock_logger, mock_emit):
        """Test safe_execute with keyword arguments."""
        def operation(value, multiplier=2):
            return value * multiplier
        
        result = OrchestratorUtilities.safe_execute(
            operation=operation,
            operation_name="multiply",
            default_return=0,
            logger_instance=mock_logger,
            emit_func=mock_emit,
            value=5,
            multiplier=3
        )
        
        assert result == 15

    def test_sanitize_config_removes_suspicious_patterns(self, mock_logger):
        """Test sanitize_config sets suspicious patterns to None."""
        config = {
            "safe_key": "safe_value",
            "dangerous_key": "DROP TABLE users;",
            "another_key": "rm -rf /",
        }
        
        sanitized = OrchestratorUtilities.sanitize_config(config, mock_logger)
        
        assert sanitized["safe_key"] == "safe_value"
        assert sanitized["dangerous_key"] is None
        assert sanitized["another_key"] is None

    def test_sanitize_config_allows_safe_values(self, mock_logger):
        """Test sanitize_config allows safe values."""
        config = {
            "key1": "normal_value",
            "key2": 123,
            "key3": True,
            "key4": ["list", "values"],
        }
        
        sanitized = OrchestratorUtilities.sanitize_config(config, mock_logger)
        
        assert sanitized["key1"] == "normal_value"
        assert sanitized["key2"] == 123
        assert sanitized["key3"] is True
        assert sanitized["key4"] == ["list", "values"]

    def test_sanitize_config_handles_empty_config(self, mock_logger):
        """Test sanitize_config with empty config."""
        config = {}
        
        sanitized = OrchestratorUtilities.sanitize_config(config, mock_logger)
        
        assert sanitized == {}

    def test_sanitize_config_logs_removed_keys(self, mock_logger):
        """Test sanitize_config logs removed keys."""
        config = {
            "safe": "value",
            "dangerous": "eval('malicious')",
        }
        
        OrchestratorUtilities.sanitize_config(config, mock_logger)
        
        # Should log warnings for removed keys
        assert mock_logger.warning.called

    def test_safe_execute_preserves_result_type(self, mock_logger, mock_emit):
        """Test safe_execute preserves result type."""
        def operation():
            return {"key": "value"}
        
        result = OrchestratorUtilities.safe_execute(
            operation=operation,
            operation_name="dict_operation",
            default_return={},
            logger_instance=mock_logger,
            emit_func=mock_emit
        )
        
        assert isinstance(result, dict)
        assert result["key"] == "value"

    def test_safe_execute_handles_none_result(self, mock_logger, mock_emit):
        """Test safe_execute handles None result."""
        def operation():
            return None
        
        result = OrchestratorUtilities.safe_execute(
            operation=operation,
            operation_name="none_operation",
            default_return="default",
            logger_instance=mock_logger,
            emit_func=mock_emit
        )
        
        assert result is None

    def test_sanitize_config_case_insensitive_detection(self, mock_logger):
        """Test sanitize_config detects patterns case-insensitively."""
        config = {
            "safe": "value",
            "dangerous1": "drop table users;",
            "dangerous2": "DELETE FROM data",
        }
        
        sanitized = OrchestratorUtilities.sanitize_config(config, mock_logger)
        
        assert sanitized["safe"] == "value"
        assert sanitized["dangerous1"] is None
        assert sanitized["dangerous2"] is None

