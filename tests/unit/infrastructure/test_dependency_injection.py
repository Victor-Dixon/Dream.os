"""
Tests for Dependency Injection Container - Infrastructure Domain

Tests for dependency injection container that wires domain ports to infrastructure.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.dependency_injection import get_dependencies


class TestDependencyInjection:
    """Tests for dependency injection container."""

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_returns_dict(self, mock_message_bus):
        """Test get_dependencies returns dictionary of dependencies."""
        # Mock SimpleMessageBus to avoid abstract class instantiation
        mock_message_bus.return_value = MagicMock()
        deps = get_dependencies()
        assert isinstance(deps, dict)
        assert "task_repository" in deps
        assert "agent_repository" in deps
        assert "message_bus" in deps
        assert "logger" in deps
        assert "assignment_service" in deps

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_returns_singleton_instances(self, mock_message_bus):
        """Test get_dependencies returns same instances on multiple calls."""
        mock_message_bus.return_value = MagicMock()
        deps1 = get_dependencies()
        deps2 = get_dependencies()
        assert deps1["task_repository"] is deps2["task_repository"]
        assert deps1["agent_repository"] is deps2["agent_repository"]
        assert deps1["message_bus"] is deps2["message_bus"]
        assert deps1["logger"] is deps2["logger"]
        assert deps1["assignment_service"] is deps2["assignment_service"]

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_task_repository(self, mock_message_bus):
        """Test task_repository dependency is available."""
        mock_message_bus.return_value = MagicMock()
        deps = get_dependencies()
        task_repo = deps["task_repository"]
        assert task_repo is not None

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_agent_repository(self, mock_message_bus):
        """Test agent_repository dependency is available."""
        mock_message_bus.return_value = MagicMock()
        deps = get_dependencies()
        agent_repo = deps["agent_repository"]
        assert agent_repo is not None

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_message_bus(self, mock_message_bus):
        """Test message_bus dependency is available."""
        mock_message_bus.return_value = MagicMock()
        deps = get_dependencies()
        message_bus = deps["message_bus"]
        assert message_bus is not None

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_logger(self, mock_message_bus):
        """Test logger dependency is available."""
        mock_message_bus.return_value = MagicMock()
        deps = get_dependencies()
        logger = deps["logger"]
        assert logger is not None

    @patch('src.infrastructure.dependency_injection.SimpleMessageBus')
    def test_get_dependencies_assignment_service(self, mock_message_bus):
        """Test assignment_service dependency is available."""
        mock_message_bus.return_value = MagicMock()
        deps = get_dependencies()
        assignment_service = deps["assignment_service"]
        assert assignment_service is not None

