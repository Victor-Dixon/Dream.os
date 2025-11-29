"""
Tests for strategy_coordinator.py

Comprehensive tests for strategy coordination, pattern matching, and routing.
Target: 10+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.services.coordination.strategy_coordinator import StrategyCoordinator
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)
# Note: Source files import from ..models.messaging_models which doesn't exist
# This is a known issue - tests use correct import path


class TestStrategyCoordinator:
    """Tests for StrategyCoordinator."""

    def test_initialization(self):
        """Test coordinator initialization."""
        coordinator = StrategyCoordinator()
        assert coordinator.coordination_rules is not None
        assert coordinator.routing_table is not None

    def test_initialize_coordination_rules(self):
        """Test coordination rules initialization."""
        coordinator = StrategyCoordinator()
        rules = coordinator.coordination_rules
        
        assert "priority_routing" in rules
        assert "type_routing" in rules
        assert "sender_routing" in rules
        assert UnifiedMessagePriority.URGENT in rules["priority_routing"]
        assert UnifiedMessageType.ONBOARDING in rules["type_routing"]
        assert SenderType.CAPTAIN in rules["sender_routing"]

    def test_initialize_routing_table(self):
        """Test routing table initialization."""
        coordinator = StrategyCoordinator()
        routing = coordinator.routing_table
        
        assert "captain_priority" in routing
        assert "urgent_delivery" in routing
        assert "system_priority" in routing
        assert "broadcast_delivery" in routing
        assert "standard_delivery" in routing

    def test_determine_coordination_strategy_captain_priority(self):
        """Test strategy determination for captain priority."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Captain Agent-4",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.CAPTAIN,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        assert strategy == "captain_priority"

    def test_determine_coordination_strategy_urgent(self):
        """Test strategy determination for urgent priority."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        assert strategy == "urgent_delivery"

    def test_determine_coordination_strategy_system_priority(self):
        """Test strategy determination for system priority type."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="System",
            recipient="Agent-6",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.SYSTEM,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        assert strategy == "system_priority"

    def test_determine_coordination_strategy_broadcast(self):
        """Test strategy determination for broadcast type."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="all",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        assert strategy == "broadcast_delivery"

    def test_determine_coordination_strategy_standard(self):
        """Test strategy determination for standard delivery."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        assert strategy == "standard_delivery"

    def test_apply_coordination_rules_urgent_priority(self):
        """Test applying coordination rules for urgent priority."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        strategy = "urgent_delivery"
        result = coordinator.apply_coordination_rules(message, strategy)
        
        assert result["strategy"] == "urgent_delivery"
        assert "urgent_priority" in result["rules_applied"]
        assert "routing_config" in result
        assert "estimated_delivery_time" in result

    def test_apply_coordination_rules_onboarding_type(self):
        """Test applying coordination rules for onboarding type."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="System",
            recipient="Agent-6",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.SYSTEM,
        )
        strategy = "system_priority"
        result = coordinator.apply_coordination_rules(message, strategy)
        
        assert "onboarding_priority" in result["rules_applied"]
        assert "system_priority" in result["rules_applied"]

    def test_apply_coordination_rules_broadcast_type(self):
        """Test applying coordination rules for broadcast type."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="all",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        strategy = "broadcast_delivery"
        result = coordinator.apply_coordination_rules(message, strategy)
        
        assert "broadcast_priority" in result["rules_applied"]

    def test_apply_coordination_rules_captain_sender(self):
        """Test applying coordination rules for captain sender."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Captain Agent-4",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.CAPTAIN,
        )
        strategy = "captain_priority"
        result = coordinator.apply_coordination_rules(message, strategy)
        
        assert "captain_priority" in result["rules_applied"]

    def test_apply_coordination_rules_system_sender(self):
        """Test applying coordination rules for system sender."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="System",
            recipient="Agent-6",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.SYSTEM,
        )
        strategy = "system_priority"
        result = coordinator.apply_coordination_rules(message, strategy)
        
        assert "system_priority" in result["rules_applied"]

    def test_estimate_delivery_time_captain_priority(self):
        """Test delivery time estimation for captain priority."""
        coordinator = StrategyCoordinator()
        time = coordinator._estimate_delivery_time("captain_priority")
        assert time == 0.1

    def test_estimate_delivery_time_urgent(self):
        """Test delivery time estimation for urgent."""
        coordinator = StrategyCoordinator()
        time = coordinator._estimate_delivery_time("urgent_delivery")
        assert time == 0.2

    def test_estimate_delivery_time_standard(self):
        """Test delivery time estimation for standard."""
        coordinator = StrategyCoordinator()
        time = coordinator._estimate_delivery_time("standard_delivery")
        assert time == 0.5

    def test_estimate_delivery_time_unknown_strategy(self):
        """Test delivery time estimation for unknown strategy."""
        coordinator = StrategyCoordinator()
        time = coordinator._estimate_delivery_time("unknown_strategy")
        assert time == 0.5  # Default

    def test_get_coordination_rules(self):
        """Test getting coordination rules."""
        coordinator = StrategyCoordinator()
        rules = coordinator.get_coordination_rules()
        
        assert isinstance(rules, dict)
        assert "priority_routing" in rules
        # Should be a copy, not the same object
        assert rules is not coordinator.coordination_rules

    def test_get_routing_table(self):
        """Test getting routing table."""
        coordinator = StrategyCoordinator()
        routing = coordinator.get_routing_table()
        
        assert isinstance(routing, dict)
        assert "captain_priority" in routing
        # Should be a copy, not the same object
        assert routing is not coordinator.routing_table

    def test_update_coordination_rule_success(self):
        """Test updating coordination rule successfully."""
        coordinator = StrategyCoordinator()
        result = coordinator.update_coordination_rule(
            "priority_routing",
            UnifiedMessagePriority.URGENT,
            "new_value"
        )
        assert result is True
        assert coordinator.coordination_rules["priority_routing"][UnifiedMessagePriority.URGENT] == "new_value"

    def test_update_coordination_rule_failure(self):
        """Test updating coordination rule with invalid rule type."""
        coordinator = StrategyCoordinator()
        result = coordinator.update_coordination_rule(
            "invalid_rule_type",
            "key",
            "value"
        )
        assert result is False

    def test_update_routing_config_success(self):
        """Test updating routing config successfully."""
        coordinator = StrategyCoordinator()
        result = coordinator.update_routing_config(
            "captain_priority",
            {"new_key": "new_value"}
        )
        assert result is True
        assert coordinator.routing_table["captain_priority"]["new_key"] == "new_value"

    def test_update_routing_config_failure(self):
        """Test updating routing config with invalid strategy."""
        coordinator = StrategyCoordinator()
        result = coordinator.update_routing_config(
            "invalid_strategy",
            {"key": "value"}
        )
        assert result is False

    def test_get_coordinator_status(self):
        """Test getting coordinator status."""
        coordinator = StrategyCoordinator()
        status = coordinator.get_coordinator_status()
        
        assert "coordination_rules_count" in status
        assert "routing_strategies_count" in status
        assert "available_strategies" in status
        assert isinstance(status["available_strategies"], list)
        assert len(status["available_strategies"]) > 0

    def test_determine_strategy_complex_priority_override(self):
        """Test strategy determination with complex priority override scenarios."""
        coordinator = StrategyCoordinator()
        # Captain with regular priority should still get captain_priority
        message = UnifiedMessage(
            content="test",
            sender="Captain Agent-4",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.CAPTAIN,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        assert strategy == "captain_priority"

    def test_apply_rules_with_all_priority_flags(self):
        """Test applying rules when message has all priority flags."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Captain Agent-4",
            recipient="Agent-6",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.CAPTAIN,
        )
        strategy = "captain_priority"
        result = coordinator.apply_coordination_rules(message, strategy)
        
        assert "urgent_priority" in result["rules_applied"]
        assert "onboarding_priority" in result["rules_applied"]
        assert "captain_priority" in result["rules_applied"]

    def test_routing_config_structure(self):
        """Test that routing config has expected structure."""
        coordinator = StrategyCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        strategy = coordinator.determine_coordination_strategy(message)
        result = coordinator.apply_coordination_rules(message, strategy)
        
        routing_config = result["routing_config"]
        assert "delivery_method" in routing_config
        assert "retry_attempts" in routing_config
        assert "timeout" in routing_config

    def test_estimate_delivery_time_all_strategies(self):
        """Test delivery time estimation for all strategies."""
        coordinator = StrategyCoordinator()
        strategies = [
            "captain_priority",
            "urgent_delivery",
            "system_priority",
            "broadcast_delivery",
            "standard_delivery",
        ]
        for strategy in strategies:
            time_est = coordinator._estimate_delivery_time(strategy)
            assert isinstance(time_est, float)
            assert time_est >= 0

    def test_update_coordination_rule_preserves_other_rules(self):
        """Test that updating one rule doesn't affect others."""
        coordinator = StrategyCoordinator()
        original_rules = coordinator.get_coordination_rules()
        coordinator.update_coordination_rule(
            "priority_routing",
            UnifiedMessagePriority.URGENT,
            "new_value"
        )
        updated_rules = coordinator.get_coordination_rules()
        
        # Other rule types should be unchanged
        assert updated_rules["type_routing"] == original_rules["type_routing"]
        assert updated_rules["sender_routing"] == original_rules["sender_routing"]

    def test_update_routing_config_preserves_existing_keys(self):
        """Test that updating routing config preserves existing keys."""
        coordinator = StrategyCoordinator()
        original_config = coordinator.routing_table["captain_priority"].copy()
        coordinator.update_routing_config(
            "captain_priority",
            {"new_key": "new_value"}
        )
        updated_config = coordinator.routing_table["captain_priority"]
        
        # Existing keys should be preserved
        assert updated_config["delivery_method"] == original_config["delivery_method"]
        assert updated_config["retry_attempts"] == original_config["retry_attempts"]
        assert updated_config["new_key"] == "new_value"

