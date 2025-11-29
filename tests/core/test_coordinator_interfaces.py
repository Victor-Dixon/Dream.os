"""
Tests for coordinator_interfaces.py

Tests for Protocol-based interfaces and abstract base classes.
"""

import pytest
from typing import Any, Dict
from unittest.mock import MagicMock
from src.core.coordinator_interfaces import (
    ICoordinatorLogger,
    ICoordinator,
    ICoordinatorRegistry,
    ICoordinatorStatusParser,
)


class TestICoordinatorLogger:
    """Tests for ICoordinatorLogger Protocol."""

    def test_protocol_implementation(self):
        """Test that a class implementing the protocol works."""
        class MockLogger:
            def info(self, message: str) -> None:
                pass

            def warning(self, message: str) -> None:
                pass

            def error(self, message: str) -> None:
                pass

        logger = MockLogger()
        # Protocol check - should not raise
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_protocol_methods_callable(self):
        """Test protocol methods are callable."""
        logger = MagicMock(spec=["info", "warning", "error"])
        logger.info("test")
        logger.warning("test")
        logger.error("test")
        logger.info.assert_called_once_with("test")
        logger.warning.assert_called_once_with("test")
        logger.error.assert_called_once_with("test")


class TestICoordinator:
    """Tests for ICoordinator Protocol."""

    def test_protocol_implementation(self):
        """Test that a class implementing the protocol works."""
        class MockCoordinator:
            @property
            def name(self) -> str:
                return "test_coordinator"

            def get_status(self) -> Dict[str, Any]:
                return {"status": "operational"}

            def shutdown(self) -> None:
                pass

        coordinator = MockCoordinator()
        assert coordinator.name == "test_coordinator"
        assert coordinator.get_status() == {"status": "operational"}
        coordinator.shutdown()  # Should not raise

    def test_protocol_property_access(self):
        """Test protocol property access."""
        coordinator = MagicMock(spec=["name", "get_status", "shutdown"])
        coordinator.name = "test_coordinator"
        assert coordinator.name == "test_coordinator"

    def test_protocol_methods_callable(self):
        """Test protocol methods are callable."""
        coordinator = MagicMock(spec=["name", "get_status", "shutdown"])
        coordinator.get_status.return_value = {"status": "operational"}
        result = coordinator.get_status()
        assert result == {"status": "operational"}
        coordinator.shutdown()
        coordinator.shutdown.assert_called_once()


