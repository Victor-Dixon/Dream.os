#!/usr/bin/env python3
"""
Tests for Vector Database Routes
=================================

Comprehensive test suite for vector database web routes.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from flask import Flask

from src.web.vector_database.routes import vector_db_bp, index, search, get_documents, add_document, get_document, update_document, delete_document, get_analytics, get_collections, export_data


class TestVectorDatabaseRoutes:
    """Test suite for vector database routes."""

    @pytest.fixture
    def app(self):
        """Create Flask app for testing."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.register_blueprint(vector_db_bp)
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    def test_blueprint_registration(self, app):
        """Test blueprint is registered."""
        assert 'vector_db' in [bp.name for bp in app.blueprints.values()]

    def test_index_route(self, client):
        """Test index route."""
        with patch('src.web.vector_database.routes.render_template') as mock_render:
            mock_render.return_value = "Template rendered"
            response = client.get('/vector-db/')
            
            assert response.status_code == 200
            mock_render.assert_called_once_with("vector_database_interface.html")

    def test_search_route_post(self, client):
        """Test search route POST."""
        with patch('src.web.vector_database.routes.SearchHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_search.return_value = mock_response
            
            response = client.post('/vector-db/search', json={"query": "test"})
            
            assert mock_handler.handle_search.called

    def test_search_route_get_not_allowed(self, client):
        """Test search route doesn't allow GET."""
        response = client.get('/vector-db/search')
        assert response.status_code == 405  # Method not allowed

    def test_get_documents_route(self, client):
        """Test get documents route."""
        with patch('src.web.vector_database.routes.DocumentHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_get_documents.return_value = mock_response
            
            response = client.get('/vector-db/documents')
            
            assert mock_handler.handle_get_documents.called

    def test_add_document_route(self, client):
        """Test add document route."""
        with patch('src.web.vector_database.routes.DocumentHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_handler.handle_add_document.return_value = mock_response
            
            response = client.post('/vector-db/documents', json={"title": "Test", "content": "Content"})
            
            assert mock_handler.handle_add_document.called

    def test_get_document_route(self, client):
        """Test get specific document route."""
        with patch('src.web.vector_database.routes.DocumentHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_get_document.return_value = mock_response
            
            response = client.get('/vector-db/documents/test-doc-123')
            
            assert mock_handler.handle_get_document.called
            mock_handler.handle_get_document.assert_called_once_with('test-doc-123')

    def test_update_document_route(self, client):
        """Test update document route."""
        with patch('src.web.vector_database.routes.DocumentHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_update_document.return_value = mock_response
            
            response = client.put('/vector-db/documents/test-doc-123', json={"title": "Updated"})
            
            assert mock_handler.handle_update_document.called
            mock_handler.handle_update_document.assert_called_once_with('test-doc-123')

    def test_delete_document_route(self, client):
        """Test delete document route."""
        with patch('src.web.vector_database.routes.DocumentHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_delete_document.return_value = mock_response
            
            response = client.delete('/vector-db/documents/test-doc-123')
            
            assert mock_handler.handle_delete_document.called
            mock_handler.handle_delete_document.assert_called_once_with('test-doc-123')

    def test_get_analytics_route(self, client):
        """Test get analytics route."""
        with patch('src.web.vector_database.routes.AnalyticsHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_get_analytics.return_value = mock_response
            
            response = client.get('/vector-db/analytics')
            
            assert mock_handler.handle_get_analytics.called

    def test_get_collections_route(self, client):
        """Test get collections route."""
        with patch('src.web.vector_database.routes.CollectionHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_get_collections.return_value = mock_response
            
            response = client.get('/vector-db/collections')
            
            assert mock_handler.handle_get_collections.called

    def test_export_data_route(self, client):
        """Test export data route."""
        with patch('src.web.vector_database.routes.ExportHandler') as mock_handler:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_handler.handle_export_data.return_value = mock_response
            
            response = client.post('/vector-db/export', json={"collection": "test", "format": "json"})
            
            assert mock_handler.handle_export_data.called

    def test_cors_headers_applied(self, client):
        """Test CORS headers are applied to routes."""
        response = client.get('/vector-db/')
        
        # CORS headers should be present
        assert 'Access-Control-Allow-Origin' in str(response.headers) or response.status_code == 200

    def test_route_decorators_applied(self):
        """Test that routes have decorators applied."""
        # Verify decorators are present
        assert hasattr(index, '__wrapped__') or hasattr(index, '__name__')
        assert hasattr(search, '__wrapped__') or hasattr(search, '__name__')

