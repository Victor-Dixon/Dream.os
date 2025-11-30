#!/usr/bin/env python3
"""
Unit tests for unified_import_system.py - Infrastructure Test Coverage

Tests UnifiedImportSystem class and delegation to core modules.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.unified_import_system import UnifiedImportSystem, get_unified_import_system


class TestUnifiedImportSystemInitialization:
    """Test suite for UnifiedImportSystem initialization."""

    def test_initialization(self):
        """Test system initialization."""
        system = UnifiedImportSystem()
        assert system is not None
        assert system._core is not None
        assert system._utilities is not None
        assert system._registry is not None
        assert system._logger is None

    def test_get_unified_import_system_singleton(self):
        """Test global singleton instance."""
        # Reset global
        import src.core.unified_import_system as mod
        mod._global_import_system = None
        
        system1 = get_unified_import_system()
        system2 = get_unified_import_system()
        
        assert system1 is system2
        assert isinstance(system1, UnifiedImportSystem)


class TestCoreImportDelegation:
    """Test suite for core import property delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance."""
        return UnifiedImportSystem()

    def test_os_property(self, system):
        """Test os module delegation."""
        assert system.os is not None
        import os
        assert system.os == os

    def test_sys_property(self, system):
        """Test sys module delegation."""
        assert system.sys is not None
        import sys
        assert system.sys == sys

    def test_json_property(self, system):
        """Test json module delegation."""
        assert system.json is not None
        import json
        assert system.json == json

    def test_logging_property(self, system):
        """Test logging module delegation."""
        assert system.logging is not None
        import logging
        assert system.logging == logging

    def test_threading_property(self, system):
        """Test threading module delegation."""
        assert system.threading is not None
        import threading
        assert system.threading == threading

    def test_time_property(self, system):
        """Test time module delegation."""
        assert system.time is not None
        import time
        assert system.time == time

    def test_re_property(self, system):
        """Test re module delegation."""
        assert system.re is not None
        import re
        assert system.re == re

    def test_datetime_property(self, system):
        """Test datetime class delegation."""
        assert system.datetime is not None
        from datetime import datetime
        assert system.datetime == datetime

    def test_path_property(self, system):
        """Test Path class delegation."""
        assert system.Path is not None
        from pathlib import Path
        assert system.Path == Path


class TestTypingImportDelegation:
    """Test suite for typing import property delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance."""
        return UnifiedImportSystem()

    def test_any_property(self, system):
        """Test Any type delegation."""
        assert system.Any is not None
        from typing import Any
        assert system.Any == Any

    def test_dict_property(self, system):
        """Test Dict type delegation."""
        assert system.Dict is not None
        # Note: Dict is actually 'dict' in newer Python versions
        assert system.Dict == dict

    def test_list_property(self, system):
        """Test List type delegation."""
        assert system.List is not None
        # Note: List is actually 'list' in newer Python versions
        assert system.List == list

    def test_optional_property(self, system):
        """Test Optional type delegation."""
        assert system.Optional is not None
        from typing import Optional
        assert system.Optional == Optional

    def test_union_property(self, system):
        """Test Union type delegation."""
        assert system.Union is not None
        from typing import Union
        assert system.Union == Union

    def test_callable_property(self, system):
        """Test Callable type delegation."""
        assert system.Callable is not None
        from collections.abc import Callable
        assert system.Callable == Callable

    def test_tuple_property(self, system):
        """Test Tuple type delegation."""
        assert system.Tuple is not None
        # Note: Tuple is actually 'tuple' in newer Python versions
        assert system.Tuple == tuple


class TestDataclassImportDelegation:
    """Test suite for dataclass import property delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance."""
        return UnifiedImportSystem()

    def test_dataclass_property(self, system):
        """Test dataclass decorator delegation."""
        assert system.dataclass is not None
        from dataclasses import dataclass
        assert system.dataclass == dataclass

    def test_field_property(self, system):
        """Test field function delegation."""
        assert system.field is not None
        from dataclasses import field
        assert system.field == field


class TestEnumImportDelegation:
    """Test suite for enum import property delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance."""
        return UnifiedImportSystem()

    def test_enum_property(self, system):
        """Test Enum class delegation."""
        assert system.Enum is not None
        from enum import Enum
        assert system.Enum == Enum


class TestABCImportDelegation:
    """Test suite for ABC import property delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance."""
        return UnifiedImportSystem()

    def test_abc_property(self, system):
        """Test ABC class delegation."""
        assert system.ABC is not None
        from abc import ABC
        assert system.ABC == ABC

    def test_abstractmethod_property(self, system):
        """Test abstractmethod decorator delegation."""
        assert system.abstractmethod is not None
        from abc import abstractmethod
        assert system.abstractmethod == abstractmethod


class TestUtilityMethodDelegation:
    """Test suite for utility method delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance with mocked utilities."""
        system = UnifiedImportSystem()
        system._utilities = MagicMock()
        return system

    def test_get_module_path(self, system):
        """Test get_module_path delegation."""
        system._utilities.get_module_path.return_value = "/path/to/module"
        result = system.get_module_path("test_module")
        system._utilities.get_module_path.assert_called_once_with("test_module")
        assert result == "/path/to/module"

    def test_is_module_available(self, system):
        """Test is_module_available delegation."""
        system._utilities.is_module_available.return_value = True
        result = system.is_module_available("test_module")
        system._utilities.is_module_available.assert_called_once_with("test_module")
        assert result is True

    def test_get_import_path(self, system):
        """Test get_import_path delegation."""
        system._utilities.get_import_path.return_value = "test.path"
        result = system.get_import_path("test_module")
        system._utilities.get_import_path.assert_called_once_with("test_module")
        assert result == "test.path"

    def test_resolve_relative_import(self, system):
        """Test resolve_relative_import delegation."""
        system._utilities.resolve_relative_import.return_value = "resolved.path"
        result = system.resolve_relative_import("base", "relative")
        system._utilities.resolve_relative_import.assert_called_once_with("base", "relative")
        assert result == "resolved.path"

    def test_get_package_root(self, system):
        """Test get_package_root delegation."""
        system._utilities.get_package_root.return_value = "/package/root"
        result = system.get_package_root("test_module")
        system._utilities.get_package_root.assert_called_once_with("test_module")
        assert result == "/package/root"

    def test_list_module_contents(self, system):
        """Test list_module_contents delegation."""
        system._utilities.list_module_contents.return_value = ["item1", "item2"]
        result = system.list_module_contents("test_module")
        system._utilities.list_module_contents.assert_called_once_with("test_module")
        assert result == ["item1", "item2"]

    def test_get_module_docstring(self, system):
        """Test get_module_docstring delegation."""
        system._utilities.get_module_docstring.return_value = "Test docstring"
        result = system.get_module_docstring("test_module")
        system._utilities.get_module_docstring.assert_called_once_with("test_module")
        assert result == "Test docstring"

    def test_validate_import_syntax(self, system):
        """Test validate_import_syntax delegation."""
        system._utilities.validate_import_syntax.return_value = True
        result = system.validate_import_syntax("import os")
        system._utilities.validate_import_syntax.assert_called_once_with("import os")
        assert result is True

    def test_get_import_dependencies(self, system):
        """Test get_import_dependencies delegation."""
        system._utilities.get_import_dependencies.return_value = ["dep1", "dep2"]
        result = system.get_import_dependencies("test_module")
        system._utilities.get_import_dependencies.assert_called_once_with("test_module")
        assert result == ["dep1", "dep2"]

    def test_create_import_alias(self, system):
        """Test create_import_alias delegation."""
        system._utilities.create_import_alias.return_value = "import os as sys"
        result = system.create_import_alias("os", "sys")
        system._utilities.create_import_alias.assert_called_once_with("os", "sys")
        assert result == "import os as sys"

    def test_create_from_import(self, system):
        """Test create_from_import delegation."""
        system._utilities.create_from_import.return_value = "from os import path"
        result = system.create_from_import("os", "path")
        system._utilities.create_from_import.assert_called_once_with("os", "path", None)
        assert result == "from os import path"

    def test_create_from_import_with_alias(self, system):
        """Test create_from_import with alias delegation."""
        system._utilities.create_from_import.return_value = "from os import path as p"
        result = system.create_from_import("os", "path", "p")
        system._utilities.create_from_import.assert_called_once_with("os", "path", "p")
        assert result == "from os import path as p"


class TestRegistryMethodDelegation:
    """Test suite for registry method delegation."""

    @pytest.fixture
    def system(self):
        """Create UnifiedImportSystem instance with mocked registry."""
        system = UnifiedImportSystem()
        system._registry = MagicMock()
        return system

    def test_register_import(self, system):
        """Test register_import delegation."""
        system.register_import("test", "value")
        system._registry.register_import.assert_called_once_with("test", "value")

    def test_get_import(self, system):
        """Test get_import delegation."""
        system._registry.get_import.return_value = "value"
        result = system.get_import("test")
        system._registry.get_import.assert_called_once_with("test")
        assert result == "value"

    def test_has_import(self, system):
        """Test has_import delegation."""
        system._registry.has_import.return_value = True
        result = system.has_import("test")
        system._registry.has_import.assert_called_once_with("test")
        assert result is True

    def test_remove_import(self, system):
        """Test remove_import delegation."""
        system._registry.remove_import.return_value = True
        result = system.remove_import("test")
        system._registry.remove_import.assert_called_once_with("test")
        assert result is True

    def test_clear_cache(self, system):
        """Test clear_cache delegation."""
        system.clear_cache()
        system._registry.clear_cache.assert_called_once()

    def test_get_cache_stats(self, system):
        """Test get_cache_stats delegation."""
        system._registry.get_cache_stats.return_value = {"count": 10}
        result = system.get_cache_stats()
        system._registry.get_cache_stats.assert_called_once()
        assert result == {"count": 10}

    def test_mark_failed_import(self, system):
        """Test mark_failed_import delegation."""
        system.mark_failed_import("test")
        system._registry.mark_failed_import.assert_called_once_with("test")

    def test_is_failed_import(self, system):
        """Test is_failed_import delegation."""
        system._registry.is_failed_import.return_value = True
        result = system.is_failed_import("test")
        system._registry.is_failed_import.assert_called_once_with("test")
        assert result is True

    def test_clear_failed_imports(self, system):
        """Test clear_failed_imports delegation."""
        system.clear_failed_imports()
        system._registry.clear_failed_imports.assert_called_once()

    def test_get_import_history(self, system):
        """Test get_import_history delegation."""
        system._registry.get_import_history.return_value = ["import1", "import2"]
        result = system.get_import_history(limit=10)
        system._registry.get_import_history.assert_called_once_with(10)
        assert result == ["import1", "import2"]

    def test_cleanup_old_imports(self, system):
        """Test cleanup_old_imports delegation."""
        system._registry.cleanup_old_imports.return_value = 5
        result = system.cleanup_old_imports(max_age_hours=24)
        system._registry.cleanup_old_imports.assert_called_once_with(24)
        assert result == 5

    def test_get_import_patterns(self, system):
        """Test get_import_patterns delegation."""
        system._registry.get_import_patterns.return_value = ["pattern1", "pattern2"]
        result = system.get_import_patterns()
        system._registry.get_import_patterns.assert_called_once()
        assert result == ["pattern1", "pattern2"]

    def test_validate_import_pattern(self, system):
        """Test validate_import_pattern delegation."""
        system._registry.validate_import_pattern.return_value = True
        result = system.validate_import_pattern("pattern")
        system._registry.validate_import_pattern.assert_called_once_with("pattern")
        assert result is True

