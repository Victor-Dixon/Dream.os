"""
Test coverage for shared_utilities.py - Captain Work
Created: 2025-11-28
Agent: Agent-4 (Captain)
Perpetual Motion Cycle - Batch 9
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.shared_utilities import (
    BaseUtility,
    CleanupManager,
    ConfigurationManager,
    ErrorHandler,
    InitializationManager,
    LoggingManager,
    ResultManager,
    StatusManager,
    ValidationManager,
    create_cleanup_manager,
    create_configuration_manager,
    create_error_handler,
    create_initialization_manager,
    create_logging_manager,
    create_result_manager,
    create_status_manager,
    create_validation_manager
)


class TestBaseUtility:
    """Test suite for BaseUtility - 3+ tests"""

    def test_base_utility_abstract(self):
        """Test BaseUtility is abstract and cannot be instantiated"""
        with pytest.raises(TypeError):
            BaseUtility()

    def test_base_utility_subclass_initialization(self):
        """Test BaseUtility subclass initialization"""
        class TestUtility(BaseUtility):
            def initialize(self):
                return True
            def cleanup(self):
                return True
        
        util = TestUtility()
        assert util.name == "TestUtility"
        assert util.logger is not None

    def test_base_utility_custom_name(self):
        """Test BaseUtility with custom name"""
        class TestUtility(BaseUtility):
            def initialize(self):
                return True
            def cleanup(self):
                return True
        
        util = TestUtility(name="CustomName")
        assert util.name == "CustomName"


class TestCleanupManager:
    """Test suite for CleanupManager - 5+ tests"""

    def test_cleanup_manager_initialization(self):
        """Test CleanupManager initialization"""
        manager = CleanupManager()
        assert manager.cleanup_handlers == []

    def test_cleanup_manager_initialize(self):
        """Test CleanupManager initialize"""
        manager = CleanupManager()
        result = manager.initialize()
        assert result is True

    def test_cleanup_manager_register_handler(self):
        """Test CleanupManager register_handler"""
        manager = CleanupManager()
        handler = Mock()
        manager.register_handler(handler)
        assert len(manager.cleanup_handlers) == 1

    def test_cleanup_manager_cleanup_success(self):
        """Test CleanupManager cleanup executes handlers"""
        manager = CleanupManager()
        handler1 = Mock()
        handler2 = Mock()
        manager.register_handler(handler1)
        manager.register_handler(handler2)
        result = manager.cleanup()
        assert result is True
        handler1.assert_called_once()
        handler2.assert_called_once()
        assert len(manager.cleanup_handlers) == 0

    def test_cleanup_manager_cleanup_failure(self):
        """Test CleanupManager cleanup handles handler failures"""
        manager = CleanupManager()
        handler = Mock(side_effect=Exception("Test error"))
        manager.register_handler(handler)
        result = manager.cleanup()
        assert result is False
        assert len(manager.cleanup_handlers) == 0


class TestConfigurationManager:
    """Test suite for ConfigurationManager - 5+ tests"""

    def test_configuration_manager_initialization(self):
        """Test ConfigurationManager initialization"""
        manager = ConfigurationManager()
        assert manager.config == {}

    def test_configuration_manager_set_get_config(self):
        """Test ConfigurationManager set/get config"""
        manager = ConfigurationManager()
        manager.set_config("key", "value")
        assert manager.get_config("key") == "value"

    def test_configuration_manager_get_config_default(self):
        """Test ConfigurationManager get_config with default"""
        manager = ConfigurationManager()
        assert manager.get_config("missing", "default") == "default"

    def test_configuration_manager_cleanup(self):
        """Test ConfigurationManager cleanup"""
        manager = ConfigurationManager()
        manager.set_config("key", "value")
        result = manager.cleanup()
        assert result is True
        assert manager.config == {}


class TestErrorHandler:
    """Test suite for ErrorHandler - 4+ tests"""

    def test_error_handler_initialization(self):
        """Test ErrorHandler initialization"""
        handler = ErrorHandler()
        assert handler.error_count == 0
        assert handler.last_error is None

    def test_error_handler_handle_error(self):
        """Test ErrorHandler handle_error"""
        handler = ErrorHandler()
        error = ValueError("Test error")
        result = handler.handle_error(error, "test_context")
        assert result is True
        assert handler.error_count == 1
        assert handler.last_error == error

    def test_error_handler_get_error_summary(self):
        """Test ErrorHandler get_error_summary"""
        handler = ErrorHandler()
        error = ValueError("Test error")
        handler.handle_error(error)
        summary = handler.get_error_summary()
        assert summary["error_count"] == 1
        assert "Test error" in str(summary["last_error"])

    def test_error_handler_cleanup(self):
        """Test ErrorHandler cleanup"""
        handler = ErrorHandler()
        handler.handle_error(ValueError("Test"))
        result = handler.cleanup()
        assert result is True
        assert handler.error_count == 0
        assert handler.last_error is None


class TestInitializationManager:
    """Test suite for InitializationManager - 4+ tests"""

    def test_initialization_manager_initialization(self):
        """Test InitializationManager initialization"""
        manager = InitializationManager()
        assert manager.initialized is False

    def test_initialization_manager_initialize(self):
        """Test InitializationManager initialize"""
        manager = InitializationManager()
        result = manager.initialize()
        assert result is True
        assert manager.initialized is True
        assert manager.init_time is not None

    def test_initialization_manager_is_initialized(self):
        """Test InitializationManager is_initialized"""
        manager = InitializationManager()
        assert manager.is_initialized() is False
        manager.initialize()
        assert manager.is_initialized() is True

    def test_initialization_manager_cleanup(self):
        """Test InitializationManager cleanup"""
        manager = InitializationManager()
        manager.initialize()
        result = manager.cleanup()
        assert result is True
        assert manager.initialized is False


class TestLoggingManager:
    """Test suite for LoggingManager - 4+ tests"""

    def test_logging_manager_initialization(self):
        """Test LoggingManager initialization"""
        manager = LoggingManager()
        assert manager.log_level is not None

    def test_logging_manager_set_log_level(self):
        """Test LoggingManager set_log_level"""
        manager = LoggingManager()
        manager.set_log_level(10)  # DEBUG
        assert manager.log_level == 10

    def test_logging_manager_log_info(self):
        """Test LoggingManager log_info"""
        manager = LoggingManager()
        manager.log_info("Test message")  # Should not raise

    def test_logging_manager_log_error(self):
        """Test LoggingManager log_error"""
        manager = LoggingManager()
        manager.log_error("Test error")  # Should not raise


class TestResultManager:
    """Test suite for ResultManager - 5+ tests"""

    def test_result_manager_initialization(self):
        """Test ResultManager initialization"""
        manager = ResultManager()
        assert manager.results == []
        assert manager.last_result is None

    def test_result_manager_add_result(self):
        """Test ResultManager add_result"""
        manager = ResultManager()
        manager.add_result("result1")
        assert len(manager.results) == 1
        assert manager.last_result == "result1"

    def test_result_manager_get_results(self):
        """Test ResultManager get_results"""
        manager = ResultManager()
        manager.add_result("result1")
        manager.add_result("result2")
        results = manager.get_results()
        assert results == ["result1", "result2"]
        assert results is not manager.results  # Should be copy

    def test_result_manager_get_last_result(self):
        """Test ResultManager get_last_result"""
        manager = ResultManager()
        assert manager.get_last_result() is None
        manager.add_result("result1")
        assert manager.get_last_result() == "result1"

    def test_result_manager_cleanup(self):
        """Test ResultManager cleanup"""
        manager = ResultManager()
        manager.add_result("result1")
        result = manager.cleanup()
        assert result is True
        assert manager.results == []
        assert manager.last_result is None


class TestStatusManager:
    """Test suite for StatusManager - 5+ tests"""

    def test_status_manager_initialization(self):
        """Test StatusManager initialization"""
        manager = StatusManager()
        assert manager.status == "initialized"
        assert len(manager.status_history) == 0

    def test_status_manager_set_status(self):
        """Test StatusManager set_status"""
        manager = StatusManager()
        manager.set_status("active")
        assert manager.status == "active"
        assert len(manager.status_history) == 1

    def test_status_manager_get_status(self):
        """Test StatusManager get_status"""
        manager = StatusManager()
        manager.set_status("active")
        assert manager.get_status() == "active"

    def test_status_manager_get_status_history(self):
        """Test StatusManager get_status_history"""
        manager = StatusManager()
        manager.set_status("active")
        manager.set_status("inactive")
        history = manager.get_status_history()
        assert len(history) == 2
        assert history is not manager.status_history  # Should be copy

    def test_status_manager_cleanup(self):
        """Test StatusManager cleanup"""
        manager = StatusManager()
        manager.set_status("active")
        result = manager.cleanup()
        assert result is True
        assert len(manager.status_history) == 0


class TestValidationManager:
    """Test suite for ValidationManager - 5+ tests"""

    def test_validation_manager_initialization(self):
        """Test ValidationManager initialization"""
        manager = ValidationManager()
        assert manager.validation_rules == {}
        assert manager.validation_results == []

    def test_validation_manager_add_validation_rule(self):
        """Test ValidationManager add_validation_rule"""
        manager = ValidationManager()
        rule = lambda x: x > 0
        manager.add_validation_rule("positive", rule)
        assert "positive" in manager.validation_rules

    def test_validation_manager_validate(self):
        """Test ValidationManager validate"""
        manager = ValidationManager()
        manager.add_validation_rule("positive", lambda x: x > 0)
        results = manager.validate(5)
        assert results["positive"] is True

    def test_validation_manager_validate_failure(self):
        """Test ValidationManager validate with failure"""
        manager = ValidationManager()
        manager.add_validation_rule("positive", lambda x: x > 0)
        results = manager.validate(-5)
        assert results["positive"] is False

    def test_validation_manager_get_validation_results(self):
        """Test ValidationManager get_validation_results"""
        manager = ValidationManager()
        manager.add_validation_rule("positive", lambda x: x > 0)
        manager.validate(5)
        results = manager.get_validation_results()
        assert len(results) == 1
        assert results is not manager.validation_results  # Should be copy


class TestFactoryFunctions:
    """Test suite for factory functions - 8+ tests"""

    def test_create_cleanup_manager(self):
        """Test create_cleanup_manager"""
        manager = create_cleanup_manager()
        assert isinstance(manager, CleanupManager)

    def test_create_configuration_manager(self):
        """Test create_configuration_manager"""
        manager = create_configuration_manager()
        assert isinstance(manager, ConfigurationManager)

    def test_create_error_handler(self):
        """Test create_error_handler"""
        handler = create_error_handler()
        assert isinstance(handler, ErrorHandler)

    def test_create_initialization_manager(self):
        """Test create_initialization_manager"""
        manager = create_initialization_manager()
        assert isinstance(manager, InitializationManager)

    def test_create_logging_manager(self):
        """Test create_logging_manager"""
        manager = create_logging_manager()
        assert isinstance(manager, LoggingManager)

    def test_create_result_manager(self):
        """Test create_result_manager"""
        manager = create_result_manager()
        assert isinstance(manager, ResultManager)

    def test_create_status_manager(self):
        """Test create_status_manager"""
        manager = create_status_manager()
        assert isinstance(manager, StatusManager)

    def test_create_validation_manager(self):
        """Test create_validation_manager"""
        manager = create_validation_manager()
        assert isinstance(manager, ValidationManager)

