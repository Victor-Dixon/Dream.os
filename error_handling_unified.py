"""Unified error handling utilities for tests."""

from __future__ import annotations

import contextlib
import json
import logging
import traceback
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    NETWORK = "network"
    DATA = "data"
    SECURITY = "security"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    component: str
    operation: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ErrorReport:
    error_id: str
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    exception_type: str
    context: ErrorContext
    timestamp: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False
    resolution_notes: Optional[str] = None


class ErrorHandler:
    def __init__(self, component: str) -> None:
        self.component = component
        self._error_history: List[ErrorReport] = []
        self._recovery_strategies: Dict[ErrorCategory, Callable[[ErrorReport], bool]] = {}

    def log_error(
        self,
        error: Exception,
        context: ErrorContext,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.RUNTIME,
    ) -> str:
        error_id = f"{self.component}_{uuid.uuid4().hex[:8]}"
        report = ErrorReport(
            error_id=error_id,
            severity=severity,
            category=category,
            message=str(error),
            exception_type=type(error).__name__,
            context=context,
        )
        self._error_history.append(report)
        logger.error(
            "error",
            extra={
                "error_id": error_id,
                "severity": severity.value,
                "category": category.value,
                "component": context.component,
                "operation": context.operation,
            },
        )
        return error_id

    def register_recovery_strategy(self, category: ErrorCategory, handler: Callable[[ErrorReport], bool]) -> None:
        self._recovery_strategies[category] = handler

    def attempt_recovery(self, report: ErrorReport) -> bool:
        handler = self._recovery_strategies.get(report.category)
        if not handler:
            return False
        return handler(report)

    def cleanup_old_errors(self, hours: int = 24) -> None:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        self._error_history = [r for r in self._error_history if r.timestamp >= cutoff]

    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent = [r for r in self._error_history if r.timestamp >= cutoff]
        by_severity: Dict[str, int] = {}
        by_category: Dict[str, int] = {}
        for report in recent:
            by_severity[report.severity.value] = by_severity.get(report.severity.value, 0) + 1
            by_category[report.category.value] = by_category.get(report.category.value, 0) + 1
        return {
            "total_errors": len(recent),
            "by_severity": by_severity,
            "by_category": by_category,
        }


_default_handler = ErrorHandler("test_component")


def get_error_handler(component: str | None = None) -> ErrorHandler:
    return _default_handler if component is None else ErrorHandler(component)


def handle_errors(
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    category: ErrorCategory = ErrorCategory.RUNTIME,
):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                context = ErrorContext(component=_default_handler.component, operation=func.__name__)
                _default_handler.log_error(exc, context, severity, category)
                if severity == ErrorSeverity.CRITICAL:
                    raise
                return None
        return wrapper
    return decorator


@contextlib.contextmanager
def error_context(component: str, operation: str, **metadata: Any):
    context = ErrorContext(component=component, operation=operation, metadata=metadata)
    try:
        yield context
    except Exception as exc:
        _default_handler.log_error(exc, context)
        raise


def safe_dict_access(data: Optional[Dict[str, Any]], key: str, default: Any = None) -> Any:
    if data is None or not isinstance(data, dict):
        return None
    return data.get(key, default)


def safe_list_access(data: Any, index: int, default: Any = None) -> Any:
    if not isinstance(data, list):
        return None
    if index < 0 or index >= len(data):
        return default
    return data[index]


def validate_json_data(data: Any) -> bool:
    return isinstance(data, (dict, list))


def validate_python_syntax(file_path: str) -> tuple[bool, Optional[str]]:
    path = Path(file_path)
    if not path.exists():
        return False, "File not found"
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, file_path, "exec")
        return True, None
    except SyntaxError as exc:
        return False, f"SyntaxError: {exc}"


def validate_project_syntax(project_root: Path) -> Dict[str, Any]:
    python_files = list(project_root.rglob("*.py"))
    errors: List[Dict[str, Any]] = []
    valid = 0
    invalid = 0
    for file_path in python_files:
        ok, error = validate_python_syntax(str(file_path))
        if ok:
            valid += 1
        else:
            invalid += 1
            errors.append({"file": str(file_path), "error": error})
    return {
        "total_files": len(python_files),
        "valid_files": valid,
        "invalid_files": invalid,
        "errors": errors,
    }
