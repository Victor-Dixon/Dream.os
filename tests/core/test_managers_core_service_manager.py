"""
Unit tests for core_service_manager.py - MEDIUM PRIORITY

Tests CoreServiceManager class (wrapper for CoreServiceCoordinator).
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_service_manager import CoreServiceManager


class TestCoreServiceManager:
    """Test suite for CoreServiceManager class."""

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    @pytest.fixture
    def manager(self):
        """Create CoreServiceManager instance (wrapper for CoreServiceCoordinator)."""
        with patch('src.core.managers.core_service_manager.CoreServiceCoordinator') as mock_coord_class:
            mock_coord = MagicMock()
            mock_coord_class.return_value = mock_coord
            manager = CoreServiceManager()
            # Since it's a wrapper, we can test it directly
            return manager

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert isinstance(manager, CoreServiceManager)

    def test_manager_is_wrapper(self):
        """Test that CoreServiceManager is a wrapper for CoreServiceCoordinator."""
        from src.core.managers.core_service_coordinator import CoreServiceCoordinator
        assert issubclass(CoreServiceManager, CoreServiceCoordinator)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

