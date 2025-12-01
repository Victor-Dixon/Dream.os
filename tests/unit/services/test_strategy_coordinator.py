"""
Unit tests for strategy_coordinator.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.coordination.strategy_coordinator import StrategyCoordinator
from src.core.messaging_models_core import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    SenderType, RecipientType
)


class TestStrategyCoordinator:
    """Test suite for StrategyCoordinator."""

    @pytest.fixture
    def coordinator(self):
        """Create StrategyCoordinator instance."""
        return StrategyCoordinator()

    @pytest.fixture
    def sample_message(self):
        """Create sample message."""
        return UnifiedMessage(
            content="Test",
            recipient="Agent-1",
            sender="System",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            recipient_type=RecipientType.AGENT,
            sender_type=SenderType.SYSTEM
        )

    def test_coordinator_initialization(self, coordinator):
        """Test coordinator initializes correctly."""
        assert coordinator is not None
        assert coordinator.coordination_rules is not None
        assert coordinator.routing_table is not None

    def test_determine_strategy_priority_urgent(self, coordinator, sample_message):
        """Test strategy determination based on urgent priority."""
        sample_message.priority = UnifiedMessagePriority.URGENT
        
        strategy = coordinator.determine_coordination_strategy(sample_message)
        
        assert strategy is not None
        assert isinstance(strategy, str)

    def test_determine_strategy_captain_sender(self, coordinator, sample_message):
        """Test strategy determination for captain sender."""
        sample_message.sender = SenderType.CAPTAIN
        
        strategy = coordinator.determine_coordination_strategy(sample_message)
        
        assert strategy is not None

    def test_determine_strategy_onboarding_type(self, coordinator, sample_message):
        """Test strategy determination for onboarding message type."""
        sample_message.message_type = UnifiedMessageType.ONBOARDING
        
        strategy = coordinator.determine_coordination_strategy(sample_message)
        
        assert strategy is not None

    def test_apply_coordination_rules_returns_result(self, coordinator, sample_message):
        """Test applying coordination rules returns result."""
        strategy = "standard"
        
        result = coordinator.apply_coordination_rules(sample_message, strategy)
        
        assert result is not None
        assert isinstance(result, dict)

    def test_routing_table_initialized(self, coordinator):
        """Test routing table is properly initialized."""
        assert "standard_delivery" in coordinator.routing_table
        assert "urgent_delivery" in coordinator.routing_table

