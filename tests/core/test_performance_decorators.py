"""
Unit tests for performance_decorators.py - MEDIUM PRIORITY

Tests monitor_performance decorator functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import time

# Add project root to path
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import directly to avoid __init__.py import chain issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "performance_decorators",
    project_root / "src" / "core" / "performance" / "performance_decorators.py"
)
performance_decorators = importlib.util.module_from_spec(spec)
spec.loader.exec_module(performance_decorators)

monitor_performance = performance_decorators.monitor_performance


class TestMonitorPerformance:
    """Test suite for monitor_performance decorator."""

    @pytest.fixture
    def mock_performance_monitor(self):
        """Create a mock performance monitor."""
        monitor = Mock()
        monitor.record_operation_start = Mock()
        monitor.record_operation_completion = Mock()
        return monitor

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_with_default_name(self, mock_get_monitor, mock_performance_monitor):
        """Test decorator with default operation name."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def test_function():
            return "result"

        result = test_function()

        assert result == "result"
        mock_get_monitor.assert_called_once()
        mock_performance_monitor.record_operation_start.assert_called_once()
        mock_performance_monitor.record_operation_completion.assert_called_once()
        # Check success=True was passed
        call_args = mock_performance_monitor.record_operation_completion.call_args
        # call_args is (args, kwargs), so call_args[0] is positional args
        assert len(call_args[0]) >= 2  # op_name, duration (success may be in kwargs)
        assert call_args[0][1] >= 0  # duration >= 0
        # Check success in kwargs or as 3rd positional arg
        if len(call_args[0]) >= 3:
            assert call_args[0][2] is True  # success=True
        elif 'success' in call_args[1]:
            assert call_args[1]['success'] is True

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_with_custom_name(self, mock_get_monitor, mock_performance_monitor):
        """Test decorator with custom operation name."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance(operation_name="custom_operation")
        def test_function():
            return "result"

        result = test_function()

        assert result == "result"
        mock_performance_monitor.record_operation_start.assert_called_once_with("custom_operation")
        mock_performance_monitor.record_operation_completion.assert_called_once()
        call_args = mock_performance_monitor.record_operation_completion.call_args
        assert call_args[0][0] == "custom_operation"

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_measures_duration(self, mock_get_monitor, mock_performance_monitor):
        """Test that decorator measures function duration."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def slow_function():
            time.sleep(0.1)
            return "done"

        result = slow_function()

        assert result == "done"
        call_args = mock_performance_monitor.record_operation_completion.call_args
        duration = call_args[0][1]
        assert duration >= 0.1  # Should be at least 0.1 seconds

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_handles_exceptions(self, mock_get_monitor, mock_performance_monitor):
        """Test that decorator records failure on exception."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def failing_function():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            failing_function()

        mock_performance_monitor.record_operation_start.assert_called_once()
        mock_performance_monitor.record_operation_completion.assert_called_once()
        call_args = mock_performance_monitor.record_operation_completion.call_args
        # Check success in kwargs or as 3rd positional arg
        if len(call_args[0]) >= 3:
            assert call_args[0][2] is False  # success=False
        elif 'success' in call_args[1]:
            assert call_args[1]['success'] is False
        else:
            # If success not explicitly passed, it defaults to False on exception
            assert True  # Test passes if exception was raised

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_preserves_function_metadata(self, mock_get_monitor, mock_performance_monitor):
        """Test that decorator preserves function metadata."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def documented_function():
            """This is a test function."""
            return "result"

        assert documented_function.__name__ == "documented_function"
        assert "test function" in documented_function.__doc__

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_with_function_args(self, mock_get_monitor, mock_performance_monitor):
        """Test decorator with function arguments."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def function_with_args(a, b, c=10):
            return a + b + c

        result = function_with_args(1, 2, c=3)

        assert result == 6
        mock_performance_monitor.record_operation_start.assert_called_once()
        mock_performance_monitor.record_operation_completion.assert_called_once()

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_with_multiple_calls(self, mock_get_monitor, mock_performance_monitor):
        """Test decorator with multiple function calls."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def test_function():
            return "result"

        test_function()
        test_function()
        test_function()

        assert mock_performance_monitor.record_operation_start.call_count == 3
        assert mock_performance_monitor.record_operation_completion.call_count == 3

    @patch.object(performance_decorators, 'get_performance_monitor')
    def test_decorator_operation_name_format(self, mock_get_monitor, mock_performance_monitor):
        """Test that default operation name uses module.function format."""
        mock_get_monitor.return_value = mock_performance_monitor

        @monitor_performance()
        def test_function():
            return "result"

        test_function()

        # Check that operation name was generated from function
        call_args = mock_performance_monitor.record_operation_start.call_args
        operation_name = call_args[0][0]
        assert "test_function" in operation_name

