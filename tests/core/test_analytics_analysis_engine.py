"""
Tests for Analysis Core Engine - Comprehensive Test Suite
=========================================================

Tests the AnalysisCoreEngine class with comprehensive coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-30
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import Any

# Import directly to avoid registry import issues
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.core.engines.analysis_core_engine import AnalysisCoreEngine
from src.core.engines.contracts import EngineContext, EngineResult


class TestAnalysisCoreEngine:
    """Test suite for AnalysisCoreEngine."""

    @pytest.fixture
    def engine(self):
        """Create AnalysisCoreEngine instance."""
        return AnalysisCoreEngine()

    @pytest.fixture
    def mock_context(self):
        """Create mock EngineContext."""
        context = Mock(spec=EngineContext)
        context.logger = Mock()
        context.logger.info = Mock()
        context.logger.error = Mock()
        return context

    def test_initialization(self, engine):
        """Test engine initialization."""
        assert engine.patterns == {}
        assert engine.violations == []
        assert engine.is_initialized is False

    def test_initialize_success(self, engine, mock_context):
        """Test successful initialization."""
        result = engine.initialize(mock_context)
        assert result is True
        assert engine.is_initialized is True
        mock_context.logger.info.assert_called_once()

    def test_initialize_failure(self, engine, mock_context):
        """Test initialization failure handling."""
        mock_context.logger.info.side_effect = Exception("Init error")
        result = engine.initialize(mock_context)
        assert result is False
        mock_context.logger.error.assert_called_once()

    def test_execute_analyze_operation(self, engine, mock_context):
        """Test execute with analyze operation."""
        payload = {"operation": "analyze", "content": "test content", "type": "general"}
        result = engine.execute(mock_context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is True

    def test_execute_extract_patterns_operation(self, engine, mock_context):
        """Test execute with extract_patterns operation."""
        payload = {"operation": "extract_patterns", "content": "def test(): pass", "pattern_type": "code"}
        result = engine.execute(mock_context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "patterns" in result.data

    def test_execute_detect_violations_operation(self, engine, mock_context):
        """Test execute with detect_violations operation."""
        payload = {"operation": "detect_violations", "content": "x" * 400, "violation_type": "general"}
        result = engine.execute(mock_context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is True

    def test_execute_unknown_operation(self, engine, mock_context):
        """Test execute with unknown operation."""
        payload = {"operation": "unknown_op"}
        result = engine.execute(mock_context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is False
        assert "Unknown" in result.error

    def test_execute_exception_handling(self, engine, mock_context):
        """Test execute exception handling."""
        payload = {"operation": "analyze"}
        with patch.object(engine, 'analyze', side_effect=Exception("Test error")):
            result = engine.execute(mock_context, payload)
            assert isinstance(result, EngineResult)
            assert result.success is False

    def test_analyze_success(self, engine, mock_context):
        """Test analyze method success."""
        data = {"content": "test content", "type": "general"}
        result = engine.analyze(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "content_length" in result.data
        assert result.data["analysis_type"] == "general"

    def test_analyze_empty_content(self, engine, mock_context):
        """Test analyze with empty content."""
        data = {"content": "", "type": "general"}
        result = engine.analyze(mock_context, data)
        assert result.success is True
        assert result.data["content_length"] == 0

    def test_analyze_exception_handling(self, engine, mock_context):
        """Test analyze exception handling."""
        data = {"content": None}
        result = engine.analyze(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_extract_patterns_success(self, engine, mock_context):
        """Test extract_patterns method success."""
        content = "def test(): pass\nclass Test: pass\nimport os"
        data = {"content": content, "pattern_type": "code"}
        result = engine.extract_patterns(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert len(result.data["patterns"]) == 3
        assert engine.patterns["code"] == result.data["patterns"]

    def test_extract_patterns_empty_content(self, engine, mock_context):
        """Test extract_patterns with empty content."""
        data = {"content": "", "pattern_type": "code"}
        result = engine.extract_patterns(mock_context, data)
        assert result.success is True
        assert len(result.data["patterns"]) == 3

    def test_extract_patterns_exception_handling(self, engine, mock_context):
        """Test extract_patterns exception handling."""
        data = {"content": None}
        result = engine.extract_patterns(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_detect_violations_line_count(self, engine, mock_context):
        """Test detect_violations with line count violation."""
        content = "x" * 400
        data = {"content": content, "violation_type": "general"}
        result = engine.detect_violations(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert len(result.data["violations"]) > 0
        assert any(v["type"] == "line_count" for v in result.data["violations"])

    def test_detect_violations_class_count(self, engine, mock_context):
        """Test detect_violations with class count violation."""
        content = "\n".join(["class Test{}: pass"] * 10)
        data = {"content": content, "violation_type": "general"}
        result = engine.detect_violations(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert any(v["type"] == "class_count" for v in result.data["violations"])

    def test_detect_violations_no_violations(self, engine, mock_context):
        """Test detect_violations with no violations."""
        content = "x" * 100
        data = {"content": content, "violation_type": "general"}
        result = engine.detect_violations(mock_context, data)
        assert result.success is True
        assert len(result.data["violations"]) == 0

    def test_detect_violations_exception_handling(self, engine, mock_context):
        """Test detect_violations exception handling."""
        data = {"content": None}
        result = engine.detect_violations(mock_context, data)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_cleanup_success(self, engine, mock_context):
        """Test cleanup method success."""
        engine.patterns = {"test": []}
        engine.violations = [{"type": "test"}]
        engine.is_initialized = True
        result = engine.cleanup(mock_context)
        assert result is True
        assert len(engine.patterns) == 0
        assert len(engine.violations) == 0
        assert engine.is_initialized is False

    def test_cleanup_exception_handling(self, engine, mock_context):
        """Test cleanup exception handling."""
        mock_context.logger.info.side_effect = Exception("Cleanup error")
        result = engine.cleanup(mock_context)
        assert result is False
        mock_context.logger.error.assert_called_once()

    def test_get_status(self, engine):
        """Test get_status method."""
        engine.is_initialized = True
        engine.patterns = {"test": []}
        engine.violations = [{"type": "test"}]
        status = engine.get_status()
        assert status["initialized"] is True
        assert status["patterns_count"] == 1
        assert status["violations_count"] == 1

    def test_get_status_not_initialized(self, engine):
        """Test get_status when not initialized."""
        status = engine.get_status()
        assert status["initialized"] is False
        assert status["patterns_count"] == 0
        assert status["violations_count"] == 0

