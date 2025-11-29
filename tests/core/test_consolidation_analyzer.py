"""
Unit tests for consolidation/consolidation_analyzer.py - HIGH PRIORITY

Tests ConsolidationAnalyzer class functionality.
Note: Maps to tools/repo_consolidation_analyzer.py RepoConsolidationAnalyzer.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path
import tempfile

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the analyzer (closest match)
from tools.repo_consolidation_analyzer import RepoConsolidationAnalyzer

# Alias for test purposes
ConsolidationAnalyzer = RepoConsolidationAnalyzer


class TestConsolidationAnalyzer:
    """Test suite for ConsolidationAnalyzer class."""

    @pytest.fixture
    def analyzer(self, tmp_path):
        """Create a ConsolidationAnalyzer instance."""
        analysis_dir = tmp_path / "analysis"
        analysis_dir.mkdir()
        return ConsolidationAnalyzer(str(analysis_dir))

    def test_initialization(self, tmp_path):
        """Test ConsolidationAnalyzer initialization."""
        analysis_dir = tmp_path / "analysis"
        analyzer = ConsolidationAnalyzer(str(analysis_dir))
        
        assert analyzer.analysis_dir == Path(analysis_dir)
        assert analyzer.repos == {}
        assert analyzer.similarity_groups == {}

    def test_initialization_default(self):
        """Test initialization with default directory."""
        analyzer = ConsolidationAnalyzer()
        
        assert analyzer.analysis_dir is not None

    def test_load_all_repos_empty_directory(self, analyzer):
        """Test load_all_repos with empty directory."""
        repos = analyzer.load_all_repos()
        
        assert repos == {}

    def test_load_all_repos_with_files(self, analyzer, tmp_path):
        """Test load_all_repos with analysis files."""
        analysis_file = analyzer.analysis_dir / "test_repo.md"
        analysis_file.write_text("# Test Repo\nAgent: Agent-1\nPurpose: Testing")
        
        repos = analyzer.load_all_repos()
        
        assert len(repos) > 0

    def test_extract_repo_name_from_title(self, analyzer):
        """Test _extract_repo_name with title pattern."""
        content = "# My Repository Analysis"
        filename = "test.md"
        
        name = analyzer._extract_repo_name(content, filename)
        
        assert "My Repository" in name or "Repository" in name

    def test_extract_repo_name_from_filename(self, analyzer):
        """Test _extract_repo_name from filename pattern."""
        content = "Some content"
        # Use filename that will use fallback mechanism
        filename = "simple_name.md"
        
        name = analyzer._extract_repo_name(content, filename)
        
        # Should return fallback extracted from filename
        assert isinstance(name, str)
        assert len(name) > 0

    def test_extract_agent(self, analyzer):
        """Test _extract_agent method."""
        content = "Agent-2 analyzed this repo"
        
        agent = analyzer._extract_agent(content)
        
        assert agent == "Agent-2"

    def test_extract_agent_not_found(self, analyzer):
        """Test _extract_agent when agent not found."""
        content = "No agent mentioned"
        
        agent = analyzer._extract_agent(content)
        
        assert agent == "Unknown"

    def test_extract_purpose(self, analyzer):
        """Test _extract_purpose method."""
        content = "Purpose: This repo does something"
        
        purpose = analyzer._extract_purpose(content)
        
        assert len(purpose) > 0
        assert purpose != "Unknown"

    def test_extract_tech_stack(self, analyzer):
        """Test _extract_tech_stack method."""
        content = "Uses Python, FastAPI, and Discord.py"
        
        tech_stack = analyzer._extract_tech_stack(content)
        
        assert "Python" in tech_stack or "Discord.py" in tech_stack

    def test_extract_category(self, analyzer):
        """Test _extract_category method."""
        content = "This is a trading bot repository"
        
        category = analyzer._extract_category(content)
        
        assert category == "trading"

    def test_find_similar_repos_empty(self, analyzer):
        """Test find_similar_repos with no repos."""
        repos = {}
        analyzer.repos = repos
        
        similar = analyzer.find_similar_repos()
        
        assert similar == {}

    def test_generate_consolidation_report(self, analyzer):
        """Test generate_consolidation_report method."""
        analyzer.repos = {
            "repo1.md": {
                "name": "Repo1",
                "category": "trading",
                "tech_stack": ["Python"]
            },
            "repo2.md": {
                "name": "Repo2",
                "category": "trading",
                "tech_stack": ["Python"]
            }
        }
        
        report = analyzer.generate_consolidation_report()
        
        assert "total_repos" in report
        assert "consolidation_groups" in report
        assert "candidates" in report

    def test_parse_repo_analysis(self, analyzer):
        """Test _parse_repo_analysis method."""
        content = "# Test Repo\nAgent-1\nPurpose: Testing"
        filename = "test.md"
        
        repo_data = analyzer._parse_repo_analysis(content, filename)
        
        assert repo_data is not None
        assert "name" in repo_data
        assert "agent" in repo_data

