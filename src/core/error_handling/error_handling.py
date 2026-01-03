#!/usr/bin/env python3
"""
Comprehensive Error Handling and Logging Framework
===================================================

V2 Compliance: Centralized error handling with proper logging, recovery, and monitoring.

Features:
- Structured logging with different severity levels
- Error classification and recovery strategies
- Performance monitoring and alerting
- Graceful degradation for non-critical errors
- Comprehensive error reporting and tracing

Author: Agent-4 (Captain) - Error Handling Specialist
Mission: V2 Compliance Implementation - Robust Error Management
"""

import logging
import logging.handlers
import sys
import traceback
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List, Type, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import wraps
from contextlib import contextmanager
import json
import threading
from enum import Enum

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.handlers.RotatingFileHandler(
            'logs/agent_cellphone.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
    ]
)

class ErrorSeverity(Enum):
    """Error severity levels for classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for better organization."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    CONFIGURATION = "configuration"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    MEMORY = "memory"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

@dataclass
class ErrorContext:
    """Context information for error reporting."""
    component: str
    operation: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ErrorReport:
    """Comprehensive error report structure."""
    error_id: str
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    exception_type: Optional[str] = None
    traceback: Optional[str] = None
    context: ErrorContext = None
    recovery_attempts: int = 0
    resolved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

class ErrorHandler:
    """Centralized error handling and logging system."""

    def __init__(self, component_name: str):
        self.component_name = component_name
        self.logger = logging.getLogger(component_name)
        self._error_history: List[ErrorReport] = []
        self._recovery_strategies: Dict[ErrorCategory, Callable] = {}
        self._alert_thresholds: Dict[ErrorSeverity, int] = {
            ErrorSeverity.LOW: 10,
            ErrorSeverity.MEDIUM: 5,
            ErrorSeverity.HIGH: 2,
            ErrorSeverity.CRITICAL: 1
        }

        # Setup structured logging
        self._setup_structured_logging()

    def _setup_structured_logging(self):
        """Setup structured logging with JSON formatting for errors."""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # JSON formatter for structured logs
        class StructuredFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                    "level": record.levelname,
                    "component": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno
                }

                # Add extra fields if present
                if hasattr(record, 'error_id'):
                    log_entry['error_id'] = record.error_id
                if hasattr(record, 'severity'):
                    log_entry['severity'] = record.severity
                if hasattr(record, 'category'):
                    log_entry['category'] = record.category

                return json.dumps(log_entry)

        # Add structured handler
        structured_handler = logging.FileHandler('logs/structured_errors.log')
        structured_handler.setFormatter(StructuredFormatter())
        structured_handler.setLevel(logging.WARNING)
        self.logger.addHandler(structured_handler)

    def log_error(self, error: Exception, context: Optional[ErrorContext] = None,
                  severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                  category: ErrorCategory = ErrorCategory.UNKNOWN) -> str:
        """Log an error with comprehensive context and generate error report."""

        # Generate unique error ID
        error_id = f"{self.component_name}_{int(time.time())}_{hash(str(error)) % 10000}"

        # Create error context if not provided
        if context is None:
            context = ErrorContext(
                component=self.component_name,
                operation="unknown",
                metadata={"error_type": type(error).__name__}
            )

        # Create error report
        report = ErrorReport(
            error_id=error_id,
            severity=severity,
            category=category,
            message=str(error),
            exception_type=type(error).__name__,
            traceback=traceback.format_exc(),
            context=context
        )

        # Store in history
        self._error_history.append(report)

        # Log with structured information
        extra = {
            'error_id': error_id,
            'severity': severity.value,
            'category': category.value
        }

        if severity == ErrorSeverity.CRITICAL:
            self.logger.critical(f"🚨 CRITICAL ERROR [{error_id}]: {error}", extra=extra, exc_info=True)
        elif severity == ErrorSeverity.HIGH:
            self.logger.error(f"🔴 HIGH ERROR [{error_id}]: {error}", extra=extra, exc_info=True)
        elif severity == ErrorSeverity.MEDIUM:
            self.logger.warning(f"🟡 MEDIUM ERROR [{error_id}]: {error}", extra=extra, exc_info=True)
        else:
            self.logger.info(f"🟢 LOW ERROR [{error_id}]: {error}", extra=extra)

        # Check if we should alert
        self._check_alert_thresholds(severity)

        # Attempt recovery if strategy exists
        if category in self._recovery_strategies:
            self._attempt_recovery(report)

        return error_id

    def _check_alert_thresholds(self, severity: ErrorSeverity):
        """Check if error frequency exceeds alert thresholds."""
        recent_errors = [
            e for e in self._error_history
            if e.created_at > datetime.now() - timedelta(hours=1)
            and e.severity == severity
        ]

        if len(recent_errors) >= self._alert_thresholds[severity]:
            self.logger.critical(
                f"🚨 ALERT: {len(recent_errors)} {severity.value.upper()} errors in last hour "
                f"(threshold: {self._alert_thresholds[severity]})"
            )

    def _attempt_recovery(self, report: ErrorReport):
        """Attempt automatic recovery for known error types."""
        try:
            strategy = self._recovery_strategies[report.category]
            result = strategy(report)

            if result:
                report.resolved = True
                report.resolved_at = datetime.now()
                self.logger.info(f"✅ Auto-recovered error {report.error_id}")
            else:
                report.recovery_attempts += 1
                self.logger.warning(f"❌ Recovery failed for error {report.error_id}")

        except Exception as recovery_error:
            self.logger.error(f"💥 Recovery strategy failed: {recovery_error}")
            report.recovery_attempts += 1

    def register_recovery_strategy(self, category: ErrorCategory, strategy: Callable[[ErrorReport], bool]):
        """Register a recovery strategy for a specific error category."""
        self._recovery_strategies[category] = strategy
        self.logger.info(f"📋 Registered recovery strategy for {category.value}")

    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary statistics."""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_errors = [e for e in self._error_history if e.created_at > cutoff]

        return {
            "total_errors": len(recent_errors),
            "by_severity": {
                severity.value: len([e for e in recent_errors if e.severity == severity])
                for severity in ErrorSeverity
            },
            "by_category": {
                category.value: len([e for e in recent_errors if e.category == category])
                for category in ErrorCategory
            },
            "unresolved": len([e for e in recent_errors if not e.resolved]),
            "auto_recovered": len([e for e in recent_errors if e.resolved and e.recovery_attempts > 0])
        }

