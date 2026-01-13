"""
Integration Tests - Validation Endpoints
=========================================

Tests for unified validation tool web integration endpoints.

Target: ≥85% coverage, comprehensive endpoint testing.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.web import create_app


@pytest.fixture
def client():
    """Create Flask test client."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestValidationEndpoints:
    """Test validation API endpoints."""

    def test_validation_health_endpoint(self, client):
        """Test validation health check endpoint."""
        response = client.get('/api/validation/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['service'] == 'validation'

    def test_validation_categories_endpoint(self, client):
        """Test get validation categories endpoint."""
        response = client.get('/api/validation/categories')
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'categories' in data['data']
        assert 'count' in data['data']
        assert isinstance(data['data']['categories'], list)
        assert len(data['data']['categories']) > 0

    @patch('src.web.validation_handlers.UnifiedValidator.validate_ssot_config')
    def test_validate_ssot_config_endpoint(self, mock_validate, client):
        """Test SSOT config validation endpoint."""
        mock_validate.return_value = {
            "category": "ssot_config",
            "valid": True,
            "timestamp": "2025-12-07T21:00:00"
        }
        response = client.post('/api/validation/validate', json={
            "category": "ssot_config"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'category' in data['data']
        assert 'validation' in data['data']

    def test_validate_imports_missing_file(self, client):
        """Test import validation with missing file."""
        response = client.post('/api/validation/validate', json={
            "category": "imports"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('src.web.validation_handlers.UnifiedValidator.validate_imports')
    def test_validate_imports_success(self, mock_validate, client):
        """Test import validation success."""
        mock_validate.return_value = {
            "category": "imports",
            "target": "test.py",
            "imports": ["os", "sys"],
            "count": 2
        }
        response = client.post('/api/validation/validate', json={
            "category": "imports",
            "file": "test.py"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert data['data']['category'] == 'imports'

    @patch('src.web.validation_handlers.UnifiedValidator.run_full_validation')
    def test_full_validation_endpoint(self, mock_full, client):
        """Test full validation suite endpoint."""
        mock_full.return_value = {
            "validations": []
        }
        response = client.post('/api/validation/full', json={})
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'full_validation' in data['data']

    def test_validate_invalid_category(self, client):
        """Test validation with invalid category."""
        response = client.post('/api/validation/validate', json={
            "category": "invalid_category"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data




