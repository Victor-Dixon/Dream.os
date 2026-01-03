#!/usr/bin/env python3
"""
Test-Driven Development for Error Handling Framework
===================================================

V2 Compliance: Comprehensive testing of error handling, logging, and recovery.

Tests cover:
- Error classification and severity levels
- Structured logging functionality
- Recovery strategy registration and execution
- Safe data access utilities
- Syntax validation utilities

Author: Agent-4 (Captain) - Error Handling Test Specialist
Mission: V2 Compliance Implementation - Test Error Management
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from src.core.error_handling import (
    ErrorHandler, ErrorSeverity, ErrorCategory, ErrorContext, ErrorReport,
    get_error_handler, handle_errors, error_context,
    safe_dict_access, safe_list_access, validate_json_data,
    validate_python_syntax, validate_project_syntax
)


class TestErrorHandling(unittest.TestCase):
    """Test error handling framework components."""

    def setUp(self):
        """Set up test fixtures."""
        self.handler = ErrorHandler("test_component")
        self.test_context = ErrorContext(
            component="test_component",
            operation="test_operation",
            agent_id="Agent-1",
            metadata={"test_key": "test_value"}
        )

    def test_error_severity_enum(self):
        """Test error severity levels."""
        self.assertEqual(ErrorSeverity.LOW.value, "low")
        self.assertEqual(ErrorSeverity.CRITICAL.value, "critical")
        # Test all severity levels exist
        self.assertIn("medium", [e.value for e in ErrorSeverity])
        self.assertIn("high", [e.value for e in ErrorSeverity])

    def test_error_category_enum(self):
        """Test error category classification."""
        self.assertEqual(ErrorCategory.SYNTAX.value, "syntax")
        self.assertEqual(ErrorCategory.RUNTIME.value, "runtime")

    def test_error_context_creation(self):
        """Test error context creation."""
        context = ErrorContext(
            component="test",
            operation="test_op",
            user_id="user123"
        )
        self.assertEqual(context.component, "test")
        self.assertEqual(context.operation, "test_op")
        self.assertEqual(context.user_id, "user123")
        self.assertIsInstance(context.timestamp, datetime)

    def test_error_report_creation(self):
        """Test error report structure."""
        report = ErrorReport(
            error_id="test_123",
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.RUNTIME,
            message="Test error message",
            exception_type="ValueError",
            context=self.test_context
        )

        self.assertEqual(report.error_id, "test_123")
        self.assertEqual(report.severity, ErrorSeverity.HIGH)
        self.assertEqual(report.category, ErrorCategory.RUNTIME)
        self.assertFalse(report.resolved)

    def test_safe_dict_access(self):
        """Test safe dictionary access."""
        test_dict = {"key1": "value1", "key2": {"nested": "value"}}

        # Normal access
        self.assertEqual(safe_dict_access(test_dict, "key1"), "value1")

        # Missing key
        self.assertEqual(safe_dict_access(test_dict, "missing", "default"), "default")

        # None input
        self.assertEqual(safe_dict_access(None, "key"), None)

        # Dict value access (should work safely)
        nested = safe_dict_access(test_dict, "key2")
        self.assertEqual(nested["nested"], "value")

    def test_safe_list_access(self):
        """Test safe list access."""
        test_list = ["item1", "item2", "item3"]

        # Normal access
        self.assertEqual(safe_list_access(test_list, 0), "item1")
        self.assertEqual(safe_list_access(test_list, 2), "item3")

        # Out of bounds
        self.assertEqual(safe_list_access(test_list, 10, "default"), "default")
        self.assertEqual(safe_list_access(test_list, -1, "default"), "default")

        # None input
        self.assertEqual(safe_list_access(None, 0), None)

        # Non-list input
        self.assertEqual(safe_list_access("not a list", 0), None)

    def test_validate_json_data(self):
        """Test JSON data validation."""
        # Valid data
        self.assertTrue(validate_json_data({"key": "value"}))
        self.assertTrue(validate_json_data(["item1", "item2"]))

        # Invalid data
        self.assertFalse(validate_json_data(None))
        self.assertFalse(validate_json_data("string"))
        self.assertFalse(validate_json_data(123))

    def test_validate_python_syntax(self):
        """Test Python syntax validation."""
        # Create a temporary valid Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('def hello():\n    print("Hello, World!")\n')
            valid_file = f.name

        try:
            is_valid, error = validate_python_syntax(valid_file)
            self.assertTrue(is_valid)
            self.assertIsNone(error)
        finally:
            os.unlink(valid_file)

        # Create a temporary invalid Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('def broken_function(\n    print("missing closing paren")\n')
            invalid_file = f.name

        try:
            is_valid, error = validate_python_syntax(invalid_file)
            self.assertFalse(is_valid)
            self.assertIn("SyntaxError", error)
        finally:
            os.unlink(invalid_file)

        # Test non-existent file
        is_valid, error = validate_python_syntax("non_existent_file.py")
        self.assertFalse(is_valid)
        self.assertIn("File not found", error)

    def test_validate_project_syntax(self):
        """Test project-wide syntax validation."""
        # Create a temporary directory with mixed Python files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Valid file
            (temp_path / "valid.py").write_text('print("hello")')

            # Invalid file
            (temp_path / "invalid.py").write_text('def broken(:\n    pass')

            # Non-Python file (should be ignored)
            (temp_path / "readme.txt").write_text("This is not Python code")

            results = validate_project_syntax(temp_path)

            self.assertEqual(results["total_files"], 2)  # Only Python files
            self.assertEqual(results["valid_files"], 1)
            self.assertEqual(results["invalid_files"], 1)
            self.assertEqual(len(results["errors"]), 1)
            self.assertIn("invalid.py", results["errors"][0]["file"])

    def test_error_handler_logging(self):
        """Test error handler logging functionality."""
        # Test error logging
        test_error = ValueError("Test error message")
        error_id = self.handler.log_error(test_error, self.test_context)

        self.assertIsInstance(error_id, str)
        self.assertTrue(error_id.startswith("test_component_"))

        # Check error history
        self.assertEqual(len(self.handler._error_history), 1)
        report = self.handler._error_history[0]
        self.assertEqual(report.message, "Test error message")
        self.assertEqual(report.exception_type, "ValueError")
        self.assertEqual(report.context, self.test_context)

    def test_recovery_strategy_registration(self):
        """Test recovery strategy registration and execution."""
        recovery_called = False

        def test_recovery(report: ErrorReport) -> bool:
            nonlocal recovery_called
            recovery_called = True
            return True

        # Register recovery strategy
        self.handler.register_recovery_strategy(ErrorCategory.RUNTIME, test_recovery)

        # Log error that should trigger recovery
        test_error = RuntimeError("Recoverable error")
        error_id = self.handler.log_error(
            test_error,
            self.test_context,
            ErrorSeverity.MEDIUM,
            ErrorCategory.RUNTIME
        )

        # Check recovery was attempted
        self.assertTrue(recovery_called)

        # Check error was marked as resolved
        report = self.handler._error_history[0]
        self.assertTrue(report.resolved)
        self.assertEqual(report.recovery_attempts, 1)

    def test_error_summary_statistics(self):
        """Test error summary statistics generation."""
        # Add some test errors
        errors = [
            (ValueError("Error 1"), ErrorSeverity.LOW, ErrorCategory.SYNTAX),
            (RuntimeError("Error 2"), ErrorSeverity.MEDIUM, ErrorCategory.RUNTIME),
            (ConnectionError("Error 3"), ErrorSeverity.HIGH, ErrorCategory.NETWORK),
            (RuntimeError("Error 4"), ErrorSeverity.MEDIUM, ErrorCategory.RUNTIME),
        ]

        for error, severity, category in errors:
            self.handler.log_error(error, self.test_context, severity, category)

        # Get summary
        summary = self.handler.get_error_summary(hours=1)

        self.assertEqual(summary["total_errors"], 4)
        self.assertEqual(summary["by_severity"]["low"], 1)
        self.assertEqual(summary["by_severity"]["medium"], 2)
        self.assertEqual(summary["by_severity"]["high"], 1)
        self.assertEqual(summary["by_category"]["syntax"], 1)
        self.assertEqual(summary["by_category"]["runtime"], 2)
        self.assertEqual(summary["by_category"]["network"], 1)

    @patch('src.core.error_handling.logger')
    def test_structured_logging(self, mock_logger):
        """Test structured JSON logging."""
        test_error = Exception("Structured test error")
        self.handler.log_error(test_error, self.test_context)

        # Verify structured logging was called
        mock_logger.error.assert_called()
        call_args = mock_logger.error.call_args
        self.assertIn('error_id', call_args.kwargs.get('extra', {}))

    def test_handle_errors_decorator(self):
        """Test error handling decorator."""
        @handle_errors(severity=ErrorSeverity.LOW, category=ErrorCategory.RUNTIME)
        def failing_function():
            raise ValueError("Test failure")

        # Function should not raise, should return None
        result = failing_function()
        self.assertIsNone(result)

        # Check error was logged
        self.assertEqual(len(self.handler._error_history), 1)
        report = self.handler._error_history[0]
        self.assertEqual(report.severity, ErrorSeverity.LOW)
        self.assertEqual(report.category, ErrorCategory.RUNTIME)

    def test_handle_errors_decorator_critical(self):
        """Test error handling decorator with critical severity."""
        @handle_errors(severity=ErrorSeverity.CRITICAL, category=ErrorCategory.RUNTIME)
        def critical_failing_function():
            raise ValueError("Critical test failure")

        # Function should re-raise critical errors
        with self.assertRaises(ValueError):
            critical_failing_function()

    def test_error_context_manager(self):
        """Test error context manager."""
        error_caught = None

        try:
            with error_context("test_component", "test_operation", test_param="value"):
                raise ValueError("Context test error")
        except ValueError as e:
            error_caught = e

        self.assertIsNotNone(error_caught)
        # Error should be logged automatically
        self.assertEqual(len(self.handler._error_history), 1)


class TestStatusMonitorErrorHandling(unittest.TestCase):
    """Test status monitor error handling specifically."""

    def setUp(self):
        """Set up status monitor test."""
        # Mock discord to avoid import issues
        with patch.dict('sys.modules', {'discord': MagicMock(), 'discord.ext': MagicMock()}):
            from src.discord_commander.status_change_monitor import StatusChangeMonitor
            self.monitor = StatusChangeMonitor(MagicMock(), channel_id=12345)

    def test_detect_changes_with_dict_values(self):
        """Test _detect_changes handles dict values safely."""
        old_status = {
            "status": "active",
            "current_mission": {"id": "mission1", "name": "Test Mission"}
        }
        new_status = {
            "status": "completed",
            "current_mission": {"id": "mission1", "name": "Test Mission"}
        }

        changes = self.monitor._detect_changes(old_status, new_status)

        # Should handle dict values without unhashable errors
        self.assertIn("status", changes)
        self.assertIn("mission", changes)
        # Dict values should be converted to strings
        self.assertIsInstance(changes["mission"]["old"], str)
        self.assertIsInstance(changes["mission"]["new"], str)

    def test_detect_changes_with_list_values(self):
        """Test _detect_changes handles list values with dicts."""
        old_status = {
            "current_tasks": [{"id": "task1", "name": "Task 1"}]
        }
        new_status = {
            "current_tasks": [
                {"id": "task1", "name": "Task 1"},
                {"id": "task2", "name": "Task 2"}
            ]
        }

        changes = self.monitor._detect_changes(old_status, new_status)

        # Should handle dicts in lists without unhashable errors
        self.assertIn("current_tasks", changes)
        self.assertEqual(len(changes["current_tasks"]), 1)  # One new task


if __name__ == '__main__':
    # Setup logging for tests
    import logging
    logging.basicConfig(level=logging.DEBUG)

    # Run tests
    unittest.main(verbosity=2)