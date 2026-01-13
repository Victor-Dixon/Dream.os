"""
Trading Robot Broker Factory
============================

<<<<<<< HEAD
<<<<<<< HEAD
<!-- SSOT Domain: trading_robot -->

=======
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
<!-- SSOT Domain: trading_robot -->

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
Provides broker factory for trading operations.

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-04
"""

import logging
<<<<<<< HEAD
<<<<<<< HEAD
import importlib
from typing import Optional, Dict, Any, Tuple
=======
from typing import Optional, Dict, Any
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
import importlib
from typing import Optional, Dict, Any, Tuple
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BrokerInterface(ABC):
    """Abstract interface for trading brokers."""

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the broker."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the broker."""
        pass

    @abstractmethod
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        pass

    @abstractmethod
    def place_order(self, symbol: str, quantity: int, order_type: str, **kwargs) -> Dict[str, Any]:
        """Place a trading order."""
        pass


class MockBroker(BrokerInterface):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    """
    Mock broker implementation for testing (PHASE 4 CONSOLIDATION).

    Provides demo balance data for safe development and testing.
    This is the OFFICIAL mock implementation - all others should use this.
    """
<<<<<<< HEAD
=======
    """Mock broker implementation for testing."""
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    def __init__(self):
        self.connected = False

    def connect(self) -> bool:
        self.connected = True
        logger.info("Mock broker connected")
        return True

    def disconnect(self) -> None:
        self.connected = False
        logger.info("Mock broker disconnected")

    def get_account_info(self) -> Dict[str, Any]:
<<<<<<< HEAD
<<<<<<< HEAD
        """Get mock account info (consolidated format for Phase 4)."""
        return {
            "balance": 10000.0,
            "cash": 10000.0,  # Added for compatibility
            "portfolio_value": 10000.0,  # Added for compatibility
            "buying_power": 10000.0,  # Added for compatibility
            "currency": "USD",
            "account_type": "demo",
            "status": "active",
            "data_source": "mock_demo",  # Marks as mock data
            "consolidated": True  # Phase 4 consolidation marker
=======
=======
        """Get mock account info (consolidated format for Phase 4)."""
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        return {
            "balance": 10000.0,
            "cash": 10000.0,  # Added for compatibility
            "portfolio_value": 10000.0,  # Added for compatibility
            "buying_power": 10000.0,  # Added for compatibility
            "currency": "USD",
<<<<<<< HEAD
            "account_type": "demo"
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
            "account_type": "demo",
            "status": "active",
            "data_source": "mock_demo",  # Marks as mock data
            "consolidated": True  # Phase 4 consolidation marker
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        }

    def place_order(self, symbol: str, quantity: int, order_type: str, **kwargs) -> Dict[str, Any]:
        return {
            "order_id": f"mock_{symbol}_{quantity}",
            "status": "filled",
            "symbol": symbol,
            "quantity": quantity,
            "type": order_type
        }


class BrokerFactory:
    """Factory for creating broker instances."""

    _brokers = {
        "mock": MockBroker,
    }

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # Dynamic imports for safety (Robinhood loaded only when requested)
    _dynamic_brokers = {
        "robinhood": ("src.trading_robot.core.robinhood_broker", "RobinhoodBroker"),
    }

<<<<<<< HEAD
=======
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    @classmethod
    def create_broker(cls, broker_type: str = "mock", **kwargs) -> Optional[BrokerInterface]:
        """
        Create a broker instance.

        Args:
            broker_type: Type of broker to create
            **kwargs: Additional broker configuration

        Returns:
            Broker instance or None if broker type not supported
        """
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        # Check static brokers first
        if broker_type in cls._brokers:
            broker_class = cls._brokers[broker_type]
        # Check dynamic brokers (for safety - Robinhood loaded on demand)
        elif broker_type in cls._dynamic_brokers:
            try:
                module_path, class_name = cls._dynamic_brokers[broker_type]
                module = importlib.import_module(module_path)
                broker_class = getattr(module, class_name)
                logger.info(f"Dynamically loaded {broker_type} broker")
            except Exception as e:
                logger.error(f"Failed to dynamically load {broker_type} broker: {e}")
                return None
        else:
<<<<<<< HEAD
=======
        if broker_type not in cls._brokers:
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            logger.warning(f"Unsupported broker type: {broker_type}")
            return None

        try:
<<<<<<< HEAD
<<<<<<< HEAD
=======
            broker_class = cls._brokers[broker_type]
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            broker = broker_class(**kwargs)
            logger.info(f"Created {broker_type} broker")
            return broker
        except Exception as e:
            logger.error(f"Failed to create {broker_type} broker: {e}")
            return None

    @classmethod
    def get_available_brokers(cls) -> list[str]:
        """Get list of available broker types."""
<<<<<<< HEAD
<<<<<<< HEAD
        return list(cls._brokers.keys()) + list(cls._dynamic_brokers.keys())
=======
        return list(cls._brokers.keys())
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
        return list(cls._brokers.keys()) + list(cls._dynamic_brokers.keys())
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    @classmethod
    def register_broker(cls, name: str, broker_class: type) -> None:
        """Register a new broker type."""
        cls._brokers[name] = broker_class
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        logger.info(f"Registered broker: {name}")
    def register_broker(cls, name: str, broker_class: type) -> None:
        """Register a new broker type."""
        cls._brokers[name] = broker_class
<<<<<<< HEAD
=======
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        logger.info(f"Registered broker: {name}")