class TestICoordinatorRegistry:
    """Tests for ICoordinatorRegistry abstract base class."""

    def test_abstract_class_cannot_be_instantiated(self):
        """Test that abstract class cannot be instantiated."""
        with pytest.raises(TypeError):
            ICoordinatorRegistry()

    def test_concrete_implementation(self):
        """Test concrete implementation of registry."""
        class MockCoordinatorRegistry(ICoordinatorRegistry):
            def __init__(self):
                self._coordinators: Dict[str, Any] = {}

            def register_coordinator(self, coordinator: Any) -> bool:
                if hasattr(coordinator, "name"):
                    self._coordinators[coordinator.name] = coordinator
                    return True
                return False

            def get_coordinator(self, name: str) -> Any:
                return self._coordinators.get(name)

            def get_all_coordinators(self) -> Dict[str, Any]:
                return self._coordinators.copy()

            def unregister_coordinator(self, name: str) -> bool:
                if name in self._coordinators:
                    del self._coordinators[name]
                    return True
                return False

            def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
                return {
                    name: coord.get_status() if hasattr(coord, "get_status") else {}
                    for name, coord in self._coordinators.items()
                }

            def shutdown_all_coordinators(self) -> None:
                for coord in self._coordinators.values():
                    if hasattr(coord, "shutdown"):
                        coord.shutdown()
                self._coordinators.clear()

            def get_coordinator_count(self) -> int:
                return len(self._coordinators)

        registry = MockCoordinatorRegistry()
        assert registry.get_coordinator_count() == 0

        # Test register
        coord = MagicMock()
        coord.name = "test_coordinator"
        coord.get_status.return_value = {"status": "operational"}
        assert registry.register_coordinator(coord) is True
        assert registry.get_coordinator_count() == 1

        # Test get
        retrieved = registry.get_coordinator("test_coordinator")
        assert retrieved == coord

        # Test get all
        all_coords = registry.get_all_coordinators()
        assert len(all_coords) == 1
        assert "test_coordinator" in all_coords

        # Test get statuses
        statuses = registry.get_coordinator_statuses()
        assert "test_coordinator" in statuses
        assert statuses["test_coordinator"] == {"status": "operational"}

        # Test unregister
        assert registry.unregister_coordinator("test_coordinator") is True
        assert registry.get_coordinator_count() == 0

        # Test shutdown all
        registry.register_coordinator(coord)
        registry.shutdown_all_coordinators()
        assert registry.get_coordinator_count() == 0
        coord.shutdown.assert_called_once()

    def test_register_coordinator_returns_bool(self):
        """Test register_coordinator returns bool."""
        class TestRegistry(ICoordinatorRegistry):
            def register_coordinator(self, coordinator: Any) -> bool:
                return True

            def get_coordinator(self, name: str) -> Any:
                return None

            def get_all_coordinators(self) -> Dict[str, Any]:
                return {}

            def unregister_coordinator(self, name: str) -> bool:
                return False

            def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
                return {}

            def shutdown_all_coordinators(self) -> None:
                pass

            def get_coordinator_count(self) -> int:
                return 0

        registry = TestRegistry()
        assert isinstance(registry.register_coordinator(MagicMock()), bool)

    def test_get_coordinator_returns_optional(self):
        """Test get_coordinator returns Optional[Any]."""
        class TestRegistry(ICoordinatorRegistry):
            def register_coordinator(self, coordinator: Any) -> bool:
                return True

            def get_coordinator(self, name: str) -> Any:
                return None

            def get_all_coordinators(self) -> Dict[str, Any]:
                return {}

            def unregister_coordinator(self, name: str) -> bool:
                return False

            def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
                return {}

            def shutdown_all_coordinators(self) -> None:
                pass

            def get_coordinator_count(self) -> int:
                return 0

        registry = TestRegistry()
        result = registry.get_coordinator("test")
        assert result is None


