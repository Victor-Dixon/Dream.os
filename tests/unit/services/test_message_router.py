"""
Unit tests for message_router.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Mock dependencies before import
import sys
from unittest.mock import MagicMock
sys.modules['src.services.protocol.routers.route_analyzer'] = MagicMock()
from src.core.messaging_models_core import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    SenderType, RecipientType
)
from src.services.protocol.messaging_protocol_models import ProtocolOptimizationStrategy
from src.services.protocol.message_router import MessageRouter


class TestMessageRouter:
    """Test suite for MessageRouter."""

    @pytest.fixture
    def router(self):
        """Create MessageRouter instance."""
        return MessageRouter()

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

    def test_router_initialization(self, router):
        """Test router initializes correctly."""
        assert router is not None
        assert router.config is not None
        assert router.analyzer is not None
        assert router.route_cache == {}
        assert router.failed_routes == {}

    def test_route_message_urgent_priority(self, router, sample_message):
        """Test routing urgent priority message."""
        sample_message.priority = UnifiedMessagePriority.URGENT
        
        with patch.object(router.analyzer, 'analyze_route_options', return_value=Mock(value="priority")):
            route = router.route_message(sample_message)
            
            assert route is not None

    def test_route_message_broadcast_type(self, router, sample_message):
        """Test routing broadcast message type."""
        sample_message.message_type = UnifiedMessageType.BROADCAST
        
        with patch.object(router.analyzer, 'analyze_route_options', return_value=Mock(value="broadcast")):
            route = router.route_message(sample_message)
            
            assert route is not None

    def test_route_with_priority_override(self, router, sample_message):
        """Test routing with priority override."""
        with patch.object(router, 'route_message', return_value=Mock(value="urgent")):
            route = router.route_with_priority(sample_message, UnifiedMessagePriority.URGENT)
            
            assert route is not None

    def test_route_with_strategy(self, router, sample_message):
        """Test routing with specific strategy."""
        strategy = ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION
        
        with patch.object(router, 'route_message', return_value=Mock(value="optimized")):
            route = router.route_with_strategy(sample_message, strategy)
            
            assert route is not None

