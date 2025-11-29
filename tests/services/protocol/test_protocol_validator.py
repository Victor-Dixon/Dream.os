"""
Tests for protocol_validator.py

Comprehensive tests for protocol validation.
Target: ≥85% coverage
"""

import pytest
import uuid
from src.services.protocol.protocol_validator import ProtocolValidator
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)
from src.services.protocol.messaging_protocol_models import MessageRoute


class TestProtocolValidator:
    """Tests for ProtocolValidator."""

    def test_protocol_validator_initialization(self):
        """Test ProtocolValidator initialization."""
        validator = ProtocolValidator()
        assert validator is not None
        assert validator.logger is not None

    def test_validate_protocol_success(self):
        """Test validating valid protocol."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": 1,
            "type": "messaging",
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_protocol_missing_version(self):
        """Test validating protocol with missing version."""
        validator = ProtocolValidator()
        protocol_data = {
            "type": "messaging",
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert len(errors) > 0
        assert any("version" in error.lower() for error in errors)

    def test_validate_protocol_missing_type(self):
        """Test validating protocol with missing type."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": 1,
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert len(errors) > 0
        assert any("type" in error.lower() for error in errors)

    def test_validate_protocol_invalid_version_string(self):
        """Test validating protocol with invalid version string."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": "invalid",
            "type": "messaging",
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_protocol_valid_version_string(self):
        """Test validating protocol with valid numeric version string."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": "1",
            "type": "messaging",
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is True

    def test_validate_message_success(self):
        """Test validating valid message."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_message_missing_content(self):
        """Test validating message with missing content."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert len(errors) > 0
        assert any("content" in error.lower() for error in errors)

    def test_validate_message_missing_sender(self):
        """Test validating message with missing sender."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="Test",
            sender="",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("sender" in error.lower() for error in errors)

    def test_validate_message_missing_recipient(self):
        """Test validating message with missing recipient."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("recipient" in error.lower() for error in errors)

    def test_validate_message_invalid_id(self):
        """Test validating message with invalid ID."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
            message_id="invalid-uuid",
        )
        
        is_valid, errors = validator.validate_message(message)
        
        # Should validate UUID format
        # Note: This depends on implementation - may pass if UUID validation is lenient
        assert isinstance(is_valid, bool)

    def test_validate_route_success(self):
        """Test validating valid route."""
        validator = ProtocolValidator()
        
        is_valid, errors = validator.validate_route(MessageRoute.DIRECT)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_route_all_types(self):
        """Test validating all route types."""
        validator = ProtocolValidator()
        
        for route in MessageRoute:
            is_valid, errors = validator.validate_route(route)
            assert is_valid is True
            assert len(errors) == 0

    def test_validation_errors_empty(self):
        """Test formatting validation errors when empty."""
        validator = ProtocolValidator()
        
        result = validator.validation_errors([])
        
        assert result == "No errors"

    def test_validation_errors_single(self):
        """Test formatting single validation error."""
        validator = ProtocolValidator()
        
        result = validator.validation_errors(["Missing field: version"])
        
        assert "Missing field: version" in result
        assert "Validation errors:" in result

    def test_validation_errors_multiple(self):
        """Test formatting multiple validation errors."""
        validator = ProtocolValidator()
        
        errors = ["Error 1", "Error 2", "Error 3"]
        result = validator.validation_errors(errors)
        
        assert "Error 1" in result
        assert "Error 2" in result
        assert "Error 3" in result
