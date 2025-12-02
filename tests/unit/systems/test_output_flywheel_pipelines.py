"""
Smoke tests for Output Flywheel pipelines.

Author: Agent-1 (Integration & Core Systems Specialist)
V2 Compliant: <300 lines
"""

import json
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from systems.output_flywheel.processors.repo_scanner import scan_repo_to_dict
from systems.output_flywheel.processors.story_extractor import extract_story_from_session
from systems.output_flywheel.processors.readme_generator import generate_readme
from systems.output_flywheel.processors.build_log_generator import generate_build_log
from systems.output_flywheel.processors.social_generator import generate_social_post
from systems.output_flywheel.processors.trade_processor import prepare_trade_journal_context, build_social_trade_summary


@pytest.fixture
def temp_session_dir(tmp_path):
    """Create temporary session directory."""
    session_dir = tmp_path / "sessions"
    session_dir.mkdir()
    return session_dir


@pytest.fixture
def temp_artifacts_dir(tmp_path):
    """Create temporary artifacts directory."""
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()
    return artifacts_dir


@pytest.fixture
def sample_build_session(temp_session_dir):
    """Create sample build session JSON."""
    session_data = {
        "session_id": "test-build-001",
        "session_type": "build",
        "timestamp": "2025-12-02T03:00:00Z",
        "agent_id": "Agent-1",
        "metadata": {
            "duration_minutes": 60,
            "files_changed": 5,
            "commits": 2,
            "lines_added": 150,
            "lines_removed": 20
        },
        "source_data": {
            "repo_path": str(project_root),
            "git_commits": [
                {
                    "hash": "abc123",
                    "message": "Add feature X",
                    "author": "Agent-1",
                    "timestamp": "2025-12-02T02:30:00Z",
                    "files": ["src/feature.py"]
                }
            ]
        },
        "artifacts": {},
        "pipeline_status": {
            "build_artifact": "pending",
            "trade_artifact": "not_applicable",
            "life_aria_artifact": "not_applicable"
        }
    }
    
    session_file = temp_session_dir / "test_build_session.json"
    session_file.write_text(json.dumps(session_data, indent=2))
    return session_file


@pytest.fixture
def sample_trade_session(temp_session_dir):
    """Create sample trade session JSON."""
    session_data = {
        "session_id": "test-trade-001",
        "session_type": "trade",
        "timestamp": "2025-12-02T03:00:00Z",
        "agent_id": "Agent-1",
        "metadata": {
            "duration_minutes": 30,
            "trades_executed": 2,
            "total_pnl": 50.00,
            "win_rate": 100.0
        },
        "source_data": {
            "trades": [
                {
                    "symbol": "AAPL",
                    "action": "buy",
                    "quantity": 5,
                    "price": 175.00,
                    "timestamp": "2025-12-02T02:45:00Z",
                    "profit_loss": 25.00
                },
                {
                    "symbol": "MSFT",
                    "action": "sell",
                    "quantity": 3,
                    "price": 380.00,
                    "timestamp": "2025-12-02T02:50:00Z",
                    "profit_loss": 25.00
                }
            ]
        },
        "artifacts": {},
        "pipeline_status": {
            "build_artifact": "not_applicable",
            "trade_artifact": "pending",
            "life_aria_artifact": "not_applicable"
        }
    }
    
    session_file = temp_session_dir / "test_trade_session.json"
    session_file.write_text(json.dumps(session_data, indent=2))
    return session_file


class TestBuildArtifactPipeline:
    """Smoke tests for build artifact pipeline."""
    
    def test_pipeline_module_imports(self):
        """Test that pipeline module imports correctly."""
        import systems.output_flywheel.pipelines.build_artifact as build_module
        assert build_module is not None
    
    def test_pipeline_runs_without_error(self, sample_build_session, temp_artifacts_dir, monkeypatch):
        """Test that pipeline runs without crashing."""
        # Import the actual function name
        from systems.output_flywheel.pipelines.build_artifact import run_build_pipeline
        
        # Mock output paths
        monkeypatch.setenv("OUTPUT_FLYWHEEL_ARTIFACTS", str(temp_artifacts_dir))
        
        try:
            with open(sample_build_session) as f:
                session_data = json.load(f)
            result = run_build_pipeline(session_data)
            assert result is not None
        except Exception as e:
            pytest.fail(f"Pipeline failed with error: {e}")


class TestTradeArtifactPipeline:
    """Smoke tests for trade artifact pipeline."""
    
    def test_pipeline_module_imports(self):
        """Test that pipeline module imports correctly."""
        import systems.output_flywheel.pipelines.trade_artifact as trade_module
        assert trade_module is not None
    
    def test_pipeline_runs_without_error(self, sample_trade_session, temp_artifacts_dir, monkeypatch):
        """Test that pipeline runs without crashing."""
        # Import the actual function name
        from systems.output_flywheel.pipelines.trade_artifact import run_trade_pipeline
        
        # Mock output paths
        monkeypatch.setenv("OUTPUT_FLYWHEEL_ARTIFACTS", str(temp_artifacts_dir))
        
        try:
            with open(sample_trade_session) as f:
                session_data = json.load(f)
            result = run_trade_pipeline(session_data)
            assert result is not None
        except Exception as e:
            pytest.fail(f"Pipeline failed with error: {e}")


class TestProcessors:
    """Smoke tests for processors."""
    
    def test_repo_scanner_imports(self):
        """Test repo scanner function imports."""
        assert scan_repo_to_dict is not None
    
    def test_story_extractor_imports(self):
        """Test story extractor function imports."""
        assert extract_story_from_session is not None
    
    def test_readme_generator_imports(self):
        """Test readme generator function imports."""
        assert generate_readme is not None
    
    def test_build_log_generator_imports(self):
        """Test build log generator function imports."""
        assert generate_build_log is not None
    
    def test_social_generator_imports(self):
        """Test social generator function imports."""
        assert generate_social_post is not None
    
    def test_trade_processor_imports(self):
        """Test trade processor function imports."""
        assert prepare_trade_journal_context is not None
        assert build_social_trade_summary is not None
    
    def test_repo_scanner_basic(self):
        """Test repo scanner with a basic repo path."""
        result = scan_repo_to_dict(str(project_root))
        assert isinstance(result, dict)
        assert "commits" in result or "error" in result
    
    def test_story_extractor_basic(self):
        """Test story extractor with minimal data."""
        from systems.output_flywheel.processors.story_extractor import StorySummary
        session_data = {
            "session_id": "test",
            "session_type": "build",
            "metadata": {"files_changed": 5}
        }
        result = extract_story_from_session(session_data)
        # Returns StorySummary object, not dict
        assert isinstance(result, StorySummary)
        assert hasattr(result, 'title')
        assert hasattr(result, 'overview')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