# Global error handler instance
_error_handler = None

def get_error_handler(component_name: str = "global") -> ErrorHandler:
    """Get or create global error handler instance."""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler(component_name)
    return _error_handler

# Decorator for error handling
def handle_errors(severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 category: ErrorCategory = ErrorCategory.UNKNOWN,
                 recovery_strategy: Optional[Callable] = None):
    """Decorator to handle errors in functions with comprehensive logging."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = get_error_handler(func.__module__)

            # Register recovery strategy if provided
            if recovery_strategy:
                handler.register_recovery_strategy(category, recovery_strategy)

            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Create context from function information
                context = ErrorContext(
                    component=func.__module__,
                    operation=f"{func.__qualname__}",
                    metadata={
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys())
                    }
                )

                # Extract agent/user info from args if possible
                if args and hasattr(args[0], '__class__'):
                    if 'agent' in str(type(args[0])).lower():
                        context.agent_id = getattr(args[0], 'agent_id', None)

                error_id = handler.log_error(e, context, severity, category)

                # Re-raise critical errors, suppress others
                if severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
                    raise
                else:
                    return None  # Return None for handled errors

        return wrapper
    return decorator

# Context manager for error handling
@contextmanager
def error_context(component: str, operation: str, **metadata):
    """Context manager for scoped error handling."""
    handler = get_error_handler(component)
    context = ErrorContext(
        component=component,
        operation=operation,
        metadata=metadata
    )

    try:
        yield context
    except Exception as e:
        handler.log_error(e, context)
        raise

# Utility functions for common error patterns
def safe_dict_access(data: Optional[dict], key: str, default=None):
    """Safely access dictionary keys with error handling."""
    try:
        if data is None:
            return default
        return data.get(key, default)
    except (TypeError, AttributeError) as e:
        handler = get_error_handler("safe_dict_access")
        context = ErrorContext(
            component="safe_dict_access",
            operation="dict_access",
            metadata={"key": key, "data_type": type(data).__name__}
        )
        handler.log_error(e, context, ErrorSeverity.LOW, ErrorCategory.RUNTIME)
        return default

def safe_list_access(items: Optional[list], index: int, default=None):
    """Safely access list indices with error handling."""
    try:
        if items is None or not isinstance(items, list):
            return default
        return items[index] if 0 <= index < len(items) else default
    except (IndexError, TypeError) as e:
        handler = get_error_handler("safe_list_access")
        context = ErrorContext(
            component="safe_list_access",
            operation="list_access",
            metadata={"index": index, "list_length": len(items) if items else 0}
        )
        handler.log_error(e, context, ErrorSeverity.LOW, ErrorCategory.RUNTIME)
        return default

def validate_json_data(data: Any, schema: Optional[Dict] = None) -> bool:
    """Validate JSON data structure with error handling."""
    try:
        if data is None:
            return False

        # Basic type checks
        if not isinstance(data, (dict, list)):
            return False

        # Schema validation if provided
        if schema:
            return _validate_against_schema(data, schema)

        return True

    except Exception as e:
        handler = get_error_handler("json_validator")
        context = ErrorContext(
            component="json_validator",
            operation="validation",
            metadata={"data_type": type(data).__name__}
        )
        handler.log_error(e, context, ErrorSeverity.MEDIUM, ErrorCategory.RUNTIME)
        return False

def _validate_against_schema(data: Any, schema: Dict) -> bool:
    """Internal schema validation."""
    # Simple schema validation - can be extended
    if "type" in schema:
        expected_type = schema["type"]
        if expected_type == "object" and not isinstance(data, dict):
            return False
        elif expected_type == "array" and not isinstance(data, list):
            return False
        elif expected_type == "string" and not isinstance(data, str):
            return False

    if "required" in schema and isinstance(data, dict):
        for field in schema["required"]:
            if field not in data:
                return False

    return True

# Syntax validation utilities
def validate_python_syntax(file_path: Union[str, Path]) -> tuple[bool, Optional[str]]:
    """Validate Python file syntax with comprehensive error reporting."""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return False, f"File not found: {file_path}"

        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        compile(source, str(file_path), 'exec')
        return True, None

    except SyntaxError as e:
        error_msg = f"SyntaxError in {file_path}:{e.lineno}:{e.offset} - {e.msg}"
        return False, error_msg
    except Exception as e:
        error_msg = f"Error validating {file_path}: {e}"
        return False, error_msg

def validate_project_syntax(project_root: Union[str, Path] = ".",
                          file_pattern: str = "**/*.py") -> Dict[str, Any]:
    """Validate syntax of all Python files in project."""
    from pathlib import Path

    project_root = Path(project_root)
    results = {
        "total_files": 0,
        "valid_files": 0,
        "invalid_files": 0,
        "errors": []
    }

    handler = get_error_handler("syntax_validator")

    for py_file in project_root.glob(file_pattern):
        if py_file.is_file() and not any(part.startswith('.') for part in py_file.parts):
            results["total_files"] += 1

            is_valid, error_msg = validate_python_syntax(py_file)

            if is_valid:
                results["valid_files"] += 1
            else:
                results["invalid_files"] += 1
                results["errors"].append({
                    "file": str(py_file),
                    "error": error_msg
                })

                # Log syntax errors
                context = ErrorContext(
                    component="syntax_validator",
                    operation="file_validation",
                    metadata={"file_path": str(py_file)}
                )
                handler.log_error(
                    Exception(error_msg),
                    context,
                    ErrorSeverity.HIGH,
                    ErrorCategory.SYNTAX
                )

    return results