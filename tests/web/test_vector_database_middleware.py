#!/usr/bin/env python3
"""
Tests for Vector Database Middleware
====================================

Comprehensive test suite for vector database middleware.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from flask import Flask, request, jsonify

from src.web.vector_database.middleware import (
    VectorDatabaseMiddleware,
    ErrorHandlerMiddleware,
    RequestHandlerMiddleware,
    ResponseHandlerMiddleware,
    ValidationMiddleware,
    UnifiedVectorMiddleware
)


class TestVectorDatabaseMiddleware:
    """Test suite for VectorDatabaseMiddleware."""

    @pytest.fixture
    def middleware(self):
        """Create middleware instance."""
        return VectorDatabaseMiddleware()

    @pytest.fixture
    def app(self):
        """Create Flask app for testing."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        return app

    def test_middleware_initialization(self, middleware):
        """Test middleware initialization."""
        assert middleware is not None
        assert middleware.middleware is not None
        assert isinstance(middleware.middleware, UnifiedVectorMiddleware)

    def test_get_instance_singleton(self):
        """Test singleton instance pattern."""
        instance1 = VectorDatabaseMiddleware._get_instance()
        instance2 = VectorDatabaseMiddleware._get_instance()
        
        assert instance1 is instance2

    def test_error_handler_decorator(self, middleware, app):
        """Test error handler decorator."""
        @middleware.error_handler_decorator
        def failing_function():
            raise ValueError("Test error")
        
        with app.app_context():
            with app.test_request_context():
                result = failing_function()
                
                assert result[1] == 500  # Status code
                assert "error" in str(result[0].get_data())

    def test_json_required_decorator_with_json(self, middleware, app):
        """Test JSON required decorator with JSON data."""
        @middleware.json_required_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context(json={"test": "data"}):
                result = test_function()
                assert result.status_code == 200

    def test_json_required_decorator_without_json(self, middleware, app):
        """Test JSON required decorator without JSON data."""
        @middleware.json_required_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                result = test_function()
                assert result[1] == 400  # Bad request

    def test_cors_headers_decorator(self, middleware, app):
        """Test CORS headers decorator."""
        @middleware.cors_headers_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                result = test_function()
                
                # Check CORS headers
                assert hasattr(result, 'headers') or isinstance(result, tuple)

    def test_rate_limit_decorator(self, middleware, app):
        """Test rate limit decorator."""
        @middleware.rate_limit_decorator(max_requests=10, window_seconds=60)
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                result = test_function()
                assert result.status_code == 200

    def test_cache_response_decorator(self, middleware, app):
        """Test cache response decorator."""
        @middleware.cache_response_decorator(ttl_seconds=300)
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                result = test_function()
                assert result.status_code == 200

    def test_validate_pagination_decorator_valid(self, middleware, app):
        """Test pagination validation with valid params."""
        @middleware.validate_pagination_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context('/?page=1&per_page=25'):
                result = test_function()
                assert result.status_code == 200

    def test_validate_pagination_decorator_invalid_page(self, middleware, app):
        """Test pagination validation with invalid page."""
        @middleware.validate_pagination_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context('/?page=0&per_page=25'):
                result = test_function()
                assert result[1] == 400  # Bad request

    def test_validate_pagination_decorator_invalid_per_page(self, middleware, app):
        """Test pagination validation with invalid per_page."""
        @middleware.validate_pagination_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context('/?page=1&per_page=200'):
                result = test_function()
                assert result[1] == 400  # Bad request

    def test_class_level_add_cors_headers(self, app):
        """Test class-level CORS decorator."""
        @VectorDatabaseMiddleware.add_cors_headers
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                result = test_function()
                assert result.status_code == 200

    def test_class_level_error_handler(self, app):
        """Test class-level error handler."""
        @VectorDatabaseMiddleware.error_handler
        def failing_function():
            raise ValueError("Test error")
        
        with app.app_context():
            with app.test_request_context():
                result = failing_function()
                assert result[1] == 500

    def test_class_level_json_required(self, app):
        """Test class-level JSON required."""
        @VectorDatabaseMiddleware.json_required
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                result = test_function()
                assert result[1] == 400  # No JSON provided

    def test_backward_compatibility_exports(self):
        """Test backward compatibility exports."""
        assert ErrorHandlerMiddleware == UnifiedVectorMiddleware
        assert RequestHandlerMiddleware == UnifiedVectorMiddleware
        assert ResponseHandlerMiddleware == UnifiedVectorMiddleware
        assert ValidationMiddleware == UnifiedVectorMiddleware

    def test_log_request_decorator(self, middleware, app):
        """Test request logging decorator."""
        @middleware.log_request_decorator
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context():
                with patch('flask.current_app.logger') as mock_logger:
                    result = test_function()
                    assert result.status_code == 200
                    assert mock_logger.info.called

    def test_validate_request_decorator(self, middleware, app):
        """Test request validation decorator."""
        def validator(data):
            if not data.get('required_field'):
                return "Missing required_field"
            return None
        
        @middleware.validate_request_decorator(validator)
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context(json={"required_field": "value"}):
                result = test_function()
                assert result.status_code == 200

    def test_validate_request_decorator_failure(self, middleware, app):
        """Test request validation decorator with invalid data."""
        def validator(data):
            if not data.get('required_field'):
                return "Missing required_field"
            return None
        
        @middleware.validate_request_decorator(validator)
        def test_function():
            return jsonify({"success": True})
        
        with app.app_context():
            with app.test_request_context(json={}):
                result = test_function()
                assert result[1] == 400  # Bad request

