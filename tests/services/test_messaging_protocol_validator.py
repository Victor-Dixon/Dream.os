"""
Tests for protocol/protocol_validator.py

Comprehensive tests for protocol validation, compliance checking, and error formatting.
Target: 10+ test methods, ≥85% coverage
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
    """Tests for ProtocolValidator class."""

    def test_initialization(self):
        """Test validator initialization."""
        validator = ProtocolValidator()
        assert validator.logger is not None

    def test_validate_protocol_success(self):
        """Test validating valid protocol data."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": "1.0",
            "type": "messaging"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_protocol_missing_version(self):
        """Test validating protocol missing version."""
        validator = ProtocolValidator()
        protocol_data = {
            "type": "messaging"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert any("version" in error.lower() for error in errors)

    def test_validate_protocol_missing_type(self):
        """Test validating protocol missing type."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": "1.0"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert any("type" in error.lower() for error in errors)

    def test_validate_protocol_version_int(self):
        """Test validating protocol with integer version."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": 1,
            "type": "messaging"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is True

    def test_validate_protocol_version_string_numeric(self):
        """Test validating protocol with numeric string version."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": "1.0",
            "type": "messaging"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is True

    def test_validate_protocol_version_invalid_type(self):
        """Test validating protocol with invalid version type."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": ["1", "0"],
            "type": "messaging"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert any("version" in error.lower() for error in errors)

    def test_validate_protocol_version_non_numeric_string(self):
        """Test validating protocol with non-numeric string version."""
        validator = ProtocolValidator()
        protocol_data = {
            "version": "v1.0",
            "type": "messaging"
        }
        
        is_valid, errors = validator.validate_protocol(protocol_data)
        
        assert is_valid is False
        assert any("numeric" in error.lower() for error in errors)

    def test_validate_message_success(self):
        """Test validating valid message."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test content",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        message.message_id = str(uuid.uuid4())
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_message_missing_content(self):
        """Test validating message missing content."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("content" in error.lower() for error in errors)

    def test_validate_message_missing_sender(self):
        """Test validating message missing sender."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test",
            sender="",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("sender" in error.lower() for error in errors)

    def test_validate_message_missing_recipient(self):
        """Test validating message missing recipient."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("recipient" in error.lower() for error in errors)

    def test_validate_message_invalid_type(self):
        """Test validating message with invalid type."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        # Manually set invalid type
        message.message_type = "invalid_type"  # type: ignore
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("type" in error.lower() for error in errors)

    def test_validate_message_invalid_priority(self):
        """Test validating message with invalid priority."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        # Manually set invalid priority
        message.priority = "invalid_priority"  # type: ignore
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("priority" in error.lower() for error in errors)

    def test_validate_message_invalid_id_format(self):
        """Test validating message with invalid ID format."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        message.message_id = "not-a-uuid"
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is False
        assert any("id" in error.lower() or "uuid" in error.lower() for error in errors)

    def test_validate_message_valid_uuid(self):
        """Test validating message with valid UUID."""
        validator = ProtocolValidator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        message.message_id = str(uuid.uuid4())
        
        is_valid, errors = validator.validate_message(message)
        
        assert is_valid is True

    def test_validate_route_success(self):
        """Test validating valid route."""
        validator = ProtocolValidator()
        route = MessageRoute.DIRECT
        
        is_valid, errors = validator.validate_route(route)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_route_invalid_type(self):
        """Test validating route with invalid type."""
        validator = ProtocolValidator()
        invalid_route = "not_a_route"  # type: ignore
        
        is_valid, errors = validator.validate_route(invalid_route)  # type: ignore
        
        assert is_valid is False
        assert any("type" in error.lower() for error in errors)

    def test_validation_errors_empty(self):
        """Test formatting errors when no errors."""
        validator = ProtocolValidator()
        result = validator.validation_errors([])
        
        assert result == "No errors"

    def test_validation_errors_single(self):
        """Test formatting single error."""
        validator = ProtocolValidator()
        result = validator.validation_errors(["Missing field: version"])
        
        assert "Missing field: version" in result

    def test_validation_errors_multiple(self):
        """Test formatting multiple errors."""
        validator = ProtocolValidator()
        errors = ["Missing field: version", "Invalid type", "Missing required field"]
        result = validator.validation_errors(errors)
        
        assert "Missing field: version" in result
        assert "Invalid type" in result
        assert "Missing required field" in result