class TestICoordinatorStatusParser:
    """Tests for ICoordinatorStatusParser Protocol."""

    def test_protocol_implementation(self):
        """Test that a class implementing the protocol works."""
        class MockStatusParser:
            def parse_status(self, coordinator: Any) -> Dict[str, Any]:
                return {"status": "parsed"}

            def can_parse_status(self, coordinator: Any) -> bool:
                return hasattr(coordinator, "get_status")

        parser = MockStatusParser()
        coord = MagicMock()
        coord.get_status.return_value = {"status": "operational"}
        assert parser.can_parse_status(coord) is True
        assert parser.parse_status(coord) == {"status": "parsed"}

    def test_protocol_methods_callable(self):
        """Test protocol methods are callable."""
        parser = MagicMock(spec=["parse_status", "can_parse_status"])
        parser.parse_status.return_value = {"status": "parsed"}
        parser.can_parse_status.return_value = True

        coord = MagicMock()
        result = parser.parse_status(coord)
        assert result == {"status": "parsed"}
        can_parse = parser.can_parse_status(coord)
        assert can_parse is True

        parser.parse_status.assert_called_once_with(coord)
        parser.can_parse_status.assert_called_once_with(coord)

    def test_can_parse_status_returns_false(self):
        """Test can_parse_status returns False for invalid coordinator."""
        class MockStatusParser:
            def parse_status(self, coordinator: Any) -> Dict[str, Any]:
                return {"status": "parsed"}

            def can_parse_status(self, coordinator: Any) -> bool:
                return False

        parser = MockStatusParser()
        coord = MagicMock()
        assert parser.can_parse_status(coord) is False

    def test_protocol_with_missing_method_raises_attribute_error(self):
        """Test that missing protocol methods raise AttributeError."""
        class IncompleteLogger:
            def info(self, message: str) -> None:
                pass
            # Missing warning and error methods

        logger = IncompleteLogger()
        assert hasattr(logger, "info")
        assert not hasattr(logger, "warning")
        assert not hasattr(logger, "error")

    def test_coordinator_registry_all_methods_implemented(self):
        """Test that all registry methods are properly implemented."""
        class CompleteRegistry(ICoordinatorRegistry):
            def __init__(self):
                self._coordinators: Dict[str, Any] = {}

            def register_coordinator(self, coordinator: Any) -> bool:
                if hasattr(coordinator, "name"):
                    self._coordinators[coordinator.name] = coordinator
                    return True
                return False

            def get_coordinator(self, name: str) -> Any:
                return self._coordinators.get(name)

            def get_all_coordinators(self) -> Dict[str, Any]:
                return self._coordinators.copy()

            def unregister_coordinator(self, name: str) -> bool:
                return name in self._coordinators and self._coordinators.pop(name, None) is not None

            def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
                return {
                    name: coord.get_status() if hasattr(coord, "get_status") else {}
                    for name, coord in self._coordinators.items()
                }

            def shutdown_all_coordinators(self) -> None:
                for coord in list(self._coordinators.values()):
                    if hasattr(coord, "shutdown"):
                        coord.shutdown()
                self._coordinators.clear()

            def get_coordinator_count(self) -> int:
                return len(self._coordinators)

        registry = CompleteRegistry()
        coord1 = MagicMock()
        coord1.name = "coord1"
        coord1.get_status.return_value = {"status": "ok"}
        coord1.shutdown = MagicMock()

        coord2 = MagicMock()
        coord2.name = "coord2"
        coord2.get_status.return_value = {"status": "ok"}

        # Test register
        assert registry.register_coordinator(coord1) is True
        assert registry.register_coordinator(coord2) is True
        assert registry.get_coordinator_count() == 2

        # Test get
        assert registry.get_coordinator("coord1") == coord1
        assert registry.get_coordinator("nonexistent") is None

        # Test get all
        all_coords = registry.get_all_coordinators()
        assert len(all_coords) == 2

        # Test get statuses
        statuses = registry.get_coordinator_statuses()
        assert len(statuses) == 2
        assert statuses["coord1"] == {"status": "ok"}

        # Test unregister
        assert registry.unregister_coordinator("coord1") is True
        assert registry.get_coordinator_count() == 1
        assert registry.unregister_coordinator("nonexistent") is False

        # Test shutdown all - re-register coord1 to test shutdown
        registry.register_coordinator(coord1)
        coord1.shutdown.reset_mock()  # Reset call count
        registry.shutdown_all_coordinators()
        assert registry.get_coordinator_count() == 0
        coord1.shutdown.assert_called_once()

    def test_coordinator_registry_register_without_name(self):
        """Test registering coordinator without name attribute."""
        class TestRegistry(ICoordinatorRegistry):
            def __init__(self):
                self._coordinators: Dict[str, Any] = {}

            def register_coordinator(self, coordinator: Any) -> bool:
                return False  # No name attribute

            def get_coordinator(self, name: str) -> Any:
                return None

            def get_all_coordinators(self) -> Dict[str, Any]:
                return {}

            def unregister_coordinator(self, name: str) -> bool:
                return False

            def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
                return {}

            def shutdown_all_coordinators(self) -> None:
                pass

            def get_coordinator_count(self) -> int:
                return 0

        registry = TestRegistry()
        coord = MagicMock()
        del coord.name  # Remove name attribute
        assert registry.register_coordinator(coord) is False

