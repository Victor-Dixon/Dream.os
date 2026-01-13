"""
Integration Tests - Analysis Endpoints
=======================================

Tests for unified analysis tool web integration endpoints.

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


class TestAnalysisEndpoints:
    """Test analysis API endpoints."""

    def test_analysis_health_endpoint(self, client):
        """Test analysis health check endpoint."""
        response = client.get('/api/analysis/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['service'] == 'analysis'

    def test_analysis_categories_endpoint(self, client):
        """Test get analysis categories endpoint."""
        response = client.get('/api/analysis/categories')
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'categories' in data['data']
        assert 'count' in data['data']
        assert isinstance(data['data']['categories'], list)
        assert len(data['data']['categories']) > 0

    @patch('src.web.analysis_handlers.UnifiedAnalyzer.analyze_project_structure')
    def test_analyze_structure_endpoint(self, mock_analyze, client):
        """Test project structure analysis endpoint."""
        mock_analyze.return_value = {
            "structure": {},
            "total_files": 100,
            "total_dirs": 10
        }
        response = client.post('/api/analysis/analyze', json={
            "category": "structure"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'category' in data['data']
        assert 'analysis' in data['data']

    def test_analyze_file_missing_file(self, client):
        """Test file analysis with missing file."""
        response = client.post('/api/analysis/analyze', json={
            "category": "file"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('src.web.analysis_handlers.UnifiedAnalyzer.analyze_file')
    def test_analyze_file_success(self, mock_analyze, client):
        """Test file analysis success."""
        mock_analyze.return_value = {
            "file_path": "test.py",
            "language": ".py",
            "functions": ["test_func"],
            "line_count": 50
        }
        response = client.post('/api/analysis/analyze', json={
            "category": "file",
            "file": "test.py"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert data['data']['category'] == 'file'

    def test_repository_analysis_missing_repos(self, client):
        """Test repository analysis with missing repos."""
        response = client.post('/api/analysis/repository', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('src.web.analysis_handlers.UnifiedAnalyzer.analyze_repository')
    def test_repository_analysis_success(self, mock_analyze, client):
        """Test repository analysis success."""
        mock_analyze.return_value = {
            "name": "test-repo",
            "path": "/path/to/repo",
            "exists": True,
            "python_files": 10
        }
        response = client.post('/api/analysis/repository', json={
            "repos": "test-repo"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'repositories' in data['data']
        assert 'count' in data['data']

    def test_analyze_invalid_category(self, client):
        """Test analysis with invalid category."""
        response = client.post('/api/analysis/analyze', json={
            "category": "invalid_category"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data



